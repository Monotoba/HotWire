# Installation from source

Requires Python 3.10 or newer. The GUI also needs a working desktop display and Qt runtime libraries appropriate to your operating system. Source installation has been exercised in CI on Linux, macOS, and Windows; individual desktop configurations can differ.

```bash
git clone https://github.com/Monotoba/HotWire.git
cd HotWire
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
wire-temp-calc --help
wire-temp-gui
```

On Windows PowerShell use `py -m venv .venv`, `.venv\Scripts\Activate.ps1`, then the same `python -m pip install -e .` and commands. You can also run `python -m wire_temp_calc.main` in the activated environment.

For development, install `python -m pip install -e '.[dev]'` and run `pytest tests/`. On Linux without a display, use `QT_QPA_PLATFORM=offscreen pytest tests/`.

The convenience scripts `install.sh`/`activate_and_run.sh` and `install.bat`/`activate_and_run.bat` use `.venv`. The POSIX script syntax has been checked; the Windows scripts still need a manual installation test. There is no verified PyPI release or packaged desktop installer at this time. Open an [issue](https://github.com/Monotoba/HotWire/issues) with your OS, Python version, and traceback if installation fails.
