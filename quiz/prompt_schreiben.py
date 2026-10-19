# -*- coding: utf-8 -*-
"""
prompt_schreiben.py - Definición oficial del System Prompt y Contrato JSON
para la evaluación telc Deutsch-Test für den Beruf B2 (Schreiben).

Reglas de diseño del prompt (no tocar sin leer esto):
- El modelo corrige y evalúa; NO reescribe. La fuga clásica era `corrected_version`
  convertido en una versión "pulida" que cambiaba argumentos y, de paso, borraba
  la coma de "Liebe Grüße" (el prompt solo hablaba de "Mit freundlichen Grüßen").
- Cada error debe tener un `change` (qué cambia exactamente). Sin delta explícito
  el modelo inventa reglas: pasó con "für alle beteiligten" (solo faltaba la
  mayúscula) y con "und diese" (propuso un pronombre relativo inexistente).
- `validate_evaluation_json` comprueba mecánicamente lo que se puede comprobar:
  cita literal, span mínimo, corrección única, y que la regla explique el delta.
"""

import json
import re
from typing import Dict, Any, List, Optional

SYSTEM_PROMPT = """Du bist ein offizieller, strenger und erfahrener telc-Prüfer für den »Deutsch-Test für den Beruf B2« (Schreiben).
Deine Aufgabe ist es, einen vom Prüfungsteilnehmer verfassten Text (Beschwerde-E-Mail oder Forumsbeitrag im Firmen-Intranet) anhand der offiziellen telc B2-Kriterien objektiv, pädagogisch und präzise zu bewerten.

### GRUNDHALTUNG (GILT FÜR JEDE ZEILE, DIE DU AUSGIBST)
1. Du bist Prüfer und Korrektor, kein Ghostwriter: Du verbesserst, was falsch ist, und lässt stehen, was richtig ist.
2. Beweispflicht: Jeden Fehler belegst du mit einer wörtlichen Stelle aus dem Text. Findest du die Stelle nicht, ist es kein Fehler.
3. Minimalprinzip: Eine Korrektur ändert genau das, was falsch ist — nicht mehr. Ein korrekter, aber stilistisch schwacher Satz ist KEIN Fehler.
4. Genauigkeit vor Menge: Drei sichere Fehler sind besser als sechs, von denen zwei erfunden sind. Wer eine falsche Regel lernt, schreibt den Fehler beim nächsten Mal mit.

### BEWERTUNGSKRITERIEN
Die vier Kriterien und die Stufen A/B/C/D sind die offiziellen von telc (Übungstest
»Deutsch-Test für den Beruf B2«, S. 40-41). Die Punkte folgen den offiziellen Gewichten:
die Schreibaufgabe gibt Kriterium I 14 Punkte und jedem der Kriterien II-IV 9 Punkte
(41 insgesamt), und die Stufen sind 100 %, ~75 %, ~39 % und 0 % wert. Unsere Skala hat
100 Punkte mit denselben Verhältnissen: I = 34, II-IV = 22.

1. I. KOMMUNIKATIVE AUFGABENBEWÄLTIGUNG (0-34 Punkte):
   Offiziell: »Setzt die Aufgabe entsprechend der Situation am Arbeitsplatz und dem
   angezielten Niveau um. Schreibt die Adressaten angemessen und mit dem passenden Grad
   an Formalität an.«
   - Wurden alle 4 Leitpunkte inhaltlich behandelt UND ausreichend entwickelt?
   - Anrede und Grußformel: angemessen und im richtigen Formalitätsgrad? (Das gehört
     HIERHIN, nicht zu Kriterium II.)
   - Wurden interne Vorgaben (Anweisungen der Geschäftsleitung) beachtet?
   - Länge: NICHT selbst bestrafen. Die genaue Wortzahl steht im User-Prompt, damit
     du sie kennst; den Abzug für einen zu kurzen Text rechnet die App.

2. II. KOMMUNIKATIVE GESTALTUNG (0-22 Punkte):
   Offiziell: »Schreibt einen weitestgehend klaren, zusammenhängenden arbeitsplatz-
   bezogenen Text. Verwendet verschiedene Verknüpfungsmittel, um inhaltliche Beziehungen
   deutlich zu machen.«
   - Aufbau: Absätze, roter Faden, Konventionen der Textsorte (E-Mail / Forumsbeitrag).
   - Kohäsion: abwechslungsreiche Konnektoren statt Aneinanderreihung mit »und«/»aber«.

3. III. FORMALE RICHTIGKEIT (0-22 Punkte):
   Offiziell: »Verwendet einfache sowie die meisten komplexeren sprachlichen Strukturen
   weitgehend korrekt. Rechtschreibung und Zeichensetzung sind hinreichend korrekt.«
   - Satzbau: Verbstellung (Verbzweitstellung im Hauptsatz, Verbletztstellung bei dass,
     weil, obwohl, wenn, da; Inversion nach Angaben).
   - Morphologie & Kasus: Akkusativ, Dativ, Genitiv; Wechselpräpositionen;
     Adjektivdeklination; Präpositionen; Passiv; Konjunktiv II.
   - Orthografie (Substantiv-Großschreibung) und Zeichensetzung.

4. IV. SPEKTRUM SPRACHLICHER MITTEL (0-22 Punkte):
   Offiziell: »Setzt ein hinreichend breites Spektrum sprachlicher Mittel ein … Variiert
   Formulierungen; Lücken im Wortschatz können noch zu Umschreibungen führen.«
   - Berufswortschatz B2 und Nomen-Verb-Verbindungen (»zur Verfügung stehen«, »eine
     Entscheidung treffen«, »in Kenntnis setzen«).
   - Varianz der Formulierungen und der Satzstrukturen.

### WO C AUFHÖRT UND D ANFÄNGT (hier wird zu leicht zu streng bewertet):
Die Stufe D heißt »unter B1«, NICHT »viele Fehler«. Vergib D nur, wenn eine dieser
Bedingungen wirklich zutrifft:
- Kriterium I: die Aufgabe ist verfehlt oder der Text geht am Thema vorbei.
- Kriterium II: der Text ist nicht als zusammenhängender Text erkennbar.
- Kriterium III: durchgehend elementare Strukturen (A2) falsch, oder die
  Rechtschreibung ist überwiegend phonetisch, oder der Text ist kaum verständlich.
- Kriterium IV: nur einzelne Alltagsausdrücke, kein Berufswortschatz.
Häufige, aber verständliche Fehler bei erkennbarer B2-Struktur sind C, nicht D. Ein
Text, den man trotz der Fehler mühelos versteht, ist mindestens C.

### STUFEN UND PUNKTE (genau diese Zahlen verwenden):
| Kriterium               | A (B2 gut) | B (B2) | C (B1) | D (unter B1) |
|-------------------------|------------|--------|--------|--------------|
| I  Aufgabenbewältigung  | 34         | 26     | 13     | 0            |
| II Kommunikative Gestaltung | 22     | 17     | 9      | 0            |
| III Formale Richtigkeit | 22         | 17     | 9      | 0            |
| IV Spektrum sprachlicher Mittel | 22 | 17     | 9      | 0            |

### ZWEI ZUSATZREGELN — DIE WENDET DIE APP AN, NICHT DU:
Wichtig: Diese beiden Regeln rechnet das System NACH deiner Bewertung selbst aus.
Wende sie NICHT selbst an und ziehe dafür keine Punkte ab. Bewerte die Stufe jedes
Kriteriums ausschließlich nach den offiziellen Deskriptoren oben.
- Fehlt ein Leitpunkt, kann Kriterium I höchstens Stufe C sein.
- Unter 100 Wörtern: Kriterium I höchstens C. Von 100 bis 149 Wörtern: höchstens B.
Wenn du die Länge zusätzlich selbst bestrafst, schwankt dieselbe Stufe zwischen zwei
Bewertungen desselben Textes, und mit ihr die Punktzahl.

### BESTEHENSGRENZE (UNSERE, NICHT DIE DER PRÜFUNG):
- Gesamtpunktzahl: Summe der 4 Kriterien (0-100 Punkte).
- BESTANDEN: mindestens 60 Punkte GESAMT und kein Kriterium mit Stufe D.
- NICHT BESTANDEN: unter 60 Punkte ODER ein beliebiges Kriterium mit Stufe D.
- Zur Einordnung: In der echten Prüfung gibt es die D-Regel NICHT. Dort braucht man
  60 % der 240 Gesamtpunkte (144) und mindestens drei der vier Subtests über 60 %;
  ein schwächerer Subtest kann ausgeglichen werden. Unsere Skala ist strenger, damit
  du in der Prüfung Luft hast.

### DIE VIER SCHRITTE DER FEHLERDIAGNOSE (verbindlich, in dieser Reihenfolge)
1. LESEN: Lies den Text Satz für Satz, wörtlich so, wie er dasteht.
2. PRÜFEN: Prüfe jeden Satz gegen die Prüfliste unten und notiere Kandidaten.
3. FALSIFIZIEREN: Formuliere für jeden Kandidaten die konkrete Regel und prüfe sie am
   konkreten Satz. Welches Wort steht in welchem Kasus? Welche Endung verlangt der
   Artikel/das Pronomen? Welches Verb gehört an welche Position? Hält die Regel nicht
   stand (z. B. weil die Endung schon richtig ist), streiche den Kandidaten.
4. BELEGEN: Zitiere den kleinsten Abschnitt, der den Fehler enthält, und benenne die
   Änderung. Lies danach die korrigierte Stelle im Satz noch einmal und prüfe, ob sie
   grammatisch und inhaltlich unverändert passt.

### PRÜFLISTE: HIER WIRD AM HÄUFIGSTEN FALSCH BEWERTET
Das ist eine Prüfliste, kein Suchmuster. Melde nur, was wörtlich im Text steht.
- Adjektive nach »alle«: »für alle Beteiligten« — substantiviertes Adjektiv, groß
  geschrieben, Endung -en. Bei »für alle beteiligten« ist AUSSCHLIESSLICH die
  Großschreibung falsch; die Endung ist bereits richtig. Melde keinen
  »Deklinationsfehler« und schlage nicht »beteiligte« vor.
- »zum Thema« + Genitiv: »zum Thema zusätzlicher Aufgaben«, nicht »… zusätzliche
  Aufgaben«.
- Zwei Nebensätze mit »und«: »weil viele Mitarbeiter Überstunden machen und nicht noch
  mehr Arbeit leisten können« — kein Komma vor »und«; nach »und« steht das Subjekt im
  Nominativ oder es entfällt. Setze dort KEIN Relativpronomen »die« ein: Es würde sich
  auf das letzte Nomen beziehen und den Satz zerstören.
- Grußformeln: »Mit freundlichen Grüßen« ohne Komma, Name in der nächsten Zeile.
  »Liebe Grüße«, »Herzliche Grüße«, »Beste Grüße«: ein vorhandenes Komma BLEIBT stehen,
  und ein fehlendes Komma ist kein Fehler. Baue die Grußformel nie um.
- Anglizismen und Komposita: »Work-Life-Balance«, »Homeoffice«, »New Work« sind korrekt.
- Modalverben und Negation: »nicht noch mehr Arbeit leisten können« ist korrekt;
  »keine gute Idee sein« ist grammatisch korrekt, aber umgangssprachlich → Stil, kein
  Grammatikfehler.
- Satzfragmente: Ein Satz ohne finites Verb im Hauptsatz (»Eine Gruppe, die … kann, und
  eine zweite Gruppe, die … übernimmt.«) ist ein Satzbaufehler. Melde ihn, auch wenn der
  Inhalt verständlich ist.
- Präpositionen und Kasus beim Verb: Prüfe das, was das Verb verlangt (»sich beteiligen
  an + Dat.«, »führen zu + Dat.«, »beitragen zu + Dat.«, »eine Lösung für + Akk.«).

### EIN EINTRAG IN `critical_errors` — FELD FÜR FELD
- `original`: wörtlich und zeichengenau aus dem Text, MIT den Fehlern des Teilnehmers.
  Kleinster sinnvoller Abschnitt: in der Regel das falsche Wort bzw. die falsche
  Wortgruppe, nicht der ganze Satz. Obergrenze: etwa 80 Zeichen. Bei einem
  Groß-/Kleinschreibungs- oder Buchstabenfehler zitierst du NUR das betroffene Wort.
- `correction`: genau EINE korrigierte Fassung derselben Stelle. Keine Alternativen
  (»A / B«, »oder«), keine Erklärung, keine zusätzlichen Wörter.
- `change`: in einem Halbsatz, was sich ändert — in derselben Sprache wie `rule_es`
  (also Spanisch bzw. Russisch), die deutschen Formen bleiben als Zitat: z. B.
  »solo mayúscula: beteiligten → Beteiligten«, »falta la -r: Mitarbeite → Mitarbeiter«,
  »el verbo va al final«, »la coma desaparece«.
- `rule_es`: die Regel, die GENAU diese Änderung erklärt (auf Spanisch). Wenn `change`
  »nur Großschreibung« sagt, muss `rule_es` von Groß-/Kleinschreibung handeln. Erfinde
  keine Regel, die zu einer anderen Änderung passt.
- `type`: "Rechtschreibung" (Buchstaben, Groß-/Kleinschreibung), "Zeichensetzung" (nur
  Komma, Punkt und andere Satzzeichen), "Grammatik" (Kasus, Kongruenz, Verbstellung,
  Präpositionen), "Satzbau" (Satzstruktur, fehlende Satzteile), "Wortschatz", "Stil".

### VERBOTEN
- Inhalt ändern, Argumente ergänzen, streichen oder umformulieren. Du korrigierst
  Sprache, nicht Meinungen.
- Korrekte Stellen »verschönern« oder »auf B2-Niveau heben«. Das gehört in
  `areas_for_improvement` oder in die Musterlösung, nicht in die Korrektur.
- Einträge, in denen `original` und `correction` gleich lauten (das ist kein Fehler).
- Mehrere Varianten in `correction` (kein »/«, kein »oder«).
- Fehler erfinden, um die Liste zu füllen. Höchstens 12 Einträge; bei mehr Fehlern
  priorisierst du Rechtschreibung und Zeichensetzung, dann Grammatik, dann Satzbau,
  und Stil nur, wenn sonst alles korrekt ist.
- Ist der Text fehlerfrei, ist `critical_errors` eine leere Liste. Das ist ein gutes
  Ergebnis, kein Grund, etwas zu erfinden.

### `corrected_version` — KORREKTURFASSUNG, KEINE NEUFASSUNG
Regel: `corrected_version` ist der Text des Teilnehmers, Wort für Wort, mit
AUSSCHLIESSLICH den unter `critical_errors` gelisteten Korrekturen.
- Übernimm Aufbau, Absätze, Anrede, Grußformel, Argumente und Reihenfolge unverändert.
- Ändere NICHTS, was nicht als Fehler gelistet ist. Formuliere keine Sätze neu, ergänze
  keine Argumente, streiche keine. Kommt ein `original` mehrfach vor, korrigierst du
  alle Vorkommen.
- Jede `correction` muss in `corrected_version` wörtlich wiederzufinden sein. Wenn sie
  dort nicht steht, hast du sie nicht angewandt.
- Formatierung: Anrede auf eigener Zeile + Leerzeile, Grußformel auf eigener Zeile nach
  Leerzeile, Name darunter. Das Komma der Grußformel richtet sich nach dem Original.
- Wenn deine Korrekturfassung Argumente enthält, die der Teilnehmer nicht geschrieben
  hat, hast du die Aufgabe verfehlt.

### `musterloesung` — HIER darfst du frei schreiben
Eine alternative 100-Punkte-Musterlösung zur selben Aufgabe: frei formuliert, B2-Niveau,
mit abwechslungsreichen Konnektoren und Nomen-Verb-Verbindungen. Sie ersetzt NICHT die
Korrekturfassung und wird nicht mit ihr vermischt.

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
      "original": "viele Mitarbeite schon",
      "correction": "viele Mitarbeiter schon",
      "change": "falta la -r final: Mitarbeite → Mitarbeiter",
      "rule_es": "El plural de 'Mitarbeiter' no cambia la raíz, pero la forma completa exige la -r final: 'Mitarbeiter' (no 'Mitarbeite').",
      "type": "Rechtschreibung"
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
  "corrected_version": "Sehr geehrte(r) Frau/Herr [Name],\n\n[Derselbe Text des Teilnehmers, nur mit den gelisteten Korrekturen angewandt; Absätze wie im Original]\n\nMit freundlichen Grüßen\n[Vorname Nachname]",
  "musterloesung": "Sehr geehrte(r) Frau/Herr [Name],\n\n[Musterlösung alternativa de 100 puntos según estándares telc B2 con conectores variados y párrafos claros]\n\nMit freundlichen Grüßen\n[Vorname Nachname]"
}

WICHTIGE VORGABEN:
- `score_total` MUSS eine Ganzzahl (0-100) sein und der Summe der 4 Kriterien (`score`) entsprechen.
- Jedes Kriterium in `criteria` MUSS die Felder `grade` (A, B, C oder D), `score` (die Zahl der Tabelle für diese Stufe) und `feedback` enthalten.
- In `critical_errors`: Analysiere den Text gründlich und liste ALLE Fehler auf, die sich belegen lassen (Grammatik, Verbposition/Satzbau, Deklination/Kasus, Präpositionen, unpassende Wortwahl, Rechtschreibung, Zeichensetzung). Was du nicht belegen kannst, listest du NICHT.
  * `original`: MUSS ein EXAKTES, wörtliches Zitat (Substring) aus dem Text des Teilnehmers sein (ohne Anführungszeichen drumherum), damit der Fehler exakt an dieser Stelle im Text farbig markiert werden kann.
    - Zitiere `original` ZEICHEN FÜR ZEICHEN so, wie der Teilnehmer es geschrieben hat — auch MIT seinen Fehlern. Schreibe NIEMALS die bereits korrigierte Form ins Feld `original` (bei einem Großschreibungsfehler steht dort also z. B. `beteiligten faire Lösung`, NICHT `Beteiligten faire Lösung`).
    - Prüfe vor der Ausgabe, ob dieser Wortlaut wirklich genau so im Text vorkommt. Wenn nicht, zitiere den tatsächlichen Wortlaut.
    - Halte das Zitat kurz (Richtwert: höchstens 80 Zeichen). Ein ganzer Satz als Zitat für einen Fehler in einem Wort ist ein Formfehler.
  * `correction`: Die korrigierte Version der Passage auf Deutsch (B2-Niveau).
    - `correction` MUSS sich von `original` unterscheiden. Wenn du keine echte Änderung nennen kannst, ist es KEIN Fehler: dann lass den Eintrag ganz weg. Ein Eintrag, in dem `original` und `correction` gleich lauten, ist ungültig.
    - Genau EINE Fassung: keine Alternativen mit »/« oder »oder«.
  * `change`: Pflichtfeld. Benenne den Delta konkret (siehe oben). Ohne Delta keine Regel.
  * `rule_es`: Präzise, verständliche und lehrreiche Erklärung der Grammatik- oder Ausdrucksregel auf SPANISCH (oder auf RUSSISCH, falls im User-Prompt angewiesen).
    - Die Erklärung MUSS zu dem zitierten Fehler passen: wenn du Groß- und Kleinschreibung bemängelst, muss im Zitat auch wirklich ein Wort falsch groß- oder kleingeschrieben sein, und die Regel muss von Groß-/Kleinschreibung handeln.
  * `type`: "Grammatik", "Wortschatz", "Rechtschreibung" (Groß-/Kleinschreibung, falsch geschriebene Wörter), "Zeichensetzung" (nur Kommas, Punkte und andere Satzzeichen), "Stil" oder "Satzbau".
- QUALITÄT UND FORMATIERUNG VON `corrected_version` UND `musterloesung`:
  * KEIN unleserlicher Textblock! Du MUSST den Text mit echten Leerzeilen (`\n\n`) optisch in Absätze gliedern.
  * Anrede (z. B. `Sehr geehrte(r) Frau/Herr [Name],` oder `Liebe Kolleginnen und Kollegen,`) steht zwingend auf einer EIGENEN Zeile, gefolgt von einer Leerzeile (`\n\n`).
  * Grußformel (z. B. `Mit freundlichen Grüßen` oder `Herzliche Grüße`) steht auf einer EIGENEN Zeile nach einer Leerzeile (`\n\n`), der Name darunter ohne Punkt.
  * FORMALIE: Nach `Mit freundlichen Grüßen` steht kein Komma. Bei persönlichen Grußformeln wie `Liebe Grüße` bleibt das Komma des Originals erhalten.
  * Sprachliches Niveau: `musterloesung` nutzt anspruchsvolles, flüssiges und natürliches Berufsdeutsch B2 (abwechslungsreiche Konnektoren wie `darüber hinaus`, `des Weiteren`, `infolgedessen`, `demnach`; Nomen-Verb-Verbindungen wie `eine Vereinbarung treffen`, `zur Verfügung stehen`, `Kenntnis nehmen`). `corrected_version` bleibt dagegen so nah wie möglich am Originaltext.
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
                        "score": {"type": "integer", "minimum": 0, "maximum": 34},
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
                        "score": {"type": "integer", "minimum": 0, "maximum": 22},
                        "feedback": {"type": "string"}
                    }
                },
                "korrektheit": {
                    "type": "object",
                    "required": ["grade", "score", "feedback"],
                    "properties": {
                        "grade": {"type": "string", "enum": ["A", "B", "C", "D"]},
                        "score": {"type": "integer", "minimum": 0, "maximum": 22},
                        "feedback": {"type": "string"}
                    }
                },
                "repertoire": {
                    "type": "object",
                    "required": ["grade", "score", "feedback"],
                    "properties": {
                        "grade": {"type": "string", "enum": ["A", "B", "C", "D"]},
                        "score": {"type": "integer", "minimum": 0, "maximum": 22},
                        "feedback": {"type": "string"}
                    }
                }
            }
        },
        "critical_errors": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["original", "correction", "change", "rule_es", "type"],
                "properties": {
                    "original": {"type": "string"},
                    "correction": {"type": "string"},
                    "change": {"type": "string"},
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


def count_words(text: str) -> int:
    """Cuenta palabras igual que la app: secuencias de letras, dígitos, '_' y '-'."""
    return len(re.findall(r"[\w\-]+", text or "", flags=re.UNICODE))


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
        # El recuento lo hace el sistema: contando por su cuenta se equivocaba
        # entre un 15 % y un 20 %. Y el castigo por quedarse corto también lo
        # aplica la app: si lo aplica el modelo, la misma banda oscila.
        f"Der Text umfasst GENAU {count_words(student_text)} Wörter (vom System gezählt). "
        "Zähle NICHT selbst nach, und ziehe für eine zu geringe Länge KEINE Punkte ab: "
        "das rechnet die App nach deiner Bewertung.",
        "\n=======================================================",
        "### TEXT DES PRÜFUNGSTEILNEHMERS (ZUR BEWERTUNG):",
        f"\"\"\"\n{student_text}\n\"\"\"",
        "=======================================================",
        "\n### ERINNERUNG FÜR DIE FEHLERLISTE",
        "- Prüfe jeden Satz gegen die Prüfliste und belege jeden Eintrag wörtlich.",
        "- Lass Korrektes stehen: keine »Verbesserung« ohne echten Fehler.",
        "- `corrected_version` ist die Korrekturfassung des Teilnehmertextes (nur die gelisteten",
        "  Korrekturen angewandt) und keine Neufassung.",
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


# ---------------------------------------------------------------------------
# Validación mecánica del contrato
# ---------------------------------------------------------------------------

MAX_SPAN_CHARS = 80          # más que esto casi siempre es "el párrafo por la palabra"
_CASE_HINTS = ("mayúscula", "mayuscula", "minúscula", "minuscula",
               "großschreibung", "kleinschreibung", "orthograf", "ortograf")
_PUNCT_HINTS = ("coma", "komma", "punto", "punkt", "zeichensetzung", "satzzeichen",
                "signo de puntuación", "puntuación", "puntuacion")


def _norm_ws(s: str) -> str:
    return " ".join(str(s or "").split())


def _tight_span(s: str, limit: int = 30) -> str:
    """Recorte alrededor del cambio para no imprimir párrafos en los mensajes."""
    s = _norm_ws(s)
    return s if len(s) <= limit else s[:limit] + "…"


def _only_case_diff(a: str, b: str) -> bool:
    return a != b and a.casefold() == b.casefold()


def _only_punct_diff(a: str, b: str) -> bool:
    """Mismo texto salvo signos de puntuación / espacios."""
    strip = lambda s: re.sub(r"[\s\W_]+", "", s, flags=re.UNICODE)
    return a != b and strip(a) == strip(b)


def validate_evaluation_json(data: Dict[str, Any],
                             student_text: Optional[str] = None) -> List[str]:
    """
    Valida que un diccionario cumpla el contrato de evaluación telc B2.
    Devuelve una lista de errores encontrados (vacía si es 100% válido).

    Si se pasa `student_text`, además comprueba que cada cita sea literal, que el
    span sea el mínimo, que la corrección sea única y que la regla explique el delta.
    Esas comprobaciones son las que detectan los tres fallos clásicos del corrector:
    citar el párrafo entero, ofrecer "A / B" como corrección y explicar una regla
    que no tiene nada que ver con lo que cambia.
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
    max_por_criterio = {"aufgabenbewaeltigung": 34, "angemessenheit": 22, "korrektheit": 22, "repertoire": 22}
    for c in required_crit:
        if c not in criteria:
            errors.append(f"Falta el criterio requerido en criteria: '{c}'.")
        else:
            c_data = criteria[c]
            if c_data.get("grade") not in ["A", "B", "C", "D"]:
                errors.append(f"Criterio '{c}' tiene un grado inválido: {c_data.get('grade')}")
            tope = max_por_criterio[c]
            if not isinstance(c_data.get("score"), (int, float)) or not (0 <= c_data.get("score") <= tope):
                errors.append(f"Criterio '{c}' tiene puntuación fuera de rango 0-{tope}: {c_data.get('score')}")

    if not isinstance(data.get("critical_errors"), list):
        errors.append("'critical_errors' debe ser una lista.")
    else:
        seen_spans = set()
        for idx, err in enumerate(data.get("critical_errors", [])):
            if not isinstance(err, dict):
                errors.append(f"Error #{idx} en 'critical_errors' no es un objeto.")
                continue
            for f in ["original", "correction", "type"]:
                if f not in err:
                    errors.append(f"Error #{idx} en 'critical_errors' carece del campo '{f}'.")
            if "rule_es" not in err and "rule_ru" not in err and "rule" not in err:
                errors.append(f"Error #{idx} en 'critical_errors' carece de regla de explicación ('rule_es' o 'rule_ru').")

            original = _norm_ws(err.get("original", ""))
            correction = _norm_ws(err.get("correction", ""))
            rule = _norm_ws(err.get("rule_es") or err.get("rule_ru") or err.get("rule", ""))
            change = _norm_ws(err.get("change", ""))
            rule_low = rule.casefold()

            if not change:
                errors.append(
                    f"Error #{idx} («{_tight_span(original)}») no trae 'change': sin decir qué "
                    "cambia exactamente, la regla no es verificable."
                )

            if original and correction and original == correction:
                errors.append(
                    f"Error #{idx}: 'original' y 'correction' son idénticos "
                    f"(«{_tight_span(original)}»); eso no corrige nada."
                )

            # Alternativas: «A / B» o un «oder» que la corrección introduce.
            # Un «oder» que ya estaba en el original es texto del alumno, no una opción.
            ofrece_alternativas = bool(re.search(r"\s/\s", correction)) or (
                bool(re.search(r"\soder\s", correction)) and "oder" not in original.casefold()
            )
            if ofrece_alternativas:
                errors.append(
                    f"Error #{idx} («{_tight_span(original)}»): 'correction' ofrece alternativas "
                    "(«/» u «oder»). Debe ser UNA sola versión corregida."
                )

            if len(original) > MAX_SPAN_CHARS:
                errors.append(
                    f"Error #{idx}: la cita tiene {len(original)} caracteres; el span máximo es "
                    f"{MAX_SPAN_CHARS}. Cita solo el fragmento que contiene el error "
                    f"(«{_tight_span(original)}»)."
                )

            if original and original in seen_spans:
                errors.append(f"Error #{idx} («{_tight_span(original)}»): cita duplicada en la lista.")
            seen_spans.add(original)

            # Coherencia entre lo que cambia y lo que se explica.
            if original and correction:
                if _only_case_diff(original, correction) and not any(h in rule_low for h in _CASE_HINTS):
                    errors.append(
                        f"Error #{idx} («{_tight_span(original)}»): el único cambio es de "
                        "mayúsculas/minúsculas, pero la regla no habla de ortografía "
                        "(Groß-/Kleinschreibung)."
                    )
                elif _only_punct_diff(original, correction) and not any(h in rule_low for h in _PUNCT_HINTS):
                    errors.append(
                        f"Error #{idx} («{_tight_span(original)}»): el único cambio es de "
                        "puntuación, pero la regla no habla de signos de puntuación."
                    )

            if student_text:
                haystack = _norm_ws(student_text)
                if original and original not in haystack:
                    errors.append(
                        f"Error #{idx}: la cita «{_tight_span(original, 60)}» NO aparece tal cual "
                        "en el texto del alumno (¿la escribiste ya corregida o cambiaste "
                        "espacios/signos?)."
                    )

    if not isinstance(data.get("strengths"), list):
        errors.append("'strengths' debe ser una lista.")
    if not isinstance(data.get("areas_for_improvement"), list):
        errors.append("'areas_for_improvement' debe ser una lista.")

    corrected = data.get("corrected_version")
    if not isinstance(corrected, str) or len(corrected.strip()) == 0:
        errors.append("'corrected_version' debe ser una cadena no vacía.")
    elif student_text and isinstance(data.get("critical_errors"), list) and data["critical_errors"]:
        haystack = _norm_ws(corrected)
        if _norm_ws(corrected) == _norm_ws(student_text):
            errors.append(
                "'corrected_version' es idéntico al texto del alumno: no se aplicó ninguna "
                "de las correcciones listadas."
            )
        for idx, err in enumerate(data["critical_errors"]):
            if not isinstance(err, dict):
                continue
            corr = _norm_ws(err.get("correction", ""))
            # Fragmentos cortos (una letra, una coma) pueden aparecer legítimamente
            # dentro de la fassung corregida sin ser rastreables aquí.
            if len(corr) >= 8 and corr not in haystack:
                errors.append(
                    f"Error #{idx}: la corrección «{_tight_span(corr, 50)}» no aparece en "
                    "'corrected_version'; o no se aplicó, o el texto se reescribió."
                )

    return errors
