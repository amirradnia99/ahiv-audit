# AHIV Industrial Audit v5.0

## Overview
AHIV Industrial Audit is a modular hardware diagnostic and certification suite designed for industrial refurbishing and quality assurance environments. The system performs automated stress testing, telemetry analysis, and error forensics to provide a standardized certification grade (GOLD, SILVER, or FAIL) for Windows-based computer systems.

## Project Structure
- /core: Central processing engine, plugin management, and reporting interfaces.
- /modules: Pluggable diagnostic tests (Thermal, Storage, RAM, Battery, etc.).
- /config: Threshold-based logic configuration via YAML.

## Key Features
- Dynamic Plugin Discovery: Automatically loads and executes hardware test modules.
- WHEA Forensics: Analyzes Windows Hardware Error Architecture logs for memory instability.
- Thermal Dynamics: Real-time FPU stress testing with integrated SVG cooling curve generation.
- Automated Certification: Generates an HTML-based hardware certificate with device serial number mapping.

## Requirements
- Windows 10/11
- Python 3.8+
- Dependencies: numpy, psutil, pywin32, pyyaml, wmi

## Usage
Run the main auditor via:
python ahiv_main.py