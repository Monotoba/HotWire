#!/usr/bin/env python3
"""
Detailed debug script for heat transfer calculations
"""

from wire_temp_calculator import WireTemperatureCalculator, WireProperties
from unit_conversions import LengthUnitConverter
import math

def debug_detailed_heat_transfer():
    """Debug heat transfer step by step"""
    print("Detailed Heat Transfer Debug")
    print("=" * 50)
    
    calc = WireTemperatureCalculator()
    
    # Create a test wire
    wire = calc.get_wire_properties(22, 'AWG', 'nichrome', 2.0, 'feet')
    
    print(f"Wire properties:")
    print(f"  Diameter: {wire.diameter_mm} mm")
    print(f"  Length: {wire.length} {wire.length_unit}")
    print(f"  Material: {wire.material}")
    print(f"  Resistance per foot: {wire.resistance_per_foot:.4f} Ω/ft")
    
    # Test temperature calculation step by step
    temp = 110.6  # Known temperature
    ambient_temp = 20.0
    temp_diff = temp - ambient_temp
    
    print(f"\nTemperature calculation:")
    print(f"  Wire temp: {temp}°C")
    print(f"  Ambient temp: {ambient_temp}°C")
    print(f"  Temperature difference: {temp_diff}°C")
    
    # Calculate surface area
    surface_area_per_length = math.pi * wire.diameter_mm / 1000
    print(f"  Surface area per meter: {surface_area_per_length:.6f} m²/m")
    
    # Convert length to meters
    length_m = LengthUnitConverter.to_mm(wire.length, wire.length_unit) / 1000
    print(f"  Length in meters: {length_m:.4f} m")
    
    # Material properties
    material_props = calc.MATERIAL_PROPERTIES[wire.material]
    h_conv = 10.0
    sigma = 5.67e-8
    emissivity = material_props['emissivity']
    
    print(f"\nHeat transfer parameters:")
    print(f"  Convection coefficient: {h_conv} W/(m²·K)")
    print(f"  Emissivity: {emissivity}")
    print(f"  Stefan-Boltzmann constant: {sigma}")
    
    # Calculate heat transfer components
    temp_k = temp + 273.15
    ambient_k = ambient_temp + 273.15
    
    q_conv_per_length = h_conv * surface_area_per_length * temp_diff
    q_rad_per_length = emissivity * sigma * surface_area_per_length * (temp_k**4 - ambient_k**4)
    
    print(f"\nHeat transfer per unit length:")
    print(f"  Convective: {q_conv_per_length:.6f} W/m")
    print(f"  Radiative: {q_rad_per_length:.6f} W/m")
    print(f"  Total per meter: {q_conv_per_length + q_rad_per_length:.6f} W/m")
    
    # Total for entire wire
    total_per_length = q_conv_per_length + q_rad_per_length
    total_heat_transfer = total_per_length * length_m
    
    print(f"\nTotal heat transfer for entire wire:")
    print(f"  Total heat transfer: {total_heat_transfer:.6f} W")
    print(f"  Heat transfer coefficient: {total_heat_transfer / temp_diff:.6f} W/K")
    
    # Now test the actual method
    print(f"\nActual calculation method:")
    heat_transfer_coeff = calc._calculate_heat_transfer(wire, temp)
    print(f"  Heat transfer coefficient: {heat_transfer_coeff:.6f} W/K")
    
    # Test power calculation
    resistance = calc._calculate_resistance(wire, temp)
    power = 1.0 ** 2 * resistance
    print(f"  Power at 1A: {power:.6f} W")
    print(f"  Power per unit length: {power / length_m:.6f} W/m")
    
    # Calculate expected temperature
    expected_temp = ambient_temp + (power / heat_transfer_coeff)
    print(f"  Expected temperature: {expected_temp:.1f}°C")

def debug_temperature_iteration():
    """Debug the temperature iteration process"""
    print("\n\nDebugging Temperature Iteration")
    print("=" * 50)
    
    calc = WireTemperatureCalculator()
    wire = calc.get_wire_properties(22, 'AWG', 'nichrome', 2.0, 'feet')
    
    print("Iterative temperature calculation:")
    print("Current (A) | Power (W) | Resistance (Ω) | Temperature (°C)")
    print("-" * 55)
    
    for current in [0.5, 1.0, 1.5, 2.0, 2.5]:
        try:
            temp = calc.calculate_temperature(wire, current)
            
            # Calculate power and resistance at this temperature
            resistance = calc._calculate_resistance(wire, temp)
            power = current ** 2 * resistance
            
            print(f"{current:>11} | {power:>9.3f} | {resistance:>12.3f} | {temp:>13.1f}")
            
        except Exception as e:
            print(f"{current:>11} | {'ERROR':>9} | {'ERROR':>12} | {'ERROR':>13}")

if __name__ == "__main__":
    debug_detailed_heat_transfer()
    debug_temperature_iteration()