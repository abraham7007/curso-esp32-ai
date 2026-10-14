# %% [markdown]
# # TinyML en la Arduino Nano 33 BLE Sense Rev2 · Clasificar colores con el APDS9960
#
# Curso «Fundamentos de ESP32 + AI» (OTI-UNI) · sesión 6 · ejemplo 21.
#
# Parte del cuaderno oficial **FruitToEmoji / FruitToEmoji.ipynb** (Dominic Pajak,
# Sandeep Mistry y Don Coleman, Arduino: https://github.com/arduino/ArduinoTensorFlowLiteTutorials/),
# corregido para el TensorFlow actual y con dos cambios de fondo:
#
# - Red más pequeña: 3 → 8 → 3 (el original usaba 3 → 8 → 5 → 3).
# - **Cuantización int8 completa** con un conjunto representativo: pesos, entrada y salida
#   en enteros de 8 bits. El sketch tiene que cuantizar la entrada con la escala y el
#   punto cero que imprime este cuaderno (los lee del propio modelo, no hay que copiarlos).
#
# El mismo código está en `entrenar_colores.py` para ejecutarlo en el PC.

# %% [markdown]
# ## 1 · Preparar el entorno
#
# Colab ya trae TensorFlow, pandas y matplotlib: no hace falta instalar nada.
# (El cuaderno original hacía `!pip install tensorflow` y `%tensorflow_version 2.x`;
# ese comando mágico ya no existe en Colab.) Esta celda solo muestra las versiones.

# %% [colab]
# !python --version
# !pip list 2>/dev/null | grep -iE "^(tensorflow|keras|numpy|pandas) "

# %% [markdown]
# ## 2 · Subir los datos
#
# Arrastra al panel de archivos de Colab un CSV por clase: `rojo.csv`, `verde.csv`, `azul.csv`
# (los que capturaste con el entorno `captura`). Cabecera `r,g,b`, una lectura por línea.
#
# Si usas otros objetos, cambia la lista `CLASSES` **y** la del sketch, en el mismo orden.

# %%
import os
import sys

import matplotlib
import numpy as np
import pandas as pd

EN_COLAB = "google.colab" in sys.modules
if EN_COLAB:
    CARPETA = "/content"
    SALIDA_MODEL_H = "/content/model.h"
else:
    matplotlib.use("Agg")       # en el PC las gráficas se guardan como PNG
    CARPETA = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()
    SALIDA_MODEL_H = os.path.join(CARPETA, "..", "include", "model.h")

import matplotlib.pyplot as plt
import tensorflow as tf


def mostrar(nombre):
    """En Colab dibuja la gráfica; en el PC la guarda en entrenamiento/graficas/."""
    if EN_COLAB:
        plt.show()
    else:
        os.makedirs(os.path.join(CARPETA, "graficas"), exist_ok=True)
        plt.savefig(os.path.join(CARPETA, "graficas", nombre + ".png"), dpi=80)
        plt.close("all")


print(f"TensorFlow version = {tf.__version__} (Keras {tf.keras.__version__}), Python {sys.version.split()[0]}\n")

SEED = 1337
np.random.seed(SEED)
tf.keras.utils.set_random_seed(SEED)

CLASSES = ["rojo", "verde", "azul"]
NUM_CLASSES = len(CLASSES)
ONE_HOT_ENCODED_CLASSES = np.eye(NUM_CLASSES)

inputs = []
outputs = []

for class_index, objectClass in enumerate(CLASSES):
    df = pd.read_csv(os.path.join(CARPETA, objectClass + ".csv"))
    # fuera líneas vacías, cabeceras repetidas y mensajes sueltos del monitor
    df = df.apply(pd.to_numeric, errors="coerce").dropna().reset_index(drop=True)
    num_recordings = df.shape[0]
    print(f"{objectClass} -> salida {class_index} del clasificador: {num_recordings} lecturas {list(df)}")

    # una franja de color por lectura (como el cuaderno original)
    plt.rcParams["figure.figsize"] = (10, 1)
    pixels = df[["r", "g", "b"]].to_numpy(dtype=float)
    for i in range(num_recordings):
        plt.axvline(x=i, linewidth=8, color=tuple(pixels[i] / np.max(pixels[i])))
    plt.title(objectClass)
    mostrar("colores_" + objectClass)

    for i in range(num_recordings):
        inputs.append(pixels[i])
        outputs.append(ONE_HOT_ENCODED_CLASSES[class_index])

