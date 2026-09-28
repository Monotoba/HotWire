#!/usr/bin/env python3
"""
Wire Temperature Calculator - Command Line Interface
Professional foam cutting and wire heating calculator
"""

import argparse
import math
import sys
from .wire_temp_calculator import WireTemperatureCalculator
from .unit_conversions import WireGaugeConverter, LengthUnitConverter
from .foam_cutting import FoamCuttingCalculator, FoamCuttingDatabase


def create_parser():
    """Create command line argument parser"""
    parser = argparse.ArgumentParser(
        description="Professional wire temperature and foam cutting calculator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Calculate temperature for 22 AWG nichrome wire at 1A
  wire-temp-calc --gauge 22 --gauge-unit AWG --material nichrome --length 2 --length-unit feet --current 1
  
  # Foam cutting with EPP foam
  wire-temp-calc --foam EPP --wire-diameter 0.644 --cutting-speed 5
  
  # List all supported foam types
  wire-temp-calc --list-foams
  
  # Get safety info for specific temperature
  wire-temp-calc --safety-info EPS 250

  # Calculate a range of currents
  wire-temp-calc --current-start 0.1 --current-end 5 --current-step 0.1
        """,
    )

    # Wire specifications
    wire_group = parser.add_argument_group("Wire Specifications")
    wire_group.add_argument(
        "--gauge", type=float, default=22, help="Wire gauge size (default: 22)"
    )
    wire_group.add_argument(
        "--gauge-unit",
        choices=["AWG", "SWG", "mm", "mils", "inch"],
        default="AWG",
        help="Wire gauge unit (default: AWG)",
    )
    wire_group.add_argument(
        "--material",
        choices=["nichrome", "stainless", "kanthal"],
        default="nichrome",
        help="Wire material (default: nichrome)",
    )
    wire_group.add_argument(
        "--length", type=float, default=2.0, help="Wire length (default: 2.0)"
    )
    wire_group.add_argument(
        "--length-unit",
        choices=["mm", "cm", "inch", "feet", "meters", "yard"],
        default="feet",
        help="Length unit (default: feet)",
    )

    # Current specifications
    current_group = parser.add_argument_group("Current Specifications")
    current_group.add_argument(
        "--current", type=float, default=None, help="Current in Amperes (default: 1.0)"
    )
    current_group.add_argument(
        "--current-start",
        type=float,
        default=None,
        help="Start current for range calculation (default: 0.1)",
    )
    current_group.add_argument(
        "--current-end",
        type=float,
        default=None,
        help="End current for range calculation (default: 5.0)",
    )
    current_group.add_argument(
        "--current-step",
        type=float,
        default=None,
        help="Current step for range calculation (default: 0.1)",
    )

    # Foam cutting options
    foam_group = parser.add_argument_group("Foam Cutting Options")
    foam_group.add_argument(
        "--foam", type=str, help="Foam type for cutting (e.g., EPS, EPP, XPS)"
    )
    foam_group.add_argument(
        "--wire-diameter", type=float, help="Wire diameter in mm for foam cutting"
    )
    foam_group.add_argument(
        "--cutting-speed",
        type=float,
        default=5.0,
        help="Cutting speed in mm/s (default: 5.0)",
    )
    foam_group.add_argument(
        "--workspace-volume",
        type=float,
        default=15.0,
        help="Workspace volume in cubic meters (default: 15.0)",
    )

    # Information options
    info_group = parser.add_argument_group("Information Options")
    info_group.add_argument(
        "--list-foams", action="store_true", help="List all supported foam types"
    )
    info_group.add_argument(
        "--safety-info",
        nargs=2,
        metavar=("FOAM_TYPE", "TEMPERATURE"),
        help="Get safety information for specific foam and temperature",
    )
    info_group.add_argument(
        "--list-units", action="store_true", help="List all supported units"
    )

    # Output options
    output_group = parser.add_argument_group("Output Options")
    output_group.add_argument(
        "--json", action="store_true", help="Output results in JSON format"
    )
    output_group.add_argument(
        "--verbose", "-v", action="store_true", help="Verbose output"
    )

    return parser


def handle_list_foams():
    """Handle --list-foams option"""
    foam_db = FoamCuttingDatabase()
    foams = foam_db.get_all_foam_types()

    print("Supported Foam Types:")
    print("=" * 60)
    for foam in foams:
        print(f"{foam.name:<12} | {foam.description}")
        print(f"  Temperature range: {foam.min_temp_celsius}-{foam.max_temp_celsius}°C")
        print(f"  Cutting speed: {foam.cutting_speed}")
        print(f"  Notes: {foam.safety_notes}")
        print()


def handle_safety_info(foam_type, temperature_str):
    """Handle --safety-info option"""
    try:
        temperature = float(temperature_str)
        if not math.isfinite(temperature):
            raise ValueError
        foam_calc = FoamCuttingCalculator()
        if not foam_calc.foam_db.get_foam_type(foam_type):
            print(f"Error: Unknown foam type '{foam_type}'", file=sys.stderr)
            sys.exit(1)

        safety_info = foam_calc.get_safety_recommendations(foam_type, temperature)

        print(f"Safety Information for {foam_type} at {temperature}°C:")
        print("=" * 50)
        print(f"Fire risk level: {safety_info['fire_risk_level']}")
        print(
            f"Ventilation required: {'Yes' if safety_info['ventilation_required'] else 'No'}"
        )
        print(
            f"Fume extraction recommended: {'Yes' if safety_info['fume_extraction_recommended'] else 'No'}"
        )
        print(
            f"Workspace requirements: {safety_info['workspace_requirements']['workspace_size']}"
        )

        if safety_info["safety_warning"]:
            print("Safety warnings:")
            print(f"  - {safety_info['safety_warning']}")

    except ValueError:
        print(f"Error: Invalid temperature '{temperature_str}'", file=sys.stderr)
        sys.exit(1)


def handle_list_units():
    """Handle --list-units option"""
    print("Supported Units:")
    print("=" * 30)

    print("Wire Gauge Units:")
    for unit in ["AWG", "SWG", "mm", "mils", "inch"]:
        print(f"  - {unit}")

    print("\nLength Units:")
    for unit in ["mm", "cm", "inch", "feet", "meters", "yard"]:
        print(f"  - {unit}")


def main():
    """Main CLI function"""
    parser = create_parser()
    args = parser.parse_args()

    range_requested = any(
        value is not None
        for value in (args.current_start, args.current_end, args.current_step)
    )
    if range_requested and args.current is not None:
        parser.error("--current cannot be combined with current range options")
    if range_requested:
        args.current_start = 0.1 if args.current_start is None else args.current_start
        args.current_end = 5.0 if args.current_end is None else args.current_end
        args.current_step = 0.1 if args.current_step is None else args.current_step
        if not all(
            math.isfinite(value)
            for value in (args.current_start, args.current_end, args.current_step)
        ) or not (0 <= args.current_start < args.current_end and args.current_step > 0):
            parser.error("current range requires 0 <= start < end and step > 0")
    else:
        args.current = 1.0 if args.current is None else args.current
        if not math.isfinite(args.current) or args.current < 0:
            parser.error("--current must be a finite, nonnegative number")

    # Handle information options
    if args.list_foams:
        handle_list_foams()
        return

    if args.safety_info:
        handle_safety_info(args.safety_info[0], args.safety_info[1])
        return

    if args.list_units:
        handle_list_units()
        return

    # Main calculation
    try:
        calc = WireTemperatureCalculator()

        # Get wire properties
        wire_props = calc.get_wire_properties(
            args.gauge, args.gauge_unit, args.material, args.length, args.length_unit
        )

        # Handle foam cutting mode
        if args.foam:
            foam_calc = FoamCuttingCalculator()
            wire_diameter = args.wire_diameter or wire_props.diameter_mm
            optimal_temp = foam_calc.calculate_optimal_wire_temperature(
                args.foam, wire_diameter, args.cutting_speed
            )

            print(f"Optimal wire temperature for {args.foam} foam cutting:")
            print(f"  Wire diameter: {wire_diameter:.3f} mm")
            print(f"  Cutting speed: {args.cutting_speed} mm/s")
            print(f"  Optimal temperature: {optimal_temp:.1f}°C")

            # Safety information
            safety_info = foam_calc.get_safety_recommendations(
                args.foam, optimal_temp, args.workspace_volume
            )
            print(f"  Fire risk: {safety_info['fire_risk_level']}")
            print(
                f"  Ventilation: {'Required' if safety_info['ventilation_required'] else 'Not required'}"
            )

        else:
            # Standard temperature calculation
            if range_requested:
                # Range calculation
                chart_data = calc.generate_temperature_chart(
                    wire_props, args.current_start, args.current_end, args.current_step
                )

                print(
                    f"Temperature vs Current for {args.gauge} {args.gauge_unit} {args.material} wire:"
                )
                print("Current (A) | Temperature (°C)")
                print("-" * 30)

                for current, temp in chart_data[::5]:  # Print every 5th point
                    print(f"{current:>11.1f} | {temp:>13.1f}")

            else:
                # Single point calculation
                temp = calc.calculate_temperature(wire_props, args.current)

                print(f"Wire Temperature Calculation:")
                print(f"  Wire: {args.gauge} {args.gauge_unit} {args.material}")
                print(f"  Length: {args.length} {args.length_unit}")
                print(f"  Current: {args.current} A")
                print(f"  Temperature: {temp:.1f}°C")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
