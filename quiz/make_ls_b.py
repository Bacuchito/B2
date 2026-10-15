import json
import re
import sys

def norm(s):
    return re.sub(r"\s+", " ", str(s or "")).strip()

# 1. p70: Spülmaschine
p70_passage = (
    "Sehr geehrte Frau Sturm,\n\n"
    "vor einer Woche haben wir bei Ihnen eine Spülmaschine für unsere Teeküche gekauft. "
    "Sie wurde sehr schnell geliefert und auch gleich eingebaut. Leider muss ich Ihnen heute aber mitteilen, dass sie bereits defekt ist. "
    "Beim Spülen ist Wasser ausgelaufen und nun ist unser Parkett beschädigt.\n\n"
    "Ich bitte Sie, uns umgehend einen Techniker zu schicken, der das Gerät repariert. "
    "Wir brauchen die Spülmaschine spätestens übermorgen, da wir ein großes Meeting unserer Außendienstmitarbeiter haben und viele Personen bewirten müssen.\n\n"
    "Außerdem müssen wir einen Teil des Parketts austauschen. Die Kosten dafür werden wir Ihnen in Rechnung stellen.\n\n"
    "Bitte schicken Sie mir so schnell wie möglich einer Terminvorschlag für die Reparatur und eine Bestätigung der Kostenübernahme. Vielen Dank!\n\n"
    "Mit freundlichen Grüßen\n"
    "Claudio Krüger"
)

v_p70 = {
    "id": "ls_b-p70",
    "label": "Beschwerde – Variante 4 (Spülmaschine)",
    "topic": "Spülmaschine",
    "page": 70,
    "note": "El bloque de la p. 70 incluye un correo interno previo (Dorothee Sturm encarga enviar un técnico y responder disculpándose): pertenece a la tarea de escritura (ítem 21) y se excluye del passage. Las preguntas 19 y 20 se resuelven íntegramente con la carta de reclamación de Claudio Krüger.",
    "kind": "text",
    "intro": "Lesen Sie die Beschwerde und die Aufgaben 19 und 20. Wählen Sie bei jeder Aufgabe die richtige Lösung a, b oder c.",
    "passage": p70_passage,
    "items": [
        {
            "n": 19,
            "type": "choice",
            "prompt": "Der Kunde",
            "options": [
                {"key": "a", "text": "fordert eine neue Spülmaschine."},
                {"key": "b", "text": "hat einen Wasserschaden in der Küche."},
                {"key": "c", "text": "beschwert sich über die Reparaturarbeiten."}
            ],
            "answer": "b",
            "confidence": "hoch",
            "quote": "Beim Spülen ist Wasser ausgelaufen und nun ist unser Parkett beschädigt.",
            "explain": "Correcto b: el lavavajillas derramó agua durante el lavado y dañó el parqué de la cocina («Beim Spülen ist Wasser ausgelaufen und nun ist unser Parkett beschädigt»), es decir, se produjo un daño por agua (Wasserschaden). a es falso porque no pide una máquina nueva sino la reparación de la existente («der das Gerät repariert»); c es falso porque aún no se han hecho reparaciones, la queja es por la avería de la máquina recién instalada."
        },
        {
            "n": 20,
            "type": "choice",
            "prompt": "Die Firma Küchenbedarf soll",
            "options": [
                {"key": "a", "text": "die Reparatur der Spülmaschine in Rechnung stellen."},
                {"key": "b", "text": "innerhalb von zwei Tagen die Spülmaschine reparieren."},
                {"key": "c", "text": "das Parkett in der Teeküche umgehend ersetzen."}
            ],
            "answer": "b",
            "confidence": "hoch",
            "quote": "Wir brauchen die Spülmaschine spätestens übermorgen, da wir ein großes Meeting unserer Außendienstmitarbeiter haben und viele Personen bewirten müssen.",
            "explain": "Correcto b: el cliente necesita el aparato reparado a más tardar pasado mañana («spätestens übermorgen»), es decir, en un plazo de dos días, para una reunión importante. a es falso porque no pide que le cobren la reparación, sino una garantía de reparación y asunción de costes; c es falso porque la sustitución del parqué la gestionan ellos mismos y le pasarán la factura a la empresa («müssen wir einen Teil des Parketts austauschen. Die Kosten dafür werden wir Ihnen in Rechnung stellen»)."
        }
    ]
}

