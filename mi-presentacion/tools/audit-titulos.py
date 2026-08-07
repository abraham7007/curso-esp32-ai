#!/usr/bin/env python3
"""Audita rótulos de tema y títulos de lámina contra la regla del proyecto.

La regla está en METODOLOGIA-DE-CURSO.md, apartado 6, y es la del proyecto —no
la genérica de «título-acción» de las guías de presentación académica, que pide
justo lo contrario: oración completa con verbo. Aquí los títulos son **frases
nominales**. Convertirlos en oraciones desharía la corrección más trabajada del
mazo.

Lo que se marca:

  · INTERROGATIVO   — prohibido sin excepciones, también en láminas de artículo.
  · VERBO CONJUGADO — señal de título-acción; el título enuncia, no narra.
  · GENÉRICO        — podría encabezar la misma lámina en cualquier curso del
                      tema («Validación del dato», «Criterios de selección»).
                      Se detecta por ser corto y no nombrar nada concreto: ni
                      sigla, ni cifra, ni identificador, ni nombre propio.
  · CATEGORÍA       — nombra el tipo de lámina en vez de su contenido.
  · DUPLICADO       — dos láminas con el mismo título en el mazo.

Marcar no es corregir: el informe es para leerlo. Un título corto puede ser
correcto si la lámina que encabeza es igual de concreta.

Uso:  python3 tools/audit-titulos.py [clase-03]
"""

from __future__ import annotations

import html
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
SLIDES = RAIZ / "src" / "slides"

# Terminaciones de verbo conjugado en español que no aparecen en un sustantivo
# ni en un adjetivo frecuentes en estos títulos. La lista es corta a propósito:
# ampliarla dispara los falsos positivos sobre palabras como «memoria»
# (termina en -ia) o «entrada» (participio lexicalizado).
# «ería» e «iría» quedan FUERA aunque sean terminaciones de condicional:
# «batería», «mensajería» e «ingeniería» son sustantivos corrientes en este
# curso y las marcaban a las tres. Un condicional en un título es rarísimo; un
# sustantivo en -ería, constante.
VERBOS = re.compile(
    r"\b\w+(?:amos|áis|aban|ábamos|aron|aremos|arán|aría|"
    r"emos|éis|ieron|eremos|erán|"
    r"imos|ían|ieran|irán)\b",
    re.IGNORECASE,
)
# Verbos sueltos de uso frecuente en títulos-acción.
VERBOS_SUELTOS = {
    "es", "son", "está", "están", "tiene", "tienen", "hace", "hacen",
    "permite", "permiten", "produce", "producen", "requiere", "requieren",
    "depende", "dependen", "cambia", "cambian", "mejora", "mejoran",
    "reduce", "reducen", "aumenta", "aumentan", "falla", "fallan",
    "puede", "pueden", "debe", "deben", "muestra", "muestran",
}

CATEGORIAS = {
    "introducción", "conclusión", "conclusiones", "resumen", "objetivos",
    "contenido", "contenidos", "agenda", "índice", "generalidades",
    "conceptos", "definiciones", "ejemplos", "aplicaciones", "resultados",
}

# Palabras que hacen concreto un título aunque sea corto.
CONCRETO = re.compile(
    r"[A-ZÁÉÍÓÚÑ]{2,}"          # siglas: GPIO, UART, ADC, MQTT
    r"|\d"                       # cifras: 3,3 V, 115200
    r"|[a-zA-Z_]+\(\)"           # identificadores: delay()
    r"|ESP32|Wokwi|FreeRTOS|Arduino|PlatformIO"
)


def terminos_del_glosario() -> set[str]:
    """Los términos que el curso define en sus doce glosarios.

    Un título que ES uno de ellos no puede ser genérico: nombra exactamente
    una cosa, y la lámina siguiente la define. «Include guard» tiene dos
    palabras y ninguna sigla, así que la regla de concreción lo marcaba; es un
    falso positivo, y alargarlo para contentar al verificador habría empeorado
    el título.
    """
    limpio = lambda x: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", x)).strip()
    salida = set()
    for f in SLIDES.glob("*/*glosario*.html"):
        t = f.read_text()
        for m in re.finditer(r"<(?:summary|h3)>(.*?)</(?:summary|h3)>", t, re.S):
            cab = re.sub(r'<span class="glossary-item__alt">.*?</span>', "",
                         m.group(1), flags=re.S)
            termino = limpio(cab)
            if termino:
                salida.add(sin_tildes(termino.lower()))
    return salida


