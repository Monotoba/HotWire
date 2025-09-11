#!/usr/bin/env python3
"""
Debug script to check length unit conversions
"""

from unit_conversions import LengthUnitConverter
from wire_temp_calculator import WireTemperatureCalculator

def debug_length_conversions():
    """Debug length unit conversions"""
    print("Debugging Length Unit Conversions")
    print("=" * 50)
    
    # Test basic conversions
    test_cases = [
        (2.0, 'feet'),
        (24.0, 'inch'),
        (0.6096, 'meters'),
        (609.6, 'mm'),
    ]
    
    print("Basic length conversions to meters:")
    for value, unit in test_cases:
        meters = LengthUnitConverter.to_mm(value, unit) / 1000
        print(f"  {value} {unit} = {meters:.4f} meters")
    
    print("\nExpected: All should be approximately 0.6096 meters")
    
    # Test with calculator
    print("\nTesting with calculator:")
    calc = WireTemperatureCalculator()
    
    for value, unit in test_cases:
        try:
            wire = calc.get_wire_properties(22, 'AWG', 'nichrome', value, unit)
            print(f"  {value} {unit}:")
            print(f"    Length: {wire.length} {wire.length_unit}")
            print(f"    Diameter: {wire.diameter_mm} mm")
            print(f"    Resistance per foot: {wire.resistance_per_foot:.4f} Ω/ft")
            print(f"    Resistance per meter: {wire.resistance_per_meter:.4f} Ω/m")
            
            # Calculate temperature
            temp = calc.calculate_temperature(wire, 1.0)
            print(f"    Temperature @ 1A: {temp:.1f}°C")
            
        except Exception as e:
            print(f"  {value} {unit}: ERROR - {e}")
        print()

if __name__ == "__main__":
    debug_length_conversions()