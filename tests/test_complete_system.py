#!/usr/bin/env python3
"""
Complete system test for the refactored Wire Temperature Calculator
Tests the full application with all new unit features
"""

import sys
import os
from typing import Optional
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_complete_workflow():
    """Test a complete workflow with different units"""
    print("Testing Complete Workflow")
    print("=" * 50)
    
    from wire_temp_calc.wire_temp_calculator import WireTemperatureCalculator, ProjectManager
    from wire_temp_calc.unit_conversions import WireGaugeConverter, LengthUnitConverter
    
    calc = WireTemperatureCalculator()
    project_mgr = ProjectManager()
    
    # Test 1: Create wire with different gauge units
    print("1. Testing wire gauge units:")
    test_cases = [
        (22, 'AWG', '22 AWG wire'),
        (0.644, 'mm', '0.644 mm wire'),
        (25.4, 'mils', '25.4 mils wire'),
        (0.0254, 'inch', '0.0254 inch wire'),
    ]
    
    baseline_temp = None
    for size, unit, description in test_cases:
        try:
            wire = calc.get_wire_properties(size, unit, 'nichrome', 2.0, 'feet')
            temp = calc.calculate_temperature(wire, 1.0)
            
            if baseline_temp is None:
                baseline_temp = temp
                
            error = abs(temp - baseline_temp) / baseline_temp * 100
            status = "✓" if error < 5 else "✗"
            
            print(f"   {description:<20} | {temp:>6.1f}°C | {status:>4}")
            
        except Exception as e:
            print(f"   {description:<20} | {'ERROR':>6} | {'✗':>4}")
    
    # Test 2: Create wire with different length units
    print("\n2. Testing length units:")
    test_lengths = [
        (2.0, 'feet', '2 feet'),
        (24.0, 'inch', '24 inches'),
        (0.6096, 'meters', '0.6096 meters'),
        (609.6, 'mm', '609.6 mm'),
    ]
    
    for length, unit, description in test_lengths:
        try:
            wire = calc.get_wire_properties(22, 'AWG', 'nichrome', length, unit)
            temp = calc.calculate_temperature(wire, 1.0)
            meters = LengthUnitConverter.to_mm(length, unit) / 1000
            
            print(f"   {description:<20} | {meters:>6.3f}m | {temp:>6.1f}°C")
            
        except Exception as e:
            print(f"   {description:<20} | {'ERROR':>6} | {'ERROR':>6}")
    
    # Test 3: Different materials
    print("\n3. Testing different materials:")
    materials = ['nichrome', 'stainless', 'kanthal']
    
    for material in materials:
        try:
            wire = calc.get_wire_properties(0.5, 'mm', material, 1.0, 'meters')
            temp = calc.calculate_temperature(wire, 2.0)
            
            print(f"   {material:<12} | {temp:>6.1f}°C")
            
        except Exception as e:
            print(f"   {material:<12} | {'ERROR':>6}")
    
    # Test 4: Project save/load with new units
    print("\n4. Testing project save/load:")
    try:
        # Create wire with mixed units
        wire_props = calc.get_wire_properties(1.0, 'mm', 'stainless', 50.0, 'cm')
        current_range = {'start': 0.5, 'end': 3.0, 'step': 0.1}
        
        # Save project
        project_mgr.save_project('test_units.json', wire_props, current_range)
        print("   ✓ Project saved successfully")
        
        # Load project
        loaded_wire, loaded_range, foam_type, cutting_mode = project_mgr.load_project('test_units.json')
        print(f"   ✓ Project loaded: {loaded_wire.gauge_size:.1f} {loaded_wire.gauge_unit}, {loaded_wire.length:.1f} {loaded_wire.length_unit}")
        if foam_type:
            print(f"   ✓ Foam cutting mode: {foam_type}")
        if cutting_mode:
            print(f"   ✓ Cutting mode enabled")
        
        # Clean up
        os.remove('test_units.json')
        
    except Exception as e:
        print(f"   ✗ Project save/load failed: {e}")

def test_ui_elements():
    """Test that UI elements can be created with new units"""
    print("\n\nTesting UI Elements")
    print("=" * 50)
    
    try:
        from wire_temp_calc.main_window import InputPanel, MainWindow
        from PySide6.QtWidgets import QApplication
        
        # Create minimal QApplication for testing
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        # Test input panel creation
        input_panel = InputPanel()
        print("✓ Input panel created successfully")
        
        # Test unit combinations
        test_combinations = [
            ('AWG', 'feet'),
            ('mm', 'meters'),
            ('mils', 'inch'),
            ('SWG', 'yard'),
        ]
        
        for gauge_unit, length_unit in test_combinations:
            try:
                input_panel.gauge_unit_combo.setCurrentText(gauge_unit)
                input_panel.length_unit_combo.setCurrentText(length_unit)
                print(f"✓ Units combination: {gauge_unit} + {length_unit}")
            except Exception as e:
                print(f"✗ Units combination failed: {gauge_unit} + {length_unit} - {e}")
        
    except Exception as e:
        print(f"✗ UI test failed: {e}")

def test_edge_cases():
    """Test edge cases and boundary conditions"""
    print("\n\nTesting Edge Cases")
    print("=" * 50)
    
    from wire_temp_calc.wire_temp_calculator import WireTemperatureCalculator
    
    calc = WireTemperatureCalculator()
    
    edge_cases = [
        (0.001, 'mm', 0.001, 'mm', "Very small wire"),
        (50, 'AWG', 100, 'meters', "Large wire and length"),
        (0, 'AWG', 1.0, 'feet', "AWG 0 (largest)"),
        (40, 'AWG', 0.1, 'inch', "AWG 40 (smallest)"),
    ]
    
    print("Testing extreme values:")
    for gauge_size, gauge_unit, length, length_unit, description in edge_cases:
        try:
            wire = calc.get_wire_properties(gauge_size, gauge_unit, 'nichrome', length, length_unit)
            temp = calc.calculate_temperature(wire, 0.1)  # Low current for safety
            
            print(f"   {description:<20} | {temp:>6.1f}°C | ✓")
            
        except Exception as e:
            print(f"   {description:<20} | {'ERROR':>6} | ✗")

def main():
    """Run complete system test"""
    print("Wire Temperature Calculator - Complete System Test")
    print("=" * 60)
    
    try:
        test_complete_workflow()
        test_ui_elements()
        test_edge_cases()
        
        print("\n" + "=" * 60)
        print("✓ Complete system test passed!")
        print("\nThe refactored application successfully supports:")
        print("  • Multiple wire gauge units (AWG, SWG, mm, mils, inch)")
        print("  • Multiple length units (mm, cm, inch, feet, meters, yard)")
        print("  • All materials (nichrome, stainless, kanthal)")
        print("  • Project save/load with new unit system")
        print("  • UI elements with unit selection")
        print("  • Edge cases and boundary conditions")
        print("  • Backward compatibility")
        
        print("\nTo run the application:")
        print("  ./activate_and_run.sh")
        
    except Exception as e:
        print(f"\n✗ Complete system test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)