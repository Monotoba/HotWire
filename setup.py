#!/usr/bin/env python3
"""
Setup script for Wire Temperature Calculator - Professional foam cutting and wire heating calculator
"""

from setuptools import setup, find_packages
import os

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

# Read version from package
version_file = os.path.join("src", "wire_temp_calc", "__init__.py")
with open(version_file, "r", encoding="utf-8") as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().strip('"').strip("'")
            break
    else:
        version = "2.0.0"

setup(
    name="wire-temperature-calculator",
    version=version,
    author="Wire Temperature Calculator Team",
    description="Professional wire temperature calculator with comprehensive foam cutting capabilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Monotoba/HotWire",
    project_urls={
        "Bug Reports": "https://github.com/Monotoba/HotWire/issues",
        "Source": "https://github.com/Monotoba/HotWire",
        "Documentation": "https://github.com/Monotoba/HotWire/tree/main/docs",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Manufacturing",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Education",
        "Topic :: Office/Business",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "flake8>=5.0.0",
            "black>=22.0.0",
            "mypy>=0.991",
            "build>=0.8.0",
            "twine>=4.0.0",
        ],
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.0.0",
            "myst-parser>=0.18.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "wire-temp-calc=wire_temp_calc.cli:main",
            "wire-temperature-calculator=wire_temp_calc.main:main",
        ],
        "gui_scripts": [
            "wire-temp-gui=wire_temp_calc.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "wire_temp_calc": [
            "resources/*",
            "templates/*",
        ],
    },
    zip_safe=False,
)
