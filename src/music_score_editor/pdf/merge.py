from pathlib import Path
from pypdf import PdfReader, PdfWriter


def merge_pdfs(files: list[Path]):
    """複数のPDFファイルを結合する。"""
    writer = PdfWriter()

    for file in files:
        reader = PdfReader(str(file))
        for page in reader.pages:
            writer.add_page(page)
    writer.write(f"{files[1]}_merged.pdf")