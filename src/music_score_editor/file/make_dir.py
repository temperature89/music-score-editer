from pathlib import Path

def make_dir(base_name: str, subdir_names: list[str]):
    instruments = [
        "Picc_Fl_Ob_Fg",
        "Cl",
        "Sax",
        "Tp",
        "Hr",
        "Tb",
        "Bass",
        "Perc",
        "スコア",
    ]

    base = Path(base_name)
    base.mkdir(exist_ok=True)

    for i, instrument in enumerate(instruments, start=1):
        instrument_dir = base / f"{i:02d}_{instrument}"
        instrument_dir.mkdir(exist_ok=True)
        
        if subdir_names == [""]:
            continue
        
        for subdir_name in subdir_names:
            subdir = Path(subdir_name)
            (instrument_dir / subdir).mkdir(exist_ok=True)