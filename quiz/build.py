#!/usr/bin/env python3
"""Valida los JSON de preguntas y construye el HTML autocontenido.

Uso:
    python build.py <datadir> <template> <salida.html>
"""
import glob
import json
import os
import re
import sys

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

try:
    from prompt_schreiben import SYSTEM_PROMPT, JSON_SCHEMA
except ImportError:
    from quiz.prompt_schreiben import SYSTEM_PROMPT, JSON_SCHEMA

CONF = {"hoch", "mittel", "niedrig"}
SECTIONS = {
    "lesen-t1": "Lesen Teil 1",
    "lesen-t2": "Lesen Teil 2",
    "lesen-t3": "Lesen Teil 3",
    "lesen-t4": "Lesen Teil 4",
    "lesen-us": "Lesen und Schreiben (Lesen)",
    "sprachbausteine-t1": "Sprachbausteine Teil 1",
    "sprachbausteine-t2": "Sprachbausteine Teil 2",
    "schreiben-beschwerde": "Schreiben: Beschwerde-E-Mail",
    "schreiben-forum": "Schreiben: Forumsbeitrag",
    "hoeren-t1": "Hören Teil 1",
    "hoeren-t2": "Hören Teil 2",
    "hoeren-t3": "Hören Teil 3",
    "hoeren-t4": "Hören Teil 4",
    "sprechen-t2": "Sprechen Teil 2 · Smalltalk",
    "sprechen-t3": "Sprechen Teil 3 · Lösungswege",
    "modeltest-11": "Modeltest 11",
    "modeltest-12": "Modeltest 12",
    "modeltest-13": "Modeltest 13",
    "modeltest-14": "Modeltest 14",
    "modeltest-15": "Modeltest 15",
    "modeltest-16": "Modeltest 16",
    "modeltest-17": "Modeltest 17",
}
ORDER = list(SECTIONS)


def validate_smalltalk(variant, err, warn):
    """Validación de las tarjetas de Smalltalk (Sprechen Teil 2)."""
    for f in ("id", "label", "page", "kind", "intro", "cards"):
        if f not in variant:
            err(f"falta el campo obligatorio «{f}» para kind=smalltalk")
    cards = variant.get("cards") or []
    if not cards:
        err("no tiene tarjetas")
        return
    nums = []
    for c in cards:
        n = c.get("n")
        if not isinstance(n, int) or n < 1:
            err(f"tarjeta con número inválido: {n!r}")
            continue
        nums.append(n)
        for campo in ("de", "es", "ru"):
            if not (c.get(campo) or "").strip():
                err(f"tarjeta {n}: «{campo}» vacío")
        if not isinstance(c.get("alt", []), list):
            err(f"tarjeta {n}: «alt» debe ser una lista")
        elif any(not str(a).strip() for a in c["alt"]):
            err(f"tarjeta {n}: alternativa vacía en «alt»")
    if len(set(nums)) != len(nums):
        repetidos = sorted({x for x in nums if nums.count(x) > 1})
        err(f"números de tarjeta repetidos: {repetidos}")
    elif nums and sorted(nums) != list(range(1, len(nums) + 1)):
        err(f"la numeración de las tarjetas debe ser 1..{len(nums)} sin huecos")
    if len(cards) < 20:
        warn(f"mazo muy corto: {len(cards)} tarjetas")


def norm_ws(s) -> str:
    """Normaliza espacios para comparar citas con el texto del que salen."""
    return " ".join(str(s or "").split())


