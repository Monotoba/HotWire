# Fix Summary: QPrintDialog Import Error

## Problem
The application was failing to start with the error:
```
Error importing required modules: cannot import name 'QPrintDialog' from 'PySide6.QtWidgets'
```

## Root Cause
`QPrintDialog` was being imported from both `PySide6.QtWidgets` and `PySide6.QtPrintSupport`, causing a conflict. In PySide6, `QPrintDialog` should only be imported from `PySide6.QtPrintSupport`.

## Solution
Removed `QPrintDialog` from the `PySide6.QtWidgets` import statement in `main_window.py`:

**Before:**
```python
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                              QHBoxLayout, QGridLayout, QLabel, QLineEdit, 
                              QComboBox, QPushButton, QGroupBox, QTableWidget,
                              QTableWidgetItem, QHeaderView, QFileDialog,
                              QPrintDialog, QDialog, QTextEdit, QMessageBox)
```

**After:**
```python
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                              QHBoxLayout, QGridLayout, QLabel, QLineEdit, 
                              QComboBox, QPushButton, QGroupBox, QTableWidget,
                              QTableWidgetItem, QHeaderView, QFileDialog,
                              QDialog, QTextEdit, QMessageBox)
```

The `QPrintDialog` import is correctly handled by:
```python
from PySide6.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog
```

## Verification
- ✅ GUI imports test passes
- ✅ Application launches successfully
- ✅ Print functionality works correctly
- ✅ PDF export functionality works correctly

## Files Modified
- `main_window.py` - Fixed import statement (line 12)

## Testing
Run these commands to verify the fix:
```bash
# Test imports
. venv/bin/activate && python test_gui_imports.py

# Test application launch
./activate_and_run.sh
```

The application now starts successfully with Python 3.13 and all features are working correctly.