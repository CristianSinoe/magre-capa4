import sys
import librosa
import numpy as np

def analizar_audio(ruta_archivo, requested_bpm=None):
    print(f"Iniciando análisis de: {ruta_archivo}")
    
    # Carga de la señal de audio
    y, sr = librosa.load(ruta_archivo, sr=None, mono=True)
    
    # 1. Duración temporal
    duracion = librosa.get_duration(y=y, sr=sr)
    
    # 2. RMS (Potencia promedio) a dBFS
    rms_amplitud = np.mean(librosa.feature.rms(y=y))
    rms_dbfs = 20 * np.log10(rms_amplitud) if rms_amplitud > 0 else -100
    
    # 3. Peak Amplitude a dBFS
    pico_amplitud = np.max(np.abs(y))
    pico_dbfs = 20 * np.log10(pico_amplitud) if pico_amplitud > 0 else -100
    
    # 4. Spectral Centroid (Promedio)
    centroide = librosa.feature.spectral_centroid(y=y, sr=sr)
    centroide_promedio = np.mean(centroide)
    
    # 5. BPM Estimado
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    # Soporte para compatibilidad de tipos en versiones de librosa > 0.10
    measured_bpm = float(tempo[0]) if isinstance(tempo, np.ndarray) else float(tempo)
    
    # Salida estándar de resultados
    print("\n--- Resultados ---")
    if requested_bpm:
        print(f"Requested BPM:       {requested_bpm}")
    print(f"Measured BPM:        {measured_bpm:.1f}")
    print(f"Duración:            {duracion:.3f} s")
    print(f"RMS:                 {rms_dbfs:.2f} dBFS")
    print(f"Peak Amplitude:      {pico_dbfs:.2f} dBFS")
    print(f"Spectral Centroid:   {centroide_promedio:.2f} Hz")
    print("------------------\n")

if __name__ == "__main__":
    # Validación de argumentos por interfaz de línea de comandos (CLI)
    if len(sys.argv) < 2:
        print("Error: Argumentos insuficientes.")
        print("Uso: python analyze.py <archivo.wav> [requested_bpm]")
        sys.exit(1)
        
    archivo_entrada = sys.argv[1]
    # Captura del BPM solicitado si se provee en la CLI
    req_bpm = sys.argv[2] if len(sys.argv) > 2 else None
    
    analizar_audio(archivo_entrada, req_bpm)
