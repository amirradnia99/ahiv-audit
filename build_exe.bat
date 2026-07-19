@echo off
REM build_exe.bat - Updated build script
echo ========================================
echo Building AHIV Industrial Audit Executable
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Display Python version
echo Python version:
python --version
echo.

REM Install/Update requirements
echo [1/5] Installing requirements...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install requirements
    pause
    exit /b 1
)
echo.

REM Install PyInstaller
echo [2/5] Installing PyInstaller...
pip install pyinstaller --upgrade
echo.

REM Clean previous builds
echo [3/5] Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del *.spec 2>nul
echo.

REM Build the executable
echo [4/5] Building executable...
echo This may take several minutes...
echo.

REM Use the spec file if it exists
if exist ahiv.spec (
    echo Using ahiv.spec file...
    pyinstaller ahiv.spec --clean --log-level=INFO
) else (
    echo Using setup.py...
    python setup.py
)

if errorlevel 1 (
    echo.
    echo [ERROR] Build failed!
    pause
    exit /b 1
)
echo.

REM Check if build was successful
echo [5/5] Build complete!
if exist dist\*.exe (
    echo.
    echo ========================================
    echo [SUCCESS] Executable created in 'dist' folder
    echo ========================================
    echo.
    echo Files created:
    dir dist\*.exe
    echo.
    echo Size:
    for %%f in (dist\*.exe) do echo %%~zf bytes
    echo.
    echo ========================================
    echo.
    echo To run the executable:
    echo 1. Copy ahiv_config.yaml to the same folder as the .exe
    echo 2. Run: dist\AHIV_Audit_v5.0.exe
    echo 3. Or use: run_with_admin.bat
    echo ========================================
) else (
    echo.
    echo ========================================
    echo [FAILED] Build failed. Check error messages above.
    echo ========================================
)

pause