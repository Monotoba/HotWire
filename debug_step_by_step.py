#!/usr/bin/env python3
"""
Step-by-step debug to find the exact ChartWidget foam_db issue
"""

import sys
sys.path.insert(0, 'src')

from wire_temp_calc import WireTemperatureCalculator, FoamCuttingCalculator

def test_step_by_step():
    """Test each step of the foam cutting process"""
    print("Testing step-by-step foam cutting process...")
    
    try:
        # Step 1: Create calculator and foam calculator
        calc = WireTemperatureCalculator()
        foam_calc = FoamCuttingCalculator()
        
        print("✅ Calculators created successfully")
        
        # Step 2: Test foam database access
        epp_foam = foam_calc.foam_db.get_foam_type('EPP')
        if epp_foam:
            print(f"✅ EPP foam found: {epp_foam.name}")
        else:
            print("❌ EPP foam not found")
            return False
        
        # Step 3: Test wire properties
        wire = calc.get_wire_properties(22, 'AWG', 'nichrome', 2.0, 'feet')
        print(f"✅ Wire properties created: {wire.gauge_size} {wire.gauge_unit}")
        
        # Step 4: Test temperature calculation
        temp = calc.calculate_temperature(wire, 1.0)
        print(f"✅ Temperature calculated: {temp:.1f}°C")
        
        # Step 5: Test foam cutting calculation
        optimal_temp = calc.calculate_foam_cutting_temperature('EPP', wire, 5.0)
        print(f"✅ Foam cutting temperature calculated: {optimal_temp:.1f}°C")
        
        # Step 6: Test foam cutting info generation
        foam_info = calc.get_foam_cutting_info('EPP')
        if foam_info:
            print(f"✅ Foam info generated: {len(foam_info)} items")
        else:
            print("❌ Foam info not generated")
            return False
        
        print("✅ All steps completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error in step-by-step test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_step_by_step()
    if success:
        print("✅ Step-by-step test completed successfully!")
    else:
        print("❌ Step-by-step test has issues")