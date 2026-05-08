from pathlib import Path
from pypdf import PdfReader, PdfWriter, Transformation


def fix_a4_to_a3(input_pdf: str, output_pdf: str | None = None) -> Path:
    """
    横向きA4のPDFをA3サイズに拡大して配置する
    """
    input_path = Path(input_pdf)
    if not input_path.exists():
        raise FileNotFoundError(f"ファイルが見つかりません: {input_pdf}")

    if output_pdf is None:
        output_path = input_path.with_name(input_path.stem + "_a3.pdf")
    else:
        output_path = Path(output_pdf)

    reader = PdfReader(input_path)
    writer = PdfWriter()

    # A3サイズ（ポイント単位）
    # 1 inch = 72 pt
    # A3: 297 × 420 mm → 約 (842 × 1191 pt)
    A3_WIDTH = 1191  # 横向き
    A3_HEIGHT = 842

    for page in reader.pages:
        # 元のサイズ取得
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)

        # スケール計算（A3に収まるように）
        scale_x = A3_WIDTH / width
        scale_y = A3_HEIGHT / height
        scale = min(scale_x, scale_y)

        # 新しい空ページ（A3）
        new_page = writer.add_blank_page(width=A3_WIDTH, height=A3_HEIGHT)

        # 中央配置のための移動量
        tx = (A3_WIDTH - width * scale) / 2
        ty = (A3_HEIGHT - height * scale) / 2

        # 変換（拡大＋移動）
        transformation = Transformation().scale(scale).translate(tx, ty)

        new_page.merge_transformed_page(page, transformation)

    with open(output_path, "wb") as f:
        writer.write(f)

    return output_path