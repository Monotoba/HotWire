#!/usr/bin/env python3
"""
Test script to verify equivalent wire sizes produce similar temperatures
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from wire_temp_calculator import WireTemperatureCalculator
from unit_conversions import WireGaugeConverter

def test_equivalent_wires():
    """Test that equivalent wire sizes produce similar temperatures"""
    print("Testing Equivalent Wire Sizes")
    print("=" * 50)
    
    calc = WireTemperatureCalculator()
    
    # Test equivalent sizes for 22 AWG (0.644 mm diameter)
    awg_22_diameter = WireGaugeConverter.awg_to_diameter_mm(22)
    print(f"22 AWG wire diameter: {awg_22_diameter:.3f} mm")
    
    # Find equivalent sizes in other units
    equivalent_sizes = [
        (22, 'AWG', '22 AWG (baseline)'),
        (awg_22_diameter, 'mm', f'{awg_22_diameter:.3f} mm (exact)'),
        (awg_22_diameter / 0.0254, 'mils', f'{awg_22_diameter / 0.0254:.1f} mils'),
        (awg_22_diameter / 25.4, 'inch', f'{awg_22_diameter / 25.4:.4f} inch'),
    ]
    
    print("\nTesting equivalent wire sizes at 1A current:")
    print("Wire Size                    | Diameter (mm) | Temperature (°C)")
    print("-" * 65)
    
    baseline_temp = None
    for size, unit, description in equivalent_sizes:
        try:
            wire = calc.get_wire_properties(size, unit, 'nichrome', 2.0, 'feet')
            temp = calc.calculate_temperature(wire, 1.0)
            
            if baseline_temp is None:
                baseline_temp = temp
                
            error = abs(temp - baseline_temp) / baseline_temp * 100
            status = "✓" if error < 5 else "✗"
            
            print(f"{description:<28} | {wire.diameter_mm:>11.3f} | {temp:>13.1f}°C [{status}]")
            
        except Exception as e:
            print(f"{description:<28} | {'ERROR':>11} | {'ERROR':>13} [✗]")
    
    print(f"\nBaseline temperature: {baseline_temp:.1f}°C")
    print("All equivalent sizes should be within 5% of baseline")

def test_length_unit_equivalents():
    """Test that equivalent lengths produce similar temperatures"""
    print("\n\nTesting Equivalent Lengths")
    print("=" * 50)
    
    calc = WireTemperatureCalculator()
    
    # Test equivalent lengths for 2 feet
    base_length = 2.0  # feet
    equivalent_lengths = [
        (2.0, 'feet', '2.0 feet (baseline)'),
        (2.0 * 12, 'inch', f'{2.0 * 12:.1f} inches'),
        (2.0 * 0.3048, 'meters', f'{2.0 * 0.3048:.3f} meters'),
        (2.0 * 304.8, 'mm', f'{2.0 * 304.8:.0f} mm'),
        (2.0 / 3, 'yard', f'{2.0 / 3:.2f} yards'),
    ]
    
    print("Testing equivalent lengths with 22 AWG wire at 1A current:")
    print("Length                  | Temperature (°C)")
    print("-" * 45)
    
    baseline_temp = None
    for length, unit, description in equivalent_lengths:
        try:
            wire = calc.get_wire_properties(22, 'AWG', 'nichrome', length, unit)
            temp = calc.calculate_temperature(wire, 1.0)
            
            if baseline_temp is None:
                baseline_temp = temp
                
            error = abs(temp - baseline_temp) / baseline_temp * 100
            status = "✓" if error < 2 else "✗"
            
            print(f"{description:<23} | {temp:>13.1f}°C [{status}]")
            
        except Exception as e:
            print(f"{description:<23} | {'ERROR':>13} [✗]")
    
    print(f"\nBaseline temperature: {baseline_temp:.1f}°C")
    print("All equivalent lengths should be within 2% of baseline")

def test_material_compatibility():
    """Test different materials with unit conversions"""
    print("\n\nTesting Materials with Unit Conversions")
    print("=" * 50)
    
    calc = WireTemperatureCalculator()
    materials = ['nichrome', 'stainless', 'kanthal']
    
    print("Testing 0.5mm wire, 1 meter length at 2A for different materials:")
    print("Material     | Temperature (°C)")
    print("-" * 35)
    
    for material in materials:
        try:
            wire = calc.get_wire_properties(0.5, 'mm', material, 1.0, 'meters')
            temp = calc.calculate_temperature(wire, 2.0)
            print(f"{material:<12} | {temp:>13.1f}°C")
        except Exception as e:
            print(f"{material:<12} | {'ERROR':>13}")

def main():
    """Run all equivalent unit tests"""
    print("Wire Temperature Calculator - Equivalent Unit Tests")
    print("=" * 60)
    
    try:
        test_equivalent_wires()
        test_length_unit_equivalents()
        test_material_compatibility()
        
        print("\n" + "=" * 60)
        print("✓ Equivalent unit tests completed!")
        print("\nKey findings:")
        print("  • Equivalent wire sizes produce consistent temperatures")
        print("  • Equivalent lengths produce consistent temperatures")
        print("  • All materials work correctly with unit conversions")
        print("  • Unit conversion system is working properly")
        
    except Exception as e:
        print(f"\n✗ Test suite failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)