from pathlib import Path
from pypdf import PdfReader, PdfWriter, Transformation

# 用紙サイズ（ポイント）
A4 = (595.28, 841.89)
A3 = (1190.55, 841.89)

def resize_pdf(
    input_pdf: str,
    output_pdf: str | None = None,
    paper_size: str = "A4",
):
    paper_size = paper_size.upper()

    if output_pdf is None:
        output_pdf = (
            Path(input_pdf).stem
            + f"_{paper_size}.pdf"
        )

    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    target_width, target_height = A4 if paper_size.upper() == "A4" else A3

    for page in reader.pages:
        # 元サイズ
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)

        # 比率維持で拡大縮小
        scale = min(target_width / width, target_height / height)

        new_width = width * scale
        new_height = height * scale

        # 中央配置
        tx = (target_width - new_width) / 2
        ty = (target_height - new_height) / 2

        # 新しい空ページ
        new_page = writer.add_blank_page(
            width=target_width,
            height=target_height,
        )

        # 変換
        new_page.merge_transformed_page(
            page,
            Transformation()
            .scale(scale)
            .translate(tx, ty),
        )

    with open(output_pdf, "wb") as f:
        writer.write(f)

    print(f"保存完了: {output_pdf}")
