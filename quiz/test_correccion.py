# -*- coding: utf-8 -*-
"""
test_correccion.py - Regresión del corrector, con el caso real que lo destapó.

Contexto: una redacción B2 (Forumsbeitrag) se evaluó con el prompt viejo. El
modelo devolvió cinco "errores", y dos de ellos estaban mal analizados:

  #2 «und diese nicht noch mehr Arbeit» → «die nicht noch mehr Arbeit»
     (propone un pronombre relativo que no existe, porque tras «und» el sujeto
      de la subordinada va en nominativo o se omite)
  #5 «beteiligten faire Lösung» → «beteiligte faire Lösung / beteiligten faire Lösung»
     (no había error de declinación: la terminación -en ya era correcta; solo
      faltaba la mayúscula de «Beteiligten». Y la segunda "opción" es idéntica
      al original.)

Además el "texto corregido" reescribía el contenido y borraba la coma de
«Liebe Grüße,».

Este test fija tres cosas:
  1. El validador caza los defectos mecánicos (falta `change`, span gigante,
     alternativas, corrección no aplicada).
  2. Una corrección bien hecha pasa sin ruido.
  3. El prompt conserva los guardarraíles que evitan repetir estos fallos.
"""

import json
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from prompt_schreiben import (SYSTEM_PROMPT, JSON_SCHEMA, build_user_prompt,
                              count_words, validate_evaluation_json)

# ---------------------------------------------------------------------------
# Texto real del alumno (tal como lo recibió el corrector)
# ---------------------------------------------------------------------------
STUDENT_TEXT = """Liebe Kolleginnen und Kollegen,

ich möchte mich an der aktuellen Diskussion zum Thema zusätzliche Aufgaben ohne Neueinstellungen beteiligen.

Meiner Ansicht nach ist diese Maßnahme ein wichtiger Schritt, weil viele Mitarbeite schon jede Woche Überstunden machen, und diese nicht noch mehr Arbeit pro Woche leisten können.

Was die Vor- und Nachteile betrifft, so bietet eine solche Mehrarbeit zwar kurzfristig die Möglichkeit, Engpässe zu überbrücken, führt jedoch langfristig zu Überlastung und Unzufriedenheit im Team.

Ein weiterer Aspekt, der unbedingt bedacht werden sollte, betrifft unsere Gesundheit und World-Life-Balance.

Aus meiner persönlichen Erfahrung kann ich berichten, dass Zusätzliche Aufgaben keine gute Idee sind.

Um eine für alle beteiligten faire Lösung zu finden, schlage ich vor, dass wir zwei Gruppen bilden. Eine Gruppe, die nicht mehr arbeiten kann, und eine zweite Gruppe, die diese zusätzlichen Aufgaben übernimmt.

Ich bin gespannt auf die Meinungen und Argumente der anderen Kolleginnen und Kollegen.

Liebe Grüße,
Sergio"""


def _criteria(grades=("B", "A", "C", "B"), scores=(26, 22, 9, 17)):
    g1, g2, g3, g4 = grades
    s1, s2, s3, s4 = scores
    return {
        "aufgabenbewaeltigung": {
            "grade": g1, "score": s1,
            "leitpunkte_check": [
                {"point": "Bezug auf die Diskussion", "covered": True, "comment": "Vorhanden."},
                {"point": "Vor- und Nachteile", "covered": True, "comment": "Ausgeführt."},
                {"point": "Eigene Erfahrung", "covered": True, "comment": "Knapp, aber vorhanden."},
                {"point": "Eigener Vorschlag", "covered": True, "comment": "Zwei Gruppen; der Satz ist aber ein Fragment."},
            ],
            "feedback": "Los cuatro puntos guía están tratados; el cierre es algo escueto.",
        },
        "angemessenheit": {"grade": g2, "score": s2,
                           "feedback": "Registro adecuado para un foro interno; «keine gute Idee» roza lo coloquial."},
        "korrektheit": {"grade": g3, "score": s3,
                        "feedback": "Erratas de mayúsculas y de caso; además una coma sobrante."},
        "repertoire": {"grade": g4, "score": s4,
                       "feedback": "Buen vocabulario laboral; faltan Nomen-Verb-Verbindungen."},
    }


