import json
import re

def norm(s):
    return re.sub(r"\s+", " ", str(s or "")).strip()

p59_passage = (
    "Protokoll 15.01.20XX, 10.00 bis 11.30 Uhr\n"
    "Sitzungsraum 205, Ort: Hauptstraße 27, 99099 Erfurt\n"
    "Anwesende: Jakob Müller (JM, Geschäftsleitung), Friedrich Döring (FD, Vertrieb), Karl Altmann (KA, Buchhaltung und Finanzen), "
    "Peter Bischoff (PB, Produktion), Karsten Hinz (KH, Logistik), Jana Bartsch (JB, Personal), Beate Fritsch (BF, Marketing), Jonas Stoll (JS, IT-Abteilung).\n"
    "Sitzungsleitung: Jakob Müller\n"
    "Protokollant: Jonas Stoll\n\n"
    "Tagesordnungspunkte:\n"
    "1. Begrüßung und Tagesordnung\n"
    "2. Kosteneinsparungen\n"
    "3. Lagebericht Produktion\n"
    "4. Kündigung des Betriebsarztes\n"
    "5. Betriebliche Altersvorsorge\n"
    "6. Sonstiges\n\n"
    "TOP 1 Begrüßung und Tagesordnung\n"
    "JM heißt die Kolleg*innen zur heutigen Besprechung herzlich willkommen und bestätigt die Anwesenheit aller eingeladenen Teilnehmer*innen. "
    "Danach erkundigt JM sich, ob noch zusätzliche Themen protokollarisch aufgenommen werden sollen. Hierzu gibt es keine Kommentare und damit gilt die Tagesordnung als genehmigt.\n\n"
    "TOP 2 Kosteneinsparungen\n"
    "Wie JM darstellt, hat sich der Markt im Vergleich zum Vorjahr stark verändert. In diesem Zusammenhang müssen deshalb Kostenstrukturen neu überdacht werden. "
    "Es wird vorgeschlagen, die administrativen Kosten zu senken, da es hier Einsparungspotential gibt. Im Vorfeld zu dieser Besprechung wurde JB bereits von der Geschäftsleitung beauftragt, "
    "eine exakte Kostenübersicht zu erstellen und Vorschläge zur Kostenreduzierung vorzulegen. JB legt dar, dass die in der Firmenzentrale eingehenden Anrufe auf ein externes Call-Center umgeleitet werden könnten. "
    "Verschiedene Kostenvoranschläge wurden hierfür auch schon eingeholt. Die Firma tele-info scheint unseren Ansprüchen am besten gerecht zu werden. "
    "Deshalb sollten Vertragsverhandlungen aufgenommen und zeitgleich Schulungspläne für die Call-Center-Mitarbeiter*innen ausgearbeitet werden, um ihnen die Organisationsstruktur des Unternehmens "
    "so schnell wie möglich näherzubringen, damit die Arbeit ohne Verzögerung aufgenommen werden kann. Durch die so gewonnene Zeitersparnis am Empfang können Mitarbeiter*innen von dort flexibler eingesetzt werden "
    "und zum Beispiel zusätzlich den für das Unternehmer wichtigen Konferenzbereich und die Gästebetreuung übernehmen. JM stimmt den Vorschlägen zu und bittet um Umsetzung der weiteren Schritte.\n\n"
    "TOP 3 Lagebericht Produktion\n"
    "PB merkt an, dass auch in seiner Abteilung eine Kostenreduzierung möglich wäre, indem unausgewogene Lagerungen von Material und Rohstoffen vermieden werden. "
    "Das Lagerungsmanagement ist optimierbar, d.h., dass sowohl zu hohe als auch niedrige Lagermengen vermieden werden müssen, da sie zu unnötigen Kosten führen. "
    "Im Fall von Überbeständen muss neue Lagerfläche geschaffen werden und im Fall von Unterbeständen kann es zu kurzfristigen Produktionsausfällen kommen. "
    "JM beauftragt PB, sich umgehend zusammen mit KH mit dieser Thematik auseinanderzusetzen und zur nächsten Sitzung konkrete Zahlen und Vorschläge vorzulegen.\n\n"
    "TOP 4 Kündigung des Betriebsarztes\n"
    "Mit Bedauern teilt die Geschäftsleitung mit, dass unser Betriebsarzt die Firma zum Jahresende verlässt, da er eine eigene Praxis eröffnen will. "
    "Aus diesem Grund hat sich die Firma entschlossen, die Ersthelferausbildung zu forcieren, damit bei kleineren Verletzungen, die im Produktionsablauf immer wieder auftreten können, "
    "sofort eingegriffen werden kann. Ärztliche Unterstützung bekommen wir ab nächstem Jahr von der Allgemeinärztlichen Praxis Dr. Mertens. Die Kontaktdaten werden bekannt gegeben.\n\n"
    "TOP 5 Betriebliche Altersvorsorge\n"
    "Seit einem Jahr bietet die Firma den Mitarbeiter*innen an, in eine betriebliche Zusatzrente zu investieren. Bisher wird dieses Angebot aber nur von wenigen Kolleg*innen genutzt. "
    "Deshalb werden erneut alle Abteilungsleiter*innen darauf hingewiesen, in ihren Abteilungen über diese Möglichkeit der Altersvorsorge aufzuklären. Interessierte Mitarbeiter*innen können "
    "in der Personalabteilung genauere Informationen erhalten. Zusätzlich bietet die Versicherungsgesellschaft immer donnerstags eine gesonderte Sprechstunde an, zu der man sich aber anmelden muss.\n\n"
    "TOP 6 Sonstiges\n"
    "Die Mitarbeiter*innen werden gebeten, im Intranet abzustimmen, ob die Firma in diesem Jahr für alle Kolleg*innen entweder einen eintägigen Betriebsausflug oder ein Sommerfest organisieren soll. "
    "Für den Betriebsausflug könnten dann auch gleich Vorschläge unterbreitet werden. Die Abstimmung muss bis zum 31.03 erfolgen, damit für das Organisationskomitee noch ausreichend Zeit für die Planung bleibt."
)

