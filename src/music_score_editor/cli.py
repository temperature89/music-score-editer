import typer
from pathlib import Path
from music_score_editor.pdf.split import split_by_n
from music_score_editor.file.make_dir import make_dir
from music_score_editor.pdf.merge import merge_pdfs
from music_score_editor.file.distribute import distribute_file

app = typer.Typer()

@app.command()
def split(
    file: Path,
    n: int = typer.Option(1, "--n", "-n", help="1つの出力PDFに含めるページ数")
):
    split_by_n(file, n)

@app.command()
def merge(
    files: list[Path]
):
    merge_pdfs(files)
    
@app.command()
def make(
    base_name: Path = typer.Option("music_scores", "--name", "-n", help="ディレクトリ名"),
    subdir_names: list[Path] = typer.Option([""], "--subdir", "-s", help="最下層のディレクトリ名")
):
    make_dir(base_name, subdir_names)

@app.command()
def distribute(
    source: Path,
    destinations: list[Path]
):
    for d in destinations:
        distribute_file(source, d)

if __name__ == "__main__":
    app()