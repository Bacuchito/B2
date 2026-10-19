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

import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from prompt_schreiben import SYSTEM_PROMPT, JSON_SCHEMA, validate_evaluation_json

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


if __name__ == "__main__":
    sys.exit(main())
