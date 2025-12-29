from core.engine import DiagnosticModule, Status
from core.sys_interface import SysAdmin

class IdentityModule(DiagnosticModule):
    def __init__(self):
        super().__init__("System Identity", critical=True)

    def run(self, context):
        sys_info = SysAdmin.run_powershell("Get-CimInstance Win32_ComputerSystem | Select-Object Model, Manufacturer, TotalPhysicalMemory")
        bios_info = SysAdmin.run_powershell("Get-CimInstance Win32_BIOS | Select-Object SerialNumber")
        
        if sys_info and bios_info:
            model = sys_info[0].get('Model')
            serial = bios_info[0].get('SerialNumber')
            ram = int(sys_info[0].get('TotalPhysicalMemory', 0)) / (1024**3)
            
            # Save to context for other modules/report
            context['serial'] = serial
            context['model'] = model
            
            self.status = Status.PASS
            self.summary = f"{model} (SN: {serial}) | {ram:.1f} GB RAM"
            self.data = {"model": model, "serial": serial, "ram_bytes": sys_info[0].get('TotalPhysicalMemory')}
        else:
            self.status = Status.FAIL
            self.summary = "Could not identify system (WMI Error)"