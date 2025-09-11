# Wire Temperature Calculator - Quick Start Guide

## Installation

### Option 1: Automated Installation (Recommended)
```bash
./install.sh
```

### Option 2: Manual Installation
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Running the Application

### Method 1: Using the launcher
```bash
./launch.py
```

### Method 2: Direct Python execution
```bash
python main_window.py
```

## Basic Usage

1. **Select Wire Parameters**:
   - Choose wire type (Nichrome or Stainless Steel)
   - Select wire gauge (20-30 AWG)
   - Enter wire length (feet or meters)

2. **Set Current Range**:
   - Start current: 0.1A (default)
   - End current: 5.0A (default)
   - Step: 0.1A (default)

3. **Calculate**:
   - Click "Calculate" button
   - View color-coded chart (darker = colder)
   - Check results table for exact values

## Advanced Features

### Custom Resistance
- Enter custom resistance per foot in the resistance field
- Leave blank to use calculated values

### Project Files
- **Save**: Ctrl+S to save current configuration
- **Open**: Ctrl+O to load saved project
- **New**: Ctrl+N to start fresh

### Export Options
- **PDF Export**: Ctrl+E to export chart as PDF
- **Print**: Ctrl+P to print chart (A4 landscape)

## Color Coding

The chart uses a blue-to-red gradient:
- **Blue/Dark**: Lower temperatures (colder)
- **Red/Bright**: Higher temperatures (hotter)

## Example Results

For 22 AWG Nichrome wire, 2 feet long:
- 1.0A → ~111°C
- 2.0A → ~273°C
- 3.0A → ~460°C

## Troubleshooting

### Application won't start
- Check Python version: `python3 --version` (requires 3.10+)
- Install dependencies: `pip install -r requirements.txt`

### Charts not displaying
- Ensure all input values are valid numbers
- Check that current range is logical (start < end)

### Print/PDF issues
- Verify system has printer configured
- Check file permissions for PDF export location

## Technical Notes

- Calculations assume 20°C ambient temperature
- Uses thermal equilibrium equations
- Considers both convective and radiative heat transfer
- Iterative solution for temperature-dependent resistance

## Keyboard Shortcuts

- **Ctrl+N**: New project
- **Ctrl+O**: Open project
- **Ctrl+S**: Save project
- **Ctrl+E**: Export PDF
- **Ctrl+P**: Print
- **Ctrl+Q**: Quit