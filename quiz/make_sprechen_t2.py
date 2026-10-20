#!/usr/bin/env python3
"""Extrae las 104 tarjetas de Smalltalk (Sprechen Teil 2) del PDF convertido.

El original viene partido por saltos de línea, con números de página sueltos,
marcadores `<!-- page: N -->` y, en 38 de las 104, la traducción rusa pegada
entre paréntesis al final. Varias traen dos formulaciones separadas por « / ».

Uso:
    python make_sprechen_t2.py <crudo.md> <borrador.json>
    python make_sprechen_t2.py <crudo.md> <borrador.json> <traducciones.json> <datos.json>

Sin traducciones escribe el borrador (alemán limpio + ruso cuando ya existe).
Con traducciones, además fusiona y escribe el JSON de datos final.
"""
import json
import re
import sys

# El bloque de Smalltalk va de la primera tarjeta a la lista de enlaces que
# precede a las Situationen del Teil 3. Se ancla en texto, no en números de
# línea: el PDF se reconvirtió una vez y las líneas se movieron.
INICIO = "1. • Ich finde, wir als Praktikant*innen"
FIN = "Возможные темы на экзамене"

CIRILICO = re.compile(r"[\u0400-\u04FF]")
NUM_ITEM = re.compile(r"^\s*(\d{1,3})\.\s*[•·–-]?\s*")
PAGINA = re.compile(r"^\s*\d{1,4}\s*$")
MARCADOR = re.compile(r"^\s*<!--\s*page:\s*\d+\s*-->\s*$")

# Erratas del documento. Cada una se comprueba antes de aplicarse: si el texto
# cambia y la errata ya no está, el script falla en vez de corregir a ciegas.
# Se anotan en `fixes` del JSON, como manda el SPEC.
CORRECCIONES = [
    # (tarjeta, campo, texto que debe estar, texto corregido)
    (50, "alt", "Was hälst du von Selbstständigkeit?", "Was hältst du von Selbstständigkeit?"),
    (72, "alt", "Ich möchte meine Stunden reduziere.", "Ich möchte meine Stunden reduzieren."),
    (83, "de", "Hast du eine Idee", "Hast du eine Idee?"),
    (83, "alt", "weißt du, was man in den Ferien mit Kindern",
     "Weißt du, was man in den Ferien mit Kindern"),
    (92, "de", "Hast du Idee", "Hast du eine Idee"),
    (99, "de", "für unsere Team", "für unser Team"),
    (102, "de", "Angst vor ihn hat", "Angst vor ihnen hat"),
]


def bloque_crudo(lineas):
    """Devuelve las líneas del bloque de Smalltalk, sin cabecera ni cola."""
    ini = next(i for i, l in enumerate(lineas) if INICIO in l)
    fin = next(i for i, l in enumerate(lineas) if FIN in l and i > ini)
    return lineas[ini:fin]


def trocear(lineas):
    """Agrupa por número de tarjeta. Devuelve [(n, [lineas…]), …]."""
    grupos = []
    for linea in lineas:
        if MARCADOR.match(linea) or PAGINA.match(linea):
            continue
        m = NUM_ITEM.match(linea)
        if m:
            grupos.append((int(m.group(1)), [NUM_ITEM.sub("", linea, count=1).strip()]))
        elif grupos:
            grupos[-1][1].append(linea.strip())
    return grupos


def limpiar(partes):
    """Une las líneas de una tarjeta en un párrafo y quita las costuras."""
    texto = " ".join(p for p in partes if p)
    texto = re.sub(r"\s+", " ", texto).strip()
    # Guion de corte de palabra al final de línea («Arbeitsunfähigkeits-
    # bescheinigung», «неис- пользованного»).
    texto = re.sub(r"(?<=\w)- (?=[a-zäöüßа-яё])", "", texto)
    return texto


def separar_idiomas(texto):
    """Devuelve (alemán, ruso o ""). El ruso es el paréntesis final con cirílico."""
    m = CIRILICO.search(texto)
    if not m:
        return texto, ""
    corte = texto.rfind("(", 0, m.start())
    if corte == -1:
        return texto, ""
    aleman = texto[:corte].strip()
    ruso = texto[corte:].strip()
    # El paréntesis puede no cerrar si el OCR cortó la línea.
    if ruso.endswith(")"):
        ruso = ruso[1:-1]
    elif ruso.startswith("("):
        ruso = ruso[1:]
    return aleman, ruso.strip()


def separar_alternativas(texto):
    """«DE (RU) / DE2 (RU2)» → (alemán, [alternativas], ruso).

    El documento trae varias veces dos formulaciones del mismo tema separadas
    por « / », y la traducción rusa puede ir dentro de cualquiera de las dos:
    hay que partir por « / » ANTES de separar los idiomas, o el ruso se traga
    la segunda formulación.
    """
    aleman, alternativas, ruso = "", [], ""
    for parte in (p.strip() for p in texto.split(" / ")):
        if not parte:
            continue
        de, ru = separar_idiomas(parte)
        if de:
            if not aleman:
                aleman = de
            else:
                alternativas.append(de)
        if ru and not ruso:
            ruso = ru
    return aleman, alternativas, ruso


