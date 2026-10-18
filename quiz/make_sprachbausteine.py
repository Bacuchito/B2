#!/usr/bin/env python3
"""make_sprachbausteine.py - Extrae los Sprachbausteine del Markdown fuente.

Genera dos ficheros de datos que el visor ya sabe pintar:

  * quiz/data/sprachbausteine_t1.json  -> kind "zuordnung"
      Teil 1 es un texto con 6 huecos (46-51) y un banco de 10 palabras (a-j):
      el mismo mecanismo que emparejar personas con anuncios, pero aquí se
      empareja cada hueco con su palabra.

  * quiz/data/sprachbausteine_t2.json  -> kind "text"
      Teil 2 es un texto con 6 huecos (52-57) y tres opciones por hueco:
      exactamente la forma de Lesen Teil 2/4.

El documento NO trae clave de respuestas (lo dice GUIA_B2.md). Las respuestas se
deducen y viven en quiz/sprachbausteine_respuestas.json, con su cita literal y su
nivel de confianza. Este script las inyecta; si falta alguna, avisa y falla, para
no publicar un ejercicio sin solución.

Uso:
    python quiz/make_sprachbausteine.py out/B2_ohne_antworten.md quiz/data

El segundo argumento es el directorio de DATOS (quiz/data). Las respuestas se leen
de quiz/sprachbausteine_respuestas.json, un nivel por encima: ahí no las ve build.py,
que solo mira los ficheros de datos.
"""
from __future__ import annotations

import json
import os
import re
import sys

CIRILICO = re.compile(r"[А-Яа-яЁё]")
PAGE_RE = re.compile(r"^<!--\s*page:\s*(\d+)\s*-->\s*$")
HEAD_RE = re.compile(r"^\*\*Sprachbausteine\s+Teil\s+([12])\s*\(вариант\s*№?\s*([^)]*)\)\s*(.*?)\*\*\s*$")
FIN_RE = re.compile(r"^\*\*Sprachbausteine\s+Training")
HUECO_RE = re.compile(r"\b(\d{2})\s*\(\s*\)")

# El PDF mezcla homóglifos cirílicos en las letras de opción («а)», «с)», «е)»).
# Solo se corrigen en la PRIMERA letra de una línea de opciones: el texto alemán y
# las notas rusas no se tocan.
HOMOGLIFOS = {"а": "a", "с": "c", "е": "e", "о": "o", "р": "p", "х": "x",
              "у": "y", "і": "i", "ѕ": "s", "ј": "j", "А": "A", "С": "C", "Е": "E"}
LETRAS_BANCO = "a-l"   # el banco oficial es a-j; hay variantes con una letra de más


def normalizar_clave(linea: str) -> str:
    """Cambia el homóglifo cirílico inicial de una línea de opciones por su letra latina."""
    for i, ch in enumerate(linea):
        if ch.isspace():
            continue
        if ch in HOMOGLIFOS:
            return linea[:i] + HOMOGLIFOS[ch] + linea[i + 1:]
        return linea
    return linea

# Notas del compilador en ruso que no forman parte del ejercicio.
NOTAS = {
    "новый": "nueva versión",
    "новая": "nueva versión",
    "тест": "test",
    "вариант": "variante",
    "от": "de",
}


def limpiar_guiones(texto: str) -> str:
    """Une las palabras partidas por el salto de línea del PDF («Ausbildungs-\\nkonzept»)."""
    return re.sub(r"(\w)-\s*\n\s*(\w)", r"\1\2", texto)


def es_nota(linea: str) -> bool:
    """Línea de aviso del compilador (rusa), no del ejercicio."""
    limpia = linea.strip().strip("*").strip()
    if not limpia or not CIRILICO.search(limpia):
        return False
    # El texto alemán del ejercicio nunca trae cirílico; una línea corta en ruso,
    # sí. Las muy largas serían un texto del examen: no las tocamos.
    return len(limpia) < 120


def etiqueta_extra(extra: str) -> str:
    """Glosa en español del sufijo ruso del encabezado, sin dejar cirílico suelto."""
    e = extra.strip().strip("()").strip()
    if not e:
        return ""
    partes = []
    if re.search(r"нов", e, re.IGNORECASE):
        partes.append("nueva versión")
    if re.search(r"тест", e, re.IGNORECASE):
        partes.append("test")
    cola = ", ".join(re.findall(r"\d{2}\.\d{2}\.\d{4}|\d{2}\.\d{4}|\b\d{6}\b", e))
    etiqueta = " ".join(partes)
    if cola:
        etiqueta = (etiqueta + " " + cola).strip()
    return etiqueta or "versión alternativa"


