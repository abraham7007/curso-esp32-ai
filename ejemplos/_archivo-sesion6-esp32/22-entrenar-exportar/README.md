# Ejemplo 22 · Entrenar en el PC, exportar a C y comprobar en el ESP32

```
entrenamiento/gestos.csv ──► entrenar.py ──► include/modelo_gestos.h ──► ESP32
   (ejemplo 21)          scikit-learn         include/casos_prueba.h     reevalúa la prueba
                         + emlearn                                       [COINCIDE] PC=ESP32
```

> **Los datos de `entrenamiento/gestos.csv` son SINTÉTICOS.** Los generó `simular_datos.py` a partir de un modelo aproximado de cómo se mueve una mano sobre el potenciómetro, aplicando la misma función de características que el ESP32. Sirven para que el ejemplo funcione desde el primer día, no para sacar conclusiones. Reemplaza `gestos.csv` por tu captura del ejemplo 21 (ver su README) y vuelve a ejecutar `entrenar.py`. **No ejecutes `simular_datos.py` después de copiar tu captura: la sobrescribe.**

## En el PC

```
cd entrenamiento
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt        (Windows: .venv\Scripts\pip ...)
.venv/bin/python entrenar.py
```

`entrenar.py`:

1. Lee `gestos.csv` (formato del ejemplo 21).
2. Separa entrenamiento y prueba **por sesión** (`GroupShuffleSplit`): las ventanas de una sesión se solapan al 50 % y comparten mano, placa y día; mezclarlas inflaría la exactitud.
3. Compara un árbol de decisión de profundidad 4 con un bosque de 10 árboles: matriz de confusión e informe de clasificación de cada uno.
4. Exporta con emlearn (`method='inline'`, `dtype='float'`) a `include/modelo_gestos.h`: C99 puro, sin librerías en el chip.
5. Escribe `include/casos_prueba.h`: las ventanas de prueba y la matriz que obtuvo el código C de emlearn en el PC.

La salida real de una ejecución está en `entrenamiento/salida_entrenamiento.txt`.

`entrenamiento/caracteristicas.py` es la definición de las cuatro características en Python. Tiene que coincidir con `lib/Ventana/Ventana.cpp` de los ejemplos 20, 21 y 23: si cambias una, cambia la otra.

## En el ESP32

Compila y graba este proyecto. El programa clasifica las ventanas de prueba, imprime la matriz y la exactitud, y la compara celda a celda con la del PC (`[COINCIDE] PC=ESP32` o `[DIFIERE] …`). También mide el tiempo de una inferencia con `micros()` y el heap libre.

En Wokwi la CPU va más despacio que en la placa: los microsegundos medidos en simulación no valen como dato real.

Coste del modelo con los datos sintéticos (bosque de 10 árboles, 89 nodos de decisión): `modelo_gestos.h` ocupa 15,7 KB de texto, pero compilado son unos 1,6 KB de flash (medido compilando con y sin el modelo) y 0 bytes de RAM estática. Las 826 ventanas de prueba ocupan otros 14 KB de flash; en el ejemplo 23 no se incluyen.

Después de volver a entrenar, copia `include/modelo_gestos.h` a `ejemplos/23-inferencia-blynk/include/`.
