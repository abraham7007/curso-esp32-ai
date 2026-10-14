# %% [markdown]
# # TinyML en la Arduino Nano 33 BLE Sense Rev2 · Reconocimiento de gestos
#
# Curso «Fundamentos de ESP32 + AI» (OTI-UNI) · sesión 6 · ejemplo 20.
#
# Versión corregida del cuaderno oficial **GestureToEmoji / arduino_tinyml_workshop.ipynb**
# (Sandeep Mistry y Don Coleman, Arduino, 2019:
# https://github.com/arduino/ArduinoTensorFlowLiteTutorials/). Cambios respecto al original:
#
# - **No instala `tensorflow==2.0.0-rc1`** (esa versión ya no existe para el Python de Colab).
#   Usa el TensorFlow que trae Colab (2.x actual, Keras 3).
# - Declara la entrada de la red (`tf.keras.Input`), que Keras 3 necesita para convertir.
# - Lee los CSV aunque tengan cabeceras repetidas (una por cada vez que abriste el monitor).
# - Mide la **exactitud** con los datos de prueba, en Keras y en el modelo `.tflite` ya convertido.
# - Escribe `model.h` con Python (no hace falta `xxd`) y con `alignas(16)`, como pide ArduTFLite.
#
# El mismo código está en `entrenar_gestos.py` para ejecutarlo en el PC.

# %% [markdown]
# ## 1 · Preparar el entorno
#
# Colab ya trae TensorFlow, pandas y matplotlib. **No instales `tensorflow==2.0.0-rc1`**
# como el cuaderno original: falla. Esta celda solo muestra las versiones.

# %% [colab]
# !python --version
# !pip list 2>/dev/null | grep -iE "^(tensorflow|keras|numpy|pandas) "

# %% [markdown]
# ## 2 · Subir los datos
#
# 1. Abre el panel de la izquierda de Colab (icono de carpeta).
# 2. Arrastra `punch.csv` y `flex.csv` (los que capturaste con el entorno `captura`).
#
# Cada archivo: cabecera `aX,aY,aZ,gX,gY,gZ`, 119 líneas por gesto y una línea vacía entre gestos.

# %%
import os
import sys

import matplotlib
import numpy as np
import pandas as pd

# ¿Dónde están los CSV? En Colab, en /content; en el PC, junto a este archivo.
EN_COLAB = "google.colab" in sys.modules
if EN_COLAB:
    CARPETA = "/content"
    SALIDA_MODEL_H = "/content/model.h"
else:
    matplotlib.use("Agg")       # en el PC las gráficas se guardan como PNG
    CARPETA = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
    SALIDA_MODEL_H = os.path.join(CARPETA, "..", "include", "model.h")

import matplotlib.pyplot as plt


def mostrar(nombre):
    """En Colab dibuja la gráfica; en el PC la guarda en entrenamiento/graficas/."""
    if EN_COLAB:
        plt.show()
    else:
        os.makedirs(os.path.join(CARPETA, "graficas"), exist_ok=True)
        plt.savefig(os.path.join(CARPETA, "graficas", nombre + ".png"), dpi=80)
        plt.close("all")


def leer_csv(nombre):
    """Lee un CSV de captura. Descarta líneas vacías, cabeceras repetidas y texto suelto."""
    df = pd.read_csv(os.path.join(CARPETA, nombre + ".csv"))
    df = df.apply(pd.to_numeric, errors="coerce").dropna().reset_index(drop=True)
    return df

# %% [markdown]
# ## 3 · Ver los datos (opcional)
#
# Aceleración y giro en gráficas separadas: tienen unidades y escalas distintas.

# %%
df = leer_csv("punch")
index = range(1, len(df["aX"]) + 1)
plt.rcParams["figure.figsize"] = (20, 10)

plt.plot(index, df["aX"], "g-", label="x")
plt.plot(index, df["aY"], "b-", label="y")
plt.plot(index, df["aZ"], "r-", label="z")
plt.title("Aceleración (punch)")
plt.xlabel("Muestra")
plt.ylabel("Aceleración (g)")
plt.legend()
mostrar("punch_aceleracion")

