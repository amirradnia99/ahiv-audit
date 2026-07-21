# AHIV Industrial Audit v5.0

Professional hardware diagnostic and certification suite for Windows systems.

## Overview

Automated hardware validation tool for industrial refurbishing, quality assurance, and hardware testing environments. Performs stress testing, telemetry analysis, and error detection with standardized certification reports.

## Key Features

- Dynamic plugin architecture for diagnostic modules
- Comprehensive hardware component testing
- WHEA memory error detection
- CPU stress testing with thermal monitoring
- Automated HTML report generation with certification grades
- Configurable thresholds via YAML
- Standalone executable (no Python required)

## Certification Grades

- **GOLD**: All tests passed - Certified for industrial use
- **SILVER**: Warnings detected - Minor issues found
- **FAIL**: Critical failures - System requires attention
- **INCOMPLETE**: Some tests could not be completed

## Hardware Tests

| Module | Description | Critical |
|--------|-------------|----------|
| System Identity | Model, serial number, and RAM detection | Yes |
| Battery Health | Capacity and wear level analysis | No |
| GPU Graphics | Driver verification and issue detection | Yes |
| RAM Forensics | WHEA log scanning for memory errors | Yes |
| Storage Wear | SSD health and wear percentage check | Yes |
| Thermal Dynamics | CPU stress test and temperature monitoring | Yes |

## Quick Start

### Option 1: Download Executable (Recommended)

1. Download the latest release from **Releases**
2. Extract the ZIP file
3. Run as Administrator
4. Wait for tests to complete
5. Open the generated HTML report

### Option 2: Run from Source

Clone the repository:

```bash
git clone git@github.com:amirradnia99/ahiv-audit.git
cd ahiv-audit
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate (Windows):

```bash
venv\Scripts\activate
```

Activate (Linux/macOS):

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python ahiv_main.py
```

## Configuration

Edit `ahiv_config.yaml`:

```yaml
thresholds:
  battery_min_health: 75.0
  ssd_max_wear: 90
  cpu_stress_sec: 20
  max_safe_temp: 85.0
  max_whea_errors: 0

meta:
  company_name: "Your Company Name"
```

## Example Output

```text
AHIV Industrial Audit v5.0
Hardware Integrity Verification
[OK] Configuration loaded
[OK] Found 6 diagnostic modules
[PASS] System Identity: Dell XPS 15 (SN: ABC123) | 16.0 GB RAM
[PASS] Battery Health: Health: 92.3%
[PASS] GPU Graphics: Drivers OK: NVIDIA GeForce GTX 1650
[PASS] RAM Forensics: Clean (No WHEA Errors)
[PASS] Storage Wear: Samsung SSD 970 EVO [Healthy] Wear: 12%
[PASS] Thermal Dynamics: Stable: Peak 72.5C
CERTIFICATION RESULT: GOLD
```

## Project Structure

```text
ahiv-audit/
├── core/
│   ├── engine.py
│   ├── reporting.py
│   └── sys_interface.py
├── modules/
│   ├── mod_battery.py
│   ├── mod_gpu.py
│   ├── mod_identity.py
│   ├── mod_ram.py
│   ├── mod_storage.py
│   └── mod_thermal.py
├── dist/
│   └── AHIV_Audit_v5.0.exe
├── reports/
├── ahiv_main.py
├── ahiv_config.yaml
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

## Requirements

- Windows 10/11 (64-bit)
- Python 3.8+
- pip

### Dependencies

- numpy >= 1.21.0
- psutil >= 5.8.0
- wmi >= 1.5.1
- pyyaml >= 6.0
- pywin32 >= 305
- pyinstaller >= 5.0.0

## Building from Source

```bash
pyinstaller --onefile --add-data "ahiv_config.yaml;." ahiv_main.py
```

Or:

```powershell
.\build_exe.bat
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## License

MIT License — see the `LICENSE` file for details.

## Support

- Open an Issue on GitHub
- Contact the maintainer

---

**About:** Professional hardware diagnostic and certification suite for Windows systems.

Repository: https://github.com/amirradnia99/ahiv-audit
