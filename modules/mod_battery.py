from core.engine import DiagnosticModule, Status
from core.sys_interface import SysAdmin

class BatteryModule(DiagnosticModule):
    def __init__(self):
        super().__init__("Battery Health", critical=False)

    def run(self, context):
        # Localization Fix: Use WMI Static Data, not HTML parsing
        static = SysAdmin.run_powershell("Get-WmiObject -Namespace root\\wmi -Class BatteryStaticData | Select-Object DesignedCapacity")
        full = SysAdmin.run_powershell("Get-WmiObject -Namespace root\\wmi -Class BatteryFullChargedCapacity | Select-Object FullChargedCapacity")
        
        if static and full:
            dc = static[0].get('DesignedCapacity', 0)
            fc = full[0].get('FullChargedCapacity', 0)
            
            if dc > 0:
                health = (fc / dc) * 100
                self.data = {"design": dc, "current": fc, "health": health}
                self.summary = f"Health: {health:.1f}%"
                
                threshold = context.get('config', {}).get('thresholds', {}).get('battery_min_health', 75.0)
                
                if health > threshold:
                    self.status = Status.PASS
                elif health > 50:
                    self.status = Status.WARN
                else:
                    self.status = Status.FAIL
            else:
                self.status = Status.INFO
                self.summary = "Battery detected but capacity is 0"
        else:
            self.status = Status.INFO
            self.summary = "No Battery / AC Power"