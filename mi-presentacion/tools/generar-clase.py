#!/usr/bin/env python3
"""Genera las láminas de una sesión a partir de un manifiesto JSON.

Emite archivos HTML autónomos, idénticos en forma a los escritos a mano: el
generador no deja rastro en el resultado ni se necesita para servirlo. Lo que
automatiza es exactamente lo que se hace mal a mano —la cabecera repetida, la
cadena de anterior/siguiente y el total de láminas—, no el contenido.

El manifiesto es una lista de láminas:

  {
    "clase": "clase-05",
    "sesion": "Sesión 5 · Máquinas de estados finitos",
    "laminas": [
      {"slug": "portada", "titulo": "…", "nav": "…", "icono": "i-flow",
       "clases": "slide", "contenido": "…html…", "scripts": "…"}
    ]
  }

`nav` es el rótulo corto que aparece en la tira de navegación; `titulo` es el
del <title> del documento. Se separan porque el rótulo debe caber en la tira y
el título debe ser completo.

Uso:
  python3 tools/generar-clase.py manifiesto.json [--dry]
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]

CABECERA = """<!doctype html>
<html lang="es">
\t<head>
\t\t<meta charset="UTF-8" />
\t\t<link rel="icon" type="image/svg+xml" href="/favicon.svg" />
\t\t<meta name="viewport" content="width=device-width, initial-scale=1.0" />
\t\t<title>{titulo}</title>

