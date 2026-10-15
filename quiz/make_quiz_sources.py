#!/usr/bin/env python3
"""Parte el Markdown convertido en ficheros fuente por bloque de variantes.

Uso:
    python make_quiz_sources.py <md> <outdir>
"""
import json
import os
import re
import sys


def load_pages(md_path: str) -> dict[int, str]:
    text = open(md_path, encoding="utf-8").read()
    parts = re.split(r"<!-- page: (\d+) -->", text)
    return {int(parts[i]): parts[i + 1] for i in range(1, len(parts), 2)}


# (nombre, primera_pagina, ultima_pagina)  -- ambos inclusive
# Fase 1: Lesen Teil 1 y Teil 2.
PHASE1 = [
    ("t1_a", 8, 8),
    ("t1_a2", 9, 10),
    ("t1_b", 11, 13),
    ("t1_c", 14, 15),
    ("t1_d", 16, 18),
    ("t2_a", 19, 21),
    ("t2_b", 22, 24),
    ("t2_c", 25, 28),
    ("t2_d", 29, 31),
]

# Fase 2: el resto de Lesen y todo Hören.
# Los cortes están alineados con el INICIO de cada variante, porque en Hören
# Teil 2-4 la transcripción y las preguntas caen en páginas distintas.
PHASE2 = [
    # Lesen Teil 3 (foro) -- p.32-42
    ("t3_a", 32, 34),
    ("t3_b", 35, 37),
    ("t3_c", 38, 39),
    ("t3_d", 40, 42),
    # Lesen Teil 4 (actas) -- p.43-64
    ("t4_a", 43, 46),
    ("t4_b", 47, 50),
    ("t4_c", 51, 54),
    ("t4_d", 55, 58),
    ("t4_e", 59, 64),
    # Lesen und Schreiben Teil 1, SOLO los ítems 19-20 (lectura) -- p.66-77
    ("ls_a", 66, 69),
    ("ls_b", 70, 73),
    ("ls_c", 74, 77),
    # Hören Teil 1 -- p.119-136
    ("h1_a", 119, 123),
    ("h1_b", 124, 128),
    ("h1_c", 129, 132),
    ("h1_d", 133, 136),
    # Hören Teil 2 (Zuordnung) -- p.137-149
    ("h2_a", 137, 140),
    ("h2_b", 141, 144),
    ("h2_c", 145, 149),
    # Hören Teil 3 -- p.150-164
    ("h3_a", 150, 153),
    ("h3_b", 154, 157),
    ("h3_c", 158, 161),
    ("h3_d", 162, 164),
    # Hören Teil 4 -- p.165-178
    ("h4_a", 165, 167),
    ("h4_b", 168, 171),
    ("h4_c", 172, 175),
    ("h4_d", 176, 178),
]

BLOCKS = {"1": PHASE1, "2": PHASE2, "all": PHASE1 + PHASE2}


def main() -> None:
    if len(sys.argv) < 3:
        print(__doc__)
        print("fases disponibles:", ", ".join(BLOCKS))
        raise SystemExit(2)
    md_path, outdir = sys.argv[1], sys.argv[2]
    phase = sys.argv[3] if len(sys.argv) > 3 else "all"
    blocks = BLOCKS.get(phase)
    if blocks is None:
        print(f"fase desconocida: {phase!r}; usa una de {list(BLOCKS)}")
        raise SystemExit(2)

    pages = load_pages(md_path)
    os.makedirs(outdir, exist_ok=True)

    manifest = []
    for name, a, b in blocks:
        chunks = []
        for n in range(a, b + 1):
            body = pages.get(n, "")
            chunks.append(f"\n<!-- page: {n} -->\n{body}")
        content = "".join(chunks)
        path = os.path.join(outdir, f"{name}.md")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
        manifest.append({"name": name, "pages": [a, b],
                         "path": path, "chars": len(content)})
        print(f"{name:6} p.{a:>3}-{b:<3} {len(content):>7,} chars -> {path}")

    with open(os.path.join(outdir, "manifest.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
