#!/usr/bin/env python3
"""Segunda ronda de correcciones detectadas en la verificación adversarial.

Uso: python fix_review2.py
"""
import json
import os

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data")

changes = []


def load(name):
    return json.load(open(os.path.join(DATA, name), encoding="utf-8"))


def save(name, data):
    with open(os.path.join(DATA, name), "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)


# ---------------------------------------------------------------- t1_d p18
# Dos citas usaban "[…]" para empalmar texto no contiguo, así que no eran
# subcadenas literales del anuncio, como exige el contrato. Se sustituyen por
# el tramo contiguo completo.
d = load("t1_d.json")
v = [x for x in d["variants"] if x["id"] == "t1_d-p18"][0]
ad = {o["key"]: o["text"] for o in v["options"]}

for it in v["items"]:
    if it["n"] == 2:
        it["quote"] = ("Wie viel sollte man in seinem Beruf verdienen? Wie viele Stunden "
                       "arbeitet man üblicherweise? Bekommt man einen Zuschuss für "
                       "Sprachkurse? Mit vielen gesetzlichen Dingen muss man sich auskennen, "
                       "wenn man im Arbeitsleben steht. Die wichtigsten Informationen finden "
                       "Sie hier zusammengefasst.")
        assert it["quote"] in ad["d"], "la cita del ítem 2 no es literal"
        changes.append("t1_d-p18/2: cita con […] sustituida por el tramo contiguo literal")
    if it["n"] == 4:
        it["quote"] = ("Andere sehen dort interessantere berufliche Möglichkeiten. "
                       "Manchmal ist das die reine Abenteuerlust. Auslandsaufenthalte können")
        assert it["quote"] in ad["h"], "la cita del ítem 4 no es literal"
        changes.append("t1_d-p18/4: cita con […] sustituida por el tramo contiguo literal")

save("t1_d.json", d)

# ------------------------------------------------- comprobacion global
# Ninguna cita debe contener "[…]".
bad = []
import glob  # noqa: E402
for path in sorted(glob.glob(os.path.join(DATA, "*.json"))):
    data = json.load(open(path, encoding="utf-8"))
    for var in data["variants"]:
        for it in var["items"]:
            if "[…]" in (it.get("quote") or ""):
                bad.append(f"{var['id']}/{it['n']}")
if bad:
    print("QUEDAN citas con […]:", bad)
else:
    print("comprobado: ninguna cita contiene […]")

print("cambios aplicados:")
for c in changes:
    print("  -", c)
