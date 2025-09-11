#!/usr/bin/env python3
"""
Debug script to check heat transfer calculations
"""

from wire_temp_calculator import WireTemperatureCalculator, WireProperties
from unit_conversions import LengthUnitConverter

def debug_heat_transfer():
    """Debug heat transfer calculations"""
    print("Debugging Heat Transfer Calculations")
    print("=" * 50)
    
    calc = WireTemperatureCalculator()
    
    # Test different lengths
    test_lengths = [
        (0.5, 'feet'),
        (1.0, 'feet'),
        (2.0, 'feet'),
        (4.0, 'feet'),
    ]
    
    print("Testing heat transfer for different wire lengths:")
    print("Length     | Meters  | Area (m²/m) | Heat Transfer | Temperature")
    print("-" * 70)
    
    for length, unit in test_lengths:
        try:
            wire = calc.get_wire_properties(22, 'AWG', 'nichrome', length, unit)
            
            # Manually calculate what the heat transfer should be
            temp = 110.0  # Approximate temperature
            temp_diff = temp - 20.0
            
            # Surface area per unit length
            surface_area_per_length = 3.14159 * wire.diameter_mm / 1000
            
            # Convert length to meters
            length_m = LengthUnitConverter.to_mm(length, unit) / 1000
            
            # Calculate heat transfer coefficient
            heat_transfer = calc._calculate_heat_transfer(wire, temp)
            
            # Calculate actual temperature
            actual_temp = calc.calculate_temperature(wire, 1.0)
            
            print(f"{length:>4} {unit:<6} | {length_m:>7.3f} | {surface_area_per_length:>11.4f} | {heat_transfer:>13.1f} | {actual_temp:>11.1f}°C")
            
        except Exception as e:
            print(f"{length:>4} {unit:<6} | {'ERROR':>7} | {'ERROR':>11} | {'ERROR':>13} | {'ERROR':>11}")

def debug_length_scaling():
    """Debug how length affects the calculation"""
    print("\n\nDebugging Length Scaling")
    print("=" * 50)
    
    calc = WireTemperatureCalculator()
    
    # Create wires with different lengths but same properties
    base_wire = calc.get_wire_properties(22, 'AWG', 'nichrome', 1.0, 'feet')
    
    print("Manual calculation for different lengths:")
    print("Length (ft) | Length (m) | Power (W) | Heat Transfer | Temp (°C)")
    print("-" * 65)
    
    for length_ft in [0.5, 1.0, 2.0, 4.0]:
        try:
            # Create wire with specific length
            wire = calc.get_wire_properties(22, 'AWG', 'nichrome', length_ft, 'feet')
            
            # Calculate power at 1A
            resistance = calc._calculate_resistance(wire, 100)  # Approximate temp
            power = 1.0 ** 2 * resistance * length_ft  # Total power for the wire length
            
            # Calculate heat transfer
            temp = 100.0
            heat_transfer = calc._calculate_heat_transfer(wire, temp)
            
            # Calculate actual temperature
            actual_temp = calc.calculate_temperature(wire, 1.0)
            
            length_m = LengthUnitConverter.to_mm(length_ft, 'feet') / 1000
            
            print(f"{length_ft:>11} | {length_m:>10.3f} | {power:>9.2f} | {heat_transfer:>13.1f} | {actual_temp:>9.1f}")
            
        except Exception as e:
            print(f"{length_ft:>11} | {'ERROR':>10} | {'ERROR':>9} | {'ERROR':>13} | {'ERROR':>9}")

if __name__ == "__main__":
    debug_heat_transfer()
    debug_length_scaling()