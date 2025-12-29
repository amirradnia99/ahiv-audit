from core.engine import DiagnosticModule, Status
from core.sys_interface import SysAdmin

class RamModule(DiagnosticModule):
    def __init__(self):
        super().__init__("RAM Forensics", critical=True)

    def run(self, context):
        # 1. WHEA Forensics (Specific IDs)
        # ID 47 = Memory Corrected, ID 18 = Machine Check Exception (Fatal)
        cmd = 'wevtutil qe System /c:50 /f:text /q:"*[System[(EventID=47 or EventID=18) and Provider[@Name=\'Microsoft-Windows-WHEA-Logger\']]]"'
        logs = SysAdmin.run_cmd_simple(cmd)
        
        fatal_errs = logs.count("Event ID: 18")
        corr_errs = logs.count("Event ID: 47")
        
        self.data = {"whea_fatal": fatal_errs, "whea_corrected": corr_errs}
        
        if fatal_errs > 0:
            self.status = Status.FAIL
            self.summary = f"CRITICAL: {fatal_errs} Fatal Memory Errors (MCE)"
        elif corr_errs > 0:
            self.status = Status.WARN
            self.summary = f"Degraded: {corr_errs} Corrected ECC Errors"
        else:
            self.status = Status.PASS
            self.summary = "Clean (No WHEA Errors)"