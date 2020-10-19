import sys
import cx_Freeze
import os
import matplotlib

 
# Dependencies are automatically detected, but it might need fine tuning.
os.environ['TCL_LIBRARY'] = "C:\\LOCAL_TO_PYTHON\\PYTHON37-64\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\LOCAL_TO_PYTHON\\PYTHON37-64\\tcl\\tk8.6"

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None

if sys.platform == "win32":
    base = "Win32GUI"
 
executables = [cx_Freeze.Executable("datamungingwinservice.py", base = base)] 

cx_Freeze.setup( 
    name = "Data Munging Win Service",
    options = {"build_exe": {"packages":["watchdog", "watchdog.observers", "watchdog.events","pandas","numpy","os","sys","tkinter","openpyxl","datetime","csv",
                                         "unicodedata","getpass","re","json","pyodbc","getpass","http","glob","pathlib","databaseconnection","pathtools"]}},
    version = "0.0.1",
    description = "",
    executables = executables
    )