# ---------------------------------------------------------------------------
# Salida REAL del modelo con el prompt viejo (los cinco "errores" de la captura)
# ---------------------------------------------------------------------------
BAD_EVAL = {
    "verdict": "BESTANDEN",
    "score_total": 74,
    "word_count": 176,
    "criteria": _criteria(),
    "critical_errors": [
        {
            "original": "viele Mitarbeite schon",
            "correction": "viele Mitarbeiter schon",
            "rule_es": "Falta la letra 'r' final en la palabra 'Mitarbeiter'.",
            "type": "Rechtschreibung",
        },
        {
            "original": "und diese nicht noch mehr Arbeit",
            "correction": "die nicht noch mehr Arbeit",
            "rule_es": "En lugar de 'und diese', el pronombre relativo 'die' es más adecuado para conectar la oración subordinada.",
            "type": "Grammatik",
        },
        {
            "original": "World-Life-Balance",
            "correction": "Work-Life-Balance",
            "rule_es": "El término anglicismo correcto es 'Work-Life-Balance', no 'World-Life-Balance'.",
            "type": "Wortschatz",
        },
        {
            # La app marcó la oración entera (91 caracteres) por una sola mayúscula
            "original": "Aus meiner persönlichen Erfahrung kann ich berichten, dass Zusätzliche Aufgaben keine gute Idee sind.",
            "correction": "Aus meiner persönlichen Erfahrung kann ich berichten, dass zusätzliche Aufgaben keine gute Idee sind.",
            "rule_es": "Los adjetivos usados como sustantivos o comunes dentro de la oración deben ir en minúscula.",
            "type": "Rechtschreibung",
        },
        {
            "original": "beteiligten faire Lösung",
            "correction": "beteiligte faire Lösung / beteiligten faire Lösung",
            "rule_es": "Error en la declinación del adjetivo antes de un sustantivo con artículo implícito o débil.",
            "type": "Grammatik",
        },
    ],
    "strengths": ["Estructura clara en párrafos.", "Registro adecuado al foro interno."],
    "areas_for_improvement": ["Revisar la puntuación de las subordinadas."],
    "corrected_version": (
        "Liebe Kolleginnen und Kollegen,\n\n"
        "ich möchte mich an der aktuellen Diskussion zum Thema zusätzliche Aufgaben ohne "
        "Neueinstellungen beteiligen.\n\n"
        "Meiner Ansicht nach ist diese Maßnahme ein wichtiger Schritt, weil viele Mitarbeiter "
        "schon jede Woche Überstunden machen und deshalb nicht noch mehr Arbeit leisten können.\n\n"
        "Was die Vor- und Nachteile betrifft, so bietet eine solche Mehrarbeit zwar kurzfristig "
        "die Möglichkeit, Engpässe zu überbrücken, führt jedoch langfristig zu Überlastung und "
        "Unzufriedenheit im Team. Ein weiterer Aspekt, der unbedingt bedacht werden sollte, "
        "betrifft unsere Gesundheit und Work-Life-Balance.\n\n"
        "Aus meiner persönlichen Erfahrung kann ich berichten, dass zusätzliche Aufgaben ohne "
        "Neueinstellungen selten zu guten Ergebnissen führen. Um eine für alle Beteiligten faire "
        "Lösung zu finden, schlage ich vor, dass wir die Aufgaben gleichmäßig verteilen oder "
        "externe Unterstützung anfordern.\n\n"
        "Ich bin gespannt auf die Meinungen und Argumente der anderen Kolleginnen und Kollegen.\n\n"
        "Liebe Grüße\nSergio"
    ),
}

