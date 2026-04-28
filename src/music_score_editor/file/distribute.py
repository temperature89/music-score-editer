from pathlib import Path
import shutil

def distribute_file(source: str, destination: str):
    source_root = Path(source)
    target_pdfs = []
    for p in source_root.rglob("*.pdf"):
        target_pdfs.append(p)

    part_to_folder = {
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
        "score": "09_スコア",
    }
    
    destination_root = Path(destination)
    for t in target_pdfs:
        parts = t.name.rstrip(".pdf").split("_")
        if len(parts) >= 2:
            t_title = parts[0]
            t_inst = parts[1]
            
            # キーが楽器名に含まれるかチェック
            matched_folder = None
            for key in part_to_folder:
                if key in t_inst:
                    matched_folder = part_to_folder[key]
                    break
            
            if matched_folder:
                # 曲名ごとのサブディレクトリを作成
                target_dir = destination_root / matched_folder / t_title
                target_dir.mkdir(parents=True, exist_ok=True)
                dest_path = target_dir / t.name
                shutil.copy2(t, dest_path)
                print(f"コピー: {t.name} → {matched_folder}/{t_title}/")
            else:
                # 未対応はdestinationの1つ下に配置
                target_dir = destination_root
                target_dir.mkdir(parents=True, exist_ok=True)
                dest_path = target_dir / t.name
                shutil.copy2(t, dest_path)
                print(f"コピー: {t.name} → {t_title}/")
