from pathlib import Path
from pypdf import PdfReader, PdfWriter


def extract_pages(input_pdf: str, start_page: int, end_page: int, output_pdf: str | None = None) -> Path:
    """
    PDFの指定したページ範囲を抽出して新しいPDFとして保存する。

    Parameters
    ----------
    input_pdf : str
        元のPDFファイルのパス
    start_page : int
        抽出開始ページ（1始まり）
    end_page : int
        抽出終了ページ（1始まり、含む）
    output_pdf : str | None
        出力ファイル名。省略時は自動生成。

    Returns
    -------
    Path
        保存したPDFファイルのパス
    """
    input_path = Path(input_pdf)

    if not input_path.exists():
        raise FileNotFoundError(f"ファイルが見つかりません: {input_pdf}")

    reader = PdfReader(input_path)
    total_pages = len(reader.pages)

    if not (1 <= start_page <= end_page <= total_pages):
        raise ValueError(
            f"ページ範囲が不正です。1〜{total_pages} の範囲で指定してください。"
        )

    if output_pdf is None:
        output_path = input_path.with_name(
            f"{input_path.stem}_p{start_page}-{end_page}{input_path.suffix}"
        )
    else:
        output_path = Path(output_pdf)

    writer = PdfWriter()

    for page_num in range(start_page - 1, end_page):
        writer.add_page(reader.pages[page_num])

    with open(output_path, "wb") as f:
        writer.write(f)

    return output_path


if __name__ == "__main__":
    input_file = input("PDFファイルのパス: ")
    start = int(input("開始ページ: "))
    end = int(input("終了ページ: "))

    output = extract_pages(input_file, start, end)
    print(f"保存しました: {output}")