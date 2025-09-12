#!/usr/bin/env python3
"""
Unit conversion system for wire gauge and length units
Supports AWG, mm, mils, SWG, and various length units
"""

import math
from typing import Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class WireGauge:
    """Wire gauge specification"""

    size: float
    unit: str
    diameter_mm: float


class WireGaugeConverter:
    """Convert between different wire gauge systems and diameter units"""

    # AWG (American Wire Gauge) to diameter in mm
    AWG_TO_MM = {
        0000: 11.684,
        000: 10.404,
        00: 9.266,
        0: 8.251,
        1: 7.348,
        2: 6.544,
        3: 5.827,
        4: 5.189,
        5: 4.621,
        6: 4.115,
        7: 3.665,
        8: 3.264,
        9: 2.906,
        10: 2.588,
        11: 2.305,
        12: 2.053,
        13: 1.828,
        14: 1.628,
        15: 1.450,
        16: 1.291,
        17: 1.150,
        18: 1.024,
        19: 0.912,
        20: 0.812,
        21: 0.723,
        22: 0.644,
        23: 0.573,
        24: 0.511,
        25: 0.455,
        26: 0.405,
        27: 0.361,
        28: 0.321,
        29: 0.286,
        30: 0.255,
        31: 0.227,
        32: 0.202,
        33: 0.180,
        34: 0.160,
        35: 0.143,
        36: 0.127,
        37: 0.113,
        38: 0.101,
        39: 0.090,
        40: 0.080,
    }

    # SWG (Standard Wire Gauge) to diameter in mm
    SWG_TO_MM = {
        1: 8.230,
        2: 7.620,
        3: 7.010,
        4: 6.540,
        5: 5.890,
        6: 5.380,
        7: 4.880,
        8: 4.470,
        9: 4.060,
        10: 3.660,
        11: 3.250,
        12: 2.950,
        13: 2.640,
        14: 2.410,
        15: 2.210,
        16: 2.030,
        17: 1.830,
        18: 1.630,
        19: 1.420,
        20: 1.220,
        21: 1.220,
        22: 1.016,
        23: 0.914,
        24: 0.813,
        25: 0.711,
        26: 0.610,
        27: 0.559,
        28: 0.508,
        29: 0.457,
        30: 0.406,
        31: 0.356,
        32: 0.305,
        33: 0.279,
        34: 0.254,
        35: 0.229,
        36: 0.203,
        37: 0.178,
        38: 0.152,
        39: 0.127,
        40: 0.102,
    }

    # Supported gauge units
    GAUGE_UNITS = ["AWG", "SWG", "mm", "mils", "inch"]

    @classmethod
    def awg_to_diameter_mm(cls, awg: int) -> float:
        """Convert AWG to diameter in mm"""
        if awg in cls.AWG_TO_MM:
            return cls.AWG_TO_MM[awg]
        else:
            # Use AWG formula for sizes not in table
            # d = 0.127 * 92^((36-AWG)/39)
            return 0.127 * (92 ** ((36 - awg) / 39))

    @classmethod
    def diameter_mm_to_awg(cls, diameter_mm: float) -> float:
        """Convert diameter in mm to AWG (returns float for non-standard sizes)"""
        # Find closest AWG size
        closest_awg = None
        min_diff = float("inf")

        for awg, dia in cls.AWG_TO_MM.items():
            diff = abs(dia - diameter_mm)
            if diff < min_diff:
                min_diff = diff
                closest_awg = awg

        # If exact match, return integer
        if min_diff < 0.001:
            return closest_awg

        # Otherwise, calculate fractional AWG using inverse formula
        # AWG = 36 - 39 * log10(d/0.127) / log10(92)
        import math

        awg_float = 36 - 39 * math.log10(diameter_mm / 0.127) / math.log10(92)
        return awg_float

    @classmethod
    def swg_to_diameter_mm(cls, swg: int) -> float:
        """Convert SWG to diameter in mm"""
        if swg in cls.SWG_TO_MM:
            return cls.SWG_TO_MM[swg]
        else:
            # For SWG sizes not in table, use interpolation
            # This is less accurate but works for estimation
            return cls._interpolate_swg(swg)

    @classmethod
    def _interpolate_swg(cls, swg: int) -> float:
        """Interpolate SWG diameter for sizes not in table"""
        if swg <= 0:
            return 10.0  # Large default
        if swg >= 50:
            return 0.01  # Small default

        # Find nearest known values
        lower_swg = max([s for s in cls.SWG_TO_MM.keys() if s <= swg])
        upper_swg = min([s for s in cls.SWG_TO_MM.keys() if s >= swg])

        if lower_swg == upper_swg:
            return cls.SWG_TO_MM[swg]

        # Linear interpolation
        lower_dia = cls.SWG_TO_MM[lower_swg]
        upper_dia = cls.SWG_TO_MM[upper_swg]

        ratio = (swg - lower_swg) / (upper_swg - lower_swg)
        return lower_dia + ratio * (upper_dia - lower_dia)

    @classmethod
    def diameter_mm_to_swg(cls, diameter_mm: float) -> float:
        """Convert diameter in mm to SWG (returns float for non-standard sizes)"""
        # Find closest SWG size
        closest_swg = None
        min_diff = float("inf")

        for swg, dia in cls.SWG_TO_MM.items():
            diff = abs(dia - diameter_mm)
            if diff < min_diff:
                min_diff = diff
                closest_swg = swg

        # If exact match, return integer
        if min_diff < 0.001:
            return closest_swg

        # Otherwise, return float based on interpolation
        return closest_swg + (diameter_mm - cls.SWG_TO_MM[closest_swg]) / min_diff

    @classmethod
    def convert_gauge_to_mm(cls, gauge_size: float, gauge_unit: str) -> float:
        """Convert any gauge unit to diameter in mm"""
        if gauge_unit == "AWG":
            return cls.awg_to_diameter_mm(int(gauge_size))
        elif gauge_unit == "SWG":
            return cls.swg_to_diameter_mm(int(gauge_size))
        elif gauge_unit == "mm":
            return gauge_size
        elif gauge_unit == "mils":
            return gauge_size * 0.0254  # 1 mil = 0.0254 mm
        elif gauge_unit == "inch":
            return gauge_size * 25.4  # 1 inch = 25.4 mm
        else:
            raise ValueError(f"Unsupported gauge unit: {gauge_unit}")

    @classmethod
    def convert_mm_to_gauge(cls, diameter_mm: float, target_unit: str) -> float:
        """Convert diameter in mm to specified gauge unit"""
        if target_unit == "AWG":
            return cls.diameter_mm_to_awg(diameter_mm)
        elif target_unit == "SWG":
            return cls.diameter_mm_to_swg(diameter_mm)
        elif target_unit == "mm":
            return diameter_mm
        elif target_unit == "mils":
            return diameter_mm / 0.0254  # mm to mils
        elif target_unit == "inch":
            return diameter_mm / 25.4  # mm to inches
        else:
            raise ValueError(f"Unsupported gauge unit: {target_unit}")

    @classmethod
    def get_standard_gauge_sizes(cls, unit: str) -> list:
        """Get list of standard gauge sizes for a unit"""
        if unit == "AWG":
            return sorted([k for k in cls.AWG_TO_MM.keys() if isinstance(k, int)])
        elif unit == "SWG":
            return sorted([k for k in cls.SWG_TO_MM.keys() if isinstance(k, int)])
        elif unit in ["mm", "mils", "inch"]:
            # Return common diameter sizes for metric/imperial units
            if unit == "mm":
                return [
                    0.1,
                    0.2,
                    0.3,
                    0.4,
                    0.5,
                    0.6,
                    0.7,
                    0.8,
                    0.9,
                    1.0,
                    1.2,
                    1.5,
                    2.0,
                    2.5,
                    3.0,
                    4.0,
                    5.0,
                ]
            elif unit == "mils":
                return [5, 10, 15, 20, 25, 30, 40, 50, 75, 100, 125, 150, 200]
            elif unit == "inch":
                return [
                    0.005,
                    0.010,
                    0.015,
                    0.020,
                    0.025,
                    0.030,
                    0.040,
                    0.050,
                    0.075,
                    0.100,
                ]
        else:
            return []


