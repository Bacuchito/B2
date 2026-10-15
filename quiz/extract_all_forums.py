# -*- coding: utf-8 -*-
import os
import sys
import re
import json

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

with open("out/B2_ohne_antworten.md", encoding="utf-8") as f:
    text = f.read()

m_start = text.find("<!-- page: 98 -->")
m_end = text.find("<!-- page: 107 -->")
p98_106 = text[m_start:m_end]

print("=== INSPECCIÓN DE PÁGINAS 98 A 106 ===")
lines = p98_106.splitlines()

# Imprimir bloques donde aparecen Thema
print(f"Total líneas en p.98-106: {len(lines)}")

# Buscar todas las menciones de Thema
matches = re.finditer(r'Thema\s*:\s*["“]([^"”]+)["”]', p98_106, re.IGNORECASE)
found = []
for m in matches:
    t = m.group(1).strip()
    found.append(t)

print(f"Total de temas encontrados con 'Thema: ...': {len(found)}")
unique = sorted(list(set(found)))
print(f"Temas únicos ({len(unique)}):")
for u in unique:
    print(f"  - {u}")
