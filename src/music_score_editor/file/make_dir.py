from pathlib import Path

def make_dir(file: str):
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

    base = Path(file)
    base.mkdir(exist_ok=True)

    for i, name in enumerate(instruments, start=1):
        folder = base / f"{i:02d}_{name}"
        folder.mkdir(exist_ok=True)
