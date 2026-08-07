#!/usr/bin/env python3
# Barrido de léxico-bandera anti-IA sobre las láminas.
# Lista cerrada tomada de la skill human-academic-writing
# (references/anti-ia__LEXICO_BANDERA_ES.md). NO se amplía por intuición:
# la lista está construida sobre frecuencias medidas, y añadir términos
# "que suenan a IA" produce falsos positivos sobre prosa humana correcta.
#
# Uso:  python3 tools/audit-lexico.py     (desde src/slides/)

# -*- coding: utf-8 -*-
import re, pathlib, collections

TERMINOS = {
 "adjetivos": ["robusto","robusta","robustos","robustas","integral","holístic","multifacétic",
   "crucial","fundamental","exhaustiv","pivotal","novedos","disruptiv","meticulos",
   "comprehensiv","considerable","sustantiv"],
 "sustantivos": ["paradigma","panorama","ecosistema","sinergia","vislumbre","tapiz","tejido",
   "paisaje"],
 "iniciadoras": ["cabe destacar","cabe señalar","cabe mencionar","cabe resaltar",
   "es importante señalar","es importante mencionar","es importante destacar",
   "es preciso mencionar","vale la pena","es menester","resulta crucial",
   "resulta fundamental","es importante notar"],
 "conectores": ["en este sentido","en este contexto","en esa línea","en el marco de",
   "en el ámbito de","por consiguiente","adicionalmente","asimismo","en conclusión"],
 "aperturas": ["el presente apartado","el presente trabajo","a continuación se presenta",
   "a continuación se expone","a continuación se describe","en lo que sigue",
   "acto seguido","hoy en día","en la actualidad","en los últimos años",
   "como se ha mencionado"],
 "calcos": ["en base a","basado en","basada en","una de las principales razones",
   "por encima de todo","como resultado","más aún","en primer lugar","en segundo lugar"],
 "verbos": ["abordar","abordan","aborda","vislumbrar","dilucidar","profundizar",
   "sustentar","propiciar","dinamizar"],
 "antitesis": ["no se trata de","más que un","más que una","lejos de"],
 "locuciones": ["habida cuenta","en aras de","a tenor de","merced a","en el seno de"],
}

def visible(html: str) -> str:
    html = re.sub(r"<pre[^>]*>.*?</pre>", " ", html, flags=re.S)
    html = re.sub(r'<div class="term">.*?</div>', " ", html, flags=re.S)
    html = re.sub(r'<div class="prompt-box">.*?</div>', " ", html, flags=re.S)
    html = re.sub(r"<script.*?</script>", " ", html, flags=re.S)
    html = re.sub(r"<style.*?</style>", " ", html, flags=re.S)
    html = re.sub(r"<[^>]+>", " ", html)
    return re.sub(r"\s+", " ", html)

hallazgos = collections.defaultdict(list)
for f in sorted(pathlib.Path(".").rglob("*.html")):
    txt = visible(f.read_text(encoding="utf-8")).lower()
    for cat, lista in TERMINOS.items():
        for t in lista:
            n = txt.count(t)
            if n:
                hallazgos[cat].append((str(f), t, n))

total = 0
for cat in TERMINOS:
    if not hallazgos[cat]: continue
    print(f"\n### {cat}")
    for arch, t, n in sorted(hallazgos[cat], key=lambda x: -x[2]):
        print(f"   {n}×  «{t}»  → {arch}")
        total += n
print(f"\nTOTAL: {total} apariciones")
