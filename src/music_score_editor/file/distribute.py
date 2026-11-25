from pathlib import Path
import shutil

from music_score_editor.file.instruments import match_part_folder


def distribute_file(source: str, destination: str):
    source_root = Path(source)
    target_pdfs = []
    for p in source_root.rglob("*.pdf"):
        target_pdfs.append(p)

    destination_root = Path(destination)
    for t in target_pdfs:
        parts = t.name.rstrip(".pdf").split("_")
        if len(parts) >= 2:
            t_title = parts[0]
            t_inst = parts[1]

            matched_folder = match_part_folder(t_inst)

            if matched_folder:
                target_dir = destination_root / matched_folder / t_title
                target_dir.mkdir(parents=True, exist_ok=True)
                dest_path = target_dir / t.name
                shutil.copy2(t, dest_path)
                print(f"コピー: {t.name} → {matched_folder}/{t_title}/")
            else:
                target_dir = destination_root / Path("09_Pf_Gt_Harp_etc") / t_title
                target_dir.mkdir(parents=True, exist_ok=True)
                dest_path = target_dir / t.name
                shutil.copy2(t, dest_path)
                print(f"コピー: {t.name} → {t_title}/")
