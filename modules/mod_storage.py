from core.engine import DiagnosticModule, Status
from core.sys_interface import SysAdmin

class StorageModule(DiagnosticModule):
    def __init__(self):
        super().__init__("Storage Wear", critical=True)

    def run(self, context):
        # Primary: NVMe Wear
        disks = SysAdmin.run_powershell("Get-PhysicalDisk | Select-Object FriendlyName, MediaType, HealthStatus, @{N='Wear';E={($_.GetStorageReliabilityCounters()).Wear}}")
        
        if not disks:
            # Fallback: Basic Status
            disks = SysAdmin.run_powershell("Get-PhysicalDisk | Select-Object FriendlyName, MediaType, HealthStatus")
            
        if not disks:
            self.status = Status.INFO
            self.summary = "No Disks Enumerated"
            return

        self.status = Status.PASS
        summaries = []
        
        max_wear = context.get('config', {}).get('thresholds', {}).get('ssd_max_wear', 90)

        for d in disks:
            name = d.get('FriendlyName')
            health = d.get('HealthStatus')
            wear = d.get('Wear')
            
            info = f"{name} [{health}]"
            if wear is not None:
                info += f" Wear: {wear}%"
                if wear > max_wear:
                    self.status = Status.FAIL
                    info += " (FAIL)"
            
            if health != "Healthy":
                self.status = Status.WARN
                
            summaries.append(info)
            
        self.summary = " | ".join(summaries)
        self.data = {"disks": disks}