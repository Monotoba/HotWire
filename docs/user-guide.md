# User Guide

## Getting Started

### Launching the Application

**GUI Mode (Recommended):**
```bash
# Run the GUI application
./activate_and_run.sh
```

**Command Line Mode:**
```bash
# Basic temperature calculation
wire-temp-calc --gauge 22 --material nichrome --current 1

# Foam cutting mode
wire-temp-calc --foam EPS --wire-diameter 0.644 --cutting-speed 5
```

### Main Interface Overview

![Main Interface](images/main_interface.png)

The application interface consists of:

1. **Wire Specifications Panel** (Top Left)
   - Wire type selection
   - Gauge size and unit input
   - Length and unit input
   - Optional resistance override

2. **Current Range Panel** (Middle Left)
   - Start, end, and step current values
   - Default: 0.1A to 5.0A in 0.1A steps

3. **Foam Cutting Panel** (Bottom Left)
   - Foam type selector
   - Cutting speed input
   - Safety information display

4. **Results Panel** (Top Right)
   - Temperature vs current table
   - Detailed numerical results

5. **Chart Panel** (Bottom Right)
   - Color-coded temperature chart
   - Visual safety indicators
   - Foam cutting zones

## Basic Operations

### 1. Simple Temperature Calculation

**Step 1:** Select Wire Type
- Choose from: Nichrome, Stainless Steel, or Kanthal
- Default: Nichrome (most common for heating applications)

**Step 2:** Enter Wire Size
- **AWG Mode**: Enter gauge number (e.g., 22 for 22 AWG)
- **Metric Mode**: Enter diameter in mm (e.g., 0.644 for 22 AWG equivalent)
- **Imperial Mode**: Enter diameter in mils or inches

**Step 3:** Enter Wire Length
- Select appropriate unit from dropdown
- Common values: 2 feet, 24 inches, 0.61 meters

**Step 4:** Set Current Range
- Default range works for most applications
- Adjust based on your power supply capabilities

**Step 5:** Click Calculate
- Results appear in table and chart
- Chart shows temperature vs current relationship

### 2. Foam Cutting Mode

**Step 1:** Enable Foam Cutting
- Select foam type from dropdown
- Choose "None" to disable foam cutting mode

**Step 2:** Select Foam Type
- **RC Aircraft**: EPP (durable), EPS (lightweight), DEPRON (thin sheets)
- **Craft Projects**: EVA (soft), FOAM_BOARD (presentation), MEMORY (cushioning)
- **Industrial**: XPS (insulation), PU (versatile), NEOPRENE (weather-resistant)

**Step 3:** Set Cutting Speed
- **Slow (1-2 mm/s)**: Maximum precision, detailed work
- **Medium (5 mm/s)**: Standard cutting, balanced approach
- **Fast (8-10 mm/s)**: Production work, rough shapes

**Step 4:** Review Safety Information
- Check optimal temperature range
- Note fire risk level
- Verify ventilation requirements

**Step 5:** Calculate and Cut
- Application shows optimal temperature
- Chart displays safe cutting zone
- Visual indicators help maintain temperature

## Advanced Features

### Custom Resistance Values

For non-standard wires:
1. Enter resistance per foot in Ω/ft
2. Application will use this instead of calculated values
3. Useful for custom alloys or measured values

### Project Management

**Saving Projects:**
1. File → Save Project
2. Choose location and filename
3. All settings including foam type are saved

**Loading Projects:**
1. File → Open Project
2. Select previously saved project file
3. All settings restored including foam cutting mode

### Export Options

**PDF Export:**
1. File → Export as PDF
2. Choose filename and location
3. Professional PDF with charts and data

**Print:**
1. File → Print
2. Configure print settings
3. Optimized for A4 paper

## Foam Cutting Guide

### Foam Type Selection

| Foam Type | Temperature Range | Best For | Characteristics |
|-----------|------------------|----------|-----------------|
| EPP | 220-260°C | RC aircraft | Durable, impact resistant |
| EPS | 180-220°C | Packaging | Lightweight, easy to cut |
| EVA | 190-230°C | Crafts | Soft, flexible |
| XPS | 200-240°C | Insulation | Dense, closed-cell |
| DEPRON | 180-220°C | RC models | Thin, rigid sheets |
| FOAM_BOARD | 160-200°C | Presentations | Paper-faced |
| MEMORY | 150-190°C | Cushioning | Temperature-sensitive |
| NEOPRENE | 180-220°C | Weather sealing | Weather-resistant |

### Cutting Speed Guidelines

| Speed Range | Application | Notes |
|-------------|-------------|-------|
| 1-2 mm/s | Maximum precision | Slow, detailed cuts |
| 3-5 mm/s | Standard cutting | Balanced approach |
| 6-8 mm/s | Production work | Faster, less precise |
| 9-10 mm/s | Rough cutting | Fastest, rough finish |

### Safety Guidelines

**Always:**
- Work in well-ventilated area
- Have fire extinguisher nearby
- Wear safety glasses and gloves
- Start with lower temperatures
- Monitor for smoke or odors

**Temperature Warnings:**
- **Green Zone**: Safe operating range
- **Yellow Zone**: Optimal cutting temperature
- **Red Zone**: Dangerous - risk of decomposition/toxic fumes

**Emergency Procedures:**
- Turn off power immediately if smoke appears
- Ventilate area if strong odors detected
- Allow wire to cool before handling
- Have emergency contact information ready

## Troubleshooting

### Common Issues

**Application Won't Start:**
1. Check Python version (3.10+ required)
2. Verify virtual environment is activated
3. Reinstall dependencies: `pip install -r requirements.txt`

**Chart Not Displaying:**
1. Check display drivers are installed
2. Try different Qt backend: `export QT_QPA_PLATFORM=xcb`
3. Verify sufficient graphics memory

**Incorrect Temperatures:**
1. Verify wire gauge and material selection
2. Check length units are correct
3. Ensure current values are realistic
4. Try with known wire specifications

**Foam Cutting Issues:**
1. Verify foam type selection
2. Check wire diameter is appropriate
3. Ensure cutting speed is reasonable
4. Review safety warnings carefully

### Getting Help

1. Check this user guide first
2. Review the [troubleshooting guide](troubleshooting.md)
3. Search [GitHub Issues](https://github.com/yourusername/wire-temperature-calculator/issues)
4. Create new issue with complete details

## Tips and Best Practices

### Wire Selection
- **Nichrome**: Best for most applications, consistent heating
- **Stainless Steel**: Good for corrosive environments
- **Kanthal**: Highest resistance, good for high temperatures

### Temperature Control
- Start with lower temperatures and increase gradually
- Allow wire to reach steady state before cutting
- Monitor temperature with infrared thermometer if available

### Foam Cutting
- Practice on scrap pieces first
- Use consistent cutting speed
- Keep wire perpendicular to foam surface
- Allow foam to cool before handling

### Maintenance
- Clean wire regularly to remove oxidation
- Check connections for corrosion
- Replace wire if resistance changes significantly
- Store in dry environment