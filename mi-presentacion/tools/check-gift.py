#!/usr/bin/env python3
"""Comprueba un archivo GIFT antes de subirlo a Moodle.

Moodle rechaza el archivo entero cuando una sola pregunta está mal formada, y
el mensaje que da nombra la línea pero no el motivo. Este comprobador dice qué
falla y por qué, que es lo que hace falta para arreglarlo.

Lo que revisa:

  · llaves sin cerrar, o cerradas sin abrir;
  · caracteres especiales sin escapar en el enunciado —en GIFT, `~ = # { }`
    llevan barra invertida cuando forman parte del texto, y olvidarlo es el
    fallo que más veces rompe una importación;
  · preguntas sin bloque de respuesta;
  · opción múltiple sin respuesta correcta, o con más de una;
  · emparejamientos cuyas parejas no llevan `->`;
  · verdadero/falso con un valor que no es TRUE, FALSE, T ni F;
  · respuesta corta sin ninguna alternativa aceptada;
  · opción múltiple con varias correctas cuyos pesos positivos no suman 100 %.

Uso:  python3 tools/check-gift.py pruebas/test-01.gift
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ESPECIALES = "~=#{}"


def sin_comentarios(texto: str) -> list[tuple[int, str]]:
    """Líneas numeradas, fuera las de comentario y las vacías del principio."""
    salida = []
    for n, linea in enumerate(texto.splitlines(), 1):
        if linea.lstrip().startswith("//"):
            continue
        salida.append((n, linea))
    return salida


def separar_preguntas(lineas: list[tuple[int, str]]) -> list[tuple[int, str]]:
    """Trocea por líneas en blanco. Devuelve (línea inicial, texto)."""
    preguntas, actual, inicio = [], [], None
    for n, linea in lineas:
        if linea.strip() == "":
            if actual:
                preguntas.append((inicio, "\n".join(actual)))
                actual, inicio = [], None
            continue
        if linea.startswith("$CATEGORY:"):
            continue
        if inicio is None:
            inicio = n
        actual.append(linea)
    if actual:
        preguntas.append((inicio, "\n".join(actual)))
    return preguntas


def trozos(pregunta: str) -> tuple[list[str], list[str]]:
    """Separa lo que está FUERA de las llaves de lo que está dentro.

    Hace falta porque las reglas de escapado son distintas a cada lado: dentro
    del bloque de respuestas, `=` y `~` son sintaxis y no se escapan.
    """
    fuera, dentro, buffer, nivel = [], [], "", 0
    i = 0
    while i < len(pregunta):
        c = pregunta[i]
        if c == "\\" and i + 1 < len(pregunta):
            buffer += pregunta[i : i + 2]
            i += 2
            continue
        if c == "{":
            if nivel == 0:
                fuera.append(buffer)
                buffer = ""
            else:
                buffer += c
            nivel += 1
        elif c == "}":
            nivel -= 1
            if nivel == 0:
                dentro.append(buffer)
                buffer = ""
            else:
                buffer += c
        else:
            buffer += c
        i += 1
    if nivel != 0:
        raise ValueError(f"llaves sin equilibrar (quedan {nivel} sin cerrar)")
    fuera.append(buffer)
    return fuera, dentro


def nombre_de(pregunta: str) -> str:
    m = re.match(r"\s*::(.*?)::", pregunta, re.S)
    return m.group(1).strip() if m else "(sin nombre)"


def revisar_enunciado(fuera: list[str]) -> list[str]:
    fallos = []
    for parte in fuera:
        # el nombre entre :: :: es sintaxis, no enunciado
        cuerpo = re.sub(r"^\s*::.*?::", "", parte, count=1, flags=re.S)
        for i, c in enumerate(cuerpo):
            if c not in ESPECIALES:
                continue
            if i > 0 and cuerpo[i - 1] == "\\":
                continue
            contexto = cuerpo[max(0, i - 30) : i + 30].replace("\n", " ").strip()
            fallos.append(f"«{c}» sin escapar en el enunciado: …{contexto}…")
    return fallos


def revisar_respuestas(bloque: str) -> list[str]:
    fallos = []
    limpio = bloque.strip()
    if not limpio:
        return ["bloque de respuestas vacío"]

    if re.fullmatch(r"(TRUE|FALSE|T|F)\b.*", limpio, re.S | re.I):
        return fallos
    if re.match(r"^(VERDADERO|FALSO)", limpio, re.I):
        return ["verdadero/falso debe escribirse TRUE o FALSE, no en español"]

    # se descarta la retroalimentación general antes de contar alternativas
    cuerpo = re.split(r"####", limpio)[0]
    correctas = re.findall(r"(?<!\\)=", cuerpo)
    distractores = re.findall(r"(?<!\\)~", cuerpo)

    if "->" in cuerpo:
        for linea in cuerpo.splitlines():
            t = linea.strip()
            if t and not t.startswith("#") and "->" not in t:
                fallos.append(f"pareja de emparejamiento sin «->»: {t}")
        if len(correctas) < 2:
            fallos.append("un emparejamiento necesita al menos dos parejas")
        return fallos

    # Opción múltiple con varias correctas: cada alternativa lleva su peso,
    # «~%50%» si suma y «~%-50%» si resta, y no hay ningún «=».
    pesos = [float(p) for p in re.findall(r"(?<!\\)~%(-?\d+(?:[.,]\d+)?)%", cuerpo)]
    if pesos and not correctas:
        positivos = sum(p for p in pesos if p > 0)
        if abs(positivos - 100) > 0.01:
            fallos.append(f"los pesos positivos suman {positivos:g} %, no 100 %")
        return fallos

    if not correctas:
        fallos.append("no hay ninguna respuesta correcta (falta «=»)")
    elif distractores and len(correctas) > 1:
        fallos.append(
            f"opción múltiple con {len(correctas)} respuestas marcadas correctas"
        )
    return fallos


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit("uso: python3 tools/check-gift.py archivo.gift")
    ruta = Path(sys.argv[1])
    lineas = sin_comentarios(ruta.read_text())
    preguntas = separar_preguntas(lineas)

    total_fallos = 0
    tipos: dict[str, int] = {}
    for inicio, texto in preguntas:
        etiqueta = f"{ruta.name}:{inicio}  {nombre_de(texto)}"
        try:
            fuera, dentro = trozos(texto)
        except ValueError as e:
            print(f"  ✗ {etiqueta}\n      {e}")
            total_fallos += 1
            continue

        fallos = revisar_enunciado(fuera)
        if not dentro:
            fallos.append("la pregunta no tiene bloque de respuestas")
        for bloque in dentro:
            fallos += revisar_respuestas(bloque)

        if fallos:
            print(f"  ✗ {etiqueta}")
            for f in fallos:
                print(f"      {f}")
            total_fallos += len(fallos)
        else:
            t = clasificar(fuera, dentro)
            tipos[t] = tipos.get(t, 0) + 1

    print(f"\n{len(preguntas)} preguntas · {total_fallos} problemas")
    if tipos:
        print("Por tipo:")
        for t, n in sorted(tipos.items()):
            print(f"  {n:>3}  {t}")
    sys.exit(1 if total_fallos else 0)


def clasificar(fuera: list[str], dentro: list[str]) -> str:
    bloque = " ".join(dentro)
    cuerpo = re.split(r"####", bloque)[0]
    if re.match(r"\s*(TRUE|FALSE|T|F)\b", bloque, re.I):
        return "verdadero/falso"
    if "->" in cuerpo:
        return "emparejamiento"
    # Si el enunciado SIGUE después del bloque de respuestas, el hueco está
    # embebido en la frase: eso es una pregunta de palabra faltante, aunque su
    # sintaxis interna sea la de una opción múltiple.
    embebida = len(fuera) > 1 and fuera[-1].strip() != ""
    if re.search(r"(?<!\\)~%\d", cuerpo) and not re.search(r"(?<!\\)=", cuerpo):
        return "opción múltiple (varias correctas)"
    if re.search(r"(?<!\\)~", cuerpo):
        return "palabra faltante" if embebida else "opción múltiple"
    return "respuesta corta"


if __name__ == "__main__":
    main()
