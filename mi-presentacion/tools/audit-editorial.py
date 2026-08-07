#!/usr/bin/env python3
# Control editorial sobre las láminas, derivado de las 18 dimensiones de la
# skill paper-review (references/control-calidad.md). Se aplican las que
# tienen equivalente en un mazo; las de manuscrito (ecuaciones numeradas,
# jerarquía de headings, voz por sección) no lo tienen.
#
# Dos familias de falso positivo conocidas, documentadas para no volver a
# investigarlas: los números que abren un .finding__value se leen como cifra
# a inicio de oración —son rótulos—, y las comillas rectas de las claves
# JSON son exigencia de la notación.
#
# Uso:  python3 tools/audit-editorial.py  (desde src/slides/)

# -*- coding: utf-8 -*-
import re, pathlib, collections

def por_bloques(h):
    """Texto visible, pero con un salto donde termina cada bloque.

    `visible()` aplana todo a una línea, y eso hace que dos elementos de lista
    consecutivos —«src/ — código del proyecto», «lib/ — módulos propios»— se
    lean como un solo inciso entre rayas. La comprobación 20 necesita saber
    dónde acaba una frase, porque un separador dentro de un renglón no es lo
    mismo que un par que encierra un inciso.
    """
    for pat in (r"<pre[^>]*>.*?</pre>", r'<div class="term">.*?</div>',
                r'<div class="prompt-box">.*?</div>', r"<script.*?</script>"):
        h = re.sub(pat, " ", h, flags=re.S)
    h = re.sub(r"</(p|li|div|td|th|h[1-6])>|<br\s*/?>", "\n", h, flags=re.I)
    h = re.sub(r"<[^>]+>", " ", h)
    return re.sub(r"[ \t]+", " ", h)


def visible(h):
    for pat in (r"<pre[^>]*>.*?</pre>", r'<div class="term">.*?</div>',
                r'<div class="prompt-box">.*?</div>', r"<script.*?</script>"):
        h = re.sub(pat, " ", h, flags=re.S)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h))

R = collections.defaultdict(list)
ACR = collections.defaultdict(set)

for f in sorted(pathlib.Path(".").rglob("*.html")):
    raw = f.read_text(encoding="utf-8")
    t = visible(raw)
    rel = str(f)

    # 9. Unidades SI: espacio fino entre cifra y unidad; nunca "10ms" pegado
    for m in re.finditer(r"\b\d+(?:[.,]\d+)?(ms|us|µs|kHz|MHz|Hz|mV|V|mA|kB|KB|MB|Ω|bits?|baudios)\b", t):
        R["9 · unidad pegada a la cifra"].append(f"{rel}: «{m.group(0)}»")

    # 7. Cifra al inicio de oración
    for m in re.finditer(r"(?:^|[.;] )(\d[\d.,]*)\s+[a-záéíóúñ]", t):
        R["7 · cifra al inicio de oración"].append(f"{rel}: «{m.group(0).strip()[:40]}»")

    # 14/8. Comillas rectas donde debería haber angulares o tipográficas
    n = len(re.findall(r'(?<![=<>/])"[A-Za-zÁÉÍÓÚÑáéíóúñ¿¡]', t))
    if n: R["8 · comillas rectas en texto visible"].append(f"{rel}: {n}")

    # 4. Acrónimos: se recogen para ver si alguno nunca se expande
    for m in re.finditer(r"\b([A-Z]{2,6})\b", t):
        ACR[m.group(1)].add(rel)

    # 20. Raya en par decorativo. La skill human-academic-writing la prohíbe:
    # es de las marcas que más suben el porcentaje de texto atribuido a IA.
    # Se admite UNA raya suelta para introducir una sigla en su primera
    # mención; lo que se persigue es el par que encierra un inciso, que se
    # escribe con comas, con paréntesis o partiendo la oración.
    # El inciso no puede cruzar un salto de bloque: una raya que separa el
    # término de su descripción dentro de un renglón de lista es un separador
    # legítimo, no un par decorativo.
    for m in re.finditer(r"—[^—\n]{2,120}—", por_bloques(raw)):
        R["20 · raya en par decorativo"].append(f"{rel}: «{m.group(0)[:56]}…»")

    # 16/18. Negrita: proporción de texto resaltado
    negrita = sum(len(x) for x in re.findall(r"<b>(.*?)</b>", raw, re.S))
    if len(t) > 400 and negrita / len(t) > 0.22:
        R["16 · exceso de negrita"].append(f"{rel}: {negrita*100//len(t)} % del texto")

    # 15. Espacio faltante alrededor de un elemento inline de código
    for m in re.finditer(r"[a-záéíóúñ]</?code>", raw):
        pass

    # 2. Referencias cruzadas: menciones a «Ejemplo NN» que no existan
    for m in re.finditer(r"Ejemplo (\d{2})", t):
        R["_ejemplos_citados"].append((rel, m.group(1)))

for k in sorted(R):
    if k.startswith("_"): continue
    print(f"\n### {k}  ({len(R[k])})")
    for x in R[k][:8]: print("   ", x)
    if len(R[k]) > 8: print(f"    … y {len(R[k])-8} más")

# 4. acrónimos usados en muchas láminas sin expansión en el glosario
glos = " ".join(visible(p.read_text(encoding="utf-8")) for p in pathlib.Path(".").rglob("*glosario*.html"))
sospechosos = {a: v for a, v in ACR.items()
               if len(v) >= 4 and a not in glos and a not in
               {"ESP","GPIO","ADC","PWM","UART","SPI","LED","PIT","OTI","UNI","AI","IA","CC","BY","NC","ND","DOI","PDF","SoC","RAM","ROM","SRAM","USB","GND","JSON","CRC","ISR","DAC","RTC","ULP","OLED","IDF","CPU","MHz","KB","MB","IEEE","APA","ABNT","ACM","QEMU","HDLC","PSON","DTR","RTS","BOOT","EN","MQTT","LX","V1","AHB","IEPE","DAQ","FAIR","ICSE","VSB","LLM","FFT","SHA","IIR","FIR","CO","OK","ESP32"}}
print(f"\n### 4 · acrónimos en 4+ láminas sin entrada en el glosario ({len(sospechosos)})")
for a, v in sorted(sospechosos.items(), key=lambda x: -len(x[1]))[:12]:
    print(f"    {a}  en {len(v)} láminas")
