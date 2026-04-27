import typer
from pathlib import Path
from music_score_editor.pdf.split import split_by_n
from music_score_editor.file.make_dir import make_dir

app = typer.Typer()

@app.command()
def split(
    file: Path,
    n: int = typer.Option(1, "--n", "-n", help="1つの出力PDFに含めるページ数")
):
    split_by_n(file, n)

@app.command()
def merge():
    """PDFを結合します"""
    print("PDFを結合します")
    
@app.command()
def make(
    file: Path = typer.Option("music_scores", "--name", "-n", help="楽譜配布用のディレクトリを作成")
):
    make_dir(file)

if __name__ == "__main__":
    app()