@echo off
:: run_with_admin.bat - Updated version
echo ========================================
echo AHIV Industrial Audit v5.0
echo ========================================
echo.

:: Check if executable exists
if not exist "%~dp0AHIV_Audit_v5.0.exe" (
    if exist "%~dp0dist\AHIV_Audit_v5.0.exe" (
        echo Found executable in dist folder...
        set "EXE_PATH=%~dp0dist\AHIV_Audit_v5.0.exe"
    ) else (
        echo [ERROR] AHIV_Audit_v5.0.exe not found!
        echo Please build the executable first using build_exe.bat
        pause
        exit /b 1
    )
) else (
    set "EXE_PATH=%~dp0AHIV_Audit_v5.0.exe"
)

echo Requesting Administrator privileges...
echo.

:: Check for admin rights
net session >nul 2>&1
if %errorLevel% == 0 (
    echo [OK] Administrator privileges confirmed
    echo.
    echo Starting AHIV Audit...
    echo ========================================
    "%EXE_PATH%"
) else (
    echo [!] This program requires Administrator privileges.
    echo Restarting with admin rights...
    echo.
    powershell -Command "Start-Process '%EXE_PATH%' -Verb RunAs"
)

pause