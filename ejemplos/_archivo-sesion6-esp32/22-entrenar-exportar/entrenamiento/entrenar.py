"""Entrena el clasificador de gestos en el PC y lo exporta a C para el ESP32.

Uso (desde esta carpeta, con el entorno de requirements.txt):
    python entrenar.py

Lee gestos.csv (el formato del ejemplo 21), separa entrenamiento y prueba POR
SESIÓN, compara un árbol de decisión de profundidad 4 con un bosque de 10
árboles, y escribe dos archivos en ../include/:

    modelo_gestos.h   el modelo como funciones C (emlearn, método inline,
                      dtype float): solo ifs y comparaciones, sin librerías
    casos_prueba.h    las ventanas de prueba (características y etiqueta) y
                      la matriz de confusión que obtuvo el PC, para que el
                      ESP32 las reevalúe y compruebe que da lo mismo
"""
import os
import sys
import tempfile

import numpy as np
import pandas as pd
import sklearn
import emlearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import GroupShuffleSplit
from sklearn.tree import DecisionTreeClassifier, export_text

from caracteristicas import NOMBRES

CLASES = ["quieto", "giro", "vaiven"]   # índice 0, 1, 2: el mismo orden en el ESP32
SEMILLA = 42
# Modelo que se exporta al ESP32: "bosque" o "arbol".
# Con estos datos los dos aciertan casi lo mismo. Se exporta el bosque porque
# el ejemplo 23 necesita una CONFIANZA: en el código de emlearn, la
# confianza es la fracción de los 10 árboles que votan por la clase ganadora
# (0.5 ... 1.0). Un árbol solo tiene un voto: su «confianza» siempre es 1.0.
# Si cambias a "arbol", los ejemplos 22 y 23 siguen compilando igual.
MODELO_EXPORTAR = "bosque"

AQUI = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.join(AQUI, "gestos.csv")
INCLUDE = os.path.join(AQUI, "..", "include")


def imprimir_matriz(m):
    print("            " + "".join("%8s" % c for c in CLASES) + "   <- prediccion")
    for nombre, fila in zip(CLASES, m):
        print("  %-8s  " % nombre + "".join("%8d" % v for v in fila))


def evaluar(nombre, modelo, X_tr, y_tr, X_te, y_te):
    modelo.fit(X_tr, y_tr)
    pred = modelo.predict(X_te)
    m = confusion_matrix(y_te, pred, labels=range(len(CLASES)))
    exactitud = accuracy_score(y_te, pred)
    print("\n=== %s ===" % nombre)
    print("Matriz de confusion (filas = real, columnas = prediccion), conjunto de PRUEBA:")
    imprimir_matriz(m)
    print("Exactitud en prueba: %.1f %%   (en entrenamiento: %.1f %%)"
          % (100 * exactitud, 100 * accuracy_score(y_tr, modelo.predict(X_tr))))
    print(classification_report(y_te, pred, labels=range(len(CLASES)),
                                target_names=CLASES, digits=3, zero_division=0))
    return pred, m, exactitud


def contar_nodos(modelo):
    arboles = modelo.estimators_ if hasattr(modelo, "estimators_") else [modelo]
    decisiones = sum(int((a.tree_.children_left != -1).sum()) for a in arboles)
    hojas = sum(int((a.tree_.children_left == -1).sum()) for a in arboles)
    return len(arboles), decisiones, hojas


def literal_c(v):
    """float32 -> literal C más corto que vuelve al mismo float32 (2375.8f, 79.0f)."""
    texto = np.format_float_positional(np.float32(v), trim="-")
    return (texto if "." in texto else texto + ".0") + "f"


