from PyPDF2 import PdfReader, PdfWriter
from pathlib import Path
FILENAME = "宝島グロッケン"
reader = PdfReader(f"../{FILENAME}.pdf")
Path("../outputs").mkdir()

for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)
    writer.write(f"../outputs/{FILENAME}_{i}.pdf")
    writer.close()