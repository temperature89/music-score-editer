from pypdf import PdfReader, PdfWriter, PageObject, Transformation

# 入力PDFを読み込む
reader = PdfReader("output_a3_combined.pdf")
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
with open("output_a4_splited.pdf", "wb") as f:
    writer.write(f)

print("A3 PDF を A4 2枚に分割しました。")