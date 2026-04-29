from pathlib import Path
from pypdf import PdfReader, PdfWriter


def remove_pages(
    input_pdf: str,
    pages_to_remove: list[int],
    output_pdf: str | None = None,
) -> Path:
    """指定したページを削除したPDFを作成する。"""
    input_path = Path(input_pdf)

    if not input_path.exists():
        raise FileNotFoundError(f"ファイルが見つかりません: {input_pdf}")

    reader = PdfReader(input_path)
    total_pages = len(reader.pages)

    # 1始まり → 0始まりに変換
    remove_set = {p - 1 for p in pages_to_remove}

    # ページ番号の検証
    for p in remove_set:
        if p < 0 or p >= total_pages:
            raise ValueError(f"無効なページ番号です: {p + 1}")

    if output_pdf is None:
        output_path = input_path.with_stem(f"{input_path.stem}_removed")
    else:
        output_path = Path(output_pdf)

    writer = PdfWriter()

    # 削除対象以外のページを追加
    for i, page in enumerate(reader.pages):
        if i not in remove_set:
            writer.add_page(page)

    with output_path.open("wb") as f:
        writer.write(f)

    return output_path


if __name__ == "__main__":
    input_file = input("入力PDFファイル: ")
    pages = input("削除するページ番号（カンマ区切り、例: 2,5,7）: ")

    pages_to_remove = [int(p.strip()) for p in pages.split(",")]

    output_file = remove_pages(input_file, pages_to_remove)
    print(f"保存しました: {output_file}")