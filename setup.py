from cx_Freeze import setup, Executable
import sys


import sys
"""
base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

executables = [
                Executable('main.py', base=base)
              ]

setup(name='Biblio',
      author='Escande Damien',
      version='0.1',
      description='Manage your books without burden',
      executables=executables
      )

"""

import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os","pygal"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "Biblio",
        version = "0.2",
        description = "Manage your personal books with ease",
        options = {"build_exe": build_exe_options},
        executables = [Executable("main.py", base=base)])
