from pathlib import Path
from pypdf import PdfReader, PdfWriter


def rotate_pdf(input_pdf: str, angle: int, output_pdf: str | None = None) -> Path:
    """
    PDFを回転する（90, 180, 270度対応）
    """
    if angle not in [90, 180, 270]:
        raise ValueError("angleは90, 180, 270のいずれか")

    input_path = Path(input_pdf)
    if not input_path.exists():
        raise FileNotFoundError(f"ファイルが見つかりません: {input_pdf}")

    output_path = (
        Path(output_pdf)
        if output_pdf
        else input_path.with_name(input_path.stem + f"_rot{angle}.pdf")
    )

    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page in reader.pages:
        page.rotate(angle)  # ←ここがポイント
        writer.add_page(page)

    with open(output_path, "wb") as f:
        writer.write(f)

    return output_path


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("使い方: python rotate.py input.pdf 90 [output.pdf]")
        sys.exit(1)

    input_pdf = sys.argv[1]
    angle = int(sys.argv[2])
    output_pdf = sys.argv[3] if len(sys.argv) > 3 else None

    out = rotate_pdf(input_pdf, angle, output_pdf)
    print(f"出力完了: {out}")