from pypdf import PdfWriter
from pathlib import Path

# ファイル一覧を取得,ソート
pdf_files = sorted(Path("../merge").iterdir())

# ライター
writer = PdfWriter()
for pdf in pdf_files:
    writer.append(pdf)
    
writer.write("../merge/merged.pdf")
writer.close()