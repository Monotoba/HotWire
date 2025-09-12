#!/usr/bin/env python3
"""
Wire Temperature Calculator
Estimates wire temperature based on current, wire type, and physical properties
"""

import math
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
import json
from .unit_conversions import (
    WireGaugeConverter,
    LengthUnitConverter,
    convert_wire_gauge,
    convert_length,
)
from .foam_cutting import FoamCuttingDatabase, FoamCuttingCalculator


@dataclass
class WireProperties:
    """Wire physical and electrical properties"""

    gauge_size: float  # Gauge size (can be AWG, SWG, mm, etc.)
    gauge_unit: str  # Unit of gauge measurement ('AWG', 'SWG', 'mm', 'mils', 'inch')
    material: str  # 'nichrome' or 'stainless'
    resistance_per_foot: float  # Ohms per foot at room temperature
    resistance_per_meter: float  # Ohms per meter at room temperature
    length: float  # Length value
    length_unit: str  # Length unit ('mm', 'cm', 'inch', 'feet', 'meters', 'yard')
    diameter_mm: float  # Wire diameter in millimeters (calculated)


class WireTemperatureCalculator:
    """Calculate wire temperature based on current and physical properties"""

    # Material properties
    MATERIAL_PROPERTIES = {
        "nichrome": {
            "resistivity_temp_coeff": 0.00017,  # Temperature coefficient of resistance
            "thermal_conductivity": 11.3,  # W/(m·K)
            "emissivity": 0.85,  # Emissivity for radiation
            "density": 8400,  # kg/m³
            "specific_heat": 450,  # J/(kg·K)
        },
        "stainless": {
            "resistivity_temp_coeff": 0.00094,  # Temperature coefficient of resistance
            "thermal_conductivity": 16.2,  # W/(m·K)
            "emissivity": 0.75,  # Emissivity for radiation
            "density": 8000,  # kg/m³
            "specific_heat": 500,  # J/(kg·K)
        },
        "kanthal": {
            "resistivity_temp_coeff": 0.00008,  # Temperature coefficient of resistance
            "thermal_conductivity": 11.0,  # W/(m·K)
            "emissivity": 0.85,  # Emissivity for radiation
            "density": 7100,  # kg/m³
            "specific_heat": 460,  # J/(kg·K)
        },
    }

    # AWG wire specifications (diameter in mm, resistance in ohms/foot at 20°C)
    # Based on copper wire resistance - will be adjusted for material type
    AWG_SPECS = {
        20: {"diameter_mm": 0.812, "resistance_ohm_per_foot": 0.01015},
        22: {"diameter_mm": 0.644, "resistance_ohm_per_foot": 0.01614},
        24: {"diameter_mm": 0.511, "resistance_ohm_per_foot": 0.02567},
        26: {"diameter_mm": 0.405, "resistance_ohm_per_foot": 0.04081},
        28: {"diameter_mm": 0.321, "resistance_ohm_per_foot": 0.06490},
        30: {"diameter_mm": 0.255, "resistance_ohm_per_foot": 0.1032},
    }

    # Material resistance factors (relative to copper)
    MATERIAL_RESISTANCE_FACTORS = {
        "nichrome": 60.0,  # Nichrome has ~60x higher resistance than copper
        "stainless": 40.0,  # Stainless steel has ~40x higher resistance than copper
        "kanthal": 70.0,  # Kanthal has ~70x higher resistance than copper
        "copper": 1.0,  # Copper baseline
    }

    def __init__(self):
        self.ambient_temp = 20.0  # °C
        self.foam_db = FoamCuttingDatabase()
        self.foam_calculator = FoamCuttingCalculator()

    def calculate_temperature(
        self, wire_props: WireProperties, current: float
    ) -> float:
        """
        Calculate wire temperature using thermal equilibrium equations

        Args:
            wire_props: Wire physical properties
            current: Current in Amperes

        Returns:
            Temperature in Celsius
        """
        # Calculate resistance at operating temperature (iterative approach)
        temp = self.ambient_temp

        # Iterative solution for temperature
        for _ in range(10):  # Max iterations
            # Calculate resistance at current temperature
            resistance = self._calculate_resistance(wire_props, temp)

            # Calculate power dissipated
            power = current**2 * resistance

            # Calculate heat transfer
            heat_transfer = self._calculate_heat_transfer(wire_props, temp)

            # New temperature estimate
            new_temp = self.ambient_temp + (power / heat_transfer)

            # Check convergence
            if abs(new_temp - temp) < 0.1:
                break

            temp = new_temp

        return temp

    def _calculate_resistance(self, wire_props: WireProperties, temp: float) -> float:
        """Calculate resistance at given temperature"""
        material_props = self.MATERIAL_PROPERTIES[wire_props.material]

        # Resistance temperature coefficient
        alpha = material_props["resistivity_temp_coeff"]

        # Base resistance at room temperature
        base_resistance = wire_props.resistance_per_foot * wire_props.length

        # Resistance at operating temperature
        resistance = base_resistance * (1 + alpha * (temp - 20.0))

        return resistance

    def _calculate_heat_transfer(
        self, wire_props: WireProperties, temp: float
    ) -> float:
        """Calculate total heat transfer coefficient (per unit temperature difference)"""
        # Avoid division by zero
        temp_diff = temp - self.ambient_temp
        if temp_diff <= 0:
            temp_diff = 0.1  # Minimum temperature difference

        # Convective heat transfer (simplified)
        h_conv = 10.0  # W/(m²·K) - typical for natural convection

        # Radiative heat transfer
        sigma = 5.67e-8  # Stefan-Boltzmann constant
        emissivity = self.MATERIAL_PROPERTIES[wire_props.material]["emissivity"]

        temp_k = temp + 273.15
        ambient_k = self.ambient_temp + 273.15

        # Surface area per unit length
        surface_area_per_length = math.pi * wire_props.diameter_mm / 1000  # m²/m

        # Convective heat transfer per unit length
        q_conv_per_length = h_conv * surface_area_per_length * temp_diff

        # Radiative heat transfer per unit length
        q_rad_per_length = (
            emissivity
            * sigma
            * surface_area_per_length
            * (temp_k**4 - ambient_k**4)
        )

        # Total heat transfer per unit length
        total_heat_transfer_per_length = q_conv_per_length + q_rad_per_length

        # Convert wire length to meters for calculation
        length_m = (
            LengthUnitConverter.to_mm(wire_props.length, wire_props.length_unit) / 1000
        )

        # Total heat transfer for the entire wire
        total_heat_transfer = total_heat_transfer_per_length * length_m

        # Return heat transfer coefficient (heat transfer per degree temperature difference)
        return total_heat_transfer / temp_diff

    def calculate_foam_cutting_temperature(
        self,
        foam_type: str,
        wire_props: WireProperties,
        cutting_speed_mm_s: float = 5.0,
    ) -> float:
        """Calculate optimal wire temperature for foam cutting"""
        return self.foam_calculator.calculate_optimal_wire_temperature(
            foam_type, wire_props.diameter_mm, cutting_speed_mm_s
        )

    def get_foam_cutting_recommendations(
        self, foam_type: str, wire_temperature: float, workspace_volume_m3: float = 10.0
    ) -> Dict[str, any]:
        """Get foam cutting recommendations and safety information"""
        return self.foam_calculator.get_safety_recommendations(
            foam_type, wire_temperature, workspace_volume_m3
        )

    def is_foam_cutting_mode_safe(
        self, foam_type: str, wire_temperature: float
    ) -> bool:
        """Check if foam cutting mode is safe for given parameters"""
        return self.foam_db.is_temperature_safe(foam_type, wire_temperature)

    def get_foam_safety_warning(
        self, foam_type: str, wire_temperature: float
    ) -> Optional[str]:
        """Get safety warning for foam cutting"""
        return self.foam_db.get_safety_warning(foam_type, wire_temperature)

    def get_foam_cutting_info(self, foam_type: str) -> Dict[str, any]:
        """Get complete foam cutting information"""
        return self.foam_calculator.foam_db.get_cutting_recommendations(foam_type)

    def generate_temperature_chart(
        self,
        wire_props: WireProperties,
        current_start: float = 0.1,
        current_end: float = 5.0,
        current_step: float = 0.1,
    ) -> List[Tuple[float, float]]:
        """Generate temperature vs current data for charting"""
        data = []
        current = current_start

        while current <= current_end:
            temp = self.calculate_temperature(wire_props, current)
            data.append((current, temp))
            current += current_step

        return data

    def get_wire_properties(
        self,
        gauge_size: float,
        gauge_unit: str,
        material: str,
        length: float,
        length_unit: str,
    ) -> WireProperties:
        """Get wire properties from gauge size/unit and material"""

        # Convert gauge to diameter in mm
        diameter_mm = WireGaugeConverter.convert_gauge_to_mm(gauge_size, gauge_unit)

        # Calculate resistance based on material and diameter
        # Use copper as baseline and apply material factor

        # For AWG sizes, use known copper resistance values
        if gauge_unit == "AWG" and gauge_size in self.AWG_SPECS:
            copper_resistance_per_foot = self.AWG_SPECS[gauge_size][
                "resistance_ohm_per_foot"
            ]
        else:
            # Calculate resistance based on diameter (copper baseline)
            # R = ρ * L/A, where A = π * (d/2)²
            # Using copper resistivity as baseline
            copper_resistivity_ohm_mm = 1.68e-5  # Ohm·mm
            area_mm2 = math.pi * (diameter_mm / 2) ** 2
            copper_resistance_per_mm = copper_resistivity_ohm_mm / area_mm2
            copper_resistance_per_foot = copper_resistance_per_mm * 304.8  # mm per foot

        # Apply material resistance factor
        if material in self.MATERIAL_RESISTANCE_FACTORS:
            resistance_factor = self.MATERIAL_RESISTANCE_FACTORS[material]
        elif material.lower() in ["kanthal", "fechral"]:
            # Handle kanthal variations
            resistance_factor = 70.0
        else:
            raise ValueError(f"Unsupported material: {material}")

        resistance_per_foot = copper_resistance_per_foot * resistance_factor
        resistance_per_meter = resistance_per_foot * 3.28084  # Convert to per meter

        return WireProperties(
            gauge_size=gauge_size,
            gauge_unit=gauge_unit,
            material=material,
            resistance_per_foot=resistance_per_foot,
            resistance_per_meter=resistance_per_meter,
            length=length,
            length_unit=length_unit,
            diameter_mm=diameter_mm,
        )

    def get_default_wire_properties(
        self, gauge: int, material: str, length: float = 1.0
    ) -> WireProperties:
        """Get default wire properties for common AWG gauges (backward compatibility)"""
        return self.get_wire_properties(gauge, "AWG", material, length, "feet")


