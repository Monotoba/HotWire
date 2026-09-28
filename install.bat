@echo off
REM Wire Temperature Calculator - Windows Installation Script
REM Professional foam cutting and wire heating calculator

echo Wire Temperature Calculator - Windows Installation
echo ===============================================
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo WARNING: Not running as administrator. Some features may not work properly.
    echo Consider running this script as administrator.
    echo.
    pause
)

REM Check Python version
echo Checking Python installation...
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10 or higher from https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo Found Python %PYTHON_VERSION%

REM Check if Python version is 3.10+
python -c "import sys; exit(0 if sys.version_info >= (3, 10) else 1)" >nul 2>&1
if %errorLevel% neq 0 (
    echo ERROR: Python 3.10 or higher is required
    echo Found version: %PYTHON_VERSION%
    echo Please upgrade Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python version check passed!
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv .venv
if %errorLevel% neq 0 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo Virtual environment created successfully!
echo.

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat
if %errorLevel% neq 0 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

echo Virtual environment activated!
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
if %errorLevel% neq 0 (
    echo WARNING: Failed to upgrade pip, continuing anyway...
)
echo.

REM Install requirements
echo Installing dependencies...
if exist setup.py (
    python -m pip install -e .
    if %errorLevel% neq 0 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
) else (
    echo ERROR: package files not found
    pause
    exit /b 1
)

echo Dependencies installed successfully!
echo.

REM Create desktop shortcut (optional)
echo Creating desktop shortcut...
set DESKTOP=%USERPROFILE%\Desktop
set SHORTCUT=%DESKTOP%\Wire Temperature Calculator.lnk

powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%SHORTCUT%'); $Shortcut.TargetPath = '%CD%\activate_and_run.bat'; $Shortcut.WorkingDirectory = '%CD%'; $Shortcut.IconLocation = '%CD%\src\wire_temp_calc\resources\icon.ico'; $Shortcut.Save()" >nul 2>&1

echo Desktop shortcut created!
echo.

REM Create Windows Start Menu shortcut
echo Creating Start Menu shortcut...
set STARTMENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs
set STARTSHORTCUT=%STARTMENU%\Wire Temperature Calculator.lnk

powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%STARTSHORTCUT%'); $Shortcut.TargetPath = '%CD%\activate_and_run.bat'; $Shortcut.WorkingDirectory = '%CD%'; $Shortcut.IconLocation = '%CD%\src\wire_temp_calc\resources\icon.ico'; $Shortcut.Save()" >nul 2>&1

echo Start Menu shortcut created!
echo.

REM Test installation
echo Testing installation...
python -c "import wire_temp_calc; print('✓ Package imported successfully')" >nul 2>&1
if %errorLevel% neq 0 (
    echo WARNING: Package import test failed, but installation may still work
) else (
    echo ✓ Installation test passed!
)
echo.

REM Create uninstall script
echo Creating uninstall script...
(
echo @echo off
echo echo Uninstalling Wire Temperature Calculator...
echo rmdir /s /q .venv
echo del "%USERPROFILE%\Desktop\Wire Temperature Calculator.lnk" 2^>nul
echo del "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Wire Temperature Calculator.lnk" 2^>nul
echo echo Uninstallation complete!
echo pause
) > uninstall.bat

echo Uninstall script created!
echo.

echo ===============================================
echo Installation completed successfully!
echo.
echo To run the application:
echo   1. Double-click activate_and_run.bat
echo   2. Or use the desktop/start menu shortcut
echo.
echo For command line usage:
echo   wire-temp-calc --help
echo.
echo To uninstall:
echo   Run uninstall.bat
echo ===============================================
echo.

pause