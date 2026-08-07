#!/usr/bin/env python3
"""Control de calidad de las pruebas, con el mismo listón que las láminas.

POR QUÉ EXISTE. Las auditorías del curso recorren `src/slides/**/*.html` y
nada más, así que los archivos de `pruebas/` —el GIFT de Moodle y el script de
Apps Script— nunca pasaron por ningún control. Se notó cuando en un enunciado
apareció una raya en par decorativo, que es de las marcas que más delatan un
texto generado, y que en una lámina se habría detectado el mismo día.

Un test es contenido del curso: lo lee el estudiante, lo lee con más atención
que una lámina porque le va la nota, y se conserva de un año para otro. No hay
razón para medirlo con un listón más bajo.

QUÉ REVISA

  · raya en par decorativo, prohibida por la skill human-academic-writing;
  · coloquialismos de la lista cerrada del curso;
  · nombres de pregunta interrogativos o con verbo conjugado — un nombre es un
    rótulo, y sigue la misma regla que un título de lámina;
  · comillas rectas donde deberían ir angulares;
  · unidades pegadas a la cifra;
  · que las dos versiones cubran los mismos términos, que es lo que hace que
    la práctica sirva de práctica.

Uso:  python3 tools/audit-pruebas.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
PRUEBAS = RAIZ / "pruebas"

# Lista cerrada, como la del resto del curso: no se amplía por intuición.
COLOQUIALISMOS = [
    "de verdad", "a secas", "al revés", "por fuera", "un montón",
    "sin más", "de golpe", "a lo tonto", "en plan", "cosa que",
    "lo dice sin rodeos", "se cae", "arranca bien",
]

VERBOS_EN_ROTULO = re.compile(
    r"\b(es|son|está|están|tiene|tienen|hace|hacen|vive|viven|"
    r"permite|permiten|cuántas|cuántos|cómo|dónde|qué|cuál|cuáles)\b",
    re.IGNORECASE,
)


def texto_visible_gift(s: str) -> str:
    """Enunciados y retroalimentación; fuera los comentarios y la sintaxis."""
    sin_comentarios = "\n".join(
        l for l in s.splitlines() if not l.lstrip().startswith("//")
    )
    return re.sub(r"\\([~=#{}])", r"\1", sin_comentarios)


def nombres_gift(s: str) -> list[str]:
    return re.findall(r"^::(.+?)::", s, re.MULTILINE)


def textos_script(s: str) -> list[str]:
    """Todo lo que el formulario muestra: título, descripción y preguntas.

    Se leen las cadenas del literal PREGUNTAS en vez de ejecutar el archivo:
    aquí no hay un motor de JavaScript, y para lo que se comprueba basta con
    el texto entre comillas.
    """
    salida = []
    m = re.search(r"const PREGUNTAS = \[(.*?)\n\];", s, re.S)
    cuerpo = m.group(1) if m else ""
    for campo in ("titulo", "explicacion"):
        salida += re.findall(campo + r':\s*\n?\s*"((?:[^"\\]|\\.)*)"', cuerpo)
    salida += re.findall(r'\["((?:[^"\\]|\\.)*)",\s*(?:true|false)\]', cuerpo)
    t = re.search(r'const TITULO = "([^"]*)"', s)
    if t:
        salida.append(t.group(1))
    d = re.search(r"const DESCRIPCION = \[(.*?)\]\.join", s, re.S)
    if d:
        salida += re.findall(r'"([^"]*)"', d.group(1))
    return salida


def revisar(gift_p: Path, script_p: Path) -> int:
    """Audita un test. Devuelve cuántos problemas encontró."""
    fallos: dict[str, list[str]] = {}

    def anotar(clave: str, detalle: str) -> None:
        fallos.setdefault(clave, []).append(detalle)

    gift = gift_p.read_text()
    script = script_p.read_text()

    visibles = [texto_visible_gift(gift)] + textos_script(script)

    for t in visibles:
        for m in re.finditer(r"—[^—]{2,120}—", t):
            anotar("raya en par decorativo", f"«{m.group(0)[:60]}…»")
        for c in COLOQUIALISMOS:
            for m in re.finditer(r"\b" + re.escape(c) + r"\b", t, re.I):
                ctx = t[max(0, m.start() - 30) : m.end() + 25].replace("\n", " ")
                anotar("coloquialismo", f"«{c}» en …{ctx.strip()}…")
        n = len(re.findall(r'(?<![=<>/:,\[ ])"[A-Za-zÁÉÍÓÚÑáéíóúñ¿¡]', t))
        if n:
            anotar("comillas rectas", f"{n} en un texto visible")
        for m in re.finditer(
            r"\b\d+(?:[.,]\d+)?(ms|us|µs|kHz|MHz|Hz|mV|V|mA|kB|KB|MB|Ω|bits?)\b", t
        ):
            anotar("unidad pegada a la cifra", f"«{m.group(0)}»")

    # Los nombres de pregunta son rótulos: frase nominal, sin interrogación.
    for nombre in nombres_gift(gift):
        etiqueta = re.sub(r"^S\d-\d+\s*", "", nombre)
        if "?" in nombre or "¿" in nombre:
            anotar("nombre de pregunta interrogativo", f"«{nombre}»")
        elif VERBOS_EN_ROTULO.search(etiqueta):
            anotar("nombre de pregunta con verbo o pronombre interrogativo",
                   f"«{nombre}»")

    # Paridad: la práctica solo sirve si cubre lo mismo que la evaluación.
    n_gift = len(nombres_gift(gift))
    n_form = len(re.findall(r'tipo:\s*"', script))
    if n_gift != n_form:
        anotar("las dos versiones no tienen el mismo número de preguntas",
               f"GIFT {n_gift} · formulario {n_form}")

    total = sum(len(v) for v in fallos.values())
    print(f"{gift_p.name} y {script_p.name} · {n_gift} preguntas · "
          f"{'sin problemas' if not total else str(total) + ' problemas'}")
    for clave, casos in sorted(fallos.items(), key=lambda kv: -len(kv[1])):
        print(f"  ### {clave}  ({len(casos)})")
        for c in casos[:12]:
            print(f"      {c}")
        if len(casos) > 12:
            print(f"      … y {len(casos) - 12} más")
    return total


def main() -> None:
    """Recorre TODOS los tests de pruebas/.

    Antes cogía el primer .gift que encontrara. Con un solo test funcionaba, y
    al añadir el segundo lo habría dejado sin auditar en silencio: exactamente
    el hueco que hizo falta esta herramienta.
    """
    tests = sorted(PRUEBAS.glob("test-*.gift"))
    if not tests:
        sys.exit("no hay ningún test-*.gift en pruebas/")

    total = 0
    for gift_p in tests:
        script_p = gift_p.with_name(gift_p.stem + "-apps-script.gs")
        if not script_p.exists():
            print(f"{gift_p.name}: falta su {script_p.name}")
            total += 1
            continue
        total += revisar(gift_p, script_p)

    print(f"\n{len(tests)} tests revisados · {total} problemas")
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
