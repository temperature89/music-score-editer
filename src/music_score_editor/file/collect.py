from pathlib import Path
import shutil


def collect_pdfs(source: Path, destination: Path):
    """指定したディレクトリ内のPDFファイルをすべて別のディレクトリにコピーする。"""
    source = Path(source)
    destination = Path(destination)

    if not source.exists() or not source.is_dir():
        raise FileNotFoundError(f"Source directory not found: {source}")

    destination.mkdir(parents=True, exist_ok=True)

    for pdf_file in source.rglob("*.pdf"):
        if pdf_file.is_file():
            target = destination / pdf_file.name
            shutil.copy2(pdf_file, target)