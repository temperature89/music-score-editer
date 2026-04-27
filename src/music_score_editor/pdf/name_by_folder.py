import os
from pathlib import Path
FILENAME = "music_folder"


def main():
    root = Path(f"./{FILENAME}")
    i = 1
    for p in root.rglob("*.pdf"):
        os.rename(p.name, f"{FILENAME}_{i}")
        i += 1
        
if __name__ == "__main__":
    main()