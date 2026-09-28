#!/usr/bin/env python3
"""
Test script to verify GUI imports work correctly
"""

def check_pyside6_imports():
    """Test all PySide6 imports used in the application"""
    print("Testing PySide6 imports...")
    
    try:
        # Core widgets
        from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                                      QHBoxLayout, QGridLayout, QLabel, QLineEdit, 
                                      QComboBox, QPushButton, QGroupBox, QTableWidget,
                                      QTableWidgetItem, QHeaderView, QFileDialog,
                                      QDialog, QTextEdit, QMessageBox)
        print("✓ QtWidgets imports successful")
        
        # Core modules
        from PySide6.QtCore import Qt, QTimer, QThread, Signal
        print("✓ QtCore imports successful")
        
        # GUI elements
        from PySide6.QtGui import QPixmap, QPainter, QPageLayout, QPageSize, QAction
        print("✓ QtGui imports successful")
        
        # Print support (this was the problematic import)
        from PySide6.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog
        print("✓ QtPrintSupport imports successful")
        
        # pyqtgraph
        import pyqtgraph as pg
        from pyqtgraph import PlotWidget
        print("✓ pyqtgraph imports successful")
        
        # numpy
        import numpy as np
        print("✓ numpy imports successful")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def check_application_import():
    """Test importing the main application"""
    print("\nTesting application import...")
    
    try:
        from wire_temp_calc.main_window import MainWindow, ChartWidget, InputPanel
        print("✓ Main application imports successful")
        
        from wire_temp_calc.wire_temp_calculator import WireTemperatureCalculator, WireProperties, ProjectManager
        print("✓ Calculator imports successful")
        
        return True
        
    except ImportError as e:
        print(f"✗ Application import error: {e}")
        return False

def main():
    """Main test function"""
    print("GUI Import Test - Wire Temperature Calculator")
    print("=" * 50)
    
    # Test basic imports
    imports_ok = check_pyside6_imports()
    
    # Test application imports
    app_ok = check_application_import()
    
    print("\n" + "=" * 50)
    
    if imports_ok and app_ok:
        print("✓ All imports successful! The GUI should work correctly.")
        print("\nYou can now run:")
        print("  ./activate_and_run.sh")
        print("  or")
        print("  . venv/bin/activate && python launch.py")
    else:
        print("✗ Some imports failed. Please check the errors above.")
        print("\nTry reinstalling dependencies:")
        print("  . venv/bin/activate && pip install --force-reinstall -r requirements.txt")
    
    return imports_ok and app_ok


def test_pyside6_imports():
    assert check_pyside6_imports()


def test_application_import():
    assert check_application_import()

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
