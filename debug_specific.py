#!/usr/bin/env python3
"""
Debug script to find the specific ChartWidget foam_db issue
"""

import sys
sys.path.insert(0, 'src')

from wire_temp_calc import WireTemperatureCalculator, FoamCuttingCalculator

def test_specific_functionality():
    """Test the specific functionality that might be causing issues"""
    print("Testing specific functionality...")
    
    try:
        # Test foam database access
        foam_calc = FoamCuttingCalculator()
        
        # Test EPP foam specifically
        epp_foam = foam_calc.foam_db.get_foam_type('EPP')
        if epp_foam:
            print(f"✅ EPP foam found: {epp_foam.name}")
            print(f"✅ Temperature range: {epp_foam.min_temp_celsius}-{epp_foam.max_temp_celsius}°C")
            print(f"✅ Optimal temp: {epp_foam.optimal_temp_celsius}°C")
        else:
            print("❌ EPP foam not found")
            return False
        
        # Test temperature calculation with EPP
        calc = WireTemperatureCalculator()
        wire = calc.get_wire_properties(22, 'AWG', 'nichrome', 2.0, 'feet')
        temp = calc.calculate_temperature(wire, 1.0)
        
        print(f"✅ Wire temperature: {temp:.1f}°C")
        
        # Test the specific foam cutting calculation
        optimal_temp = foam_calc.calculate_optimal_wire_temperature('EPP', 0.644, 5.0)
        print(f"✅ EPP optimal cutting temperature: {optimal_temp:.1f}°C")
        
        # Test safety recommendations
        safety_info = foam_calc.get_safety_recommendations('EPP', optimal_temp)
        print(f"✅ Safety info: Fire risk {safety_info['fire_risk_level']}")
        
        print("✅ All foam cutting functionality working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_specific_functionality()
    if success:
        print("✅ Specific functionality working correctly!")
    else:
        print("❌ Specific functionality has issues")