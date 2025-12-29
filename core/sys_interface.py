import subprocess
import json

class SysAdmin:
    @staticmethod
    def run_powershell(cmd):
        """
        Executes PowerShell with JSON output for reliability.
        """
        full_cmd = f"{cmd} | ConvertTo-Json -Depth 2 -Compress"
        try:
            # Use list arguments to avoid shell injection
            result = subprocess.run(
                ["powershell", "-NoProfile", "-Command", full_cmd],
                capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            if not result.stdout.strip(): return None
            
            try:
                data = json.loads(result.stdout)
                # Normalize return to list
                return [data] if isinstance(data, dict) else data
            except json.JSONDecodeError:
                return None
        except:
            return None

    @staticmethod
    def run_cmd_simple(cmd):
        """
        Runs simple CMD commands where JSON isn't needed (e.g., wevtutil).
        """
        try:
            return subprocess.run(
                cmd, capture_output=True, text=True, shell=True, 
                creationflags=subprocess.CREATE_NO_WINDOW
            ).stdout.strip()
        except: return ""