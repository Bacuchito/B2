# -*- coding: utf-8 -*-
"""
prompt_schreiben.py - Definición oficial del System Prompt y Contrato JSON
para la evaluación telc Deutsch-Test für den Beruf B2 (Schreiben).
"""

import json
from typing import Dict, Any, List

SYSTEM_PROMPT = """Du bist ein offizieller, strenger und erfahrener telc-Prüfer für den »Deutsch-Test für den Beruf B2« (Schreiben).
Deine Aufgabe ist es, einen vom Prüfungsteilnehmer verfassten Text (Beschwerde-E-Mail oder Forumsbeitrag im Firmen-Intranet) anhand der offiziellen telc B2-Kriterien objektiv, pädagogisch und präzise zu bewerten.

### BEWERTUNGSKRITERIEN (telc Deutsch B2 Beruf):
1. I. AUFGABENBEWÄLTIGUNG (0-25 Punkte):
   - Wurden alle 4 vorgegebenen Leitpunkte inhaltlich angemessen und ausreichend detailliert behandelt?
   - Wortanzahl: Das geforderte Minimum liegt bei 150 Wörtern.
     * < 100 Wörter: Strikter Punktabzug (maximal Stufe C oder D).
     * 100 - 149 Wörter: Punktabzug bei der Vollständigkeit.
     * >= 150 Wörter: Volle Punktzahl möglich, sofern alle Leitpunkte behandelt wurden.
   - Wurden eventuelle interne Vorgaben (z. B. Anweisungen der Geschäftsleitung) beachtet?

2. II. KOMMUNIKATIVE ANGEMESSENHEIT & REGISTER (0-25 Punkte):
   - Textsortenkonventionen:
     * Bei Beschwerde-E-Mail: Formelle Anrede (z. B. »Sehr geehrte Damen und Herren« / »Sehr geehrte(r) Frau/Herr...«), professioneller Betreffbezug, höflicher/deeskalierender Ton, formelle Grußformel (»Mit freundlichen Grüßen«), Name/Abteilung.
     * Bei Forumsbeitrag: Angemessene kollegiale Anrede (z. B. »Liebe Kolleginnen und Kollegen,« / »Hallo zusammen,«), strukturierte Darlegung der eigenen Meinung mit Argumenten/Beispielen, kollegialer Schluss und Abschiedsgruß.
   - Soziolinguistische Angemessenheit: Angemessener B2-Berufsregister (weder zu umgangssprachlich noch gestelzt).

3. III. FORMALE RICHTIGKEIT / KORREKTHEIT (0-25 Punkte):
   - Satzbau / Syntax: Korrekte Verbstellung (Verbzweitstellung im Hauptsatz, Verbletztstellung bei subordinierenden Konjunktionen wie dass, weil, obwohl, wenn, da; Inversion nach Angaben).
   - Morphologie & Kasus: Akkusativ, Dativ, Genitiv; Wechselpräpositionen; Adjektivdeklinationen; Passivformen; Konjunktiv II (Höflichkeit).
   - Orthografie & Interpunktion: Substantiv-Großschreibung, Kommasetzung vor Nebensätzen und Infinitivgruppen.

4. IV. SPRACHLICHE MITTEL & REPERTOIRE (0-25 Punkte):
   - Wortschatz: Angemessener B2-Fach- und Berufswortschatz, Nomen-Verb-Verbindungen (z. B. »zur Verfügung stehen«, »eine Entscheidung treffen«, »in Kenntnis setzen«).
   - Kohäsion & Konnektoren: Abwechslungsreiche Konnektoren (z. B. »darüber hinaus«, »folglich«, »einerseits ... andererseits«, »aus diesem Grund«, »zwar ... aber«) statt bloßer Aneinanderreihung mit »und« oder »aber«.

### NOTENSTUFEN JE KRITERIUM:
- A (23-25 Punkte): voll erfüllt (überzeugendes B2-Niveau, fast muttersprachliche Souveränität)
- B (18-22 Punkte): gut erfüllt (solides B2-Niveau, kleinere Ungenauigkeiten beeinträchtigen die Verständlichkeit nicht)
- C (12-17 Punkte): teilweise erfüllt (eher B1-Niveau, häufige Fehler oder oberflächliche Behandlung)
- D (0-11 Punkte): ungenügend (A2-Niveau oder Thema verfehlt)

### BESTEHENSGRENZE (VERDICT):
- Gesamtpunktzahl: Summe der 4 Kriterien (0-100 Punkte).
- BESTANDEN: Mindestens 60 Punkte GESAMT und kein Kriterium mit Stufe D (<= 11 Punkte).
- NICHT BESTANDEN: Unter 60 Punkte ODER ein beliebiges Kriterium mit Stufe D.

### AUSGABEFORMAT:
Du MUSST deine Antwort AUSSCHLIESSLICH als valides JSON-Objekt formatieren (ohne Markdown-Backticks ```json, ohne einleitenden Text, ohne Grußformel).
Verwende EXAKT folgende Schlüssel (Keys) und Struktur:
{
  "verdict": "BESTANDEN" oder "NICHT BESTANDEN",
  "score_total": 85,
  "word_count": 168,
  "criteria": {
    "aufgabenbewaeltigung": {
      "grade": "A",
      "score": 23,
      "leitpunkte_check": [
        {"point": "Leitpunkt 1", "covered": true, "comment": "Ausführlich und überzeugend behandelt."},
        {"point": "Leitpunkt 2", "covered": true, "comment": "Angemessen ausgeführt."},
        {"point": "Leitpunkt 3", "covered": true, "comment": "Eigene Erfahrung plausibel geschildert."},
        {"point": "Leitpunkt 4", "covered": true, "comment": "Konkreter Vorschlag unterbreitet."}
      ],
      "feedback": "Explicación detallada en español sobre el cumplimiento de la tarea y puntos guía."
    },
    "angemessenheit": {
      "grade": "B",
      "score": 21,
      "feedback": "Explicación detallada en español sobre registro formal, saludo, despedida y tono."
    },
    "korrektheit": {
      "grade": "B",
      "score": 20,
      "feedback": "Explicación detallada en español sobre sintaxis, posición del verbo, casos y ortografía."
    },
    "repertoire": {
      "grade": "B",
      "score": 21,
      "feedback": "Explicación detallada en español sobre vocabulario profesional B2 y conectores."
    }
  },
  "critical_errors": [
    {
      "original": "Frase errónea del alumno",
      "correction": "Versión corregida en alemán B2",
      "rule_es": "Regla gramatical clara explicada en español",
      "type": "Grammatik"
    }
  ],
  "strengths": [
    "Punto fuerte 1 en español",
    "Punto fuerte 2 en español"
  ],
  "areas_for_improvement": [
    "Área de mejora 1 en español",
    "Área de mejora 2 en español"
  ],
  "corrected_version": "Sehr geehrte(r) Frau/Herr [Name],\n\nvielen Dank für Ihre Nachricht bezüglich...\n\n[Texto completo corregido y pulido del alumno, estructurado en párrafos claros con saltos de línea (\n\n)]\n\nMit freundlichen Grüßen\n[Vorname Nachname]\n[Abteilung]",
  "musterloesung": "Sehr geehrte(r) Frau/Herr [Name],\n\n[Musterlösung alternativa de 100 puntos según estándares telc B2 con conectores variados y párrafos claros]\n\nMit freundlichen Grüßen\n[Vorname Nachname]"
}

WICHTIGE VORGABEN:
- `score_total` MUSS eine Ganzzahl (0-100) sein und der Summe der 4 Kriterien (`score`) entsprechen.
- Jedes Kriterium in `criteria` MUSS die Felder `grade` (A, B, C oder D), `score` (Zahl von 0 bis 25) und `feedback` enthalten.
- In `critical_errors`: Analysiere den Text gründlich und liste ALLE konkreten Fehler auf (Grammatik, Verbposition/Satzbau, Deklination/Kasus, Präpositionen, unpassende Wortwahl, Rechtschreibung, Zeichensetzung).
  * `original`: MUSS ein EXAKTES, wörtliches Zitat (Substring) aus dem Text des Teilnehmers sein (ohne Anführungszeichen drumherum), damit der Fehler exakt an dieser Stelle im Text farbig markiert werden kann!
    - Zitiere `original` ZEICHEN FÜR ZEICHEN so, wie der Teilnehmer es geschrieben hat — auch MIT seinen Fehlern. Schreibe NIEMALS die bereits korrigierte Form ins Feld `original` (bei einem Großschreibungsfehler steht dort also z. B. `zuständigen abteilung`, NICHT `zuständigen Abteilung`).
    - Prüfe vor der Ausgabe, ob dieser Wortlaut wirklich genau so im Text vorkommt. Wenn nicht, zitiere den tatsächlichen Wortlaut.
  * `correction`: Die korrigierte Version der Passage auf Deutsch (B2-Niveau).
    - `correction` MUSS sich von `original` unterscheiden. Wenn du keine echte Änderung nennen kannst, ist es KEIN Fehler: dann lass den Eintrag ganz weg. Ein Eintrag, in dem `original` und `correction` gleich lauten, ist ungültig.
  * `rule_es`: Präzise, verständliche und lehrreiche Erklärung der Grammatik- oder Ausdrucksregel auf SPANISCH (oder auf RUSSISCH, falls im User-Prompt angewiesen).
    - Die Erklärung MUSS zu dem zitierten Fehler passen: wenn du Groß- und Kleinschreibung bemängelst, muss im Zitat auch wirklich ein Wort falsch groß- oder kleingeschrieben sein.
  * `type`: "Grammatik", "Wortschatz", "Rechtschreibung" (Groß-/Kleinschreibung, falsch geschriebene Wörter), "Zeichensetzung" (nur Kommas, Punkte und andere Satzzeichen), "Stil" oder "Satzbau".
- QUALITÄT UND FORMATIERUNG VON `corrected_version` UND `musterloesung`:
  * KEIN unleserlicher Textblock! Du MUSST den Text mit echten Leerzeilen (`\n\n`) optisch in 3 bis 4 übersichtliche Absätze gliedern (Anrede, Einleitung/Dank, Behandlung der Leitpunkte, Lösung/Schluss, Grußformel, Name).
  * Anrede (z. B. `Sehr geehrte(r) Frau/Herr [Name],` oder `Liebe Kolleginnen und Kollegen,`) steht zwingend auf einer EIGENEN Zeile, gefolgt von einer Leerzeile (`\n\n`).
  * Grußformel (z. B. `Mit freundlichen Grüßen` oder `Herzliche Grüße`) steht auf einer EIGENEN Zeile nach einer Leerzeile (`\n\n`).
  * WICHTIGE FORMALIE: Im Deutschen steht nach `Mit freundlichen Grüßen` NIEMALS ein Komma! Danach folgt ein Zeilenumbruch mit Vor- und Nachname.
  * Sprachliches Niveau: Nutze anspruchsvolles, flüssiges und natürliches Berufsdeutsch B2 (abwechslungsreiche Konnektoren wie `darüber hinaus`, `des Weiteren`, `infolgedessen`, `demnach`; Nomen-Verb-Verbindungen wie `eine Vereinbarung treffen`, `zur Verfügung stehen`, `Kenntnis nehmen`).
- Erklärungen der Fehler (`rule_es`), Stärken (`strengths`), Schwächen (`areas_for_improvement`) und `feedback` MÜSSEN auf SPANISCH sein (oder auf RUSSISCH, falls im User-Prompt ausdrücklich vorgegeben).
- `corrected_version` und `musterloesung` MÜSSEN auf DEUTSCH sein.
"""

