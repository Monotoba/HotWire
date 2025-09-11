# Wire Temperature Calculator Documentation

## Overview

The Wire Temperature Calculator is a professional-grade application for calculating wire temperatures and foam cutting parameters. It supports multiple wire gauge units, length units, and foam types with comprehensive safety monitoring.

## Features

### Core Capabilities
- **Multi-unit support**: AWG, SWG, mm, mils, inch for wire gauges
- **Length units**: mm, cm, inch, feet, meters, yards
- **Materials**: Nichrome, Stainless Steel, Kanthal
- **Foam cutting**: 10 professional foam types with safety monitoring
- **Visualization**: Color-coded charts with safety indicators
- **Export**: PDF and print support
- **Project management**: Save/load configurations

### Safety Features
- Real-time temperature validation
- Fire risk assessment
- Toxic fume warnings
- Ventilation requirements
- PPE recommendations

## Quick Start

### GUI Application
```bash
# Run the GUI application
./activate_and_run.sh
```

### Command Line Interface
```bash
# Calculate temperature for 22 AWG nichrome wire at 1A
wire-temp-calc --gauge 22 --gauge-unit AWG --material nichrome --length 2 --length-unit feet --current 1

# Foam cutting with EPP foam
wire-temp-calc --foam EPP --wire-diameter 0.644 --cutting-speed 5
```

## Installation

### Automated Installation (Recommended)
```bash
# Clone the repository
git clone https://github.com/yourusername/wire-temperature-calculator.git
cd wire-temperature-calculator

# Run automated installer
./install.sh
```

### Manual Installation
```bash
# Create virtual environment
python3.13 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate.bat  # Windows

# Install dependencies
pip install -r requirements.txt

# Run application
python -m wire_temp_calc.main
```

## Documentation Sections

- [Installation Guide](installation/index.md) - Detailed installation instructions
- [User Guide](user-guide.md) - Complete usage guide
- [API Reference](api/index.md) - Developer API documentation
- [Examples](examples/index.md) - Usage examples and tutorials
- [Safety Guidelines](safety.md) - Important safety information
- [Troubleshooting](troubleshooting.md) - Common issues and solutions

## Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/wire-temperature-calculator/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/wire-temperature-calculator/discussions)
- **Email**: support@wiretempcalc.com

## License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.