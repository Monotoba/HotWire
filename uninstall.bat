@echo off
REM Wire Temperature Calculator - Windows Uninstall Script
echo Wire Temperature Calculator - Uninstalling...
echo ===============================================

REM Remove virtual environment
if exist venv (
    echo Removing virtual environment...
    rmdir /s /q venv
    if %errorLevel% equ 0 (
        echo ✓ Virtual environment removed
    ) else (
        echo ✗ Failed to remove virtual environment
    )
) else (
    echo Virtual environment not found
)

REM Remove desktop shortcut
set DESKTOP=%USERPROFILE%\Desktop
set SHORTCUT=%DESKTOP%\Wire Temperature Calculator.lnk
if exist "%SHORTCUT%" (
    echo Removing desktop shortcut...
    del "%SHORTCUT%" 2>nul
    if %errorLevel% equ 0 (
        echo ✓ Desktop shortcut removed
    ) else (
        echo ✗ Failed to remove desktop shortcut
    )
) else (
    echo Desktop shortcut not found
)

REM Remove Start Menu shortcut
set STARTMENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs
set STARTSHORTCUT=%STARTMENU%\Wire Temperature Calculator.lnk
if exist "%STARTSHORTCUT%" (
    echo Removing Start Menu shortcut...
    del "%STARTSHORTCUT%" 2>nul
    if %errorLevel% equ 0 (
        echo ✓ Start Menu shortcut removed
    ) else (
        echo ✗ Failed to remove Start Menu shortcut
    )
) else (
    echo Start Menu shortcut not found
)

REM Remove uninstall script itself
echo Removing uninstall script...
del "%~f0" 2>nul

echo.
echo ===============================================
echo Uninstallation completed successfully!
echo Thank you for using Wire Temperature Calculator!
echo ===============================================
echo.

pause