from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pypdf import PdfWriter, PageObject

from music_score_editor.pdf.label import infer_label, label_pdfs


def _touch_pdf(path: Path) -> None:
    writer = PdfWriter()
    writer.add_page(PageObject.create_blank_page(width=595, height=842))
    with path.open("wb") as f:
        writer.write(f)


def test_infer_label_from_header_text():
    text = "The Stars and Stripes Forever\n1st Flute\nMarch"
    assert infer_label(text) == ("The Stars and Stripes Forever", "Fl1")


def test_label_pdfs_renames_directory_with_injected_text(tmp_path):
    input_dir = tmp_path / "scores"
    input_dir.mkdir()
    first = input_dir / "a.pdf"
    second = input_dir / "b.pdf"
    _touch_pdf(first)
    _touch_pdf(second)

    texts = {
        first.resolve(): "1st Flute",
        second.resolve(): "Trumpet 2",
    }

    planned = label_pdfs(
        input_dir,
        title="星条旗",
        text_reader=lambda path: texts[path.resolve()],
    )

    names = {target.name for _, target in planned}
    assert names == {"星条旗_Fl1.pdf", "星条旗_Tp2.pdf"}
    assert (input_dir / "星条旗_Fl1.pdf").exists()
    assert (input_dir / "星条旗_Tp2.pdf").exists()


def test_label_pdfs_dry_run_does_not_rename(tmp_path):
    pdf_path = tmp_path / "part.pdf"
    _touch_pdf(pdf_path)

    planned = label_pdfs(
        pdf_path,
        title="星条旗",
        dry_run=True,
        text_reader=lambda _path: "Clarinet",
    )

    assert planned[0][1].name == "星条旗_Cl.pdf"
    assert pdf_path.exists()
    assert not (tmp_path / "星条旗_Cl.pdf").exists()
