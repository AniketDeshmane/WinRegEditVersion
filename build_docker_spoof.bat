@echo off
setlocal

REM Change to the script directory
cd /d "%~dp0"

echo [*] Ensuring PyInstaller is installed...
py -m pip install --user pyinstaller
if errorlevel 1 (
    echo [!] Failed to install PyInstaller. Make sure Python is installed and in PATH.
    pause
    exit /b 1
)

echo [*] Building docker_spoof_gui.exe with PyInstaller...
py -m PyInstaller --onefile --noconsole docker_spoof_gui.py
if errorlevel 1 (
    echo [!] Build failed.
    pause
    exit /b 1
)

echo.
echo [*] Build completed successfully.
echo [*] You can find docker_spoof_gui.exe in the "dist" folder.
echo [*] IMPORTANT: Right-click docker_spoof_gui.exe and choose "Run as administrator".
echo.
pause

endlocal

