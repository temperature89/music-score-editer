from pathlib import Path
import os

FILENAME = "宝島"
path = Path(f"../{FILENAME}")
instruments = [
    "Picc_Fl_Ob_Fg",
    "Cl",
    "Sax",
    "Hr",
    "Tb",
    "Bass",
    "Perc",
    "スコア",
]

path.mkdir()
for i, name in enumerate(instruments):
    folder_name = path / f"0{i + 1}_{name}"
    folder_name.mkdir()