v_p59 = {
    "id": "t4_e-p59",
    "label": "Variante 7 (Protokoll 15.01.20XX, Erfurt)",
    "topic": "Kosteneinsparungen, Lagebericht, Betriebsarzt",
    "page": 59,
    "note": "Acta de la reunión del 15.01.20XX en Erfurt (pp. 59-60). El original la etiqueta como «тест №140321, 140301».",
    "kind": "text",
    "intro": "Lesen Sie das Protokoll und die Aufgaben 14–18. Wählen Sie bei jeder Aufgabe die richtige Lösung a, b oder c.",
    "passage": p59_passage,
    "items": [
        {
            "n": 14,
            "type": "choice",
            "prompt": "Bei der Besprechung",
            "options": [
                {"key": "a", "text": "müssen weitere Themen besprochen werden."},
                {"key": "b", "text": "sind alle Mitarbeiter*innen des Unternehmens anwesend."},
                {"key": "c", "text": "wird die Tagesordnung angenommen."}
            ],
            "answer": "c",
            "confidence": "hoch",
            "quote": "Hierzu gibt es keine Kommentare und damit gilt die Tagesordnung als genehmigt.",
            "explain": "Correcto c: tras preguntar el presidente de la sesión si hay puntos adicionales y no haber comentarios, el orden del día se aprueba («gilt die Tagesordnung als genehmigt»). a es falso porque nadie propuso temas adicionales; b es falso porque solo asisten los directores y jefes de departamento, no toda la plantilla."
        },
        {
            "n": 15,
            "type": "choice",
            "prompt": "Um Kosten zu sparen,",
            "options": [
                {"key": "a", "text": "sollen einige Empfangsmitarbeiter*innen in ein Call-Center wechseln."},
                {"key": "b", "text": "werden die Aufgaben der Mitarbeitenden am Empfang neu festgelegt."},
                {"key": "c", "text": "wird der Empfang demnächst geschlossen."}
            ],
            "answer": "b",
            "confidence": "hoch",
            "quote": "Durch die so gewonnene Zeitersparnis am Empfang können Mitarbeiter*innen von dort flexibler eingesetzt werden und zum Beispiel zusätzlich den für das Unternehmer wichtigen Konferenzbereich und die Gästebetreuung übernehmen.",
            "explain": "Correcto b: al desviar las llamadas telefónicas entrantes a un centro de llamadas externo, el personal de recepción asume nuevas tareas (atención de visitas y salas de conferencias). a y c son falsos: el personal no se traslada al call center externo ni se cierra la recepción."
        },
        {
            "n": 16,
            "type": "choice",
            "prompt": "Der Lagerbestand muss",
            "options": [
                {"key": "a", "text": "an die Produktion angepasst werden."},
                {"key": "b", "text": "dauerhaft ausgebaut werden."},
                {"key": "c", "text": "kurzfristig reduziert werden."}
            ],
            "answer": "a",
            "confidence": "hoch",
            "quote": "dass sowohl zu hohe als auch niedrige Lagermengen vermieden werden müssen, da sie zu unnötigen Kosten führen.",
            "explain": "Correcto a: se busca evitar tanto el exceso de existencias (costes de espacio) como la escasez (parones de producción), es decir, equilibrar y ajustar el stock a las necesidades productivas reales. b y c son falsos porque no se pretende ni una reducción drástica ni una ampliación continuada, sino optimización."
        },
        {
            "n": 17,
            "type": "choice",
            "prompt": "Der Betriebsarzt wird",
            "options": [
                {"key": "a", "text": "mit Dr. Mertens zusammenarbeiten."},
                {"key": "b", "text": "zukünftig selbstständig arbeiten."},
                {"key": "c", "text": "zum Jahresende entlassen."}
            ],
            "answer": "b",
            "confidence": "hoch",
            "quote": "dass unser Betriebsarzt die Firma zum Jahresende verlässt, da er eine eigene Praxis eröffnen will.",
            "explain": "Correcto b: el médico de empresa deja la compañía voluntariamente para abrir su propia consulta («da er eine eigene Praxis eröffnen will»), es decir, para ejercer de forma autónoma/independiente. a es falso porque la consulta del Dr. Mertens asume el servicio médico de la empresa en su sustitución, no en cooperación; c es falso porque no ha sido despedido sino que se marcha voluntariamente."
        },
        {
            "n": 18,
            "type": "choice",
            "prompt": "Die betriebliche Altersvorsorge",
            "options": [
                {"key": "a", "text": "kann bei einem vereinbarten Termin besprochen werden."},
                {"key": "b", "text": "nehmen viele Mitarbeiter*innen an."},
                {"key": "c", "text": "wird neu in der Fima eingeführt."}
            ],
            "answer": "a",
            "confidence": "hoch",
            "quote": "Zusätzlich bietet die Versicherungsgesellschaft immer donnerstags eine gesonderte Sprechstunde an, zu der man sich aber anmelden muss.",
            "explain": "Correcto a: la aseguradora ofrece consultas los jueves requiriendo cita previa («zu der man sich aber anmelden muss»). b es falso porque el acta subraya que hasta ahora muy pocos empleados se han acogido («nur von wenigen Kolleg*innen genutzt»); c es falso porque el plan lleva ofertándose un año («Seit einem Jahr bietet die Firma...»)."
        }
    ]
}

