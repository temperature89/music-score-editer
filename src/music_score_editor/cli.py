import typer
from pathlib import Path
from music_score_editor.pdf.split import split_by_n
from music_score_editor.file.make_dir import make_dir
from music_score_editor.pdf.merge import merge_pdfs
from music_score_editor.file.distribute import distribute_file
from music_score_editor.file.collect import collect_pdfs
from music_score_editor.pdf.split_a3_to_a4 import split_a3_to_a4
from music_score_editor.pdf.combine_a4_to_a3 import combine_a4_to_a3
from music_score_editor.pdf.extract import extract_pages
from music_score_editor.pdf.remove import remove_pages
from music_score_editor.pdf.make_booklet import impose_booklet
from music_score_editor.pdf.split_booklet import booklet_a3_to_a4
from music_score_editor.pdf.fix_a4_to_a3 import resize_pdf
from music_score_editor.pdf.rotate import rotate_pdf

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
        
@app.command()
def collect(
    source: Path,
    destination: Path = typer.Option("outputs", "--destination", "-d", help="収集したファイルのパス")
):
    collect_pdfs(source, destination)

@app.command()
def resize(
    source: Path,
    size: str,
    destination: Path | None = typer.Option(
        None,
        "--destination",
        "-d",
        help="出力先ファイル"
    )
):
    # -d が指定されていない場合
    if destination is None:
        destination = source.with_name(f"{source.stem}_resized.pdf")

    # ディレクトリが指定された場合
    elif destination.is_dir() or destination.suffix == "":
        destination.mkdir(parents=True, exist_ok=True)
        destination = destination / f"{source.stem}_resized.pdf"

    if size.lower() == "a3":
        combine_a4_to_a3(source, destination)
    elif size.lower() == "a4":
        split_a3_to_a4(source, destination)
    else:
        raise typer.BadParameter("size は 'a3' または 'a4' を指定してください。")
    
@app.command()
def extract(
    input_pdf: Path, 
    start_page: int, 
    end_page: int, 
    output_pdf: Path | None = typer.Option(
        None,
        "--name",
        "-n", 
        help="出力先ファイル"
        )
):
    if output_pdf == None:
        output_pdf = input_pdf.with_name(f"{input_pdf.stem}_extracted.pdf")
    extract_pages(input_pdf, start_page, end_page, output_pdf)

@app.command()
def remove(
    input_pdf: Path, 
    pages_to_remove: list[int],
    output_pdf: Path | None = typer.Option(
        None,
        "--name",
        "-n", 
        help="出力先ファイル"
        )
):
    if output_pdf == None:
        output_pdf = input_pdf.with_name(f"{input_pdf.stem}_removed.pdf")
    remove_pages(input_pdf, pages_to_remove, output_pdf)

@app.command()
def booklet(
    source: Path,
    destination: Path | None = typer.Option(
        None,
        "--destination",
        "-d",
        help="出力先ファイル"
    )
):
    impose_booklet(source, destination)
    
@app.command()
def unbooklet(
    source: Path,
    destination: Path | None = typer.Option(
        None,
        "--destination",
        "-d",
        help="出力先ファイル"
    )
):
    booklet_a3_to_a4(source, destination)
    
@app.command()
def fixsize(
    source: Path,
    paper_size: str,
    destination: Path | None = typer.Option(
        None,
        "--destination",
        "-d",
        help="出力先ファイル"
    )
):
    resize_pdf(source, destination, paper_size)
    
@app.command()
def rotate(
    source: Path,
    angle: int,
    destination: Path | None = typer.Option(
        None,
        "--destination",
        "-d",
        help="出力先ファイル"
    )
):
    rotate_pdf(source, angle, destination)

if __name__ == "__main__":
    app()