# 2. p71: Umzug
p71a_passage = (
    "Sehr geehrte Frau Börne,\n\n"
    "am Wochenende ist unser Büro mit Hilfe Ihres Unternehmens von Hanau nach Frankfurt umgezogen. Leider waren wir mit Ihrem Service überhaupt nicht zufrieden.\n\n"
    "Ihre Mitarbeiter kamen eine halbe Stunde zu spät und nur zu dritt statt wie vereinbart zu viert. Deshalb dauerte der ganze Umzug natürlich länger als geplant und einige Arbeiten sind auch noch nicht abgeschlossen: Es sind noch nicht alle Möbel aufgebaut, deshalb konnten wir noch nicht unsere Sachen einräumen.\n\n"
    "Bitte schicken Sie uns deshalb am Mittwochmorgen noch zwei Personen, die den Möbelaufbau erledigen. Des Weiteren sind Glasplatten zu Bruch gegangen und einige Schränke sind verkratzt. Ich gehe davon aus, dass Ihre Firma die Kosten dafür übernimmt.\n\n"
    "Mit freundlichen Grüßen\n"
    "Thomas Zaun"
)

v_p71a = {
    "id": "ls_b-p71a",
    "label": "Beschwerde – Variante 5 (Umzug – Fassung 1, Thomas Zaun)",
    "topic": "Umzug",
    "page": 71,
    "note": "La p. 71 presenta la reclamación de la mudanza de Hanau a Fráncfort con dos formulaciones de preguntas (Fassung 1: Thomas Zaun / Börne; Fassung 2: Matteo Lozano / Prince). El correo interno de Frieda Börne se omite por pertenecer a la tarea de redacción.",
    "kind": "text",
    "intro": "Lesen Sie die Beschwerde und die Aufgaben 19 und 20. Wählen Sie bei jeder Aufgabe die richtige Lösung a, b oder c.",
    "passage": p71a_passage,
    "items": [
        {
            "n": 19,
            "type": "choice",
            "prompt": "Herr Zaun beschwert sich über",
            "options": [
                {"key": "a", "text": "die Mitarbeiter der Firma."},
                {"key": "b", "text": "die Qualität von Produkten."},
                {"key": "c", "text": "eine ausbleibende Lieferung."}
            ],
            "answer": "a",
            "confidence": "hoch",
            "quote": "Ihre Mitarbeiter kamen eine halbe Stunde zu spät und nur zu dritt statt wie vereinbart zu viert.",
            "explain": "Correcto a: se queja de la impuntualidad y la falta de personal del equipo de mudanza («Ihre Mitarbeiter kamen eine halbe Stunde zu spät und nur zu dritt statt wie vereinbart zu viert») así como de los desperfectos que ocasionaron. b es falso porque no se trata de productos sino de un servicio de mudanza; c es falso porque no falta una entrega, la mudanza se realizó pero con retraso y daños."
        },
        {
            "n": 20,
            "type": "choice",
            "prompt": "Herr Zaun",
            "options": [
                {"key": "a", "text": "ist nach Hanau gezogen."},
                {"key": "b", "text": "musste seinen Umzug verschieben."},
                {"key": "c", "text": "verlangt Schadensersatz."}
            ],
            "answer": "c",
            "confidence": "hoch",
            "quote": "Des Weiteren sind Glasplatten zu Bruch gegangen und einige Schränke sind verkratzt. Ich gehe davon aus, dass Ihre Firma die Kosten dafür übernimmt.",
            "explain": "Correcto c: exige que la empresa asuma el coste de los cristales rotos y muebles rayados («dass Ihre Firma die Kosten dafür übernimmt»), lo que equivale a reclamar una indemnización por daños (Schadensersatz). a es falso porque se mudaron DE Hanau A Fráncfort («von Hanau nach Frankfurt umgezogen»), no hacia Hanau; b es falso porque la mudanza se llevó a cabo el fin de semana, no se aplazó."
        }
    ]
}

