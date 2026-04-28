from pypdf import PdfReader, PdfWriter, PageObject, Transformation

def combine_a4_to_a3(input_pdf_path, output_pdf_path):
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    # A4の標準サイズ（ポイント単位: 72dpiの場合）
    # A4: 595 x 842 pts
    # A3: 1190 x 842 pts (A4を横に2枚並べたサイズ)
    
    num_pages = len(reader.pages)

    for i in range(0, num_pages, 2):
        # 1枚目のページを取得
        p1 = reader.pages[i]
        width = p1.mediabox.width
        height = p1.mediabox.height

        # 新しいA3横サイズのページを作成 (幅を2倍にする)
        # width * 2 = 1190.0, height = 842.0
        new_page = PageObject.create_blank_page(width=width * 2, height=height)

        # 左側に1枚目を配置
        new_page.merge_page(p1)

        # 2枚目があるか確認
        if i + 1 < num_pages:
            p2 = reader.pages[i + 1]
            # 右側に配置するために、x軸方向にwidth分だけスライドさせる変形を適用
            transformation = Transformation().translate(tx=float(width), ty=0)
            new_page.merge_transformed_page(p2, transformation)

        writer.add_page(new_page)
        
    with open(output_pdf_path, "wb") as f:
        writer.write(f)

    print(f"結合完了: {output_pdf_path}")