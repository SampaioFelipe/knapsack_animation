import cx_Freeze

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
