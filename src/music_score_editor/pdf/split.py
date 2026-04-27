from pathlib import Path
from pypdf import PdfReader, PdfWriter


def split_by_n(file: str, n: int) -> None:
    reader = PdfReader(file)

    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    input_path = Path(file)
    stem = input_path.stem

    writer = PdfWriter()
    part = 1

    for i, page in enumerate(reader.pages, start=1):
        writer.add_page(page)

        if i % n == 0:
            output_file = output_dir / f"{stem}_{part}.pdf"
            with open(output_file, "wb") as f:
                writer.write(f)

            writer = PdfWriter()
            part += 1

    # 余ったページを保存
    if len(writer.pages) > 0:
        output_file = output_dir / f"{stem}_{part}.pdf"
        with open(output_file, "wb") as f:
            writer.write(f)

# split_by_n("../output_a3_combined.pdf", 1)