class LengthUnitConverter:
    """Convert between different length units"""

    # Conversion factors to millimeters
    TO_MM = {
        "mm": 1.0,
        "cm": 10.0,
        "inch": 25.4,
        "mils": 0.0254,
        "foot": 304.8,
        "feet": 304.8,
        "yard": 914.4,
        "meter": 1000.0,
        "meters": 1000.0,
    }

    # Abbreviation mappings
    ABBREVIATIONS = {
        "mm": "mm",
        "millimeter": "mm",
        "millimeters": "mm",
        "cm": "cm",
        "centimeter": "cm",
        "centimeters": "cm",
        "in": "inch",
        "inch": "inch",
        "inches": "inch",
        "mil": "mils",
        "mils": "mils",
        "ft": "feet",
        "foot": "feet",
        "feet": "feet",
        "yd": "yard",
        "yard": "yard",
        "yards": "yard",
        "m": "meters",
        "meter": "meters",
        "meters": "meters",
    }

    @classmethod
    def normalize_unit(cls, unit: str) -> str:
        """Normalize unit string to standard form"""
        unit = unit.lower().strip()
        return cls.ABBREVIATIONS.get(unit, unit)

    @classmethod
    def convert_length(cls, value: float, from_unit: str, to_unit: str) -> float:
        """Convert length between units"""
        from_unit = cls.normalize_unit(from_unit)
        to_unit = cls.normalize_unit(to_unit)

        if from_unit not in cls.TO_MM:
            raise ValueError(f"Unsupported from unit: {from_unit}")
        if to_unit not in cls.TO_MM:
            raise ValueError(f"Unsupported to unit: {to_unit}")

        # Convert to mm first, then to target unit
        mm_value = value * cls.TO_MM[from_unit]
        return mm_value / cls.TO_MM[to_unit]

    @classmethod
    def to_mm(cls, value: float, unit: str) -> float:
        """Convert any length to millimeters"""
        unit = cls.normalize_unit(unit)
        if unit not in cls.TO_MM:
            raise ValueError(f"Unsupported unit: {unit}")
        return value * cls.TO_MM[unit]

    @classmethod
    def from_mm(cls, value_mm: float, unit: str) -> float:
        """Convert millimeters to specified unit"""
        unit = cls.normalize_unit(unit)
        if unit not in cls.TO_MM:
            raise ValueError(f"Unsupported unit: {unit}")
        return value_mm / cls.TO_MM[unit]

    @classmethod
    def get_supported_units(cls) -> list:
        """Get list of supported length units"""
        return list(cls.TO_MM.keys())

    @classmethod
    def get_unit_abbreviations(cls) -> list:
        """Get list of unit abbreviations for UI"""
        return ["mm", "cm", "inch", "mils", "feet", "yard", "meters"]


