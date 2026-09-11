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