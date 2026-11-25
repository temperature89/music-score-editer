from __future__ import annotations

import re

PART_TO_FOLDER = {
    "Picc": "01_Picc_Fl_Ob_Fg",
    "Fl": "01_Picc_Fl_Ob_Fg",
    "Ob": "01_Picc_Fl_Ob_Fg",
    "Fg": "01_Picc_Fl_Ob_Fg",
    "Cl": "02_Cl",
    "Sax": "03_Sax",
    "Tp": "04_Tp",
    "Hr": "05_Hr",
    "Tb": "06_Tb",
    "Euph": "07_Bass",
    "Tub": "07_Bass",
    "Perc": "08_Perc",
    "Pf": "09_Pf_Gt_Harp_etc",
    "Gt": "09_Pf_Gt_Harp_etc",
    "Harp": "09_Pf_Gt_Harp_etc",
    "score": "10_スコア",
}

# 長い表記を先に当て、Bass Clarinet を Cl と誤認しないようにする。
_INSTRUMENT_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("BCl", re.compile(r"bass\s*clarinets?|バスクラリネット|バスクラ", re.I)),
    ("ASax", re.compile(r"alto\s*sax(ophone)?s?|アルト\s*サックス|a\.?\s*sax", re.I)),
    ("TSax", re.compile(r"tenor\s*sax(ophone)?s?|テナー\s*サックス|t\.?\s*sax", re.I)),
    ("BSax", re.compile(r"baritone\s*sax(ophone)?s?|バリトン\s*サックス|b\.?\s*sax", re.I)),
    ("Euph", re.compile(r"euphoniums?|ユーフォニウム|ユーフォ|euph", re.I)),
    ("Picc", re.compile(r"piccolos?|ピッコロ|picc", re.I)),
    ("Harp", re.compile(r"harps?|ハープ", re.I)),
    ("Perc", re.compile(r"percussions?|timpan[iy]|snare|cymbals?|打楽器|パーカッション|ティンパニ|ドラム", re.I)),
    ("Sax", re.compile(r"saxophones?|サックス|\bsax\b", re.I)),
    ("score", re.compile(r"full\s*score|conductor|スコア|指揮者|\bscore\b", re.I)),
    ("Cl", re.compile(r"clarinets?|クラリネット|\bcl\b|\bcl\.", re.I)),
    ("Fl", re.compile(r"flutes?|フルート|\bfl\b|\bfl\.", re.I)),
    ("Ob", re.compile(r"oboes?|オーボエ|\bob\b|\bob\.", re.I)),
    ("Fg", re.compile(r"bassoons?|fagott[oi]?|ファゴット|バスーン|\bfg\b|\bbsn\b", re.I)),
    ("Tp", re.compile(r"trumpets?|cornets?|トランペット|コルネット|\btp\b|\btpt\b|\btp\.", re.I)),
    ("Hr", re.compile(r"horns?|ホルン|\bhr\b|\bhn\b", re.I)),
    ("Tb", re.compile(r"trombones?|トロンボーン|\btb\b|\btbn\b", re.I)),
    ("Tub", re.compile(r"tubas?|チューバ|テューバ|\btub\b", re.I)),
    ("Pf", re.compile(r"pianos?|ピアノ|\bpf\b|\bpno\b", re.I)),
    ("Gt", re.compile(r"guitars?|ギター|\bgt\b", re.I)),
]

_PART_NUMBER = [
    (re.compile(r"\b1st\b|first|第\s*1|\bi\b", re.I), "1"),
    (re.compile(r"\b2nd\b|second|第\s*2|\bii\b", re.I), "2"),
    (re.compile(r"\b3rd\b|third|第\s*3|\biii\b", re.I), "3"),
    (re.compile(r"\b4th\b|fourth|第\s*4|\biv\b", re.I), "4"),
    (re.compile(r"(?<![0-9])1(?![0-9])"), "1"),
    (re.compile(r"(?<![0-9])2(?![0-9])"), "2"),
    (re.compile(r"(?<![0-9])3(?![0-9])"), "3"),
    (re.compile(r"(?<![0-9])4(?![0-9])"), "4"),
]

_NOISE_LINE = re.compile(
    r"^(allegro|andante|moderato|maestoso|page|p\.?|pp|ff|mf|mp|copyright|©|\d+)$",
    re.I,
)

# パート番号を付けない略称
_NO_PART_NUMBER = {"BCl", "Euph", "Picc", "Harp", "Perc", "score", "Tub", "Pf", "Gt"}


def match_part_folder(instrument_token: str) -> str | None:
    """distribute 用。略称トークンからフォルダ名を返す。長いキーを優先する。"""
    for key in sorted(PART_TO_FOLDER, key=len, reverse=True):
        if key in instrument_token:
            return PART_TO_FOLDER[key]
    return None


def sanitize_title(title: str) -> str:
    cleaned = title.strip()
    cleaned = re.sub(r'[\\/:*?"<>|]', "", cleaned)
    cleaned = cleaned.replace("_", "-")
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def detect_instrument(text: str) -> str | None:
    """OCR/抽出テキストから distribute 互換の楽器略称を返す。"""
    if not text:
        return None

    for abbr, pattern in _INSTRUMENT_PATTERNS:
        match = pattern.search(text)
        if not match:
            continue
        if abbr in _NO_PART_NUMBER:
            return abbr
        number = _detect_part_number(text)
        return f"{abbr}{number}" if number else abbr
    return None


def detect_title(text: str, title_override: str | None = None) -> str | None:
    if title_override:
        sanitized = sanitize_title(title_override)
        return sanitized or None

    lines = [re.sub(r"\s+", " ", line).strip() for line in text.splitlines()]
    candidates: list[str] = []
    for line in lines:
        if len(line) < 2 or _NOISE_LINE.match(line):
            continue
        if detect_instrument(line):
            continue
        candidates.append(line)

    if not candidates:
        return None

    candidates.sort(key=lambda line: (len(re.findall(r"[一-龯ぁ-んァ-ン]", line)), len(line)), reverse=True)
    return sanitize_title(candidates[0]) or None


def build_score_filename(title: str, instrument: str) -> str:
    return f"{sanitize_title(title)}_{instrument}.pdf"


def _detect_part_number(text: str) -> str | None:
    window = text[:200]
    for pattern, number in _PART_NUMBER:
        if pattern.search(window):
            return number
    return None
