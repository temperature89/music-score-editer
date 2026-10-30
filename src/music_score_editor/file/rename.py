from pathlib import Path


def rename_pdfs(directory: Path | str, filename: str) -> list[Path]:
    """指定ディレクトリ内のPDFを <filename>_<通し番号>.pdf にリネームする。"""
    directory = Path(directory)

    if not directory.exists() or not directory.is_dir():
        raise FileNotFoundError(f"Directory not found: {directory}")

    base_name = filename[:-4] if filename.lower().endswith(".pdf") else filename
    if not base_name:
        raise ValueError("filename must not be empty")

    pdf_files = sorted(p for p in directory.rglob("*.pdf") if p.is_file())
    if not pdf_files:
        return []

    # 衝突回避のため一時名へ移してから最終名へリネームする
    temps: list[tuple[Path, Path]] = []
    for i, pdf in enumerate(pdf_files, start=1):
        temp = pdf.with_name(f".__msc_rename_tmp_{i}__{pdf.name}")
        pdf.rename(temp)
        temps.append((temp, pdf.parent / f"{base_name}_{i}.pdf"))

    renamed: list[Path] = []
    for temp, final in temps:
        temp.rename(final)
        renamed.append(final)

    return renamed
