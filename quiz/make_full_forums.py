# -*- coding: utf-8 -*-
"""
make_full_forums.py - Generador del catálogo exhaustivo de Forumsbeiträge (telc B2 Beruf).
Extrae y estructura todos los temas de debate de examen real presentes en las pp. 98–106 de B2_ohne_antworten.md.
"""

import json
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

STANDARD_REDEMITTEL = [
    "Ich möchte mich an der aktuellen Diskussion zum Thema «...» beteiligen.",
    "In unserem Unternehmen wird zurzeit viel über die Frage diskutiert, ob...",
    "Meiner Ansicht / Meinung nach ist diese Maßnahme ein wichtiger Schritt, weil...",
    "Einerseits bietet dieses Modell entscheidende Vorteile, wie zum Beispiel...",
    "Andererseits darf man jedoch nicht übersehen, dass damit auch Nachteile verbunden sind, etwa...",
    "Ein weiterer Aspekt, der unbedingt bedacht werden sollte, ist...",
    "Aus meiner persönlichen Erfahrung kann ich berichten, dass...",
    "In meinem Heimatland / an meinem früheren Arbeitsplatz war es üblich, dass...",
    "Um eine für alle Beteiligten faire Lösung zu finden, schlage ich vor, dass...",
    "Ein sinnvoller Kompromiss könnte meiner Meinung nach darin bestehen, dass...",
    "Zusammenfassend lässt sich sagen, dass eine ausgewogene Regelung im Sinne aller Kollegen wäre.",
    "Ich bin gespannt auf die Meinungen und Argumente der anderen Kolleginnen und Kollegen."
]

def make_forum(fid, num, title, topic, page, scenario, lp1, lp2, lp3, lp4):
    """Un tema de Forumsbeitrag. Sin `colleague_post`: la aportación del compañero
    era invención nuestra y el libro no la trae (la app oculta ese bloque)."""
    return {
        "id": fid,
        "category": "forum",
        "kind": "schreiben",
        "label": f"Forumsbeitrag {num}: {title}",
        "topic": topic,
        "page": page,
        "num": num,
        "scenario": scenario,
        "prompt": "Schreiben Sie einen Beitrag für das Diskussionsforum Ihrer Firma. Behandeln Sie dabei die folgenden vier Punkte:",
        "leitpunkte": [
            lp1,
            lp2,
            lp3,
            lp4
        ],
        "min_words": 150,
        "time_minutes": 45,
        "redemittel": STANDARD_REDEMITTEL
    }

