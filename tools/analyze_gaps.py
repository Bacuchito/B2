#!/usr/bin/env python3
"""Diagnostico: distribucion de huecos entre fragmentos de texto.

Objetivo: elegir el umbral que separa kerning (sin espacio) de
espacio tipografico real, en lugar de fijarlo a ojo.
"""
import sys
import collections
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pdf2md  # noqa: E402

PDF = sys.argv[1]

pdf = pdf2md.PDF(PDF)
pages = pdf.pages()
font_cache: dict = {}
buckets = collections.Counter()
examples = collections.defaultdict(list)

MAXP = int(sys.argv[2]) if len(sys.argv) > 2 else len(pages)

for i, pnum in enumerate(pages[:MAXP], 1):
    runs = pdf2md.page_runs(pdf, pnum, font_cache)
    if not runs:
        continue
    heights = [r.size for r in runs if r.size > 0]
    med = sorted(heights)[len(heights) // 2] if heights else 10.0
    tol = max(1.6, med * 0.45)
    ordered = sorted(runs, key=lambda r: (-r.y, r.x))
    groups = []
    for r in ordered:
        if groups and abs(groups[-1][0].y - r.y) <= tol:
            groups[-1].append(r)
        else:
            groups.append([r])
    for grp in groups:
        grp.sort(key=lambda r: r.x)
        prev = None
        for r in grp:
            if prev is not None and r.size > 0:
                gap = r.x - max(prev.x1, prev.x)
                ratio = gap / r.size
                # solo interesa la banda ambigua
                if -0.05 <= ratio <= 0.60:
                    b = round(ratio * 100 / 5) * 5  # cubos de 0.05 em
                    buckets[b] += 1
                    key = b
                    if len(examples[key]) < 6:
                        examples[key].append(
                            f"{prev.text[-14:]!r}+{r.text[:14]!r}")
            prev = r

print(f"paginas analizadas: {min(MAXP, len(pages))}")
print("distribucion de hueco/tamano de fuente (en centesimas de em):")
print(f"{'ratio':>7} {'casos':>8}  ejemplos")
for b in sorted(buckets):
    print(f"{b/100:>7.2f} {buckets[b]:>8}  {'; '.join(examples[b][:3])}")
