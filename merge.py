from PyPDF2 import PdfReader, PdfWriter
from pathlib import Path

FILENAME = "music_folder"

def main():
    root = Path(f"./{FILENAME}")
    matches = []
    for p in root.rglob("*.pdf"):
        matches.append(p)
    writer = PdfWriter()
    for m in matches:
        writer.append(m)
        
    writer.write("merged.pdf")
    writer.close()

if __name__ == "__main__":
    main()