# Definición de los temas de examen recopilados de las pp. 98–106
RAW_TOPICS = [
    # --- PÁGINA 98 ---
    (
        "schr-f-01-aufgaben", 1, "Zusätzliche Aufgaben ohne Neueinstellungen", "Zusätzliche Aufgaben / Arbeitsbelastung", 98,
        "Alle Mitarbeiterinnen und Mitarbeiter in Ihrer Firma müssen mehr Aufgaben übernehmen, da keine neuen Mitarbeitenden eingestellt werden können.",
        "Äußern Sie Ihre Meinung zu der Übernahme zusätzlicher Aufgaben.",
        "Nennen Sie Vor- und Nachteile einer solchen vorübergehenden Mehrarbeit.",
        "Berichten Sie von Erfahrungen mit hoher Arbeitsbelastung an früheren Arbeitsplätzen.",
        "Schlagen Sie eine faire Lösung oder Entlastungsmaßnahmen für das Team vor."
    ),
    (
        "schr-f-02-krankmeldung", 2, "Ärztliche Krankmeldung ab dem 1. Tag", "Krankmeldung ab Tag 1", 98,
        "Alle Mitarbeiterinnen und Mitarbeiter in Ihrer Firma sollen im Krankheitsfall schon ab dem ersten Tag eine ärztliche Krankmeldung vorlegen. Andernfalls gelten die Tage als Fehlzeit.",
        "Äußern Sie Ihre Meinung zu der Verpflichtung eines Attests ab dem ersten Tag.",
        "Erläutern Sie Vor- und Nachteile dieser Neuregelung für Betrieb und Belegschaft.",
        "Beschreiben Sie, wie Krankmeldungen in Ihrem Heimatland oder früheren Betrieben gehandhabt werden.",
        "Machen Sie einen konstruktiven Vorschlag für eine praxistaugliche Regelung im Unternehmen."
    ),
    (
        "schr-f-03-jobticket-gehalt", 3, "Jobticket gegen Gehaltsverzicht", "Jobticket & Mobilität", 98,
        "An dem kommenden Jahr sollen alle Mitarbeiterinnen und Mitarbeiter auf ihr Gehalt verzichten. Dafür bekommen alle ein kostenloses Jobticket.",
        "Äußern Sie Ihre Ansicht zu dem Angebot des Jobtickets mit Gehaltsabzug.",
        "Nennen Sie je zwei Vor- und Nachteile des Modells für verschiedene Mitarbeitergruppen.",
        "Erzählen Sie von Ihren eigenen täglichen Wegen zur Arbeit und Mobilitätserfahrungen.",
        "Formulieren Sie einen Vorschlag für ein freiwilliges und faires Ticketmodell."
    ),
    (
        "schr-f-04-zeitmanagement", 4, "Verpflichtender Workshop zum Zeitmanagement", "Weiterbildung & Arbeitsabläufe", 98,
        "Alle Mitarbeiterinnen und Mitarbeiter in Ihrer Firma sollen an einem Workshop zum Zeitmanagement teilnehmen, um Ihre Arbeitsabläufe effizienter gestalten zu können.",
        "Äußern Sie Ihre Meinung zu der Verpflichtung für alle Mitarbeiter.",
        "Nennen Sie Vor- und Nachteile von internen Zeitmanagement-Schulungen.",
        "Berichten Sie, wie Sie Ihren Arbeitsalltag organisieren und Prioritäten setzen.",
        "Schlagen Sie alternative Methoden vor, um Arbeitsabläufe im Betrieb zu optimieren."
    ),
    (
        "schr-f-07-privathandys", 5, "Aufbewahrung von Privathandys im Spind", "Smartphone-Nutzung am Arbeitsplatz", 98,
        "Alle Mitarbeiterinnen und Mitarbeiter in Ihrer Firma sollen ihre Mobiltelefone während der Arbeitszeit im Aufenthaltsraum aufbewahren. Privattelefone sind nur in den Pausen gestattet. Nur die leitenden Angestellten dürfen das.",
        "Äußern Sie Ihre Haltung zu dem Handyverbot am Arbeitsplatz.",
        "Nennen Sie Vor- und Nachteile dieser Maßnahme für Betriebsklima und Produktivität.",
        "Erzählen Sie, wie mit privaten Handys an früheren Arbeitsplätzen umgegangen wurde.",
        "Geben Sie eine konkrete Empfehlung für klare und verhältnismäßige Nutzungsregeln."
    ),
    (
        "schr-f-05-urlaubsplanung-kinder", 6, "Urlaubsplanung in den Sommerferien", "Urlaubsgerechtigkeit", 98,
        "Alle Mitarbeitenden in Ihrer Firma sollen ihren Urlaub planen. In den Sommerferien sollen nur Mitarbeiter mit schulpflichtigen Kindern Urlaub bekommen. Mitarbeiter ohne Kinder müssen zu anderen Zeiten Urlaub machen.",
        "Nehmen Sie Stellung zu der Bevorzugung von Eltern bei der Sommerurlaubsplanung.",
        "Wägen Sie Vor- und Nachteile für die verschiedenen Interessengruppen im Betrieb ab.",
        "Berichten Sie von Ihren Erfahrungen mit Urlaubsabsprachen in Teams.",
        "Unterbreiten Sie einen Kompromissvorschlag für eine gerechte Urlaubsverteilung."
    ),
    (
        "schr-f-06-ueberstunden-stopp", 7, "Automatischer System-Logout gegen Überstunden", "Überstundenverbot / Work-Life-Balance", 98,
        "Alle Mitarbeiterinnen und Mitarbeiter in Ihrer Firma sollen keine Überstunden mehr leisten. Zur Durchsetzung dieser Maßnahme wird man nach acht Arbeitsstunden automatisch aus dem Computer-System abgemeldet.",
        "Äußern Sie Ihre Meinung zur automatischen Rechnersperre nach 8 Stunden.",
        "Diskutieren Sie Vor- und Nachteile einer strikten Begrenzung der Arbeitszeit.",
        "Schildern Sie Ihre persönlichen Erfahrungen mit Überstunden und Arbeitszeitregelungen.",
        "Schlagen Sie flexible Lösungen für den Umgang mit Mehrarbeit und Pausen vor."
    ),
    (
        "schr-f-ueberstunden-gehalt", 8, "Überstunden sind mit dem Gehalt abgegolten", "Überstunden & Vergütung", 98,
        "Alle Mitarbeiterinnen und Mitarbeiter sollen bereit sein, Überstunden zu leisten. Diese werden nicht extra bezahlt, sondern sind mit dem übertariflichen Gehalt ausgeglichen.",
        "Äußern Sie Ihre Meinung zur Abgeltung von Überstunden mit dem Gehalt.",
        "Nennen Sie Vor- und Nachteile dieser Regelung für Betrieb und Beschäftigte.",
        "Berichten Sie, wie Überstunden in einem früheren Betrieb oder in Ihrem Heimatland geregelt waren.",
        "Schlagen Sie ein faires Modell für Überstunden vor (Ausgleich, Zuschlag, Obergrenze)."
    ),
    # --- PÁGINA 99 ---
    (
        "schr-f-08-weiterbildung-wochenende", 9, "Weiterbildung am Wochenende (50 € Prämie)", "Betriebliche Fortbildung", 99,
        "Weiterbildung zweimal pro Jahr am Wochenende, außerhalb der Arbeitszeiten.",
        "Äußern Sie Ihre Ansicht zu Fortbildungen am Wochenende mit Bonuszahlung.",
        "Nennen Sie Vor- und Nachteile von Schulungen in der Freizeit.",
        "Berichten Sie von eigenen Erfahrungen mit Weiterbildungsangeboten.",
        "Schlagen Sie alternative Modelle (z. B. Bildungsurlaub oder Hybridseminare) vor."
    ),
    (
        "schr-f-jobticket-parkgebuehr", 10, "Kostenloses Jobticket, dafür Parken kostenpflichtig", "Mobilität & Parkraumbewirtschaftung", 99,
        "Ihre Firma möchte für alle Mitarbeitenden ein kostenloses Jobticket für die Fahrten mit dem ÖPNV einführen. Dafür soll Parken auf dem Firmenparkplatz in Zukunft Geld kosten.",
        "Äußern Sie Ihre Meinung zum Jobticket und zur Gegenfinanzierung durch Parkgebühren.",
        "Nennen Sie Vor- und Nachteile für Autofahrer, ÖPNV-Nutzende und den Betrieb.",
        "Schildern Sie Ihre eigenen Wege zur Arbeit und Ihre Erfahrungen damit.",
        "Schlagen Sie einen Kompromiss vor (gestaffelte Gebühren, Ausnahmen, Alternativen)."
    ),
    (
        "schr-f-09-firmenumzug", 11, "Firmenumzug an einen neuen Standort", "Standortverlegung / Pendeln", 99,
        "Alle Mitarbeiterinnen und Mitarbeiter in Ihrer Firma müssen umziehen, weil das Unternehmen in eine andere Stadt zieht; die Kosten für den Umzug werden erstattet.",
        "Nehmen Sie Stellung zu den Plänen der Standortverlegung.",
        "Wägen Sie Vor- und Nachteile eines solchen Firmenumzugs ab.",
        "Beschreiben Sie Ihre eigenen Prioritäten bezüglich Arbeitsort und Pendelzeit.",
        "Machen Sie Vorschläge, wie das Unternehmen die betroffenen Mitarbeiter unterstützen kann."
    ),
    (
        "schr-f-10-parkplatz-kunden", 12, "Firmenparkplatz nur noch für Kunden", "Parkplatzordnung", 99,
        "Alle Mitarbeiterinnen und Mitarbeiter in Ihrer Firma dürfen nicht mehr ihre Autos auf dem Firmengelände parken. Das Parken ist jetzt nur noch für Kunden. Das Unternehmen übernimmt die Kosten nur noch den öffentlichen Nahverkehr.",
        "Äußern Sie Ihre Meinung zum Wegfall der Mitarbeiterparkplätze.",
        "Nennen Sie Vor- und Nachteile der Maßnahme aus Sicht von Kunden und Personal.",
        "Erzählen Sie, wie die Parkplatzsituation an Ihren früheren Arbeitsorten geregelt war.",
        "Schlagen Sie ein faires Konzept vor (z. B. Parkplatz-Sharing oder Fahrgemeinschaften)."
    ),
    (
        "schr-f-11-soziale-netzwerke", 13, "Soziale Netzwerke zur internen Kommunikation", "Social Media am Arbeitsplatz", 99,
        "(Die Nutzung sozialer Netzwerke zur Kommunikation am Arbeitsplatz.)",
        "Äußern Sie Ihre Meinung zur dienstlichen Nutzung privater sozialer Netzwerke.",
        "Nennen Sie Vor- und Nachteile von Messenger-Gruppen für die Zusammenarbeit.",
        "Berichten Sie von Ihren Erfahrungen mit digitaler Kommunikation im Team.",
        "Schlagen Sie sichere und datenschutzkonforme Alternativen für das Unternehmen vor."
    ),
    (
        "schr-f-12-fitnessstudio", 14, "Fitnessraum im Betrieb gegen Monatsgebühr", "Betriebliche Gesundheitsförderung", 99,
        "Alle Mitarbeiterinnen und Mitarbeiter sollen die Möglichkeit haben, die neue Fitnessstudio-Einrichtung am Arbeitsplatz während der Pausen zu nutzen. Dafür wird eine Gebühr von 15 Euro pro Monat direkt vom Gehalt abgezogen.",
        "Nehmen Sie Stellung zur Einrichtung eines firmeninternen Fitnessraums.",
        "Diskutieren Sie Vor- und Nachteile des Angebots und der Kostenbeteiligung.",
        "Schildern Sie eigene Erfahrungen mit sportlichen Angeboten im Beruf.",
        "Formulieren Sie einen Vorschlag für die Gestaltung und Finanzierung des Angebots."
    ),
    (
        "schr-f-13-erreichbarkeit", 15, "Betriebliche Erreichbarkeit nach Feierabend", "Erreichbarkeit / Work-Life-Balance", 99,
        "Wegen eines großen Betriebsauftrags müssen alle Mitarbeitenden am Wochenende / unter der Woche telefonisch erreichbar sein. Dann bekommen sie noch 2 extra Urlaubstage.",
        "Äußern Sie Ihre Haltung zur Erreichbarkeitspflicht außerhalb der Arbeitszeiten.",
        "Erläutern Sie die Vor- und Nachteile für das Projekt und das Wohlbefinden der Mitarbeiter.",
        "Berichten Sie von Ihren persönlichen Grenzen zwischen Freizeit und Beruf.",
        "Schlagen Sie eine geregelte Bereitschaftsregelung mit fairem Zeitausgleich vor."
    ),
    (
        "schr-f-fruehstueckspause", 16, "Keine Frühstückspause, dafür eine Stunde Mittagspause", "Pausenregelung", 99,
        "Nicht mehr 15 Minuten Frühstückspause, sondern verlängert sich die Mittagspause vom 45 Minuten zu einer Stunde in einem Stück.",
        "Äußern Sie Ihre Meinung zur Streichung der Frühstückspause.",
        "Erläutern Sie die Auswirkungen auf Konzentration, Gesundheit und Arbeitsabläufe.",
        "Schildern Sie Ihre eigene Pausenroutine während des Arbeitstages.",
        "Machen Sie einen Vorschlag für eine flexible Pausenregelung."
    ),
    (
        "schr-f-14-vegan-kantine", 17, "Rein vegane Kantine mit 20 % Preisaufschlag", "Ernährung & Kantine", 99,
        "Alle Mitarbeitenden in Ihrer Firma sollen in der Kantine nur noch zwischen fleischlosen Gerichten wählen können. Alles soll Bioqualität haben und dafür etwas mehr kosten.",
        "Äußern Sie Ihre Meinung zur vollständigen Umstellung auf vegane Bio-Kost.",
        "Wägen Sie Vor- und Nachteile bezüglich Gesundheit, Kosten und Akzeptanz ab.",
        "Berichten Sie, wie Verpflegung an anderen Arbeitsplätzen organisiert ist.",
        "Schlagen Sie ein ausgewogenes Kantinenkonzept mit Wahlmöglichkeiten vor."
    ),
    # --- PÁGINA 100 ---
    (
        "schr-f-firmenumzug-urlaubstage", 18, "Firmenumzug mit fünf zusätzlichen Urlaubstagen", "Standortwechsel & Ausgleich", 100,
        "Alle Mitarbeiterinnen und Mitarbeiter müssen an einen anderen Standort ziehen. Die Firma unterstützt Sie dabei und gewährt einen zusätzlichen Urlaubstag sowie fünf weitere Urlaubstage.",
        "Äußern Sie Ihre Meinung zum Umzug und zum angebotenen Ausgleich.",
        "Wägen Sie Vor- und Nachteile des neuen Standorts für Pendelzeit und Alltag ab.",
        "Berichten Sie von Ihren eigenen Erfahrungen mit langen Arbeitswegen.",
        "Schlagen Sie weitere Ausgleichsmaßnahmen vor (Homeoffice, Fahrtkostenzuschuss, Gleitzeit)."
    ),
    (
        "schr-f-fitnessstudio-35", 19, "Fitnessstudio-Mitgliedschaft gegen 35 Euro Gehaltsabzug", "Betriebliche Gesundheitsförderung", 100,
        "Alle Mitarbeiterinnen und Mitarbeiter sollen 35 Euro weniger Gehalt bekommen. Dafür bezahlt die Firma die Mitgliedschaft im Fitnessstudio.",
        "Äußern Sie Ihre Meinung zur Mitgliedschaft mit Gehaltsabzug.",
        "Nennen Sie Vor- und Nachteile für Gesundheit und Motivation der Belegschaft.",
        "Berichten Sie von Ihren eigenen Sport- und Gesundheitsgewohnheiten.",
        "Schlagen Sie Alternativen vor (freiwillige Teilnahme, Zuschuss, andere Angebote)."
    ),
    (
        "schr-f-15-wochenendreise", 20, "Wochenendreise statt Weihnachtsfeier", "Teamevents & Feiern", 100,
        "Alle Mitarbeiterinnen und Mitarbeiter in Ihrer Firma sollen zukünftig auf die Weihnachtsfeier verzichten. Stattdessen lädt das Unternehmen sie mit ihren Familien zu einer gemeinsamen Wochenendreise ein.",
        "Nehmen Sie Stellung zu der geplanten Wochenendreise anstelle der Weihnachtsfeier.",
        "Nennen Sie Vor- und Nachteile einer solchen gemeinsamen Reise mit Familien.",
        "Berichten Sie von gelungenen Betriebsfeiern und Teamevents aus Ihrer Erfahrung.",
        "Machen Sie einen konkreten Vorschlag für das diesjährige Jahresabschluss-Event."
    ),
    (
        "schr-f-16-grossraumbuero", 21, "Umzug in ein offenes Großraumbüro", "Bürokonzepte / Open Space", 100,
        "Alle Mitarbeitenden in Ihrer Firma sollen zukünftig gemeinsam in einem Großraumbüro arbeiten. Einzelbüro wird es nicht mehr geben.",
        "Äußern Sie Ihre Meinung zum Konzept des Großraumbüros.",
        "Diskutieren Sie Vor- und Nachteile von Open-Space-Büros für die Arbeitsleistung.",
        "Beschreiben Sie Ihre ideale Arbeitsumgebung für konzentriertes Arbeiten.",
        "Schlagen Sie ein durchdachtes Raumkonzept (z. B. Ruhezonen, Meeting-Pods) vor."
    ),
    (
        "schr-f-17-mitarbeiter-des-jahres", 22, "Wahl zum «Mitarbeiter des Jahres» mit Prämie", "Mitarbeiteranerkennung", 100,
        "Die Firma plant, jedes Jahr einen \"Mitarbeiter*in des Jahres\" zu wählen. Der oder die Gewinner*in erhält eine finanzielle Belohnung.",
        "Äußern Sie Ihre Ansicht zur Einführung einer solchen Auszeichnung.",
        "Nennen Sie Vor- und Nachteile von individuellen Leistungsanreizen im Betrieb.",
        "Berichten Sie von Belohnungssystemen und Motivation an früheren Arbeitsstellen.",
        "Schlagen Sie alternative Modelle zur Teamanerkennung und Wertschätzung vor."
    ),
    (
        "schr-f-18-spanischkurs", 23, "Verpflichtender Spanischkurs nach Feierabend", "Sprachförderung & Internationalisierung", 100,
        "Alle Mitarbeiterinnen und Mitarbeiter in Ihrer Firma sollen verpflichtet werden, einen Spanischkurs zu besuchen, weil das Unternehmen einen neuen Standort in Spanien eröffnet. Die Kursgebühren übernimmt die Firma.",
        "Nehmen Sie Stellung zu dem verpflichtenden Sprachkurs nach Arbeitsende.",
        "Wägen Sie Vor- und Nachteile für die persönliche und berufliche Entwicklung ab.",
        "Erzählen Sie von Ihren Erfahrungen beim Erlernen von Fremdsprachen für den Beruf.",
        "Unterbreiten Sie einen Vorschlag für flexible Lernzeiten oder Online-Module."
    ),
    (
        "schr-f-19-auslandsdienst", 24, "6-monatiger Auslandsdienst zur Einarbeitung", "Auslandseinsatz / Mobilität", 100,
        "Alle Mitarbeiter in ihrer Firma sollen einen/eine Kolleg*in aus ihrer Abteilung auswählen, der/die für 6 Monaten nach Italien geht, um dort am Firmenstandort neue Kollegen*innen einzuarbeiten.",
        "Äußern Sie Ihre Haltung zu der sechsmonatigen Entsendung von Mitarbeitern.",
        "Nennen Sie Vor- und Nachteile eines solchen Auslandseinsatzes.",
        "Berichten Sie von Ihren Erfahrungen mit interkultureller Arbeit und Auslandsaufenthalten.",
        "Schlagen Sie Kriterien für eine faire und freiwillige Auswahl der Entsendeten vor."
    ),
    (
        "schr-f-leiharbeit-stellen", 25, "Freie Stellen nur noch mit Leiharbeitenden besetzen", "Personalpolitik & Leiharbeit", 100,
        "Alle Mitarbeiter in der Firma sollen zukünftig keine neuen festangestellten Kolleg*innen mehr bekommen. Bei Bedarf werden offene Stellen ausschließlich mit Leiharbeiter*innen besetzen.",
        "Äußern Sie Ihre Meinung zur Besetzung aller Stellen mit Leiharbeitenden.",
        "Nennen Sie Vor- und Nachteile für Team, Einarbeitung und Kosten.",
        "Berichten Sie von Ihren Erfahrungen mit Leiharbeit oder befristeten Stellen.",
        "Machen Sie Vorschläge für eine tragfähige Personalplanung."
    ),
    (
        "schr-f-20-firmenkita-247", 26, "24/7 Firmen-Kita für Schichtarbeiter", "Betriebliche Kinderbetreuung", 100,
        "Alle Mitarbeiterinnen und Mitarbeiter in Schichtarbeit haben jetzt die Möglichkeit, die Firmen-Kita flexibel zu nutzen. Die Öffnungszeiten sind auf eine 24h Betreuung ausgeweitet worden.",
        "Äußern Sie Ihre Meinung zur Einrichtung einer 24h-Betriebskita.",
        "Diskutieren Sie Vor- und Nachteile flexibler Betreuungsangebote für Eltern und Betrieb.",
        "Schildern Sie die Vereinbarkeit von Beruf und Familie aus Ihrer eigenen Erfahrung.",
        "Machen Sie Vorschläge für die konkrete Umsetzung und pädagogische Gestaltung."
    ),
    (
        "schr-f-mittagessen-samstag", 27, "Kostenfreies Mittagessen für Samstagsarbeit", "Benefits & Wochenendarbeit", 100,
        "Alle Mitarbeiterinnen und Mitarbeiter in Ihrer Firma, die samstags arbeiten müssen, erhalten an diesem Tag zukünftig ein kostenfreies Mittagessen in der Firmenkantine.",
        "Äußern Sie Ihre Meinung zum Gratisessen als Ausgleich für Samstagsarbeit.",
        "Erörtern Sie Vor- und Nachteile dieser Regelung und mögliche Ungleichbehandlung.",
        "Berichten Sie von Ihren eigenen Erfahrungen mit Wochenendarbeit.",
        "Schlagen Sie gerechtere Alternativen vor."
    ),
    (
        "schr-f-21-kantinenschliessung", 28, "Schließung der Kantine und Essensmarken", "Verpflegung & Betriebsklima", 100,
        "Alle Mitarbeiterinnen und Mitarbeiter in Ihren Firma sollen zukünftig nicht mehr in der Kantine essen können. Diese wird geschlossen. Stattdessen werden Essenmarken für verschiedene Restaurants in der Nähe ausgegeben.",
        "Nehmen Sie Stellung zur Schließung der Firmenkantine zugunsten von Essensmarken.",
        "Nennen Sie Vor- und Nachteile von Essensgutscheinen im Vergleich zu einer Kantine vor Ort.",
        "Berichten Sie von der Mittagspausenkultur an Ihren bisherigen Arbeitsplätzen.",
        "Schlagen Sie Alternativen vor, um Verpflegung und sozialen Zusammenhalt zu sichern."
    ),
    (
        "schr-f-heizen-oktober", 29, "Sparpläne: Heizen erst ab Oktober und maximal 19 Grad", "Energiesparen im Betrieb", 100,
        "Alle Mitarbeiterinnen und Mitarbeiter in Ihren Firma sollen zukünftig ihre Büros erst ab Oktober heizen und die Raumtemperatur auf maximal 19°C begrenzen. Das Unternehmen möchte damit die Energiekosten reduzieren.",
        "Äußern Sie Ihre Meinung zum späteren Heizbeginn und zur Temperaturgrenze.",
        "Wägen Sie Vor- und Nachteile für Gesundheit, Konzentration und Kosten ab.",
        "Berichten Sie von Ihren Erfahrungen mit kalten Büroräumen.",
        "Schlagen Sie praktikable Kompromisse vor."
    ),
    # --- PÁGINA 101 ---
    (
        "schr-f-22-urlaubstage-jahresende", 30, "Urlaubsverfall: Alle Tage bis Jahresende nehmen", "Urlaubsregelung", 101,
        "Alle Mitarbeitenden müssen die verbleibenden Urlaubstage bis zum Ende eines jeden Jahres verbraucht werden, sonst verfallen sie.",
        "Äußern Sie Ihre Ansicht zur strikten Frist für den Urlaub bis Jahresende.",
        "Erläutern Sie die Vor- und Nachteile für die Personalplanung und die Mitarbeiter.",
        "Berichten Sie, wie Urlaubsübertragungen in Ihrem Heimatland geregelt sind.",
        "Schlagen Sie eine flexiblere Übergangsfrist für Resturlaub vor."
    ),
    (
        "schr-f-23-byod-verbot", 31, "Verbot privater Geräte am Arbeitsplatz (BYOD-Verbot)", "IT-Sicherheit / Datenschutz", 101,
        "In eurer Firma wurde es verboten , private Geräte jeglicher Art zu benutzen oder sie über die Steckdosen der Firma aufzuladen. Es dürfen nur firmeneigene elektronische Geräte verwendet werden.",
        "Äußern Sie Ihre Meinung zum Verbot privater Hardware im Unternehmen.",
        "Wägen Sie Sicherheitsaspekte gegen Arbeitsflexibilität und Komfort ab.",
        "Erzählen Sie von Ihren Erfahrungen mit Datenschutz und Sicherheitsregeln im Betrieb.",
        "Unterbreiten Sie einen Vorschlag für einen sicheren und modernen Mittelweg."
    ),
    (
        "schr-f-mitarbeiterbindung-urlaubstag", 32, "Mitarbeiterbindung: alle fünf Jahre ein Urlaubstag mehr", "Mitarbeiterbindung & Benefits", 101,
        "Um die Mitarbeiterbindung zu stärken, möchte unsere Firma in Zukunft den Mitarbeiterinnen und Mitarbeitern alle 5 Jahre den Urlaub um einen Tag verlängern.",
        "Äußern Sie Ihre Meinung zur Maßnahme als Mittel der Mitarbeiterbindung.",
        "Nennen Sie wirksamere Vor- und Nachteile beziehungsweise Alternativen.",
        "Berichten Sie, was Sie persönlich an einen Arbeitgeber bindet.",
        "Machen Sie konkrete Vorschläge für ein attraktiveres Modell."
    ),
    (
        "schr-f-urlaubstage-statt-bonus", 33, "Zusätzliche Urlaubstage statt Bonuszahlungen", "Leistungsanreize & Vergütung", 101,
        "Alle Mitarbeiterinnen und Mitarbeiter in Ihrer Firma sollen für besonders gute Arbeitsleistungen nicht mehr wie bisher Bonuszahlungen erhalten. Stattdessen bekommen sie zusätzliche Urlaubstage.",
        "Äußern Sie Ihre Meinung zu Urlaubstagen als Prämie.",
        "Wägen Sie Vor- und Nachteile gegenüber Bonuszahlungen ab.",
        "Berichten Sie von Ihren Erfahrungen mit Prämien und Anerkennung im Beruf.",
        "Schlagen Sie ein flexibles Prämiensystem vor."
    ),
    (
        "schr-f-sozialer-tag", 34, "Soziales Engagement statt Betriebsausflug", "Soziales Engagement", 101,
        "Alle Mitarbeiterinnen und Mitarbeiter in Ihrer Firma sollen sich anstelle eines Betriebsausflugs dieses Jahr an einem sozialen Tag gemeinsam ehrenamtlich engagieren. Auch dieser Tag zählt als Arbeitszeit.",
        "Äußern Sie Ihre Meinung zum ehrenamtlichen Tag als Ersatz für den Betriebsausflug.",
        "Nennen Sie Vor- und Nachteile für Team, Motivation und Außenwirkung.",
        "Berichten Sie von Ihren eigenen Erfahrungen mit ehrenamtlicher Arbeit.",
        "Machen Sie einen Vorschlag, wie sich beides sinnvoll verbinden lässt."
    ),
    (
        "schr-f-25-erste-hilfe", 35, "Verpflichtende Erste-Hilfe-Kurse für alle", "Arbeitssicherheit & Gesundheit", 101,
        "Alle Mitarbeiterinnen und Mitarbeiter in Ihrer Firma sollen verpflichtet Erste-Hilfe- Kurse machen, die vom Unternehmen finanziert werden. Dafür gibt es Freizeitausgleich.",
        "Äußern Sie Ihre Haltung zur Erste-Hilfe-Schulung für die gesamte Belegschaft.",
        "Diskutieren Sie den Nutzen für die Sicherheit im Betrieb gegen den zeitlichen Aufwand.",
        "Schildern Sie eigene Erfahrungen mit Notfallsituationen oder Schulungen.",
        "Geben Sie Empfehlungen für eine effiziente und praxisnahe Durchführung der Kurse."
    ),
    (
        "schr-f-kommunikationstraining-wochenende", 36, "Kommunikationstraining am Wochenende", "Teamentwicklung & Arbeitsbelastung", 101,
        "Die Geschäftsleitung möchte, dass die Mitarbeitenden am Wochenende an einem verpflichtenden Kommunikationstraining teilnehmen. Aufgrund der derzeit hohen Arbeitsbelastung wird der Kurs am Wochenenden durchgeführt.",
        "Äußern Sie Ihre Meinung zum Wochenendtermin für die Schulung.",
        "Wägen Sie Vor- und Nachteile von Fortbildungen außerhalb der Arbeitszeit ab.",
        "Berichten Sie von Ihren Erfahrungen mit Schulungen am Wochenende.",
        "Schlagen Sie eine bessere Lösung vor (Freizeitausgleich, Arbeitszeit, Online-Format)."
    ),
    (
        "schr-f-26-firmenhandy-bereitschaft", 37, "Diensthandy mit Bereitschaftspflicht", "Diensthandy & Freizeit", 101,
        "Alle Mitarbeiterinnen und Mitarbeiter in ihrer Firma sollen ein Firmenhandy bekommen. Dafür müssen sie bereit sein 24 Stunden auf Nachrichten zu reagieren.",
        "Äußern Sie Ihre Meinung zur Koppelung von Firmenhandy und Wochenendbereitschaft.",
        "Nennen Sie Vor- und Nachteile von Diensthandys für Arbeitnehmer.",
        "Berichten Sie von Ihrem persönlichen Umgang mit dienstlicher Erreichbarkeit.",
        "Schlagen Sie klare Abschaltzeiten und geregelte Vertretungspläne vor."
    ),
    (
        "schr-f-wochenende-feiertage", 38, "Arbeit am Wochenende und an Feiertagen", "Arbeitszeit & Ausgleich", 101,
        "Alle Mitarbeiterinnen und Mitarbeiter Ihrer Firma sollen am Wochenende und an Feiertagen arbeiten. Zusätzlich bekommen sie vier Urlaubstagen.",
        "Äußern Sie Ihre Meinung zur Ausweitung der Arbeitszeit auf Wochenenden und Feiertage.",
        "Wägen Sie Vor- und Nachteile ab und bewerten Sie den angebotenen Ausgleich.",
        "Berichten Sie von Ihren Erfahrungen mit Wochenend- oder Feiertagsarbeit.",
        "Schlagen Sie faire Regeln vor (Freiwilligkeit, Zuschläge, Planbarkeit)."
    ),
    (
        "schr-f-urlaubsplanung-oktober", 39, "Urlaubsplanung für das ganze Jahr bis Oktober", "Urlaubsplanung & Fristen", 101,
        "Alle Mitarbeiterinnen und Mitarbeiter in ihrer Firma sollen schon im Oktober ihre Urlaubsplanung für das nächste Jahr eintragen. Urlaubsanträge, die später eingereicht werden, können eventuell nicht mehr berücksichtig werden.",
        "Äußern Sie Ihre Meinung zur frühen Planungsfrist.",
        "Wägen Sie Vor- und Nachteile für Betriebsablauf und Privatleben ab.",
        "Berichten Sie von Ihren Erfahrungen mit der Urlaubsplanung im Betrieb.",
        "Schlagen Sie ein faires und flexibles Verfahren vor."
    ),
    (
        "schr-f-27-dienstkleidung", 40, "Verpflichtende Dienstkleidung in Firmenfarben", "Corporate Identity / Dresscode", 101,
        "Alle Mitarbeitenden in Ihrer Firma sollen während Arbeitszeit Hemden/Blusen in roten/weißen Farben tragen. Sie sollen aber neue Kleidung selbst kaufen und Firma übernimmt keine Kosten.",
        "Nehmen Sie Stellung zu der Pflicht von Dienstkleidung in Firmenfarben.",
        "Wägen Sie Einheitlichkeit und Markenauftritt gegen persönliche Freiheit ab.",
        "Berichten Sie von Kleidungsvorschriften an früheren Arbeitsstellen.",
        "Formulieren Sie einen Kompromiss (z. B. nur bei direktem Kundenkontakt)."
    ),
    (
        "schr-f-homeoffice-ein-tag", 41, "Nur noch ein Tag Homeoffice pro Woche", "Homeoffice & Präsenzpflicht", 101,
        "Ab nächsten Monat wird das Homeoffice vollständig abgeschaft. Alle Mitarbeiterinnen und Mitarbeiter der Firma sollen künftig an vier Tagen pro Woche im Büro arbeiten. Die Arbeit von zu Hause ist nur noch an einem Tag möglich.",
        "Äußern Sie Ihre Meinung zur Reduzierung auf einen Homeoffice-Tag.",
        "Wägen Sie Vor- und Nachteile für Zusammenarbeit, Arbeitswege und Vereinbarkeit ab.",
        "Berichten Sie von Ihren eigenen Erfahrungen mit mobilem Arbeiten.",
        "Schlagen Sie ein ausgewogenes Modell vor."
    ),
    # --- PÁGINA 102 ---
    (
        "schr-f-weiterbildung-kommunizieren", 42, "Kostenfreie Weiterbildung «Erfolgreich kommunizieren»", "Weiterbildung & Kommunikation", 102,
        "Alle Mitarbeiterinnen und Mitarbeiter in Ihrer Firma sollen an der kostenfreien Weiterbildung “Erfolgreich mit den Kunden kommunizieren” 2 Mal pro Jahr teilnehmen, die in der Arbeitszeit stattfinden wird.",
        "Äußern Sie Ihre Meinung zur verpflichtenden Kommunikationsschulung.",
        "Nennen Sie Vor- und Nachteile von Weiterbildung während der Arbeitszeit.",
        "Berichten Sie von Ihren Erfahrungen mit Kommunikationsproblemen im Beruf.",
        "Machen Sie Vorschläge für ein bedarfsgerechtes Weiterbildungsangebot."
    ),
    (
        "schr-f-homeoffice-vereinbaren", 43, "Homeoffice-Tage individuell mit der Führungskraft vereinbaren", "Homeoffice & Flexibilität", 102,
        "Alle Mitarbeiterinnen und Mitarbeiter in Ihrer Firma sollen die Möglichkeit erhalten, mehr Stunden im Homeoffice zu verbringen, um Familie und Beruf besser miteinander vereinbaren zu können.",
        "Äußern Sie Ihre Meinung zu Homeoffice als individueller Vereinbarung.",
        "Wägen Sie Vor- und Nachteile flexibler Lösungen gegenüber festen Regeln ab.",
        "Berichten Sie von Ihren Erfahrungen mit Heimarbeit.",
        "Schlagen Sie klare und faire Kriterien vor."
    ),
    (
        "schr-f-28-bueromoebel-ergonomie", 44, "Ergonomische Büromöbel und Stehtische", "Gesundheit am Arbeitsplatz", 102,
        "Alle Mitarbeitenden Ihrer Firma sollen ihre Überstunden durch Freizeit ausgleichen. Die dadurch eingesparten Mittel werden für die Anschaffung neuer Büromöbel verwendet.",
        "Äußern Sie Ihre Meinung zur Anschaffung ergonomischer Büromöbel.",
        "Nennen Sie Vor- und Nachteile dieser gesundheitlichen Investition.",
        "Berichten Sie von Ihren Erfahrungen mit körperlicher Belastung am Schreibtisch.",
        "Schlagen Sie zusätzliche Maßnahmen zur Förderung der Mitarbeitergesundheit vor."
    ),
    (
        "schr-f-29-gesundheitscheck", 45, "Jährlicher Gesundheitscheck auf Firmenkosten", "Betriebsärztliche Vorsorge", 102,
        "",
        "Äußern Sie Ihre Ansicht zu dem betrieblichen Gesundheitscheck.",
        "Diskutieren Sie Chancen für die Prävention und Bedenken bezüglich des Datenschutzes.",
        "Erzählen Sie von medizinischer Vorsorge in Ihrem Heimatland.",
        "Machen Sie Vorschläge für die Wahrung der strikten ärztlichen Schweigepflicht."
    ),
    (
        "schr-f-elternzeit-weiterbildung", 46, "Weiterbildungen während der Elternzeit", "Elternzeit & Karriere", 102,
        "Allen Kolleg*innen wurde mitgeteilt, dass sie während der Elternzeit entweder an Teambesprechungen oder an Weiterbildungen teilnehmen sollen. Der Grund dafür ist, dass sie den Kontakt zur Firma nicht verlieren.",
        "Äußern Sie Ihre Meinung zu Weiterbildungen während der Elternzeit.",
        "Wägen Sie Vor- und Nachteile für den Wiedereinstieg und für die Erholung ab.",
        "Berichten Sie von Ihren eigenen Erfahrungen oder Beobachtungen zum Thema.",
        "Schlagen Sie freiwillige und familienfreundliche Regeln vor."
    ),
    (
        "schr-f-30-firmenchat-slack", 47, "Einführung eines firmenweiten Instant-Chats", "Interne Kommunikation", 102,
        "Alle Mitarbeiterinnen und Mitarbeiter in Ihrer Firma werden nach der Kündigung aus dem Firmenchat entfernt, damit sie nicht auf die aktuellen Informationen der Firma zugreifen können.",
        "Nehmen Sie Stellung zur Einführung eines internen Chat-Tools anstelle von E-Mails.",
        "Wägen Sie Schnelligkeit gegen Ablenkung und Informationsüberflutung ab.",
        "Berichten Sie von Ihren bevorzugten Kommunikationswegen bei der Arbeit.",
        "Schlagen Sie klare Kommunikationsregeln (z. B. feste Ruhezeiten) vor."
    ),
    (
        "schr-f-24-samstagsarbeit", 48, "Verpflichtende Samstagsarbeit zweimal pro Jahr", "Arbeitszeit & Wochenendarbeit", 102,
        "Alle Mitarbeiterinnen und Mitarbeiter in Ihrer Firma sollen aufgrund der guten Auftragslage auch an Samstagen arbeiten. Diese Arbeitszeiten werden mit einem Zuschlag in Höhe von 120 Prozent vergütet.",
        "Nehmen Sie Stellung zur Verpflichtung zu zwei Samstagsdiensten pro Jahr.",
        "Nennen Sie Vor- und Nachteile für das Unternehmen und das Privatleben.",
        "Berichten Sie von Erfahrungen mit Samstags- oder Schichtarbeit.",
        "Schlagen Sie ein freiwilliges Bonussystem für Wochenendeinsätze vor."
    ),
    (
        "schr-f-firmenlaptop-versicherung", 49, "Firmenlaptop mit privater Nutzung gegen eigene Versicherung", "Arbeitsmittel & IT-Ausstattung", 102,
        "Alle Mitarbeiterinnen und Mitarbeiter in Ihrer Firma erhalten einen Laptop. Dieser darf auch privat genutzt werden. Allerdings müssen sie dafür eine Laptopversicherung abschließen und diese selbst bezahlen.",
        "Äußern Sie Ihre Meinung zur privaten Nutzung mit eigener Versicherung.",
        "Nennen Sie Vor- und Nachteile für Beschäftigte und Unternehmen.",
        "Berichten Sie von Ihren Erfahrungen mit Firmengeräten und privater Nutzung.",
        "Schlagen Sie alternative Regelungen vor."
    ),
    (
        "schr-f-unternehmen-schulen", 50, "Unternehmen in Schulen vorstellen", "Nachwuchsgewinnung & Image", 102,
        "Alle Mitarbeiterinnen und Mitarbeiter Ihrer Firma sollen künftig in den Schulen der Region das Unternehmen vorstellen. Ziel dieser Maßnahme ist es, für das Ausbildungsangebot des Betriebs zu werben und neue Auszubildende zu gewinnen. Nicht alle ihn Team sind von dieser Idee begeistert.",
        "Äußern Sie Ihre Meinung zum Einsatz aller Beschäftigten in Schulen.",
        "Wägen Sie Vor- und Nachteile für Nachwuchsgewinnung und Arbeitsalltag ab.",
        "Berichten Sie von Ihren Erfahrungen mit Präsentationen oder Ausbildung.",
        "Machen Sie einen Vorschlag, wie sich das Engagement freiwillig und wirksam organisieren lässt."
    ),
    (
        "schr-f-32-zigarettenpause", 51, "Zigarettenpausen nur noch mit Ausstempeln", "Pausenregelung & Gleichbehandlung", 102,
        "In jedem Firmengebäude soll ein Raucherraum eingerichtet werden. Damit Raucher ihre 5Minuten-Zigarettenpause schneller machen können, ohne vor das Gebäude zu gehen. Raucher sollen jedoch 15 Minuten länger arbeiten.",
        "Äußern Sie Ihre Meinung zur Zeiterfassungspflicht bei Raucherpausen.",
        "Diskutieren Sie Vor- und Nachteile für das Betriebsklima und die Gerechtigkeit.",
        "Schildern Sie Regelungen zu Raucherpausen aus Ihren früheren Erfahrungen.",
        "Machen Sie einen Vorschlag für eine einvernehmliche und gesunde Pausenregelung."
    ),
    (
        "schr-f-31-papierlose-abrechnung", 52, "Rein papierlose Lohnabrechnung im Online-Portal", "Digitalisierung & Umwelt", 102,
        "Alle Mitarbeiterinnen und Mitarbeiter in Ihrer Firma erhalten künftig keine Lohn- / Gehaltsabrechnungen mehr in Papierform, sondern können diese selbst online einsehen. Sie müssen diese ab sofort selbst von ihrem persönlichen Konto im Intranet herunterladen.",
        "Äußern Sie Ihre Haltung zur Umstellung auf rein digitale Abrechnungen.",
        "Nennen Sie Vor- und Nachteile der Digitalisierung der Personaldokumente.",
        "Berichten Sie von Ihren Erfahrungen mit Online-Behörden und digitalen Portalen.",
        "Schlagen Sie Hilfsangebote und Schulungen für weniger technikaffine Kollegen vor."
    ),
    (
        "schr-f-betriebsferien-august", 53, "Urlaub während der dreiwöchigen Betriebsferien im August", "Betriebsferien & Urlaubsplanung", 102,
        "Alle Mitarbeiterinnen und Mitarbeiter in Ihrer Firma sollen ab dem kommenden Jahr während der dreiwöchigen Betriebsferien im August Urlaub nehmen. Die restlichen Urlaubstage können sie selbst planen.",
        "Äußern Sie Ihre Meinung zu verpflichtenden Betriebsferien im August.",
        "Nennen Sie Vor- und Nachteile für Betrieb und Beschäftigte.",
        "Schildern Sie Ihre eigene Urlaubsplanung und Ihre Erfahrungen damit.",
        "Machen Sie einen Vorschlag für eine flexiblere Regelung."
    ),
    (
        "schr-f-homeoffice-wechseln", 54, "Zwischen Homeoffice und Büro wechseln – ohne eigenen Schreibtisch", "Arbeitsplatzmodelle & Desk-Sharing", 102,
        "Alle Mitarbeiterinnen und Mitarbeiter sollen in Ihrer Firma zwischen Homeoffice und Büro wechseln. Dafür haben sie keinen eigenen Schreibtisch mehr, sondern persönliches Arbeitsmaterial im Rollcontainer.",
        "Äußern Sie Ihre Meinung zum Wechselmodell ohne festen Schreibtisch.",
        "Wägen Sie Vor- und Nachteile für Konzentration, Zusammenarbeit und Organisation ab.",
        "Berichten Sie von Ihren Erfahrungen mit wechselnden Arbeitsplätzen.",
        "Machen Sie Vorschläge für praktikable Regeln."
    ),
    (
        "schr-f-parken-firmengebaeude", 55, "Parken im Firmengebäude kostet 20 Euro", "Parken & Mobilität", 102,
        "Alle Mitarbeiterinnen und Mitarbeiter in Ihrer Firma sollen im Firmengebäude parken und jeden Monat 20€ bezahlen.",
        "Äußern Sie Ihre Meinung zu Parkgebühren für Beschäftigte.",
        "Wägen Sie Vor- und Nachteile für Autofahrende, ÖPNV-Nutzung und Betrieb ab.",
        "Berichten Sie von Ihren Erfahrungen mit dem Parken am Arbeitsplatz.",
        "Schlagen Sie Kompromisse vor (Ausnahmen, Alternativen, Zuschüsse)."
    ),
    # --- PÁGINA 103 ---
    (
        "schr-f-33-obstkorb", 56, "Frisches Bio-Obst im Büro für 5 € monatlich", "Gesunde Ernährung im Büro", 103,
        "Alle Mitarbeiterinnen und Mitarbeiter in Ihrer Firma sollen für das bisher kostenfreie Obst monatlich 5 Euro bezahlen. Sie befinden sich in der Teeküche. Damit möchte die Firma die regionale Landwirtschaft der Stadt unterstützen.",
        "Äußern Sie Ihre Ansicht zur Obstkorb-Initiative und der Kostenbeteiligung.",
        "Wägen Sie die gesundheitlichen Vorteile gegen den monatlichen Eigenanteil ab.",
        "Berichten Sie von Verpflegungsangeboten an früheren Arbeitsstellen.",
        "Schlagen Sie eine faire Finanzierung oder Sponsoring durch den Betrieb vor."
    ),
    (
        "schr-f-34-glaswaende", 57, "Transparente Bürowände aus Glas", "Arbeitsplatzgestaltung", 103,
        "Alle Mitarbeiterinnen und Mitarbeiter in Ihrer Firma sollen zwar ihre Einzelbüros behalten, doch die gemauerten Bürowände werden demnächst durch Glas ersetzt. Damit soll ein besseres Betriebsklima gefördert werden.",
        "Nehmen Sie Stellung zum Einbau transparenter Glaswände im Büro.",
        "Diskutieren Sie Vor- und Nachteile von optischer Offenheit versus Privatsphäre.",
        "Beschreiben Sie, wie Ihre ideale Büroaufteilung aussehen sollte.",
        "Schlagen Sie Lösungen vor (z. B. Sichtschutzfolien oder Vorhänge nach Bedarf)."
    ),
    (
        "schr-f-dresscode", 58, "Dresscode: formelle Kleidung statt Jeans", "Dresscode & Außenwirkung", 103,
        "Alle Mitarbeitenden Ihrer Firma sollen einen Dresscode anhalten und formelle Kleidung statt Jeans und Sportschuhe tragen.",
        "Äußern Sie Ihre Meinung zu einem verbindlichen Dresscode.",
        "Wägen Sie Vor- und Nachteile für Außenwirkung, Kosten und Wohlbefinden ab.",
        "Berichten Sie von Ihren Erfahrungen mit Kleidungsvorschriften.",
        "Machen Sie einen Vorschlag für eine angemessene Regelung."
    ),
    (
        "schr-f-35-clean-desk", 59, "Clean-Desk-Policy: Schreibtisch täglich komplett leeren", "Ordnung am Arbeitsplatz", 103,
        "Alle Mitarbeitenden Ihrer Firma sollen selbst ihre Arbeitsplätze aufräumen. Als Vergütung bekommt man dann Snacks, Obst und Gemüse.",
        "Äußern Sie Ihre Haltung zur strikten Clean-Desk-Regel.",
        "Nennen Sie Vor- und Nachteile für Datenschutz, Ordnung und Wohlbefinden.",
        "Erzählen Sie, wie an Ihrem Arbeitsplatz mit Dokumenten und Ordnung verfahren wird.",
        "Schlagen Sie praxistaugliche Regeln vor, die Sicherheit und Gemütlichkeit verbinden."
    ),
    (
        "schr-f-fortbildung-fuenfmal", 60, "Fünf Fortbildungen pro Jahr – in der Arbeitszeit", "Weiterbildung & Arbeitszeit", 103,
        "Alle Mitarbeiterinnen und Mitarbeiter in Ihrer Firma können fünfmal pro Jahr an einer Weiterbildung teilnehmen. Die Weiterbildung sollen sie selbst bezahlen, aber sie findet während der Arbeitszeit statt.",
        "Äußern Sie Ihre Meinung zu fünf Fortbildungen mit Eigenbeteiligung.",
        "Nennen Sie Vor- und Nachteile für Beschäftigte und Betrieb.",
        "Berichten Sie von Ihren Erfahrungen mit selbst finanzierten Weiterbildungen.",
        "Machen Sie einen Vorschlag für ein gerechtes Finanzierungsmodell."
    ),
    (
        "schr-f-firmenraeume-privat", 61, "Firmenräume kostenlos für private Veranstaltungen nutzen", "Benefits & Betriebsgelände", 103,
        "Alle Mitarbeiterinnen und Mitarbeiter in Ihrer Firma dürfen Räume, Küche und Garten für private Veranstaltungen kostenlos nutzen.",
        "Äußern Sie Ihre Meinung zur kostenlosen privaten Nutzung der Firmenräume.",
        "Wägen Sie Vor- und Nachteile für Betriebsklima und Organisation ab.",
        "Berichten Sie, wofür Sie die Räume selbst nutzen würden.",
        "Machen Sie einen Vorschlag für klare Regeln (Reinigung, Haftung, Termine)."
    ),
    (
        "schr-f-36-englisch-firmensprache", 62, "Englisch als verbindliche Firmensprache", "Sprachregelung & Internationalität", 103,
        "Alle Mitarbeitenden sollen zukünftig ausschließlich Englisch miteinander sprechen, weil das Unternehmen einen neuen Eigentümer aus Großbritannien hat. Intensive Englischkurse werden während der Arbeitszeit angeboten.",
        "Äußern Sie Ihre Meinung zur Einführung von Englisch als alleiniger Firmensprache.",
        "Wägen Sie internationale Wettbewerbsfähigkeit gegen Sprachbarrieren im Team ab.",
        "Berichten Sie von Ihren eigenen Erfahrungen mit Fremdsprachen im Arbeitsumfeld.",
        "Schlagen Sie ein schrittweises Modell mit gezielter Sprachförderung vor."
    ),
    (
        "schr-f-geburtstagsgeschenke", 63, "Geburtstagsgeschenke über einen Monatsbeitrag von 5 Euro", "Teamkultur & Kostenbeteiligung", 103,
        "Alle Mitarbeitenden sollen einen Beitrag von 5 € monatlich einzahlen. Das Geld wird für die Geburtstagsgeschenke finanziert.",
        "Äußern Sie Ihre Meinung zum verpflichtenden Beitrag für Geschenke.",
        "Wägen Sie Vor- und Nachteile für Teamkultur und Fairness ab.",
        "Berichten Sie von Ihren Erfahrungen mit Geschenken im Team.",
        "Machen Sie einen Vorschlag für eine freiwillige oder faire Lösung."
    ),
    (
        "schr-f-vier-tage-woche", 64, "Vier-Tage-Woche mit zehn Stunden pro Tag", "Arbeitszeitmodelle", 103,
        "Alle Mitarbeiterinnen und Mitarbeiter in Ihrer Firma sollen zukünftig nur noch an vier Tagen pro Woche arbeiten. Dafür wird die Arbeitszeit an den anderen Tagen auf zehn Stunden erhöht.",
        "Äußern Sie Ihre Meinung zur Vier-Tage-Woche mit langen Arbeitstagen.",
        "Wägen Sie Vor- und Nachteile für Gesundheit, Familie und Betrieb ab.",
        "Berichten Sie von Ihren Erfahrungen mit langen oder verdichteten Arbeitstagen.",
        "Machen Sie einen Vorschlag für ein flexibles Arbeitszeitmodell."
    ),
    (
        "schr-f-37-essverbot-schreibtisch", 65, "Essverbot am Schreibtisch und Computer", "Hygiene & Pausenkultur", 103,
        "Alle Mitarbeiterinnen und Mitarbeiter in Ihrer Firma sollen aus hygienischen Gründen nicht mehr am Arbeitsplatz essen. Selbst ein Stückchen Schokolade darf ausschließlich in der Teeküche gegessen werden.",
        "Nehmen Sie Stellung zum Verbot von Snacks und Essen am Arbeitsplatz.",
        "Diskutieren Sie Vor- und Nachteile bezüglich Hygiene, Geruch und Flexibilität.",
        "Schildern Sie die Pausengewohnheiten an Ihren früheren Arbeitsplätzen.",
        "Machen Sie Vorschläge für eine saubere und dennoch praxisnahe Regelung."
    ),
    # --- PÁGINA 104 ---
    (
        "schr-f-38-konfliktmanagement", 66, "Verpflichtendes Konfliktmanagement-Seminar", "Teamentwicklung & Zusammenarbeit", 104,
        "Alle Mitarbeiterinnen und Mitarbeiter in Ihrem Unternehmen sollen an einem Seminar teilnehmen, um die Kommunikation und das Arbeitsklima im Unternehmen zu verbessern.",
        "Äußern Sie Ihre Ansicht zu dem verordneten Konfliktlösungs-Training.",
        "Nennen Sie Vor- und Nachteile von verpflichtenden psychologischen Teamtrainings.",
        "Berichten Sie von Ihren Erfahrungen mit Konfliktlösungen im beruflichen Alltag.",
        "Schlagen Sie alternative, wirksame Wege zur Verbesserung des Betriebsklimas vor."
    ),
    (
        "schr-f-39-dienstrad", 67, "Dienstrad-Leasing und Reparaturzuschuss", "Nachhaltige Mobilität", 104,
        "Alle Mitarbeiterinnen und Mitarbeiter in Ihrer Firma, die mit dem Fahrrad zur Arbeit kommen, sollen einen Zuschuss für die Reparaturen und Wartung erhalten. Autofahrer bekommen aber nichts.",
        "Nehmen Sie Stellung zu dem Dienstrad-Leasingangebot der Firma.",
        "Diskutieren Sie die Vor- und Nachteile für die Gesundheit, die Umwelt und den Betrieb.",
        "Erzählen Sie von Ihren eigenen Mobilitätsgewohnheiten auf dem Weg zur Arbeit.",
        "Schlagen Sie begleitende Maßnahmen (z. B. überdachte Abstellanlagen, Ladestationen) vor."
    ),
    (
        "schr-f-40-sommerkleidung-kurz", 68, "Verbot kurzer Kleidung bei Sommerhitze", "Dresscode bei Hitze", 104,
        "Allen Mitarbeiterinnen und Mitarbeiter in Ihrer Firma ist es im Sommer nicht erlaubt, unangemessen kurze Kleidung bei der Arbeit zu tragen. Außerdem sollten kurze Hosen, Miniröcke und ärmellose Oberteile nicht getragen werden.",
        "Äußern Sie Ihre Meinung zum Verbot von leichter Sommerkleidung.",
        "Wägen Sie professionelles Auftreten gegen Gesundheit und Wohlbefinden bei Hitze ab.",
        "Berichten Sie von Kleidungsvorschriften im Sommer in Ihrem Heimatland.",
        "Schlagen Sie eine hitzeangepasste Kleiderordnung für die Sommermonate vor."
    ),
    (
        "schr-f-41-azubi-betreuung", 69, "Patenschaften: Jeder Mitarbeiter betreut Auszubildende", "Ausbildung & Nachwuchsförderung", 104,
        "Alle Mitarbeiterinnen und Mitarbeiter in Ihrer Firma sollen ab sofort in die Betreuung der Auszubildenden aktiver eingebunden werden und dazu einen Plan erstellen, wer welche Aufgaben übernimmt.",
        "Nehmen Sie Stellung zu dem verpflichtenden Patenschafts-Modell.",
        "Nennen Sie Vor- und Nachteile für Auszubildende und erfahrene Mitarbeiter.",
        "Berichten Sie von Ihren eigenen Erfahrungen während der Ausbildung oder Einarbeitung.",
        "Unterbreiten Sie Vorschläge für Schulungen und Zeitanrechnungen für die Paten."
    ),
    (
        "schr-f-42-pausenhof-garten", 70, "Grüner Pausenhof statt Firmenparkplatz", "Betriebsgelände & Erholung", 104,
        "Alle Mitarbeiterinnen und Mitarbeiter in Ihrer Firma sollen demnächst nicht mehr im Innenhof parken können. Die Fläche soll bepflanz und Sitzgelegenheiten für die Pausen ausgestattet werden.",
        "Äußern Sie Ihre Meinung zum Umbau der Parkplätze in einen Erholungshof.",
        "Wägen Sie Erholungswert und Klimaschutz gegen den Verlust von Stellplätzen ab.",
        "Beschreiben Sie, wie Sie Ihre Mittagspausen am liebsten verbringen.",
        "Schlagen Sie einen Kompromiss vor, der Grünflächen und Parkmöglichkeiten vereint."
    ),
    (
        "schr-f-fortbildung-punkte", 71, "Mehr Fortbildungen mit Punkten und Gutscheinen", "Weiterbildung & Anreize", 104,
        "Alle Mitarbeiterinnen und Mitarbeiter sollen mehr Fortbildungen besuchen. Für jede absolvierte Fortbildung erhalten sie Punkte, die später gegen Gutscheine (z. B. für Freizeitangebote oder Einkaufsgutscheine) eingetauscht werden können.",
        "Äußern Sie Ihre Meinung zu Punkten und Gutscheinen als Anreiz.",
        "Wägen Sie Vor- und Nachteile für Motivation und Qualität der Weiterbildung ab.",
        "Berichten Sie von Ihren Erfahrungen mit Prämien- oder Bonussystemen.",
        "Machen Sie einen Vorschlag für ein sinnvolleres Anreizmodell."
    ),
    (
        "schr-f-einsatzorte", 72, "Arbeiten an verschiedenen Einsatzorten ohne Fahrkostenerstattung", "Reisetätigkeit & Kosten", 104,
        "In Ihrer Firma ist geplant, dass im Sommer alle Mitarbeiterinnen und Mitarbeiter an verschiedenen Einsatzorten arbeiten sollen. Die Fahrkosten werden jedoch nicht erstatten.",
        "Äußern Sie Ihre Meinung zum Einsatz an wechselnden Orten.",
        "Wägen Sie Vor- und Nachteile für Erfahrung, Belastung und Kosten ab.",
        "Berichten Sie von Ihren Erfahrungen mit Reisetätigkeit oder Pendeln.",
        "Machen Sie einen Vorschlag für eine faire Kostenregelung."
    ),
    (
        "schr-f-kita-freitag", 73, "Firmen-Kita freitags wegen Personalmangels geschlossen", "Kinderbetreuung & Vereinbarkeit", 104,
        "Alle Mitarbeiter und Mitarbeiterinnen in Ihrer Firma sollen freitags für eine private Kinderbetreuung sorgen. Die Firmen-Kita ist ab sofort an diesem Tag wegen Personalmangels geschlossen.",
        "Äußern Sie Ihre Meinung zur Schließung der Firmen-Kita am Freitag.",
        "Erörtern Sie die Folgen für Familien und für den Betrieb.",
        "Berichten Sie von Ihren Erfahrungen mit Kinderbetreuung und Arbeitszeiten.",
        "Machen Sie Vorschläge für Übergangslösungen und langfristige Verbesserungen."
    ),
    (
        "schr-f-66-buero-mit-hunden", 74, "Bürohunde im Unternehmen erlaubt", "Haustiere am Arbeitsplatz", 104,
        "Alle Mitarbeiterinnen und Mitarbeiter in Ihrer Firma sollen ihre Hunde ins Büro mitbringen dürfen. Diese Regelung dient der Förderung des Betriebsklimas. Allerdings dürfen die Hunde andere Kolleg*innen nicht stören.",
        "Äußern Sie Ihre Haltung zu Hunden am Arbeitsplatz.",
        "Wägen Sie Entspannung und Freude gegen Allergien, Ängste und Hygiene ab.",
        "Berichten Sie von Ihren Erfahrungen mit Haustieren im beruflichen Umfeld.",
        "Formulieren Sie konkrete Richtlinien für ein harmonisches Miteinander von Mensch und Tier."
    ),
    (
        "schr-f-64-gleitzeit-abschaffung", 75, "Gleitzeit wird abgeschafft (feste Arbeitszeit 8:30–17:00)", "Arbeitszeitmodell / Flexibilität", 104,
        "Alle Mitarbeiterinnen und Mitarbeiter sollen von 8:30 bis 17 arbeiten. Gleitzeit wird abgeschafft.",
        "Nehmen Sie Stellung zur Abschaffung der Gleitzeit zugunsten starrer Kernzeiten.",
        "Wägen Sie Kundenorientierung gegen Flexibilität und Lebensqualität der Beschäftigten ab.",
        "Schildern Sie Ihre Erfahrungen mit verschiedenen Arbeitszeitmodellen.",
        "Schlagen Sie ein Modell mit Kernarbeitszeiten vor, das beiden Seiten gerecht wird."
    ),
    (
        "schr-f-43-dienstreisen-online", 76, "Kurze Dienstreisen nur noch virtuell", "Reiserichtlinie & Klimaschutz", 104,
        "Alle Mitarbeiterinnen und Mitarbeiter Ihrer Firma sollen kurze Dienstreise zwischen Mitarbeitern und Kunden aus anderen Städten nur noch virtuell durchführen.",
        "Nehmen Sie Stellung zu der Pflicht, kurze Dienstreisen virtuell durchzuführen.",
        "Diskutieren Sie Vor- und Nachteile von Online-Meetings im Kundenkontakt.",
        "Berichten Sie von eigenen Erfahrungen mit Dienstreisen und Videocalls.",
        "Schlagen Sie Kriterien vor, wann ein persönliches Treffen weiterhin erlaubt sein sollte."
    ),
    (
        "schr-f-65-weiterbildung-nur-online", 77, "Weiterbildungen nur noch online / als E-Learning", "Digitale Fortbildung", 104,
        "Die Geschäftsleitung Ihrer Firma hat beschlossen, dass alle Mitarbeiterinnen und Mitarbeiter im nächsten Jahr an einer Weiterbildung teilnehmen sollen. Dabei werden ausschließlich Online-Kurse berücksichtigt.",
        "Äußern Sie Ihre Meinung zur ausschließlichen Nutzung von Online-Fortbildungen.",
        "Nennen Sie Vor- und Nachteile von E-Learning im Vergleich zu Präsenzseminaren.",
        "Berichten Sie von Ihren Erfahrungen mit digitalen Lernangeboten im Beruf.",
        "Schlagen Sie ein Blended-Learning-Konzept vor, das Online- und Präsenzteile verbindet."
    ),
    (
        "schr-f-44-baumpflanzen", 78, "Gemeinsame Baumpflanz-Aktion im Stadtwald", "Corporate Social Responsibility", 104,
        "Alle Mitarbeiterinnen und Mitarbeiter in Ihrer Firma sollen nach Möglichkeit am kommenden Wochenende an einer Baumpflanz- Aktion im Stadtwald teilnehmen, um das Umweltengagement der Firma zu unterstützen.",
        "Äußern Sie Ihre Meinung zu dem bezahlten Umwelttag im Stadtwald.",
        "Nennen Sie Vor- und Nachteile solcher gemeinnützigen Firmenaktionen.",
        "Berichten Sie von Umwelt- und Nachhaltigkeitsprojekten, an denen Sie teilgenommen haben.",
        "Schlagen Sie weitere nachhaltige Ideen für den betrieblichen Alltag vor."
    ),
    # --- PÁGINA 105 ---
    (
        "schr-f-45-betriebsausflug-samstag", 79, "Pflicht-Betriebsausflug am Samstag", "Teambuilding & Freizeit", 105,
        "Der diesjährige Betriebsausflug soll an einem Samstag stattfinden. Die Teilnahme ist Pflicht. Dafür können alle Mitarbeiterinnen und Mitarbeiter innerhalb der folgenden zwei Wochen einen freien Tag unter der Woche nehmen.",
        "Nehmen Sie Stellung zur Verpflichtung zu einem Wochenend-Betriebsausflug.",
        "Wägen Sie Teambildung gegen den Eingriff in das private Wochenende ab.",
        "Berichten Sie von Betriebsausflügen und Firmenfeiern an früheren Arbeitsstellen.",
        "Schlagen Sie eine flexiblere oder freiwillige Gestaltung des Ausflugs vor."
    ),
    (
        "schr-f-homeoffice-privater-laptop", 80, "Homeoffice mit privatem Laptop", "Homeoffice & Ausstattung", 105,
        "Alle Mitarbeiterinnen und Mitarbeiter sollen die Möglichkeit bekommen, zukünftig ein bis zwei Tage pro Woche von zu Hause aus zu arbeiten. Sie sollen dafür ihre privaten Laptops benutzen.",
        "Äußern Sie Ihre Meinung zur Homeoffice-Regelung mit privaten Geräten.",
        "Wägen Sie Vor- und Nachteile für Beschäftigte und Unternehmen ab (Kosten, Sicherheit, Datenschutz).",
        "Berichten Sie von Ihren Erfahrungen mit der Ausstattung im Homeoffice.",
        "Machen Sie einen Vorschlag für eine klare Ausstattungsregelung."
    ),
    (
        "schr-f-46-kamera-pflicht", 81, "Kamera-Pflicht bei allen Online-Meetings", "Videokonferenzen / Netiquette", 105,
        "Alle Mitarbeiterinnen und Mitarbeiter in Ihrer Firma sollen während der Online- Konferenzen ständig ihre Kamera eingeschaltet lassen. Dies soll die Zusammenarbeit angenehmer machen und aktive Teilnahme fördern.",
        "Äußern Sie Ihre Meinung zur dauerhaften Kamera-Pflicht in Online-Meetings.",
        "Diskutieren Sie Vor- und Nachteile von eingeschalteten Kameras für die Meeting-Kultur.",
        "Schildern Sie Ihre eigenen Erfahrungen und Gewohnheiten bei Videokonferenzen.",
        "Formulieren Sie Regeln für eine respektvolle und zweckmäßige Kameranutzung."
    ),
    (
        "schr-f-47-urlaubssperre-praemie", 82, "Urlaubssperre im August/September mit 500 € Bonus", "Urlaubssperre & Belastung", 105,
        "Alle Mitarbeiterinnen und Mitarbeiter in Ihrer Firma sollen im August und September wegen eines Großauftrags keinen Urlaub machen. Als Dankeschön gibt es einen Bonus von 500 €. (Es wurde vorgeschlagen, als Ausgleich für Urlaub eine Geldprämie in Höhe von 500 € zu zahlen.)",
        "Nehmen Sie Stellung zu der kurzfristigen Urlaubssperre mit finanzieller Entschädigung.",
        "Wägen Sie geschäftliche Dringlichkeit gegen die Erholungsbedürfnisse der Mitarbeiter ab.",
        "Berichten Sie von Situationen mit hohem Arbeitsaufkommen und Termindruck.",
        "Schlagen Sie Alternativen (z. B. studentische Aushilfen oder Projektprämien) vor."
    ),
    (
        "schr-f-48-ueberstunden-freizeit", 83, "Überstundenausgleich ausschließlich in Freizeit", "Überstundenvergütung", 105,
        "Die Mitarbeiterinnen und Mitarbeiter in Ihrer Firma sollen ihre Überstunden zu künftig in Form von Freizeit ausgleichen. Die Absprache mit der Abteilungsleitung ist erforderlich. Eine Auszahlung ist nicht mehr möglich.",
        "Äußern Sie Ihre Ansicht zur Streichung der Überstundenauszahlung.",
        "Nennen Sie Vor- und Nachteile von Freizeitausgleich im Vergleich zu Geldvergütung.",
        "Berichten Sie, wie Überstunden an Ihren früheren Arbeitsplätzen geregelt wurden.",
        "Schlagen Sie ein Wahlmodell zwischen Freizeitausgleich und Auszahlung vor."
    ),
    (
        "schr-f-49-kurzarbeit", 84, "Kurzarbeit um 50 % wegen Auftragsmangel", "Krisenmanagement & Kurzarbeit", 105,
        "Alle Mitarbeiterinnen und Mitarbeiter in Ihrer Firma sollen aufgrund der schlechten Auftragslage ab sofort in Kurzarbeit gehen. Die Arbeitszeit wird für die gesamte Belegschaft um 50% verringert.",
        "Nehmen Sie Stellung zur Einführung von Kurzarbeit im Unternehmen.",
        "Diskutieren Sie Vor- und Nachteile von Kurzarbeit gegenüber Kündigungen.",
        "Berichten Sie von Erfahrungen mit wirtschaftlichen Krisen im Berufsleben.",
        "Schlagen Sie Weiterbildungsmaßnahmen während der Kurzarbeitszeit vor."
    ),
    (
        "schr-f-50-betriebsferien-weihnachten", 85, "Betriebsferien zwischen Weihnachten und Neujahr", "Betriebsruhe & Urlaubsanspruch", 105,
        "Alle Mitarbeitenden Ihrer Firma sollen auf zwei Tage ihres Urlaubs verzichten, damit alle Betriebsferien zwischen Weihnachten und Neujahr abgedeckt sind.",
        "Äußern Sie Ihre Meinung zur Festlegung von Betriebsferien zum Jahreswechsel.",
        "Wägen Sie Ruhe für den gesamten Betrieb gegen individuelle Urlaubsfreiheit ab.",
        "Erzählen Sie von Feiertags- und Urlaubsregelungen in Ihrem Herkunftsland.",
        "Machen Sie einen Vorschlag für Notbesetzungen oder flexible Zeiterfassungsmodelle."
    ),
    (
        "schr-f-51-innenhof-freizeit", 86, "Gestaltung des Innenhofs in der Freizeit", "Mitarbeiterengagement / Pausengestaltung", 105,
        "Alle Mitarbeitenden Ihrer Firma sollen dabei helfen, den Innenhof als Aufenthaltsbereich für die Pause zu gestalten. Sie sollen ihn auch am Wochenende und in ihrer Freizeit pflegen.",
        "Nehmen Sie Stellung zu dem Aufruf zur freiwilligen Wochenendarbeit für den Innenhof.",
        "Nennen Sie Vor- und Nachteile von Teameinsätzen für die Arbeitsumgebung.",
        "Berichten Sie von ehrenamtlichen oder gemeinschaftlichen Projekten im Beruf.",
        "Schlagen Sie vor, wie das Projekt während der regulären Arbeitszeit umgesetzt werden kann."
    ),
    (
        "schr-f-52-oepnv-jahresticket", 87, "Kostenloses ÖPNV-Abo bei Verzicht aufs Privatauto", "Betrieblicher Klimaschutz", 105,
        "Alle Mitarbeiterinnen und Mitarbeiter in Ihrer Firma sollen motiviert werden, aus Gründen des Umweltschutzes ab sofort das Auto stehenzulassen. Dafür erhalten sie ein kostenfreies Jahres-Abo für Bus und Bahn.",
        "Äußern Sie Ihre Meinung zu der Prämie für den Verzicht auf das Auto.",
        "Wägen Sie Umweltentlastung gegen die Realität ländlicher Pendler ab.",
        "Berichten Sie von Ihren täglichen Mobilitätsentscheidungen.",
        "Schlagen Sie Ergänzungen wie Park-and-Ride-Modelle oder Fahrgemeinschaften vor."
    ),
    (
        "schr-f-53-urlaubstag-fortbildung", 88, "Ein Urlaubstag für hochwertige Fortbildungen", "Investition in Weiterbildung", 105,
        "Alle Mitarbeiterinnen und Mitarbeiter in Ihrer Firma sollen ab dem kommenden Jahr für Fortbildungen einen Urlaubstag nehmen. Bezahlt werden die Fortbildungen aber weiterhin von der Firma.",
        "Nehmen Sie Stellung zu der Bedingung, einen Urlaubstag für Weiterbildung einzusetzen.",
        "Diskutieren Sie Vor- und Nachteile dieses Co-Finanzierungsmodells.",
        "Schildern Sie Erfahrungen mit beruflichen Fortbildungen und Eigenleistungen.",
        "Schlagen Sie klare Vereinbarungen über Bildungszeit und Kostenübernahme vor."
    ),
    (
        "schr-f-54-papierverbrauch-limit", 89, "Strenges Kopier- und Drucklimit pro Mitarbeiter", "Umweltschutz im Büro", 105,
        "Das Unternehmen hat beschlossen, in Zukunft aus Gründen des Umweltschutzes den Papierverbrauch im Unternehmen zu minimieren und die Anzahl der Kopien pro Mitarbeiter zu limitieren.",
        "Äußern Sie Ihre Haltung zu festen Druckkontingenten am Arbeitsplatz.",
        "Nennen Sie Vor- und Nachteile von Restriktionen beim Papierverbrauch.",
        "Berichten Sie von Ihren Erfahrungen mit dem papierlosen Büro.",
        "Schlagen Sie digitale Alternativen vor, die Arbeitsabläufe nicht ausbremsen."
    ),
    (
        "schr-f-55-kleiderspende", 90, "Betriebliche Kleiderspenden-Aktion für Kinder", "Soziales Engagement", 105,
        "Alle Mitarbeitenden Ihrer Firma können sich auf Wunsch an einer Sammelaktion für Kinderkleidung beteiligen. Der gesamte Erlös kommt einer Spende zugute.",
        "Äußern Sie Ihre Ansicht zu karitativen Aktionen am Arbeitsplatz.",
        "Erläutern Sie die Vor- und Nachteile von sozialem Engagement im Firmenrahmen.",
        "Berichten Sie von Hilfsprojekten oder Spendenaktionen aus Ihrem Umfeld.",
        "Machen Sie Vorschläge für die logistische Durchführung und Information der Kollegen."
    ),
    # --- PÁGINA 106 ---
    (
        "schr-f-56-ausflug-eigenes-essen", 91, "Betriebsausflug: Eigenes Essen mitbringen", "Sparmaßnahmen bei Firmenevents", 106,
        "Alle Mitarbeiterinnen und Mitarbeiter in Ihrer Firma müssen Essen für einen Betriebsausflug mitbringen. Sie müssen das Essen , das sie gerne essen, selbst zubereiten und mitbringen. Die Firma möchte Geld sparen.",
        "Nehmen Sie Stellung zu der Sparmaßnahme beim Betriebsausflug.",
        "Diskutieren Sie Vor- und Nachteile eines Mitbring-Büfetts (Potluck) im Vergleich zum Catering.",
        "Berichten Sie von Teamevents an früheren Arbeitsplätzen.",
        "Schlagen Sie ein faires Konzept vor (z. B. Grillen mit Basisverpflegung durch die Firma)."
    ),
    (
        "schr-f-57-freizeitbad-jahreskarte", 92, "Kostenlose Jahreskarte fürs Freizeitbad gegen Stress", "Betriebliche Gesundheitsvorsorge", 106,
        "Alle Mitarbeiterinnen und Mitarbeiter in Ihrer Firma sollen von Ihrer Firma Jahresjobtickets für das Freizeitbad der Stadt geschickt bekommen, um die Arbeit Alltagsstress abzubauen.",
        "Äußern Sie Ihre Meinung zu der Jahreskarte als betriebliche Gesundheitsförderung.",
        "Nennen Sie Vor- und Nachteile dieses spezifischen Freizeitangebots.",
        "Berichten Sie von Ihren persönlichen Methoden zur Stressbewältigung nach der Arbeit.",
        "Schlagen Sie weitere Ideen vor, um die Gesundheit der Belegschaft nachhaltig zu stärken."
    ),
    (
        "schr-f-58-geschaeftsreisen-bahn", 93, "Geschäftsreisen: Bahn statt Privat- oder Dienstwagen", "Nachhaltige Dienstreisen", 106,
        "Alle Mitarbeiterinnen und Mitarbeiter in Ihrer Firma sind angehalten, für Geschäftsreisen vermehrt Verkehrsmittel wie die Bahn anstelle des eigenen Autos zu nutzen.",
        "Nehmen Sie Stellung zur Verpflichtung, Dienstreisen mit der Bahn durchzuführen.",
        "Wägen Sie Klimaschutz und Arbeitskomfort gegen Unpünktlichkeit und Flexibilität ab.",
        "Erzählen Sie von Ihren Erfahrungen mit geschäftlichen Zugfahrten.",
        "Formulieren Sie Ausnahmeregelungen für zeitkritische oder abgelegene Termine."
    ),
    (
        "schr-f-59-keine-getraenke-mehr", 94, "Kaffee und Getränke nicht mehr kostenlos bereitgestellt", "Kürzung von Mitarbeiter-Benefits", 106,
        "Alle Mitarbeiterinnen und Mitarbeiter in Ihrer Firma sollen Kaffee und andere Getränke ab sofort vor zu Hause mitbringen, da die Firma diese nicht mehr bereitstellt.",
        "Äußern Sie Ihre Haltung zur Streichung der kostenlosen Getränke.",
        "Diskutieren Sie den Einfluss von kleinen Mitarbeiter-Benefits auf Motivation und Stimmung.",
        "Berichten Sie von Standards und Extras an Ihren bisherigen Arbeitsplätzen.",
        "Schlagen Sie einen Kompromiss (z. B. Kaffee-Kasse oder Wasserspender) vor."
    ),
    (
        "schr-f-60-handyverbot-grosskueche", 95, "Handyverbot in der Großküche aus Hygienegründen", "Hygiene & Lebensmittelsicherheit", 106,
        "Aus hygienischen Gründen dürfen die Küchenmitarbeiter kein Handy während der Arbeitszeit benutzen. Die Handys sollen im Spind eingeschlossen sein.",
        "Nehmen Sie Stellung zum Handyverbot in der Lebensmittelverarbeitung.",
        "Wägen Sie Hygiene- und Sicherheitsanforderungen gegen die Erreichbarkeit in Pausen ab.",
        "Berichten Sie von Hygiene- und Sicherheitsvorschriften aus Ihrer Berufspraxis.",
        "Machen Sie Vorschläge für klare Notfallkommunikation bei eingeschlossenen Handys."
    ),
    (
        "schr-f-61-fahrgemeinschaft-zuschuss", 96, "Benzinzuschuss nur für Fahrgemeinschaften", "Pendlerförderung & Umweltschutz", 106,
        "Alle Mitarbeitende, die einen Fahrgemeinschaft auf dem Weg zur Arbeit organisieren, bekommen einen Zuschuss von Benzingeld. Die einzelnen Fahrer erhalten keine Unterstützung.",
        "Äußern Sie Ihre Meinung zum Tankzuschuss exklusiv für Fahrgemeinschaften.",
        "Diskutieren Sie Vor- und Nachteile von Fahrgemeinschaften für den Arbeitsalltag.",
        "Erzählen Sie, wie Sie Ihren täglichen Arbeitsweg bewältigen.",
        "Schlagen Sie eine faire Pendlerpauschale für alle umweltfreundlichen Wege vor."
    ),
    (
        "schr-f-62-energie-sparen-fleece", 97, "Heizung drosseln (Energie sparen) und Fleecejacken", "Energiesparen & Bürotemperatur", 106,
        "In der Firma soll Energie gespart und nicht mehr so viel geheizt werden. Im Winter können die Mitarbeitenden, wenn ihnen zu kalt ist, in Winterkleidung ( Fleece Jacke von der Firma) im Büro arbeiten. ",
        "Nehmen Sie Stellung zur Absenkung der Heiztemperatur und der Bereitstellung von Fleecejacken.",
        "Wägen Sie Energiekosten und Klimaschutz gegen Gesundheit und Konzentration ab.",
        "Berichten Sie von Temperatur- und Klimaverhältnissen an früheren Arbeitsplätzen.",
        "Unterbreiten Sie praxistaugliche Vorschläge für Energieeffizienz ohne Frieren im Büro."
    ),
    (
        "schr-f-63-teambildung-wochenende", 98, "Teambuilding-Event am Wochenende in anderer Stadt", "Teamentwicklung & Reise", 106,
        "Alle Mitarbeiterinnen und Mitarbeiter sollen an einem Teambildungs-Event in einer anderen Stadt am Wochenende teilnehmen.",
        "Äußern Sie Ihre Ansicht zu dem Wochenend-Teambuilding mit Hotelübernachtung.",
        "Diskutieren Sie Chancen für den Zusammenhalt gegen die Belastung des privaten Wochenendes.",
        "Berichten Sie von Teambuilding-Events und Ausflügen aus Ihrer Erfahrung.",
        "Schlagen Sie alternative Formate während der regulären Arbeitswoche vor."
    ),
]
def main():
    variants = []
    for item in RAW_TOPICS:
        fid, num, title, topic, page, scenario, lp1, lp2, lp3, lp4 = item
        v = make_forum(fid, num, title, topic, page, scenario, lp1, lp2, lp3, lp4)
        variants.append(v)

    data = {
        "block": "schreiben_forum",
        "section": "schreiben-forum",
        "variants": variants
    }

    out_path = "quiz/data/schreiben_forum.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)

    print(f"OK: Generados {len(variants)} temas exhaustivos de Forumsbeitrag en {out_path}.")

if __name__ == "__main__":
    main()
