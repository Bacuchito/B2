#!/usr/bin/env python3
"""Genera un indice navegable a partir del Markdown producido por pdf2md.py."""
import json
import re
import sys
import os

src_md = sys.argv[1]
out_txt = sys.argv[2]

text = open(src_md, encoding="utf-8").read()
parts = re.split(r"<!-- page: (\d+) -->", text)
pages = {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}

# palabras clave que suelen marcar el inicio de un bloque nuevo
KEY = re.compile(
    r"^(TOP\s*\d+|Teil\s*\d+|LESEN|HÖREN|SCHREIBEN|SPRECHEN|SPRACHBAUSTEINE|"
    r"Lesen|Hören|Schreiben|Sprechen|Aufgabe\s*\d+|Test\s*\d+|Modelltest|"
    r"ЧАСТЬ|Часть|LESEN:|HÖREN:|SCHREIBEN:|SPRECHEN:|"
    r"Вариант|ВАРИАНТ|Экзамен|ЭКЗАМЕН|Приложение|ПРИЛОЖЕНИЕ|"
    r"Redemittel|Redewendungen|Wortschatz|Grammatik|Brief|Beschwerde|"
    r"Формулы|Фразы|Структура|Шаблон|План)",
    re.IGNORECASE,
)

rows = []
for n in sorted(pages):
    lines = [l.strip() for l in pages[n].splitlines() if l.strip()]
    if not lines:
        rows.append((n, 0, ""))
        continue
    head = ""
    for l in lines:
        if l.startswith("### "):
            head = l[4:]
            break
    if not head:
        for l in lines:
            if KEY.match(l):
                head = l[:90]
                break
    if not head:
        # primer parrafo con longitud razonable
        for l in lines:
            if 15 <= len(l) <= 90 and not l.startswith("http"):
                head = l
                break
    if not head:
        head = lines[0][:90]
    rows.append((n, len(lines), head))

with open(out_txt, "w", encoding="utf-8") as fh:
    fh.write(f"INDICE DE {os.path.basename(src_md)}\n")
    fh.write(f"{len(rows)} paginas\n")
    fh.write("=" * 100 + "\n\n")
    for n, cnt, head in rows:
        fh.write(f"p.{n:>3}  ({cnt:>2} l)  {head}\n")

print(f"escrito {out_txt}: {len(rows)} paginas")
print()
print(open(out_txt, encoding="utf-8").read()[:4000])
