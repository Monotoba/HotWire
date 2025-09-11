# Installation Guide

## System Requirements

### Minimum Requirements
- **Python**: 3.10 or higher (Python 3.13 recommended)
- **Operating System**: Windows 10+, macOS 10.14+, Linux (Ubuntu 18.04+)
- **Memory**: 4GB RAM minimum, 8GB recommended
- **Storage**: 500MB free space
- **Display**: 1024x768 resolution minimum

### Recommended Requirements
- **Python**: 3.13+ with latest updates
- **Memory**: 8GB RAM or more
- **Storage**: 1GB free space
- **Display**: 1920x1080 resolution or higher

## Installation Methods

### Method 1: Automated Installation (Recommended)

**Linux/macOS:**
```bash
# Clone the repository
git clone https://github.com/yourusername/wire-temperature-calculator.git
cd wire-temperature-calculator

# Make installer executable
chmod +x install.sh

# Run automated installer
./install.sh

# Launch application
./activate_and_run.sh
```

**Windows:**
```cmd
# Clone the repository
git clone https://github.com/yourusername/wire-temperature-calculator.git
cd wire-temperature-calculator

# Run automated installer
install.bat

# Launch application
activate_and_run.bat
```

### Method 2: Manual Installation

**Step 1: Install Python**
Download and install Python 3.13+ from [python.org](https://www.python.org/downloads/)

**Step 2: Clone Repository**
```bash
git clone https://github.com/yourusername/wire-temperature-calculator.git
cd wire-temperature-calculator
```

**Step 3: Create Virtual Environment**
```bash
# Linux/macOS
python3.13 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

**Step 4: Install Dependencies**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Step 5: Run Application**
```bash
# GUI Application
python -m wire_temp_calc.main

# Command Line Interface
python -m wire_temp_calc.cli --help
```

### Method 3: Package Installation

**From PyPI (when published):**
```bash
pip install wire-temperature-calculator
wire-temp-calc --help
```

**From Source Distribution:**
```bash
# Build from source
python setup.py sdist bdist_wheel

# Install the package
pip install dist/wire_temperature_calculator-2.0.0-py3-none-any.whl
```

## Platform-Specific Instructions

### Windows

**Prerequisites:**
- Visual C++ Redistributable (usually included with Python)
- Windows 10 or higher

**Installation Notes:**
- Run PowerShell as Administrator for system-wide installation
- Windows Defender may flag the application - add to exclusions if needed
- Use Windows Terminal for best experience

### macOS

**Prerequisites:**
- Xcode Command Line Tools: `xcode-select --install`
- Homebrew (recommended): `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`

**Installation Notes:**
- May need to allow app in Security & Privacy settings
- Use Homebrew Python for best compatibility

### Linux

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3.13 python3.13-venv python3-pip
```

**Fedora/RHEL:**
```bash
sudo dnf install python3.13 python3-pip
```

**Arch Linux:**
```bash
sudo pacman -S python python-pip
```

## Verification

### Test Installation
```bash
# Test basic functionality
python -m wire_temp_calc.cli --list-foams

# Test temperature calculation
python -m wire_temp_calc.cli --gauge 22 --material nichrome --current 1

# Test GUI (if display available)
python -m wire_temp_calc.main
```

### Expected Output
```
Supported Foam Types:
============================
EPP          | Expanded Polypropylene - High performance, multiple impacts
  Temperature range: 220-260°C
  Cutting speed: medium
  Fire risk: medium

EPS          | Expanded Polystyrene - Common white foam, easy to cut
  Temperature range: 180-220°C
  Cutting speed: fast
  Fire risk: medium
...
```

## Troubleshooting

### Common Issues

**1. Import Error: No module named 'PySide6'**
```bash
# Solution: Reinstall requirements
pip install --force-reinstall -r requirements.txt
```

**2. Permission Denied on install.sh**
```bash
chmod +x install.sh
./install.sh
```

**3. Virtual Environment Activation Fails**
```bash
# Try explicit Python version
python3.13 -m venv venv
source venv/bin/activate
```

**4. Display Issues on Linux**
```bash
# Install display dependencies
sudo apt install libgl1-mesa-glx libglib2.0-0
```

### Getting Help

If you encounter issues:

1. Check the [Troubleshooting Guide](../troubleshooting.md)
2. Search [GitHub Issues](https://github.com/yourusername/wire-temperature-calculator/issues)
3. Create a new issue with:
   - Your operating system and version
   - Python version
   - Complete error message
   - Steps to reproduce

## Uninstallation

### Automated Uninstall
```bash
# Run uninstall script
./uninstall.sh
```

### Manual Uninstall
```bash
# Remove virtual environment
rm -rf venv

# Remove application files
rm -rf wire-temperature-calculator

# Remove configuration files
rm -rf ~/.config/WireTempCalc
```