from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader

from music_score_editor.file.instruments import (
    build_score_filename,
    detect_instrument,
    detect_title,
)


def _iter_input_pdfs(input_path: Path) -> list[Path]:
    if input_path.is_dir():
        return sorted(
            p for p in input_path.iterdir() if p.is_file() and p.suffix.lower() == ".pdf"
        )
    return [input_path]


def _extract_text_layer(pdf_path: Path) -> str:
    reader = PdfReader(pdf_path)
    if not reader.pages:
        return ""
    return reader.pages[0].extract_text() or ""


def _ocr_header(pdf_path: Path, header_fraction: float = 0.28) -> str:
    import pypdfium2 as pdfium
    import pytesseract

    pdf = pdfium.PdfDocument(str(pdf_path))
    try:
        page = pdf[0]
        image = page.render(scale=2.5).to_pil()
    finally:
        pdf.close()

    width, height = image.size
    header = image.crop((0, 0, width, max(1, int(height * header_fraction))))

    try:
        return pytesseract.image_to_string(header, lang="jpn+eng")
    except pytesseract.TesseractError:
        return pytesseract.image_to_string(header, lang="eng")


def collect_header_text(pdf_path: Path) -> str:
    """1ページ目の文字レイヤーと、スキャン用のヘッダーOCR結果を合わせる。"""
    chunks = [_extract_text_layer(pdf_path)]
    try:
        chunks.append(_ocr_header(pdf_path))
    except Exception as exc:
        print(f"OCRをスキップしました ({pdf_path.name}): {exc}")
    return "\n".join(chunk for chunk in chunks if chunk.strip())


def infer_label(text: str, title_override: str | None = None) -> tuple[str, str] | None:
    instrument = detect_instrument(text)
    title = detect_title(text, title_override)
    if not instrument or not title:
        return None
    return title, instrument


def _unique_path(path: Path, reserved: set[Path] | None = None) -> Path:
    reserved = reserved or set()
    candidate = path
    stem = path.stem
    suffix = path.suffix
    index = 2
    while candidate.exists() or candidate.resolve() in reserved:
        candidate = path.with_name(f"{stem}-{index}{suffix}")
        index += 1
    return candidate


def label_pdfs(
    source: str | Path,
    title: str | None = None,
    destination: str | Path | None = None,
    dry_run: bool = False,
    text_reader=collect_header_text,
) -> list[tuple[Path, Path]]:
    """楽譜ヘッダーから曲名と楽器略称を推定し、<曲名>_<略称>.pdf にリネームする。"""
    source_path = Path(source)
    if not source_path.exists():
        raise FileNotFoundError(f"ファイルが見つかりません: {source}")

    pdfs = _iter_input_pdfs(source_path)
    if not pdfs:
        raise FileNotFoundError(f"PDFファイルが見つかりません: {source}")

    dest_dir: Path | None = None
    if destination is not None:
        dest_dir = Path(destination)
        if not dry_run:
            dest_dir.mkdir(parents=True, exist_ok=True)

    planned: list[tuple[Path, Path]] = []
    reserved: set[Path] = set()
    for pdf_path in pdfs:
        text = text_reader(pdf_path)
        label = infer_label(text, title)
        if label is None:
            print(f"推定できませんでした: {pdf_path.name}")
            continue
        filename = build_score_filename(*label)
        target_dir = dest_dir if dest_dir is not None else pdf_path.parent
        target = _unique_path(target_dir / filename, reserved)
        reserved.add(target.resolve())
        planned.append((pdf_path, target))
        action = "提案" if dry_run else "リネーム"
        print(f"{action}: {pdf_path.name} → {target.name}")

    if dry_run:
        return planned

    # 衝突回避のため一時名を経由する
    temps: list[tuple[Path, Path]] = []
    for source_pdf, target in planned:
        if source_pdf.resolve() == target.resolve():
            temps.append((source_pdf, target))
            continue
        temp = source_pdf.with_name(f".__msc_label_tmp__{source_pdf.name}")
        source_pdf.rename(temp)
        temps.append((temp, target))

    renamed: list[tuple[Path, Path]] = []
    for temp, target in temps:
        if temp.resolve() != target.resolve():
            target.parent.mkdir(parents=True, exist_ok=True)
            temp.rename(target)
        renamed.append((temp, target))
    return planned