# ---------------------------------------------------------------------------
# Corrección correcta: spans mínimos, un solo cambio cada uno, contenido intacto
# ---------------------------------------------------------------------------
GOOD_EVAL = {
    "verdict": "BESTANDEN",
    "score_total": 74,
    "word_count": 176,
    "criteria": _criteria(),
    "critical_errors": [
        {
            "original": "viele Mitarbeite schon",
            "correction": "viele Mitarbeiter schon",
            "change": "Buchstabe r ergänzt: Mitarbeite → Mitarbeiter",
            "rule_es": "«Mitarbeiter» se escribe con -r final; el plural no cambia la forma del nominativo.",
            "type": "Rechtschreibung",
        },
        {
            "original": "machen, und diese",
            "correction": "machen und diese",
            "change": "Komma entfällt vor »und«",
            "rule_es": "Entre dos oraciones subordinadas coordinadas con «und» no se pone coma por defecto: "
                       "la coma antes de «und» sobra.",
            "type": "Zeichensetzung",
        },
        {
            "original": "World-Life-Balance",
            "correction": "Work-Life-Balance",
            "change": "Buchstabe d → k: World → Work",
            "rule_es": "El compuesto fijo es «Work-Life-Balance» (Work = trabajo); «World» significa mundo.",
            "type": "Wortschatz",
        },
        {
            "original": "Zusätzliche",
            "correction": "zusätzliche",
            "change": "nur Groß-/Kleinschreibung: Z → z",
            "rule_es": "Dentro de la oración, el adjetivo «zusätzliche» va en minúscula: solo se escribe "
                       "en mayúscula al inicio de frase o si es sustantivo.",
            "type": "Rechtschreibung",
        },
        {
            "original": "beteiligten",
            "correction": "Beteiligten",
            "change": "nur Groß-/Kleinschreibung: b → B",
            "rule_es": "«Beteiligten» es un adjetivo sustantivado («die Beteiligten»): se escribe con "
                       "mayúscula. La terminación -en ya era correcta tras «alle».",
            "type": "Rechtschreibung",
        },
    ],
    "strengths": ["Estructura clara en párrafos.", "Registro adecuado al foro interno."],
    "areas_for_improvement": [
        "Puntuar las subordinadas y revisar mayúsculas de adjetivos sustantivados.",
        "La frase «Eine Gruppe, die …» es un fragmento: le falta el verbo principal.",
    ],
    "corrected_version": (
        "Liebe Kolleginnen und Kollegen,\n\n"
        "ich möchte mich an der aktuellen Diskussion zum Thema zusätzliche Aufgaben ohne "
        "Neueinstellungen beteiligen.\n\n"
        "Meiner Ansicht nach ist diese Maßnahme ein wichtiger Schritt, weil viele Mitarbeiter "
        "schon jede Woche Überstunden machen und diese nicht noch mehr Arbeit pro Woche "
        "leisten können.\n\n"
        "Was die Vor- und Nachteile betrifft, so bietet eine solche Mehrarbeit zwar kurzfristig "
        "die Möglichkeit, Engpässe zu überbrücken, führt jedoch langfristig zu Überlastung und "
        "Unzufriedenheit im Team.\n\n"
        "Ein weiterer Aspekt, der unbedingt bedacht werden sollte, betrifft unsere Gesundheit "
        "und Work-Life-Balance.\n\n"
        "Aus meiner persönlichen Erfahrung kann ich berichten, dass zusätzliche Aufgaben keine "
        "gute Idee sind.\n\n"
        "Um eine für alle Beteiligten faire Lösung zu finden, schlage ich vor, dass wir zwei "
        "Gruppen bilden. Eine Gruppe, die nicht mehr arbeiten kann, und eine zweite Gruppe, "
        "die diese zusätzlichen Aufgaben übernimmt.\n\n"
        "Ich bin gespannt auf die Meinungen und Argumente der anderen Kolleginnen und Kollegen.\n\n"
        "Liebe Grüße,\nSergio"
    ),
}