def validate_situation(variant, err, warn):
    """Validación de una situación de Sprechen Teil 3.

    Tampoco se corrige: es un caso para discutir una solución. Cada variante es
    UNA situación, con su alemán verbatim, su ayuda en los dos idiomas, los
    Stichpunkte traducidos y al menos dos ejemplos de habla.
    """
    for f in ("id", "label", "page", "kind", "n", "titel", "de", "es", "ru",
              "punkte", "beispiele"):
        if f not in variant:
            err(f"falta el campo obligatorio «{f}» para kind=situation")
    n = variant.get("n")
    if not isinstance(n, int) or n < 1:
        err(f"número de situación inválido: {n!r}")
    for campo in ("titel", "de", "es", "ru"):
        if not (variant.get(campo) or "").strip():
            err(f"situación {n}: «{campo}» vacío")
    puntos = variant.get("punkte") or []
    if not isinstance(puntos, list) or not puntos:
        err(f"situación {n}: sin Stichpunkte")
    for p in puntos:
        if not isinstance(p, dict):
            err(f"situación {n}: Stichpunkt sin estructura")
            continue
        for campo in ("de", "es", "ru"):
            if not (p.get(campo) or "").strip():
                err(f"situación {n}: Stichpunkt sin «{campo}»: {(p.get('de') or '')[:40]}")
    ejemplos = variant.get("beispiele") or []
    if not isinstance(ejemplos, list) or len(ejemplos) < 2:
        err(f"situación {n}: menos de dos ejemplos en alemán")
    elif any(not str(e).strip() for e in ejemplos):
        err(f"situación {n}: ejemplo vacío")


def validate_ohne_key(variant, err, warn):
    """Validación de un bloque sin clave (Hören de los Modeltests).

    No hay audio ni transcripción en el origen, así que no se puede deducir la
    respuesta. Se exigen enunciados y opciones completos, pero ni `answer` ni
    `quote` ni `confidence`: la app deja elegir y no corrige.
    """
    for f in ("id", "label", "page", "kind", "intro", "items"):
        if f not in variant:
            err(f"falta el campo obligatorio «{f}» para kind=ohne-key")
    items = variant.get("items") or []
    if not items:
        err("no tiene ítems")
        return
    pool = variant.get("options") or []
    if pool:
        claves = [str(o.get("key", "")).lower() for o in pool]
        if len(set(claves)) != len(claves):
            err("opciones globales con clave duplicada")
        for o in pool:
            if not (o.get("text") or o.get("title") or "").strip():
                err(f"opción global {o.get('key')} sin texto")
        for it in items:
            if not (it.get("prompt") or "").strip():
                err(f"ítem {it.get('n')}: prompt vacío")
    else:
        for it in items:
            n = it.get("n")
            if it.get("type") not in ("choice", "truefalse"):
                err(f"ítem {n}: type inválido {it.get('type')!r}")
            if not (it.get("prompt") or "").strip():
                err(f"ítem {n}: prompt vacío")
            opciones = it.get("options") or []
            if not opciones:
                err(f"ítem {n}: sin opciones")
            claves = [str(o.get("key", "")).lower() for o in opciones]
            if len(set(claves)) != len(claves):
                err(f"ítem {n}: claves de opción duplicadas")
            for o in opciones:
                if not (o.get("text") or "").strip():
                    err(f"ítem {n}: opción {o.get('key')} sin texto")


