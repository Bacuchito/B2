#!/usr/bin/env python3
"""Extrae las 67 situaciones de Sprechen Teil 3 del PDF convertido.

El bloque original trae las descripciones partidas por líneas, con números de
página sueltos, separadores de guiones bajos y, en las situaciones 38-67, los
Stichpunkte con viñeta `•`. Varias traen dos formulaciones del mismo caso
separadas por « / » o entre paréntesis: se conservan tal cual.

Uso:
    python make_sprechen_t3.py <crudo.md> <borrador.json>
    python make_sprechen_t3.py <crudo.md> <borrador.json> <ayuda.json> <datos.json>

Sin ayuda escribe el borrador (alemán limpio). Con ayuda fusiona y escribe el
JSON de datos final que consume build.py: una variante por situación.
"""
import json
import re
import sys

# El bloque va de la Situation 1 a la página de resultados del Sprechen. Se
# ancla en texto, no en líneas: el PDF se reconvirtió una vez y se movieron.
INICIO = "Situation 1 Beschreibung:"
FIN = "Ermittlung des Teilergebnisses Sprechen"

MARCADOR = re.compile(r"^\s*<!--\s*page:\s*\d+\s*-->\s*$")
PAGINA = re.compile(r"^\s*\d{1,4}\s*$")
ENLACE = re.compile(r"^\s*https?://\S+\s*$")
GUIONES = re.compile(r"^\s*_+\s*$")
SEPARADOR = re.compile(r"Situation\s+(\d{1,2})\s+(?=Beschreibung:)")
NUM_PUNTO = re.compile(r"(?:^|\s)(\d{1,2})\.\s+(?=[A-ZÄÖÜ„])")

# Correcciones de erratas del OCR. Cada una se comprueba antes de aplicarse: si
# el texto cambió y la errata ya no está, el script falla en vez de corregir a
# ciegas. Se anotan en `fixes`, como manda el SPEC.
CORRECCIONES = [
    (51, "Gaste: Lösung?", "Gäste: Lösung?"),
    (54, "Konditorei, ihr Vermieter", "Konditorei, Ihr Vermieter"),
    (50, "CateringFirma", "Catering-Firma"),
]

# Los Stichpunkte de estas situaciones vienen mezclados por columnas en el PDF.
# Se escriben a mano, respetando el texto del documento, en el orden correcto.
STICHPUNKTE_MANUALES = {
    14: [
        "Falsche oder späte Lieferungen: Was tun?",
        "Kunden: Wie reagieren und was anbieten?",
        "Langfristig: Was tun, damit Pizzen richtig und pünktlich geliefert werden?",
    ],
    44: [
        "Sofortmaßnahmen: Wie Ersatz organisieren?",
        "Doppelbuchungen: Was tun?",
        "Gäste: Was anbieten?",
        "Wie die nächsten Buchungen kontrollieren?",
        "Langfristig: Wie in Zukunft vermeiden?",
    ],
    56: [
        "Persönlich ansprechen",
        "Gründe: Zeitmangel?",
        "Desinteresse?",
        "Gegenvorschläge?",
    ],
    59: [
        "Was mit dem Essen machen?",
        "Wen informieren?",
        "Kosten: wer bezahlt?",
        "Kunde: was fordern?",
    ],
    61: [
        "Wen informieren?",
        "Kosten: Schaden beheben.",
        "Kundin: Was anbieten?",
        "Langfristig: Wie solche Fälle vermeiden?",
    ],
}


def bloque_crudo(lineas):
    """Devuelve (líneas limpias, {situación: página}) del bloque.

    Las páginas se leen de los marcadores `<!-- page: N -->`: cada situación se
    queda con la página en la que empieza, para que el rótulo del PDF no mienta.
    """
    ini = next(i for i, l in enumerate(lineas) if INICIO in l)
    fin = next(i for i, l in enumerate(lineas)
               if FIN in l and i > ini)
    pagina, paginas = None, {}
    # La Situation 1 empieza después del marcador de su página, que queda fuera
    # del bloque: se busca hacia atrás el último `<!-- page: N -->`.
    for k in range(ini, -1, -1):
        m = MARCADOR.match(lineas[k])
        if m:
            pagina = int(re.search(r"\d+", lineas[k]).group())
            break
    limpias = []
    for linea in lineas[ini:fin]:
        m = MARCADOR.match(linea)
        if m:
            pagina = int(re.search(r"\d+", linea).group())
            continue
        m = re.match(r"^Situation (\d{1,2})\b", linea)
        if m and pagina is not None:
            paginas[int(m.group(1))] = pagina
        if PAGINA.match(linea):
            continue
        if ENLACE.match(linea) or GUIONES.match(linea):
            continue
        limpias.append(linea.strip())
    return limpias, paginas


