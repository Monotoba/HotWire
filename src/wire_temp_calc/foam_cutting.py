#!/usr/bin/env python3
"""
Foam cutting temperature database and safety guidelines
Provides recommended cutting temperatures for various foam types
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple
import math


@dataclass
class FoamType:
    """Foam type specifications"""

    name: str
    abbreviation: str
    description: str
    min_temp_celsius: float
    optimal_temp_celsius: float
    max_temp_celsius: float
    cutting_speed: str  # 'slow', 'medium', 'fast'
    safety_notes: str
    applications: List[str]
    density_range_kg_m3: Tuple[float, float]
    melting_point_celsius: Optional[float] = None
    decomposition_temp_celsius: Optional[float] = None


class FoamCuttingDatabase:
    """Comprehensive foam cutting temperature database"""

    def __init__(self):
        self.foam_types = self._initialize_foam_database()
        self.safety_guidelines = self._initialize_safety_guidelines()

    def _initialize_foam_database(self) -> Dict[str, FoamType]:
        """Initialize foam cutting temperature database"""

        foam_data = {
            "EPP": FoamType(
                name="Expanded Polypropylene",
                abbreviation="EPP",
                description="High-performance foam with excellent impact resistance and multiple impact capability",
                min_temp_celsius=220,
                optimal_temp_celsius=240,
                max_temp_celsius=260,
                cutting_speed="medium",
                safety_notes="Requires higher temperatures. Ensure good ventilation. Avoid overheating.",
                applications=[
                    "RC aircraft",
                    "Model aircraft",
                    "Protective packaging",
                    "Automotive parts",
                ],
                density_range_kg_m3=(20, 200),
                melting_point_celsius=160,
                decomposition_temp_celsius=300,
            ),
            "EPS": FoamType(
                name="Expanded Polystyrene",
                abbreviation="EPS",
                description="Common white foam, lightweight and rigid, easy to cut",
                min_temp_celsius=180,
                optimal_temp_celsius=200,
                max_temp_celsius=220,
                cutting_speed="fast",
                safety_notes="Most common foam. Low odor. Avoid excessive melting.",
                applications=[
                    "Insulation",
                    "Packaging",
                    "Model building",
                    "Craft projects",
                ],
                density_range_kg_m3=(10, 50),
                melting_point_celsius=100,
                decomposition_temp_celsius=250,
            ),
            "EPE": FoamType(
                name="Expanded Polyethylene",
                abbreviation="EPE",
                description="Flexible, resilient foam with good cushioning properties",
                min_temp_celsius=200,
                optimal_temp_celsius=220,
                max_temp_celsius=240,
                cutting_speed="slow",
                safety_notes="Flexible foam requires careful handling. May produce more fumes.",
                applications=[
                    "Packaging",
                    "Cushioning",
                    "Exercise mats",
                    "Protective padding",
                ],
                density_range_kg_m3=(25, 200),
                melting_point_celsius=120,
                decomposition_temp_celsius=280,
            ),
            "EVA": FoamType(
                name="Ethylene-Vinyl Acetate",
                abbreviation="EVA",
                description="Soft, flexible foam with rubber-like properties",
                min_temp_celsius=190,
                optimal_temp_celsius=210,
                max_temp_celsius=230,
                cutting_speed="slow",
                safety_notes="Very flexible. Requires lower temperatures. Good ventilation essential.",
                applications=[
                    "Craft foam",
                    "Cosplay",
                    "Shoe insoles",
                    "Exercise equipment",
                ],
                density_range_kg_m3=(30, 300),
                melting_point_celsius=90,
                decomposition_temp_celsius=260,
            ),
            "PU": FoamType(
                name="Polyurethane Foam",
                abbreviation="PU",
                description="Versatile foam available in various densities and flexibilities",
                min_temp_celsius=170,
                optimal_temp_celsius=190,
                max_temp_celsius=210,
                cutting_speed="medium",
                safety_notes="Can produce isocyanates when overheated. Stay within recommended range.",
                applications=[
                    "Upholstery",
                    "Insulation",
                    "Model making",
                    "Craft projects",
                ],
                density_range_kg_m3=(10, 150),
                melting_point_celsius=120,
                decomposition_temp_celsius=240,
            ),
            "XPS": FoamType(
                name="Extruded Polystyrene",
                abbreviation="XPS",
                description="Dense, rigid foam with closed-cell structure, excellent insulation",
                min_temp_celsius=200,
                optimal_temp_celsius=220,
                max_temp_celsius=240,
                cutting_speed="medium",
                safety_notes="Denser than EPS. Requires higher temperatures. Clean cuts possible.",
                applications=[
                    "Insulation boards",
                    "Model aircraft",
                    "Architectural models",
                    "Signage",
                ],
                density_range_kg_m3=(25, 50),
                melting_point_celsius=110,
                decomposition_temp_celsius=260,
            ),
            "DEPRON": FoamType(
                name="Depron",
                abbreviation="DEPRON",
                description="Thin, rigid foam sheet popular for RC aircraft",
                min_temp_celsius=180,
                optimal_temp_celsius=200,
                max_temp_celsius=220,
                cutting_speed="fast",
                safety_notes="Thin material cuts easily. Low temperatures sufficient.",
                applications=[
                    "RC aircraft",
                    "Model aircraft",
                    "Architectural models",
                    "Craft projects",
                ],
                density_range_kg_m3=(30, 45),
                melting_point_celsius=100,
                decomposition_temp_celsius=250,
            ),
            "FOAM_BOARD": FoamType(
                name="Foam Board",
                abbreviation="FOAM_BOARD",
                description="Paper-faced foam core, common in crafts and presentations",
                min_temp_celsius=160,
                optimal_temp_celsius=180,
                max_temp_celsius=200,
                cutting_speed="fast",
                safety_notes="Be careful not to scorch paper facing. Lower temperatures preferred.",
                applications=[
                    "Presentation boards",
                    "Craft projects",
                    "School projects",
                    "Signage",
                ],
                density_range_kg_m3=(40, 80),
                melting_point_celsius=90,
                decomposition_temp_celsius=230,
            ),
            "MEMORY_FOAM": FoamType(
                name="Memory Foam",
                abbreviation="MEMORY",
                description="Viscoelastic foam that conforms to shape, temperature-sensitive",
                min_temp_celsius=150,
                optimal_temp_celsius=170,
                max_temp_celsius=190,
                cutting_speed="very slow",
                safety_notes="Extremely temperature-sensitive. Use lowest effective temperature.",
                applications=["Mattresses", "Pillows", "Cushions", "Medical supports"],
                density_range_kg_m3=(40, 100),
                melting_point_celsius=80,
                decomposition_temp_celsius=220,
            ),
            "NEOPRENE": FoamType(
                name="Neoprene",
                abbreviation="NEOPRENE",
                description="Synthetic rubber foam, oil and weather resistant",
                min_temp_celsius=180,
                optimal_temp_celsius=200,
                max_temp_celsius=220,
                cutting_speed="slow",
                safety_notes="Rubber-based material. May produce more fumes. Excellent ventilation required.",
                applications=["Gaskets", "Seals", "Wetsuits", "Insulation"],
                density_range_kg_m3=(80, 300),
                melting_point_celsius=100,
                decomposition_temp_celsius=250,
            ),
        }

        return foam_data

    def _initialize_safety_guidelines(self) -> Dict[str, str]:
        """Initialize safety guidelines for foam cutting"""
        return {
            "ventilation": "Always work in well-ventilated area. Use exhaust fan or work outdoors.",
            "temperature_monitoring": "Use temperature controller. Never exceed maximum recommended temperature.",
            "protective_equipment": "Wear safety glasses, heat-resistant gloves, and respiratory protection.",
            "fire_safety": "Keep fire extinguisher nearby. Never leave hot wire unattended.",
            "fume_extraction": "Use fume extraction system for prolonged cutting or high-temperature foams.",
            "material_identification": "Identify foam type before cutting. When in doubt, start with lower temperature.",
            "gradual_heating": "Start at minimum temperature and increase gradually until clean cut is achieved.",
            "cool_down": "Allow wire to cool completely before handling or storage.",
            "workspace_preparation": "Clear workspace of flammable materials. Use non-combustible work surface.",
            "emergency_procedures": "Know emergency shutdown procedures. Keep first aid kit accessible.",
        }

    def get_foam_type(self, foam_key: str) -> Optional[FoamType]:
        """Get foam type by key"""
        return self.foam_types.get(foam_key.upper())

    def get_all_foam_types(self) -> List[FoamType]:
        """Get list of all foam types"""
        return list(self.foam_types.values())

    def get_foam_names(self) -> List[str]:
        """Get list of foam names for UI"""
        return [
            f"{foam.abbreviation} - {foam.name}" for foam in self.foam_types.values()
        ]

    def get_foam_keys(self) -> List[str]:
        """Get list of foam keys for internal use"""
        return list(self.foam_types.keys())

    def get_recommended_temperature_range(
        self, foam_key: str
    ) -> Optional[Tuple[float, float, float]]:
        """Get recommended temperature range for foam type"""
        foam = self.get_foam_type(foam_key)
        if foam:
            return (
                foam.min_temp_celsius,
                foam.optimal_temp_celsius,
                foam.max_temp_celsius,
            )
        return None

    def is_temperature_safe(self, foam_key: str, temperature_celsius: float) -> bool:
        """Check if temperature is safe for foam type"""
        foam = self.get_foam_type(foam_key)
        if foam:
            return foam.min_temp_celsius <= temperature_celsius <= foam.max_temp_celsius
        return False

    def get_safety_warning(
        self, foam_key: str, temperature_celsius: float
    ) -> Optional[str]:
        """Get safety warning for temperature and foam combination"""
        foam = self.get_foam_type(foam_key)
        if not foam:
            return "Unknown foam type. Use caution and start with low temperatures."

        if temperature_celsius < foam.min_temp_celsius:
            return f"Temperature too low for {foam.name}. May not cut effectively. Recommended: {foam.min_temp_celsius}-{foam.max_temp_celsius}°C."
        elif temperature_celsius > foam.max_temp_celsius:
            return f"WARNING: Temperature too high for {foam.name}! Risk of decomposition and toxic fumes. Maximum: {foam.max_temp_celsius}°C."
        elif temperature_celsius > foam.optimal_temp_celsius + 10:
            return f"Temperature above optimal for {foam.name}. Consider reducing to {foam.optimal_temp_celsius}°C for cleaner cuts."

        return None

    def get_cutting_recommendations(self, foam_key: str) -> Dict[str, Any]:
        """Get cutting recommendations for foam type"""
        foam = self.get_foam_type(foam_key)
        if not foam:
            return {}

        return {
            "optimal_temperature": foam.optimal_temp_celsius,
            "temperature_range": (foam.min_temp_celsius, foam.max_temp_celsius),
            "cutting_speed": foam.cutting_speed,
            "safety_notes": foam.safety_notes,
            "applications": foam.applications,
            "density_range": foam.density_range_kg_m3,
            "melting_point": foam.melting_point_celsius,
            "decomposition_temp": foam.decomposition_temp_celsius,
        }

    def get_foam_suitable_for_temperature(
        self, temperature_celsius: float
    ) -> List[FoamType]:
        """Get foam types suitable for given temperature"""
        suitable_foams = []
        for foam in self.foam_types.values():
            if foam.min_temp_celsius <= temperature_celsius <= foam.max_temp_celsius:
                suitable_foams.append(foam)
        return suitable_foams

    def estimate_foam_type_from_description(self, description: str) -> Optional[str]:
        """Estimate foam type from user description"""
        description_lower = description.lower()

        # Common keywords and their associated foam types
        keywords = {
            "white": "EPS",
            "styrofoam": "EPS",
            "packaging": "EPS",
            "insulation": "XPS",
            "blue": "XPS",
            "pink": "XPS",
            "rc": "DEPRON",
            "aircraft": "EPP",
            "flexible": "EPE",
            "soft": "EVA",
            "craft": "FOAM_BOARD",
            "presentation": "FOAM_BOARD",
            "memory": "MEMORY_FOAM",
            "mattress": "MEMORY_FOAM",
            "wetsuit": "NEOPRENE",
            "rubber": "NEOPRENE",
            "polyurethane": "PU",
            "upholstery": "PU",
        }

        for keyword, foam_type in keywords.items():
            if keyword in description_lower:
                return foam_type

        return "EPS"  # Default to EPS if no match found


class FoamCuttingCalculator:
    """Calculator specifically for foam cutting applications"""

    def __init__(self):
        self.foam_db = FoamCuttingDatabase()

    def calculate_optimal_wire_temperature(
        self, foam_type: str, wire_diameter_mm: float, cutting_speed_mm_s: float = 5.0
    ) -> float:
        """Calculate optimal wire temperature for foam cutting"""
        foam = self.foam_db.get_foam_type(foam_type)
        if not foam:
            return 200.0  # Default temperature

        # Base temperature from foam database
        base_temp = foam.optimal_temp_celsius

        # Adjust for wire diameter (thicker wires need higher temps)
        # Reference diameter is 0.5mm (22 AWG)
        reference_diameter = 0.5
        diameter_factor = math.sqrt(wire_diameter_mm / reference_diameter)

        # Adjust for cutting speed (faster cuts need higher temps)
        # Reference speed is 5 mm/s
        reference_speed = 5.0
        speed_factor = math.sqrt(cutting_speed_mm_s / reference_speed)

        # Calculate adjusted temperature
        optimal_temp = base_temp * diameter_factor * speed_factor

        # Ensure temperature stays within safe range
        optimal_temp = max(
            foam.min_temp_celsius, min(optimal_temp, foam.max_temp_celsius)
        )

        return optimal_temp

    def calculate_power_requirements(
        self,
        foam_type: str,
        wire_diameter_mm: float,
        wire_length_m: float,
        target_temp_celsius: float,
    ) -> Dict[str, float]:
        """Calculate power requirements for foam cutting"""
        foam = self.foam_db.get_foam_type(foam_type)
        if not foam:
            foam = self.foam_db.get_foam_type("EPS")  # Default to EPS

        # Calculate wire resistance (simplified calculation)
        # Using nichrome resistance as baseline for cutting wire
        nichrome_resistance_per_meter = 1.0  # Approximate for 0.5mm wire
        wire_resistance = nichrome_resistance_per_meter * wire_length_m

        # Calculate required current for target temperature
        # This is a simplified thermal calculation
        temp_rise = target_temp_celsius - 20.0  # Ambient to target
        thermal_mass = (
            wire_diameter_mm * wire_length_m * 1000
        )  # Simplified thermal mass

        # Required power (simplified)
        required_power = thermal_mass * temp_rise * 0.001  # Simplified coefficient

        # Calculate current
        current = math.sqrt(required_power / wire_resistance)

        # Calculate voltage
        voltage = current * wire_resistance

        return {
            "current_amps": current,
            "voltage_volts": voltage,
            "power_watts": required_power,
            "resistance_ohms": wire_resistance,
            "temperature_celsius": target_temp_celsius,
        }

    def get_safety_recommendations(
        self, foam_type: str, wire_temperature: float, workspace_volume_m3: float = 10.0
    ) -> Dict[str, Any]:
        """Get safety recommendations for foam cutting operation"""
        foam = self.foam_db.get_foam_type(foam_type)
        if not foam:
            return {"warning": "Unknown foam type. Use extreme caution."}

        recommendations = {
            "foam_type": foam.name,
            "temperature_safe": self.foam_db.is_temperature_safe(
                foam_type, wire_temperature
            ),
            "safety_warning": self.foam_db.get_safety_warning(
                foam_type, wire_temperature
            ),
            "ventilation_required": wire_temperature > foam.optimal_temp_celsius + 10,
            "fume_extraction_recommended": wire_temperature
            > foam.max_temp_celsius - 20,
            "fire_risk_level": self._assess_fire_risk(foam_type, wire_temperature),
            "recommended_ppe": self._get_recommended_ppe(foam_type, wire_temperature),
            "workspace_requirements": self._get_workspace_requirements(
                foam_type, wire_temperature, workspace_volume_m3
            ),
        }

        return recommendations

    def _assess_fire_risk(self, foam_type: str, temperature_celsius: float) -> str:
        """Assess fire risk level"""
        foam = self.foam_db.get_foam_type(foam_type)
        if not foam:
            return "unknown"

        if temperature_celsius > foam.max_temp_celsius:
            return "high"
        elif temperature_celsius > foam.optimal_temp_celsius + 15:
            return "medium"
        else:
            return "low"

    def _get_recommended_ppe(
        self, foam_type: str, temperature_celsius: float
    ) -> List[str]:
        """Get recommended personal protective equipment"""
        foam = self.foam_db.get_foam_type(foam_type)
        if not foam:
            return ["safety_glasses", "heat_resistant_gloves"]

        ppe = ["safety_glasses", "heat_resistant_gloves"]

        if temperature_celsius > foam.optimal_temp_celsius:
            ppe.append("respirator")

        if temperature_celsius > foam.max_temp_celsius - 20:
            ppe.append("fire_extinguisher_nearby")

        return ppe

    def _get_workspace_requirements(
        self, foam_type: str, temperature_celsius: float, workspace_volume_m3: float
    ) -> Dict[str, Any]:
        """Get workspace requirements"""
        foam = self.foam_db.get_foam_type(foam_type)
        if not foam:
            return {"ventilation": "adequate", "clearance": "1_meter"}

        requirements = {
            "ventilation": (
                "adequate"
                if temperature_celsius <= foam.optimal_temp_celsius
                else "enhanced"
            ),
            "clearance": "1_meter",
            "fire_extinguisher": temperature_celsius > foam.max_temp_celsius - 20,
            "fume_extraction": temperature_celsius > foam.optimal_temp_celsius + 10,
            "workspace_size": (
                "adequate" if workspace_volume_m3 >= 5.0 else "consider_larger_area"
            ),
        }

        return requirements


# Convenience functions
def get_foam_cutting_info(foam_type: str) -> Dict[str, Any]:
    """Get complete foam cutting information"""
    calculator = FoamCuttingCalculator()
    foam = calculator.foam_db.get_foam_type(foam_type)

    if not foam:
        return {"error": "Foam type not found"}

    return {
        "foam_info": foam,
        "recommendations": calculator.foam_db.get_cutting_recommendations(foam_type),
        "optimal_temperature": calculator.calculate_optimal_wire_temperature(
            foam_type, 0.5
        ),  # 0.5mm wire
        "safety_guidelines": calculator.foam_db.safety_guidelines,
    }


def suggest_foam_for_temperature(temperature_celsius: float) -> List[Dict[str, Any]]:
    """Suggest foam types suitable for given temperature"""
    calculator = FoamCuttingCalculator()
    suitable_foams = calculator.foam_db.get_foam_suitable_for_temperature(
        temperature_celsius
    )

    return [
        {
            "name": foam.name,
            "abbreviation": foam.abbreviation,
            "optimal_temp": foam.optimal_temp_celsius,
            "applications": foam.applications[:3],  # First 3 applications
        }
        for foam in suitable_foams
    ]


if __name__ == "__main__":
    # Test the foam cutting database
    print("Foam Cutting Database Test")
    print("=" * 50)

    db = FoamCuttingDatabase()

    print("Available foam types:")
    for foam in db.get_all_foam_types():
        print(f"  {foam.abbreviation}: {foam.name}")

    print(f"\nEPP cutting info:")
    epp_info = get_foam_cutting_info("EPP")
    if "foam_info" in epp_info:
        foam = epp_info["foam_info"]
        print(f"  Optimal temperature: {foam.optimal_temp_celsius}°C")
        print(f"  Range: {foam.min_temp_celsius}-{foam.max_temp_celsius}°C")
        print(f"  Applications: {', '.join(foam.applications[:2])}")

    print(f"\nTemperature 200°C suitable foams:")
    suitable = suggest_foam_for_temperature(200)
    for item in suitable:
        print(f"  {item['abbreviation']}: {item['name']}")

    print(f"\nSafety test for EPS at 220°C:")
    calc = FoamCuttingCalculator()
    warning = calc.foam_db.get_safety_warning("EPS", 220)
    if warning:
        print(f"  Warning: {warning}")
    else:
        print("  Temperature is safe")
