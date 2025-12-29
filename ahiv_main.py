import sys
import os
import multiprocessing
import yaml
from core.engine import PluginManager, Status
from core.reporting import ReportExporter

def load_config():
    if os.path.exists('ahiv_config.yaml'):
        with open('ahiv_config.yaml', 'r') as f:
            return yaml.safe_load(f)
    return {}

def calculate_grade(results):
    # Industrial Grading Logic
    has_fail = any(r['status'] == 'FAIL' for r in results)
    has_warn = any(r['status'] == 'WARN' for r in results)
    critical_missing = any(r['status'] == 'INFO' and r.get('critical', False) for r in results)

    if has_fail: return "FAIL"
    if critical_missing: return "INCOMPLETE"
    if has_warn: return "SILVER"
    return "GOLD"

def main():
    # Windows Multiprocessing Fix for PyInstaller
    multiprocessing.freeze_support()

    print("--- AHIV Industrial Audit v5.0 ---")
    
    # 1. Load Config
    config = load_config()
    
    # 2. Discover Plugins
    manager = PluginManager()
    plugins = manager.discover_modules()
    
    if not plugins:
        print("[!] No plugins found. Check 'modules' folder.")
        return

    results = []
    context = {"config": config}
    
    # 3. Run Tests
    for plugin in plugins:
        print(f"[*] Running {plugin.name}...", end="\r")
        try:
            plugin.run(context)
        except Exception as e:
            plugin.status = Status.FAIL
            plugin.summary = f"Crashed: {str(e)}"
        
        # Save result
        res = plugin.get_result()
        results.append(res)
        
        # Console Feedback
        status_color = ""
        if res['status'] == 'FAIL': status_color = "!!!"
        print(f"[{res['status']}] {plugin.name}: {plugin.summary} {status_color}")

    # 4. Generate Report
    grade = calculate_grade(results)
    
    # Inject Serial into Meta for filename
    serial = context.get('serial', 'Unknown')
    payload = {
        "meta": {"serial": serial, "grade": grade}, 
        "results": results
    }
    
    html = ReportExporter.generate_html(payload, grade)
    
    filename = f"Cert_{serial}_{grade}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)
        
    print("\n" + "="*40)
    print(f"FINAL CERTIFICATION: {grade}")
    print(f"Report saved: {filename}")
    print("="*40)
    
    input("Press Enter to exit...")

if __name__ == "__main__":
    main()