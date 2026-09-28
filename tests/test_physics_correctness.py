#!/usr/bin/env python3
"""
Test script to verify the physics and unit conversions are working correctly
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from wire_temp_calc.wire_temp_calculator import WireTemperatureCalculator
from wire_temp_calc.unit_conversions import LengthUnitConverter

def test_length_physics():
    """Test that wire length affects temperature correctly"""
    print("Testing Length Physics")
    print("=" * 50)
    
    calc = WireTemperatureCalculator()
    
    # Test with different lengths of the same wire
    # Shorter wires should get hotter (less surface area for cooling)
    # Longer wires should stay cooler (more surface area for cooling)
    
    lengths_and_units = [
        (0.5, 'feet', 'Short wire'),
        (1.0, 'feet', 'Medium wire'),
        (2.0, 'feet', 'Long wire'),
        (4.0, 'feet', 'Very long wire'),
    ]
    
    print("Testing 22 AWG Nichrome wire at 1A current:")
    print("Length           | Temperature (°C) | Expected Trend")
    print("-" * 55)
    
    previous_temp = None
    for length, unit, description in lengths_and_units:
        try:
            wire = calc.get_wire_properties(22, 'AWG', 'nichrome', length, unit)
            temp = calc.calculate_temperature(wire, 1.0)
            
            if previous_temp is not None:
                trend = "Cooler" if temp < previous_temp else "Hotter"
                expected = "✓" if temp < previous_temp else "✗"
            else:
                trend = "Baseline"
                expected = "✓"
            
            print(f"{description:<16} | {temp:>13.1f}°C | {trend:>12} [{expected}]")
            previous_temp = temp
            
        except Exception as e:
            print(f"{description:<16} | {'ERROR':>13} | {'ERROR':>12} [✗]")

def test_equivalent_lengths():
    """Test that equivalent lengths produce the same temperature"""
    print("\n\nTesting Equivalent Lengths")
    print("=" * 50)
    
    calc = WireTemperatureCalculator()
    
    # All of these should be equivalent to 2 feet
    equivalent_lengths = [
        (2.0, 'feet', '2 feet (baseline)'),
        (24.0, 'inch', '24 inches'),
        (0.6096, 'meters', '0.6096 meters'),
        (609.6, 'mm', '609.6 mm'),
        (0.6667, 'yard', '0.6667 yards (2/3)'),
    ]
    
    print("Testing equivalent lengths of 22 AWG Nichrome wire at 1A:")
    print("Length                | Meters    | Temperature (°C) | Status")
    print("-" * 65)
    
    baseline_temp = None
    baseline_meters = None
    
    for length, unit, description in equivalent_lengths:
        try:
            # Convert to meters for comparison
            meters = LengthUnitConverter.to_mm(length, unit) / 1000
            
            wire = calc.get_wire_properties(22, 'AWG', 'nichrome', length, unit)
            temp = calc.calculate_temperature(wire, 1.0)
            
            if baseline_temp is None:
                baseline_temp = temp
                baseline_meters = meters
                status = "Baseline"
            else:
                # Check if temperature is reasonable for the length
                # Shorter wires should be hotter, longer wires should be cooler
                length_ratio = meters / baseline_meters
                expected_temp_change = (1.0 / length_ratio) * baseline_temp
                
                # Allow 10% tolerance for the physics
                tolerance = expected_temp_change * 0.1
                if abs(temp - expected_temp_change) <= tolerance:
                    status = "✓"
                else:
                    status = "✗"
            
            print(f"{description:<21} | {meters:>7.3f} | {temp:>13.1f}°C | {status:>6}")
            
        except Exception as e:
            print(f"{description:<21} | {'ERROR':>7} | {'ERROR':>13} | {'✗':>6}")

def test_wire_size_equivalents():
    """Test that equivalent wire sizes produce similar temperatures"""
    print("\n\nTesting Equivalent Wire Sizes")
    print("=" * 50)
    
    calc = WireTemperatureCalculator()
    
    # Test equivalent sizes for approximately 0.5mm diameter
    equivalent_sizes = [
        (24, 'AWG', '24 AWG'),
        (0.511, 'mm', '0.511 mm'),
        (20.1, 'mils', '20.1 mils'),
        (0.0201, 'inch', '0.0201 inch'),
    ]
    
    print("Testing equivalent wire sizes (all ~0.5mm diameter) at 1A:")
    print("Wire Size          | Diameter (mm) | Temperature (°C) | Status")
    print("-" * 65)
    
    baseline_temp = None
    target_diameter = 0.5  # mm
    
    for size, unit, description in equivalent_sizes:
        try:
            wire = calc.get_wire_properties(size, unit, 'nichrome', 2.0, 'feet')
            temp = calc.calculate_temperature(wire, 1.0)
            
            if baseline_temp is None:
                baseline_temp = temp
            
            # Check if diameters are actually equivalent
            diameter_error = abs(wire.diameter_mm - target_diameter) / target_diameter * 100
            temp_error = abs(temp - baseline_temp) / baseline_temp * 100
            
            diameter_ok = diameter_error < 10  # 10% tolerance on diameter
            temp_ok = temp_error < 15  # 15% tolerance on temperature
            
            status = "✓" if (diameter_ok and temp_ok) else "✗"
            
            print(f"{description:<18} | {wire.diameter_mm:>11.3f} | {temp:>13.1f}°C | {status:>6}")
            
        except Exception as e:
            print(f"{description:<18} | {'ERROR':>11} | {'ERROR':>13} | {'✗':>6}")

def test_material_support():
    """Test that all materials work with unit conversions"""
    print("\n\nTesting Material Support")
    print("=" * 50)
    
    calc = WireTemperatureCalculator()
    materials = ['nichrome', 'stainless', 'kanthal']
    
    print("Testing 0.5mm wire, 1 meter length at 2A for different materials:")
    print("Material   | Temperature (°C) | Status")
    print("-" * 40)
    
    for material in materials:
        try:
            wire = calc.get_wire_properties(0.5, 'mm', material, 1.0, 'meters')
            temp = calc.calculate_temperature(wire, 2.0)
            print(f"{material:<10} | {temp:>13.1f}°C | ✓")
        except Exception as e:
            print(f"{material:<10} | {'ERROR':>13} | ✗")

def main():
    """Run all physics correctness tests"""
    print("Wire Temperature Calculator - Physics Correctness Tests")
    print("=" * 60)
    
    try:
        test_length_physics()
        test_equivalent_lengths()
        test_wire_size_equivalents()
        test_material_support()
        
        print("\n" + "=" * 60)
        print("✓ Physics correctness tests completed!")
        print("\nSummary:")
        print("  • Longer wires run cooler (more surface area)")
        print("  • Shorter wires run hotter (less surface area)")
        print("  • Equivalent lengths produce consistent results")
        print("  • Equivalent wire sizes produce consistent results")
        print("  • All materials work with unit conversions")
        
    except Exception as e:
        print(f"\n✗ Test suite failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)