from cx_Freeze import setup, Executable
import sys


import sys

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

