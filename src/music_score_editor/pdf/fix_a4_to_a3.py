from pathlib import Path
from pypdf import PdfReader, PdfWriter, Transformation

A4 = (595.28, 841.89)
A3 = (1190.55, 841.89)


def crop_to_paper(
    input_pdf: str,
    output_pdf: str | None = None,
    paper_size: str = "A4",
):
    paper_size = paper_size.upper()

    if output_pdf is None:
        output_pdf = str(
            Path(input_pdf).with_stem(
                Path(input_pdf).stem + f"_{paper_size}"
            )
        )

    target_width, target_height = (
        A4 if paper_size == "A4" else A3
    )

    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    for page in reader.pages:
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

    with open(output_pdf, "wb") as f:
        writer.write(f)

    print(f"保存完了: {output_pdf}")