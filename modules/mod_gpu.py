from core.engine import DiagnosticModule, Status
from core.sys_interface import SysAdmin

class GpuModule(DiagnosticModule):
    def __init__(self):
        super().__init__("GPU Graphics", critical=True)

    def run(self, context):
        gpus = SysAdmin.run_powershell("Get-CimInstance Win32_VideoController | Select-Object Name, DriverVersion")
        
        if not gpus:
            self.status = Status.FAIL
            self.summary = "No Video Adapter Detected"
            return
            
        names = []
        self.status = Status.PASS
        for g in gpus:
            name = g.get('Name', 'Unknown')
            names.append(name)
            if "Microsoft Basic" in name:
                self.status = Status.FAIL
                self.summary = "Driver Missing (Microsoft Basic Adapter)"
                return

        self.summary = f"Drivers OK: {', '.join(names)}"
        self.data = {"adapters": gpus}