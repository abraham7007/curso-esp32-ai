#!/usr/bin/env python3
"""Busca artículos de acceso abierto en OpenAlex y lista los descargables.

Filtra por acceso abierto y por existencia de PDF localizable, que son las
dos condiciones para que `get-paper.py` pueda traerlo. Sin ese filtro, la
mayoría de resultados relevantes no se pueden descargar y hay que
descartarlos uno a uno.

Uso:
  python3 tools/buscar-oa.py "FreeRTOS ESP32 dual core scheduling" [n]
"""

from __future__ import annotations

import json
import subprocess
import sys
from urllib.parse import quote

CORREO = "infinity.witss@gmail.com"


def buscar(consulta: str, n: int = 12) -> None:
    url = (
        "https://api.openalex.org/works"
        f"?search={quote(consulta)}"
        "&filter=is_oa:true,from_publication_date:2017-01-01"
        f"&per-page={n * 3}&mailto={CORREO}"
    )
    salida = subprocess.run(
        ["curl", "-sL", "--max-time", "60", url], capture_output=True, timeout=90
    )
    try:
        datos = json.loads(salida.stdout)
    except json.JSONDecodeError:
        print("  ! respuesta ilegible de OpenAlex")
        return

    mostrados = 0
    for w in datos.get("results", []):
        loc = w.get("best_oa_location") or {}
        # Sin url_for_pdf no hay descarga automática posible.
        if not loc.get("pdf_url"):
            continue
        doi = (w.get("doi") or "").replace("https://doi.org/", "")
        if not doi:
            continue
        rev = (loc.get("source") or {}).get("display_name") or "—"
        print(f"\n{doi}   [{w.get('publication_year')}]  {w.get('cited_by_count')} cit.")
        print(f"  {(w.get('title') or '')[:110]}")
        print(f"  {rev[:70]}  ·  {loc.get('license') or 'sin licencia declarada'}")
        mostrados += 1
        if mostrados >= n:
            break
    if not mostrados:
        print("  (sin resultados descargables)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    buscar(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 12)
