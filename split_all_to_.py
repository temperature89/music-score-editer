from PyPDF2 import PdfReader, PdfWriter
from pathlib import Path
reader = PdfReader("./merged.pdf")
Path("./pdf_files").mkdir()

writer = PdfWriter()
for i, page in enumerate(reader.pages):
    writer.add_page(page)
    if i % 2 == 1:
        writer.write(f"./pdf_files/sample_{i}.pdf")
        writer.close()
        writer = PdfWriter()