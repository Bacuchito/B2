#!/usr/bin/env python3
"""Correcciones puntuales detectadas en la verificación adversarial.

Uso: python fix_review.py
"""
import json
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(BASE, "data")

changes = []


def load(name):
    return json.load(open(os.path.join(DATA, name), encoding="utf-8"))


def save(name, data):
    with open(os.path.join(DATA, name), "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)


def find(data, vid):
    for v in data["variants"]:
        if v["id"] == vid:
            return v
    return None


# ---------------------------------------------------------------- t2_a p19b
# La opción a) aparecía en el fuente con DOS redacciones; el JSON conservó la
# débil y perdía el «nur», que es justo lo que la hace falsa.
d = load("t2_a.json")
v = find(d, "t2_a-p19b")
it = [i for i in v["items"] if i["n"] == 7][0]
it["options"][0]["text"] = ("ist nur über die Personalabteilung einsehbar. / "
                            "kann in der Personalabteilung eingesehen werden.")
it["explain"] = (
    "La c es la única que queda en pie, por eliminación. "
    "a) dice que la cuenta solo se ve a través de la oficina de personal, y el texto lo "
    "contradice de forma directa: «Die Personalabteilung richtet Ihnen einen Zugang … ein. "
    "Damit können Sie im Intranet Ihr Arbeitszeitkonto jederzeit einsehen.» Es la propia "
    "oficina de personal la que le habilita el acceso, pero usted lo consulta por su cuenta "
    "en la intranet, no en ventanilla. "
    "b) es falsa porque las horas no las apunta el trabajador: «Die Zeiterfassung berechnet "
    "automatisch die reguläre Arbeitszeit sowie eventuelle Über- als auch Minusstunden.» "
    "c) no aparece literalmente en el texto —de ahí la confianza media—, pero el fichaje de "
    "entrada y salida es diario y el saldo se calcula de forma automática, así que es la "
    "lectura razonable una vez descartadas a y b."
)
it["confidence"] = "mittel"
changes.append("t2_a-p19b/7: opción a) con sus dos redacciones y explicación por eliminación")

save("t2_a.json", d)

# ---------------------------------------------------------------- t2_b p23
# La nota avisaba de un bug del visor (clave id#n) que ya está corregido:
# ahora la clave es posicional y los dos ítems n=6 se puntúan por separado.
d = load("t2_b.json")
v = find(d, "t2_b-p23")
old = v.get("note", "")
cut = old.find("AVISO TÉCNICO")
if cut != -1:
    v["note"] = old[:cut].strip() + (
        " Los dos ítems con n=6 se muestran como 6a y 6b y se puntúan por separado.")
    changes.append("t2_b-p23: retirado el aviso técnico obsoleto")
save("t2_b.json", d)

print("cambios aplicados:")
for c in changes:
    print("  -", c)