p61_passage = (
    "Protokoll 25.06.20XX\n"
    "Sitzungsraum: 112, Ort: Ludwigstr. 23, 79342 Herbolzen\n"
    "Anwesende: Jan Schneider (JS, Geschäftsleitung), Sabine Faust (SF, Leiterin Marketing), Paul Mayer (PM, Leiter Produktion), "
    "Tim Janzen (TJ, Leiter Vertrieb), Chiara Reich (CR, Leiterin IT), Simon Zitzmann (SZ, Leiter Personal), Mona Seil (MS, Leiterin Controlling)\n"
    "Sitzungsleitung: Jan Schneider, Protokollant: Simon Zitzmann\n\n"
    "Tagesordnungspunkte:\n"
    "1. Begrüßung und Genehmigung der Tagesordnungspunkte\n"
    "2. Marketingmaßnahmen\n"
    "3. Berichte\n"
    "4. Erweiterte Überstundenregelung\n"
    "5. Einführung Jobticket\n"
    "6. Sonstiges\n\n"
    "TOP 1 Begrüßung und Genehmigung der Tagesordnungspunkte\n"
    "JS begrüßt die Abteilungsleitungen zur heutigen Sitzung, die daraufhin pünktlich eröffnet wird. Anschließend bittet er um die Genehmigung der Tagesordnungspunkte. "
    "Nach Handzeichen wird die Tagesordnung ohne Ergänzungen und Änderungen einstimmig genehmigt. Als nächster Besprechungstermin wird der 25.06. vor der großen Sommerpause einstimmig festgelegt.\n\n"
    "TOP 2 Marketingmaßnahmen\n"
    "Nach dem im letzten Quartal von MS und TJ festgestellten Absatzrückgang wurden bereits auf der letzten Sitzung neue Verkaufsstrategien beschlossen. "
    "Hierzu wurde von der Geschäftsleitung ein Budget von 350.000 Euro freigegeben. SF berichtet, dass schon im Vorfeld neue Zielgruppen beleuchtet wurden, "
    "insbesondere die Gruppe der Berufseinsteiger und Hochschulabsolventen, also die Altersgruppe 17 bis 25 Jahre. Im Vergleich dazu lag der Fokus bisher auf Verbraucher im Alter von 30 bis 50 Jahren.\n"
    "Zunächst wurde eine Social-Media-Agentur beauftragt, um gezielt neue Endverbraucher anzusprechen. Hierzu liegen auch schon erste Ergebnisse vor, "
    "die zeigen, dass das Interesse die Aufmerksamkeit um 38% gestiegen sind. Infolgedessen stieg der Umsatz um 18 % im Vergleich zum Vorjahr. "
    "JS zeigt sich mit dieser ersten Entwicklung zufrieden und erwartet einen weiteren positiven Trend. Für das nächste Quartal ist geplant, positive Kundenreaktionen im Internet hochzuladen. "
    "SF betont, dass gerade in diesem Bereich die Zukunft liegt und regelmäßige Neuerungen erwartet werden können. Deshalb wird sie in den kommenden Sitzungen regelmäßig neue Konzepte präsentieren.\n\n"
    "TOP 3 Berichte\n"
    "SZ berichtet darüber, dass die Mitarbeitenden in der Produktion seit dem Einbau der neuen Maschinen gehäuft über eine enorme Lärmbelastung klagen würden. "
    "Hier bestehe dringender Handlungsbedarf, da im anderen Fall eine Überprüfung durch die Behörden erfolgen konnte. PM wird mit der Herstellerfirma dieser Anlagen Kontakt aufnehmen, "
    "um dieses Problem zu klären. Bis zur Lösung sollten Gehörschützer benutzt werden.\n\n"
    "TOP 4 Erweiterte Überstundenregelung\n"
    "JS teilt einen Vorschlag der Geschäftsleitung hinsichtlich einer erweiterten Überstundenregelung mit. Aufgrund einer sich ständig ändernden Auftragslage kommt es vor, "
    "dass den Mitarbeitenden immer mehr Überstunden zugemutet werden. Die bisherige Regelung, dass bis zehn Stunden Mehrarbeit im Monat bezahlt werden, bleibt bestehen. "
    "Die Stunden darüber hinaus werden weiterhin als Freizeitausgleich gewährt. Neu kommt hinzu, dass ab dem kommenden Jahr für jeweils 100 geleistete Überstunden jährlich ein Urlaubstag zusätzlich gegeben wird. "
    "SZ wird diese Maßnahme in der nächsten Betriebsratssitzung zur Prüfung und Genehmigung vorlegen.\n\n"
    "TOP 5 Einführung Jobticket\n"
    "Da in der Vergangenheit die Situation auf unseren Firmenparkplätzen sehr angespannt war, nahm die Firma Kontakt zum örtlichen öffentlichen Personennahverkehr auf, "
    "um die Einführung von Jobtickets für die Mitarbeitenden möglich zu machen. Viele Mitarbeitende hatten zuvor diesen Wunsch geäußert. SZ teilt mit, dass die Verhandlungen kurz vor dem Abschluss stehen. "
    "Wer Interesse an diesem günstigen Ticket hat, sollte sich per Mail oder persönlich in der Personalabteilung dafür anmelden. Die Abteilungsleiter übernehmen es, Ihre Abteilungen zu informieren.\n\n"
    "TOP 6\n"
    "Unser Unternehmen und das Fitnesscenter fit und fun, das sich in der unmittelbaren Nähe unserer Firma befindet, haben gemeinsam ein Angebot für unsere Mitarbeiter erarbeitet. "
    "Wenn man seine Betriebszugehörigkeit nachweist, kann man einen Vertrag zu besonders günstigen Konditionen abschließen. SZ schlägt vor, man könnte dort zu einem späteren Zeitpunkt sogar ein Sportfest für die Abteilungen durchführen. Diesen Vorschlag begrüßt JS."
)

