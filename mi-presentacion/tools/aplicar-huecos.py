#!/usr/bin/env python3
"""Aplica a la FUENTE el plan de reparto que produjo proponer-stretch.mjs.

Dos fuentes distintas, y por eso dos caminos:

  · sesiones 1-4  — el HTML de src/slides ES la fuente, se edita ahí;
  · sesiones 5-12 — el HTML lo escribe tools/clases/clase_NN.py, así que
    editarlo se perdería en la siguiente regeneración. Se edita el generador.

El bloque se localiza por sus clases, nunca por su posición: en el generador
`cabecera()` emite dos hijos —la insignia y el título— que en el archivo no se
ven, de modo que el índice que da el navegador no coincide con el del código.
Si las clases no identifican un único bloque, la lámina se salta y se informa;
mejor dejarla a mano que acertar por casualidad.

Uso:  python3 tools/aplicar-huecos.py plan.json [--ensayo]
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
SLIDES = RAIZ / "src" / "slides"
GENERADORES = RAIZ / "tools" / "clases"

# Las sesiones cuyo HTML se escribe a mano. El resto se genera.
A_MANO = {"clase-01", "clase-02", "clase-03", "clase-04"}


class NoAplicable(Exception):
    """La localización no es inequívoca; la lámina queda para revisión."""


# Marcas que este script pone. Los patrones de localización las admiten a
# ambos lados del juego de clases identificador, por dos razones distintas:
# detrás, para que una segunda pasada reconozca su propio trabajo; delante,
# porque las diez láminas que se marcaron a mano en la sesión 1 las llevan
# escritas ahí —«class="is-stretch slide__split"»— y son fuente igual de válida.
MARCAS = ("is-stretch", "is-spread")
_DETRAS = "".join(f"(?: {m})?" for m in MARCAS)
_DELANTE = "".join(f"(?:{m} )?" for m in MARCAS)


def _añadir_clase(linea: str, clase: str) -> str:
    """Añade una clase al FINAL del atributo class de una etiqueta.

    Al final y no al principio: puesta delante desplazaría la clase que
    identifica al bloque y los patrones de localización dejarían de
    reconocerlo, que es lo que hacía fallar la segunda pasada."""
    if clase in linea:
        return linea  # ya aplicada: la operación es idempotente
    return re.sub(r'class="([^"]*)"', rf'class="\1 {clase}"', linea, count=1)


def _localizar(lineas: list[str], patron: re.Pattern, ordinal: int) -> int:
    """Índice de la línea que hace de ordinal-ésima coincidencia."""
    hallados = [i for i, l in enumerate(lineas) if patron.search(l)]
    if not hallados:
        raise NoAplicable("no se encuentra el bloque en la fuente")
    if ordinal >= len(hallados):
        raise NoAplicable(
            f"el bloque aparece {len(hallados)} vez/veces y se pedía la número {ordinal + 1}"
        )
    return hallados[ordinal]


def _patron_bloque(seña: dict, tabs: str) -> re.Pattern:
    """Etiqueta de apertura con EXACTAMENTE ese juego de clases, al nivel de
    hijo directo de .slide__content. El anclaje a la indentación evita
    confundirlo con un bloque homónimo anidado más adentro.

    Dos formas, porque el formateador parte las etiquetas largas: el atributo
    puede ir en la misma línea que la etiqueta o en la siguiente, un tabulador
    más adentro. La segunda es la de los glosarios, cuya lista de clases de
    utilidad no cabe en una línea."""
    clases = f'{_DELANTE}{re.escape(seña["clases"])}{_DETRAS}'
    return re.compile(
        f'^{tabs}<{seña["etiqueta"]} class="{clases}"'
        f'|^{tabs}\t?class="{clases}"'
    )


def aplicar_html(ruta: Path, entrada: dict) -> list[str]:
    texto = ruta.read_text()
    lineas = texto.split("\n")
    hechos = []

    if entrada.get("estirar"):
        i = _localizar(lineas, _patron_bloque(entrada["estirar"], "\t{4}"),
                       entrada["estirar"]["ordinal"])
        lineas[i] = _añadir_clase(lineas[i], "is-stretch")
        hechos.append("is-stretch")

    if "lamina" in entrada["repartir"]:
        i = _localizar(lineas, re.compile(r'^\t{3}<div class="slide__content[^"]*"'), 0)
        lineas[i] = _añadir_clase(lineas[i], "is-spread")
        hechos.append("is-spread en la lámina")

    if "columna" in entrada["repartir"]:
        i = _localizar(lineas, re.compile(rf'^\t{{5}}<div class="slide__split-text{_DETRAS}"'), 0)
        lineas[i] = _añadir_clase(lineas[i], "is-spread")
        hechos.append("is-spread en la columna")

    ruta.write_text("\n".join(lineas))
    return hechos


def _bloque_lamina(fuente: str, slug: str) -> tuple[int, int]:
    """Rango [inicio, fin) del texto de la llamada lamina() de ese slug."""
    marca = f'lamina(\n    "{slug}",\n'
    inicio = fuente.find(marca)
    if inicio == -1:
        raise NoAplicable(f"no hay una llamada lamina() para «{slug}»")
    # Las llamadas cierran con «)» en la columna 0; ese es el final del bloque.
    fin = fuente.find("\n)\n", inicio)
    if fin == -1:
        raise NoAplicable("no se encuentra el cierre de la llamada lamina()")
    return inicio, fin + 3


def aplicar_generador(ruta: Path, slug: str, entrada: dict) -> list[str]:
    fuente = ruta.read_text()
    ini, fin = _bloque_lamina(fuente, slug)
    bloque = fuente[ini:fin]
    lineas = bloque.split("\n")
    hechos = []

    # En el generador la indentación son los DOS CARACTERES \t, no tabuladores.
    if entrada.get("estirar"):
        i = _localizar(lineas, _patron_bloque(entrada["estirar"], r"(?:\\t){4}"),
                       entrada["estirar"]["ordinal"])
        lineas[i] = _añadir_clase(lineas[i], "is-stretch")
        hechos.append("is-stretch")

    if "columna" in entrada["repartir"]:
        i = _localizar(
            lineas, re.compile(rf'^(?:\\t){{5}}<div class="slide__split-text{_DETRAS}"'), 0
        )
        lineas[i] = _añadir_clase(lineas[i], "is-spread")
        hechos.append("is-spread en la columna")

    bloque = "\n".join(lineas)

    # `.slide__content` lo emite envolver(); la clase se pasa como segundo
    # argumento. ESPARCIDO vive en comun.py para que no haya doce copias de la
    # misma cadena repartidas por los generadores.
    if "lamina" in entrada["repartir"]:
        if "ESPARCIDO" not in bloque:
            n = bloque.count('"""),')
            if n != 1:
                raise NoAplicable(
                    f"se esperaba un único cierre de envolver() y hay {n}"
                )
            bloque = bloque.replace('"""),', '""", ESPARCIDO),')
            hechos.append("is-spread en la lámina")

    fuente = fuente[:ini] + bloque + fuente[fin:]

    # Sin el import el generador falla con NameError en la regeneración, que es
    # un error tardío y confuso; se resuelve aquí mismo.
    if "ESPARCIDO" in fuente:
        fuente = _asegurar_import(fuente)

    ruta.write_text(fuente)
    return hechos


