import numpy as np
import soundfile as sf
import librosa

# 1. Generamos un archivo WAV de prueba
print("Generando audio sintético...")
sr_generado = 44100
t = np.linspace(0, 3.0, int(sr_generado * 3.0), endpoint=False)
tone = 0.3 * np.sin(2 * np.pi * 440 * t)
sf.write("test_tone.wav", tone, sr_generado)

# 2. Lo cargamos con librosa para cumplir la meta del día
print("Cargando archivo con librosa...")
y, sr_leido = librosa.load("test_tone.wav", sr=None, mono=True)
duracion = librosa.get_duration(y=y, sr=sr_leido)

print("-" * 25)
print(f"Archivo:     test_tone.wav")
print(f"Sample rate: {sr_leido} Hz")
print(f"Muestras:    {len(y)}")
print(f"Duración:    {duracion:.3f} s")
print("-" * 25)
