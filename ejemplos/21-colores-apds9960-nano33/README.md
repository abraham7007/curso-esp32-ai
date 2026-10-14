# Ejemplo 21 · Colores con el APDS9960 y un modelo cuantizado int8 (Nano 33 BLE Sense Rev2)

```
env:captura ──► rojo.csv / verde.csv / azul.csv ──► Colab (colores_tinyml_colab.ipynb) ──► model.h ──► env:inferencia
 r,g,b normalizado     una lectura por línea         red 3 → 8 → 3, cuantización int8       include/    LED RGB del color
```

**Placa: Arduino Nano 33 BLE Sense Rev2.** El sensor de color, proximidad y gestos (APDS9960, junto al LED de encendido) es el mismo en la **Rev1**: este proyecto sirve para las dos sin cambios.
Wokwi no simula el nRF52840: hace falta la placa real.

Frente al ejemplo 20 cambian dos cosas: la red es diminuta (59 parámetros) y el modelo está **cuantizado a int8 completo** (pesos, entrada y salida), así que el sketch cuantiza la entrada y descuantiza la salida. Para eso no sirve ArduTFLite (solo maneja tensores float): se usa directamente el intérprete de Chirale_TensorFLowLite.

## Qué hay en la carpeta

| Archivo | Para qué |
|---|---|
| `platformio.ini` | Entornos `captura` (`src/captura/`) e `inferencia` (`src/inferencia/`, el predeterminado). |
| `src/captura/main.cpp` | Con un objeto pegado al sensor (proximidad = 0) y luz suficiente, imprime `r,g,b` normalizados por la suma. |
| `src/inferencia/main.cpp` | Lee el color, lo cuantiza con la escala y el punto cero del modelo, ejecuta la red y enciende el LED RGB del color. |
| `include/model.h` | Modelo int8 (2 360 bytes). Lo genera el cuaderno. |
| `entrenamiento/colores_tinyml_colab.ipynb` | Cuaderno para Colab con la conversión int8 y el conjunto representativo. |
| `entrenamiento/entrenar_colores.py` | El mismo código, para el PC. |
| `entrenamiento/rojo.csv`, `verde.csv`, `azul.csv` | **Datos SINTÉTICOS** (ver abajo). |
| `entrenamiento/simular_datos.py` | El script que los generó. |
| `entrenamiento/salida_entrenamiento.txt` | Salida real de `entrenar_colores.py`. |
| `diagrama-flujo.excalidraw`, `diagrama-pipeline.excalidraw` | Flujo del sketch de inferencia y camino completo. |

