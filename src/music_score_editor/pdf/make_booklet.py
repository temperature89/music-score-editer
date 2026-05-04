from pathlib import Path
from pypdf import PdfReader, PdfWriter, Transformation, PageObject 


def impose_booklet(input_pdf: str, output_pdf: str | None = None) -> Path:
    """A4 PDFをA3両面・中綴じ用に面付けする。"""
    input_path = Path(input_pdf)
    if not input_path.exists():
        raise FileNotFoundError(f"ファイルが見つかりません: {input_pdf}")

    if output_pdf is None:
        output_path = input_path.with_name(f"{input_path.stem}_booklet.pdf")
    else:
        output_path = Path(output_pdf)

    reader = PdfReader(str(input_path))
    writer = PdfWriter()

    pages = list(reader.pages)
    original_count = len(pages)

    # 4の倍数になるまで空白ページを追加
    while len(pages) % 4 != 0:
        blank = PageObject.create_blank_page(
            width=pages[0].mediabox.width,
            height=pages[0].mediabox.height,
        )
        pages.append(blank)

    a4_width = float(pages[0].mediabox.width)
    a4_height = float(pages[0].mediabox.height)

    # A3横（A4を2ページ並べる）
    a3_width = a4_width * 2
    a3_height = a4_height

    total = len(pages)

    for i in range(total // 4):
        left_index_front = total - 1 - 2 * i
        right_index_front = 2 * i

        left_index_back = 2 * i + 1
        right_index_back = total - 2 - 2 * i

        # 表面
        front = PageObject.create_blank_page(
            width=a3_width,
            height=a3_height,
        )
        front.merge_transformed_page(
            pages[left_index_front],
            Transformation().translate(tx=0, ty=0),
        )
        front.merge_transformed_page(
            pages[right_index_front],
            Transformation().translate(tx=a4_width, ty=0),
        )
        writer.add_page(front)

        # 裏面
        back = PageObject.create_blank_page(
            width=a3_width,
            height=a3_height,
        )
        back.merge_transformed_page(
            pages[left_index_back],
            Transformation().translate(tx=0, ty=0),
        )
        back.merge_transformed_page(
            pages[right_index_back],
            Transformation().translate(tx=a4_width, ty=0),
        )
        writer.add_page(back)

    with output_path.open("wb") as f:
        writer.write(f)

    print(f"入力ページ数: {original_count}")
    print(f"面付け後ページ数: {len(writer.pages)} (A3ページ)")
    print(f"出力ファイル: {output_path}")

    return output_path