def check(cond, msg, fails):
    if not cond:
        fails.append(msg)
    return cond


def main() -> int:
    fails = []

    print("=== TEST DE REGRESIÓN DEL CORRECTOR (caso real) ===")

    # 1) El validador debe cazar los defectos de la salida vieja.
    print("[1/5] La salida defectuosa (prompt viejo) no debe pasar el validador...")
    bad_errors = validate_evaluation_json(BAD_EVAL, STUDENT_TEXT)
    faltan_change = [e for e in bad_errors if "no trae 'change'" in e]
    check(len(faltan_change) == 5, f"esperaba 5 avisos de 'change' ausente, hay {len(faltan_change)}", fails)
    check(any("ofrece alternativas" in e for e in bad_errors),
          "no detectó las alternativas «A / B» en la corrección #5", fails)
    check(any("span máximo" in e for e in bad_errors),
          "no detectó que la cita #4 es un párrafo en vez de una palabra", fails)
    print(f"      OK: {len(bad_errors)} defectos detectados (5 sin 'change', alternativas, span).")
    for e in bad_errors[:8]:
        print(f"        - {e}")

    # 2) Caso honesto: #2 y #5 no se pueden tumbar mecánicamente, pero el prompt
    #    los prohíbe con reglas explícitas. Eso lo comprueba el lint del prompt.
    print("[2/5] La corrección correcta pasa sin ruido...")
    good_errors = validate_evaluation_json(GOOD_EVAL, STUDENT_TEXT)
    check(len(good_errors) == 0, f"la corrección correcta generó {len(good_errors)} avisos: {good_errors}", fails)
    print("      OK: 0 avisos.")

    # 3) La fuga del texto "pulido": reescribir en vez de corregir.
    print("[3/5] Una versión reescrita (no corregida) debe ser rechazada...")
    rewritten = dict(GOOD_EVAL)
    rewritten["corrected_version"] = BAD_EVAL["corrected_version"]
    rewritten_errors = validate_evaluation_json(rewritten, STUDENT_TEXT)
    check(any("no aparece en 'corrected_version'" in e for e in rewritten_errors),
          "no detectó que las correcciones no se aplicaron al texto final", fails)
    print(f"      OK: {len(rewritten_errors)} avisos (corrección no aplicada).")

    # 4) Cita no literal: la firma típica del corrector que cita lo que quería escribir.
    print("[4/5] Una cita no literal debe ser rechazada...")
    edited = dict(GOOD_EVAL)
    edited["critical_errors"] = [
        dict(GOOD_EVAL["critical_errors"][0], original="viele Mitarbeiter schon"),
    ] + GOOD_EVAL["critical_errors"][1:]
    edited_errors = validate_evaluation_json(edited, STUDENT_TEXT)
    check(any("NO aparece tal cual" in e for e in edited_errors),
          "aceptó una cita que no está literalmente en el texto", fails)
    print(f"      OK: {len(edited_errors)} avisos (cita no literal).")

    # 5) Lint del prompt: los guardarraíles que evitan repetir los fallos.
    print("[5/5] Los guardarraíles del prompt siguen en su sitio...")
    anclas = [
        "GRUNDHALTUNG",
        "Beweispflicht",
        "PRÜFLISTE",
        "MINIMALPRINZIP".capitalize(),          # "Minimalprinzip"
        "für alle Beteiligten",                  # el caso #5
        "zum Thema zusätzlicher Aufgaben",       # el genitivo que se le escapó
        "Relativpronomen",                       # el caso #2
        "Liebe Grüße",                           # la coma que borró
        "Work-Life-Balance",                     # el typo #3
        "KORREKTURFASSUNG, KEINE NEUFASSUNG",
        "keine Alternativen",
    ]
    for a in anclas:
        check(a in SYSTEM_PROMPT, f"falta el guardarraíl «{a}» en SYSTEM_PROMPT", fails)

    items_schema = JSON_SCHEMA["properties"]["critical_errors"]["items"]
    check("change" in items_schema["properties"], "el esquema no declara el campo `change`", fails)
    items_required = items_schema["required"]
    check("change" in items_required, "`change` no está en los campos requeridos de critical_errors", fails)
    print("      OK: guardarraíles y esquema verificados.")

    if fails:
        print(f"\nFALLOS ({len(fails)}):")
        for f in fails:
            print(f"  - {f}")
        return 1

    print("\nTodo OK: el corrector queda blindado contra estos cinco fallos.")
    return 0


