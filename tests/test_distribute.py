from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from music_score_editor.file.distribute import distribute_file


def test_distribute_preserves_underscores_in_title(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    pdf = source / "Song_Title_Fl1.pdf"
    pdf.write_bytes(b"pdf")

    destination = tmp_path / "destination"
    distribute_file(str(source), str(destination))

    copied_pdf = (
        destination
        / "01_Picc_Fl_Ob_Fg"
        / "Song_Title"
        / "Song_Title_Fl1.pdf"
    )
    assert copied_pdf.read_bytes() == b"pdf"
