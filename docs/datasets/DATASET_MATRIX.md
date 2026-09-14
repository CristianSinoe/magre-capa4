# Matriz Comparativa de Datasets — Proyecto MAG-RE (Capa 4)

Documento de evaluación de recursos de audio, MIDI y anotaciones emocionales para la selección del baseline del Piloto P0.

| Dataset | Tipo de datos | MIDI | Audio | Etiquetas afectivas | Señales fisiológicas | Licencia | Disponibilidad | Utilidad para P0 |
|---|---|---|---|---|---|---|---|---|
| **EMOPIA** | Simbólico / Audio | Sí (1,087 clips) | Sí (WAV / YouTube IDs) | Sí (4 cuadrantes VA: Q1–Q4) | No | CC BY-NC-SA 4.0 | Abierta (Zenodo / GitHub) | **Alta** (Dataset primario seleccionado) |
| **ZBra-music** | Audio / Metadatos | No / Por verificar | Sí (Música popular brasileña) | Sí (Valence / Arousal continuo) | No | Académica (Por verificar) | Bajo solicitud / Repositorio | **Baja** (Ausencia de pistas MIDI estandarizadas) |
| **MCUD 1.0** | Multimodal | No | Sí | Sí (Categorías afectivas) | Sí (EEG / ECG) | Restringida | Acceso restringido | **Baja** (Enfoque en respuesta fisiológica, no en síntesis) |
| **Slakh (Slakh2100)** | Simbólico / Audio Multipista | Sí (2,100 canciones) | Sí (Stems audio aislados) | No | No | CC BY 4.0 | Abierta (Zenodo / Sitio oficial) | **Media** (Excelente para audio/renderizado, carece de etiquetas emocionales) |

---

### Fuentes Documentadas y Estado de Registro

* **EMOPIA:** Hung et al. (ISMIR 2021). Referencia primaria para generación de piano simbólico con control emocional.
* **ZBra-music:** Anotaciones continuas de emoción en audio. *Campos de formato MIDI y licencia exacta pendientes de validación por el equipo.*
* **MCUD 1.0:** Dataset enfocado en computación afectiva fisiológica. *Descartado para la fase de generación simbólica P0.*
* **Slakh:** Manilow et al. (WASPAA 2019). Estándar multipista sintetizado. *Útil como recurso secundario de renderizado.*