def unir(lineas):
    """Une el bloque en un párrafo y cose los cortes de línea."""
    texto = re.sub(r"\s+", " ", " ".join(l for l in lineas if l)).strip()
    # Palabra partida: «ent- scheiden» → «entscheiden».
    texto = re.sub(r"(?<=\w)- (?=[a-zäöüß])", "", texto)
    # Guion real al final de línea: «Online- Geschäften» → «Online-Geschäften».
    texto = re.sub(r"(?<=\w)- (?=[A-ZÄÖÜ])", "-", texto)
    # Espacio que el OCR metió tras un paréntesis abierto.
    texto = re.sub(r"\( (?=[A-Za-zÄÖÜäöüß])", "(", texto)
    return texto


def trocear(texto):
    """Devuelve [(n, descripción, [stichpunkte…]), …]."""
    piezas = list(SEPARADOR.finditer(texto))
    salida = []
    for i, m in enumerate(piezas):
        n = int(m.group(1))
        fin = piezas[i + 1].start() if i + 1 < len(piezas) else len(texto)
        cuerpo = texto[m.end():fin].strip()
        if cuerpo.startswith("Beschreibung:"):
            cuerpo = cuerpo[len("Beschreibung:"):].strip()
        if "Stichpunkte:" in cuerpo:
            descripcion, puntos = cuerpo.split("Stichpunkte:", 1)
        else:
            descripcion, puntos = cuerpo, ""
        descripcion = descripcion.strip(" ,")
        puntos = puntos.strip()
        lista = STICHPUNKTE_MANUALES.get(n)
        if lista is None:
            lista = partir_puntos(puntos)
        salida.append((n, descripcion, [p for p in lista if p.strip()]))
    return salida


def partir_puntos(texto):
    """Parte los Stichpunkte por «1.», «2.» o por viñeta «•»."""
    if not texto:
        return []
    if texto.count("•") >= 2:
        crudos = [p.strip() for p in texto.split("•") if p.strip()]
    else:
        marcas = list(NUM_PUNTO.finditer(texto))
        if not marcas:
            return [texto]
        crudos = []
        for i, m in enumerate(marcas):
            fin = marcas[i + 1].start() if i + 1 < len(marcas) else len(texto)
            crudos.append(texto[m.end():fin].strip())
    return [re.sub(r"\s+", " ", p).strip() for p in crudos]


def aplicar_correcciones(situaciones):
    por_n = {s["n"]: s for s in situaciones}
    aplicadas = []
    for n, antes, despues in CORRECCIONES:
        s = por_n[n]
        if antes in s["de"]:
            s["de"] = s["de"].replace(antes, despues)
        else:
            golpe = [i for i, p in enumerate(s["punkte"]) if antes in p]
            if not golpe:
                raise SystemExit(f"corrección {n}: no encuentro «{antes}»")
            i = golpe[0]
            s["punkte"][i] = s["punkte"][i].replace(antes, despues)
        aplicadas.append(f"situación {n}: «{antes}» → «{despues}»")
    return aplicadas


