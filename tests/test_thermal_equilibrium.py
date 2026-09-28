"""Check physical invariants of the estimated wire temperature model."""

import math

import pytest

from wire_temp_calc.wire_temp_calculator import WireTemperatureCalculator


@pytest.fixture
def calculator():
    return WireTemperatureCalculator()


def test_temperature_increases_with_current(calculator):
    wire = calculator.get_wire_properties(22, "AWG", "nichrome", 2, "feet")
    currents = (0, 0.1, 1, 2, 5, 10)
    temperatures = [
        calculator.calculate_temperature(wire, current) for current in currents
    ]
    assert temperatures[0] == calculator.ambient_temp
    assert all(a < b for a, b in zip(temperatures, temperatures[1:]))


@pytest.mark.parametrize("material", ("nichrome", "stainless", "kanthal"))
def test_equivalent_lengths_and_wire_diameters(calculator, material):
    settings = (
        (22, "AWG", 2, "feet"),
        (22, "AWG", 24, "inch"),
        (0.644, "mm", 0.6096, "meters"),
    )
    wires = [
        calculator.get_wire_properties(gauge, unit, material, length, length_unit)
        for gauge, unit, length, length_unit in settings
    ]
    for current in (0.5, 1, 3):
        baseline = calculator.calculate_temperature(wires[0], current)
        assert calculator.calculate_temperature(wires[1], current) == pytest.approx(
            baseline
        )
        assert calculator.calculate_temperature(wires[2], current) == pytest.approx(
            baseline, rel=0.02
        )


def test_equilibrium_balances_electrical_power_and_heat_loss(calculator):
    wire = calculator.get_wire_properties(24, "AWG", "kanthal", 0.6, "meters")
    temperature = calculator.calculate_temperature(wire, 2)
    electrical_power = 4 * calculator._calculate_resistance(wire, temperature)
    heat_loss = calculator._calculate_heat_transfer(wire, temperature) * (
        temperature - calculator.ambient_temp
    )
    assert electrical_power == pytest.approx(heat_loss, rel=1e-8)


@pytest.mark.parametrize(
    "material,resistivity", (("nichrome", 1.09), ("kanthal", 1.45))
)
def test_manufacturer_resistivity_at_room_temperature(
    calculator, material, resistivity
):
    # Kanthal datasheets give resistivity in Ω·mm²/m; compare R per metre.
    wire = calculator.get_wire_properties(1, "mm", material, 1, "meters")
    assert wire.resistance_per_meter == pytest.approx(resistivity / (math.pi / 4))


@pytest.mark.parametrize(
    "length,diameter", ((0, 0.5), (-1, 0.5), (1, 0), (1, math.nan))
)
def test_invalid_geometry_rejected(calculator, length, diameter):
    with pytest.raises(ValueError):
        calculator.get_wire_properties(diameter, "mm", "nichrome", length, "meters")


@pytest.mark.parametrize("current", (-1, math.nan, math.inf))
def test_invalid_currents_rejected(calculator, current):
    wire = calculator.get_wire_properties(22, "AWG", "nichrome", 2, "feet")
    with pytest.raises(ValueError, match="Current"):
        calculator.calculate_temperature(wire, current)