def sufijo_id(extra: str) -> str:
    """Sufijo estable para distinguir variantes con el mismo número."""
    e = extra.strip().strip("()").strip()
    if not e:
        return ""
    fecha = re.search(r"(\d{2})\.(\d{2})\.?(\d{4})?", e)
    if fecha:
        return "-" + "".join(x for x in fecha.groups() if x)
    test = re.search(r"(\d{6})", e)
    if test:
        return "-test-" + test.group(1)
    return "-b"


def es_titular(linea: str) -> bool:
    """Línea de título: toda en negrita, sin huecos y que no sea una opción.

    En el Teil 2 las opciones también van en negrita (`**52. a) den Erwerb**`), así
    que sin esta última condición cada opción parecería el título de otro ejercicio.
    """
    t = linea.strip()
    if HUECO_RE.search(t) or es_linea_de_opciones(normalizar_clave(t)):
        return False
    return bool(re.fullmatch(r"\*\*[^*]+\*\*", t))


def dividir_subvariantes(lineas):
    """Un mismo bloque puede traer DOS cartas pegadas.

    Pasa en la variante 4 del Teil 1: debajo de «Kündigung» viene otra vez el
    mismo texto como «Kündigung ( новый от 04.04.25)», cada uno con su banco. Se
    corta en el segundo titular que llega después de las opciones de la primera,
    que es lo que delata que empieza otro ejercicio.
    """
    partes, actual, visto_opcion = [], [], False
    for linea in lineas:
        if es_linea_de_opciones(normalizar_clave(linea.strip())):
            visto_opcion = True
        if es_titular(linea) and visto_opcion and actual:
            partes.append(actual)
            actual = [linea]
            visto_opcion = False
            continue
        actual.append(linea)
    if actual:
        partes.append(actual)
    return partes


def partir_secciones(texto: str):
    """Devuelve la lista de variantes crudas de la parte de Sprachbausteine."""
    lineas = texto.split("\n")
    ini = next((i for i, l in enumerate(lineas) if HEAD_RE.match(l)), None)
    if ini is None:
        raise SystemExit("no encuentro la primera cabecera de Sprachbausteine")
    fin = next((i for i, l in enumerate(lineas) if i > ini and FIN_RE.match(l)), len(lineas))

    # La página del primer bloque es la del último marcador ANTES de la cabecera.
    pagina = 0
    for l in lineas[:ini]:
        m = PAGE_RE.match(l)
        if m:
            pagina = int(m.group(1))
    bloques = []
    for i in range(ini, fin):
        linea = lineas[i]
        mpage = PAGE_RE.match(linea)
        if mpage:
            pagina = int(mpage.group(1))
            continue
        m = HEAD_RE.match(linea)
        if m:
            bloques.append({"teil": int(m.group(1)), "num": m.group(2).strip(),
                            "extra": m.group(3), "page": pagina, "lineas": []})
            continue
        if bloques:
            bloques[-1]["lineas"].append(linea)

    # Dos cartas pegadas bajo una misma cabecera solo ocurre en el Teil 1 (variante
    # 4). En el Teil 2 las variantes vienen con su propia cabecera, así que ahí no
    # se parte nada.
    expandidos = []
    for b in bloques:
        partes = dividir_subvariantes(b["lineas"]) if b["teil"] == 1 else [b["lineas"]]
        for i, parte in enumerate(partes):
            expandidos.append({**b, "lineas": parte, "parte": i})
    return expandidos


def leer_opciones_t1(lineas):
    """Banco de palabras: una por línea o dos en columnas («a) GERNE f) ÜBER»)."""
    opciones, orden = {}, []
    for linea in lineas:
        limpia = linea.strip().strip("*").strip()
        if not limpia:
            continue
        marcas = list(re.finditer(r"(?:^|\s)([" + LETRAS_BANCO + r"])\)\s*", limpia))
        if not marcas:
            continue
        for k, m in enumerate(marcas):
            desde = m.end()
            hasta = marcas[k + 1].start() if k + 1 < len(marcas) else len(limpia)
            texto = limpia[desde:hasta].strip(" .*")
            clave = m.group(1).lower()
            if texto and clave not in opciones:
                opciones[clave] = texto
                orden.append(clave)
    return [{"key": k, "text": opciones[k]} for k in sorted(orden)]


