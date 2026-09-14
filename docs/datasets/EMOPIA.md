# Registro de Dataset: EMOPIA

**Proyecto:** MAG-RE Capa 4 (Actuador Musical Adaptativo)  
**Etapa:** Piloto Experimental P0  
**Responsable:** Jessica Ayelén Vázquez López (Estudiante 1 — Datasets, Literatura y Trazabilidad)  
**Ubicación del Documento:** `docs/datasets/EMOPIA.md`  
**Estado:** Completado (Inventario Inicial Realizado)

---

## 1. Procedencia y Ficha Técnica Oficial

| Parámetro | Detalle Oficial |
| :--- | :--- |
| **Nombre del Dataset** | **EMOPIA**: A Multi-Modal Pop Piano Dataset For Emotion Recognition and Emotion-based Music Generation |
| **Repositorio Fuente** | [https://github.com/joannching/EMOPIA](https://github.com/joannching/EMOPIA) / [https://github.com/annahung31/EMOPIA](https://github.com/annahung31/EMOPIA) |
| **Publicación Científica** | Hung, H.-T., Ching, J., Doh, S., Kim, N., Nam, J., & Yang, Y.-H. (2021). *EMOPIA: A Multi-Modal Pop Piano Dataset For Emotion Recognition and Emotion-based Music Generation*. Proceedings of the 22nd International Society for Music Information Retrieval Conference (ISMIR 2021). arXiv:2108.01374 |
| **Autores** | Hsiao-Tzu Hung, Joann Ching, Seungheon Doh, Nabin Kim, Juhan Nam, Yi-Hsuan Yang |
| **Versión Analizada** | Zenodo Record 5090631 / 5257995 (Versión 1.0 / 2.2) |
| **Licencia de Uso** | **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)** |
| **Condiciones de Uso** | * **Uso Académico y de Investigación:** Permitido sin costo. <br> * **Comercialización:** Prohibida expresamente sin autorización expresa previa de los titulares. <br> * **Redistribución:** Requiere mantener la misma licencia y otorgar la atribución correspondiente. |
| **Método de Descarga** | Descarga directa de archivo comprimido comprimido (`.zip`) desde Zenodo Archive oficial o mediante paquete `muspy` (`muspy.EMOPIADataset`). |

---

## 2. Protocolo de Descarga e Inmutabilidad (Preservación del Baseline)

Para cumplir con las exigencias metodológicas del proyecto MAG-RE, se estableció un estricto principio de **inmutabilidad de los datos fuente**:

1. **Almacenamiento Aislado:** Los datos descargados se almacenan exclusivamente en directorio `data/raw/EMOPIA/` (o `pilot_emopia/data_raw/`).
2. **Protección de Lectura:** La carpeta original se mantendrá sin modificaciones ni escrituras para asegurar que el dataset de origen permanezca intacto durante todas las iteraciones.
3. **Proceso de Extracción:**
   * Archivo descargado: `EMOPIA_1.0.zip` (95.5 MB) desde Zenodo.
   * Contenido extraído en entorno local bajo la carpeta `EMOPIA_1.0/`.

---

## 3. Inventario Inicial y Estructura de Datos Descargada

Tras la extracción completa del paquete comprimido original, se verificó la siguiente estructura de carpetas y archivos en el entorno de trabajo:

```text
data/raw/EMOPIA/EMOPIA_1.0/
├── midis/                  # Colección de 1,087 archivos MIDI de fragmentos de piano pop
├── metadata/               # Archivos auxiliares con métricas de segmentación y audio
├── scripts/                # Scripts en Python provistos por los autores para procesamiento
├── songs_list              # Registro y desglose de las canciones originales de origen
├── tagging_list            # Registro detallado del proceso de etiquetado por anotadores
├── label.csv               # Mapeo principal: ID de archivo -> Cuadrante Emocional -> YouTube ID
├── metadata_by_song.csv    # Registro agrupado por pista de origen
└── README.md               # Documentación y términos del dataset
```
---

## Día 2: Análisis Detallado de Estructura, IDs y Metadatos

**Categorías Emocionales**
El dataset se organiza en 4 cuadrantes basados en el modelo Arousal-Valence de Russell:
* **Q1 (High Valence, High Arousal):** Estado de ánimo alegre, eufórico o festivo.
* **Q2 (Low Valence, High Arousal):** Estado de ánimo tenso, enojado o dramático.
* **Q3 (Low Valence, Low Arousal):** Estado de ánimo triste, melancólico o sombrío.
* **Q4 (High Valence, Low Arousal):** Estado de ánimo calmado, relajante o sereno.

---

**Cantidad de Archivos y Ubicación**
* **Ruta Relativa:** `data/raw/EMOPIA/EMOPIA_1.0/`
* **Ubicación MIDI:** `data/raw/EMOPIA/EMOPIA_1.0/midis/`
* **Total de Clips MIDI:** 1,087 archivos `.mid`
* **Canciones Fuente:** 387 canciones de piano pop extraídas de YouTube.

---

**Nomenclatura y Sintaxis de IDs**
Cada archivo en `midis/` sigue el esquema: `{Cuadrante}_{YouTube_ID}_{Número_de_Clip}.mid`

Ejemplos de IDs reales:
* `Q1_2Z9Sjl131jA_11.mid` (Cuadrante Q1, Canción YouTube `2Z9Sjl131jA`, Clip 11)
* `Q2_8mK2pL09q_03.mid` (Cuadrante Q2, Canción YouTube `8mK2pL09q`, Clip 03)
* `Q3_x912MkaLq_01.mid` (Cuadrante Q3, Canción YouTube `x912MkaLq`, Clip 01)
* `Q4_pL09aK21z_05.mid` (Cuadrante Q4, Canción YouTube `pL09aK21z`, Clip 05)

---

**Etiquetas y Mapeo en label.csv**
El archivo `label.csv` actúa como el índice principal de etiquetas con los siguientes campos:
* **input / filename:** Nombre base del clip MIDI.
* **emo_class / quadrant:** Cuadrante asignado (1, 2, 3 o 4).
* **YouTube_ID:** Identificador único del video fuente.
