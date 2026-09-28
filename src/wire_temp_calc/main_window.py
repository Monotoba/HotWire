#!/usr/bin/env python3
"""
Wire Temperature Calculator GUI
Main application window using PySide6
"""

import sys
from typing import Optional
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QGroupBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QFileDialog,
    QDialog,
    QTextEdit,
    QMessageBox,
)
from PySide6.QtCore import Qt, QTimer, QThread, Signal
from PySide6.QtGui import QPixmap, QPainter, QPageLayout, QPageSize, QAction
from PySide6.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog
import pyqtgraph as pg
from pyqtgraph import PlotWidget
import numpy as np
from datetime import datetime
import os

from .wire_temp_calculator import (
    WireTemperatureCalculator,
    WireProperties,
    ProjectManager,
)
from .foam_cutting import FoamCuttingDatabase, FoamCuttingCalculator


class ChartWidget(QWidget):
    """Custom widget for displaying temperature chart"""

    def __init__(self, foam_db=None):
        super().__init__()
        self.foam_db = foam_db
        self.setup_ui()
        self.chart_data = []

    def setup_ui(self):
        """Setup the chart UI"""
        layout = QVBoxLayout(self)

        # Create plot widget
        self.plot_widget = PlotWidget()
        self.plot_widget.setBackground("white")
        self.plot_widget.setTitle("Wire Temperature vs Current", size="14pt")
        self.plot_widget.setLabel("left", "Temperature", units="°C")
        self.plot_widget.setLabel("bottom", "Current", units="A")
        self.plot_widget.showGrid(x=True, y=True, alpha=0.3)

        layout.addWidget(self.plot_widget)

    def update_chart(
        self,
        chart_data,
        wire_props,
        foam_type: Optional[str] = None,
        optimal_temp: Optional[float] = None,
    ):
        """Update chart with new data"""
        self.chart_data = chart_data

        # Clear previous plot
        self.plot_widget.clear()

        if not chart_data:
            return

        # Extract x and y data
        currents = [point[0] for point in chart_data]
        temperatures = [point[1] for point in chart_data]

        # Create color gradient based on temperature (darker = colder)
        min_temp = min(temperatures)
        max_temp = max(temperatures)
        temp_range = max_temp - min_temp if max_temp != min_temp else 1

        # Plot with color gradient
        for i in range(len(chart_data) - 1):
            temp_ratio = (temperatures[i] - min_temp) / temp_range

            # Create color from blue (cold) to red (hot)
            r = int(255 * temp_ratio)
            b = int(255 * (1 - temp_ratio))
            color = (r, 0, b)

            # Plot line segment
            x_data = [currents[i], currents[i + 1]]
            y_data = [temperatures[i], temperatures[i + 1]]
            self.plot_widget.plot(x_data, y_data, pen=pg.mkPen(color=color, width=2))

        # Add scatter points
        self.plot_widget.plot(
            currents,
            temperatures,
            pen=None,
            symbol="o",
            symbolSize=4,
            symbolBrush="black",
        )

        # Add foam cutting temperature ranges if in foam cutting mode
        if foam_type and optimal_temp:
            # Get foam info from main window's foam database
            foam = self.foam_db.get_foam_type(foam_type)
            if foam:
                # Add temperature range indicators
                self.add_foam_temperature_ranges(foam, min(currents), max(currents))

        # Add info text
        info_text = f"Wire: {wire_props.gauge_size:.3f} {wire_props.gauge_unit} {wire_props.material.title()}\n"
        info_text += f"Length: {wire_props.length:.2f} {wire_props.length_unit}"

        if foam_type:
            # Get foam info from main window's foam database
            foam = self.foam_db.get_foam_type(foam_type)
            if foam:
                info_text += (
                    f"\nFoam: {foam.name} | Optimal: {foam.optimal_temp_celsius}°C"
                )

        text = pg.TextItem(info_text, anchor=(0, 1), color="black")
        text.setPos(max(currents) * 0.02, max(temperatures) * 0.98)
        self.plot_widget.addItem(text)

    def add_foam_temperature_ranges(self, foam, min_current: float, max_current: float):
        """Add foam cutting temperature range indicators to chart"""
        # Add horizontal lines for temperature ranges
        y_min = foam.min_temp_celsius
        y_opt = foam.optimal_temp_celsius
        y_max = foam.max_temp_celsius

        # Safe range (green background)
        safe_range = pg.LinearRegionItem(
            values=[y_min, y_max],
            orientation="horizontal",
            brush=(0, 255, 0, 30),  # Green with transparency
            pen={"color": (0, 255, 0, 100), "width": 1},
        )
        self.plot_widget.addItem(safe_range)

        # Optimal range (yellow background, narrower)
        opt_range = pg.LinearRegionItem(
            values=[y_opt - 5, y_opt + 5],
            orientation="horizontal",
            brush=(255, 255, 0, 40),  # Yellow with transparency
            pen={"color": (255, 255, 0, 150), "width": 1},
        )
        self.plot_widget.addItem(opt_range)

        # Add text labels for ranges
        min_text = pg.TextItem(f"Min: {y_min}°C", anchor=(1, 0), color=(0, 128, 0))
        min_text.setPos(max_current * 0.98, y_min)
        self.plot_widget.addItem(min_text)

        opt_text = pg.TextItem(
            f"Optimal: {y_opt}°C", anchor=(1, 0.5), color=(128, 128, 0)
        )
        opt_text.setPos(max_current * 0.98, y_opt)
        self.plot_widget.addItem(opt_text)

        max_text = pg.TextItem(f"Max: {y_max}°C", anchor=(1, 1), color=(255, 0, 0))
        max_text.setPos(max_current * 0.98, y_max)
        self.plot_widget.addItem(max_text)


