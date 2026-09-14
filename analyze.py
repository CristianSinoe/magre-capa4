import sys
import librosa
import numpy as np

def analizar_audio(ruta_archivo):
    print(f"Iniciando análisis de: {ruta_archivo}")
    
    # Cargar el archivo de audio
    y, sr = librosa.load(ruta_archivo, sr=None, mono=True)
    
    # 1. Duración
    duracion = librosa.get_duration(y=y, sr=sr)
    
    # 2. RMS (Potencia promedio) convertido a dBFS
    rms_amplitud = np.mean(librosa.feature.rms(y=y))
    # Evitamos logaritmo de 0 asignando un piso de -100 dBFS
    rms_dbfs = 20 * np.log10(rms_amplitud) if rms_amplitud > 0 else -100
    
    # 3. Peak Amplitude (Pico máximo) convertido a dBFS
    pico_amplitud = np.max(np.abs(y))
    pico_dbfs = 20 * np.log10(pico_amplitud) if pico_amplitud > 0 else -100
    
    # 4. Spectral Centroid (Brillo) promedio en Hz
    centroide = librosa.feature.spectral_centroid(y=y, sr=sr)
    centroide_promedio = np.mean(centroide)
    
    # Salida clara requerida por el profesor
    print("\n--- Resultados ---")
    print(f"Duración:            {duracion:.3f} s")
    print(f"RMS:                 {rms_dbfs:.2f} dBFS")
    print(f"Peak Amplitude:      {pico_dbfs:.2f} dBFS")
    print(f"Spectral Centroid:   {centroide_promedio:.2f} Hz")
    print("------------------\n")

if __name__ == "__main__":
    # Instrucciones básicas si el usuario olvida el archivo
    if len(sys.argv) < 2:
        print("Error: Falta el archivo de audio.")
        print("Uso: python analyze.py <archivo.wav>")
        sys.exit(1)
        
    archivo_entrada = sys.argv[1]
    analizar_audio(archivo_entrada)
