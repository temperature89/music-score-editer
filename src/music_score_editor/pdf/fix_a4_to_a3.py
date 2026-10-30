from pathlib import Path
from pypdf import PdfReader, PdfWriter, Transformation


def _iter_input_pdfs(input_path: str | Path):
    path = Path(input_path)
    if path.is_dir():
        return sorted(
            p for p in path.iterdir() if p.is_file() and p.suffix.lower() == ".pdf"
        )
    return [path]

A4 = (595.28, 841.89)
A3 = (1190.55, 841.89)


def crop_to_paper(
    input_pdf: str,
    output_pdf: str | None = None,
    paper_size: str = "A4",
):
    paper_size = paper_size.upper()
    input_path = Path(input_pdf)

    if output_pdf is None:
        output_pdf = str(
            input_path.with_stem(input_path.stem + f"_{paper_size}")
        )

    target_width, target_height = (
        A4 if paper_size == "A4" else A3
    )

    input_files = _iter_input_pdfs(input_path)
    if not input_files:
        raise FileNotFoundError(f"PDFファイルが見つかりません: {input_pdf}")

    if len(input_files) == 1 and input_path.is_file():
        output_paths = [Path(output_pdf)]
    else:
        output_dir = Path(output_pdf)
        output_dir.mkdir(parents=True, exist_ok=True)
        output_paths = [output_dir / f"{pdf_path.stem}_{paper_size}.pdf" for pdf_path in input_files]

    for pdf_path, output_path in zip(input_files, output_paths, strict=False):
        reader = PdfReader(pdf_path)
        writer = PdfWriter()

        for page in reader.pages:
            page = page.get_object()
            page.transfer_rotation_to_content()

            width = float(page.mediabox.width)
            height = float(page.mediabox.height)

            # 全面に広げる
            scale = max(
                target_width / width,
                target_height / height,
            )

            new_width = width * scale
            new_height = height * scale

            # 中央配置
            tx = (target_width - new_width) / 2
            ty = (target_height - new_height) / 2

            new_page = writer.add_blank_page(
                width=target_width,
                height=target_height,
            )

            new_page.merge_transformed_page(
                page,
                Transformation()
                .scale(scale)
                .translate(tx, ty),
            )

        with open(output_path, "wb") as f:
            writer.write(f)

        print(f"保存完了: {output_path}")