def escribir_casos(ruta, X_te, y_te, m_pc, exactitud, nombre, n_arb, n_dec, n_hojas, bytes_h):
    with open(ruta, "w") as f:
        f.write("// !!! Generado por entrenamiento/entrenar.py: no lo edites a mano !!!\n")
        f.write("// Ventanas del conjunto de PRUEBA (sesiones que el modelo no vio al\n")
        f.write("// entrenar) y la matriz de confusion que obtuvo el PC con ellas.\n")
        f.write("#pragma once\n#include <stdint.h>\n\n")
        f.write("#define N_CARACTERISTICAS %d  // %s\n" % (len(NOMBRES), ", ".join(NOMBRES)))
        f.write("#define N_CLASES %d           // %s\n" % (len(CLASES), ", ".join(CLASES)))
        f.write("#define N_CASOS %d\n\n" % len(y_te))
        f.write('static const char* const NOMBRE_CLASE[N_CLASES] = {%s};\n'
                % ", ".join('"%s"' % c for c in CLASES))
        f.write('static const char* const MODELO_NOMBRE = "%s";\n' % nombre)
        f.write("static const int MODELO_ARBOLES = %d;\n" % n_arb)
        f.write("static const int MODELO_NODOS_DECISION = %d;\n" % n_dec)
        f.write("static const int MODELO_HOJAS = %d;\n" % n_hojas)
        f.write("static const long MODELO_BYTES_H = %d;  // tamano del texto de modelo_gestos.h\n" % bytes_h)
        f.write("static const float EXACTITUD_PC = %.4ff;\n\n" % exactitud)
        f.write("// Matriz de confusion del PC: filas = real, columnas = prediccion\n")
        f.write("static const uint16_t MATRIZ_PC[N_CLASES][N_CLASES] = {\n")
        for fila in m_pc:
            f.write("    {%s},\n" % ", ".join(str(int(v)) for v in fila))
        f.write("};\n\n")
        f.write("// media, desv, rango, cruces (mismo redondeo que imprime el ejemplo 21)\n")
        f.write("static const float CASOS_X[N_CASOS][N_CARACTERISTICAS] = {\n")
        for fila in X_te:
            f.write("    {%s},\n" % ", ".join(literal_c(v) for v in fila))
        f.write("};\n\n")
        f.write("static const uint8_t CASOS_Y[N_CASOS] = {\n")
        for i in range(0, len(y_te), 25):
            f.write("    %s,\n" % ", ".join(str(int(v)) for v in y_te[i:i + 25]))
        f.write("};\n")


