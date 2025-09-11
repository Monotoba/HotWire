#!/usr/bin/env python3
"""
Test script for wire temperature calculator
"""

from wire_temp_calculator import WireTemperatureCalculator, WireProperties

def test_basic_calculations():
    """Test basic temperature calculations"""
    calc = WireTemperatureCalculator()
    
    print("Testing Wire Temperature Calculator")
    print("=" * 50)
    
    # Test different wire gauges and materials
    test_cases = [
        (22, 'nichrome', 2.0, 1.0),
        (22, 'nichrome', 2.0, 2.0),
        (24, 'nichrome', 2.0, 1.5),
        (22, 'stainless', 2.0, 1.0),
        (26, 'stainless', 1.5, 2.5),
    ]
    
    for gauge, material, length, current in test_cases:
        print(f"\nTesting {gauge} AWG {material}, {length}ft, {current}A:")
        
        try:
            wire = calc.get_default_wire_properties(gauge, material, length)
            temp = calc.calculate_temperature(wire, current)
            resistance = calc._calculate_resistance(wire, temp)
            
            print(f"  Temperature: {temp:.1f}°C")
            print(f"  Resistance: {resistance:.3f} Ω")
            print(f"  Power: {current**2 * resistance:.2f} W")
            
        except Exception as e:
            print(f"  Error: {e}")
    
    print("\n" + "=" * 50)
    print("Testing chart generation...")
    
    # Test chart generation
    wire = calc.get_default_wire_properties(22, 'nichrome', 2.0)
    chart_data = calc.generate_temperature_chart(wire, 0.1, 2.0, 0.1)
    
    print(f"Generated {len(chart_data)} data points")
    print("First 5 points:")
    for i, (current, temp) in enumerate(chart_data[:5]):
        print(f"  {current:.1f}A → {temp:.1f}°C")
    
    print("Last 5 points:")
    for i, (current, temp) in enumerate(chart_data[-5:]):
        print(f"  {current:.1f}A → {temp:.1f}°C")

def test_edge_cases():
    """Test edge cases and limits"""
    calc = WireTemperatureCalculator()
    
    print("\n" + "=" * 50)
    print("Testing edge cases...")
    
    # Test very low current
    wire = calc.get_default_wire_properties(22, 'nichrome', 1.0)
    temp = calc.calculate_temperature(wire, 0.01)
    print(f"Very low current (0.01A): {temp:.1f}°C")
    
    # Test high current
    temp = calc.calculate_temperature(wire, 10.0)
    print(f"High current (10A): {temp:.1f}°C")
    
    # Test different wire lengths
    for length in [0.1, 1.0, 5.0, 10.0]:
        wire = calc.get_default_wire_properties(22, 'nichrome', length)
        temp = calc.calculate_temperature(wire, 1.0)
        print(f"Length {length}ft: {temp:.1f}°C")

if __name__ == "__main__":
    test_basic_calculations()
    test_edge_cases()
    print("\nAll tests completed!")