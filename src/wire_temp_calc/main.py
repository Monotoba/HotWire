#!/usr/bin/env python3
"""
Wire Temperature Calculator - Main entry point
Professional foam cutting and wire heating calculator
"""

import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from .main_window import MainWindow


def main():
    """Main entry point for the Wire Temperature Calculator"""
    # Create QApplication
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    # Set application properties
    app.setApplicationName("Wire Temperature Calculator")
    from . import __version__

    app.setApplicationVersion(__version__)
    app.setOrganizationName("WireTempCalc")
    app.setOrganizationDomain("wiretempcalc.com")

    # Set application style
    app.setStyle("Fusion")

    # Create and show main window
    window = MainWindow()
    window.show()

    # Run the application
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
