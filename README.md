# 🔥 Wire Temperature Calculator

[![CI/CD Pipeline](https://github.com/yourusername/wire-temperature-calculator/workflows/CI/CD%20Pipeline/badge.svg)](https://github.com/yourusername/wire-temperature-calculator/actions)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI Version](https://img.shields.io/pypi/v/wire-temperature-calculator)](https://pypi.org/project/wire-temperature-calculator/)
[![Downloads](https://pepy.tech/badge/wire-temperature-calculator)](https://pepy.tech/project/wire-temperature-calculator)

> **Professional-grade wire temperature calculator with comprehensive foam cutting capabilities**

## 🎯 Overview

The Wire Temperature Calculator is a sophisticated application for calculating wire temperatures and optimizing foam cutting operations. It combines precise thermal calculations with comprehensive safety monitoring, making it ideal for both hobbyists and professionals.

### ✨ Key Features

- **🌡️ Multi-Unit Support**: AWG, SWG, mm, mils, inch for wire gauges
- **📏 Length Units**: mm, cm, inch, feet, meters, yards  
- **🔧 Materials**: Nichrome, Stainless Steel, Kanthal
- **🧽 Foam Cutting**: 10 professional foam types with safety monitoring
- **📊 Visualization**: Color-coded charts with safety indicators
- **📄 Export**: PDF and print support
- **💾 Project Management**: Save/load configurations
- **🛡️ Safety First**: Comprehensive safety monitoring and warnings

## 🚀 Quick Start

### GUI Application (Recommended)
```bash
# One-click installation and launch
./activate_and_run.sh  # Linux/Mac
activate_and_run.bat   # Windows
```

### Command Line Interface
```bash
# Calculate temperature for 22 AWG nichrome wire
wire-temp-calc --gauge 22 --material nichrome --current 1

# Foam cutting with EPP foam
wire-temp-calc --foam EPP --wire-diameter 0.644 --cutting-speed 5

# List all supported foam types
wire-temp-calc --list-foams
```

## 📦 Installation

### Automated Installation (Recommended)
```bash
# Clone and install
git clone https://github.com/yourusername/wire-temperature-calculator.git
cd wire-temperature-calculator
./install.sh  # Linux/Mac
install.bat   # Windows
```

### PyPI Installation
```bash
pip install wire-temperature-calculator
wire-temp-calc --help
```

### Manual Installation
```bash
# Create virtual environment
python3.13 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run application
python -m wire_temp_calc.main
```

## 🎯 Core Capabilities

### Wire Temperature Calculation
- **Precise thermal modeling** with material-specific properties
- **Iterative temperature solving** accounting for resistance changes
- **Multi-current range analysis** with customizable steps
- **Real-time safety validation** with visual feedback

### Foam Cutting Optimization
- **10 professional foam types** with specific temperature ranges
- **Automatic optimal temperature calculation** based on wire and foam properties
- **Cutting speed recommendations** for different applications
- **Safety monitoring** with real-time warnings

### Unit System
- **Bidirectional conversion** between any supported units
- **Precision preservation** across conversions
- **Flexible input methods** - enter values in any unit
- **Professional display** with appropriate unit formatting

### Safety Features
- **Temperature range validation** for each foam type
- **Fire risk assessment** (low/medium/high)
- **Toxic fume warnings** for dangerous temperatures
- **Ventilation and PPE recommendations**
- **Emergency procedure guidelines**

## 🧽 Supported Foam Types

| Foam | Temperature Range | Best For | Characteristics |
|------|------------------|----------|-----------------|
| **EPP** | 220-260°C | RC Aircraft | Durable, impact resistant |
| **EPS** | 180-220°C | Packaging | Lightweight, easy to cut |
| **EVA** | 190-230°C | Crafts | Soft, flexible |
| **XPS** | 200-240°C | Insulation | Dense, closed-cell |
| **DEPRON** | 180-220°C | RC Models | Thin, rigid sheets |
| **FOAM_BOARD** | 160-200°C | Presentations | Paper-faced |
| **MEMORY** | 150-190°C | Cushioning | Temperature-sensitive |
| **NEOPRENE** | 180-220°C | Weather Sealing | Weather-resistant |
| **PU** | 170-210°C | Upholstery | Versatile |
| **EPE** | 200-240°C | Packaging | Flexible, cushioning |

## 📊 Example Usage

### RC Aircraft Building
```bash
# EPP wing construction with 22 AWG wire
wire-temp-calc --foam EPP --gauge 22 --material nichrome --length 3 --cutting-speed 5
# Output: Optimal temperature: 240°C, Fire risk: medium, Ventilation: Required
```

### Craft Projects
```bash
# EPS foam board cutting
wire-temp-calc --foam FOAM_BOARD --wire-diameter 0.5 --cutting-speed 2
# Output: Optimal temperature: 180°C, Fire risk: low, Ventilation: Not required
```

### Industrial Applications
```bash
# XPS insulation cutting with safety check
wire-temp-calc --safety-info XPS 250
# Output: WARNING: Temperature too high! Maximum: 240°C
```

## 🛡️ Safety Features

### Automatic Safety Monitoring
- **Real-time temperature validation** against foam-specific limits
- **Visual danger indicators** on charts (red zones)
- **Fire risk assessment** with appropriate warnings
- **Toxic fume alerts** for decomposition temperatures

### Professional Safety Standards
- **Ventilation requirements** based on foam type and temperature
- **Personal protective equipment** recommendations
- **Emergency procedures** for different scenarios
- **Workspace safety guidelines** with volume considerations

## 🧪 Testing

The project includes comprehensive test coverage:

```bash
# Run all tests
pytest tests/ --cov=src/wire_temp_calc --cov-report=term

# Run specific test suite
pytest tests/test_foam_cutting.py

# Run with coverage report
pytest tests/ --cov-report=html
```

**Test Coverage:**
- ✅ Unit conversion accuracy tests
- ✅ Physics behavior verification
- ✅ Safety system validation
- ✅ GUI functionality tests
- ✅ Cross-platform compatibility

## 🏗️ Architecture

```
wire-temperature-calculator/
├── src/wire_temp_calc/          # Core package
│   ├── wire_temp_calculator.py  # Temperature calculations
│   ├── foam_cutting.py         # Foam cutting logic
│   ├── unit_conversions.py     # Unit conversion system
│   ├── main_window.py          # GUI implementation
│   └── cli.py                  # Command line interface
├── tests/                       # Comprehensive test suite
├── docs/                        # Professional documentation
├── scripts/                     # Utility scripts
└── dist/                        # Distribution packages
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Contribution Guide
```bash
# Fork and clone
git clone https://github.com/yourusername/wire-temperature-calculator.git

# Set up development environment
./install.sh
source venv/bin/activate

# Make changes and test
pytest tests/
black src/
flake8 src/

# Submit pull request
```

## 📈 Performance

- **Temperature calculations**: <1ms response time
- **Chart rendering**: 60 FPS smooth interaction
- **Memory efficient**: <100MB typical usage
- **Cross-platform**: Tested on Windows, macOS, Linux

## 📄 Documentation

Comprehensive documentation available at:
- **[Installation Guide](docs/installation/index.md)** - Detailed setup instructions
- **[User Guide](docs/user-guide.md)** - Complete usage guide
- **[API Reference](docs/api/index.md)** - Developer documentation
- **[Safety Guidelines](docs/safety.md)** - Important safety information

## 🐛 Issues & Support

- **Bug Reports**: [GitHub Issues](https://github.com/yourusername/wire-temperature-calculator/issues)
- **Feature Requests**: [GitHub Discussions](https://github.com/yourusername/wire-temperature-calculator/discussions)
- **Security Issues**: security@wiretempcalc.com

## 📜 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **PySide6 Team** for the excellent Qt bindings
- **PyQtGraph Team** for the visualization library
- **Contributors** for their valuable input and testing
- **RC Aircraft Community** for foam cutting expertise

---

<div align="center">

**Made with ❤️ for makers, hobbyists, and professionals worldwide**

[⭐ Star this repo](https://github.com/yourusername/wire-temperature-calculator) if you find it useful!

</div>