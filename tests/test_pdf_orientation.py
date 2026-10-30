from pathlib import Path
import sys

import pytest
from pypdf import PdfReader, PdfWriter, PageObject

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from music_score_editor.pdf.combine_a4_to_a3 import combine_a4_to_a3
from music_score_editor.pdf.fix_a4_to_a3 import crop_to_paper
from music_score_editor.pdf.split_a3_to_a4 import split_a3_to_a4


def test_split_and_combine_preserve_rotation(tmp_path):
    input_pdf = tmp_path / "input.pdf"
    split_pdf = tmp_path / "split.pdf"
    combined_pdf = tmp_path / "combined.pdf"

    writer = PdfWriter()
    page = PageObject.create_blank_page(width=842, height=595)
    page.rotate(90)
    writer.add_page(page)

    with input_pdf.open("wb") as f:
        writer.write(f)

    split_a3_to_a4(input_pdf, split_pdf)

    split_reader = PdfReader(split_pdf)
    assert split_reader.pages[0].mediabox.width == pytest.approx(297.5)
    assert split_reader.pages[0].mediabox.height == pytest.approx(842.0)
    assert split_reader.pages[1].mediabox.width == pytest.approx(297.5)
    assert split_reader.pages[1].mediabox.height == pytest.approx(842.0)

    combine_a4_to_a3(split_pdf, combined_pdf)

    combined_reader = PdfReader(combined_pdf)
    assert combined_reader.pages[0].mediabox.width == pytest.approx(595.0)
    assert combined_reader.pages[0].mediabox.height == pytest.approx(842.0)


def test_fixsize_corrects_rotated_page_before_resize(tmp_path):
    input_pdf = tmp_path / "input.pdf"
    output_pdf = tmp_path / "output.pdf"

    writer = PdfWriter()
    page = PageObject.create_blank_page(width=842, height=595)
    page.rotate(90)
    writer.add_page(page)

    with input_pdf.open("wb") as f:
        writer.write(f)

    crop_to_paper(input_pdf, output_pdf, "A4")

    reader = PdfReader(output_pdf)
    page = reader.pages[0]
    assert page.mediabox.width == pytest.approx(595.28)
    assert page.mediabox.height == pytest.approx(841.89)


def test_fixsize_processes_all_pdfs_in_directory(tmp_path):
    input_dir = tmp_path / "inputs"
    output_dir = tmp_path / "outputs"
    input_dir.mkdir()
    output_dir.mkdir()

    for name in ["one.pdf", "two.pdf"]:
        writer = PdfWriter()
        page = PageObject.create_blank_page(width=842, height=595)
        page.rotate(90)
        writer.add_page(page)

        with (input_dir / name).open("wb") as f:
            writer.write(f)

    crop_to_paper(input_dir, output_dir, "A4")

    for name in ["one_A4.pdf", "two_A4.pdf"]:
        output_pdf = output_dir / name
        assert output_pdf.exists()

        reader = PdfReader(output_pdf)
        page = reader.pages[0]
        assert page.mediabox.width == pytest.approx(595.28)
        assert page.mediabox.height == pytest.approx(841.89)
