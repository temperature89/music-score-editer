# import typer
# from pathlib import Path
# import split_by_n

# app = typer.Typer()

# @app.command()
# def merge():
#     print("PDFを結合します")

# @app.command()
# def split(
#     input_file: Path,
#     pages_per_file: int = typer.Option(
#         1,
#         "--pages-per-file",
#         "-n",
#         help="1つの出力PDFに含めるページ数"
#     ),
# ):
#     split_by_n.split_by_n(input_file, pages_per_file)

# if __name__ == "__main__":
#     app()

# if __name__ == "__main__":
#     app()

from music_score_editor.cli import app

if __name__ == "__main__":
    app()