JSON_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "required": [
        "verdict",
        "score_total",
        "word_count",
        "criteria",
        "critical_errors",
        "strengths",
        "areas_for_improvement",
        "corrected_version"
    ],
    "properties": {
        "verdict": {
            "type": "string",
            "enum": ["BESTANDEN", "NICHT BESTANDEN"]
        },
        "score_total": {
            "type": "integer",
            "minimum": 0,
            "maximum": 100
        },
        "word_count": {
            "type": "integer"
        },
        "musterloesung": {
            "type": "string"
        },
        "criteria": {
            "type": "object",
            "required": ["aufgabenbewaeltigung", "angemessenheit", "korrektheit", "repertoire"],
            "properties": {
                "aufgabenbewaeltigung": {
                    "type": "object",
                    "required": ["grade", "score", "leitpunkte_check", "feedback"],
                    "properties": {
                        "grade": {"type": "string", "enum": ["A", "B", "C", "D"]},
                        "score": {"type": "integer", "minimum": 0, "maximum": 25},
                        "leitpunkte_check": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "required": ["point", "covered", "comment"],
                                "properties": {
                                    "point": {"type": "string"},
                                    "covered": {"type": "boolean"},
                                    "comment": {"type": "string"}
                                }
                            }
                        },
                        "feedback": {"type": "string"}
                    }
                },
                "angemessenheit": {
                    "type": "object",
                    "required": ["grade", "score", "feedback"],
                    "properties": {
                        "grade": {"type": "string", "enum": ["A", "B", "C", "D"]},
                        "score": {"type": "integer", "minimum": 0, "maximum": 25},
                        "feedback": {"type": "string"}
                    }
                },
                "korrektheit": {
                    "type": "object",
                    "required": ["grade", "score", "feedback"],
                    "properties": {
                        "grade": {"type": "string", "enum": ["A", "B", "C", "D"]},
                        "score": {"type": "integer", "minimum": 0, "maximum": 25},
                        "feedback": {"type": "string"}
                    }
                },
                "repertoire": {
                    "type": "object",
                    "required": ["grade", "score", "feedback"],
                    "properties": {
                        "grade": {"type": "string", "enum": ["A", "B", "C", "D"]},
                        "score": {"type": "integer", "minimum": 0, "maximum": 25},
                        "feedback": {"type": "string"}
                    }
                }
            }
        },
        "critical_errors": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["original", "correction", "rule_es", "type"],
                "properties": {
                    "original": {"type": "string"},
                    "correction": {"type": "string"},
                    "rule_es": {"type": "string"},
                    "type": {
                        "type": "string",
                        "enum": ["Grammatik", "Wortschatz", "Rechtschreibung", "Zeichensetzung", "Stil", "Satzbau"]
                    }
                }
            }
        },
        "strengths": {
            "type": "array",
            "items": {"type": "string"}
        },
        "areas_for_improvement": {
            "type": "array",
            "items": {"type": "string"}
        },
        "corrected_version": {
            "type": "string"
        }
    }
}


