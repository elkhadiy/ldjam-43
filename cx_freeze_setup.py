import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["pathlib","pygame","yaml"],
    "excludes": ["tkinter", "PyQt4", "PyQt5", "matplotlib", "scipy"],
    "optimize": 2
    }

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "ulis43",
        version = "1.0.1",
        description = "Ludum Dare ",
        options = {"build_exe": build_exe_options},
        executables = [Executable("ulis43/gui.py", base=base, targetName="ulis43")])
