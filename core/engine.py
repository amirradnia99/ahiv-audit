import importlib
import pkgutil
import inspect
import sys
import os
from enum import Enum

# Ensure we can find the modules folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class Status(Enum):
    PASS = "PASS"
    WARN = "WARN"
    FAIL = "FAIL"
    INFO = "INFO"

class DiagnosticModule:
    def __init__(self, name: str, critical: bool = False):
        self.name = name
        self.critical = critical
        self.status = Status.INFO
        self.summary = "Pending"
        self.data = {}

    def run(self, context: dict): raise NotImplementedError
    def get_result(self): 
        return {
            "name": self.name, 
            "status": self.status.value, 
            "summary": self.summary, 
            "data": self.data,
            "critical": self.critical
        }

class PluginManager:
    def __init__(self):
        self.modules = []

    def discover_modules(self):
        self.modules = []
        try:
            import modules
        except ImportError as e:
            print(f"[!] Could not import 'modules' package: {e}")
            return []

        prefix = modules.__name__ + "."
        for _, name, _ in pkgutil.iter_modules(modules.__path__, prefix):
            try:
                mod = importlib.import_module(name)
                for _, obj in inspect.getmembers(mod):
                    if inspect.isclass(obj) and issubclass(obj, DiagnosticModule) and obj is not DiagnosticModule:
                        self.modules.append(obj())
            except Exception as e:
                print(f"[!] Plugin Load Error ({name}): {e}")
        
        return self.modules