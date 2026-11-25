from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from music_score_editor.file.instruments import (
    build_score_filename,
    detect_instrument,
    detect_title,
    match_part_folder,
    sanitize_title,
)


def test_detect_common_abbreviations():
    assert detect_instrument("Flute 1") == "Fl1"
    assert detect_instrument("1st Trumpet") == "Tp1"
    assert detect_instrument("Alto Saxophone") == "ASax"
    assert detect_instrument("クラリネット 2") == "Cl2"
    assert detect_instrument("ホルン") == "Hr"
    assert detect_instrument("ピッコロ") == "Picc"
    assert detect_instrument("Score") == "score"


def test_bass_clarinet_is_not_plain_clarinet():
    assert detect_instrument("Bass Clarinet") == "BCl"


def test_filename_matches_distribute_pattern():
    filename = build_score_filename("星条旗", "Fl1")
    assert filename == "星条旗_Fl1.pdf"
    title, inst = filename[:-4].split("_")
    assert match_part_folder(inst) == "01_Picc_Fl_Ob_Fg"
    assert title == "星条旗"


def test_harp_does_not_match_horn_folder():
    assert match_part_folder("Harp") == "09_Pf_Gt_Harp_etc"
    assert match_part_folder("Hr1") == "05_Hr"


def test_title_override_and_sanitize():
    assert sanitize_title("星_条 旗") == "星-条 旗"
    assert detect_title("Flute\nignored", title_override=" 行進曲 ") == "行進曲"


def test_detect_title_skips_instrument_line():
    text = "1st Flute\n星条旗よ永遠なれ\nAllegro"
    assert detect_title(text) == "星条旗よ永遠なれ"
