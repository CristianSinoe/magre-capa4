import sys
import platform
import subprocess
from pathlib import Path

def render_midi_to_wav(
    midi_path: Path, 
    soundfont_path: Path, 
    output_wav_path: Path,
    sample_rate: int = 44100
) -> None:
    """
    Convierte un archivo MIDI a WAV utilizando el ejecutable de FluidSynth vía subprocess.
    """
    if not midi_path.exists():
        raise FileNotFoundError(f"Error: No se encontró el archivo MIDI en '{midi_path}'")
    if not soundfont_path.exists():
        raise FileNotFoundError(f"Error: No se encontró el SoundFont en '{soundfont_path}'")

    output_wav_path.parent.mkdir(parents=True, exist_ok=True)

    print("==================================================")
    print("       MAG-RE Capa 4 — Registro de Renderizado    ")
    print("==================================================")
    print(f"• Renderer:          FluidSynth (CLI Directo)")
    print(f"• SoundFont (.sf2):  {soundfont_path.name}")
    print(f"• Sample Rate:       {sample_rate} Hz")
    print(f"• Canales:           2 (Estéreo / Stereo PCM)")
    print(f"• Bit Depth:         16-bit PCM (Estándar CD/WAV)")
    print(f"• Versión Python:    {platform.python_version()}")
    print("==================================================")

    # Comando CLI oficial de FluidSynth para renderizado fast-render a archivo WAV
    cmd = [
        "fluidsynth",
        "-ni",                          # Sin interfaz interactiva
        "-F", str(output_wav_path.resolve()), # Archivo WAV de salida
        "-r", str(sample_rate),          # Sample Rate (44100 Hz)
        str(soundfont_path.resolve()),   # Banco de sonidos .sf2
        str(midi_path.resolve())         # Entrada MIDI
    ]

    print(f"[*] Iniciando renderizado de '{midi_path.name}' a WAV...")
    
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"FluidSynth error ({result.returncode}):\n{result.stderr}")

    if output_wav_path.exists():
        size_mb = output_wav_path.stat().st_size / (1024 * 1024)
        print(f"[✓] Renderizado completado con éxito.")
        print(f"[✓] Archivo generado: {output_wav_path.resolve()}")
        print(f"[✓] Tamaño del WAV: {size_mb:.2f} MB")
    else:
        raise RuntimeError("El proceso terminó pero el archivo WAV no fue creado.")

if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent.parent

    MIDI_INPUT = BASE_DIR / "data" / "input_sample.mid"
    SOUNDFONT_INPUT = BASE_DIR / "static" / "soundfont.sf2"
    WAV_OUTPUT = BASE_DIR / "outputs" / "rendered_audio.wav"

    try:
        render_midi_to_wav(
            midi_path=MIDI_INPUT,
            soundfont_path=SOUNDFONT_INPUT,
            output_wav_path=WAV_OUTPUT,
            sample_rate=44100
        )
    except Exception as err:
        print(f"[X] Fallo en el renderizado: {err}", file=sys.stderr)
        sys.exit(1)