def build_user_prompt(task: Dict[str, Any], student_text: str, lang: str = "es") -> str:
    """
    Construye el prompt de entrada para el modelo combinando la tarea oficial y el texto del alumno.
    Permite especificar el idioma ('es' o 'ru') en el que el examinador debe dar explicaciones y feedback.
    """
    leitpunkte_str = "\n".join([f"   {i+1}. {lp}" for i, lp in enumerate(task.get("leitpunkte", []))])

    prompt_parts = [
        "### AUFGABENSTELLUNG (TELC DEUTSCH B2 BERUF):",
        f"Kategorie: {task.get('category', 'Allgemein')}",
        f"Titel: {task.get('label', task.get('title', ''))}",
    ]
    if task.get("topic"):
        prompt_parts.append(f"Thema: {task['topic']}")
    prompt_parts.append(f"Situation: {task.get('scenario', '')}")

    if task.get("source_letter"):
        prompt_parts.append(f"\nEingehende Kundenbeschwerde / E-Mail:\n\"\"\"\n{task['source_letter']}\n\"\"\"")

    if task.get("colleague_post"):
        prompt_parts.append(f"\nBeitrag des Kollegen im Firmen-Intranet:\n\"\"\"\n{task['colleague_post']}\n\"\"\"")

    if task.get("boss_instructions"):
        prompt_parts.append(f"\nInterne Anweisung der Geschäftsleitung:\n\"\"\"\n{task['boss_instructions']}\n\"\"\"")

    prompt_parts.extend([
        f"\nArbeitsauftrag: {task.get('prompt', '')}",
        f"Zu behandelnde 4 Leitpunkte:\n{leitpunkte_str}",
        f"Geforderte Mindestlänge: {task.get('min_words', 150)} Wörter.",
        "\n=======================================================",
        "### TEXT DES PRÜFUNGSTEILNEHMERS (ZUR BEWERTUNG):",
        f"\"\"\"\n{student_text}\n\"\"\"",
        "======================================================="
    ])

    if lang == "ru":
        prompt_parts.extend([
            "\nWICHTIGE VORGABE ZUR SPRACHE DES FEEDBACKS:",
            "Die Prüfungskandidatin lernt Deutsch und ihre Muttersprache ist RUSSISCH.",
            "- Alle Erklärungen der Fehler im Feld `rule_es` MÜSSEN AUF RUSSISCH verfasst werden!",
            "- Die Stärken (`strengths`), Schwächen (`areas_for_improvement`) und das Feedback zu den 4 Kriterien (`feedback`) MÜSSEN AUF RUSSISCH sein!",
            "- Die korrigierte Fassung (`corrected_version`) und die Musterlösung (`musterloesung`) MÜSSEN selbstverständlich auf DEUTSCH (B2-Niveau) sein.",
            "- Verwende präzise russische linguistische Fachbegriffe für Deutschlerner (z. B. 'Порядок слов в предложении', 'Управление глаголов и предлоги', 'Спряжение', 'Падежи и артикли')."
        ])
    else:
        prompt_parts.extend([
            "\nWICHTIGE VORGABE ZUR SPRACHE DES FEEDBACKS:",
            "- Alle Erklärungen der Fehler im Feld `rule_es`, Stärken (`strengths`), Schwächen (`areas_for_improvement`) und das Kriterien-Feedback MÜSSEN auf SPANISCH verfasst werden!",
            "- Die korrigierte Fassung (`corrected_version`) und die Musterlösung (`musterloesung`) MÜSSEN auf DEUTSCH (B2-Niveau) sein."
        ])

    prompt_parts.append("\nAnalysiere nun den Text und gib das strukturierte JSON-Ergebnis gemäß der Schema-Definition zurück.")

    return "\n".join(prompt_parts)