def validate(variant, errors, warns, infos):
    vid = variant.get("id", "<sin id>")

    def err(m):
        errors.append(f"[{vid}] {m}")

    def warn(m):
        warns.append(f"[{vid}] {m}")

    kind = variant.get("kind")
    if kind not in ("zuordnung", "text", "schreiben", "smalltalk", "situation", "ohne-key"):
        err(f"kind inválido: {kind!r}")
        return

    if kind == "ohne-key":
        validate_ohne_key(variant, err, warn)
        return

    if kind == "situation":
        validate_situation(variant, err, warn)
        return

    if kind == "smalltalk":
        # Sin clave y sin cita: no se responde, se habla. Lo que sí se exige es
        # que cada tarjeta tenga su alemán y su ayuda en los dos idiomas, porque
        # la app las pinta como texto y no hay dónde caer.
        validate_smalltalk(variant, err, warn)
        return

    if kind == "schreiben":
        for f in ("id", "label", "page", "kind", "category", "topic", "prompt", "leitpunkte"):
            if f not in variant:
                err(f"falta el campo obligatorio «{f}» para kind=schreiben")
        cat = variant.get("category")
        if cat not in ("beschwerde", "forum"):
            err(f"category inválida en schreiben: {cat!r}")
        lps = variant.get("leitpunkte") or []
        if len(lps) < 4:
            warn(f"tiene menos de 4 Leitpunkte: {len(lps)}")
        if cat == "beschwerde":
            if not variant.get("source_letter"):
                warn("beschwerde sin source_letter")
            if not variant.get("boss_instructions"):
                warn("beschwerde sin boss_instructions")
        return

    for f in ("id", "label", "page", "kind", "intro", "items"):
        if f not in variant:
            err(f"falta el campo obligatorio «{f}»")

    items = variant.get("items") or []
    if not items:
        err("no tiene ítems")

    # --- zuordnung ---
    # Teil 1 usa 5 personas ↔ 8 anuncios; Teil 3 usa 4 posteos ↔ 6 respuestas.
    # La forma cambia, la regla no: cada opción se usa como máximo una vez, así
    # que las respuestas han de ser distintas y salir del pool de opciones.
    if kind == "zuordnung":
        opts = variant.get("options") or []
        keys = [str(o.get("key", "")).lower() for o in opts]
        if len(keys) < 4:
            warn(f"pocas opciones en el pool: {len(keys)}")
        if len(set(keys)) != len(keys):
            err("claves de opción duplicadas")
        for o in opts:
            if not (o.get("text") or "").strip():
                err(f"opción {o.get('key')} sin texto")
        answers = [str(i.get("answer", "")).lower() for i in items]
        permitir_x = bool(variant.get("allowNone"))
        if len(set(answers)) != len(answers):
            err(f"las respuestas se repiten (cada opción se usa una vez): {answers}")
        for a in answers:
            if a == "x" and permitir_x:
                continue
            if a not in keys:
                err(f"respuesta «{a}» no está entre las opciones")
        if permitir_x:
            if answers.count("x") > 1:
                err("sólo una pregunta puede quedar sin consejo (x)")
            elif "x" not in answers:
                warn("allowNone está activo pero ninguna respuesta es x")
        unused = sorted(set(keys) - set(answers))
        if len(unused) == 0:
            warn("no sobra ninguna opción: ¿faltan distractores?")
        else:
            infos.append(f"[{vid}] {len(items)} ítems ↔ {len(keys)} opciones, "
                         f"{len(unused)} sin usar: {unused}")

    # --- text ---
    if kind == "text":
        if not (variant.get("passage") or "").strip():
            err("kind=text sin «passage» (el texto de lectura)")
        elif len(variant["passage"]) < 300:
            warn(f"passage muy corto ({len(variant['passage'])} chars): ¿está completo?")

    # --- literalidad de las citas ---
    # El SPEC exige que `quote` sea una frase COPIADA del texto. Una cita
    # parafraseada o empalmada con "[…]" no permite verificar el razonamiento,
    # que es justo para lo que sirve. Aquí se comprueba automáticamente.
    if kind == "text":
        pas = norm_ws(variant.get("passage"))
        if pas:
            for it in items:
                q = norm_ws(it.get("quote"))
                if q and q not in pas:
                    warn(f"ítem {it.get('n')}: la cita NO es literal del texto "
                         f"(¿parafraseada o empalmada?): «{q[:70]}…»")
    elif kind == "zuordnung":
        # La cita puede empezar por el TITULAR de la opción, que forma parte
        # de ella igual que el cuerpo, así que se comparan los dos juntos.
        pool = {str(o.get("key", "")).lower():
                norm_ws((o.get("title") or "") + " " + (o.get("text") or ""))
                for o in (variant.get("options") or [])}
        pas = norm_ws(variant.get("passage"))
        for it in items:
            q = norm_ws(it.get("quote"))
            ans = str(it.get("answer", "")).lower()
            base = pool.get(ans)
            # En un ejercicio de huecos (Sprachbausteine Teil 1) la opción es UNA
            # palabra, así que la cita no puede estar dentro de ella: la cita es la
            # frase del texto, con el hueco marcado. Se aceptan las dos formas.
            if q and not ((base and q in base) or (pas and q in pas)):
                warn(f"ítem {it.get('n')}: la cita NO aparece ni en la opción "
                     f"{ans} que se le asigna ni en el texto: «{q[:70]}…»")

    # --- items ---
    for it in items:
        n = it.get("n", "?")
        if it.get("type") not in ("choice", "truefalse"):
            err(f"ítem {n}: type inválido {it.get('type')!r}")
        if not (it.get("prompt") or "").strip():
            err(f"ítem {n}: prompt vacío")
        es_x = (str(it.get("answer", "")).lower() == "x"
                and bool(variant.get("allowNone")))
        if not (it.get("quote") or "").strip() and not es_x:
            err(f"ítem {n}: quote vacío (es obligatorio)")
        if not (it.get("explain") or "").strip():
            err(f"ítem {n}: explain vacío")
        c = str(it.get("confidence", "")).lower()
        if c not in CONF:
            err(f"ítem {n}: confidence inválida {it.get('confidence')!r}")

        ans = str(it.get("answer", "")).lower()
        if it.get("type") == "truefalse":
            if ans not in ("richtig", "falsch"):
                err(f"ítem {n}: answer debe ser Richtig/Falsch, es {ans!r}")
        elif kind == "text":
            okeys = [str(o.get("key", "")).lower() for o in (it.get("options") or [])]
            if not okeys:
                err(f"ítem {n}: no tiene opciones")
            elif ans not in okeys:
                err(f"ítem {n}: answer «{ans}» no está entre las opciones {okeys}")

    # --- números de ítem repetidos ---
    # El PDF original repite numeración en dos variantes: t2_b-p23 (6, 6, 7) y
    # t4_c-p51 (14, 15, 15, 16, 17, 18). No viene del extractor: el documento lo
    # trae así y se copia literal. Avisa, no bloquea, porque el número identifica
    # el ítem en dos sitios que entonces se confunden: la insignia de
    # «2ª lectura» (verified.json va por número) y lo que el alumno ya respondió.
    vistos = set()
    for it in items:
        n = it.get("n")
        if n in vistos:
            warn(f"ítem {n} repetido en «{variant.get('id')}»: el original repite "
                 f"numeración, así que «2ª lectura» y la respuesta guardada marcan "
                 f"los dos ítems con un solo número")
        vistos.add(n)


