# AHIV Industrial Audit v5.0

[![Version](https://img.shields.io/badge/version-5.0-blue.svg)](https://github.com/amirradnia99/ahiv-audit)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-Windows%2010%2F11-lightgrey.svg)](https://www.microsoft.com/windows)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Release](https://img.shields.io/github/v/release/amirradnia99/ahiv-audit)](https://github.com/amirradnia99/ahiv-audit/releases)
[![Downloads](https://img.shields.io/github/downloads/amirradnia99/ahiv-audit/total.svg)](https://github.com/amirradnia99/ahiv-audit/releases)

## Overview

AHIV Industrial Audit is a professional hardware diagnostic and certification suite designed for industrial refurbishing, quality assurance, and hardware validation environments. It performs automated stress testing, telemetry analysis, and error forensics to provide standardized certification grades for Windows-based computer systems.

## Key Features

- **Dynamic Plugin Architecture**: Automatically discovers and loads diagnostic modules
- **Hardware Validation**: Comprehensive testing of all major hardware components
- **WHEA Forensics**: Advanced memory error detection via Windows Hardware Error Architecture
- **Thermal Dynamics**: Real-time CPU stress testing with SVG cooling curve visualization
- **Automated Certification**: Generates professional HTML reports with certification grades
- **Threshold-Based Testing**: Configurable pass/fail criteria via YAML configuration
- **Standalone Executable**: Ready-to-use .exe file, no Python installation required

## Certification Grades

| Grade | Description |
|-------|-------------|
| 🥇 **GOLD** | All tests passed - System is certified for industrial use |
| 🥈 **SILVER** | Warnings detected - Minor issues found |
| ❌ **FAIL** | Critical failures - System requires attention |
| ⚠️ **INCOMPLETE** | Some tests could not be completed |

## Hardware Tests

| Module | Description | Critical |
|--------|-------------|----------|
| **System Identity** | Detects model, serial number, and RAM | ✅ Yes |
| **Battery Health** | Analyzes battery capacity and wear level | ❌ No |
| **GPU Graphics** | Verifies GPU drivers and detects issues | ✅ Yes |
| **RAM Forensics** | Scans WHEA logs for memory errors | ✅ Yes |
| **Storage Wear** | Checks SSD health and wear percentage | ✅ Yes |
| **Thermal Dynamics** | Stress tests CPU and monitors temperature | ✅ Yes |

## Quick Start

### Option 1: Download Executable (Recommended)
1. Download the latest release from [Releases](https://github.com/amirradnia99/ahiv-audit/releases)
2. Extract the ZIP file
3. **Run as Administrator** (right-click → Run as administrator)
4. Wait for the tests to complete
5. Open the generated HTML report

### Option 2: Run from Source
 + "" + "" + "" + "bash
# Clone the repository
git clone git@github.com:amirradnia99/ahiv-audit.git
cd ahiv-audit

# Create virtual environment
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python ahiv_main.py
 + "" + "" + "" + "

## Configuration

Edit hiv_config.yaml to customize thresholds:

 + "" + "" + "" + "yaml
thresholds:
  battery_min_health: 75.0    # Minimum battery health percentage
  ssd_max_wear: 90            # Maximum SSD wear percentage
  cpu_stress_sec: 20          # CPU stress test duration (seconds)
  max_safe_temp: 85.0         # Maximum safe CPU temperature (°C)
  max_whea_errors: 0          # Maximum allowed WHEA errors

meta:
  company_name: "TechRefurb Global"
 + "" + "" + "" + "

## Example Output

 + "" + "" + "" + "
==================================================
   AHIV Industrial Audit v5.0
   Hardware Integrity Verification
==================================================
[OK] Configuration loaded
[OK] Found 6 diagnostic modules
[PASS] System Identity: Dell XPS 15 (SN: ABC123) | 16.0 GB RAM
[PASS] Battery Health: Health: 92.3%
[PASS] GPU Graphics: Drivers OK: NVIDIA GeForce GTX 1650
[PASS] RAM Forensics: Clean (No WHEA Errors)
[PASS] Storage Wear: Samsung SSD 970 EVO [Healthy] Wear: 12%
[PASS] Thermal Dynamics: Stable: Peak 72.5C

==================================================
CERTIFICATION RESULT: GOLD
==================================================
 + "" + "" + "" + "

## Project Structure

 + "" + "" + "" + "
ahiv-audit/
├── core/                       # Core engine
│   ├── engine.py              # Plugin management
│   ├── reporting.py           # HTML report generation
│   └── sys_interface.py       # System interface layer
├── modules/                    # Diagnostic modules
│   ├── mod_battery.py         # Battery health test
│   ├── mod_gpu.py             # GPU driver test
│   ├── mod_identity.py        # System identity test
│   ├── mod_ram.py             # RAM forensics test
│   ├── mod_storage.py         # Storage wear test
│   └── mod_thermal.py         # Thermal dynamics test
├── dist/                       # Build output
│   └── AHIV_Audit_v5.0.exe   # Standalone executable
├── reports/                    # Generated reports
├── ahiv_main.py               # Main application
├── ahiv_config.yaml           # Configuration file
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── LICENSE                    # MIT License
└── .gitignore                 # Git ignore file
 + "" + "" + "" + "

## Requirements

### For Development
- Windows 10/11 (64-bit)
- Python 3.8 or higher
- pip (Python package manager)

### Dependencies
 + "" + "" + "" + "
numpy >= 1.21.0
psutil >= 5.8.0
wmi >= 1.5.1
pyyaml >= 6.0
pywin32 >= 305
pyinstaller >= 5.0.0
 + "" + "" + "" + "

## Building from Source

### Windows Build
 + "" + "" + "" + "powershell
# Build using PyInstaller
pyinstaller --onefile --add-data \"ahiv_config.yaml;.\" ahiv_main.py

# Or use the build script
.\build_exe.bat
 + "" + "" + "" + "

## Contributing

1. Fork the repository
2. Create a feature branch (git checkout -b feature/amazing-feature)
3. Commit your changes (git commit -m 'Add amazing feature')
4. Push to the branch (git push origin feature/amazing-feature)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, questions, or issues:
- Open an [Issue](https://github.com/amirradnia99/ahiv-audit/issues)
- Contact the maintainer

## Acknowledgments

- Built with Python and PyInstaller
- Uses Windows WMI for hardware detection
- Special thanks to the open-source community

---
**Made with ❤️ by Amir Radnia**
