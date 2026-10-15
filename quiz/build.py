#!/usr/bin/env python3
"""Valida los JSON de preguntas y construye el HTML autocontenido.

Uso:
    python build.py <datadir> <template> <salida.html>
"""
import glob
import json
import os
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

CONF = {"hoch", "mittel", "niedrig"}
SECTIONS = {
    "lesen-t1": "Lesen Teil 1",
    "lesen-t2": "Lesen Teil 2",
    "lesen-t3": "Lesen Teil 3",
    "lesen-t4": "Lesen Teil 4",
    "lesen-us": "Lesen und Schreiben (Lesen)",
    "schreiben-beschwerde": "Schreiben: Beschwerde-E-Mail",
    "schreiben-forum": "Schreiben: Forumsbeitrag",
    "hoeren-t1": "Hören Teil 1",
    "hoeren-t2": "Hören Teil 2",
    "hoeren-t3": "Hören Teil 3",
    "hoeren-t4": "Hören Teil 4",
}
ORDER = list(SECTIONS)


def norm_ws(s) -> str:
    """Normaliza espacios para comparar citas con el texto del que salen."""
    return " ".join(str(s or "").split())


def validate(variant, errors, warns, infos):
    vid = variant.get("id", "<sin id>")

    def err(m):
        errors.append(f"[{vid}] {m}")

    def warn(m):
        warns.append(f"[{vid}] {m}")

    kind = variant.get("kind")
    if kind not in ("zuordnung", "text", "schreiben"):
        err(f"kind inválido: {kind!r}")
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
        if len(set(answers)) != len(answers):
            err(f"las respuestas se repiten (cada opción se usa una vez): {answers}")
        for a in answers:
            if a not in keys:
                err(f"respuesta «{a}» no está entre las opciones")
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
        for it in items:
            q = norm_ws(it.get("quote"))
            ans = str(it.get("answer", "")).lower()
            base = pool.get(ans)
            if q and base and q not in base:
                warn(f"ítem {it.get('n')}: la cita NO aparece en la opción "
                     f"{ans} que se le asigna: «{q[:70]}…»")

    # --- items ---
    for it in items:
        n = it.get("n", "?")
        if it.get("type") not in ("choice", "truefalse"):
            err(f"ítem {n}: type inválido {it.get('type')!r}")
        if not (it.get("prompt") or "").strip():
            err(f"ítem {n}: prompt vacío")
        if not (it.get("quote") or "").strip():
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
    nvar = nitem = 0
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
                conf_count[str(it.get("confidence", "?")).lower()] = \
                    conf_count.get(str(it.get("confidence", "?")).lower(), 0) + 1
            by_section.setdefault(sec, []).append(v)
            nvar += 1
            nitem += len(v.get("items", []))

    print(f"ficheros: {len(files)} · variantes: {nvar} · ítems: {nitem}")
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

    seen_prompt = {}
    for sec_variants in by_section.values():
        for v in sec_variants:
            passage = norm(v.get("passage"))
            for it in v.get("items", []):
                p = norm(it.get("prompt"))
                if len(p) < 12:
                    continue
                a = str(it.get("answer", "")).lower()
                cur = (a, v.get("id"), opt_sig(it), passage)
                if p not in seen_prompt:
                    seen_prompt[p] = cur
                    continue
                prev = seen_prompt[p]
                if prev[0] == a:
                    continue
                same_opts = prev[2] == cur[2]
                same_text = prev[3] == cur[3] and prev[3] != ""
                where = f"«{p[:58]}…» → {prev[0]} ({prev[1]}) vs {a} ({cur[1]})"
                if same_opts and same_text:
                    warns.append("CONFLICTO probable, mismo texto y opciones: " + where)
                elif same_opts:
                    infos.append("mismo enunciado y opciones, distinto texto "
                                 "(cambio de versión, esperado): " + where)
                else:
                    infos.append("mismo enunciado, opciones distintas "
                                 "(pregunta distinta, sin conflicto): " + where)

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
        vs = sorted(by_section[sid], key=lambda v: (v.get("page", 0), v.get("id", "")))
        for v in vs:
            ok_ns = set(verified.get(v.get("id"), []))
            for it in v.get("items", []):
                if it.get("n") in ok_ns:
                    it["verified"] = True
                    nver += 1
        sections.append({"id": sid, "title": SECTIONS[sid], "variants": vs})

    payload = {"generated": True, "sections": sections}
    tpl = open(template, encoding="utf-8").read()
    html = tpl.replace("/*__DATA__*/", json.dumps(payload, ensure_ascii=False))
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(html)

    print(f"\nOK -> {out}  ({len(html):,} bytes, {len(sections)} secciones)")
    print(f"   respuestas con verificación independiente: {nver}/{nitem}")
    for s in sections:
        print(f"   {s['title']:35} {len(s['variants']):>3} variantes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