# ---------------------------------------------------------------------------
# Modo en vivo: evalúa el texto real con Gemini y audita la respuesta
# ---------------------------------------------------------------------------

LIVE_TASK = {
    "category": "forum",
    "label": "Forumsbeitrag: zusätzliche Aufgaben ohne Neueinstellungen",
    "topic": "Arbeitsbelastung / Aufgabenverteilung im Team",
    "scenario": "Im Firmen-Intranet diskutiert das Team, ob zusätzliche Aufgaben ohne neue "
                "Stellen übernommen werden sollen.",
    "prompt": "Schreiben Sie einen Beitrag für das Firmen-Intranet und nehmen Sie zur "
              "Diskussion Stellung.",
    "leitpunkte": [
        "Bezug auf die laufende Diskussion",
        "Eigene Position mit Begründung (Vor- und Nachteile)",
        "Aspekt Gesundheit und Work-Life-Balance",
        "Konkreter Vorschlag zur Lösung",
    ],
    "min_words": 150,
}


def _call_gemini(api_key: str, model: str, user_prompt: str) -> dict:
    import urllib.error
    import urllib.parse
    import urllib.request

    url = ("https://generativelanguage.googleapis.com/v1beta/models/"
           + urllib.parse.quote(model, safe="")
           + ":generateContent?key=" + urllib.parse.quote(api_key, safe=""))
    cfg = {"temperature": 0, "response_mime_type": "application/json"}

    def post(generation_config: dict) -> dict:
        payload = {
            "system_instruction": {"parts": [{"text": SYSTEM_PROMPT}]},
            "contents": [{"parts": [{"text": user_prompt}]}],
            "generationConfig": generation_config,
        }
        req = urllib.request.Request(
            url, data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=180) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            # El cuerpo del error dice si el problema es el esquema o la petición.
            detail = exc.read().decode("utf-8", "replace")
            return {"__http_error": exc.code, "__detail": detail}
        except urllib.error.URLError as exc:
            return {"__http_error": 0, "__detail": str(exc.reason)}

    data = post({**cfg, "response_schema": JSON_SCHEMA})
    if data.get("__http_error") in (400, 422) and "schema" in str(data.get("__detail", "")).lower():
        print("      (el esquema fue rechazado; reintento sin response_schema)")
        data = post(cfg)
    if "__http_error" in data:
        code, detail = data["__http_error"], str(data.get("__detail", ""))
        pista = ("revisa que la clave sea válida y tenga la Generative Language API activa"
                 if code in (400, 403) else "revisa la conexión y el nombre del modelo")
        raise SystemExit(f"ERROR HTTP {code}: {detail[:300]}\n  → {pista}")

    cands = data.get("candidates") or []
    if not cands:
        raise SystemExit("respuesta sin candidatos: " + json.dumps(data)[:400])
    parts = cands[0].get("content", {}).get("parts", [])
    raw = "".join(p.get("text", "") for p in parts)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        raise SystemExit("el modelo no devolvió JSON válido:\n" + raw[:600])