def aplicar_correcciones(tarjetas):
    por_n = {t["n"]: t for t in tarjetas}
    aplicadas = []
    for n, campo, antes, despues in CORRECCIONES:
        t = por_n[n]
        if campo == "alt":
            golpe = [i for i, a in enumerate(t["alt"]) if antes in a]
            if not golpe:
                raise SystemExit(f"corrección {n}/{campo}: no encuentro «{antes}»")
            i = golpe[0]
            t["alt"][i] = t["alt"][i].replace(antes, despues)
        else:
            if antes not in t[campo]:
                raise SystemExit(f"corrección {n}/{campo}: no encuentro «{antes}»")
            t[campo] = t[campo].replace(antes, despues)
        aplicadas.append(f"tarjeta {n}: «{antes}» → «{despues}»")
    return aplicadas


def main():
    crudo, borrador = sys.argv[1], sys.argv[2]
    lineas = open(crudo, encoding="utf-8").read().split("\n")
    tarjetas = []
    for n, partes in trocear(bloque_crudo(lineas)):
        aleman, alt, ruso = separar_alternativas(limpiar(partes))
        de = aleman
        if not de:
            raise SystemExit(f"tarjeta {n} sin texto alemán")
        tarjetas.append({"n": n, "de": de, "alt": alt, "ru": ruso, "es": ""})

    nums = [t["n"] for t in tarjetas]
    if nums != list(range(1, len(tarjetas) + 1)):
        faltan = sorted(set(range(1, max(nums) + 1)) - set(nums))
        raise SystemExit(f"numeración rota: {len(tarjetas)} tarjetas, faltan {faltan}")
    # Una tarjeta es alemán con su ayuda rusa; el cirílico en el alemán o un
    # paréntesis huérfano en el ruso significan que el corte de idiomas falló.
    for t in tarjetas:
        if CIRILICO.search(t["de"]) or any(CIRILICO.search(a) for a in t["alt"]):
            raise SystemExit(f"tarjeta {t['n']}: cirílico en el texto alemán")
        if t["ru"].count("(") != t["ru"].count(")"):
            raise SystemExit(f"tarjeta {t['n']}: paréntesis sin cerrar en el ruso: {t['ru'][:60]}")
    fixes = aplicar_correcciones(tarjetas)
    con_ru = sum(1 for t in tarjetas if t["ru"])
    con_alt = sum(1 for t in tarjetas if t["alt"])
    print(f"tarjetas: {len(tarjetas)} · con ruso original: {con_ru} · con alternativa: {con_alt}")
    print(f"más larga: {max(len(t['de']) for t in tarjetas)} chars · "
          f"más corta: {min(len(t['de']) for t in tarjetas)} chars")

    if len(sys.argv) < 5:
        json.dump({"cards": tarjetas}, open(borrador, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        print(f"borrador -> {borrador}")
        return 0

    trad = json.load(open(sys.argv[3], encoding="utf-8"))
    faltan_es, faltan_ru = [], []
    for t in tarjetas:
        par = trad.get(str(t["n"])) or trad.get(t["n"]) or {}
        t["es"] = (par.get("es") or "").strip()
        # El ruso del documento manda: es el original. Solo se rellena el hueco.
        t["ru"] = t["ru"] or (par.get("ru") or "").strip()
        if not t["es"]:
            faltan_es.append(t["n"])
        if not t["ru"]:
            faltan_ru.append(t["n"])
    if faltan_es or faltan_ru:
        raise SystemExit(f"traducciones incompletas · es: {faltan_es} · ru: {faltan_ru}")

    datos = {
        "block": "sprechen_t2",
        "section": "sprechen-t2",
        "variants": [{
            "id": "spr-t2-smalltalk",
            "label": "Alle Karten",
            "page": 182,
            "kind": "smalltalk",
            "intro": ("Teil 2 der mündlichen Prüfung. Sie unterhalten sich mit einer Kollegin "
                      "oder einem Kollegen über Alltag und Beruf. Wählen Sie eine Karte und "
                      "sprechen Sie etwa drei Minuten darüber."),
            "time_minutes": 3,
            "cards": tarjetas,
        }],
        "fixes": [
            "p.182-187: unidas las líneas partidas y quitados los números de página sueltos.",
            "p.182-187: las dos formulaciones separadas por « / » van en la misma tarjeta (campo alt).",
        ] + fixes,
    }
    json.dump(datos, open(sys.argv[4], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"datos -> {sys.argv[4]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
