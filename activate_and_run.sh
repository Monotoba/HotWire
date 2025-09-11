#!/bin/bash

# Activation and run script for Wire Temperature Calculator
# This script activates the Python 3.13 venv and runs the application

echo "Wire Temperature Calculator - Python 3.13"
echo "========================================="

# Check if venv exists and is Python 3.13
if [ ! -d "venv" ] || [ ! -f "venv/bin/python" ] || ! "venv/bin/python" --version | grep -q "3.13"; then
    echo "Creating/Updating Python 3.13 virtual environment..."
    rm -rf venv  # Remove old venv if it exists
    python3.13 -m venv venv
fi

# Activate virtual environment
echo "Activating Python 3.13 virtual environment..."
. venv/bin/activate

# Verify Python version
echo "Python version: $(python --version)"

# Check if dependencies are installed
if ! python -c "import PySide6, pyqtgraph, numpy" 2>/dev/null; then
    echo "Installing dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
fi

# Run the application
echo "Starting Wire Temperature Calculator..."
echo ""
python launch.py

# Deactivate virtual environment when done
deactivate