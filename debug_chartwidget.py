#!/usr/bin/env python3
"""
Debug script to find the ChartWidget foam_db issue
"""

import sys

sys.path.insert(0, "src")

from wire_temp_calc import WireTemperatureCalculator, FoamCuttingCalculator
from wire_temp_calc.main_window import MainWindow, ChartWidget
from wire_temp_calc.foam_cutting import FoamCuttingDatabase


def test_chartwidget_specifically():
    """Test ChartWidget functionality step by step"""
    print("Testing ChartWidget step by step...")

    try:
        # Create foam database for ChartWidget
        foam_db = FoamCuttingDatabase()

        # Test basic ChartWidget creation
        chart_widget = ChartWidget(foam_db=foam_db)
        print("✅ ChartWidget created successfully")

        # Test basic chart update
        calc = WireTemperatureCalculator()
        wire = calc.get_wire_properties(22, "AWG", "nichrome", 2.0, "feet")
        chart_data = calc.generate_temperature_chart(wire, 0.1, 2.0, 0.1)

        print(f"✅ Generated {len(chart_data)} data points")

        # Test chart update with foam
        foam_calc = FoamCuttingCalculator()
        optimal_temp = foam_calc.calculate_optimal_wire_temperature("EPP", 0.644, 5.0)

        print(f"✅ EPP optimal temperature: {optimal_temp:.1f}°C")

        # Test the specific update_chart call
        chart_widget.update_chart(chart_data, wire, "EPP", optimal_temp)
        print("✅ ChartWidget.update_chart() completed successfully")

    except Exception as e:
        print(f"❌ Error in ChartWidget: {e}")
        import traceback

        traceback.print_exc()
        return False

    return True


if __name__ == "__main__":
    success = test_chartwidget_specifically()
    if success:
        print("✅ ChartWidget functionality working correctly!")
    else:
        print("❌ ChartWidget has issues that need fixing")
