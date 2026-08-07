#!/usr/bin/env python3
"""Descarga el PDF de acceso abierto de un artículo a src/paper/clase-NN/.

Se apoya en Unpaywall (api.unpaywall.org) para resolver un DOI a la mejor
copia legalmente accesible, porque la dirección del PDF no es deducible del
DOI y varía según la editorial y el repositorio que lo aloje.

Verifica que lo recibido sea realmente un PDF: varias editoriales responden
200 con una página de bloqueo, y un archivo HTML con extensión .pdf pasa
inadvertido hasta que alguien intenta abrirlo.

Uso:
  python3 tools/get-paper.py clase-02 10.1186/s13174-024-00181-w  nombre-corto
  python3 tools/get-paper.py clase-03 https://arxiv.org/abs/2501.01234 nombre-corto
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urljoin, urlparse

RAIZ = Path(__file__).resolve().parents[1]
CORREO = "infinity.witss@gmail.com"

# Sin una cabecera de navegador creíble, varias editoriales devuelven una
# página de bloqueo en vez del archivo.
CABECERAS = [
    "-A",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "-H",
    "Accept: application/pdf,text/html,*/*",
    "-H",
    "Accept-Language: es-ES,es;q=0.9,en;q=0.8",
]


def curl(url: str, destino: Path | None = None) -> bytes:
    orden = ["curl", "-sL", "--max-time", "90", *CABECERAS]
    if destino:
        orden += ["-o", str(destino)]
    orden.append(url)
    salida = subprocess.run(orden, capture_output=True, timeout=120)
    return salida.stdout


def via_europepmc(doi: str) -> list[str]:
    """Copia depositada en Europe PMC, si existe.

    Es la vía que rescata buena parte del catálogo de MDPI: su propio sitio
    responde 403 a cualquier descarga automatizada, pero muchos de sus
    artículos biomédicos y de sensores están depositados en PMC, que sí
    entrega el archivo.
    """
    consulta = (
        "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
        f"?query=DOI:%22{doi}%22&resultType=core&format=json"
    )
    try:
        datos = json.loads(curl(consulta))
        resultados = datos["resultList"]["result"]
    except (json.JSONDecodeError, KeyError, IndexError):
        return []
    urls = []
    for r in resultados:
        pmcid = r.get("pmcid")
        if pmcid:
            urls.append(f"https://europepmc.org/articles/{pmcid}?pdf=render")
        for u in (r.get("fullTextUrlList") or {}).get("fullTextUrl", []):
            if u.get("documentStyle") == "pdf" and "mdpi.com" not in u.get("url", ""):
                urls.append(u["url"])
    return urls


def candidatos(referencia: str) -> list[str]:
    """Direcciones de PDF a probar, en orden de preferencia."""
    ref = referencia.strip()

    # arXiv: la dirección del PDF es directa y siempre accesible.
    m = re.search(r"arxiv\.org/(?:abs|pdf)/([\d.]+v?\d*)", ref) or re.fullmatch(
        r"arxiv:([\d.]+v?\d*)", ref, re.I
    )
    if m:
        return [f"https://arxiv.org/pdf/{m.group(1)}"]

    if ref.startswith("http"):
        return [ref]

    # DOI: se pregunta a Unpaywall por todas las copias abiertas conocidas y
    # se prueban de la más fiable a la menos.
    datos = curl(f"https://api.unpaywall.org/v2/{ref}?email={CORREO}")
    try:
        d = json.loads(datos)
    except json.JSONDecodeError:
        return []
    if not d.get("is_oa"):
        print(f"  ! Unpaywall no lo declara de acceso abierto: {ref}")
        return []

    # Europe PMC primero: es el que sortea el bloqueo de las editoriales.
    urls, vistos = list(via_europepmc(ref)), set()
    localizaciones = d.get("oa_locations") or []
    # Los repositorios institucionales rara vez bloquean; las editoriales sí.
    localizaciones.sort(key=lambda x: 0 if x.get("host_type") == "repository" else 1)
    for loc in localizaciones:
        for clave in ("url_for_pdf", "url"):
            u = loc.get(clave)
            if u and u not in vistos:
                vistos.add(u)
                urls.append(u)
    return urls


def enlace_incrustado(html: bytes, base: str) -> str | None:
    """Extrae el enlace real al PDF de una página que solo lo envuelve.

    Muchas revistas con OJS (y varios repositorios) sirven un visor HTML en
    la dirección que parece la del PDF; el archivo cuelga de otra ruta con un
    identificador más. Sin este salto, la descarga devuelve el visor.

    El orden de los patrones importa: los repositorios DSpace incluyen en su
    plantilla varios PDF institucionales (política del repositorio, guías de
    autoarchivo), así que buscar «el primer .pdf» devuelve uno de esos en vez
    del artículo. Las rutas de descarga van primero por eso.
    """
    texto = html[:400_000].decode("utf-8", "ignore")
    for patron in (
        r'href="([^"]*/article/download/[^"]+)"',
        r'href="([^"]*/bitstream/[^"]+\.pdf[^"]*)"',
        r'href="([^"]*/(?:download|fulltext|content)/[^"]*\.pdf[^"]*)"',
        r'href="([^"]*\.pdf(?:\?[^"]*)?)"',
        r'content="([^"]*\.pdf(?:\?[^"]*)?)"',
    ):
        m = re.search(patron, texto)
        if m:
            # Un href relativo no es descargable tal cual: hay que resolverlo
            # contra la página que lo contiene.
            return urljoin(base, m.group(1).replace("&amp;", "&"))
    return None


def titulo_esperado(referencia: str) -> str | None:
    """Título que Crossref asocia al DOI, para poder contrastarlo."""
    if referencia.startswith("http") or referencia.lower().startswith("arxiv"):
        return None
    try:
        d = json.loads(curl(f"https://api.crossref.org/works/{referencia}"))
        return d["message"]["title"][0]
    except (json.JSONDecodeError, KeyError, IndexError):
        return None


def texto_del_pdf(p: Path) -> str:
    """Texto de las primeras páginas, en minúsculas y sin puntuación.

    Se prefiere `pdftotext` (poppler) porque el extractor de reserva no sabe
    resolver las fuentes con codificación CID que usan varias editoriales, y
    ante ellas devuelve basura: eso hacía rechazar descargas correctas.
    """
    try:
        r = subprocess.run(
            ["pdftotext", "-f", "1", "-l", "2", str(p), "-"],
            capture_output=True,
            timeout=30,
        )
        if r.returncode == 0 and len(r.stdout) > 80:
            return re.sub(r"[^a-z0-9 ]", " ", r.stdout.decode("utf-8", "ignore").lower())
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return _texto_de_reserva(p)


def _texto_de_reserva(p: Path) -> str:
    """Extractor propio, para cuando poppler no está instalado."""
    import zlib

    datos = p.read_bytes()
    trozos = []
    for m in re.finditer(rb"stream\r?\n(.*?)endstream", datos, re.S):
        try:
            d = zlib.decompress(m.group(1))
        except Exception:
            continue
        t = b" ".join(re.findall(rb"\((?:\\.|[^\\()])*\)", d))
        t = re.sub(rb"[()]", b" ", t)
        if t.strip():
            trozos.append(t.decode("latin-1"))
        if len(" ".join(trozos)) > 3000:
            break
    return re.sub(r"[^a-z0-9 ]", " ", " ".join(trozos).lower())


def coincide(esperado: str, p: Path, doi: str = "") -> bool:
    """¿El PDF descargado es el artículo pedido?

    Un DOI mal transcrito devuelve un PDF perfectamente válido de OTRO
    artículo, y el fallo pasa inadvertido hasta que alguien lo abre.

    Se acepta por dos vías. El DOI impreso en la portada es prueba directa y
    basta por sí solo; si no aparece —muchas editoriales no lo imprimen— se
    recurre a contar cuántas palabras largas del título están en el texto.
    Ante la duda se acepta: rechazar una descarga correcta cuesta más que
    dejar pasar una dudosa, que la revisión posterior detecta.
    """
    texto = texto_del_pdf(p)
    if len(texto.strip()) < 80:
        return True  # PDF de imagen o ilegible: no se puede contrastar
    if doi and re.sub(r"[^a-z0-9 ]", " ", doi.lower()).strip() in texto:
        return True
    palabras = [w for w in re.sub(r"[^a-z0-9 ]", " ", esperado.lower()).split() if len(w) > 4]
    if not palabras:
        return True
    aciertos = sum(1 for w in palabras if w in texto)
    return aciertos >= max(2, len(palabras) // 2)


def descargar(clase: str, referencia: str, nombre: str) -> bool:
    # Un argumento mal entrecomillado en el shell llega aquí como
    # «clase-10 10.3390» y crea un árbol de carpetas espurio que solo se
    # descubre al contar los archivos. Se rechaza antes de tocar el disco.
    if not re.fullmatch(r"clase-\d\d", clase):
        print(f"  ✗ nombre de clase no válido: «{clase}» (se espera clase-NN)")
        return False

    carpeta = RAIZ / "src" / "paper" / clase
    carpeta.mkdir(parents=True, exist_ok=True)
    destino = carpeta / f"{nombre}.pdf"

    for url in candidatos(referencia):
        for intento in (url, None):
            if intento is None:
                # Lo recibido era HTML: se busca dentro el enlace verdadero.
                incrustado = enlace_incrustado(curl(url), url)
                if not incrustado:
                    break
                intento = incrustado

            curl(intento, destino)
            if destino.exists() and destino.read_bytes()[:5] == b"%PDF-":
                esperado = titulo_esperado(referencia)
                if esperado and not coincide(esperado, destino, referencia):
                    # Se sigue con la siguiente copia en vez de abandonar: que
                    # una fuente entregue el archivo equivocado no dice nada
                    # de las demás, y suele haber tres o cuatro por artículo.
                    print(f"  · {urlparse(intento).netloc} entregó otro documento")
                    destino.unlink(missing_ok=True)
                    continue
                kb = destino.stat().st_size // 1024
                print(
                    f"  ✓ {destino.relative_to(RAIZ)}  ({kb} KB)  "
                    f"desde {urlparse(intento).netloc}"
                )
                # Se imprime SIEMPRE el título obtenido. La comprobación
                # anterior detecta que el PDF no corresponda al DOI, pero no
                # que el DOI pedido sea el equivocado: un identificador mal
                # transcrito descarga un artículo válido y ajeno, y el fallo
                # solo se ve al abrirlo. Con el título a la vista se detecta
                # en el acto.
                if esperado:
                    print(f"    «{esperado[:88]}»")
                return True
            destino.unlink(missing_ok=True)

        print(f"  · sin PDF en {urlparse(url).netloc}")

    print(f"  ✗ no se pudo descargar: {referencia}")
    return False


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(1)
    sys.exit(0 if descargar(sys.argv[1], sys.argv[2], sys.argv[3]) else 1)
