import time
import multiprocessing
import numpy as np
from core.engine import DiagnosticModule, Status
from core.sys_interface import SysAdmin

def _numpy_burn(stop_event):
    # Heavy Matrix Math for FPU saturation (Bypasses GIL)
    # Generate random matrices
    a = np.random.rand(600, 600)
    b = np.random.rand(600, 600)
    while not stop_event.is_set():
        np.dot(a, b)

class ThermalModule(DiagnosticModule):
    def __init__(self):
        super().__init__("Thermal Dynamics", critical=True)

    def _get_temp(self):
        try:
            res = SysAdmin.run_powershell("Get-CimInstance MSAcpi_ThermalZoneTemperature | Select-Object CurrentTemperature")
            if res and isinstance(res[0], dict):
                t = int(res[0].get('CurrentTemperature', 0))
                # Convert Deci-Kelvin to Celsius
                return (t / 10.0) - 273.15
        except: pass
        return 0

    def generate_svg(self, history, cool_down):
        all_data = history + cool_down
        if not all_data: return ""
        w, h = 400, 100
        # Dynamic Scaling
        max_t = max(all_data) + 5
        min_t = min(all_data) - 5
        if max_t == min_t: max_t += 1
        
        pts = []
        for i, t in enumerate(all_data):
            x = (i / len(all_data)) * w
            y = h - ((t - min_t) / (max_t - min_t) * h)
            pts.append(f"{x:.1f},{y:.1f}")
        
        # Stress line
        polyline = f'<polyline points="{" ".join(pts)}" fill="none" stroke="#e74c3c" stroke-width="2" />'
        
        # Cool-down marker line
        mid_x = (len(history) / len(all_data)) * w
        marker = f'<line x1="{mid_x}" y1="0" x2="{mid_x}" y2="{h}" stroke="#3498db" stroke-dasharray="4" />'
        
        return f'<svg width="{w}" height="{h}" style="background:#f9f9f9;border:1px solid #ddd">{polyline}{marker}</svg>'

    def run(self, context):
        stop_event = multiprocessing.Event()
        
        # 1. Pre-Flight
        start_temp = self._get_temp()
        if start_temp == 0:
            self.status = Status.INFO
            self.summary = "No Thermal Sensors (Skipping Stress)"
            return

        # 2. Stress Phase
        duration = context.get('config', {}).get('thresholds', {}).get('cpu_stress_sec', 20)
        procs = [multiprocessing.Process(target=_numpy_burn, args=(stop_event,)) for _ in range(multiprocessing.cpu_count())]
        
        for p in procs: p.start()
        
        history = []
        for _ in range(duration):
            history.append(self._get_temp())
            time.sleep(1)
            
        stop_event.set()
        for p in procs: p.join()
        
        # 3. Cool-Down Phase
        cool_down = []
        for _ in range(10):
            cool_down.append(self._get_temp())
            time.sleep(1)

        # 4. Analysis
        peak = max(history)
        drop = peak - cool_down[-1]
        
        self.data['svg_graph'] = self.generate_svg(history, cool_down)
        self.data['peak_temp'] = peak
        self.data['cooldown_drop'] = drop
        
        max_safe = context.get('config', {}).get('thresholds', {}).get('max_safe_temp', 85.0)
        
        if peak > max_safe:
            self.status = Status.FAIL
            self.summary = f"Overheat: {peak:.1f}C"
        elif drop < 3:
            self.status = Status.WARN
            self.summary = f"Poor Cooling (Only dropped {drop:.1f}C)"
        else:
            self.status = Status.PASS
            self.summary = f"Stable: Peak {peak:.1f}C"