inputs = np.array(inputs, dtype=np.float32)
outputs = np.array(outputs, dtype=np.float32)
print("Data set parsing and preparation complete.")

# %% [markdown]
# ## 3 · Mezclar y separar: 60 % entrenamiento, 20 % prueba, 20 % validación
#
# Ojo: las lecturas seguidas de una misma tanda se parecen mucho. Si las mezclas al azar,
# la prueba ve «casi» los mismos datos que el entrenamiento y la exactitud sale optimista.
# Lo honesto es probar con una tanda que la red no vio (otro día, otra luz, otro objeto).

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
print(f"Entrenamiento: {len(inputs_train)} lecturas, prueba: {len(inputs_test)}, validación: {len(inputs_validate)}")

# %% [markdown]
# ## 4 · Construir y entrenar la red: 3 → 8 → 3

# %%
model = tf.keras.Sequential([
    tf.keras.Input(shape=(3,)),
    tf.keras.layers.Dense(8, activation="relu"),
    tf.keras.layers.Dense(NUM_CLASSES, activation="softmax"),
])
model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.01),
              loss="categorical_crossentropy", metrics=["accuracy"])
model.summary()


class Progreso(tf.keras.callbacks.Callback):
    """Una línea cada 50 épocas."""
    def on_epoch_end(self, epoch, logs=None):
        if (epoch + 1) % 50 == 0:
            print(f"época {epoch + 1:3d}: loss={logs['loss']:.4f} val_loss={logs['val_loss']:.4f} "
                  f"accuracy={logs['accuracy']:.3f} val_accuracy={logs['val_accuracy']:.3f}")


history = model.fit(inputs_train, outputs_train, epochs=300, batch_size=8,
                    validation_data=(inputs_validate, outputs_validate),
                    verbose=0, callbacks=[Progreso()])

plt.rcParams["figure.figsize"] = (12, 6)
plt.plot(history.history["loss"], "g.", label="Pérdida de entrenamiento")
plt.plot(history.history["val_loss"], "b", label="Pérdida de validación")
plt.title("Pérdida (entropía cruzada)")
plt.xlabel("Época")
plt.legend()
mostrar("perdida")

perdida_test, exactitud_test = model.evaluate(inputs_test, outputs_test, verbose=0)
real = outputs_test.argmax(axis=1)
print(f"\nPérdida final: entrenamiento={history.history['loss'][-1]:.4f} "
      f"validación={history.history['val_loss'][-1]:.4f} prueba={perdida_test:.4f}")
print(f"Exactitud (Keras float32, prueba): {exactitud_test * 100:.1f} %")

# %% [markdown]
# ## 5 · Convertir dos veces: float32 y int8
#
# **float32**: igual que el ejemplo 20.
#
# **int8 completo**: el convertidor mide los valores reales que circulan por la red con un
# *conjunto representativo* (aquí, 150 lecturas de entrenamiento más los extremos 0 y 1; con 100 a 500 basta) y elige,
# para cada tensor, una escala y un punto cero: `real = (entero − zero_point) × scale`.
# `inference_input_type = tf.int8` hace que también la ENTRADA y la SALIDA sean int8:
# el sketch cuantiza `r, g, b` antes de invocar y descuantiza las probabilidades después.

# %%
convertidor_float = tf.lite.TFLiteConverter.from_keras_model(model)
modelo_float = convertidor_float.convert()


def dataset_representativo():
    # Los extremos (1,0,0), (0,1,0), (0,0,1) y (0,0,0) fijan la escala de la entrada en 0..1:
    # sin ellos, un objeto más rojo que los del entrenamiento se saturaría en +127.
    for x in np.vstack([np.eye(3, dtype=np.float32), np.zeros((1, 3), np.float32)]):
        yield [x.reshape(1, 3)]
    for x in inputs_train[:150]:
        yield [x.reshape(1, 3)]


convertidor = tf.lite.TFLiteConverter.from_keras_model(model)
convertidor.optimizations = [tf.lite.Optimize.DEFAULT]
convertidor.representative_dataset = dataset_representativo
convertidor.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
convertidor.inference_input_type = tf.int8
convertidor.inference_output_type = tf.int8
modelo_int8 = convertidor.convert()

