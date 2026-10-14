# Ejemplo 20 · Gestos con el IMU de la Nano 33 BLE Sense Rev2 (TensorFlow Lite Micro)

```
env:captura  ──► punch.csv / flex.csv ──► Colab (gestos_tinyml_colab.ipynb) ──► model.h ──► env:inferencia
 IMU 119 muestras      CSV por serie          red 714 → 50 → 15 → 2, float32          include/     LED RGB
```

**Placa: Arduino Nano 33 BLE Sense Rev2** (ABX00069; serigrafía inferior «NANO 33 BLE SENSE REV2»), IMU BMI270 + BMM150.
Wokwi no simula el nRF52840: este ejemplo necesita la placa real.

> **Rev1** (IMU LSM9DS1, ya descatalogada): en `platformio.ini` cambia `arduino-libraries/Arduino_BMI270_BMM150@1.2.4` por `arduino-libraries/Arduino_LSM9DS1@1.1.1`, y en los dos `main.cpp` cambia `#include <Arduino_BMI270_BMM150.h>` por `#include <Arduino_LSM9DS1.h>`. El resto (umbral, 119 muestras, normalización) no cambia.

## Qué hay en la carpeta

| Archivo | Para qué |
|---|---|
| `platformio.ini` | Dos entornos: `captura` (compila `src/captura/`) e `inferencia` (compila `src/inferencia/`, el predeterminado). |
| `src/captura/main.cpp` | Espera un movimiento de más de 2,5 g y manda 119 muestras `aX,aY,aZ,gX,gY,gZ` en CSV, con una línea vacía entre gestos. |
| `src/inferencia/main.cpp` | Graba el gesto igual, lo normaliza igual que el cuaderno, ejecuta la red con ArduTFLite y enciende el LED RGB. |
| `include/model.h` | El modelo entrenado (float32, 148 380 bytes). Lo genera el cuaderno. |
| `entrenamiento/gestos_tinyml_colab.ipynb` | Cuaderno para Google Colab, corregido para el TensorFlow actual. |
| `entrenamiento/entrenar_gestos.py` | El mismo código que el cuaderno, para ejecutarlo en el PC. |
| `entrenamiento/punch.csv`, `flex.csv` | **Datos SINTÉTICOS** (ver abajo). |
| `entrenamiento/simular_datos.py` | El script que generó esos datos sintéticos. |
| `entrenamiento/salida_entrenamiento.txt` | Salida real de una ejecución de `entrenar_gestos.py`. |
| `diagrama-flujo.excalidraw`, `diagrama-pipeline.excalidraw` | Flujo de los dos programas y camino completo captura → modelo → placa. |

