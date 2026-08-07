#!/usr/bin/env python3
"""Aplica la tabla de tools/terminologia.py a la fuente del curso.

Tres sitios, con reglas distintas en cada uno:

  · CUERPO — el término del campo, y la glosa en español SOLO en su primera
    aparición dentro de cada sesión. Repetirla en cada mención es exactamente
    la sobrecarga que se quiere evitar.

  · TÍTULOS — el término a secas, nunca con paréntesis. Un título es un rótulo;
    una aclaración entre paréntesis dentro de él lo convierte en una frase. Por
    eso la glosa solo se inserta dentro de un párrafo o de un elemento de lista.

  · GLOSARIO — la entrada pasa a encabezarse con el término del campo y la
    aclaración va en el segundo renglón, que la hoja de estilo dibuja entre
    paréntesis. Sin glosa no se deja segundo renglón: «Timestamp (timestamp)»
    no aclara nada.

EL ORDEN IMPORTA, y costó una pasada equivocada averiguarlo. En las sesiones
5-12 el glosario vive DENTRO del mismo archivo generador que el cuerpo, así que
si el glosario se escribe primero, el paso del cuerpo encuentra la glosa recién
puesta —«memoria no volátil»— y la sustituye por el término nuevo, dejando
«NVS (NVS)». Con el cuerpo primero y el glosario después, buscando ya por el
nombre NUEVO, el problema desaparece sin necesidad de proteger nada.

Uso:  python3 tools/aplicar-terminos.py [--ensayo]
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from terminologia import FLIPS  # noqa: E402

RAIZ = Path(__file__).resolve().parents[1]
SLIDES = RAIZ / "src" / "slides"
GENERADORES = RAIZ / "tools" / "clases"
A_MANO = {"clase-01", "clase-02", "clase-03", "clase-04"}

ensayo = "--ensayo" in sys.argv
cuenta = {"cuerpo": 0, "glosa": 0, "glosario": 0}


def escribir(f: Path, s: str) -> None:
    if not ensayo:
        f.write_text(s)


def minuscula(termino: str) -> str:
    """Forma del término a mitad de frase.

    Un acrónimo no se escribe en minúscula: `NVS`, `OTA`, `ISR` y `QoS` se leen
    igual al principio y en medio de una oración, y bajarles la primera letra
    producía «nVS» y «oTA». Se reconocen por llevar dos o más mayúsculas.
    """
    if sum(1 for c in termino if c.isupper()) >= 2:
        return termino
    return termino[0].lower() + termino[1:]


# La glosa solo entra aquí dentro: nunca en un <title> ni en un <h1>.
CUERPO = re.compile(r"<(p|li)\b[^>]*>.*?</\1>", re.S)


def cambiar(texto: str, viejo: str, nuevo: str) -> tuple[str, int]:
    hechos = 0
    for antes, despues in ((viejo, nuevo), (minuscula(viejo), minuscula(nuevo))):
        if antes == despues:
            continue
        texto, n = re.subn(re.escape(antes), despues, texto)
        hechos += n
    return texto, hechos


def glosar(texto: str, nuevo: str, glosa: str) -> tuple[str, bool]:
    """Pone «(glosa)» tras la primera mención que caiga en un párrafo o lista."""
    for m in CUERPO.finditer(texto):
        bloque = m.group(0)
        for forma in dict.fromkeys((nuevo, minuscula(nuevo))):
            i = bloque.find(forma)
            if i == -1:
                continue
            corte = i + len(forma)
            return (
                texto[: m.start()]
                + bloque[:corte]
                + f" ({glosa})"
                + bloque[corte:]
                + texto[m.end() :],
                True,
            )
    return texto, False


# ── 1 · cuerpo y títulos ───────────────────────────────────────────────────
for clase in sorted({p.name for p in SLIDES.iterdir() if p.is_dir()}):
    glosados: set[str] = set()
    objetivos = (
        sorted(SLIDES.glob(f"{clase}/*.html"))
        if clase in A_MANO
        else [GENERADORES / f"clase_{clase.split('-')[1]}.py"]
    )
    for f in objetivos:
        if not f.exists():
            continue
        # El glosario de las sesiones 1-4 es un archivo aparte y se trata en el
        # paso 2. El de las 5-12 va dentro del generador y también, pero
        # después, por el orden que explica la cabecera.
        if "glosario" in f.name:
            continue
        s = original = f.read_text()
        for viejo, nuevo, glosa in FLIPS:
            s, n = cambiar(s, viejo, nuevo)
            cuenta["cuerpo"] += n
            if n and glosa and nuevo not in glosados:
                s, puesta = glosar(s, nuevo, glosa)
                if puesta:
                    glosados.add(nuevo)
                    cuenta["glosa"] += 1
        if s != original:
            escribir(f, s)

# ── 2 · glosario ───────────────────────────────────────────────────────────
SPAN = '<span class="glossary-item__alt">'

for viejo, nuevo, glosa in FLIPS:
    for f in sorted(SLIDES.glob("clase-0[1-4]/*glosario*.html")):
        s = f.read_text()
        patron = re.compile(
            r"(<summary>\s*)"
            + re.escape(viejo)
            + r"\s*"
            + re.escape(SPAN)
            + r"[^<]*</span>"
        )
        reemplazo = (
            f"\\1{nuevo}\n\t\t\t\t\t\t\t{SPAN}{glosa}</span>"
            if glosa
            else f"\\1{nuevo}"
        )
        s2, n = patron.subn(reemplazo, s)
        if n:
            escribir(f, s2)
            cuenta["glosario"] += n

    # En los generadores el cuerpo ya cambió el nombre, así que aquí se busca
    # por el término NUEVO y solo se ajusta la glosa.
    for f in sorted(GENERADORES.glob("clase_*.py")):
        s = f.read_text()
        patron = re.compile(
            r'termino\(\s*"(?:'
            + re.escape(viejo)
            + "|"
            + re.escape(nuevo)
            + r')"\s*,\s*"[^"]*"'
        )
        s2, n = patron.subn(f'termino("{nuevo}", "{glosa}"', s)
        if n:
            escribir(f, s2)
            cuenta["glosario"] += n

marca = "(ensayo) " if ensayo else ""
print(f"{marca}apariciones cambiadas en cuerpo y títulos: {cuenta['cuerpo']}")
print(f"{marca}glosas puestas (una por sesión y término):  {cuenta['glosa']}")
print(f"{marca}entradas de glosario reencabezadas:         {cuenta['glosario']}")
