#!/usr/bin/env python3
"""
Simple launcher for Wire Temperature Calculator
"""

import sys
import os

# Add src directory to path for package imports
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

try:
    from wire_temp_calc.main import main
    main()
except ImportError as e:
    print(f"Error importing required modules: {e}")
    print("Please install dependencies with: pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"Error starting application: {e}")
    sys.exit(1)