v_p61 = {
    "id": "t4_e-p61",
    "label": "Variante 8 (Protokoll Herbolzen)",
    "topic": "Marketingmaßnahmen, Einführung Jobticket",
    "page": 61,
    "note": "Acta de la reunión en Herbolzen (pp. 61-62). El original la etiqueta como «тест №160201, 160221».",
    "kind": "text",
    "intro": "Lesen Sie das Protokoll und die Aufgaben 14–18. Wählen Sie bei jeder Aufgabe die richtige Lösung a, b oder c.",
    "passage": p61_passage,
    "items": [
        {
            "n": 14,
            "type": "choice",
            "prompt": "Die Besprechung",
            "options": [
                {"key": "a", "text": "beginnt zur festgelegten Uhrzeit."},
                {"key": "b", "text": "soll auf den 25.06. verlegt werden."},
                {"key": "c", "text": "wird durch Änderungen ergänzt."}
            ],
            "answer": "a",
            "confidence": "hoch",
            "quote": "JS begrüßt die Abteilungsleitungen zur heutigen Sitzung, die daraufhin pünktlich eröffnet wird.",
            "explain": "Correcto a: la reunión da comienzo con puntualidad («pünktlich eröffnet wird»). b es falso porque el 25.06 es la fecha acordada para la próxima reunión; c es falso porque el orden del día se aprobó sin enmiendas ni modificaciones («ohne Ergänzungen und Änderungen»)."
        },
        {
            "n": 15,
            "type": "choice",
            "prompt": "Die Umsatzsteigerung",
            "options": [
                {"key": "a", "text": "beträgt 350.000 Euro."},
                {"key": "b", "text": "liegt bei 38 %."},
                {"key": "c", "text": "wird sich fortsetzen."}
            ],
            "answer": "c",
            "confidence": "hoch",
            "quote": "JS zeigt sich mit dieser ersten Entwicklung zufrieden und erwartet einen weiteren positiven Trend.",
            "explain": "Correcto c: la dirección manifiesta su satisfacción con el aumento inicial de ventas (+18 %) y anticipa que la tendencia al alza continuará («erwartet einen weiteren positiven Trend»). a es falso porque 350.000 € fue el presupuesto aprobado de marketing; b es falso porque el 38 % se refiere al aumento de atención/interés en redes sociales, no a la facturación."
        },
        {
            "n": 16,
            "type": "choice",
            "prompt": "Die Überstundenregelung",
            "options": [
                {"key": "a", "text": "bleibt genauso bestehen."},
                {"key": "b", "text": "erhält eine Ergänzung."},
                {"key": "c", "text": "gilt ab 100 Überstunden."}
            ],
            "answer": "b",
            "confidence": "hoch",
            "quote": "Neu kommt hinzu, dass ab dem kommenden Jahr für jeweils 100 geleistete Überstunden jährlich ein Urlaubstag zusätzlich gegeben wird.",
            "explain": "Correcto b: el régimen existente se mantiene en sus bases pero añade una cláusula nueva («Neu kommt hinzu... ein Urlaubstag zusätzlich»), recibiendo así un complemento. a es falso porque se amplía; c es falso porque la compensación de horas extras opera desde las primeras horas, no a partir de 100."
        },
        {
            "n": 17,
            "type": "choice",
            "prompt": "Das Jobticket",
            "options": [
                {"key": "a", "text": "ist eine preislich unattraktive Variante."},
                {"key": "b", "text": "können die Mitarbeiter beim ÖPNV kaufen."},
                {"key": "c", "text": "soll den Arbeitsweg stressfreier machen."}
            ],
            "answer": "c",
            "confidence": "hoch",
            "quote": "Da in der Vergangenheit die Situation auf unseren Firmenparkplätzen sehr angespannt war, nahm die Firma Kontakt zum örtlichen öffentlichen Personennahverkehr auf, um die Einführung von Jobtickets für die Mitarbeitenden möglich zu machen.",
            "explain": "Correcto c: la iniciativa surge para aliviar el colapso del aparcamiento de empresa y responder al deseo de los trabajadores, facilitando un desplazamiento más cómodo y sin estrés. a es falso porque se describe expresamente como «diesem günstigen Ticket»; b es falso porque la solicitud se tramita internamente en el departamento de personal de la empresa."
        },
        {
            "n": 18,
            "type": "choice",
            "prompt": "Sportliche Aktivitäten",
            "options": [
                {"key": "a", "text": "finden in dem Unternehmen statt."},
                {"key": "b", "text": "sollen in den Abteilungen stattfinden."},
                {"key": "c", "text": "werden von der Firma gefördert."}
            ],
            "answer": "c",
            "confidence": "hoch",
            "quote": "Wenn man seine Betriebszugehörigkeit nachweist, kann man einen Vertrag zu besonders günstigen Konditionen abschließen.",
            "explain": "Correcto c: la empresa promueve la práctica deportiva negociando con un gimnasio cercano tarifas ventajosas subvencionadas/descontadas para sus empleados («besonders günstige Konditionen»). a y b son falsos porque las actividades no se imparten dentro de las instalaciones ni en los departamentos de la compañía sino en un centro fitness externo."
        }
    ]
}