class ProjectManager:
    """Handle saving and loading project files"""

    def save_project(
        self,
        filename: str,
        wire_props: WireProperties,
        current_range: Dict[str, float],
        foam_type: Optional[str] = None,
        cutting_mode: bool = False,
    ) -> None:
        """Save project settings to file"""
        project_data = {
            "wire_properties": {
                "gauge_size": wire_props.gauge_size,
                "gauge_unit": wire_props.gauge_unit,
                "material": wire_props.material,
                "resistance_per_foot": wire_props.resistance_per_foot,
                "resistance_per_meter": wire_props.resistance_per_meter,
                "length": wire_props.length,
                "length_unit": wire_props.length_unit,
                "diameter_mm": wire_props.diameter_mm,
            },
            "current_range": current_range,
            "foam_cutting_mode": cutting_mode,
            "foam_type": foam_type,
        }

        with open(filename, "w") as f:
            json.dump(project_data, f, indent=2)

    def load_project(
        self, filename: str
    ) -> Tuple[WireProperties, Dict[str, float], Optional[str], bool]:
        """Load project settings from file"""
        with open(filename, "r") as f:
            project_data = json.load(f)

        wire_data = project_data["wire_properties"]

        # Handle backward compatibility for old project files
        if "gauge" in wire_data and "gauge_unit" not in wire_data:
            # Old format - assume AWG and feet
            wire_props = WireProperties(
                gauge_size=wire_data["gauge"],
                gauge_unit="AWG",
                material=wire_data["material"],
                resistance_per_foot=wire_data["resistance_per_foot"],
                resistance_per_meter=wire_data["resistance_per_meter"],
                length=wire_data["length"],
                length_unit="feet",
                diameter_mm=wire_data["diameter_mm"],
            )
        else:
            # New format
            wire_props = WireProperties(
                gauge_size=wire_data["gauge_size"],
                gauge_unit=wire_data["gauge_unit"],
                material=wire_data["material"],
                resistance_per_foot=wire_data["resistance_per_foot"],
                resistance_per_meter=wire_data["resistance_per_meter"],
                length=wire_data["length"],
                length_unit=wire_data["length_unit"],
                diameter_mm=wire_data["diameter_mm"],
            )

        current_range = project_data["current_range"]

        # Handle foam cutting mode (new feature)
        foam_type = project_data.get("foam_type")
        cutting_mode = project_data.get("foam_cutting_mode", False)

        return wire_props, current_range, foam_type, cutting_mode


if __name__ == "__main__":
    # Test the calculator
    calc = WireTemperatureCalculator()

    # Create a sample wire
    wire = calc.get_default_wire_properties(22, "nichrome", length=2.0)

    # Generate chart data
    chart_data = calc.generate_temperature_chart(wire)

    print("Current (A)\tTemperature (°C)")
    print("-" * 30)
    for current, temp in chart_data[::5]:  # Print every 5th point
        print(f"{current:.1f}\t\t{temp:.1f}")