def _asegurar_import(fuente: str) -> str:
    """Añade ESPARCIDO a la línea `from comun import ...`, en orden."""
    patron = re.compile(r"^from comun import (.+)$", re.MULTILINE)
    m = patron.search(fuente)
    if not m:
        raise NoAplicable("no hay una línea «from comun import» que ampliar")
    nombres = [n.strip() for n in m.group(1).split(",")]
    if "ESPARCIDO" in nombres:
        return fuente
    # Las mayúsculas primero, como es costumbre para las constantes.
    nombres = ["ESPARCIDO"] + nombres
    return patron.sub(f"from comun import {', '.join(nombres)}", fuente, count=1)


def main() -> None:
    argumentos = sys.argv[1:]
    ensayo = "--ensayo" in argumentos
    ruta_plan = next(a for a in argumentos if not a.startswith("--"))
    datos = json.loads(Path(ruta_plan).read_text())

    aplicadas, saltadas = [], []
    generadores_tocados = set()

    for entrada in datos["plan"]:
        clase, archivo = entrada["lamina"].split("/")
        slug = re.sub(r"^\d+-", "", archivo).removesuffix(".html")
        try:
            if clase in A_MANO:
                destino = SLIDES / clase / archivo
                hechos = ["(ensayo)"] if ensayo else aplicar_html(destino, entrada)
            else:
                destino = GENERADORES / f"clase_{clase.split('-')[1]}.py"
                hechos = (
                    ["(ensayo)"]
                    if ensayo
                    else aplicar_generador(destino, slug, entrada)
                )
                generadores_tocados.add(destino.name)
            aplicadas.append((entrada, destino, hechos))
        except NoAplicable as e:
            saltadas.append((entrada, str(e)))

    print(f"Aplicadas: {len(aplicadas)}")
    for entrada, destino, hechos in aplicadas:
        print(
            f"  {entrada['antes']:>4} → {entrada['despues']:>3} px  "
            f"{entrada['lamina']}  [{', '.join(hechos)}]"
        )

    if saltadas:
        print(f"\nSaltadas ({len(saltadas)}) — requieren revisión a mano:")
        for entrada, motivo in saltadas:
            print(f"  {entrada['lamina']}: {motivo}")

    if generadores_tocados and not ensayo:
        print("\nRegenerar:")
        for g in sorted(generadores_tocados):
            print(f"  python3 tools/clases/{g}")


if __name__ == "__main__":
    main()