def main():
    print("Python %s | scikit-learn %s | emlearn %s | numpy %s | pandas %s"
          % (sys.version.split()[0], sklearn.__version__, emlearn.__version__,
             np.__version__, pd.__version__))

    # Lectura tolerante con un registro del monitor serie pegado tal cual:
    # se ignoran las líneas «#», las cabeceras repetidas (una por arranque) y
    # cualquier línea que no sea un dato completo (texto de arranque, cortes).
    columnas = ["sesion", "ventana", "etiqueta"] + NOMBRES
    crudo = pd.read_csv(CSV, comment="#", header=None, names=columnas, dtype=str,
                        on_bad_lines="skip", skip_blank_lines=True)
    datos = crudo[crudo["etiqueta"].isin(CLASES)].copy()
    for col in NOMBRES:
        datos[col] = pd.to_numeric(datos[col], errors="coerce")
    datos = datos.dropna(subset=NOMBRES)
    descartadas = len(crudo) - len(datos) - int((crudo["sesion"] == "sesion").sum())
    if descartadas:
        print("Aviso: %d lineas de gestos.csv no son datos validos y se ignoran" % descartadas)
    X = datos[NOMBRES].to_numpy(dtype=np.float32)
    y = datos["etiqueta"].map({c: i for i, c in enumerate(CLASES)}).to_numpy()
    grupos = datos["sesion"].to_numpy()

    print("\ngestos.csv: %d ventanas, %d sesiones" % (len(datos), len(set(grupos))))
    print("  por clase: " + "  ".join("%s=%d" % (c, (y == i).sum()) for i, c in enumerate(CLASES)))

    # Separar POR SESIÓN: las ventanas de una misma sesión se solapan al 50 %
    # y comparten mano, placa y día. Si unas caen en entrenamiento y otras en
    # prueba, el modelo «ya vio» la prueba y la exactitud sale inflada.
    corte = GroupShuffleSplit(n_splits=1, test_size=0.25, random_state=SEMILLA)
    idx_tr, idx_te = next(corte.split(X, y, grupos))
    X_tr, y_tr, X_te, y_te = X[idx_tr], y[idx_tr], X[idx_te], y[idx_te]
    print("  entrenamiento: %d ventanas de %d sesiones" % (len(idx_tr), len(set(grupos[idx_tr]))))
    print("  prueba:        %d ventanas de %d sesiones (no vistas al entrenar)"
          % (len(idx_te), len(set(grupos[idx_te]))))

    arbol = DecisionTreeClassifier(max_depth=4, random_state=SEMILLA)
    bosque = RandomForestClassifier(n_estimators=10, max_depth=4, random_state=SEMILLA)
    _, m_arbol, ex_arbol = evaluar("Arbol de decision (profundidad 4)", arbol, X_tr, y_tr, X_te, y_te)
    _, m_bosque, ex_bosque = evaluar("Bosque de 10 arboles (profundidad 4)", bosque, X_tr, y_tr, X_te, y_te)

    print("Reglas del arbol de profundidad 4 (exportado como arbol, emlearn las escribe como ifs de C;\n el bosque son 10 arboles asi, cada uno con su propia muestra de los datos):")
    print(export_text(arbol, feature_names=NOMBRES, decimals=2))

    modelo = bosque if MODELO_EXPORTAR == "bosque" else arbol
    nombre = ("bosque de 10 arboles (profundidad 4)" if MODELO_EXPORTAR == "bosque"
              else "arbol de decision (profundidad 4)")

    # Exportar a C. method='inline' escribe cada árbol como ifs anidados;
    # dtype='float' compara las características como float (no hace falta
    # cuantizar: el ESP32 tiene unidad de coma flotante de precisión simple).
    os.makedirs(INCLUDE, exist_ok=True)
    ruta_modelo = os.path.join(INCLUDE, "modelo_gestos.h")
    # emlearn compila el C en el PC para poder predecir aquí con él; deja sus
    # archivos intermedios en ./tmp, así que se trabaja en una carpeta temporal.
    with tempfile.TemporaryDirectory() as temporal:
        os.chdir(temporal)
        c_modelo = emlearn.convert(modelo, method="inline", dtype="float")
        c_modelo.save(file=ruta_modelo, name="modelo_gestos")
        pred_c = np.array(c_modelo.predict(X_te))
        votos_c = np.array(c_modelo.predict_proba(X_te))
        os.chdir(AQUI)
    bytes_h = os.path.getsize(ruta_modelo)

    # La referencia para el ESP32 es lo que predice el código C de emlearn
    # (ejecutado aquí, en el PC), no scikit-learn: en un bosque, scikit-learn
    # PROMEDIA las probabilidades de los árboles y emlearn CUENTA VOTOS. Casi
    # siempre coinciden; en un empate de votos (5 a 5) pueden no hacerlo.
    pred_sk = modelo.predict(X_te)
    distintas = np.flatnonzero(pred_c != pred_sk)
    print("\nemlearn: el codigo C coincide con scikit-learn en %d de %d ventanas de prueba"
          % (len(y_te) - len(distintas), len(y_te)))
    for i in distintas:
        print("  distinta: %s -> scikit-learn=%s, C de emlearn=%s (votos %s)"
              % (X_te[i].tolist(), CLASES[pred_sk[i]], CLASES[pred_c[i]],
                 np.round(votos_c[i] * len(getattr(modelo, "estimators_", [0])), 1).tolist()))
    m_pc = confusion_matrix(y_te, pred_c, labels=range(len(CLASES)))
    exactitud = accuracy_score(y_te, pred_c)
    print("Matriz del modelo exportado (codigo C de emlearn en el PC) = la que debe dar el ESP32:")
    imprimir_matriz(m_pc)
    print("Exactitud: %.1f %% (%d/%d)" % (100 * exactitud, int(np.trace(m_pc)), len(y_te)))

    n_arb, n_dec, n_hojas = contar_nodos(modelo)
    ruta_casos = os.path.join(INCLUDE, "casos_prueba.h")
    escribir_casos(ruta_casos, X_te, y_te, m_pc, exactitud, nombre, n_arb, n_dec, n_hojas, bytes_h)

    print("\nExportado al ESP32: %s" % nombre)
    print("  %d arbol(es), %d nodos de decision, %d hojas" % (n_arb, n_dec, n_hojas))
    print("  include/modelo_gestos.h  %6d bytes de texto C" % bytes_h)
    print("  include/casos_prueba.h   %6d bytes (%d ventanas de prueba + matriz del PC)"
          % (os.path.getsize(ruta_casos), len(y_te)))


if __name__ == "__main__":
    main()
