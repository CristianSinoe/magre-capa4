# Definición de Métricas Experimentales (Piloto P0)
**Archivo:** `docs/metrics_definition.md`
**Objetivo:** Establecer las métricas de evaluación independientes para el análisis de archivos WAV generados por el modelo, permitiendo medir la precisión de los parámetros solicitados y detectar acoplamiento (*cross-talk*) entre variables.

---

### 1. BPM Estimado (Tempo)
*   **Qué representa:** La velocidad o pulso de la pieza musical (Beats Per Minute).
*   **Unidad:** BPM.
*   **Herramienta candidata:** `librosa.beat.beat_track` o `Essentia` (RhythmExtractor).
*   **Utilidad experimental:** Permite verificar si una solicitud directa de modificación de tempo en el actuador se refleja con exactitud matemática en el audio renderizado.
*   **Limitaciones conocidas:** El algoritmo puede cometer errores de octava (calcular el doble o la mitad del tempo real, ej. 60 BPM vs 120 BPM) y pierde precisión en piezas ambientales, sin percusión o con métricas altamente sincopadas.

### 2. Loudness (Sonoridad Perceptiva)
*   **Qué representa:** La percepción subjetiva humana de la intensidad acústica o volumen del audio. Considera la sensibilidad del oído a diferentes frecuencias.
*   **Unidad:** LUFS (Loudness Units relative to Full Scale).
*   **Herramienta candidata:** Librería `pyloudnorm` (implementación estándar ITU-R BS.1770-4).
*   **Utilidad experimental:** Fundamental para estudios de modulación de *Arousal* (activación). Permite comprobar si el sistema está logrando mayor intensidad perceptiva o si un cambio en otra variable (ej. densidad) alteró accidentalmente el volumen aparente.
*   **Limitaciones conocidas:** El valor integrado (Integrated LUFS) promedia toda la pista; los picos dinámicos repentinos pueden diluirse en el cálculo total del fragmento.

### 3. RMS (Root Mean Square)
*   **Qué representa:** La potencia promedio de la señal eléctrica/digital del audio en una ventana de tiempo. Es una medida física pura de energía.
*   **Unidad:** dBFS (Decibelios relativos a escala completa).
*   **Herramienta candidata:** `librosa.feature.rms`.
*   **Utilidad experimental:** Sirve como punto de contraste objetivo frente al Loudness perceptivo. Ayuda a auditar la ganancia general de la señal generada.
*   **Limitaciones conocidas:** No toma en cuenta la psicoacústica. Una pista con frecuencias graves muy altas (que el oído humano percibe menos) arrojará un RMS alto, aunque no "suene" tan fuerte.

### 4. Peak Amplitude (Amplitud Pico)
*   **Qué representa:** El valor absoluto de la muestra más alta en la forma de onda digital.
*   **Unidad:** dBFS (True Peak).
*   **Herramienta candidata:** `librosa` (`np.max(np.abs(audio_array))`) o `pyloudnorm` (medición de True Peak).
*   **Utilidad experimental:** Métrica de seguridad y control de calidad. Garantiza que el actuador no esté generando saturación, distorsión o *clipping* digital al modificar otras variables.
*   **Limitaciones conocidas:** No proporciona información sobre la dinámica, la densidad o la energía sostenida de la pista; un solo golpe de platillo dictará el valor máximo de todo el archivo.

### 5. Onset Rate (Densidad Rítmica)
*   **Qué representa:** La frecuencia con la que ocurren eventos musicales nuevos (ataques de notas, golpes de percusión, cambios de acordes) en la pista.
*   **Unidad:** Onsets por segundo (Hz) o conteo total de onsets.
*   **Herramienta candidata:** `librosa.onset.onset_detect`.
*   **Utilidad experimental:** Es clave para evaluar el *cross-talk*. Nos permite responder a la pregunta: ¿Aumentar el tempo de la pista provocó que el modelo también generara más notas o eventos de los requeridos por la velocidad?
*   **Limitaciones conocidas:** Altamente dependiente del ajuste del umbral (*threshold*). Los ataques suaves, instrumentos de cuerda frotada (legato) o texturas *drone* (ambientales) pueden causar falsos negativos en la detección.

### 6. Spectral Centroid (Brillo / Brightness)
*   **Qué representa:** El "centro de masa" del espectro de frecuencias. Indica dónde se concentra la mayor parte de la energía sonora y se correlaciona con la percepción de "brillo" en el sonido.
*   **Unidad:** Hertz (Hz).
*   **Herramienta candidata:** `librosa.feature.spectral_centroid`.
*   **Utilidad experimental:** Como variable experimental secundaria, ayuda a identificar cambios no solicitados en la instrumentación (ej. si al pedir "activación" el modelo añadió sintetizadores agudos en lugar de simplemente subir el tempo o el volumen).
*   **Limitaciones conocidas:** En pistas polifónicas densas (ej. bajo profundo sonando al mismo tiempo que unos *hi-hats* brillantes), el centroide calculará un promedio en las frecuencias medias que no representa a ninguno de los dos instrumentos de manera aislada.
