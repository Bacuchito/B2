#!/usr/bin/env python3
"""Tercera ronda de correcciones detectadas por la comprobación de literalidad.

Uso: python fix_review3.py
"""
import glob
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data")

changes = []


def norm_ws(s):
    return " ".join(str(s or "").split())


# ------------------------------------------------------------------ t4_c p51
# La cita del segundo ítem 15 arrastraba la anotación del compilador
# («(Personalthemen, Urlaubssperre)»), que no está en el acta, y unos puntos
# suspensivos. Se deja solo la frase literal que sostiene la respuesta.
path = os.path.join(DATA, "t4_c.json")
d = json.load(open(path, encoding="utf-8"))
v = [x for x in d["variants"] if x["id"] == "t4_c-p51"][0]
pas = norm_ws(v["passage"])
for it in v["items"]:
    if it["n"] == 15 and "(Personalthemen" in it.get("quote", ""):
        nueva = ("Urlaubsanträge können im Moment nur im Falle dringender "
                 "persönlicher Angelegenheiten genehmigt werden.")
        assert norm_ws(nueva) in pas, "la cita nueva tampoco es literal"
        it["quote"] = nueva
        changes.append("t4_c-p51/15b: cita sin la anotación del compilador ni «…»")
with open(path, "w", encoding="utf-8") as fh:
    json.dump(d, fh, ensure_ascii=False, indent=1)

# --------------------------------------------------- comprobación de cierres
# Ninguna cita debe contener unipsis ni anotaciones parentéticas de terceros.
sospechosas = []
for p in sorted(glob.glob(os.path.join(DATA, "*.json"))):
    data = json.load(open(p, encoding="utf-8"))
    for var in data["variants"]:
        for it in var["items"]:
            q = it.get("quote") or ""
            if "…" in q or "[…]" in q or "(Personalthemen" in q:
                sospechosas.append(f"{var['id']}/{it['n']}")
if sospechosas:
    print("QUEDAN citas sospechosas:", sospechosas)
else:
    print("comprobado: ninguna cita contiene «…» ni anotaciones ajenas")

print("cambios aplicados:")
for c in changes:
    print("  -", c)