p63_passage = (
    "Protokoll 19. Februar 20XX, 10.00-11.45 Uhr\n"
    "Konferenzraum 7, Ort: Neuburger Allee 28, 87341 Ballhausen\n"
    "Anwesende: Maria Loppinet (ML, Geschäftsführung), Lukas Meier (LM, Leitung Einkauf), Magda Nauner (MN, Leitung Personal), "
    "Gert Schrader (GS, Leitung Produktion), Peter Schuldt (PS, Leitung Verkauf), Katja Stevens (KS, Leitung Qualitätskontrolle), Volha Schäfer (VS, Leitung Finanzen)\n"
    "Gast: Wanda Lubic (WL, IT-Beauftragte)\n"
    "Sitzungsleitung: Magda Nauner\n"
    "Protokollantin: Volha Schäfer\n\n"
    "Tagesordnungspunkte:\n"
    "1. Begrüßung und Genehmigung des letzten Protokolls\n"
    "2. Stand des Projekts „Fertigungsanlage“\n"
    "3. Berichte\n"
    "4. Neue Mitarbeiterinnen und Mitarbeiter\n"
    "5. Update der Software\n"
    "6. Sonstiges\n\n"
    "TOP 1 Begrüßung und Genehmigung des letzten Protokolls\n"
    "MN begrüßt Frau Loppinet und alle Leiterinnen und Leiter zur heutigen Sitzung. Sie bittet um Genehmigung des Protokolls der letzten Sitzung. "
    "Nach Handzeichen wird das Protokoll der Sitzung vom 15.01. ohne weitere Änderungen und Ergänzungen genehmigt.\n\n"
    "TOP 2 Stand des Projekts „Fertigungsanlage“\n"
    "LM gibt einen Überblick zum Projekt „Fertigungsanlage“. Er berichtet über den Auftrag an eine Firma aus Italien, die bereits ähnliche Anlagen hergestellt und aufgebaut hat. "
    "Die italienische Firma kommt nächsten Monat, um sich vor Ort ein Bild von unseren Werkshallen II und IV zu machen, wo die Anlage stehen soll. Der genaue Termin steht noch nicht fest. "
    "Wenn Werkshalle II oder IV als geeignet erscheint, wird unmittelbar mit der Herstellung der Fertigungsanlage in Italien begonnen. Die Montage der Anlage ist dann einige Monate später. "
    "Wie geplant soll die neue Fertigungsanlage im folgenden Frühjahr betriebsbereit sein. Sollte keine der beiden Werkshallen für den Aufbau der Fertigungsanlage groß genug sein, "
    "müssten wir zuerst eine komplett neue Werkshalle auf dem südlichen Werksgelände errichten lassen. Dadurch könnte sich die Inbetriebnahme einer neuen Fertigungsanlage um mindestens 8 bis 9 Monate verschieben.\n\n"
    "TOP 3 Berichte\n"
    "GS berichtet über die ohne große Probleme laufende Produktion der Metallkästen und Metallgehäuse, die sehr nachgefragt sind. "
    "Bei noch größerer Nachfrage nach Metallgehäusen könnte jedoch die derzeitige Fertigungsanlage nicht ausreichen. GS freut sich daher über die Planung einer neuen Fertigungsanlage. "
    "PS legt neue Verkaufszahlen vor, die im letzten Quartal 20 Prozent über dem vergleichbaren Quartal des Vorjahrs liegen. Besonders die Metallgehäuse für den Hochbau zeigen sehr gute Verkaufszahlen. "
    "PS erwähnt hier einen großen Auftrag aus Kasachstan, der für das hohe Auftragsvolumen ausschlaggebend ist.\n\n"
    "TOP 4 Neue Mitarbeiterinnen und Mitarbeiter\n"
    "MN nennt die Namen von fünf neuen Mitarbeiterinnen und Mitarbeitern, drei Frauen und zwei Männern, die ab dem 1. des Monats im Betrieb in Vollzeit tätig sind.\n\n"
    "TOP 5 Update der Software\n"
    "WL spielt am kommenden Freitag ab 19 Uhr ein Software-Update auf unser Computersystem. Daher darf am Freitag ab 19 Uhr niemand am Computer arbeiten. "
    "Die leicht überarbeitete Software hat einige Neuerungen. Allen Mitarbeiterinnen und Mitarbeitern werden diese Neuerungen in einem halbtägigen Info-Workshop demonstriert. "
    "Es wird zeitversetzte Workshops geben. Die Termine dafür werden noch bekannt gegeben.\n\n"
    "TOP 6 Sonstiges\n"
    "ML berichtet über den Stand der Planung eines Sommerfests, das etwas größer als in den vergangenen Jahren sein soll. Alle wichtigen Kunden und großen Lieferanten werden eingeladen. "
    "ML bittet alle Leiterinnen und Leiter, sich den 31. Juli freizuhalten. Der Ort steht auch schon fest. ML möchte ihn aber noch nicht nennen. "
    "Es soll eine Überraschung für alle sein, da der 31. Juli auch ihr 60. Geburtstag ist, den sie mit allen feiern möchte."
)