p71b_passage = (
    "Sehr geehrte Frau Prince,\n\n"
    "am Wochenende ist unser Büro mit Hilfe Ihres Unternehmens von Hanau nach Frankfurt umgezogen. Leider waren wir mit Ihrem Service überhaupt nicht zufrieden.\n\n"
    "Ihre Mitarbeiter kamen eine halbe Stunde zu spät und nur zu dritt statt wie vereinbart zu viert. Deshalb dauerte der ganze Umzug natürlich länger als geplant und einige Arbeiten sind auch noch nicht abgeschlossen: Es sind noch nicht alle Möbel aufgebaut, deshalb konnten wir noch nicht unsere Sachen einräumen.\n\n"
    "Bitte schicken Sie uns deshalb am Mittwochmorgen noch zwei Personen, die den Möbelaufbau erledigen. Des Weiteren sind Glasplatten zu Bruch gegangen und einige Schränke sind verkratzt. Ich gehe davon aus, dass Ihre Firma die Kosten dafür übernimmt.\n\n"
    "Mit freundlichen Grüßen\n"
    "Matteo Lozano"
)

v_p71b = {
    "id": "ls_b-p71b",
    "label": "Beschwerde – Variante 5 (Umzug – Fassung 2, Matteo Lozano)",
    "topic": "Umzug",
    "page": 71,
    "note": "Segunda formulación de preguntas de la p. 71 («второй вариант вопросов»), con los nombres alternativos (Matteo Lozano, Sophia Prince) anotados en el original.",
    "kind": "text",
    "intro": "Lesen Sie die Beschwerde und die Aufgaben 19 und 20. Wählen Sie bei jeder Aufgabe die richtige Lösung a, b oder c.",
    "passage": p71b_passage,
    "items": [
        {
            "n": 19,
            "type": "choice",
            "prompt": "Beim Umzug",
            "options": [
                {"key": "a", "text": "haben vier Möbelpacker gearbeitet."},
                {"key": "b", "text": "kam es zu Verzögerungen."},
                {"key": "c", "text": "wurden nicht alle Möbel transportiert."}
            ],
            "answer": "b",
            "confidence": "hoch",
            "quote": "Deshalb dauerte der ganze Umzug natürlich länger als geplant und einige Arbeiten sind auch noch nicht abgeschlossen:",
            "explain": "Correcto b: la mudanza sufrió demoras («dauerte der ganze Umzug natürlich länger als geplant») debido a que los operarios llegaron media hora tarde y eran tres en vez de cuatro. a es falso porque trabajaron tres mozos («nur zu dritt statt wie vereinbart zu viert»); c es falso porque los muebles se transportaron todos, lo que quedó pendiente fue el montaje («Es sind noch nicht alle Möbel aufgebaut»)."
        },
        {
            "n": 20,
            "type": "choice",
            "prompt": "Herr Lozano",
            "options": [
                {"key": "a", "text": "musste seinen Umzug verschieben."},
                {"key": "b", "text": "verlangt Schadensersatz."},
                {"key": "c", "text": "ist nach Hanau gezogen."}
            ],
            "answer": "b",
            "confidence": "hoch",
            "quote": "Des Weiteren sind Glasplatten zu Bruch gegangen und einige Schränke sind verkratzt. Ich gehe davon aus, dass Ihre Firma die Kosten dafür übernimmt.",
            "explain": "Correcto b: reclama que la empresa cubra los costes de los daños causados en cristales y armarios («Ich gehe davon aus, dass Ihre Firma die Kosten dafür übernimmt»), es decir, indemnización por daños. a es falso porque la mudanza se ejecutó durante el fin de semana; c es falso porque el traslado fue de Hanau a Fráncfort."
        }
    ]
}