def leer_opciones_t2(lineas):
    """Bloques «52. a) …» + «b) …» + «c) …», a veces con negrita y con erratas."""
    por_item, actual = {}, None
    for linea in lineas:
        limpia = linea.strip().strip("*").strip()
        if not limpia:
            continue
        cab = re.match(r"^(\d{2})\.\s*([a-c])\)\s*(.+)$", limpia, flags=re.IGNORECASE)
        if cab:
            actual = cab.group(1)
            por_item[actual] = []
            por_item[actual].append({"key": "a", "text": cab.group(3).strip(" .*")})
            continue
        op = re.match(r"^([a-c])\)\s*(.+)$", limpia, flags=re.IGNORECASE)
        if op and actual:
            por_item[actual].append({"key": op.group(1).lower(), "text": op.group(2).strip(" .*")})
    return por_item


def es_linea_de_opciones(limpia: str) -> bool:
    """¿Es una línea del banco (a-j) o de un bloque de opciones (52. a) …)?"""
    if re.match(r"^(\d{2}\.\s*)?[" + LETRAS_BANCO + r"]\)", limpia, flags=re.IGNORECASE):
        return True
    # Banco a dos columnas: «a) GERNE f) ÜBER»
    return bool(re.search(r"\s[" + LETRAS_BANCO + r"]\)\s", limpia))


def partir_cuerpo(lineas):
    """Separa título, texto y líneas de opciones."""
    titulo, cuerpo, opciones, notas = "", [], [], []
    visto_texto = False
    for linea in lineas:
        limpia = linea.strip()
        if not limpia or PAGE_RE.match(limpia) or re.fullmatch(r"\d{1,3}", limpia):
            continue
        # Las opciones van al final: hay que reconocerlas ANTES que al texto y antes
        # que a las notas, porque una opción con homóglifo cirílico («с)») parece rusa.
        clave = normalizar_clave(limpia)
        if es_linea_de_opciones(clave):
            opciones.append(clave)
            continue
        if es_nota(limpia):
            notas.append(limpia.strip("*").strip())
            continue
        solo_titulo = re.fullmatch(r"\*\*([^*]+)\*\*", limpia)
        # El título va antes del texto; una línea en negrita con huecos es texto.
        if solo_titulo and not visto_texto and not HUECO_RE.search(limpia):
            titulo = solo_titulo.group(1).strip()
            continue
        visto_texto = True
        cuerpo.append(limpia.replace("**", ""))
    return titulo, limpiar_guiones("\n".join(cuerpo)).strip(), opciones, notas


def frase_del_hueco(texto: str, n: str) -> str:
    """Contexto del hueco (una ventana de texto alrededor), para el enunciado del ítem."""
    plano = " ".join(texto.split())
    # Se coge una ventana de texto alrededor del hueco, no la frase entera: dos
    # huecos de la misma frase darían el mismo enunciado y build.py avisaría de un
    # «conflicto» que no existe. El hueco puede venir como `48 ( )` o como `48( )`.
    m = re.search(r"\b" + re.escape(n) + r"\s*\(\s*\)", plano)
    if not m:
        return ""
    ventana = 80
    ini, fin = max(0, m.start() - ventana), min(len(plano), m.end() + ventana)
    if ini > 0:
        esp = plano.find(" ", ini)
        ini = esp + 1 if esp != -1 else ini
    if fin < len(plano):
        esp = plano.rfind(" ", m.end(), fin)
        fin = esp if esp != -1 else fin
    return plano[ini:fin].strip()