class InputPanel(QWidget):
    """Input panel for wire parameters"""

    def __init__(self):
        super().__init__()
        self.foam_db = FoamCuttingDatabase()
        self.setup_ui()

    def setup_ui(self):
        """Setup input panel UI"""
        layout = QGridLayout(self)

        # Wire Type
        layout.addWidget(QLabel("Wire Type:"), 0, 0)
        self.wire_type_combo = QComboBox()
        self.wire_type_combo.addItems(["nichrome", "stainless", "kanthal"])
        layout.addWidget(self.wire_type_combo, 0, 1)

        # Wire Gauge
        layout.addWidget(QLabel("Wire Size:"), 1, 0)
        gauge_layout = QHBoxLayout()
        self.gauge_edit = QLineEdit("22")
        self.gauge_edit.setFixedWidth(80)
        gauge_layout.addWidget(self.gauge_edit)
        self.gauge_unit_combo = QComboBox()
        self.gauge_unit_combo.addItems(["AWG", "SWG", "mm", "mils", "inch"])
        self.gauge_unit_combo.setCurrentText("AWG")
        self.gauge_unit_combo.currentTextChanged.connect(self.on_gauge_unit_changed)
        gauge_layout.addWidget(self.gauge_unit_combo)
        gauge_layout.addStretch()
        layout.addLayout(gauge_layout, 1, 1)

        # Wire Length
        layout.addWidget(QLabel("Wire Length:"), 2, 0)
        length_layout = QHBoxLayout()
        self.length_edit = QLineEdit("2.0")
        self.length_edit.setFixedWidth(80)
        length_layout.addWidget(self.length_edit)
        self.length_unit_combo = QComboBox()
        self.length_unit_combo.addItems(["mm", "cm", "inch", "feet", "meters", "yard"])
        self.length_unit_combo.setCurrentText("feet")
        length_layout.addWidget(self.length_unit_combo)
        length_layout.addStretch()
        layout.addLayout(length_layout, 2, 1)

        # Resistance (optional override)
        layout.addWidget(QLabel("Resistance per foot (Ω):"), 3, 0)
        self.resistance_edit = QLineEdit("")
        self.resistance_edit.setPlaceholderText("Auto-calculated")
        layout.addWidget(self.resistance_edit, 3, 1)

        # Current Range
        current_group = QGroupBox("Current Range")
        current_layout = QGridLayout(current_group)

        current_layout.addWidget(QLabel("Start (A):"), 0, 0)
        self.current_start_edit = QLineEdit("0.1")
        self.current_start_edit.setFixedWidth(60)
        current_layout.addWidget(self.current_start_edit, 0, 1)

        current_layout.addWidget(QLabel("End (A):"), 0, 2)
        self.current_end_edit = QLineEdit("5.0")
        self.current_end_edit.setFixedWidth(60)
        current_layout.addWidget(self.current_end_edit, 0, 3)

        current_layout.addWidget(QLabel("Step (A):"), 0, 4)
        self.current_step_edit = QLineEdit("0.1")
        self.current_step_edit.setFixedWidth(60)
        current_layout.addWidget(self.current_step_edit, 0, 5)

        layout.addWidget(current_group, 4, 0, 1, 2)

        # Foam Cutting Mode
        self.foam_group = QGroupBox("Foam Cutting Mode (Optional)")
        foam_layout = QGridLayout(self.foam_group)

        # Foam type selector
        foam_layout.addWidget(QLabel("Foam Type:"), 0, 0)
        self.foam_type_combo = QComboBox()
        foam_types = ["None"] + self.foam_db.get_foam_names()
        self.foam_type_combo.addItems(foam_types)
        self.foam_type_combo.setCurrentText("None")
        self.foam_type_combo.currentTextChanged.connect(self.on_foam_type_changed)
        foam_layout.addWidget(self.foam_type_combo, 0, 1)

        # Cutting speed
        foam_layout.addWidget(QLabel("Cutting Speed:"), 1, 0)
        speed_layout = QHBoxLayout()
        self.cutting_speed_edit = QLineEdit("5.0")
        self.cutting_speed_edit.setFixedWidth(60)
        speed_layout.addWidget(self.cutting_speed_edit)
        speed_layout.addWidget(QLabel("mm/s"))
        speed_layout.addStretch()
        foam_layout.addLayout(speed_layout, 1, 1)

        # Foam info display
        self.foam_info_label = QLabel("Select a foam type for cutting recommendations")
        self.foam_info_label.setWordWrap(True)
        self.foam_info_label.setStyleSheet("font-size: 9px; color: #666;")
        foam_layout.addWidget(self.foam_info_label, 2, 0, 1, 2)

        layout.addWidget(self.foam_group, 5, 0, 1, 2)

        # Buttons
        button_layout = QHBoxLayout()

        self.calculate_btn = QPushButton("Calculate")
        self.calculate_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        button_layout.addWidget(self.calculate_btn)

        self.reset_btn = QPushButton("Reset")
        button_layout.addWidget(self.reset_btn)

        button_layout.addStretch()
        layout.addLayout(button_layout, 6, 0, 1, 2)

        layout.setRowStretch(8, 1)

    def on_foam_type_changed(self, foam_text: str):
        """Handle foam type selection change"""
        if foam_text == "None":
            self.foam_info_label.setText(
                "Select a foam type for cutting recommendations"
            )
            self.foam_info_label.setStyleSheet("font-size: 9px; color: #666;")
            return

        # Extract foam key from display text
        foam_key = foam_text.split(" - ")[0]
        foam = self.foam_db.get_foam_type(foam_key)

        if foam:
            info = f"Optimal: {foam.optimal_temp_celsius}°C | Range: {foam.min_temp_celsius}-{foam.max_temp_celsius}°C | {foam.cutting_speed.title()} speed"
            self.foam_info_label.setText(info)

            # Update cutting speed recommendation
            if foam.cutting_speed == "slow":
                self.cutting_speed_edit.setText("2.0")
            elif foam.cutting_speed == "very slow":
                self.cutting_speed_edit.setText("1.0")
            elif foam.cutting_speed == "fast":
                self.cutting_speed_edit.setText("10.0")
            else:
                self.cutting_speed_edit.setText("5.0")

            # Color code based on safety
            if foam.cutting_speed in ["slow", "very slow"]:
                self.foam_info_label.setStyleSheet(
                    "font-size: 9px; color: #d9534f;"
                )  # Red for slow
            elif foam.cutting_speed == "fast":
                self.foam_info_label.setStyleSheet(
                    "font-size: 9px; color: #5cb85c;"
                )  # Green for fast
            else:
                self.foam_info_label.setStyleSheet(
                    "font-size: 9px; color: #f0ad4e;"
                )  # Orange for medium
        else:
            self.foam_info_label.setText("Foam type not found")
            self.foam_info_label.setStyleSheet("font-size: 9px; color: #d9534f;")

    def get_foam_type(self) -> str:
        """Get selected foam type"""
        foam_text = self.foam_type_combo.currentText()
        if foam_text == "None":
            return ""
        return foam_text.split(" - ")[0]

    def get_cutting_speed(self) -> float:
        """Get cutting speed"""
        try:
            return float(self.cutting_speed_edit.text())
        except ValueError:
            return 5.0  # Default

    def on_gauge_unit_changed(self, unit: str):
        """Handle gauge unit change - update input field and suggestions"""
        current_text = self.gauge_edit.text()

        if unit == "AWG":
            # For AWG, suggest standard sizes
            self.gauge_edit.setText("22")
        elif unit == "SWG":
            # For SWG, suggest standard sizes
            self.gauge_edit.setText("22")
        elif unit in ["mm", "mils", "inch"]:
            # For diameter units, show current diameter equivalent
            try:
                if (
                    current_text and unit != "AWG"
                ):  # Only convert if we have a value and it's not already AWG
                    # Convert current value to new unit
                    if unit == "mm":
                        self.gauge_edit.setText("0.644")
                    elif unit == "mils":
                        self.gauge_edit.setText("25.4")
                    elif unit == "inch":
                        self.gauge_edit.setText("0.025")
            except ValueError:
                # If conversion fails, set a reasonable default
                if unit == "mm":
                    self.gauge_edit.setText("0.5")
                elif unit == "mils":
                    self.gauge_edit.setText("20.0")
                elif unit == "inch":
                    self.gauge_edit.setText("0.020")

    def get_wire_size(self) -> tuple:
        """Get wire size and unit from input"""
        try:
            size = float(self.gauge_edit.text())
            unit = self.gauge_unit_combo.currentText()
            return size, unit
        except ValueError:
            return 22.0, "AWG"  # Default fallback

    def get_wire_length(self) -> tuple:
        """Get wire length and unit from input"""
        try:
            length = float(self.length_edit.text())
            unit = self.length_unit_combo.currentText()
            return length, unit
        except ValueError:
            return 2.0, "feet"  # Default fallback


