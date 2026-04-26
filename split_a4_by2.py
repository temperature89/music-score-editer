from PyPDF2 import PdfReader, PdfWriter
from pathlib import Path
FILENAME = "宝島ピッコロ"
reader = PdfReader(f"../{FILENAME}.pdf")
Path("../outputs").mkdir()

writer = PdfWriter()
for i, page in enumerate(reader.pages):
    writer.add_page(page)
    if i % 2 == 1:
        writer.write(f"../outputs/{FILENAME}_{(i + 1) // 2}.pdf")
        writer.close()
        writer = PdfWriter()