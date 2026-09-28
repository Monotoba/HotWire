"""Exercise the installed CLI exactly as users invoke it."""

import subprocess
import sysconfig
from pathlib import Path

import pytest


@pytest.fixture(scope="module")
def command():
    executable = Path(sysconfig.get_path("scripts")) / (
        "wire-temp-calc.exe"
        if sysconfig.get_platform().startswith("win")
        else "wire-temp-calc"
    )
    assert executable.exists(), "Install the package before running CLI tests"
    return str(executable)


def run_cli(command, *args):
    return subprocess.run([command, *args], capture_output=True, text=True, timeout=30)


def test_list_foams(command):
    result = run_cli(command, "--list-foams")
    assert result.returncode == 0, result.stderr
    assert "Expanded Polystyrene" in result.stdout
    assert "Temperature range: 180-220°C" in result.stdout
    assert "Notes:" in result.stdout


def test_safety_info_and_warning(command):
    result = run_cli(command, "--safety-info", "EPS", "250")
    assert result.returncode == 0, result.stderr
    assert "Fire risk level: high" in result.stdout
    assert "Modeled upper bound: 220°C" in result.stdout
    assert "Ventilation required: Yes" in result.stdout


@pytest.mark.parametrize(
    "foam,temperature", [("UNKNOWN", "250"), ("EPS", "bad"), ("EPS", "nan")]
)
def test_safety_info_rejects_bad_input(command, foam, temperature):
    result = run_cli(command, "--safety-info", foam, temperature)
    assert result.returncode != 0
    assert "Error:" in result.stderr
    assert "Traceback" not in result.stderr


def test_single_current(command):
    result = run_cli(
        command, "--gauge", "22", "--material", "nichrome", "--current", "1"
    )
    assert result.returncode == 0, result.stderr
    assert "Current: 1.0 A" in result.stdout
    assert "Temperature:" in result.stdout
    assert "Temperature vs Current" not in result.stdout


def test_default_current(command):
    result = run_cli(command)
    assert result.returncode == 0, result.stderr
    assert "Current: 1.0 A" in result.stdout


def test_explicit_range(command):
    result = run_cli(
        command, "--current-start", "1", "--current-end", "2", "--current-step", "0.5"
    )
    assert result.returncode == 0, result.stderr
    assert "Temperature vs Current" in result.stdout
    assert "Current (A) | Temperature (°C)" in result.stdout


@pytest.mark.parametrize(
    "args",
    [
        ("--current", "1", "--current-start", "0.1"),
        ("--current-start", "2", "--current-end", "1"),
        ("--current-step", "0"),
        ("--current", "nan"),
    ],
)
def test_invalid_current_arguments(command, args):
    result = run_cli(command, *args)
    assert result.returncode == 2
    assert "error:" in result.stderr
    assert "Traceback" not in result.stderr
