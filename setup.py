import cx_Freeze
import os

os.environ['TCL_LIBRARY'] = r"C:\Python\Python36\tcl\tcl8.6"
os.environ['TK_LIBRARY'] = r"C:\Python\Python36\tcl\tcl8.6"

exes = [cx_Freeze.Executable("main.py")]

cx_Freeze.setup(name="knapsack_exe",
                options={"build_exe": {"packages": ["pygame"],
                                       "include_files": ["assets/knapsack-logo.png",
                                                         "assets/mochila_cinza.png",
                                                         "assets/mochila_verde.png",
                                                         "assets/mochila_vermelha.png"]
                                       }},
                description="algumas descrição",
                executables=exes
                )
