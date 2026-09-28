@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\wire-temp-gui.exe" (
  echo Run install.bat first, or follow docs\installation\index.md.
  exit /b 1
)
.venv\Scripts\wire-temp-gui.exe
