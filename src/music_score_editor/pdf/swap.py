from pathlib import Path
from pypdf import PdfReader, PdfWriter


def _iter_input_pdfs(input_path: str | Path):
    path = Path(input_path)
    if path.is_dir():
        return sorted(
            p for p in path.iterdir() if p.is_file() and p.suffix.lower() == ".pdf"
        )
    return [path]


def swap_pages(
    input_pdf: str | Path,
    pages: list[int],
    output_pdf: str | Path | None = None,
) -> list[Path]:
    """指定したページ同士を入れ替えたPDFを作成する。

    `pages` は 1始まりのページ番号を偶数個並べる。先頭から2つずつを組にして
    順に入れ替える。例: [1, 3] は1ページ目と3ページ目を交換する。
    """
    if len(pages) < 2 or len(pages) % 2 != 0:
        raise ValueError("入れ替えるページは2つ以上の偶数個で指定してください。")

    pairs = list(zip(pages[::2], pages[1::2], strict=False))

    input_path = Path(input_pdf)
    if not input_path.exists():
        raise FileNotFoundError(f"ファイルが見つかりません: {input_pdf}")

    input_files = _iter_input_pdfs(input_path)
    if not input_files:
        raise FileNotFoundError(f"PDFファイルが見つかりません: {input_pdf}")

    if output_pdf is None:
        output_pdf = str(input_path.with_stem(f"{input_path.stem}_swapped"))

    if len(input_files) == 1 and input_path.is_file():
        output_paths = [Path(output_pdf)]
    else:
        output_dir = Path(output_pdf)
        output_dir.mkdir(parents=True, exist_ok=True)
        output_paths = [
            output_dir / f"{pdf_path.stem}_swapped.pdf" for pdf_path in input_files
        ]

    saved: list[Path] = []
    for pdf_path, output_path in zip(input_files, output_paths, strict=False):
        reader = PdfReader(pdf_path)
        source_pages = list(reader.pages)
        total_pages = len(source_pages)

        order = list(range(total_pages))
        for a, b in pairs:
            if not (1 <= a <= total_pages and 1 <= b <= total_pages):
                raise ValueError(
                    f"{pdf_path.name}: 無効なページ番号です: {a}, {b} "
                    f"(全{total_pages}ページ)"
                )
            ia, ib = a - 1, b - 1
            order[ia], order[ib] = order[ib], order[ia]

        writer = PdfWriter()
        for index in order:
            writer.add_page(source_pages[index])

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open("wb") as f:
            writer.write(f)

        print(f"保存完了: {output_path}")
        saved.append(output_path)

    return saved
