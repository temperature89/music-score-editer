from PyPDF2 import PdfReader, PdfWriter
from pathlib import Path

FILENAME = "music_folder"

def main():
    root = Path(f"./{FILENAME}")
    matches = []
    for p in root.rglob("*.pdf"):
        writer = PdfWriter()
        writer.append(p)
        writer.write(f"./output/{p.name}")
        writer.close()
        
if __name__ == "__main__":
    main()