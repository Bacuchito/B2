#!/usr/bin/env python3
"""merge_sprachbausteine_respuestas.py - Consolida las respuestas deducidas.

Los Sprachbausteine no traen clave en el documento original: las respuestas se
deducen leyendo el texto (lo dice GUIA_B2.md). Se deducen por grupos en ficheros
`quiz/_resp_*.json` y este script los funde en un único
`quiz/sprachbausteine_respuestas.json`, que es la fuente de verdad que lee
`make_sprachbausteine.py`.

Comprueba lo que puede comprobarse solo:
  * que la respuesta esté entre las opciones del hueco,
  * que la cita aparezca literalmente en el texto,
  * que no haya dos respuestas iguales dentro de una variante del Teil 1,
  * que no haya huecos sin respuesta.

Uso:
    python quiz/merge_sprachbausteine_respuestas.py quiz

El argumento es la raíz del módulo (quiz). Los datos se leen de quiz/data/ y el
fichero consolidado se escribe en quiz/, donde build.py no lo confunde con un
fichero de datos.
"""
from __future__ import annotations

import glob
import json
import os
import re
import sys


def norm_ws(s) -> str:
    return " ".join(str(s or "").split())


def main():
    raiz = sys.argv[1] if len(sys.argv) > 1 else "quiz"
    datadir = os.path.join(raiz, "data")
    datos = {}
    for f in ("sprachbausteine_t1.json", "sprachbausteine_t2.json"):
        d = json.load(open(os.path.join(datadir, f), encoding="utf-8"))
        for v in d["variants"]:
            datos[v["id"]] = v

    respuestas, origen = {}, {}
    ficheros = sorted(glob.glob(os.path.join(raiz, "_resp_*.json")))
    if not ficheros:
        # Sin ficheros de origen, reescribir dejaría el consolidado vacío y se
        # perderían las 132 respuestas. Mejor no tocar nada.
        print("No hay ficheros _resp_*.json: no se reescribe nada. "
              "El consolidado sigue como estaba.")
        return 0
    for ruta in ficheros:
        grupo = json.load(open(ruta, encoding="utf-8"))
        for vid, huecos in grupo.items():
            if vid not in datos:
                print(f"  aviso: {os.path.basename(ruta)} trae una variante desconocida: {vid}")
                continue
            respuestas.setdefault(vid, {})
            for n, r in huecos.items():
                respuestas[vid][str(int(n))] = r
                origen[(vid, str(int(n)))] = os.path.basename(ruta)

    problemas, sin_respuesta = [], []
    for vid, v in datos.items():
        if v["kind"] == "zuordnung":
            claves = [str(o["key"]).lower() for o in v.get("options", [])]
        for it in v["items"]:
            n = str(it["n"])
            r = (respuestas.get(vid) or {}).get(n)
            if not r or not r.get("answer"):
                sin_respuesta.append(f"{vid}#{n}")
                continue
            ans = str(r["answer"]).lower()
            if v["kind"] == "zuordnung":
                if ans not in claves:
                    problemas.append(f"{vid}#{n}: respuesta «{ans}» fuera del banco")
            else:
                okeys = [str(o["key"]).lower() for o in it.get("options", [])]
                if ans not in okeys:
                    problemas.append(f"{vid}#{n}: respuesta «{ans}» fuera de las opciones {okeys}")
            for campo in ("quote", "explain", "explain_ru"):
                if not (r.get(campo) or "").strip():
                    problemas.append(f"{vid}#{n}: falta «{campo}»")
            if r.get("confidence") not in ("hoch", "mittel", "niedrig"):
                problemas.append(f"{vid}#{n}: confidence inválida ({r.get('confidence')!r})")
            if r.get("quote") and norm_ws(r["quote"]) not in norm_ws(v.get("passage")):
                problemas.append(f"{vid}#{n}: la cita no es literal del texto: «{norm_ws(r['quote'])[:60]}…»")
        if v["kind"] == "zuordnung":
            resp = [str((respuestas.get(vid) or {}).get(str(it["n"]), {}).get("answer", "")).lower()
                    for it in v["items"]]
            # Solo tiene sentido mirar repeticiones cuando están todas: si falta
            # alguna, ya se ha avisado arriba.
            if all(resp) and len(set(resp)) != len(resp):
                problemas.append(f"{vid}: respuestas repetidas en el banco: {resp}")

    ruta = os.path.join(raiz, "sprachbausteine_respuestas.json")
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(respuestas, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")

    total = sum(len(h) for h in respuestas.values())
    print(f"{total} respuestas de {len(respuestas)} variantes -> {ruta}")
    if sin_respuesta:
        print(f"\nSIN RESPUESTA ({len(sin_respuesta)}): " + ", ".join(sin_respuesta[:20]))
    if problemas:
        print(f"\nPROBLEMAS ({len(problemas)}):")
        for p in problemas[:40]:
            print("  ", p)
    if not sin_respuesta and not problemas:
        print("Todo coherente: respuestas dentro de las opciones, citas literales y sin repetir.")
    return 1 if (sin_respuesta or problemas) else 0


if __name__ == "__main__":
    sys.exit(main())