plt.plot(index, df["gX"], "g-", label="x")
plt.plot(index, df["gY"], "b-", label="y")
plt.plot(index, df["gZ"], "r-", label="z")
plt.title("Giroscopio (punch)")
plt.xlabel("Muestra")
plt.ylabel("Giro (grados/s)")
plt.legend()
mostrar("punch_giroscopio")

# %% [markdown]
# ## 4 · Preparar los datos
#
# Cada gesto (119 muestras × 6 valores = 714 números) es UNA entrada de la red.
# Se normaliza a 0…1 con los mismos rangos que usa el sketch de inferencia:
# aceleración −4…+4 g y giro −2000…+2000 grados/s (los rangos del BMI270 en la Rev2).
#
# Si capturas otros gestos, cambia la lista `GESTURES` **y** la del sketch, en el mismo orden.

# %%
import tensorflow as tf

print(f"TensorFlow version = {tf.__version__} (Keras {tf.keras.__version__}), Python {sys.version.split()[0]}\n")

# Semilla fija: misma ejecución, mismos números
SEED = 1337
np.random.seed(SEED)
tf.keras.utils.set_random_seed(SEED)

GESTURES = [
    "punch",
    "flex",
]

SAMPLES_PER_GESTURE = 119
NUM_GESTURES = len(GESTURES)
ONE_HOT_ENCODED_GESTURES = np.eye(NUM_GESTURES)

inputs = []
outputs = []

for gesture_index in range(NUM_GESTURES):
    gesture = GESTURES[gesture_index]
    print(f"Processing index {gesture_index} for gesture '{gesture}'.")
    output = ONE_HOT_ENCODED_GESTURES[gesture_index]
    df = leer_csv(gesture)

    num_recordings = int(df.shape[0] / SAMPLES_PER_GESTURE)
    sobrantes = df.shape[0] - num_recordings * SAMPLES_PER_GESTURE
    print(f"\tThere are {num_recordings} recordings of the {gesture} gesture.")
    if sobrantes:
        print(f"\tAVISO: sobran {sobrantes} filas (un gesto cortado al cerrar el monitor); se ignoran.")

    for i in range(num_recordings):
        tensor = []
        for j in range(SAMPLES_PER_GESTURE):
            index = i * SAMPLES_PER_GESTURE + j
            # normalizar a 0..1: aceleración -4..+4 g, giro -2000..+2000 grados/s
            tensor += [
                (df["aX"][index] + 4) / 8,
                (df["aY"][index] + 4) / 8,
                (df["aZ"][index] + 4) / 8,
                (df["gX"][index] + 2000) / 4000,
                (df["gY"][index] + 2000) / 4000,
                (df["gZ"][index] + 2000) / 4000,
            ]
        inputs.append(tensor)
        outputs.append(output)

inputs = np.array(inputs, dtype=np.float32)
outputs = np.array(outputs, dtype=np.float32)
print("Data set parsing and preparation complete.")

# %% [markdown]
# ## 5 · Mezclar y separar: 60 % entrenamiento, 20 % prueba, 20 % validación

# %%
num_inputs = len(inputs)
randomize = np.arange(num_inputs)
np.random.shuffle(randomize)
inputs = inputs[randomize]
outputs = outputs[randomize]

TRAIN_SPLIT = int(0.6 * num_inputs)
TEST_SPLIT = int(0.2 * num_inputs + TRAIN_SPLIT)

inputs_train, inputs_test, inputs_validate = np.split(inputs, [TRAIN_SPLIT, TEST_SPLIT])
outputs_train, outputs_test, outputs_validate = np.split(outputs, [TRAIN_SPLIT, TEST_SPLIT])
print(f"Entrenamiento: {len(inputs_train)} gestos, prueba: {len(inputs_test)}, validación: {len(inputs_validate)}")
print("Data set randomization and splitting complete.")

# %% [markdown]
# ## 6 · Construir y entrenar la red
#
# La misma red del tutorial: 714 → 50 → 15 → 2 (densa, ReLU, softmax).
# Única diferencia: Keras 3 necesita conocer la forma de la entrada (`tf.keras.Input`).

# %%
model = tf.keras.Sequential([
    tf.keras.Input(shape=(SAMPLES_PER_GESTURE * 6,)),
    tf.keras.layers.Dense(50, activation="relu"),
    tf.keras.layers.Dense(15, activation="relu"),
    tf.keras.layers.Dense(NUM_GESTURES, activation="softmax"),
])
model.compile(optimizer="rmsprop", loss="mse", metrics=["mae", "accuracy"])
model.summary()


