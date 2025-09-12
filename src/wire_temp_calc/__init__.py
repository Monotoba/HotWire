"""
Wire Temperature Calculator - Professional foam cutting and wire heating calculator

A comprehensive application for calculating wire temperatures and foam cutting parameters
with support for multiple wire gauge units, length units, and foam types.
"""

__version__ = "2.0.0"
__author__ = "Wire Temperature Calculator Team"
__email__ = "support@wiretempcalc.com"
__description__ = "Professional wire temperature and foam cutting calculator"

from .wire_temp_calculator import (
    WireTemperatureCalculator,
    WireProperties,
    ProjectManager,
)
from .unit_conversions import WireGaugeConverter, LengthUnitConverter
from .foam_cutting import FoamCuttingCalculator, FoamCuttingDatabase

__all__ = [
    "WireTemperatureCalculator",
    "WireProperties",
    "ProjectManager",
    "WireGaugeConverter",
    "LengthUnitConverter",
    "FoamCuttingCalculator",
    "FoamCuttingDatabase",
]