def main():
    datadir, template, out = sys.argv[1], sys.argv[2], sys.argv[3]

    files = sorted(glob.glob(os.path.join(datadir, "*.json")))

    # Respuestas que han pasado una segunda lectura independiente.
    # Formato: {"t1-v1": [1,2,3,4,5], "t2_b-p22a": [6,7]}
    vpath = os.path.join(os.path.dirname(os.path.abspath(datadir)), "verified.json")
    verified = {}
    if os.path.exists(vpath):
        try:
            verified = json.load(open(vpath, encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(f"aviso: verified.json ilegible ({e}); se ignora", file=sys.stderr)

    if not files:
        print("no hay ficheros de datos", file=sys.stderr)
        return 1

    errors, warns, infos = [], [], []
    by_section = {}
    seen_ids = set()
    nvar = nitem = ncard = nsit = nitem_clave = 0
    conf_count = {}

    for path in files:
        try:
            data = json.load(open(path, encoding="utf-8"))
        except json.JSONDecodeError as e:
            errors.append(f"[{os.path.basename(path)}] JSON inválido: {e}")
            continue
        sec = data.get("section")
        if sec not in SECTIONS:
            errors.append(f"[{os.path.basename(path)}] section desconocida: {sec!r}")
            continue
        for v in data.get("variants", []):
            if v.get("id") in seen_ids:
                errors.append(f"id duplicado en todo el proyecto: {v.get('id')}")
            seen_ids.add(v.get("id"))
            validate(v, errors, warns, infos)
            for it in v.get("items", []):
                if "confidence" not in it:
                    continue
                conf_count[str(it.get("confidence", "?")).lower()] = \
                    conf_count.get(str(it.get("confidence", "?")).lower(), 0) + 1
            by_section.setdefault(sec, []).append(v)
            nvar += 1
            nitem += len(v.get("items", []))
            nitem_clave += sum(1 for it in v.get("items", []) if "answer" in it)
            ncard += len(v.get("cards", []))
            if v.get("kind") == "situation":
                nsit += 1

    print(f"ficheros: {len(files)} · variantes: {nvar} · ítems: {nitem}"
          + (f" (con clave: {nitem_clave}, sin clave: {nitem - nitem_clave})" if nitem != nitem_clave else "")
          + (f" · tarjetas: {ncard}" if ncard else "")
          + (f" · situaciones: {nsit}" if nsit else ""))
    print("confianza:", dict(sorted(conf_count.items())))

    # --- coherencia entre variantes ---
    # Un mismo enunciado debería llevar la misma respuesta, aunque la variante
    # lo numere distinto. Pero hay dos casos legítimos que NO son errores:
    #   - el texto de lectura cambió entre versiones (p. ej. "cada 3 años" pasó
    #     a "cada año") → la respuesta se invierte a propósito;
    #   - las opciones son distintas, así que la pregunta no es la misma.
    # Solo es un conflicto real si enunciado, opciones Y texto coinciden.
    def norm(s):
        return " ".join(str(s or "").lower().replace("–", "-").split()).strip(" .!?")

    def opt_sig(it):
        return tuple(sorted(norm(o.get("text") or o.get("key"))
                            for o in (it.get("options") or [])))

    def palabra_respuesta(v, it):
        """Palabra que señala la respuesta.

        Hace falta porque una misma versión puede traer el banco con las letras
        renumeradas: entonces la respuesta es la misma palabra con otra letra, y
        comparar letras daría un «conflicto» que no existe.
        """
        ans = str(it.get("answer", "")).lower()
        for o in list(it.get("options") or []) + list(v.get("options") or []):
            if str(o.get("key", "")).lower() == ans:
                return norm(o.get("text") or "")
        return ans

    seen_prompt = {}
    for sec_variants in by_section.values():
        for v in sec_variants:
            passage = norm(v.get("passage"))
            for it in v.get("items", []):
                p = norm(it.get("prompt"))
                if len(p) < 12:
                    continue
                a = str(it.get("answer", "")).lower()
                cur = (a, v.get("id"), opt_sig(it), passage, palabra_respuesta(v, it))
                if p not in seen_prompt:
                    seen_prompt[p] = cur
                    continue
                prev = seen_prompt[p]
                if prev[0] == a:
                    continue
                same_opts = prev[2] == cur[2]
                same_text = prev[3] == cur[3] and prev[3] != ""
                where = f"«{p[:58]}…» → {prev[0]} ({prev[1]}) vs {a} ({cur[1]})"
                if same_opts and same_text and prev[4] == cur[4] and prev[4]:
                    infos.append("misma respuesta con otra letra (banco renumerado): " + where)
                elif same_opts and same_text:
                    warns.append("CONFLICTO probable, mismo texto y opciones: " + where)
                elif same_opts:
                    infos.append("mismo enunciado y opciones, distinto texto "
                                 "(cambio de versión, esperado): " + where)
                else:
                    infos.append("mismo enunciado, opciones distintas "
                                 "(pregunta distinta, sin conflicto): " + where)

    # --- cobertura del catálogo de Schreiben ---
    # La parte de lectura (sección «lesen-us») ya trae las variantes 1-9 del
    # bloque Beschwerde (pp. 66-77). Si una variante tiene lectura pero no tarea
    # de redacción, al catálogo le falta contenido: pasó con las variantes 3, 8
    # y 9, que estuvieron meses sin su tarea de escritura sin que nadie lo notara.
    nums_lesen = set()
    for v in by_section.get("lesen-us", []):
        for m in re.finditer(r"Variante (\d+)", str(v.get("label") or "")):
            nums_lesen.add(int(m.group(1)))
    nums_schreiben = {v.get("source_variant")
                      for v in by_section.get("schreiben-beschwerde", [])}
    sin_tarea = sorted(n for n in nums_lesen if n not in nums_schreiben)
    if sin_tarea:
        errors.append("Beschwerde: variantes con lectura pero sin tarea de redacción: "
                      + ", ".join(f"Nº {n}" for n in sin_tarea))

    # --- orden del catálogo de Forumsbeitrag ---
    # El menú se ordena por (página, num). Un `num` repetido o con huecos
    # descoloca el bloque respecto al PDF: las entradas 64-66 tenían página 104
    # y se colaban entre la 44 y la 45.
    nums_foro = [v.get("num") for v in by_section.get("schreiben-forum", [])]
    if any(n is None for n in nums_foro):
        errors.append("Forumsbeitrag: hay entradas sin `num` (orden del PDF)")
    elif len(set(nums_foro)) != len(nums_foro):
        errors.append("Forumsbeitrag: `num` repetido en el catálogo")
    elif sorted(nums_foro) != list(range(1, len(nums_foro) + 1)):
        errors.append("Forumsbeitrag: la numeración debe ser 1..N sin huecos")

    # --- orden de las situaciones de Sprechen T3 ---
    # Cada situación es una entrada de menú, como los Forumsbeiträge: el número
    # que lleva en el nombre es el del documento y manda el orden.
    nums_sit = [v.get("n") for v in by_section.get("sprechen-t3", [])]
    if any(n is None for n in nums_sit):
        errors.append("Sprechen T3: hay situaciones sin `n`")
    elif len(set(nums_sit)) != len(nums_sit):
        errors.append("Sprechen T3: `n` repetido")
    elif nums_sit and sorted(nums_sit) != list(range(1, len(nums_sit) + 1)):
        errors.append("Sprechen T3: la numeración debe ser 1..N sin huecos")

    if infos:
        print(f"\n--- INFORMATIVO ({len(infos)}) ---")
        for i in infos:
            print("  ", i)

    if warns:
        print(f"\n--- AVISOS ({len(warns)}) ---")
        for w in warns[:60]:
            print("  ", w)
        if len(warns) > 60:
            print(f"   ... y {len(warns)-60} más")

    if errors:
        print(f"\n--- ERRORES ({len(errors)}) ---")
        for e in errors[:80]:
            print("  ", e)
        if len(errors) > 80:
            print(f"   ... y {len(errors)-80} más")
        print("\nNo se genera el HTML hasta que no haya errores.")
        return 1

    sections = []
    nver = 0
    for sid in ORDER:
        if sid not in by_section:
            continue
        # `num` es la posición en el PDF (solo lo usan los Forumsbeiträge);
        # donde no existe, 0 y decide el id.
        vs = sorted(by_section[sid], key=lambda v: (v.get("page", 0), v.get("num", 0), v.get("id", "")))
        for v in vs:
            ok_ns = set(verified.get(v.get("id"), []))
            for it in v.get("items", []):
                if it.get("n") in ok_ns:
                    it["verified"] = True
                    nver += 1
        sections.append({"id": sid, "title": SECTIONS[sid], "variants": vs})

    payload = {
        "generated": True,
        "sections": sections,
        "prompt_schreiben": {
            "system_prompt": SYSTEM_PROMPT,
            "json_schema": JSON_SCHEMA
        }
    }
    tpl = open(template, encoding="utf-8").read()
    html = tpl.replace("/*__DATA__*/", json.dumps(payload, ensure_ascii=False))
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(html)

    print(f"\nOK -> {out}  ({len(html):,} bytes, {len(sections)} secciones)")
    print(f"   respuestas con verificación independiente: {nver}/{nitem_clave}")
    for s in sections:
        print(f"   {s['title']:35} {len(s['variants']):>3} variantes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
