# User guide

## Wire temperature estimate

Install from [source](installation/index.md), then run `wire-temp-gui`. Choose a wire material and diameter or gauge, wire length, and current range. Press **Calculate** to view a chart and results table. The model assumes 20 °C ambient temperature, approximate natural convection, a fixed emissivity, and an isolated wire in still air. Clamps, airflow, contact with foam, and supply behavior can change the actual temperature. See [validation and limitations](model-validation.md).

CLI examples:

```bash
wire-temp-calc --gauge 22 --material nichrome --current 1
wire-temp-calc --current-start 0.1 --current-end 5 --current-step 0.1
wire-temp-calc --list-units
```

Use `--current` for a single value. Use one or more of `--current-start`, `--current-end`, and `--current-step` for a range (defaults 0.1, 5.0, and 0.1 respectively). Do not combine `--current` with range options.

## Projects and PDF

After calculating in the GUI, use **File → Save Project** for a JSON file and **File → Open Project** to restore wire and current settings. The current project format does not preserve a custom cutting speed. Use **File → Export as PDF** to save the plotted chart or **File → Print** to open a system printer dialog. PDF export has an automated offscreen smoke test; printer hardware has not been tested.

## Foam information

Selecting a foam displays an **estimated cutting range**, not a safe exposure or fire threshold. The CLI provides `--safety-info EPS 250` for preliminary guidance. The foam type and actual product composition matter; consult the product safety data sheet. Do not rely on a low heuristic fire-risk label or an in-range result to omit ventilation. A temperature estimate describes an isolated wire, not the temperature or emissions of foam in contact with it.

Keep a hot wire supervised, prevent contact with flammables, and arrange suitable ventilation and fume control. See the [model and safety notes](model-validation.md) for sources and unresolved validation work.

For bugs and feature requests, use [GitHub Issues](https://github.com/Monotoba/HotWire/issues).