# Convenience functions
def convert_wire_gauge(gauge_size: float, from_unit: str, to_unit: str) -> float:
    """Convert wire gauge between different units"""
    # First convert to diameter in mm
    diameter_mm = WireGaugeConverter.convert_gauge_to_mm(gauge_size, from_unit)
    # Then convert to target unit
    return WireGaugeConverter.convert_mm_to_gauge(diameter_mm, to_unit)


def convert_length(value: float, from_unit: str, to_unit: str) -> float:
    """Convert length between units"""
    return LengthUnitConverter.convert_length(value, from_unit, to_unit)


if __name__ == "__main__":
    # Test the converters
    print("Wire Gauge Converter Test")
    print("=" * 40)

    # Test AWG conversions
    print("22 AWG to mm:", WireGaugeConverter.awg_to_diameter_mm(22))
    print("0.644 mm to AWG:", WireGaugeConverter.diameter_mm_to_awg(0.644))

    # Test SWG conversions
    print("22 SWG to mm:", WireGaugeConverter.swg_to_diameter_mm(22))
    print("0.711 mm to SWG:", WireGaugeConverter.diameter_mm_to_swg(0.711))

    # Test unit conversions
    print("\nLength Converter Test")
    print("=" * 40)
    print("2.5 mm to inches:", LengthUnitConverter.convert_length(2.5, "mm", "inch"))
    print("0.1 inch to mm:", LengthUnitConverter.convert_length(0.1, "inch", "mm"))
    print("1 foot to meters:", LengthUnitConverter.convert_length(1, "feet", "meters"))

    # Test wire gauge unit conversions
    print("\nWire Gauge Unit Test")
    print("=" * 40)
    print("22 AWG to mils:", convert_wire_gauge(22, "AWG", "mils"))
    print("0.025 inch to AWG:", convert_wire_gauge(0.025, "inch", "AWG"))