v_p63 = {
    "id": "t4_e-p63",
    "label": "Variante 9 (Protokoll 19.02.20XX, Ballhausen)",
    "topic": "Fertigungsanlage, Software-Update, Sommerfest",
    "page": 63,
    "note": "Acta de la reunión del 19.02.20XX en Ballhausen (pp. 63-64). En el original aparece anotada como «вариант № 9 (не с экзамена)».",
    "kind": "text",
    "intro": "Lesen Sie das Protokoll und die Aufgaben 14–18. Wählen Sie bei jeder Aufgabe die richtige Lösung a, b oder c.",
    "passage": p63_passage,
    "items": [
        {
            "n": 14,
            "type": "choice",
            "prompt": "Das Protokoll",
            "options": [
                {"key": "a", "text": "der letzten Sitzung ist nach Überarbeitung genehmigt."},
                {"key": "b", "text": "nennt die Teilnehmer der Januar-Sitzung."},
                {"key": "c", "text": "wird heute von Frau Schäfer geschrieben."}
            ],
            "answer": "c",
            "confidence": "hoch",
            "quote": "Protokollantin: Volha Schäfer",
            "explain": "Correcto c: el encabezado del documento indica expresamente que la redactora del acta actual es Volha Schäfer («Protokollantin: Volha Schäfer»). a es falso porque el acta de la sesión previa se aprobó sin enmiendas («ohne weitere Änderungen und Ergänzungen»); b es falso porque el acta lista los asistentes de la sesión presente de febrero, no los de enero."
        },
        {
            "n": 15,
            "type": "choice",
            "prompt": "Die neue Fertigungsanlage",
            "options": [
                {"key": "a", "text": "kommt in die Werkshalle IV."},
                {"key": "b", "text": "steht in einem Neubau."},
                {"key": "c", "text": "wird in Italien gebaut."}
            ],
            "answer": "c",
            "confidence": "hoch",
            "quote": "wird unmittelbar mit der Herstellung der Fertigungsanlage in Italien begonnen.",
            "explain": "Correcto c: la fabricación de la maquinaria se realiza en las instalaciones de la empresa adjudicataria en Italia («in Italien begonnen»). a es falso porque aún no se sabe si encajará en la nave II o en la IV; b es falso porque solo se construiría una nave nueva si las existentes resultaran insuficientes tras la inspección técnica."
        },
        {
            "n": 16,
            "type": "choice",
            "prompt": "Metallkästen und Metallgehäuse",
            "options": [
                {"key": "a", "text": "lassen sich nur in Deutschland verkaufen."},
                {"key": "b", "text": "sind eine Belastung für die Produktion."},
                {"key": "c", "text": "zeigen steigende Verkaufszahlen."}
            ],
            "answer": "c",
            "confidence": "hoch",
            "quote": "Besonders die Metallgehäuse für den Hochbau zeigen sehr gute Verkaufszahlen.",
            "explain": "Correcto c: las ventas trimestrales superaron en un 20 % las del año anterior y las carcasas metálicas registraron cifras excepcionales. a es falso porque destaca una gran venta internacional para Kazajistán; b es falso porque la producción discurre sin incidentes y con alta demanda."
        },
        {
            "n": 17,
            "type": "choice",
            "prompt": "Das Update der Software",
            "options": [
                {"key": "a", "text": "erfordert ein neues Computersystem."},
                {"key": "b", "text": "schließt einen eintägigen Workshop mit ein."},
                {"key": "c", "text": "wird am Freitag installiert."}
            ],
            "answer": "c",
            "confidence": "hoch",
            "quote": "WL spielt am kommenden Freitag ab 19 Uhr ein Software-Update auf unser Computersystem.",
            "explain": "Correcto c: la responsable de TI cargará la actualización el próximo viernes a partir de las 19:00 horas («am kommenden Freitag ab 19 Uhr ein Software-Update»). a es falso porque se actualiza el sistema existente; b es falso porque los talleres de formación para el personal son de media jornada («in einem halbtägigen Info-Workshop»), no de un día entero."
        },
        {
            "n": 18,
            "type": "choice",
            "prompt": "Die Geschäftsführerin",
            "options": [
                {"key": "a", "text": "berichtet über Ort und Termin eines Sommerfests."},
                {"key": "b", "text": "erwartet eine genaue Planung des Sommerfests."},
                {"key": "c", "text": "möchte zum Sommerfest Kunden und Lieferanten einladen."}
            ],
            "answer": "c",
            "confidence": "hoch",
            "quote": "Alle wichtigen Kunden und großen Lieferanten werden eingeladen.",
            "explain": "Correcto c: la directora general (Maria Loppinet) informa de que se cursará invitación a los clientes y proveedores más relevantes para la fiesta de verano. a es falso porque mantiene en secreto el lugar de celebración como sorpresa de su 60 cumpleaños; b no se ajusta a lo tratado en la reunión."
        }
    ]
}

out_data = {
    "block": "t4_e",
    "section": "lesen-t4",
    "variants": [v_p59, v_p61, v_p63]
}

# Validación previa
for v in out_data["variants"]:
    np_ = norm(v["passage"])
    for it in v["items"]:
        keys = [o["key"] for o in it["options"]]
        assert it["answer"] in keys
        assert norm(it["quote"]) in np_, f"Quote not in passage for {v['id']} item {it['n']}: {it['quote']}"

with open(r"quiz\data\t4_e.json", "w", encoding="utf-8") as f:
    json.dump(out_data, f, ensure_ascii=False, indent=1)

print("t4_e.json generado y validado con éxito!")
