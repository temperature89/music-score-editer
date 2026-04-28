from pypdf import PdfReader, PdfWriter, PageObject, Transformation
from pathlib import Path

# 入力PDFを読み込む
def split_a3_to_a4(input_pdf_path, output_pdf_path):
    input = Path(input_pdf_path)
    reader = PdfReader(input)
    writer = PdfWriter()

    for page in reader.pages:
        # 元ページのサイズを取得
        width = float(page.mediabox.width)
        height = float(page.mediabox.height)

        # 左半分のページを作成
        left_page = PageObject.create_blank_page(
            width=width / 2,
            height=height
        )
        left_page.merge_page(page)

        # 右半分のページを作成
        right_page = PageObject.create_blank_page(
            width=width / 2,
            height=height
        )
        right_page.merge_transformed_page(
            page,
            Transformation().translate(-width / 2, 0)
        )

        # 出力PDFに追加
        writer.add_page(left_page)
        writer.add_page(right_page)

    # 保存
    output = Path(output_pdf_path)
    with open(output, "wb") as f:
        writer.write(f)

    print("A3 PDF を A4 2枚に分割しました。")