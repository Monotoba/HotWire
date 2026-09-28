# Model validation and limitations

This page describes what was checked for the alpha version and what remains unverified. **No measured wire-temperature calibration or material-specific occupational exposure assessment has been performed.**

## Wire model

At a given current, the solver finds a steady-state temperature where `I² R(T)` equals estimated convection plus radiation from a cylindrical wire. It assumes ambient temperature 20 °C, natural convection coefficient 10 W/(m²·K), uniform wire temperature, fixed emissivity, and a temperature-dependent resistance approximation. It ignores support conduction, contacts, forced airflow, foam contact, transient heating, local hot spots, power-supply regulation, wire oxidation, and changes in emissivity. The solver stops if it cannot find equilibrium below 2000 °C; this is a numerical bound, **not** a permissible material temperature.

20 °C resistivity inputs (Ω·mm²/m):

| UI material | Model input | Evidence and limitation |
| --- | ---: | --- |
| Nichrome | 1.09 | [Kanthal Nikrothal 80 datasheet](https://www.kanthal.com/products/datasheets/material-datasheets/wire/resistance-heating-wire-and-resistance-wire/nikrothal-80/); the user's alloy may differ. |
| Kanthal | 1.45 | [Kanthal A-1 datasheet](https://prodshop.kanthal.com/en/products/datasheets/material-datasheets/wire/resistance-heating-wire-and-resistance-wire/kanthal_a_1/); other Kanthal grades may differ. |
| Stainless | 0.672 | Generic estimate retained pending selection and verification of a specific grade. |

Manufacturer data constrain electrical resistivity, **not** the full temperature prediction. Temperature-dependent resistance, convection, and emissivity are approximations. A user-entered resistance per foot overrides the room-temperature resistance used in a GUI calculation. The formulas are tested for current monotonicity, equivalent unit inputs, and power balance; those are consistency checks, not measurement validation.

**Before using the estimate to set hardware:** identify the exact wire alloy and dimensions, measure cold resistance and operating wire temperature with a suitable method over the intended current range, and record airflow and mounting. Compare measurements to predictions and revise the model or show uncertainty. Do not extrapolate beyond validated conditions.

## Foam guidance

The ten built-in foam ranges and speed adjustments are unverified heuristics. They are not decomposition temperatures, exposure limits, fire limits, or proof of safe cutting. The application does not measure smoke or airborne exposure and cannot determine ventilation adequacy from workspace volume or wire temperature. Use the exact foam product's safety data sheet and an appropriate exposure-control assessment. The [UK Health and Safety Executive's hot-wire cutting guidance](https://www.hse.gov.uk/plastics/fire-safety.htm#hot-wire) discusses overheating, fire, and fume hazards for flexible PU foam; its discussion is not a validation of HotWire's numbers for other foam products.

The CLI and GUI retain preliminary warnings and risk categories for exploration, but a “low” label cannot rule out hazardous fumes or fire. Ventilation is recommended regardless of the estimated cutting range. A physical wire temperature is not necessarily the temperature of the heated foam. Additional material-by-material evidence and emission measurements are required before using foam guidance for an operating procedure.

## Validation performed

- Automated tests: CLI behavior, GUI calculation and PDF smoke test, project round trip, equivalent units, current trend, power balance, and manufacturer room-temperature resistivity inputs.
- Source/wheel packaging and cross-platform CI are checked separately in the [release checklist](release-checklist.md).
- No wire thermometry, fume sampling, fire testing, installer usability testing, or print hardware testing has been performed.
