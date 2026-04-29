# music-score-editor

PDF楽譜を編集するためのCLIツールです。

## インストール

```bash
pip install -e .
```

## 前提ライブラリ

```bash
pip install pypdf PyPDF2
```

## コマンド一覧

### split

PDFを指定したページ数ごとに分割します。

```bash
msc split <file> --n <1つの出力PDFに含めるページ数>
```

**例:**
```bash
msc split input.pdf --n 2
```

### merge

複数のPDFファイルを1つのPDFに結合します。

```bash
msc merge <file1> <file2> ...
```

**例:**
```bash
msc merge file1.pdf file2.pdf file3.pdf
```

### make

楽譜用のフォルダ構造を作成します。

```bash
msc make --name <ディレクトリ名> --subdir <最下層のディレクトリ名>
```

**例:**
```bash
msc make --name "定期演奏会" --subdir "01_Picc" "02_Cl" "03_Sax"
```

### distribute

ファイルを複数のディレクトリにコピーします。

```bash
msc distribute <source> --destinations <destination1> <destination2> ...
```

**例:**
```bash
msc distribute score.pdf --destinations dir1 dir2 dir3
```

### collect

指定フォルダ内のPDFを収集して1つのフォルダにまとめます。

```bash
msc collect <source> --destination <出力先>
```

**例:**
```bash
msc collect 定期演奏会 --destination outputs
```

### resize

PDFのサイズを変更します（A3 ↔ A4）。

```bash
msc resize <source> <a3|a4> --destination <出力先>
```

**例:**
```bash
# A4 PDFをA3サイズに結合
msc resize input.pdf a3 --destination output.pdf

# A3 PDFをA4サイズに分割
msc resize input.pdf a4 --destination output.pdf
```

### extract

PDFから指定した範囲のページを抽出します。

```bash
msc extract <input_pdf> <start_page> <end_page> --name <出力先>
```

**例:**
```bash
msc extract input.pdf 1 10 --name extracted.pdf
```

### remove

PDFから指定したページを削除します。

```bash
msc remove <input_pdf> <pages_to_remove> --name <出力先>
```

**例:**
```bash
msc remove input.pdf 1 3 5 --name output.pdf
```
