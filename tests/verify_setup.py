#!/usr/bin/env python3
"""
Setup verification script for Wire Temperature Calculator
Verifies Python version, virtual environment, and dependencies
"""

import sys
import os
import subprocess
import importlib

def check_python_version():
    """Check Python version"""
    print("Checking Python version...")
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor >= 10:
        print("✓ Python version is compatible (3.10+)")
        return True
    else:
        print("✗ Python 3.10 or higher is required")
        return False

def check_virtual_environment():
    """Check if running in virtual environment"""
    print("\nChecking virtual environment...")
    
    # Check if we're in a venv
    in_venv = (
        hasattr(sys, 'real_prefix') or
        (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    )
    
    if in_venv:
        print("✓ Running in virtual environment")
        print(f"Virtual environment path: {sys.prefix}")
        return True
    else:
        print("⚠ Not running in virtual environment")
        print("It's recommended to use the virtual environment for isolation")
        return False

def check_dependencies():
    """Check if all dependencies are installed"""
    print("\nChecking dependencies...")
    
    required_packages = [
        ('PySide6', 'PySide6>=6.5.0'),
        ('pyqtgraph', 'pyqtgraph>=0.13.0'),
        ('numpy', 'numpy>=1.24.0')
    ]
    
    all_ok = True
    
    for package, requirement in required_packages:
        try:
            module = importlib.import_module(package)
            if hasattr(module, '__version__'):
                version = module.__version__
                print(f"✓ {package} version {version}")
            else:
                print(f"✓ {package} (version unknown)")
        except ImportError:
            print(f"✗ {package} not installed")
            all_ok = False
    
    return all_ok

def check_application_files():
    """Check if all application files exist"""
    print("\nChecking application files...")
    
    required_files = [
        'wire_temp_calculator.py',
        'main_window.py',
        'launch.py',
        'requirements.txt'
    ]
    
    all_ok = True
    
    for filename in required_files:
        if os.path.exists(filename):
            print(f"✓ {filename}")
        else:
            print(f"✗ {filename} missing")
            all_ok = False
    
    return all_ok

def test_calculator():
    """Test the calculator functionality"""
    print("\nTesting calculator functionality...")
    
    try:
        from wire_temp_calculator import WireTemperatureCalculator
        
        calc = WireTemperatureCalculator()
        wire = calc.get_default_wire_properties(22, 'nichrome', 2.0)
        temp = calc.calculate_temperature(wire, 1.0)
        
        print(f"✓ Calculator working (22 AWG Nichrome @ 1A = {temp:.1f}°C)")
        return True
        
    except Exception as e:
        print(f"✗ Calculator test failed: {e}")
        return False

def main():
    """Main verification function"""
    print("Wire Temperature Calculator - Setup Verification")
    print("=" * 50)
    
    checks = [
        ("Python Version", check_python_version()),
        ("Virtual Environment", check_virtual_environment()),
        ("Dependencies", check_dependencies()),
        ("Application Files", check_application_files()),
        ("Calculator Test", test_calculator())
    ]
    
    print("\n" + "=" * 50)
    print("Verification Summary:")
    
    all_passed = True
    for check_name, result in checks:
        status = "PASS" if result else "FAIL"
        print(f"{check_name}: {status}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 50)
    
    if all_passed:
        print("✓ All checks passed! The application is ready to use.")
        print("\nTo run the application:")
        print("  Linux/Mac: ./activate_and_run.sh")
        print("  Windows: activate_and_run.bat")
        print("  Or manually: . venv/bin/activate && python launch.py")
    else:
        print("✗ Some checks failed. Please review the issues above.")
        print("\nTo fix issues:")
        print("1. Ensure Python 3.10+ is installed")
        print("2. Create virtual environment: python3.13 -m venv venv")
        print("3. Install dependencies: . venv/bin/activate && pip install -r requirements.txt")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)