def validate_evaluation_json(data: Dict[str, Any]) -> List[str]:
    """
    Valida que un diccionario cumpla el contrato de evaluación telc B2.
    Devuelve una lista de errores encontrados (vacía si es 100% válido).
    """
    errors = []

    required_top = ["verdict", "score_total", "word_count", "criteria", "critical_errors", "strengths", "areas_for_improvement", "corrected_version"]
    for field in required_top:
        if field not in data:
            errors.append(f"Falta el campo principal requerido '{field}'.")

    if data.get("verdict") not in ["BESTANDEN", "NICHT BESTANDEN"]:
        errors.append(f"El campo 'verdict' debe ser 'BESTANDEN' o 'NICHT BESTANDEN', recibido: {data.get('verdict')}")

    score = data.get("score_total")
    if not isinstance(score, (int, float)) or not (0 <= score <= 100):
        errors.append(f"'score_total' debe ser un número entre 0 y 100, recibido: {score}")

    criteria = data.get("criteria", {})
    required_crit = ["aufgabenbewaeltigung", "angemessenheit", "korrektheit", "repertoire"]
    for c in required_crit:
        if c not in criteria:
            errors.append(f"Falta el criterio requerido en criteria: '{c}'.")
        else:
            c_data = criteria[c]
            if c_data.get("grade") not in ["A", "B", "C", "D"]:
                errors.append(f"Criterio '{c}' tiene un grado inválido: {c_data.get('grade')}")
            if not isinstance(c_data.get("score"), (int, float)) or not (0 <= c_data.get("score") <= 25):
                errors.append(f"Criterio '{c}' tiene puntuación fuera de rango 0-25: {c_data.get('score')}")

    if not isinstance(data.get("critical_errors"), list):
        errors.append("'critical_errors' debe ser una lista.")
    else:
        for idx, err in enumerate(data.get("critical_errors", [])):
            for f in ["original", "correction", "type"]:
                if f not in err:
                    errors.append(f"Error #{idx} en 'critical_errors' carece del campo '{f}'.")
            if "rule_es" not in err and "rule_ru" not in err and "rule" not in err:
                errors.append(f"Error #{idx} en 'critical_errors' carece de regla de explicación ('rule_es' o 'rule_ru').")

    if not isinstance(data.get("strengths"), list):
        errors.append("'strengths' debe ser una lista.")
    if not isinstance(data.get("areas_for_improvement"), list):
        errors.append("'areas_for_improvement' debe ser una lista.")
    if not isinstance(data.get("corrected_version"), str) or len(data.get("corrected_version", "").strip()) == 0:
        errors.append("'corrected_version' debe ser una cadena no vacía.")

    return errors