with open(os.path.join(CARPETA, "color_model_float.tflite"), "wb") as f:
    f.write(modelo_float)
with open(os.path.join(CARPETA, "color_model_int8.tflite"), "wb") as f:
    f.write(modelo_int8)

# %% [markdown]
# ## 6 · Comparar: tamaño y exactitud de los dos modelos convertidos

# %%
def interprete_de(modelo):
    # Sin el acelerador XNNPACK del PC: mismas operaciones que ejecutará la placa
    it = tf.lite.Interpreter(
        model_content=modelo,
        experimental_op_resolver_type=tf.lite.experimental.OpResolverType.BUILTIN_WITHOUT_DEFAULT_DELEGATES)
    it.allocate_tensors()
    return it


def exactitud_tflite(modelo):
    it = interprete_de(modelo)
    ent, sal = it.get_input_details()[0], it.get_output_details()[0]
    aciertos = 0
    for x, r in zip(inputs_test, real):
        if ent["dtype"] == np.int8:            # cuantizar la entrada, como en el sketch
            escala, cero = ent["quantization"]
            x = np.clip(np.round(x / escala + cero), -128, 127).astype(np.int8)
        it.set_tensor(ent["index"], x.reshape(1, 3))
        it.invoke()
        aciertos += int(it.get_tensor(sal["index"]).argmax() == r)
    ops = sorted({d["op_name"] for d in it._get_ops_details()})
    return aciertos, ent, sal, ops


def texto_model_h(datos, descripcion):
    lineas = [
        "// model.h · generado por entrenamiento/entrenar_colores.py (o el cuaderno de Colab)",
        f"// {descripcion}",
        f"// {len(datos):,} bytes. No lo edites a mano: vuelve a entrenar y reemplázalo.",
        "#pragma once",
        "",
        "alignas(16) const unsigned char model[] = {",
    ]
    for i in range(0, len(datos), 12):
        lineas.append("  " + ", ".join(f"0x{b:02x}" for b in datos[i:i + 12]) + ",")
    lineas += ["};", f"const unsigned int model_len = {len(datos)};", ""]
    return "\n".join(lineas)


print(f"Parámetros de la red: {model.count_params()} "
      f"(float32: {model.count_params() * 4} bytes de pesos; int8: ~{model.count_params()} bytes)\n")
for nombre, modelo in (("float32", modelo_float), ("int8", modelo_int8)):
    aciertos, ent, sal, ops = exactitud_tflite(modelo)
    print(f"[{nombre}] .tflite: {len(modelo):,} bytes · model.h: "
          f"{len(texto_model_h(modelo, '').encode('utf-8')):,} bytes de texto")
    print(f"[{nombre}] exactitud en prueba: {aciertos / len(real) * 100:.1f} % ({aciertos}/{len(real)})")
    print(f"[{nombre}] entrada {ent['dtype'].__name__} scale={ent['quantization'][0]:.6f} "
          f"zero_point={ent['quantization'][1]} · salida {sal['dtype'].__name__} "
          f"scale={sal['quantization'][0]:.6f} zero_point={sal['quantization'][1]}")
    print(f"[{nombre}] operaciones: {', '.join(ops)}\n")

print(f"Relación de tamaño int8/float32: {len(modelo_int8) / len(modelo_float):.2f}")
print("Con 59 parámetros, casi todo el archivo son metadatos (nombres, formas, escalas):")
print("la cuantización solo encoge de verdad cuando los pesos dominan (ejemplo 20: 36 547 parámetros).")

# %% [markdown]
# ## 7 · Escribir `model.h` (el modelo int8) para el sketch
#
# En Colab: panel de archivos → `model.h` → Descargar. Cópialo en `include/model.h`.

# %%
with open(SALIDA_MODEL_H, "w", encoding="utf-8") as f:
    f.write(texto_model_h(modelo_int8,
                          f"Colores {CLASSES}, red densa 3 -> 8 -> {NUM_CLASSES}, cuantizada int8 (entrada y salida int8)."))
print(f"Header file, model.h, is {os.path.getsize(SALIDA_MODEL_H):,} bytes.")
if EN_COLAB:
    print("\nAbre el panel de archivos (actualízalo si hace falta) y descarga model.h.")
else:
    print(f"Escrito en {os.path.normpath(SALIDA_MODEL_H)}")