def main():
    crudo, borrador = sys.argv[1], sys.argv[2]
    lineas = open(crudo, encoding="utf-8").read().split("\n")
    crudas, paginas = bloque_crudo(lineas)
    texto = unir(crudas)
    # El pie de página («Informaciones 49») se cuela antes del ancla de fin.
    texto = re.sub(r"\s+Informationen \d+\s*$", "", texto)

    situaciones = []
    for n, de, puntos in trocear(texto):
        situaciones.append({"n": n, "de": de, "punkte": puntos})

    nums = [s["n"] for s in situaciones]
    if nums != list(range(1, len(situaciones) + 1)):
        faltan = sorted(set(range(1, max(nums) + 1)) - set(nums))
        raise SystemExit(f"numeración rota: {len(situaciones)} situaciones, faltan {faltan}")
    fixes = aplicar_correcciones(situaciones)

    # Un Stichpunkt vacío o una descripción sin verbo son señal de mal corte.
    for s in situaciones:
        if len(s["de"]) < 60 or s["de"].startswith("Stichpunkte"):
            raise SystemExit(f"situación {s['n']}: descripción sospechosa: {s['de'][:70]}")
        if not (3 <= len(s["punkte"]) <= 6):
            raise SystemExit(f"situación {s['n']}: {len(s['punkte'])} Stichpunkte: {s['punkte']}")
        for p in s["punkte"]:
            if len(p) < 6:
                raise SystemExit(f"situación {s['n']}: Stichpunkt sospechoso: {p!r}")

    largas = sorted(situaciones, key=lambda s: -len(s["de"]))[:3]
    print(f"situaciones: {len(situaciones)} · con 2ª formulación: "
          f"{sum(1 for s in situaciones if ' / ' in s['de'])}")
    print(f"más larga: {len(largas[0]['de'])} chars · "
          f"stichpunkte: {sum(len(s['punkte']) for s in situaciones)}")

    if len(sys.argv) < 5:
        json.dump({"situations": situaciones}, open(borrador, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        print(f"borrador -> {borrador}")
        return 0

    ayuda = json.load(open(sys.argv[3], encoding="utf-8"))
    faltan = []
    for s in situaciones:
        h = ayuda.get(str(s["n"])) or {}
        s["titel"] = (h.get("titel") or "").strip()
        s["es"] = (h.get("es") or "").strip()
        s["ru"] = (h.get("ru") or "").strip()
        ejemplos = [str(e).strip() for e in (h.get("beispiele") or []) if str(e).strip()]
        s["beispiele"] = ejemplos
        puntos = h.get("punkte") or []
        if len(puntos) != len(s["punkte"]):
            faltan.append(f"{s['n']}: {len(puntos)} ayudas para {len(s['punkte'])} puntos")
        for p, a in zip(s["punkte"], puntos):
            p_es = (a.get("es") or "").strip() if isinstance(a, dict) else ""
            p_ru = (a.get("ru") or "").strip() if isinstance(a, dict) else ""
            if not p_es or not p_ru:
                faltan.append(f"{s['n']}: punto sin traducir: {p[:40]}")
        s["punkte"] = [{"de": p,
                        "es": (a.get("es") or "").strip() if isinstance(a, dict) else "",
                        "ru": (a.get("ru") or "").strip() if isinstance(a, dict) else ""}
                       for p, a in zip(s["punkte"], puntos)]
        for campo in ("titel", "es", "ru"):
            if not s[campo]:
                faltan.append(f"{s['n']}: «{campo}» vacío")
        if len(s["beispiele"]) < 2:
            faltan.append(f"{s['n']}: menos de 2 ejemplos en alemán")
    if faltan:
        raise SystemExit("ayuda incompleta:\n  " + "\n  ".join(faltan[:20]))

    # Una variante por situación: así el menú las lista por separado y cada una
    # tiene su página, en vez de una sola página con las 67 y una ventana encima.
    variantes = []
    for s in situaciones:
        if s["n"] not in paginas:
            raise SystemExit(f"situación {s['n']}: sin página en el documento")
        variantes.append({
            "id": f"spr-t3-{s['n']:02d}",
            "label": f"{s['n']} · {s['titel']}",
            "page": paginas[s["n"]],
            "kind": "situation",
            "n": s["n"],
            "titel": s["titel"],
            "de": s["de"],
            "es": s["es"],
            "ru": s["ru"],
            "punkte": s["punkte"],
            "beispiele": s["beispiele"],
        })

    datos = {
        "block": "sprechen_t3",
        "section": "sprechen-t3",
        "variants": variantes,
        "fixes": [
            "pp.188-200: unidas las líneas partidas, cosidos los guiones de corte, quitados los números de página sueltos y el espacio que el OCR dejó tras un paréntesis.",
            "pp.188-200: los Stichpunkte de las situaciones 14, 44, 56 y 59 venían mezclados por columnas; se ordenan sin cambiar el texto.",
        ] + fixes,
    }
    json.dump(datos, open(sys.argv[4], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"datos -> {sys.argv[4]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