class Progreso(tf.keras.callbacks.Callback):
    """Una línea cada 100 épocas en lugar de 600 líneas."""
    def on_epoch_end(self, epoch, logs=None):
        if (epoch + 1) % 100 == 0:
            print(f"época {epoch + 1:3d}: loss={logs['loss']:.2e} val_loss={logs['val_loss']:.2e} "
                  f"accuracy={logs['accuracy']:.3f} val_accuracy={logs['val_accuracy']:.3f}")


history = model.fit(inputs_train, outputs_train, epochs=600, batch_size=1,
                    validation_data=(inputs_validate, outputs_validate),
                    verbose=0, callbacks=[Progreso()])

# %% [markdown]
# ## 7 · Verificar: pérdida y error medio absoluto

# %%
plt.rcParams["figure.figsize"] = (20, 10)
loss = history.history["loss"]
val_loss = history.history["val_loss"]
epochs = range(1, len(loss) + 1)
plt.plot(epochs, loss, "g.", label="Pérdida de entrenamiento")
plt.plot(epochs, val_loss, "b", label="Pérdida de validación")
plt.title("Pérdida (error cuadrático medio)")
plt.xlabel("Época")
plt.ylabel("Pérdida")
plt.legend()
mostrar("perdida")

SKIP = 100
mae = history.history["mae"]
val_mae = history.history["val_mae"]
plt.plot(epochs[SKIP:], mae[SKIP:], "g.", label="MAE de entrenamiento")
plt.plot(epochs[SKIP:], val_mae[SKIP:], "b.", label="MAE de validación")
plt.title("Error medio absoluto (desde la época 100)")
plt.xlabel("Época")
plt.ylabel("MAE")
plt.legend()
mostrar("mae")

# %% [markdown]
# ## 8 · Probar con datos que la red no vio
#
# Exactitud = gestos bien clasificados / gestos de prueba. Con pocos datos, un solo error
# mueve mucho el porcentaje: mira también la matriz de confusión.

# %%
perdida_test, mae_test, exactitud_test = model.evaluate(inputs_test, outputs_test, verbose=0)
predictions = model.predict(inputs_test, verbose=0)
print("predictions =\n", np.round(predictions, decimals=3))
print("actual =\n", outputs_test)

real = outputs_test.argmax(axis=1)
pred = predictions.argmax(axis=1)
matriz = np.zeros((NUM_GESTURES, NUM_GESTURES), dtype=int)
for r, p in zip(real, pred):
    matriz[r, p] += 1
print(f"\nPérdida final (MSE): entrenamiento={loss[-1]:.2e} validación={val_loss[-1]:.2e} prueba={perdida_test:.2e}")
print(f"Exactitud (Keras, prueba): {exactitud_test * 100:.1f} % ({int((real == pred).sum())}/{len(real)})")
print("Matriz de confusión (filas = real, columnas = predicho):", GESTURES)
print(matriz)

# %% [markdown]
# ## 9 · Convertir a TensorFlow Lite (sin cuantizar, float32)
#
# `tf.lite` sigue funcionando en TensorFlow 2.x aunque está marcado como obsoleto
# (su reemplazo es el paquete `ai-edge-litert`). El modelo se queda en float32:
# cada uno de los 36 547 parámetros ocupa 4 bytes. El ejemplo 21 lo cuantiza a int8.

# %%
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

with open(os.path.join(CARPETA, "gesture_model.tflite"), "wb") as f:
    f.write(tflite_model)
print(f"Parámetros del modelo: {model.count_params():,}")
print(f"Model is {len(tflite_model):,} bytes")

# Comprobar que el .tflite clasifica igual que Keras
# Sin el acelerador XNNPACK del PC: así se ven las mismas operaciones que ejecutará la placa
interprete = tf.lite.Interpreter(
    model_content=tflite_model,
    experimental_op_resolver_type=tf.lite.experimental.OpResolverType.BUILTIN_WITHOUT_DEFAULT_DELEGATES)