\t\t<link rel="preconnect" href="https://fonts.googleapis.com" />
\t\t<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
\t\t<link
\t\t\thref="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap"
\t\t\trel="stylesheet"
\t\t/>
\t\t<link rel="stylesheet" href="../../css/base.css" />
\t</head>
\t<body data-deck-total="{total}">
\t\t<main class="{clases}">
{contenido}
{nav}
\t\t</main>
{scripts}
\t\t<script type="module" src="../../js/deck.js"></script>
\t</body>
</html>
"""

ENLACE_ANT = """\t\t\t\t<a class="slide-nav__link" href="{href}">
\t\t\t\t\t<svg class="icon" aria-hidden="true"><use href="/course-icons.svg#{icono}" /></svg>
\t\t\t\t\t<span>{rotulo}</span>
\t\t\t\t</a>"""

ENLACE_SIG = """\t\t\t\t<a class="slide-nav__link" href="{href}">
\t\t\t\t\t<span>{rotulo}</span>
\t\t\t\t\t<svg class="icon" aria-hidden="true"><use href="/course-icons.svg#{icono}" /></svg>
\t\t\t\t</a>"""


def nombre(indice: int, slug: str) -> str:
    return f"{indice + 1:02d}-{slug}.html"


def bloque_nav(laminas: list[dict], i: int) -> str:
    partes = ['\t\t\t<nav class="slide-nav" aria-label="Navegación de la diapositiva">']
    if i > 0:
        prev = laminas[i - 1]
        partes.append(
            ENLACE_ANT.format(
                href=nombre(i - 1, prev["slug"]),
                rotulo=prev.get("nav", prev["titulo"]),
                icono=prev.get("icono", "i-flow"),
            )
        )
    else:
        # La portada no tiene lámina anterior; el hueco mantiene la
        # distribución de la tira, que es un grid de dos columnas.
        partes.append("\t\t\t\t<span></span>")
    if i < len(laminas) - 1:
        sig = laminas[i + 1]
        partes.append(
            ENLACE_SIG.format(
                href=nombre(i + 1, sig["slug"]),
                rotulo=sig.get("nav", sig["titulo"]),
                icono=sig.get("icono", "i-flow"),
            )
        )
    else:
        partes.append("\t\t\t\t<span></span>")
    partes.append("\t\t\t</nav>")
    return "\n".join(partes)


# Etiqueta de Wokwi → módulo que la define. La lista es explícita y no se
# deriva del nombre: `wokwi-esp32-devkit-v1` vive en `esp32-devkit-v1-element`,
# sin el prefijo, y adivinarlo produciría un import roto que solo se nota al
# proyectar.
MODULOS_WOKWI = {
    "wokwi-esp32-devkit-v1": "esp32-devkit-v1-element",
    "wokwi-led": "led-element",
    "wokwi-resistor": "resistor-element",
    "wokwi-pushbutton": "pushbutton-element",
    "wokwi-potentiometer": "potentiometer-element",
    "wokwi-ssd1306": "ssd1306-element",
    "wokwi-dht22": "dht22-element",
    "wokwi-buzzer": "buzzer-element",
    "wokwi-servo": "servo-element",
    "wokwi-slide-switch": "slide-switch-element",
}


def importes_wokwi(contenido: str, scripts: str) -> str:
    """Añade el import de cada componente de Wokwi que la lámina usa.

    Un componente sin su import no falla: simplemente no dibuja nada, y la
    lámina sale con un hueco donde debería estar el montaje. Eso ya ocurrió, y
    el arreglo de entonces fue sustituir la placa por una etiqueta de texto —
    curar el síntoma. Derivándolo del contenido, la clase de fallo desaparece:
    quien escribe la lámina no tiene que acordarse de nada.
    """
    faltan = [
        MODULOS_WOKWI[etiqueta]
        for etiqueta in MODULOS_WOKWI
        if f"<{etiqueta}" in contenido and MODULOS_WOKWI[etiqueta] not in scripts
    ]
    if not faltan:
        return scripts
    lineas = "\n".join(
        f'\t\t\timport "@wokwi/elements/dist/esm/{m}.js";' for m in sorted(faltan)
    )
    bloque = f'\t\t<script type="module">\n{lineas}\n\t\t</script>\n'
    return scripts + bloque if scripts else bloque


def generar_desde(m: dict, seco: bool = False) -> int:
    """Emite las láminas de un manifiesto ya cargado en memoria.

    Los guiones de cada sesión llaman aquí en vez de escribir un JSON
    intermedio: el contenido es HTML, y en Python cabe en cadenas triples
    legibles, mientras que en JSON habría que escapar cada comilla.
    """
    laminas = m["laminas"]
    total = len(laminas)
    destino = RAIZ / "src" / "slides" / m["clase"]
    destino.mkdir(parents=True, exist_ok=True)

    escritos: set[str] = set()
    for i, lam in enumerate(laminas):
        contenido = lam["contenido"].rstrip("\n")
        html = CABECERA.format(
            titulo=lam["titulo"],
            total=total,
            clases=lam.get("clases", "slide slide--start"),
            contenido=contenido,
            nav=bloque_nav(laminas, i),
            scripts=importes_wokwi(contenido, lam.get("scripts", "")),
        )
        archivo = destino / nombre(i, lam["slug"])
        escritos.add(archivo.name)
        if seco:
            print(f"  · {archivo.relative_to(RAIZ)}")
        else:
            archivo.write_text(html)

    # Un slug que cambia deja atrás el archivo con el nombre viejo, y ese
    # fantasma no molesta a nadie hasta que se cuentan las láminas: el mazo
    # pasó a declarar 324 donde hay 322, y el verificador de títulos empezó a
    # ver duplicados que no existían. Se borra lo que esta pasada no ha
    # escrito, y se dice cuál para que el borrado nunca sea silencioso.
    sobrantes = sorted(
        f for f in destino.glob("*.html") if f.name not in escritos
    )
    for f in sobrantes:
        print(f"  {'(simulado) ' if seco else ''}sobra y se elimina: {f.name}")
        if not seco:
            f.unlink()

    print(f"{'(simulado) ' if seco else ''}{total} láminas en {destino.relative_to(RAIZ)}")
    return total


def generar(ruta_manifiesto: Path, seco: bool) -> int:
    return generar_desde(json.loads(ruta_manifiesto.read_text()), seco)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    generar(Path(sys.argv[1]), "--dry" in sys.argv)
