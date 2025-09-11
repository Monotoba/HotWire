#!/bin/bash

# Installation script for Wire Temperature Calculator

echo "Wire Temperature Calculator - Installation Script"
echo "================================================="

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
required_version="3.10"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "Error: Python 3.10 or higher is required. Found: $python_version"
    exit 1
fi

echo "Python version check passed: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

# Make scripts executable
echo "Setting up executable permissions..."
chmod +x launch.py
chmod +x test_calculator.py

echo ""
echo "Installation completed successfully!"
echo ""
echo "To run the application:"
echo "  source venv/bin/activate"
echo "  python launch.py"
echo ""
echo "Or simply:"
echo "  ./launch.py"
echo ""