import os
import subprocess
for (_, _, ui_files) in os.walk('ui/xml'):
    for ui_file in ui_files:
        name = ui_file[:-3]
        subprocess.run(
            ["pyside6-uic", f"ui/xml/{ui_file}", "-o", f"ui/{name}_ui.py"])