# 3. p72: Der Drucker
p72_passage = (
    "Sehr geehrte Frau Aichele,\n\n"
    "vorgestern wurde von einem Ihrer Mitarbeiter unser fast neues Druck- und Kopiergerät der Marke Lexios zum dritten Mal innerhalb von zwei Wochen geprüft, da bei diesem immer wieder Papierstaus aufgetreten sind. "
    "Gestern kam es schon wieder zu einer Fehlermeldung, was zur Folge hatte, dass wir Unterlagen nicht fristgerecht einreichen konnten. Aus diesem Grund haben wir eine für uns sehr wichtige Ausschreibung verpasst. "
    "Von einer Schadensersatzforderung sehen wir vorerst ab, wir fordern Sie aber auf, uns umgehend auf Ihre Kosten ein anderes Gerät zu liefern. "
    "Es handelt sich hier nämlich eindeutig um einen technischen Fehler, den wir nicht zu verantworten haben. Die Rechnungen für die drei vorangegangenen Technikereinsätze werden wir natürlich nicht bezahlen.\n\n"
    "Ich erwarte Ihre umgehende Rückmeldung.\n\n"
    "Mit freundlichen Grüßen\n"
    "Benno Schmidt"
)

v_p72a = {
    "id": "ls_b-p72a",
    "label": "Beschwerde – Variante 6 (Der Drucker – Fassung 1)",
    "topic": "Der Drucker",
    "page": 72,
    "note": "La p. 72 presenta la reclamación de Benno Schmidt sobre un copiador averiado con dos juegos de preguntas alternativos en el PDF. En el ítem 20 (Die Firma Copyprofi), la opción a («besteht auf der Bezahlung der Rechnungen») refleja la respuesta dada en el correo interno de Sibyl Aichele («Die Kosten für die Überprüfung des Geräts bleiben die Angelegenheit der Mova GmbH»); como dicho correo pertenece a la tarea de redacción y queda fuera del passage, la confianza se marca como «mittel».",
    "kind": "text",
    "intro": "Lesen Sie die Beschwerde und die Aufgaben 19 und 20. Wählen Sie bei jeder Aufgabe die richtige Lösung a, b oder c.",
    "passage": p72_passage,
    "items": [
        {
            "n": 19,
            "type": "choice",
            "prompt": "Das Gerät",
            "options": [
                {"key": "a", "text": "ist erst seit Kurzem im Einsatz."},
                {"key": "b", "text": "muss noch mal überprüft werden."},
                {"key": "c", "text": "wurde immer richtig bedient."}
            ],
            "answer": "a",
            "confidence": "hoch",
            "quote": "vorgestern wurde von einem Ihrer Mitarbeiter unser fast neues Druck- und Kopiergerät der Marke Lexios zum dritten Mal innerhalb von zwei Wochen geprüft, da bei diesem immer wieder Papierstaus aufgetreten sind.",
            "explain": "Correcto a: el aparato es «fast neu» (casi nuevo) y ha sido revisado tres veces en dos semanas, lo que indica que lleva poco tiempo en funcionamiento en la oficina. b es falso porque el cliente no pide otra revisión sino la sustitución inmediata por otra máquina («ein anderes Gerät zu liefern»); c no es seguro porque el servicio técnico achaca los fallos al mal uso."
        },
        {
            "n": 20,
            "type": "choice",
            "prompt": "Die Firma Copyprofi",
            "options": [
                {"key": "a", "text": "besteht auf der Bezahlung der Rechnungen."},
                {"key": "b", "text": "repariert den Kopierer noch einmal kostenfrei."},
                {"key": "c", "text": "tauscht das Gerät schnellstmöglich aus."}
            ],
            "answer": "a",
            "confidence": "mittel",
            "quote": "Die Rechnungen für die drei vorangegangenen Technikereinsätze werden wir natürlich nicht bezahlen.",
            "explain": "Correcto a: el cliente rechaza pagar las tres facturas anteriores («werden wir natürlich nicht bezahlen») y la empresa Copyprofi insiste en que las abone (en el correo interno: «Die Kosten für die Überprüfung des Geräts bleiben die Angelegenheit der Mova GmbH»). Confianza media porque la confirmación explícita de la postura de la empresa está en la nota interna excluida del texto de lectura. b y c son falsos: la empresa no cambia el equipo ni ofrece repararlo gratis, solo una sesión formativa al personal."
        }
    ]
}

