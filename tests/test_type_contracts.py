from wire_temp_calc.unit_conversions import WireGaugeConverter
from wire_temp_calc.wire_temp_calculator import WireTemperatureCalculator


def test_exact_diameter_matches_standard_gauges():
    assert WireGaugeConverter.diameter_mm_to_awg(WireGaugeConverter.AWG_TO_MM[22]) == 22
    assert WireGaugeConverter.diameter_mm_to_swg(WireGaugeConverter.SWG_TO_MM[22]) == 22


def test_unknown_gauge_unit_has_no_standard_sizes():
    assert WireGaugeConverter.get_standard_gauge_sizes("unsupported") == []


def test_integral_float_awg_uses_standard_specification():
    calculator = WireTemperatureCalculator()
    integer_gauge = calculator.get_wire_properties(22, "AWG", "nichrome", 2.0, "feet")
    float_gauge = calculator.get_wire_properties(22.0, "AWG", "nichrome", 2.0, "feet")
    assert float_gauge == integer_gauge