def audit_live(data: dict) -> tuple:
    """Separa fallos duros (la respuesta es incorrecta) de avisos de recall."""
    hard = list(validate_evaluation_json(data, STUDENT_TEXT))
    soft = []
    entries = [e for e in (data.get("critical_errors") or []) if isinstance(e, dict)]

    print("\n--- Tarjetas devueltas por el modelo ---")
    if not entries:
        soft.append("no marcó ningún error (¿texto perfecto?)")
    for i, e in enumerate(entries, 1):
        print(f"  #{i} [{e.get('type')}] „{e.get('original')}“ → „{e.get('correction')}“ "
              f"| {e.get('change') or '(sin change)'}")

    for i, e in enumerate(entries, 1):
        original = (e.get("original") or "")
        correction = (e.get("correction") or "")
        low_orig = original.casefold()
        low_corr = correction.casefold()

        # El fallo #2 del caso real: meter un relativo donde va el nominativo.
        if low_corr.startswith("die ") and not low_orig.startswith("die"):
            hard.append(f"#{i}: la corrección introduce «die» como relativo "
                        f"(agramatical): «{correction}»")

        # El fallo #5: «Beteiligten» solo necesitaba mayúscula.
        if "beteiligten" in low_orig and "Beteiligten" not in correction:
            hard.append(f"#{i}: cita «{original}» pero la corrección no escribe "
                        f"«Beteiligten» con mayúscula: «{correction}»")

        # «Zusätzliche» a mitad de oración va en minúscula.
        if original.startswith("Zusätzliche") and not correction.startswith("zusätzliche"):
            hard.append(f"#{i}: «Zusätzliche» debe quedar en minúscula: «{correction}»")

    cv = data.get("corrected_version") or ""
    if "Liebe Grüße," in STUDENT_TEXT and "Liebe Grüße," not in cv:
        hard.append("la despedida perdió la coma de «Liebe Grüße,»")
    for frag in ("zwei Gruppen bilden", "Eine Gruppe, die nicht mehr arbeiten kann"):
        if frag not in cv:
            hard.append(f"el texto corregido ya no contiene «{frag}» (se reescribió)")

    ratio = len(cv) / max(len(STUDENT_TEXT), 1)
    if not 0.75 <= ratio <= 1.35:
        soft.append(f"el texto corregido mide {ratio:.2f}× el original: huele a reescritura")

    if not any("zum Thema" in (e.get("original") or "") for e in entries):
        soft.append("no marcó el genitivo tras «zum Thema» (fallo de recall del caso real)")

    campos = ("original", "correction", "change", "rule_es")
    for i, e in enumerate(entries, 1):
        for c in campos:
            if not (e.get(c) or "").strip():
                hard.append(f"#{i}: falta el campo «{c}»")
    return hard, soft


def live_main(api_key: str, model: str, save: str = "") -> int:
    print(f"=== CORRECTOR EN VIVO ({model}) ===")
    print(f"texto: {count_words(STUDENT_TEXT)} palabras · {len(STUDENT_TEXT)} caracteres")
    user_prompt = build_user_prompt(LIVE_TASK, STUDENT_TEXT, lang="es")
    data = _call_gemini(api_key, model, user_prompt)
    if save:
        with open(save, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
        print(f"respuesta guardada en {save}")

    hard, soft = audit_live(data)
    print(f"\nveredicto del modelo: {data.get('verdict')} ({data.get('score_total')}/100)")

    if soft:
        print(f"\nAVISOS ({len(soft)}):")
        for s in soft:
            print(f"  - {s}")
    if hard:
        print(f"\nFALLOS ({len(hard)}):")
        for h in hard:
            print(f"  - {h}")
        print("\nEl corrector TODAVÍA falla: no lo des por bueno.")
        return 1

    print("\nOK: la respuesta pasa el contrato y las trampas del caso real.")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--gemini-key" in args:
        import argparse
        ap = argparse.ArgumentParser(description="Corrector telc B2: suite offline o prueba en vivo")
        ap.add_argument("--gemini-key", required=True)
        ap.add_argument("--model", default="gemini-3.5-flash-lite")
        ap.add_argument("--save", default="")
        ns = ap.parse_args(args)
        sys.exit(live_main(ns.gemini_key, ns.model, ns.save))
    sys.exit(main())