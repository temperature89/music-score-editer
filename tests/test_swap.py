from pathlib import Path
import sys

import pytest
from pypdf import PdfReader, PdfWriter, PageObject

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from music_score_editor.pdf.swap import swap_pages


def _write_sized_pages(path: Path, sizes: list[tuple[float, float]]) -> None:
    writer = PdfWriter()
    for width, height in sizes:
        writer.add_page(PageObject.create_blank_page(width=width, height=height))
    with path.open("wb") as f:
        writer.write(f)


def _page_sizes(path: Path) -> list[tuple[float, float]]:
    reader = PdfReader(path)
    return [
        (float(page.mediabox.width), float(page.mediabox.height))
        for page in reader.pages
    ]


def test_swap_two_pages(tmp_path):
    input_pdf = tmp_path / "input.pdf"
    output_pdf = tmp_path / "output.pdf"
    sizes = [(100, 200), (200, 300), (300, 400)]
    _write_sized_pages(input_pdf, sizes)

    saved = swap_pages(input_pdf, [1, 3], output_pdf)

    assert saved == [output_pdf]
    assert _page_sizes(output_pdf) == [(300, 400), (200, 300), (100, 200)]


def test_swap_applies_pairs_in_order(tmp_path):
    input_pdf = tmp_path / "input.pdf"
    output_pdf = tmp_path / "output.pdf"
    sizes = [(100, 100), (200, 200), (300, 300), (400, 400)]
    _write_sized_pages(input_pdf, sizes)

    swap_pages(input_pdf, [1, 4, 2, 3], output_pdf)

    assert _page_sizes(output_pdf) == [
        (400, 400),
        (300, 300),
        (200, 200),
        (100, 100),
    ]


def test_swap_processes_all_pdfs_in_directory(tmp_path):
    input_dir = tmp_path / "inputs"
    output_dir = tmp_path / "outputs"
    input_dir.mkdir()

    for name in ["one.pdf", "two.pdf"]:
        _write_sized_pages(input_dir / name, [(100, 200), (200, 300), (300, 400)])

    saved = swap_pages(input_dir, [1, 2], output_dir)

    assert {path.name for path in saved} == {"one_swapped.pdf", "two_swapped.pdf"}
    for name in ["one_swapped.pdf", "two_swapped.pdf"]:
        output_pdf = output_dir / name
        assert output_pdf.exists()
        assert _page_sizes(output_pdf) == [(200, 300), (100, 200), (300, 400)]


def test_swap_rejects_odd_page_count():
    with pytest.raises(ValueError, match="偶数個"):
        swap_pages("unused.pdf", [1])


def test_swap_rejects_out_of_range_page(tmp_path):
    input_pdf = tmp_path / "input.pdf"
    _write_sized_pages(input_pdf, [(100, 200), (200, 300)])

    with pytest.raises(ValueError, match="無効なページ番号"):
        swap_pages(input_pdf, [1, 5], tmp_path / "output.pdf")
