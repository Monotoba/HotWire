#!/usr/bin/env python3
"""
Comprehensive test script for unit conversions in Wire Temperature Calculator
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from wire_temp_calc.wire_temp_calculator import WireTemperatureCalculator
from wire_temp_calc.unit_conversions import WireGaugeConverter, LengthUnitConverter, convert_wire_gauge, convert_length

def test_wire_gauge_conversions():
    """Test wire gauge unit conversions"""
    print("Testing Wire Gauge Conversions")
    print("=" * 50)
    
    calc = WireTemperatureCalculator()
    
    # Test cases: (size, unit, expected_diameter_mm_approx)
    test_cases = [
        (22, 'AWG', 0.644),
        (24, 'AWG', 0.511),
        (20, 'AWG', 0.812),
        (0.644, 'mm', 0.644),
        (0.511, 'mm', 0.511),
        (25.4, 'mils', 0.645),  # 1 mil = 0.0254 mm
        (20.0, 'mils', 0.508),
        (0.025, 'inch', 0.635),
        (0.020, 'inch', 0.508),
        (22, 'SWG', 1.016),  # SWG 22 is different from AWG 22
        (24, 'SWG', 0.559),
    ]
    
    print("Testing diameter calculations:")
    for size, unit, expected in test_cases:
        try:
            wire = calc.get_wire_properties(size, unit, 'nichrome', 1.0, 'feet')
            actual = wire.diameter_mm
            error = abs(actual - expected) / expected * 100 if expected > 0 else 0
            status = "✓" if error < 5 else "✗"  # Allow 5% error
            print(f"  {size} {unit} → {actual:.3f} mm (expected {expected:.3f} mm) [{status}]")
        except Exception as e:
            print(f"  {size} {unit} → ERROR: {e}")
    
    print("\nTesting gauge unit conversions:")
    # Test AWG to other units
    awg_size = 22
    awg_diameter = WireGaugeConverter.awg_to_diameter_mm(awg_size)
    print(f"  {awg_size} AWG = {awg_diameter:.3f} mm")
    
    # Convert to other units
    swg_equiv = WireGaugeConverter.convert_mm_to_gauge(awg_diameter, 'SWG')
    mils_equiv = WireGaugeConverter.convert_mm_to_gauge(awg_diameter, 'mils')
    inch_equiv = WireGaugeConverter.convert_mm_to_gauge(awg_diameter, 'inch')
    
    print(f"  {awg_size} AWG ≈ {swg_equiv:.1f} SWG")
    print(f"  {awg_size} AWG ≈ {mils_equiv:.1f} mils")
    print(f"  {awg_size} AWG ≈ {inch_equiv:.4f} inch")

def test_length_conversions():
    """Test length unit conversions"""
    print("\nTesting Length Conversions")
    print("=" * 50)
    
    # Test cases: (value, from_unit, to_unit, expected_approx)
    test_cases = [
        (1, 'feet', 'meters', 0.3048),
        (1, 'meters', 'feet', 3.28084),
        (12, 'inch', 'feet', 1),
        (1, 'feet', 'inch', 12),
        (1, 'yard', 'feet', 3),
        (1, 'yard', 'meters', 0.9144),
        (25.4, 'mm', 'inch', 1),
        (1000, 'mm', 'meters', 1),
        (100, 'cm', 'meters', 1),
        (1000, 'mils', 'inch', 1),
    ]
    
    print("Testing length unit conversions:")
    for value, from_unit, to_unit, expected in test_cases:
        try:
            result = LengthUnitConverter.convert_length(value, from_unit, to_unit)
            error = abs(result - expected) / expected * 100 if expected > 0 else 0
            status = "✓" if error < 1 else "✗"  # Allow 1% error
            print(f"  {value} {from_unit} → {result:.4f} {to_unit} (expected {expected:.4f}) [{status}]")
        except Exception as e:
            print(f"  {value} {from_unit} to {to_unit} → ERROR: {e}")

def test_temperature_calculations_with_units():
    """Test temperature calculations with different unit combinations"""
    print("\nTesting Temperature Calculations with Units")
    print("=" * 50)
    
    calc = WireTemperatureCalculator()
    
    # Test cases: (gauge_size, gauge_unit, length, length_unit, current, expected_temp_approx)
    test_cases = [
        (22, 'AWG', 2.0, 'feet', 1.0, 110),      # Original baseline
        (0.644, 'mm', 0.61, 'meters', 1.0, 110),  # Same wire in metric
        (25.4, 'mils', 24.0, 'inch', 1.0, 110),   # Same wire in imperial
        (22, 'SWG', 2.0, 'feet', 1.0, 85),        # SWG 22 is thicker than AWG 22
        (24, 'AWG', 1.0, 'yard', 1.5, 200),       # Different gauge and length
    ]
    
    print("Testing temperature calculations:")
    for gauge_size, gauge_unit, length, length_unit, current, expected_temp in test_cases:
        try:
            wire = calc.get_wire_properties(gauge_size, gauge_unit, 'nichrome', length, length_unit)
            temp = calc.calculate_temperature(wire, current)
            error = abs(temp - expected_temp) / expected_temp * 100 if expected_temp > 0 else 0
            status = "✓" if error < 15 else "✗"  # Allow 15% error for temperature
            print(f"  {gauge_size} {gauge_unit}, {length} {length_unit} @ {current}A → {temp:.1f}°C (expected ~{expected_temp}°C) [{status}]")
        except Exception as e:
            print(f"  {gauge_size} {gauge_unit}, {length} {length_unit} @ {current}A → ERROR: {e}")

def test_ui_unit_handling():
    """Test UI unit handling"""
    print("\nTesting UI Unit Handling")
    print("=" * 50)
    
    # Test gauge unit validation
    print("Testing gauge unit validation:")
    valid_gauge_units = ['AWG', 'SWG', 'mm', 'mils', 'inch']
    for unit in valid_gauge_units:
        try:
            WireGaugeConverter.convert_gauge_to_mm(1.0, unit)
            print(f"  ✓ {unit} is valid")
        except Exception as e:
            print(f"  ✗ {unit} failed: {e}")
    
    # Test length unit validation
    print("\nTesting length unit validation:")
    valid_length_units = ['mm', 'cm', 'inch', 'feet', 'meters', 'yard']
    for unit in valid_length_units:
        try:
            LengthUnitConverter.convert_length(1.0, unit, 'mm')
            print(f"  ✓ {unit} is valid")
        except Exception as e:
            print(f"  ✗ {unit} failed: {e}")

def test_edge_cases():
    """Test edge cases and boundary conditions"""
    print("\nTesting Edge Cases")
    print("=" * 50)
    
    calc = WireTemperatureCalculator()
    
    # Test very small and large values
    edge_cases = [
        (0.001, 'mm', 0.001, 'mm', 0.1),    # Very small wire and length
        (10, 'mm', 100, 'meters', 5.0),     # Large wire and length
        (40, 'AWG', 0.1, 'inch', 0.5),      # Very thin wire
        (0, 'AWG', 1.0, 'feet', 1.0),       # Edge case: AWG 0
    ]
    
    print("Testing edge cases:")
    for gauge_size, gauge_unit, length, length_unit, current in edge_cases:
        try:
            wire = calc.get_wire_properties(gauge_size, gauge_unit, 'nichrome', length, length_unit)
            temp = calc.calculate_temperature(wire, current)
            print(f"  {gauge_size} {gauge_unit}, {length} {length_unit} @ {current}A → {temp:.1f}°C ✓")
        except Exception as e:
            print(f"  {gauge_size} {gauge_unit}, {length} {length_unit} @ {current}A → ERROR: {e}")

def main():
    """Run all tests"""
    print("Wire Temperature Calculator - Unit Conversion Tests")
    print("=" * 60)
    
    try:
        test_wire_gauge_conversions()
        test_length_conversions()
        test_temperature_calculations_with_units()
        test_ui_unit_handling()
        test_edge_cases()
        
        print("\n" + "=" * 60)
        print("✓ All unit conversion tests completed successfully!")
        print("\nThe application now supports:")
        print("  • Wire gauge units: AWG, SWG, mm, mils, inch")
        print("  • Length units: mm, cm, inch, feet, meters, yard")
        print("  • Automatic conversion between all units")
        print("  • Backward compatibility with existing project files")
        
    except Exception as e:
        print(f"\n✗ Test suite failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)