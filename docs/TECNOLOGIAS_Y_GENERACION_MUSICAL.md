# Tecnologias y Generacion Musical

## Que tecnologias se estan usando y como?

El prototipo usa un stack local de Python para backend y sintesis, con una
interfaz web ligera:

- **Python 3.11+**: lenguaje principal del backend y motor musical.
- **FastAPI**: expone la interfaz y API (`/api/generate`, sesiones y archivos WAV).
- **Pydantic**: valida que los estados afectivos esten entre `0.0` y `1.0`, y
  que la duracion sea valida.
- **NumPy**: construye las senales de audio y mezcla las capas musicales.
- **SciPy**: escribe los archivos WAV a `44 100 Hz`.
- **Uvicorn**: servidor local que inicia la aplicacion con `python run.py`.
- **SQLite**: guarda sesiones, estados de entrada, parametros crudos y seguros,
  acciones de seguridad y ruta del WAV.
- **HTML, CSS y JavaScript puro**: formulario web, llamada `fetch` a la API,
  reproductor y descarga del audio.
- **Pytest**: pruebas unitarias del controlador, limites de seguridad y
  generacion WAV.
- **PlantUML**: diagramas `.puml` para documentar arquitectura, secuencia,
  sintesis y trazabilidad.

No usa servicios externos, modelos de IA entrenados, frameworks frontend,
autenticacion, nube ni MIDI. La generacion musical es algoritmica: reglas de
Python transforman los estados afectivos en parametros y el motor sintetiza el
audio directamente.

## Cuales son las reglas para hacer audio?

Las reglas actuales estan en dos etapas: primero se calculan parametros
musicales y despues se sintetiza el WAV.

### Reglas afectivo-musicales

- Si el `arousal` objetivo baja, baja el BPM, la densidad de notas y el volumen.
- Si el `arousal` objetivo sube, suben el BPM y la actividad melodica.
- `valence` alta selecciona `major` o `lydian`; baja favorece `minor` o `dorian`.
- `stress` alto reduce volumen, brillo, BPM y complejidad ritmica cuando se
  busca relajacion.
- `engagement` alto permite mas melodia y variacion ritmica.
- Un objetivo relajado aumenta la intensidad del pad y reduce complejidad
  ritmica.

### Reglas de seguridad

- BPM: `60-130`.
- Volumen: `0.05-0.25`; con estres alto, maximo `0.18`.
- Brillo: `0.10-0.80`; con estres alto, maximo `0.55`.
- Densidad: `0.50-3.00`; con arousal objetivo bajo, maximo `1.5`.
- Con estres alto y objetivo de bajar arousal, BPM maximo `110`.

### Conversion a audio

- Se crea un **pad armonico** usando grados 1, 3 y 5 de la escala elegida.
- Se genera una **melodia** con notas aleatorias dentro de esa escala; BPM,
  densidad y actividad determinan su frecuencia.
- Se anade un **pulso suave** de ruido con decaimiento, condicionado por BPM y
  complejidad ritmica.
- El brillo mezcla onda seno con onda triangular.
- Cada evento usa una envolvente ADSR para evitar cortes bruscos.
- Las tres capas se mezclan, se normalizan, reciben fade-in/fade-out y se
  exportan como WAV mono a `44 100 Hz`.

Estas son reglas heuristicas de ingenieria, no reglas clinicamente validadas.

## Que algoritmos se usan para hacer la musica?

Se usan algoritmos de sintesis y composicion algoritmica simples, no un modelo
de IA entrenado:

- **Mapeo determinista por reglas**: formulas convierten `arousal`, `valence`,
  `stress` y `engagement` en BPM, modo, densidad, brillo, volumen y actividad
  musical.
- **Seleccion de escala**: elige `major`, `minor`, `dorian` o `lydian` segun la
  valence objetivo.
- **Generacion armonica**: crea un pad con acordes formados por los grados 1, 3
  y 5 de la escala, rotados por segmentos.
- **Osciladores aditivos**: mezcla una onda seno y una onda triangular; el
  parametro `brightness` controla la proporcion.
- **Melodia estocastica restringida**: selecciona notas aleatorias dentro de la
  escala. La semilla opcional permite repetir la misma secuencia.
- **Pulso percusivo probabilistico**: crea eventos de ruido con decaimiento en
  cada beat, con probabilidad dependiente de la complejidad ritmica.
- **Envolvente ADSR**: aplica ataque, caida, sostenimiento y liberacion para
  suavizar cada nota o acorde.
- **Normalizacion y fades**: ajusta el pico de amplitud, aplica el volumen
  seguro y hace fade-in/fade-out de hasta un segundo.

En resumen: es composicion algoritmica basada en reglas mas sintesis digital
directa de audio.