v_p72b = {
    "id": "ls_b-p72b",
    "label": "Beschwerde – Variante 6 (Der Drucker – Fassung 2)",
    "topic": "Der Drucker",
    "page": 72,
    "note": "Segunda formulación de preguntas de la p. 72 («второй вариант вопросов»): ítems centrados en el problema de atascos y la exigencia de sustitución del equipo.",
    "kind": "text",
    "intro": "Lesen Sie die Beschwerde und die Aufgaben 19 und 20. Wählen Sie bei jeder Aufgabe die richtige Lösung a, b oder c.",
    "passage": p72_passage,
    "items": [
        {
            "n": 19,
            "type": "choice",
            "prompt": "Beim Gerät",
            "options": [
                {"key": "a", "text": "handelt sich um ein älteres Modell."},
                {"key": "b", "text": "kommt es häufig zu Papierstaus."},
                {"key": "c", "text": "wurde es nur einmal überprüft."}
            ],
            "answer": "b",
            "confidence": "hoch",
            "quote": "da bei diesem immer wieder Papierstaus aufgetreten sind.",
            "explain": "Correcto b: el cliente señala que la máquina sufre atascos de papel continuos («immer wieder Papierstaus aufgetreten sind»). a es falso porque es un aparato casi nuevo («fast neues … Gerät»), no un modelo antiguo; c es falso porque ya se inspeccionó tres veces en dos semanas («zum dritten Mal innerhalb von zwei Wochen geprüft»)."
        },
        {
            "n": 20,
            "type": "choice",
            "prompt": "Herr Schmidt",
            "options": [
                {"key": "a", "text": "verlangt die Lieferung eines neuen Geräts."},
                {"key": "b", "text": "möchte weitere Technikertermine vereinbaren."},
                {"key": "c", "text": "akzeptiert die bisherigen Rechnungen."}
            ],
            "answer": "a",
            "confidence": "hoch",
            "quote": "wir fordern Sie aber auf, uns umgehend auf Ihre Kosten ein anderes Gerät zu liefern.",
            "explain": "Correcto a: el cliente exige formalmente que le entreguen otro aparato de sustitución a cargo de la empresa proveedora («fordern Sie aber auf, uns umgehend auf Ihre Kosten ein anderes Gerät zu liefern»). b es falso porque rechaza más revisiones técnicas que no solucionan el fallo; c es falso porque se niega rotundamente a pagar las facturas de las intervenciones previas («werden wir natürlich nicht bezahlen»)."
        }
    ]
}

out_data = {
    "block": "ls_b",
    "section": "lesen-us",
    "variants": [v_p70, v_p71a, v_p71b, v_p72a, v_p72b]
}

# Validación previa
for v in out_data["variants"]:
    np_ = norm(v["passage"])
    for it in v["items"]:
        keys = [o["key"] for o in it["options"]]
        assert it["answer"] in keys
        assert norm(it["quote"]) in np_, f"Quote not in passage for {v['id']} item {it['n']}: {it['quote']}"

with open(r"quiz\data\ls_b.json", "w", encoding="utf-8") as f:
    json.dump(out_data, f, ensure_ascii=False, indent=1)

print("ls_b.json escrito con éxito!")