interprete.allocate_tensors()
ent = interprete.get_input_details()[0]
sal = interprete.get_output_details()[0]
aciertos = 0
for x, r in zip(inputs_test, real):
    interprete.set_tensor(ent["index"], x.reshape(1, -1))
    interprete.invoke()
    aciertos += int(interprete.get_tensor(sal["index"]).argmax() == r)
print(f"Exactitud (.tflite float32, prueba): {aciertos / len(real) * 100:.1f} % ({aciertos}/{len(real)})")
print(f"Entrada: {ent['dtype'].__name__} {ent['shape'].tolist()}  Salida: {sal['dtype'].__name__} {sal['shape'].tolist()}")
ops = sorted({d["op_name"] for d in interprete._get_ops_details()})
print("Operaciones que necesita el microcontrolador:", ", ".join(ops))

# %% [markdown]
# ## 10 · Escribir `model.h` para el sketch
#
# El arreglo se llama `model`, como espera `src/inferencia/main.cpp`, y va con `alignas(16)`.
# (Equivale a `xxd -i gesture_model.tflite`, que en Colab exigía instalar `xxd` con apt-get.)
# En Colab: panel de archivos → `model.h` → Descargar. Cópialo en `include/model.h` del proyecto.

# %%
def escribir_model_h(datos, ruta, descripcion):
    lineas = [
        "// model.h · generado por entrenamiento/entrenar_gestos.py (o el cuaderno de Colab)",
        f"// {descripcion}",
        f"// {len(datos):,} bytes. No lo edites a mano: vuelve a entrenar y reemplázalo.",
        "#pragma once",
        "",
        "alignas(16) const unsigned char model[] = {",
    ]
    for i in range(0, len(datos), 12):
        lineas.append("  " + ", ".join(f"0x{b:02x}" for b in datos[i:i + 12]) + ",")
    lineas += ["};", f"const unsigned int model_len = {len(datos)};", ""]
    with open(ruta, "w", encoding="utf-8") as f:
        f.write("\n".join(lineas))


escribir_model_h(tflite_model, SALIDA_MODEL_H,
                 f"Gestos {GESTURES}, red densa 714 -> 50 -> 15 -> {NUM_GESTURES}, float32 sin cuantizar.")
model_h_size = os.path.getsize(SALIDA_MODEL_H)
print(f"Header file, model.h, is {model_h_size:,} bytes.")
if EN_COLAB:
    print("\nAbre el panel de archivos (actualízalo si hace falta) y descarga model.h.")
else:
    print(f"Escrito en {os.path.normpath(SALIDA_MODEL_H)}")

# %% [markdown]
# ## 11 · (Solo para comparar) ¿Cuánto ocuparía cuantizado a int8?
#
# Esta celda NO cambia `model.h`: el sketch de este ejemplo usa ArduTFLite, que trabaja
# con entradas y salidas float. La cuantización int8 completa se hace en el ejemplo 21.

# %%
def dataset_representativo():
    for x in inputs_train:
        yield [x.reshape(1, -1)]


conv8 = tf.lite.TFLiteConverter.from_keras_model(model)
conv8.optimizations = [tf.lite.Optimize.DEFAULT]
conv8.representative_dataset = dataset_representativo
conv8.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
conv8.inference_input_type = tf.int8
conv8.inference_output_type = tf.int8
modelo_int8 = conv8.convert()

it8 = tf.lite.Interpreter(
    model_content=modelo_int8,
    experimental_op_resolver_type=tf.lite.experimental.OpResolverType.BUILTIN_WITHOUT_DEFAULT_DELEGATES)
it8.allocate_tensors()
e8, s8 = it8.get_input_details()[0], it8.get_output_details()[0]
escala, cero = e8["quantization"]
aciertos8 = 0
for x, r in zip(inputs_test, real):
    xq = np.clip(np.round(x / escala + cero), -128, 127).astype(np.int8)
    it8.set_tensor(e8["index"], xq.reshape(1, -1))
    it8.invoke()
    aciertos8 += int(it8.get_tensor(s8["index"]).argmax() == r)
print(f"float32: {len(tflite_model):,} bytes · int8: {len(modelo_int8):,} bytes "
      f"({len(tflite_model) / len(modelo_int8):.1f} veces más pequeño)")
print(f"Exactitud (.tflite int8, prueba): {aciertos8 / len(real) * 100:.1f} % ({aciertos8}/{len(real)})")
