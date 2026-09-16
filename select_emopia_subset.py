import os
import csv
import random
import shutil

# 1. Parámetros de reproducibilidad
SEED = 42
SAMPLES_PER_QUADRANT = 10

# 2. Rutas del proyecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "data/raw/EMOPIA")
LABEL_CSV = os.path.join(DATASET_DIR, "label.csv")
MIDIS_DIR = os.path.join(DATASET_DIR, "midis")

OUTPUT_DIR = os.path.join(BASE_DIR, "outputs/subset_p0")
PROVENANCE_CSV = os.path.join(BASE_DIR, "docs/datasets/provenance_p0.csv")

def run_selection():
    random.seed(SEED)
    
    if not os.path.exists(LABEL_CSV):
        print(f"Error: No se encontró el archivo {LABEL_CSV}")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(PROVENANCE_CSV), exist_ok=True)

    quadrants = {"1": [], "2": [], "3": [], "4": []}

    # Leer etiquetas usando los nombres reales de columna: ID y 4Q
    with open(LABEL_CSV, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            q = str(row.get("4Q", "")).strip()
            file_id = row.get("ID", "").strip()
            
            if file_id:
                filename = file_id if file_id.endswith(".mid") else f"{file_id}.mid"
                if q in quadrants:
                    quadrants[q].append((filename, file_id))

    selected = []

    # Selección aleatoria determinista por semilla
    for q in ["1", "2", "3", "4"]:
        available = quadrants[q]
        chosen = random.sample(available, min(SAMPLES_PER_QUADRANT, len(available)))
        selected.extend([(q, item[0], item[1]) for item in chosen])

    # Copiado y registro de trazabilidad
    with open(PROVENANCE_CSV, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["sample_id", "quadrant", "original_filename", "youtube_id"])

        for idx, (q, orig_file, file_id) in enumerate(selected, 1):
            src_path = os.path.join(MIDIS_DIR, orig_file)
            dst_path = os.path.join(OUTPUT_DIR, orig_file)
            
            parts = file_id.split('_')
            yt_id = parts[1] if len(parts) >= 2 else "N/A"

            if os.path.exists(src_path):
                shutil.copy2(src_path, dst_path)
            
            writer.writerow([f"P0_{idx:02d}", f"Q{q}", orig_file, yt_id])

    print(f" Muestreo reproducido exitosamente (Semilla={SEED}).")
    print(f" Archivos copiados en: {OUTPUT_DIR}")
    print(f" Registro de trazabilidad: {PROVENANCE_CSV}")

if __name__ == "__main__":
    run_selection()
