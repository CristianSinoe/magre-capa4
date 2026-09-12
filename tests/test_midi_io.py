import sys
from pathlib import Path
import pretty_midi

def run_midi_pipeline(input_path: Path, output_path: Path) -> None:
    if not input_path.exists():
        raise FileNotFoundError(f"Error: El archivo de entrada '{input_path}' no existe.")

    print(f"[*] Cargando archivo MIDI: {input_path.name}...")
    midi_data = pretty_midi.PrettyMIDI(str(input_path))

    # Guardar copia exacta sin modificar parámetros
    midi_data.write(str(output_path))
    print(f"[✓] Copia guardada exitosamente en: {output_path.resolve()}")

if __name__ == "__main__":
    # BASE_DIR es la raíz del proyecto (magre-capa4), calculada desde tests/test_midi_io.py
    BASE_DIR = Path(__file__).resolve().parent.parent
    
    # Rutas basadas en la estructura de tu repositorio
    INPUT_MIDI = BASE_DIR / "data" / "input_sample.mid"
    OUTPUT_MIDI = BASE_DIR / "outputs" / "output_sample.mid"

    try:
        run_midi_pipeline(INPUT_MIDI, OUTPUT_MIDI)
    except Exception as e:
        print(f"[X] Error en la ejecución: {e}", file=sys.stderr)
        sys.exit(1)