> **Los `punch.csv` y `flex.csv` que trae el proyecto son SINTÉTICOS.** El repositorio oficial del tutorial ([ArduinoTensorFlowLiteTutorials](https://github.com/arduino/ArduinoTensorFlowLiteTutorials)) no publica datos de gestos: cada participante graba los suyos. `simular_datos.py` los fabrica con un modelo aproximado del movimiento (golpe hacia delante y flexión del brazo) para que el cuaderno y la compilación funcionen desde el primer día. **El `model.h` incluido está entrenado con esos datos: no esperes que reconozca bien tus gestos reales.** Captura los tuyos, vuelve a entrenar y reemplaza `include/model.h`. No ejecutes `simular_datos.py` después de copiar tu captura: la sobrescribe.

## Paso 1 · Capturar gestos (env:captura)

```
pio run -e captura -t upload
pio device monitor -e captura -f log2file
```

El monitor guarda todo lo que llega en `platformio-device-monitor-<fecha>.log` dentro del proyecto. Al abrirlo verás:

```
aX,aY,aZ,gX,gY,gZ
```

Sujeta la placa con el USB hacia el codo y haz un **punch** (golpe hacia delante). El LED naranja se enciende mientras graba (≈ 1,2 s) y llegan 119 líneas como estas (los números dependen de tu movimiento), seguidas de una línea vacía:

```
0.512,2.734,1.020,12.451,-3.112,40.270
...
```

Repite el gesto 10 a 40 veces, cierra el monitor (`Ctrl+C`), renombra el `.log` a `punch.csv` y deja la cabecera una sola vez (el cuaderno ignora igualmente las cabeceras repetidas y las líneas vacías). Haz lo mismo con **flex** (flexión del brazo, como al levantar una pesa) → `flex.csv`.

La Nano 33 BLE tiene USB nativo: `while (!Serial)` espera a que abras el monitor, y la velocidad (115200) no limita nada. Si la subida falla, pulsa dos veces seguidas el botón de reset (el LED naranja «respira») y vuelve a subir.

## Paso 2 · Entrenar en Colab

1. Abre `entrenamiento/gestos_tinyml_colab.ipynb` en [colab.research.google.com](https://colab.research.google.com) (Archivo → Subir cuaderno).
2. Sube `punch.csv` y `flex.csv` al panel de archivos.
3. Entorno de ejecución → Ejecutar todas. Tarda 1 o 2 minutos (600 épocas con `batch_size=1`).
4. Descarga `model.h` del panel de archivos y cópialo en `include/model.h`.

Correcciones respecto al cuaderno oficial: no instala `tensorflow==2.0.0-rc1` (ya no se puede), declara la entrada con `tf.keras.Input` (Keras 3), mide la exactitud en Keras y en el `.tflite`, y escribe `model.h` con Python (sin `xxd`). La red, la normalización y la división 60/20/20 son las del original.

**En el PC** (opcional, Python 3.10–3.12):

```
cd entrenamiento
python3 -m venv .venv
.venv/bin/pip install tensorflow pandas matplotlib
.venv/bin/python entrenar_gestos.py        (escribe ../include/model.h y graficas/)
```

Resultado real con los datos sintéticos (`salida_entrenamiento.txt`, TensorFlow 2.21.0, Keras 3.15.1, Python 3.11.7): 36 547 parámetros, exactitud en prueba 100 % (16/16) en Keras y en el `.tflite`, pérdida MSE de prueba 4,0 × 10⁻⁸, `.tflite` de 148 380 bytes, `model.h` de 915 352 bytes de texto. Cuantizado a int8 (solo para comparar, no se usa aquí) ocuparía 40 872 bytes, 3,6 veces menos: eso lo hace el ejemplo 21. Con datos sintéticos tan limpios el 100 % no demuestra nada; con tus datos, mira la matriz de confusión.

## Paso 3 · Inferencia (env:inferencia)

```
pio run -e inferencia -t upload
pio device monitor -e inferencia
```

Salida (los valores marcados con … dependen del gesto y de la placa):

```
[INICIO] Ejemplo 20 - clasificador de gestos (TensorFlow Lite Micro)
[IMU] acelerometro 99.84 Hz, giroscopio 99.84 Hz
[MODELO] model.h: 148380 bytes en flash, arena de 8192 bytes en RAM
[MODELO] listo. Haz un gesto (punch o flex) con la placa en la mano.
[GESTO 1] 119 muestras en … ms, inferencia en … us
  punch: …… %
  flex: …… %
  -> punch (LED rojo)
```

El LED RGB queda en **rojo** (punch), **azul** (flex) o **amarillo** si la probabilidad mayor no llega al 80 % (`-> dudoso: maximo …… % < 80 % (LED amarillo)`). Sin PC conectado, el programa arranca a los 5 s y los LED funcionan igual.

Si cambias los gestos: misma lista y mismo orden en `GESTURES` (cuaderno) y `GESTOS` (sketch); si son más de dos, añade colores en el `if` final.

## Compilación

| Entorno | Flash | RAM |
|---|---|---|
| `captura` | 107 292 bytes (10,9 %) | 44 504 bytes (17,0 %) |
| `inferencia` | 503 512 bytes (51,2 %) | 58 536 bytes (22,3 %) |

La **primera** compilación de un proyecto nuevo tarda bastante: PlatformIO descarga la plataforma `nordicnrf52` y el núcleo Arduino mbed (varios cientos de MB, unos 10 minutos según la conexión) y compila TensorFlow Lite Micro entero (34 minutos medidos en este equipo, compilando a la vez los ejemplos 20 y 21, con el núcleo ya descargado). Las siguientes tardan unos segundos. Si solo cambias `model.h`, se recompila `main.cpp`.

## Licencias y créditos

- `src/captura/main.cpp`: adaptación de `IMU_Capture` (Don Coleman, Sandeep Mistry, Dominic Pajak; dominio público) del repositorio [arduino/ArduinoTensorFlowLiteTutorials](https://github.com/arduino/ArduinoTensorFlowLiteTutorials).
- `src/inferencia/main.cpp`: basado en `ArduinoNano33BLE_GestureClassifier` de [ArduTFLite](https://github.com/spaziochirale/ArduTFLite) (Spazio Chirale, Apache 2.0; el sketch se declara de dominio público).
- El cuaderno parte de `GestureToEmoji/arduino_tinyml_workshop.ipynb` del mismo repositorio de Arduino (sin archivo de licencia; se cita y se reescribe, no se copian datos).
- Librerías (se descargan, no se incluyen): ArduTFLite 1.0.2 y Chirale_TensorFLowLite 2.0.0 (Apache 2.0), Arduino_BMI270_BMM150 1.2.4 (LGPL 2.1).
