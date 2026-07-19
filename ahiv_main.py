# ahiv_main.py - Fixed version with proper encoding
import sys
import os
import multiprocessing
import yaml
import traceback
from datetime import datetime
from pathlib import Path
from core.engine import PluginManager, Status
from core.reporting import ReportExporter

# Add the current directory to path for bundled executables
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    base_path = sys._MEIPASS
else:
    # Running as script
    base_path = os.path.dirname(os.path.abspath(__file__))

def load_config():
    """Load configuration with fallback to default values"""
    config_paths = [
        os.path.join(base_path, 'ahiv_config.yaml'),
        'ahiv_config.yaml',
        os.path.join(os.path.dirname(sys.executable), 'ahiv_config.yaml')
    ]
    
    for path in config_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f)
            except Exception as e:
                print(f"[!] Error loading config from {path}: {e}")
                continue
    
    # Default configuration if file not found
    print("[!] No config file found, using defaults")
    return {
        'thresholds': {
            'battery_min_health': 75.0,
            'ssd_max_wear': 90,
            'cpu_stress_sec': 20,
            'max_safe_temp': 85.0,
            'max_whea_errors': 0
        },
        'meta': {
            'company_name': 'TechRefurb Global'
        }
    }

def calculate_grade(results):
    """Enhanced grading logic with more detailed criteria"""
    # Count results by status
    status_counts = {'FAIL': 0, 'WARN': 0, 'PASS': 0, 'INFO': 0}
    critical_fails = []
    
    for r in results:
        status_counts[r['status']] += 1
        if r.get('critical', False) and r['status'] == 'FAIL':
            critical_fails.append(r['name'])
    
    # Strict criteria for industrial certification
    if status_counts['FAIL'] > 0:
        if critical_fails:
            return "FAIL", f"Critical failures in: {', '.join(critical_fails)}"
        else:
            return "FAIL", "Non-critical failures detected"
    
    # Check for incomplete tests
    critical_missing = any(r['status'] == 'INFO' and r.get('critical', False) for r in results)
    if critical_missing:
        return "INCOMPLETE", "Critical tests could not be completed"
    
    # Check for warnings
    if status_counts['WARN'] > 0:
        return "SILVER", f"Warnings present ({status_counts['WARN']})"
    
    # All pass
    return "GOLD", "All tests passed successfully"

def main():
    # Windows Multiprocessing Fix
    multiprocessing.freeze_support()
    
    print("="*50)
    print("   AHIV Industrial Audit v5.0")
    print("   Hardware Integrity Verification")
    print("="*50)
    print(f"Base Path: {base_path}")
    print(f"Python Version: {sys.version.split()[0]}")
    print("-"*50)
    
    try:
        # 1. Load Config
        config = load_config()
        print("[OK] Configuration loaded")
        
        # 2. Discover Plugins
        manager = PluginManager()
        plugins = manager.discover_modules()
        
        if not plugins:
            print("[!] No plugins found. Check 'modules' folder.")
            print(f"[!] Available modules: {os.listdir(base_path)}")
            input("Press Enter to exit...")
            return
        
        print(f"[OK] Found {len(plugins)} diagnostic modules")
        
        # 3. Run Tests
        results = []
        context = {"config": config}
        
        for i, plugin in enumerate(plugins, 1):
            print(f"[*] Running {plugin.name}... ({i}/{len(plugins)})")
            try:
                plugin.run(context)
            except Exception as e:
                print(f"[!] Error in {plugin.name}: {str(e)}")
                traceback.print_exc()
                plugin.status = Status.FAIL
                plugin.summary = f"Module crashed: {str(e)}"
            
            # Save result
            res = plugin.get_result()
            results.append(res)
            
            # Console Feedback with status
            status_icon = {
                'PASS': '[PASS]',
                'WARN': '[WARN]',
                'FAIL': '[FAIL]',
                'INFO': '[INFO]'
            }.get(res['status'], '[UNK]')
            
            print(f"  {status_icon} {res['name']}: {res['summary']}")
        
        # 4. Generate Report
        grade, grade_reason = calculate_grade(results)
        
        # Get serial from context
        serial = context.get('serial', 'Unknown')
        model = context.get('model', 'Unknown')
        
        # Create reports directory
        if getattr(sys, 'frozen', False):
            reports_dir = os.path.join(os.path.dirname(sys.executable), 'reports')
        else:
            reports_dir = 'reports'
        
        os.makedirs(reports_dir, exist_ok=True)
        
        # Generate HTML report
        payload = {
            "meta": {"serial": serial, "grade": grade, "model": model},
            "results": results
        }
        
        html = ReportExporter.generate_html(payload, grade)
        
        # Save report
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"Cert_{serial}_{grade}_{timestamp}.html"
        filepath = os.path.join(reports_dir, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        
        # Summary
        print("\n" + "="*50)
        print(f"CERTIFICATION RESULT: {grade}")
        print(f"Reason: {grade_reason}")
        print(f"Report saved: {filepath}")
        print(f"System: {model} (SN: {serial})")
        print("="*50)
        
        # Show test summary
        print("\nTest Summary:")
        for r in results:
            icon = '[PASS]' if r['status'] == 'PASS' else '[WARN]' if r['status'] == 'WARN' else '[FAIL]' if r['status'] == 'FAIL' else '[INFO]'
            print(f"  {icon} {r['name']}: {r['status']}")
        
        print("\n" + "="*50)
        
    except Exception as e:
        print(f"\n[!] Critical Error: {str(e)}")
        traceback.print_exc()
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()