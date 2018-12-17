import os
import sys
from cx_Freeze import setup, Executable
from pathlib import Path
import ulis43

build_dir = Path(__file__).parent / "build" / "-".join(
    ["Ulis43", sys.platform])

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {
    "packages": ["pathlib", "pygame", "yaml"],
    "excludes": ["tkinter", "PyQt4", "PyQt5", "matplotlib", "scipy"],
    "optimize": 2,
    "build_exe": str(build_dir)
}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"
    target_name = "Ulis43"
else:
    target_name = "run"

setup(
    name="Ulis43",
    version=ulis43.__version__,
    description="Ludum Dare 43 Jam Entry",
    options={"build_exe": build_exe_options},
    executables=[
        Executable("ulis43/gui.py", base=base, targetName=target_name)
    ])

# Make a launch script on linux

if sys.platform != "win32":
    launch_script = build_dir / "Ulis43.sh"
    launch_script.write_text("""#!/bin/bash\nLD_LIBRARY_PATH=./lib ./run\n""")
    os.chmod(str(launch_script), 0o775)
