# setup.py - Simplified version
import PyInstaller.__main__
import os

if __name__ == "__main__":
    # Check if spec file exists
    if os.path.exists('ahiv.spec'):
        print("Building using ahiv.spec file...")
        PyInstaller.__main__.run([
            'ahiv.spec',
            '--clean',
            '--log-level=INFO',
        ])
    else:
        print("Building using command-line arguments...")
        PyInstaller.__main__.run([
            'ahiv_main.py',
            '--name=AHIV_Audit_v5.0',
            '--onefile',
            '--add-data=ahiv_config.yaml;.',
            '--hidden-import=numpy',
            '--hidden-import=psutil',
            '--hidden-import=wmi',
            '--hidden-import=pyyaml',
            '--hidden-import=core.engine',
            '--hidden-import=core.reporting',
            '--hidden-import=core.sys_interface',
            '--hidden-import=modules.mod_battery',
            '--hidden-import=modules.mod_gpu',
            '--hidden-import=modules.mod_identity',
            '--hidden-import=modules.mod_ram',
            '--hidden-import=modules.mod_storage',
            '--hidden-import=modules.mod_thermal',
            '--collect-submodules=core',
            '--collect-submodules=modules',
            '--exclude-module=tkinter',
            '--exclude-module=unittest',
            '--exclude-module=test',
            '--log-level=INFO',
            '--clean',
        ])