class MainWindow(QMainWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()
        self.calculator = WireTemperatureCalculator()
        self.project_manager = ProjectManager()
        self.foam_db = FoamCuttingDatabase()
        self.current_wire_props = None
        self.chart_data = []
        self.foam_type = None
        self.foam_cutting_mode = False

        self.setup_ui()
        self.setup_menu()
        self.connect_signals()

    def setup_ui(self):
        """Setup main UI"""
        self.setWindowTitle("Wire Temperature Calculator")
        self.setGeometry(100, 100, 1200, 800)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QHBoxLayout(central_widget)

        # Left panel - Inputs
        left_panel = QWidget()
        left_panel.setFixedWidth(350)
        left_layout = QVBoxLayout(left_panel)

        self.input_panel = InputPanel()
        left_layout.addWidget(self.input_panel)

        # Results table
        results_group = QGroupBox("Results")
        results_layout = QVBoxLayout(results_group)

        self.results_table = QTableWidget()
        self.results_table.setColumnCount(2)
        self.results_table.setHorizontalHeaderLabels(
            ["Current (A)", "Temperature (°C)"]
        )
        self.results_table.horizontalHeader().setStretchLastSection(True)
        self.results_table.setMaximumHeight(200)
        results_layout.addWidget(self.results_table)

        left_layout.addWidget(results_group)

        # Right panel - Chart
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        self.chart_widget = ChartWidget(foam_db=self.foam_db)
        right_layout.addWidget(self.chart_widget)

        # Add panels to main layout
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel, 1)

    def setup_menu(self):
        """Setup menu bar"""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("File")

        new_action = QAction("New Project", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_project)
        file_menu.addAction(new_action)

        open_action = QAction("Open Project...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_project)
        file_menu.addAction(open_action)

        save_action = QAction("Save Project", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_project)
        file_menu.addAction(save_action)

        save_as_action = QAction("Save Project As...", self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.triggered.connect(self.save_project_as)
        file_menu.addAction(save_as_action)

        file_menu.addSeparator()

        export_pdf_action = QAction("Export as PDF...", self)
        export_pdf_action.setShortcut("Ctrl+E")
        export_pdf_action.triggered.connect(self.export_pdf)
        file_menu.addAction(export_pdf_action)

        file_menu.addSeparator()

        print_action = QAction("Print...", self)
        print_action.setShortcut("Ctrl+P")
        print_action.triggered.connect(self.print_chart)
        file_menu.addAction(print_action)

        file_menu.addSeparator()

        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Help menu
        help_menu = menubar.addMenu("Help")

        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def connect_signals(self):
        """Connect UI signals"""
        self.input_panel.calculate_btn.clicked.connect(self.calculate_temperatures)
        self.input_panel.reset_btn.clicked.connect(self.reset_inputs)

    def calculate_temperatures(self):
        """Calculate temperatures for current range"""
        try:
            # Get input values
            wire_type = self.input_panel.wire_type_combo.currentText()
            gauge_size, gauge_unit = self.input_panel.get_wire_size()
            length, length_unit = self.input_panel.get_wire_length()

            # Get foam cutting parameters
            foam_type = self.input_panel.get_foam_type()
            cutting_speed = self.input_panel.get_cutting_speed()
            self.foam_type = foam_type if foam_type else None
            self.foam_cutting_mode = bool(foam_type)

            # Get current range
            current_start = float(self.input_panel.current_start_edit.text())
            current_end = float(self.input_panel.current_end_edit.text())
            current_step = float(self.input_panel.current_step_edit.text())

            # Validate inputs
            if current_start >= current_end:
                QMessageBox.warning(
                    self, "Invalid Input", "Start current must be less than end current"
                )
                return

            if current_step <= 0:
                QMessageBox.warning(
                    self, "Invalid Input", "Current step must be positive"
                )
                return

            # Get wire properties using new unit system
            self.current_wire_props = self.calculator.get_wire_properties(
                gauge_size, gauge_unit, wire_type, length, length_unit
            )

            # If in foam cutting mode, calculate optimal temperature and provide recommendations
            if self.foam_cutting_mode and self.foam_type:
                optimal_temp = self.calculator.calculate_foam_cutting_temperature(
                    self.foam_type, self.current_wire_props, cutting_speed
                )

                # Check if current temperature range is appropriate for foam cutting
                self.check_foam_cutting_safety(optimal_temp)

                # Update chart info with foam cutting recommendations
                self.update_foam_cutting_info(optimal_temp)

            # Override resistance if specified
            resistance_text = self.input_panel.resistance_edit.text().strip()
            if resistance_text:
                try:
                    resistance_override = float(resistance_text)
                    self.current_wire_props.resistance_per_foot = resistance_override
                    self.current_wire_props.resistance_per_meter = (
                        resistance_override * 3.28084
                    )
                except ValueError:
                    QMessageBox.warning(
                        self, "Invalid Input", "Invalid resistance value"
                    )
                    return

            # Calculate temperatures
            self.chart_data = self.calculator.generate_temperature_chart(
                self.current_wire_props, current_start, current_end, current_step
            )

            # Update chart with foam cutting information if applicable
            self.chart_widget.update_chart(
                self.chart_data,
                self.current_wire_props,
                self.foam_type,
                optimal_temp if self.foam_cutting_mode else None,
            )

            # Update results table
            self.update_results_table()

        except ValueError as e:
            QMessageBox.warning(
                self, "Invalid Input", f"Please check your input values: {str(e)}"
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

    def check_foam_cutting_safety(self, optimal_temp: float):
        """Check foam cutting safety and show warnings"""
        if not self.foam_type:
            return

        # Check if temperature range is safe for foam
        max_temp_in_range = (
            max([temp for _, temp in self.chart_data]) if self.chart_data else 0
        )

        if not self.calculator.is_foam_cutting_mode_safe(
            self.foam_type, max_temp_in_range
        ):
            warning = self.calculator.get_foam_safety_warning(
                self.foam_type, max_temp_in_range
            )
            if warning:
                QMessageBox.warning(self, "Foam Cutting Safety Warning", warning)

        # Check if optimal temperature is within the calculated range
        min_temp_in_range = (
            min([temp for _, temp in self.chart_data]) if self.chart_data else 0
        )

        if optimal_temp < min_temp_in_range or optimal_temp > max_temp_in_range:
            suggestion = f"For {self.foam_type} foam cutting, consider using a current range that produces {optimal_temp:.1f}°C for optimal results."
            QMessageBox.information(self, "Foam Cutting Recommendation", suggestion)

    def update_foam_cutting_info(self, optimal_temp: float):
        """Update chart with foam cutting information"""
        if not self.foam_type or not self.chart_data:
            return

        foam_info = self.calculator.get_foam_cutting_info(self.foam_type)
        if not foam_info:
            return

        # Add foam cutting information to chart
        foam = self.foam_db.get_foam_type(self.foam_type)
        if foam:
            info_text = f"Foam: {foam.name} | Optimal: {foam.optimal_temp_celsius}°C | Range: {foam.min_temp_celsius}-{foam.max_temp_celsius}°C"

            # Add this info to the chart (will be implemented in chart update)
            pass

    def update_results_table(self):
        """Update results table with chart data"""
        self.results_table.setRowCount(len(self.chart_data))

        for row, (current, temp) in enumerate(self.chart_data):
            self.results_table.setItem(row, 0, QTableWidgetItem(f"{current:.1f}"))
            self.results_table.setItem(row, 1, QTableWidgetItem(f"{temp:.1f}"))

    def reset_inputs(self):
        """Reset input fields to defaults"""
        self.input_panel.wire_type_combo.setCurrentText("nichrome")
        self.input_panel.gauge_edit.setText("22")
        self.input_panel.gauge_unit_combo.setCurrentText("AWG")
        self.input_panel.length_edit.setText("2.0")
        self.input_panel.length_unit_combo.setCurrentText("feet")
        self.input_panel.resistance_edit.clear()
        self.input_panel.current_start_edit.setText("0.1")
        self.input_panel.current_end_edit.setText("5.0")
        self.input_panel.current_step_edit.setText("0.1")
        self.input_panel.foam_type_combo.setCurrentText("None")
        self.input_panel.cutting_speed_edit.setText("5.0")
        self.foam_type = None
        self.foam_cutting_mode = False

    def new_project(self):
        """Create new project"""
        self.reset_inputs()
        self.chart_widget.plot_widget.clear()
        self.results_table.setRowCount(0)
        self.current_wire_props = None
        self.chart_data = []
        self.foam_type = None
        self.foam_cutting_mode = False

    def open_project(self):
        """Open project file"""
        filename, _ = QFileDialog.getOpenFileName(
            self, "Open Project", "", "JSON Files (*.json)"
        )

        if filename:
            try:
                (
                    wire_props,
                    current_range,
                    foam_type,
                    cutting_mode,
                ) = self.project_manager.load_project(filename)
                self.current_wire_props = wire_props
                self.foam_type = foam_type
                self.foam_cutting_mode = cutting_mode

                # Update UI with loaded values
                self.input_panel.wire_type_combo.setCurrentText(wire_props.material)
                self.input_panel.gauge_edit.setText(f"{wire_props.gauge_size:.3f}")
                self.input_panel.gauge_unit_combo.setCurrentText(wire_props.gauge_unit)
                self.input_panel.resistance_edit.setText(
                    f"{wire_props.resistance_per_foot:.4f}"
                )

                # Set length and unit
                self.input_panel.length_edit.setText(f"{wire_props.length:.3f}")
                self.input_panel.length_unit_combo.setCurrentText(
                    wire_props.length_unit
                )

                # Set current range
                self.input_panel.current_start_edit.setText(
                    f"{current_range['start']:.1f}"
                )
                self.input_panel.current_end_edit.setText(f"{current_range['end']:.1f}")
                self.input_panel.current_step_edit.setText(
                    f"{current_range['step']:.1f}"
                )

                # Set foam cutting parameters
                if foam_type:
                    foam_display = (
                        f"{foam_type} - {self.foam_db.get_foam_type(foam_type).name}"
                    )
                    self.input_panel.foam_type_combo.setCurrentText(foam_display)
                else:
                    self.input_panel.foam_type_combo.setCurrentText("None")

                # Recalculate
                self.calculate_temperatures()

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load project: {str(e)}")

    def save_project(self):
        """Save current project"""
        if not self.current_wire_props:
            QMessageBox.warning(self, "No Data", "No calculation data to save")
            return

        filename, _ = QFileDialog.getSaveFileName(
            self, "Save Project", "", "JSON Files (*.json)"
        )

        if filename:
            try:
                current_range = {
                    "start": float(self.input_panel.current_start_edit.text()),
                    "end": float(self.input_panel.current_end_edit.text()),
                    "step": float(self.input_panel.current_step_edit.text()),
                }

                self.project_manager.save_project(
                    filename,
                    self.current_wire_props,
                    current_range,
                    self.foam_type,
                    self.foam_cutting_mode,
                )
                QMessageBox.information(self, "Success", "Project saved successfully")

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save project: {str(e)}")

    def save_project_as(self):
        """Save project with different filename"""
        self.save_project()

    def export_pdf(self):
        """Export chart as PDF"""
        if not self.chart_data:
            QMessageBox.warning(self, "No Data", "No chart data to export")
            return

        filename, _ = QFileDialog.getSaveFileName(
            self, "Export PDF", "", "PDF Files (*.pdf)"
        )

        if filename:
            try:
                printer = QPrinter(QPrinter.HighResolution)
                printer.setOutputFormat(QPrinter.PdfFormat)
                printer.setOutputFileName(filename)
                printer.setPageSize(QPageSize(QPageSize.A4))
                printer.setOrientation(QPageLayout.Landscape)

                self.print_chart_to_printer(printer)
                QMessageBox.information(self, "Success", "PDF exported successfully")

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export PDF: {str(e)}")

    def print_chart(self):
        """Print chart using system dialog"""
        if not self.chart_data:
            QMessageBox.warning(self, "No Data", "No chart data to print")
            return

        printer = QPrinter(QPrinter.HighResolution)
        printer.setPageSize(QPageSize(QPageSize.A4))
        printer.setOrientation(QPageLayout.Landscape)

        dialog = QPrintDialog(printer, self)
        if dialog.exec() == QPrintDialog.Accepted:
            try:
                self.print_chart_to_printer(printer)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to print: {str(e)}")

    def print_chart_to_printer(self, printer):
        """Print chart to given printer"""
        painter = QPainter()
        painter.begin(printer)

        # Get chart pixmap
        pixmap = self.chart_widget.plot_widget.grab()

        # Scale to fit page
        page_rect = printer.pageRect(QPrinter.DevicePixel)
        scaled_pixmap = pixmap.scaled(
            page_rect.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
        )

        # Center on page
        x = (page_rect.width() - scaled_pixmap.width()) // 2
        y = (page_rect.height() - scaled_pixmap.height()) // 2

        painter.drawPixmap(x, y, scaled_pixmap)

        # Add title and info
        painter.setPen(Qt.black)
        font = painter.font()
        font.setPointSize(12)
        font.setBold(True)
        painter.setFont(font)

        title = f"Wire Temperature Chart - {self.current_wire_props.gauge} AWG {self.current_wire_props.material.title()}"
        painter.drawText(page_rect.width() // 2 - 200, 30, title)

        # Add date
        font.setPointSize(8)
        font.setBold(False)
        painter.setFont(font)
        painter.drawText(
            page_rect.width() - 200,
            page_rect.height() - 20,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        )

        painter.end()

    def show_about(self):
        """Show about dialog"""
        about_text = """
        <h3>Wire Temperature Calculator</h3>
        <p>Version 1.0</p>
        <p>This application calculates wire temperature based on current, 
        wire type, and physical properties.</p>
        <p>Supports Nichrome and Stainless Steel wires in various gauges.</p>
        <p>© 2024 - Open Source Application</p>
        """

        QMessageBox.about(self, "About", about_text)


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Wire Temperature Calculator")
    app.setOrganizationName("WireCalc")

    # Set application style
    app.setStyle("Fusion")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
