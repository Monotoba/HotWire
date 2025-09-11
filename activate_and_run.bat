@echo off
REM Activation and run script for Wire Temperature Calculator (Windows)
REM This script activates the Python 3.13 venv and runs the application

echo Wire Temperature Calculator - Python 3.13
echo =========================================

REM Check if venv exists
if not exist "venv" (
    echo Virtual environment not found. Creating Python 3.13 venv...
    python3.13 -m venv venv
)

REM Activate virtual environment
echo Activating Python 3.13 virtual environment...
call venv\Scripts\activate.bat

REM Verify Python version
echo Python version:
python --version

REM Check if dependencies are installed
python -c "import PySide6, pyqtgraph, numpy" 2>nul
if errorlevel 1 (
    echo Installing dependencies...
    pip install --upgrade pip
    pip install -r requirements.txt
)

REM Run the application
echo Starting Wire Temperature Calculator...
echo.
python launch.py

REM Deactivate virtual environment when done
deactivate