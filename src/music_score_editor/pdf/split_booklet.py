from pathlib import Path
from pypdf import PdfReader, PdfWriter, Transformation, PageObject


def booklet_a3_to_a4(input_pdf: str, output_pdf: str | None = None) -> Path:
    """
    A3両面・中綴じ用に面付けされたPDFを、
    ページ順に並んだA4 PDFへ変換する。

    例:
        [8|1], [2|7], [6|3], [4|5]
            ↓
        [1, 2, 3, 4, 5, 6, 7, 8]
    """
    input_path = Path(input_pdf)
    if not input_path.exists():
        raise FileNotFoundError(f"ファイルが見つかりません: {input_path}")

    if output_pdf is None:
        output_path = input_path.with_name(f"{input_path.stem}_ordered_a4.pdf")
    else:
        output_path = Path(output_pdf)

    reader = PdfReader(str(input_path))
    a3_page_count = len(reader.pages)
    a4_page_count = a3_page_count * 2

    if a4_page_count % 4 != 0:
        raise ValueError(
            "中綴じPDFとして不正です。A4ページ数は4の倍数である必要があります。"
        )

    # 最終的なA4ページを順番どおりに格納する配列
    ordered_pages: list[PageObject | None] = [None] * a4_page_count

    for i, page in enumerate(reader.pages):
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)
        half_width = width / 2

        # 左ページ作成
        left_page = PageObject.create_blank_page(
            width=half_width,
            height=height,
        )
        left_page.merge_transformed_page(
            page,
            Transformation(),
        )
        left_page.mediabox.lower_left = (0, 0)
        left_page.mediabox.upper_right = (half_width, height)

        # 右ページ作成
        right_page = PageObject.create_blank_page(
            width=half_width,
            height=height,
        )
        right_page.merge_transformed_page(
            page,
            Transformation().translate(tx=-half_width, ty=0),
        )

        # 中綴じ面付けのページ番号を計算（1始まり）
        if i % 2 == 0:
            left_num = a4_page_count - i
            right_num = i + 1
        else:
            left_num = i + 1
            right_num = a4_page_count - i

        ordered_pages[left_num - 1] = left_page
        ordered_pages[right_num - 1] = right_page

    writer = PdfWriter()
    for page in ordered_pages:
        if page is None:
            raise RuntimeError("ページの並べ替えに失敗しました。")
        writer.add_page(page)

    with open(output_path, "wb") as f:
        writer.write(f)

    return output_path