"""Headless integration checks for GUI calculations and file actions."""

import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest
from PySide6.QtWidgets import QApplication, QFileDialog, QMessageBox

from wire_temp_calc.main_window import MainWindow


@pytest.fixture(scope="module")
def app():
    application = QApplication.instance() or QApplication([])
    yield application


@pytest.fixture
def window(app, monkeypatch):
    messages = []
    monkeypatch.setattr(
        QMessageBox, "warning", lambda *args: messages.append(("warning", args[2]))
    )
    monkeypatch.setattr(
        QMessageBox,
        "information",
        lambda *args: messages.append(("information", args[2])),
    )
    monkeypatch.setattr(
        QMessageBox, "critical", lambda *args: messages.append(("critical", args[2]))
    )
    main_window = MainWindow()
    yield main_window, messages
    main_window.close()


def test_foam_warning_uses_fresh_chart_on_first_and_second_calculation(
    window, monkeypatch
):
    main_window, messages = window
    main_window.input_panel.foam_type_combo.setCurrentIndex(2)  # EPS
    assert main_window.input_panel.get_foam_type() == "EPS"
    checked_temperatures = []
    original_check = main_window.calculator.is_foam_cutting_mode_safe

    def record_check(foam_type, temperature):
        checked_temperatures.append(temperature)
        return original_check(foam_type, temperature)

    monkeypatch.setattr(
        main_window.calculator, "is_foam_cutting_mode_safe", record_check
    )
    main_window.input_panel.current_start_edit.setText("4")
    main_window.input_panel.current_end_edit.setText("5")
    main_window.calculate_temperatures()
    assert main_window.chart_data
    assert main_window.results_table.rowCount() == len(main_window.chart_data)
    assert checked_temperatures == [max(temp for _, temp in main_window.chart_data)]
    assert not any(kind == "critical" for kind, _ in messages)

    messages.clear()
    main_window.input_panel.current_start_edit.setText("0.1")
    main_window.input_panel.current_end_edit.setText("0.2")
    main_window.calculate_temperatures()
    assert checked_temperatures[-1] == max(temp for _, temp in main_window.chart_data)
    assert checked_temperatures[0] != checked_temperatures[1]


def test_project_save_open_restores_metric_inputs(window, monkeypatch, tmp_path):
    main_window, messages = window
    main_window.input_panel.gauge_unit_combo.setCurrentText("mm")
    main_window.input_panel.gauge_edit.setText("0.7")
    main_window.input_panel.length_unit_combo.setCurrentText("cm")
    main_window.input_panel.length_edit.setText("60")
    main_window.calculate_temperatures()
    project = tmp_path / "project.json"
    monkeypatch.setattr(
        QFileDialog, "getSaveFileName", lambda *args: (str(project), "")
    )
    main_window.save_project()
    assert project.is_file()
    assert any(kind == "information" and "saved" in text for kind, text in messages)

    main_window.new_project()
    monkeypatch.setattr(
        QFileDialog, "getOpenFileName", lambda *args: (str(project), "")
    )
    main_window.open_project()
    assert main_window.current_wire_props.gauge_size == pytest.approx(0.7)
    assert main_window.current_wire_props.gauge_unit == "mm"
    assert main_window.current_wire_props.length == pytest.approx(60)
    assert main_window.results_table.rowCount() > 0
    assert not any(kind == "critical" for kind, _ in messages)


def test_export_pdf_contains_chart_and_wire_title(window, monkeypatch, tmp_path):
    main_window, messages = window
    main_window.calculate_temperatures()
    pdf = tmp_path / "chart.pdf"
    monkeypatch.setattr(QFileDialog, "getSaveFileName", lambda *args: (str(pdf), ""))
    main_window.export_pdf()
    assert pdf.read_bytes().startswith(b"%PDF-")
    assert pdf.stat().st_size > 1_000
    assert any(kind == "information" and "exported" in text for kind, text in messages)
    assert not any(kind == "critical" for kind, _ in messages)