> **Los tres CSV del proyecto son SINTÉTICOS.** `simular_datos.py` supone unas proporciones típicas de cartulinas roja, verde y azul (150 lecturas por color, en 6 tandas) y les suma ruido. El sensor real puede dar proporciones distintas (sus canales verde y azul suelen pesar más de lo esperado), así que **captura tus objetos y vuelve a entrenar antes de la clase**. El tutorial oficial FruitToEmoji publica datos de manzana, plátano y naranja en `FruitToEmoji/SampleData/`, pero el repositorio no tiene licencia, por eso no se copian aquí: puedes descargarlos de [github.com/arduino/ArduinoTensorFlowLiteTutorials](https://github.com/arduino/ArduinoTensorFlowLiteTutorials/tree/master/FruitToEmoji/SampleData) (cabecera `Red,Green,Blue`: cámbiala por `r,g,b`). No ejecutes `simular_datos.py` después de copiar tu captura: la sobrescribe.

## Paso 1 · Capturar colores (env:captura)

```
pio run -e captura -t upload
pio device monitor -e captura -f log2file
```

Al abrir el monitor llega la cabecera `r,g,b`. Acerca el objeto hasta casi tocar el sensor: mientras esté ahí, el LED naranja se enciende y llega una línea por lectura (los valores dependen del objeto y de la luz; suman 1):

```
r,g,b
0.552,0.241,0.207
0.548,0.244,0.208
...
```

Mueve un poco el objeto, cambia el ángulo, aléjalo y vuelve a acercarlo (varias «tandas»). Unas 100 a 200 lecturas por color bastan. Renombra el `.log` a `rojo.csv` y repite con `verde.csv` y `azul.csv`.

## Paso 2 · Entrenar y cuantizar en Colab

1. Abre `entrenamiento/colores_tinyml_colab.ipynb` en Colab y sube los tres CSV.
2. Ejecutar todas (unos 20 s).
3. Descarga `model.h` y cópialo en `include/model.h`.

El cuaderno convierte el modelo dos veces y compara:

```python
convertidor.optimizations = [tf.lite.Optimize.DEFAULT]
convertidor.representative_dataset = dataset_representativo   # 150 lecturas + los extremos 0 y 1
convertidor.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
convertidor.inference_input_type = tf.int8
convertidor.inference_output_type = tf.int8
```

Resultado real con los datos sintéticos (`salida_entrenamiento.txt`, TensorFlow 2.21.0, Keras 3.15.1, Python 3.11.7):

| | `.tflite` | `model.h` (texto) | Exactitud en prueba |
|---|---|---|---|
| float32 | 1 992 bytes | 12 543 bytes | 100 % (90/90) |
| int8 | 2 360 bytes | 14 911 bytes | 100 % (90/90) |

Entrada int8: `scale = 0.003922` (1/255), `zero_point = -128`. Salida int8: `scale = 0.003906` (1/256), `zero_point = -128`.

**Aquí int8 ocupa más que float32**: con 59 parámetros, los pesos ocupan 236 bytes en float y unos 92 en int8 (48 pesos en int8 más 11 sesgos, que TFLite guarda en int32), y lo demás del archivo (estructura, nombres, escalas de cuantización) pesa más. La cuantización encoge de verdad cuando los pesos dominan: la red del ejemplo 20 (36 547 parámetros) pasa de 148 380 a 40 872 bytes, 3,6 veces menos. Lo que int8 sí aporta siempre es aritmética entera (más rápida en el Cortex-M4 con CMSIS-NN) y menos RAM por tensor.

Las lecturas seguidas de una misma tanda se parecen mucho; el reparto 60/20/20 al azar (como el original) da una exactitud optimista. Lo honesto es probar con una tanda nueva, otro día o con otra luz.

En el PC: `python3 -m venv .venv && .venv/bin/pip install tensorflow pandas matplotlib && .venv/bin/python entrenar_colores.py` (dentro de `entrenamiento/`).

## Paso 3 · Inferencia (env:inferencia)

```
pio run -e inferencia -t upload
pio device monitor -e inferencia
```

Salida (las líneas `[MODELO]` son las del `model.h` incluido; `[OBJETO]` y los porcentajes dependen del objeto, y «…» del momento):

```
[INICIO] Ejemplo 21 - clasificador de colores int8 (TensorFlow Lite Micro)
[MODELO] model.h: 2360 bytes en flash, arena usada … de 4096 bytes
[MODELO] entrada int8 scale=0.003922 zero_point=-128
[MODELO] salida  int8 scale=0.003906 zero_point=-128
[MODELO] listo. Acerca un objeto rojo, verde o azul hasta casi tocar el sensor.
[OBJETO 1] r=0.552 g=0.241 b=0.207 -> int8 [13, -67, -75], inferencia en … us
  rojo: 99.61 %
  verde: 0.00 %
  azul: 0.00 %
  -> rojo (LED rojo)
```

(Esos porcentajes son los que da el modelo incluido para esa entrada, calculados en el PC con el mismo `.tflite`; para `r=0.400 g=0.350 b=0.250` da 25,00 % / 74,22 % / 0,39 % y responde `-> dudoso (LED apagado)` porque ninguno llega al 80 %.)

El LED RGB se enciende del color detectado hasta que retiras el objeto. Si al arrancar falta el sensor o el modelo no es int8, imprime `[ERROR] …` y el LED rojo parpadea.

## Compilación

| Entorno | Flash | RAM |
|---|---|---|
| `captura` | 86 108 bytes (8,8 %) | 43 864 bytes (16,7 %) |
| `inferencia` | 129 696 bytes (13,2 %) | 48 368 bytes (18,5 %) |

Primera compilación: PlatformIO descarga `nordicnrf52` y el núcleo Arduino mbed (unos 10 minutos según la conexión) y compila TensorFlow Lite Micro (32 minutos medidos en este equipo, compilando a la vez los ejemplos 20 y 21, con el núcleo ya descargado). Después, segundos. El sketch registra solo `FULLY_CONNECTED` y `SOFTMAX` (`MicroMutableOpResolver<2>`), las dos operaciones que el cuaderno dice que usa la red. Por eso, y por el modelo de 2 KB, la inferencia ocupa 130 KB de flash frente a los 504 KB del ejemplo 20 (que registra todas las operaciones con ArduTFLite y lleva un modelo de 148 KB).

## Licencias y créditos

- `src/captura/main.cpp`: adaptación de `object_color_capture` (tutorial FruitToEmoji de Arduino, dominio público), [arduino/ArduinoTensorFlowLiteTutorials](https://github.com/arduino/ArduinoTensorFlowLiteTutorials).
- `src/inferencia/main.cpp`: flujo de `object_color_classify` (mismo tutorial, dominio público), reescrito para int8 con la cuantización del ejemplo `hello_world` de [Chirale_TensorFlowLite](https://github.com/spaziochirale/Chirale_TensorFlowLite) (Apache 2.0).
- El cuaderno parte de `FruitToEmoji/FruitToEmoji.ipynb` (repositorio sin archivo de licencia; se cita y se reescribe).
- Librerías (se descargan, no se incluyen): Chirale_TensorFLowLite 2.0.0 (Apache 2.0), Arduino_APDS9960 1.0.4 (LGPL 2.1).