def sin_tildes(s: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn"
    )


def extraer(f: Path) -> tuple[str, str, str]:
    s = f.read_text()
    m = (
        re.search(r"<h1\b[^>]*>(.*?)</h1>", s, re.S)
        or re.search(r'<h2 class="(?:paper|code-hour)__title"[^>]*>(.*?)</h2>', s, re.S)
        or re.search(r"<h2\b[^>]*>(.*?)</h2>", s, re.S)
    )
    limpio = lambda x: html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", x))).strip()
    titulo = limpio(m.group(1)) if m else ""
    b = re.search(r'<span class="badge"\b[^>]*>(.*?)</span>', s, re.S)
    rotulo = limpio(b.group(1)) if b else ""
    # Las láminas de cierre las prescribe la metodología por nombre y se
    # repiten en las doce sesiones a propósito: marcarlas como genéricas o
    # duplicadas sería marcar la estructura del curso.
    estructural = any(
        k in f.name for k in ("glosario", "resumen", "referencias", "problemas-frecuentes")
    )
    tipo = (
        "portada" if f.name.startswith("01-portada")
        else "código" if "codigo" in f.name
        else "artículo" if "paper" in f.name
        else "cierre" if estructural
        else "concepto"
    )
    return tipo, rotulo, titulo


def revisar(titulo: str, tipo: str) -> list[str]:
    fallos = []
    if "?" in titulo or "¿" in titulo:
        fallos.append("INTERROGATIVO")

    palabras = re.findall(r"\b[\wáéíóúñÁÉÍÓÚÑ]+\b", titulo)
    minus = {sin_tildes(p.lower()) for p in palabras}
    if VERBOS.search(titulo) or (minus & {sin_tildes(v) for v in VERBOS_SUELTOS}):
        fallos.append("VERBO CONJUGADO")

    # La portada lleva el título de la sesión, no el de una lámina: no aplica
    # el criterio de concreción.
    if tipo not in ("portada", "cierre") and sin_tildes(titulo.lower()) not in GLOSARIO:
        # Una enumeración de conceptos con nombre —«Estado, evento y
        # transición»— es específica aunque sea corta y no lleve ninguna sigla.
        # El defecto que persigue la metodología es el rótulo de categoría de
        # dos o tres palabras: «Validación del dato», «Criterios de selección».
        enumeracion = "," in titulo
        if len(palabras) <= 3 and not CONCRETO.search(titulo) and not enumeracion:
            fallos.append("GENÉRICO")
        if minus & CATEGORIAS and len(palabras) <= 3:
            fallos.append("CATEGORÍA")
    return fallos


GLOSARIO: set[str] = set()


def main() -> None:
    global GLOSARIO
    GLOSARIO = terminos_del_glosario()
    filtro = sys.argv[1] if len(sys.argv) > 1 else None
    filas = []
    for f in sorted(SLIDES.rglob("*.html")):
        rel = f"{f.parent.name}/{f.name}"
        if filtro and filtro not in rel:
            continue
        tipo, rotulo, titulo = extraer(f)
        filas.append((rel, tipo, rotulo, titulo, revisar(titulo, tipo)))

    # Los títulos repetidos solo son defecto entre láminas de concepto: dos
    # sesiones pueden cerrar las dos con «Resumen de la sesión» a propósito.
    repes = Counter(t for _, tp, _, t, _ in filas if tp == "concepto" and t)
    for fila in filas:
        if fila[1] == "concepto" and repes[fila[3]] > 1:
            fila[4].append("DUPLICADO")

    marcadas = [f for f in filas if f[4]]
    print(f"Revisados {len(filas)} títulos · {len(marcadas)} marcados\n")
    for rel, tipo, rotulo, titulo, fallos in marcadas:
        print(f"  {', '.join(fallos)}")
        print(f"    {rel}  [{tipo}]")
        print(f"    «{titulo}»")
        if rotulo:
            print(f"    rótulo: {rotulo}")
        print()

    conteo = Counter(f for _, _, _, _, fs in filas for f in fs)
    if conteo:
        print("Por motivo:")
        for k, v in conteo.most_common():
            print(f"  {v:>3}  {k}")


if __name__ == "__main__":
    main()