def main():
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    fuente, destino = sys.argv[1], sys.argv[2]
    raiz = os.path.dirname(os.path.abspath(destino))
    ruta_resp = os.path.join(raiz, "sprachbausteine_respuestas.json")

    texto = open(fuente, encoding="utf-8").read()
    respuestas = {}
    if os.path.exists(ruta_resp):
        respuestas = json.load(open(ruta_resp, encoding="utf-8"))
    else:
        print(f"aviso: no existe {ruta_resp}; saldrá sin respuestas", file=sys.stderr)

    bloques = partir_secciones(texto)
    usados, t1, t2 = set(), [], []
    faltan, avisos, anomalias_t1 = [], [], []

    for b in bloques:
        titulo, cuerpo, lineas_op, notas = partir_cuerpo(b["lineas"])
        # El sufijo de la versión puede venir en el encabezado o en la nota rusa
        # que va debajo («Тест от 07.02.2025»).
        pista = (b["extra"] + " " + " ".join(notas)).strip()
        base = f"sb{b['teil']}-v{b['num']}"
        vid = base if base not in usados else base + sufijo_id(pista)
        while vid in usados:
            vid += "x"
        usados.add(vid)

        huecos = sorted({m.group(1) for m in HUECO_RE.finditer(cuerpo)})
        extra = etiqueta_extra(pista)
        etiqueta = f"Variante {b['num']}" + (f" ({extra})" if extra else "")

        if len(huecos) != 6:
            avisos.append(f"{vid}: {len(huecos)} huecos en vez de 6 -> {huecos}")

        if b["teil"] == 1:
            banco = leer_opciones_t1(lineas_op)
            if len(banco) != 10:
                avisos.append(f"{vid}: {len(banco)} palabras en el banco en vez de 10")
                anomalias_t1.append(
                    f"{vid} (p. {b['page']}): el original trae {len(banco)} palabras en el banco "
                    f"en vez de 10 ({', '.join(o['key'] for o in banco)}); se ha respetado lo que hay.")
            items = []
            for n in huecos:
                r = (respuestas.get(vid) or {}).get(n) or {}
                items.append({
                    "n": int(n),
                    "type": "choice",
                    "prompt": frase_del_hueco(cuerpo, n),
                    "answer": r.get("answer", ""),
                    "confidence": r.get("confidence", "niedrig"),
                    "quote": r.get("quote", ""),
                    "explain": r.get("explain", ""),
                    "explain_ru": r.get("explain_ru", ""),
                })
            t1.append({
                "id": vid, "label": etiqueta, "page": b["page"], "kind": "zuordnung",
                "intro": "Lesen Sie den Brief. Welches Wort (a-j) passt in jede Lücke (46-51)? "
                         "Vier Wörter bleiben übrig.",
                "optionsLabel": "Wörter",
                "passage": (titulo + "\n\n" + cuerpo).strip() if titulo else cuerpo,
                "options": banco, "items": items,
            })
        else:
            ops = leer_opciones_t2(lineas_op)
            items = []
            for n in huecos:
                r = (respuestas.get(vid) or {}).get(n) or {}
                opciones = ops.get(n, [])
                if len(opciones) != 3:
                    avisos.append(f"{vid}#{n}: {len(opciones)} opciones en vez de 3")
                items.append({
                    "n": int(n),
                    "type": "choice",
                    "prompt": frase_del_hueco(cuerpo, n),
                    "options": opciones,
                    "answer": r.get("answer", ""),
                    "confidence": r.get("confidence", "niedrig"),
                    "quote": r.get("quote", ""),
                    "explain": r.get("explain", ""),
                    "explain_ru": r.get("explain_ru", ""),
                })
            t2.append({
                "id": vid, "label": etiqueta, "page": b["page"], "kind": "text",
                "intro": "Lesen Sie den Text. Welche Lösung (a, b oder c) passt in jede Lücke (52-57)?",
                "passage": (titulo + "\n\n" + cuerpo).strip() if titulo else cuerpo,
                "items": items,
            })

    def volcar(nombre, section, variantes, bloque, descartadas=(), anomalias=()):
        ruta = os.path.join(destino, nombre)
        datos = {"block": bloque, "section": section, "variants": variantes, "fixes": [
            "p. 91-94: las letras de opción venían a veces con homóglifos cirílicos "
            "(«а)», «с)»); normalizadas a latinas.",
            "Se han unido las palabras que el PDF partía al final de línea («Ausbildungs-\\nkonzept»).",
        ] + list(anomalias) + [
            f"{d['id']}: descartada; el original no trae las tres opciones en todos los huecos."
            for d in descartadas]}
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=1)
            f.write("\n")
        return ruta

    # Una variante del Teil 2 (la del test 160201) trae solo la opción a) en casi
    # todos los huecos: el PDF perdió b) y c). Sin las tres opciones el ejercicio no
    # se puede hacer, así que se descarta en vez de ofrecerlo mal.
    descartadas = [v for v in t2 if any(len(it["options"]) != 3 for it in v["items"])]
    if descartadas:
        t2 = [v for v in t2 if v not in descartadas]
        for v in descartadas:
            avisos.append(f"{v['id']}: descartada (faltan opciones en el original)")

    # Solo se exige respuesta a lo que de verdad se publica: una variante descartada
    # por incompleta no necesita clave.
    for v in t1 + t2:
        for it in v["items"]:
            if not (it.get("answer") or "").strip():
                faltan.append(f"{v['id']}#{it['n']}")

    r1 = volcar("sprachbausteine_t1.json", "sprachbausteine-t1", t1, "sprachbausteine_t1")
    r2 = volcar("sprachbausteine_t2.json", "sprachbausteine-t2", t2, "sprachbausteine_t2", descartadas)

    print(f"Teil 1: {len(t1)} variantes -> {r1}")
    print(f"Teil 2: {len(t2)} variantes -> {r2}")
    for a in avisos:
        print("  aviso:", a)
    if faltan:
        print(f"\nFALTAN {len(faltan)} respuestas en {ruta_resp}:")
        for f in faltan:
            print("   ", f)
        return 1
    print("\nTodas las respuestas están cubiertas.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
