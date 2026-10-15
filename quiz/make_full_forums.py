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

def make_forum(fid, num, title, topic, page, scenario, colleague_post, lp1, lp2, lp3, lp4):
    return {
        "id": fid,
        "category": "forum",
        "kind": "schreiben",
        "label": f"Forumsbeitrag {num}: {title}",
        "topic": topic,
        "page": page,
        "scenario": scenario,
        "colleague_post": colleague_post,
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
        "Aufgrund eines vorübergehenden Einstellungsstopps und unbesetzter Stellen sollen alle Mitarbeiterinnen und Mitarbeiter in Ihrer Firma ab sofort zusätzliche Aufgaben übernehmen. Im Firmen-Intranet diskutieren die Kollegen darüber.",
        "Liebe Kolleginnen und Kollegen, die Geschäftsleitung bittet uns, zusätzliche Aufgaben zu übernehmen, weil keine neuen Leute eingestellt werden können. Ich finde das sehr problematisch, da wir jetzt schon an unserer Belastungsgrenze arbeiten! Wie seht ihr das? — Markus",
        "Äußern Sie Ihre Meinung zu der Übernahme zusätzlicher Aufgaben.",
        "Nennen Sie Vor- und Nachteile einer solchen vorübergehenden Mehrarbeit.",
        "Berichten Sie von Erfahrungen mit hoher Arbeitsbelastung an früheren Arbeitsplätzen.",
        "Schlagen Sie eine faire Lösung oder Entlastungsmaßnahmen für das Team vor."
    ),
    (
        "schr-f-02-krankmeldung", 2, "Ärztliche Krankmeldung ab dem 1. Tag", "Krankmeldung ab Tag 1", 98,
        "Bisher musste ein ärztliches Attest erst ab dem dritten Krankheitstag eingereicht werden. Nun plant die Geschäftsleitung, dass eine ärztliche Krankmeldung bereits ab dem ersten Fehltag vorgelegt werden muss, andernfalls gilt der Tag als unentschuldigte Fehlzeit.",
        "Hallo zusammen, ab sofort schon am ersten Tag zum Arzt zu müssen, halte ich für übertrieben. Bei einer leichten Erkältung braucht man doch vor allem Ruhe und sollte nicht stundenlang im überfüllten Wartezimmer sitzen! Was meint ihr dazu? — Sandra",
        "Äußern Sie Ihre Meinung zu der Verpflichtung eines Attests ab dem ersten Tag.",
        "Erläutern Sie Vor- und Nachteile dieser Neuregelung für Betrieb und Belegschaft.",
        "Beschreiben Sie, wie Krankmeldungen in Ihrem Heimatland oder früheren Betrieben gehandhabt werden.",
        "Machen Sie einen konstruktiven Vorschlag für eine praxistaugliche Regelung im Unternehmen."
    ),
    (
        "schr-f-03-jobticket-gehalt", 3, "Jobticket gegen Gehaltsverzicht", "Jobticket & Mobilität", 98,
        "Das Unternehmen bietet allen Beschäftigten ein kostenloses Jobticket für den öffentlichen Nahverkehr an. Im Gegenzug wird jedoch eine monatliche Eigenbeteiligung direkt vom Bruttogehalt einbehalten. Im Forum wird über die Vor- und Nachteile debattiert.",
        "Liebe Kolleginnen und Kollegen, die Idee mit dem Jobticket klingt im ersten Moment gut, aber wer ohnehin mit dem Fahrrad oder zu Fuß kommt, zahlt dann für etwas, das er gar nicht nutzt. Wir sollten das unbedingt diskutieren! — Thomas",
        "Äußern Sie Ihre Ansicht zu dem Angebot des Jobtickets mit Gehaltsabzug.",
        "Nennen Sie je zwei Vor- und Nachteile des Modells für verschiedene Mitarbeitergruppen.",
        "Erzählen Sie von Ihren eigenen täglichen Wegen zur Arbeit und Mobilitätserfahrungen.",
        "Formulieren Sie einen Vorschlag für ein freiwilliges und faires Ticketmodell."
    ),
    (
        "schr-f-04-zeitmanagement", 4, "Verpflichtender Workshop zum Zeitmanagement", "Weiterbildung & Arbeitsabläufe", 98,
        "Um Arbeitsabläufe effizienter zu gestalten, plant die Unternehmensführung einen obligatorischen zweitägigen Workshop zum Thema Zeitmanagement und Selbstorganisation für die gesamte Belegschaft.",
        "Hallo Team, die Geschäftsleitung möchte, dass wir alle an einem Zeitmanagement-Seminar teilnehmen. Manche von uns haben ihre Abläufe schon perfekt im Griff, andere könnten sicher profitieren. Brauchen wir wirklich alle diesen Workshop? — Sabine",
        "Äußern Sie Ihre Meinung zu der Verpflichtung für alle Mitarbeiter.",
        "Nennen Sie Vor- und Nachteile von internen Zeitmanagement-Schulungen.",
        "Berichten Sie, wie Sie Ihren Arbeitsalltag organisieren und Prioritäten setzen.",
        "Schlagen Sie alternative Methoden vor, um Arbeitsabläufe im Betrieb zu optimieren."
    ),
    (
        "schr-f-05-urlaubsplanung-kinder", 5, "Urlaubsplanung in den Sommerferien", "Urlaubsgerechtigkeit", 98,
        "Die Geschäftsleitung schlägt vor, dass in den sechs Wochen der Schulsommerferien vorrangig Kolleginnen und Kollegen mit schulpflichtigen Kindern Urlaub nehmen dürfen. Mitarbeiter ohne Kinder sollen auf andere Zeiten im Jahr ausweichen.",
        "Liebe Kollegen, natürlich verstehe ich, dass Eltern auf die Schulferien angewiesen sind. Aber auch wir ohne schulpflichtige Kinder haben Partner oder Hobbys, die an den Sommer gebunden sind. Eine strikte Bevorzugung finde ich nicht ganz fair. — Martin",
        "Nehmen Sie Stellung zu der Bevorzugung von Eltern bei der Sommerurlaubsplanung.",
        "Wägen Sie Vor- und Nachteile für die verschiedenen Interessengruppen im Betrieb ab.",
        "Berichten Sie von Ihren Erfahrungen mit Urlaubsabsprachen in Teams.",
        "Unterbreiten Sie einen Kompromissvorschlag für eine gerechte Urlaubsverteilung."
    ),
    (
        "schr-f-06-ueberstunden-stopp", 6, "Automatischer System-Logout gegen Überstunden", "Überstundenverbot / Work-Life-Balance", 98,
        "Um Überstunden konsequent zu verhindern und die Gesundheit zu schützen, plant die Geschäftsführung, die Computer aller Angestellten nach exakt acht Stunden Arbeitszeit automatisch zu sperren.",
        "Hallo zusammen, einerseits ist Feierabend wichtig, aber was passiert, wenn man gerade mitten in einem wichtigen Kundenkontakt oder einer dringenden Frist ist? Eine starre Zwangssperre nach 8 Stunden halte ich für unpraktisch! — Elena",
        "Äußern Sie Ihre Meinung zur automatischen Rechnersperre nach 8 Stunden.",
        "Diskutieren Sie Vor- und Nachteile einer strikten Begrenzung der Arbeitszeit.",
        "Schildern Sie Ihre persönlichen Erfahrungen mit Überstunden und Arbeitszeitregelungen.",
        "Schlagen Sie flexible Lösungen für den Umgang mit Mehrarbeit und Pausen vor."
    ),
    (
        "schr-f-07-privathandys", 7, "Aufbewahrung von Privathandys im Spind", "Smartphone-Nutzung am Arbeitsplatz", 98,
        "Aus Gründen der Konzentration und Produktivität plant das Management, dass alle privaten Smartphones während der Arbeitszeit im Spind bzw. Aufenthaltsraum eingeschlossen werden müssen. Private Telefonate sind nur noch in den Pausen gestattet.",
        "Liebe Kolleginnen und Kollegen, ständiges Handyklingeln nervt, klar. Aber was ist, wenn die Schule der Kinder anruft oder es einen familiären Notfall gibt? Eine totale Einschließung ist nicht mehr zeitgemäß. — Michael",
        "Äußern Sie Ihre Haltung zu dem Handyverbot am Arbeitsplatz.",
        "Nennen Sie Vor- und Nachteile dieser Maßnahme für Betriebsklima und Produktivität.",
        "Erzählen Sie, wie mit privaten Handys an früheren Arbeitsplätzen umgegangen wurde.",
        "Geben Sie eine konkrete Empfehlung für klare und verhältnismäßige Nutzungsregeln."
    ),

    # --- PÁGINA 99 ---
    (
        "schr-f-08-weiterbildung-wochenende", 8, "Weiterbildung am Wochenende (50 € Prämie)", "Betriebliche Fortbildung", 99,
        "Die Geschäftsführung möchte Fortbildungen künftig an Samstagen außerhalb der regulären Arbeitszeit durchführen. Die Firma zahlt die Seminarkosten und eine Prämie von 50 Euro, die Zeit investieren die Mitarbeiter in ihrer Freizeit.",
        "Hallo Team, Fortbildung ist super, aber das Wochenende gehört der Familie und der Erholung. 50 Euro wiegen einen verlorenen Samstag nicht auf. Was denkt ihr darüber? — Christian",
        "Äußern Sie Ihre Ansicht zu Fortbildungen am Wochenende mit Bonuszahlung.",
        "Nennen Sie Vor- und Nachteile von Schulungen in der Freizeit.",
        "Berichten Sie von eigenen Erfahrungen mit Weiterbildungsangeboten.",
        "Schlagen Sie alternative Modelle (z. B. Bildungsurlaub oder Hybridseminare) vor."
    ),
    (
        "schr-f-09-firmenumzug", 9, "Firmenumzug an einen neuen Standort", "Standortverlegung / Pendeln", 99,
        "Das Unternehmen plant, den Hauptsitz an einen etwa 30 km entfernten Standort mit moderneren Gebäuden zu verlegen. Die Firma bietet Umzugskostenzuschüsse und Unterstützung an. Im Intranet herrscht große Aufregung über die längeren Fahrtzeiten.",
        "Liebe Kollegen, der neue Standort mag modern sein, aber für viele von uns bedeutet das täglich zwei Stunden mehr Pendelzeit. Lohnt sich dieser Umzug wirklich für die Belegschaft? — Katrin",
        "Nehmen Sie Stellung zu den Plänen der Standortverlegung.",
        "Wägen Sie Vor- und Nachteile eines solchen Firmenumzugs ab.",
        "Beschreiben Sie Ihre eigenen Prioritäten bezüglich Arbeitsort und Pendelzeit.",
        "Machen Sie Vorschläge, wie das Unternehmen die betroffenen Mitarbeiter unterstützen kann."
    ),
    (
        "schr-f-10-parkplatz-kunden", 10, "Firmenparkplatz nur noch für Kunden", "Parkplatzordnung", 99,
        "Aufgrund wachsender Besucherzahlen sollen die Parkplätze auf dem Firmengelände ab nächstem Monat ausschließlich für Kunden reserviert sein. Angestellte sollen mit Bus und Bahn kommen oder öffentliche Parkhäuser gegen Gebühr nutzen.",
        "Hallo zusammen, nicht jeder von uns hat eine gute Busanbindung, gerade wer vom Land kommt, ist aufs Auto angewiesen. Wenn wir nicht mehr auf dem Firmengelände parken dürfen, wird der Arbeitsweg zum Albtraum! — Stefan",
        "Äußern Sie Ihre Meinung zum Wegfall der Mitarbeiterparkplätze.",
        "Nennen Sie Vor- und Nachteile der Maßnahme aus Sicht von Kunden und Personal.",
        "Erzählen Sie, wie die Parkplatzsituation an Ihren früheren Arbeitsorten geregelt war.",
        "Schlagen Sie ein faires Konzept vor (z. B. Parkplatz-Sharing oder Fahrgemeinschaften)."
    ),
    (
        "schr-f-11-soziale-netzwerke", 11, "Soziale Netzwerke zur internen Kommunikation", "Social Media am Arbeitsplatz", 99,
        "Die Abteilungsleitung schlägt vor, interne Absprachen und Projektupdates künftig über soziale Netzwerke und Messenger-Gruppen zu organisieren, um die Reaktionszeiten zu verkürzen.",
        "Liebe Kollegen, geschäftliche Chats auf privaten Social-Media-Plattformen vermischen Beruf und Privatleben viel zu sehr. Außerdem mache ich mir Sorgen um den Datenschutz! Was haltet ihr davon? — Laura",
        "Äußern Sie Ihre Meinung zur dienstlichen Nutzung privater sozialer Netzwerke.",
        "Nennen Sie Vor- und Nachteile von Messenger-Gruppen für die Zusammenarbeit.",
        "Berichten Sie von Ihren Erfahrungen mit digitaler Kommunikation im Team.",
        "Schlagen Sie sichere und datenschutzkonforme Alternativen für das Unternehmen vor."
    ),
    (
        "schr-f-12-fitnessstudio", 12, "Fitnessraum im Betrieb gegen Monatsgebühr", "Betriebliche Gesundheitsförderung", 99,
        "Im Keller des Firmengebäudes soll ein voll ausgestatteter Fitnessraum eingerichtet werden, den alle Mitarbeiter in den Pausen und nach Feierabend nutzen können. Dafür wird eine monatliche Gebühr von 15 Euro vom Gehalt einbehalten.",
        "Hallo Team, Sport direkt am Arbeitsplatz ist eine geniale Idee gegen Rückenschmerzen vom vielen Sitzen. Aber sollte so ein Angebot für die eigene Belegschaft nicht kostenlos sein? — Daniel",
        "Nehmen Sie Stellung zur Einrichtung eines firmeninternen Fitnessraums.",
        "Diskutieren Sie Vor- und Nachteile des Angebots und der Kostenbeteiligung.",
        "Schildern Sie eigene Erfahrungen mit sportlichen Angeboten im Beruf.",
        "Formulieren Sie einen Vorschlag für die Gestaltung und Finanzierung des Angebots."
    ),
    (
        "schr-f-13-erreichbarkeit", 13, "Betriebliche Erreichbarkeit nach Feierabend", "Erreichbarkeit / Work-Life-Balance", 99,
        "Wegen eines großen internationalen Kundenauftrags sollen alle Angestellten der Projektteams auch nach Feierabend und am Wochenende per E-Mail und Firmen-App erreichbar sein, um Verzögerungen zu vermeiden.",
        "Liebe Kollegen, ständige Erreichbarkeit führt direkt ins Burnout. Ein Feierabend muss ein echter Feierabend bleiben, sonst leidet auf Dauer unsere Gesundheit! Wie seht ihr diese Anforderung? — Frank",
        "Äußern Sie Ihre Haltung zur Erreichbarkeitspflicht außerhalb der Arbeitszeiten.",
        "Erläutern Sie die Vor- und Nachteile für das Projekt und das Wohlbefinden der Mitarbeiter.",
        "Berichten Sie von Ihren persönlichen Grenzen zwischen Freizeit und Beruf.",
        "Schlagen Sie eine geregelte Bereitschaftsregelung mit fairem Zeitausgleich vor."
    ),
    (
        "schr-f-14-vegan-kantine", 14, "Rein vegane Kantine mit 20 % Preisaufschlag", "Ernährung & Kantine", 99,
        "Um den CO2-Ausstoß des Betriebs zu senken, plant die Leitung, die Betriebskantine vollständig auf vegane Bio-Menüs umzustellen. Da Bio-Zutaten teurer sind, steigen die Preise der Gerichte um 20 %.",
        "Hallo zusammen, Nachhaltigkeit ist lobenswert, aber den Kollegen vorzuschreiben, was sie essen dürfen, und dafür auch noch 20 % mehr zu verlangen, sorgt für Riesenfrust in der Pause! — Anna",
        "Äußern Sie Ihre Meinung zur vollständigen Umstellung auf vegane Bio-Kost.",
        "Wägen Sie Vor- und Nachteile bezüglich Gesundheit, Kosten und Akzeptanz ab.",
        "Berichten Sie, wie Verpflegung an anderen Arbeitsplätzen organisiert ist.",
        "Schlagen Sie ein ausgewogenes Kantinenkonzept mit Wahlmöglichkeiten vor."
    ),

    # --- PÁGINA 100 ---
    (
        "schr-f-15-wochenendreise", 15, "Wochenendreise statt Weihnachtsfeier", "Teamevents & Feiern", 100,
        "Die Geschäftsleitung schlägt vor, die alljährliche traditionelle Weihnachtsfeier im Betrieb zu streichen. Stattdessen werden alle Mitarbeitenden mit ihren Familien zu einer gemeinsamen Wochenendreise in eine europäische Metropole eingeladen.",
        "Liebe Kolleginnen und Kollegen, eine Reise klingt verlockend, aber an einem Wochenende vor Weihnachten haben viele Verpflichtungen mit Verwandten. Eine Feier am Abend vor Ort wäre stressfreier! — Julia",
        "Nehmen Sie Stellung zu der geplanten Wochenendreise anstelle der Weihnachtsfeier.",
        "Nennen Sie Vor- und Nachteile einer solchen gemeinsamen Reise mit Familien.",
        "Berichten Sie von gelungenen Betriebsfeiern und Teamevents aus Ihrer Erfahrung.",
        "Machen Sie einen konkreten Vorschlag für das diesjährige Jahresabschluss-Event."
    ),
    (
        "schr-f-16-grossraumbuero", 16, "Umzug in ein offenes Großraumbüro", "Bürokonzepte / Open Space", 100,
        "Um die abteilungsübergreifende Zusammenarbeit und Kommunikation zu fördern, plant die Geschäftsführung, die bisherigen Einzel- und Zweierbüros aufzugeben und alle Teams in einem modernen Großraumbüro zusammenzufassen.",
        "Hallo Team, ich befürchte, dass die Geräuschkulisse im Großraumbüro jede konzentrierte Arbeit unmöglich macht. Ohne Rückzugsorte werden Fehler vorprogrammiert sein! Was denkt ihr? — Oliver",
        "Äußern Sie Ihre Meinung zum Konzept des Großraumbüros.",
        "Diskutieren Sie Vor- und Nachteile von Open-Space-Büros für die Arbeitsleistung.",
        "Beschreiben Sie Ihre ideale Arbeitsumgebung für konzentriertes Arbeiten.",
        "Schlagen Sie ein durchdachtes Raumkonzept (z. B. Ruhezonen, Meeting-Pods) vor."
    ),
    (
        "schr-f-17-mitarbeiter-des-jahres", 17, "Wahl zum «Mitarbeiter des Jahres» mit Prämie", "Mitarbeiteranerkennung", 100,
        "Die Firmenleitung beabsichtigt, eine jährliche Auszeichnung «Mitarbeiter des Jahres» einzuführen. Der Gewinner oder die Gewinnerin erhält eine finanzielle Prämie und eine öffentliche Ehrung.",
        "Liebe Kollegen, ein Einzelsieger fördert doch nur Ellenbogenmentalität und Neid im Team. Gute Arbeit ist bei uns immer Teamleistung und kein Sololauf! Was meint ihr dazu? — Monika",
        "Äußern Sie Ihre Ansicht zur Einführung einer solchen Auszeichnung.",
        "Nennen Sie Vor- und Nachteile von individuellen Leistungsanreizen im Betrieb.",
        "Berichten Sie von Belohnungssystemen und Motivation an früheren Arbeitsstellen.",
        "Schlagen Sie alternative Modelle zur Teamanerkennung und Wertschätzung vor."
    ),
    (
        "schr-f-18-spanischkurs", 18, "Verpflichtender Spanischkurs nach Feierabend", "Sprachförderung & Internationalisierung", 100,
        "Da das Unternehmen eine neue Niederlassung in Spanien eröffnet, sollen alle Angestellten verpflichtet werden, zweimal wöchentlich nach Feierabend an einem firmeneigenen Spanischkurs teilzunehmen.",
        "Hallo zusammen, Sprachkenntnisse sind ein toller Vorteil, aber nach acht Stunden anstrengender Arbeit noch Grammatik zu pauken, überfordert viele. Solche Kurse sollten während der Arbeitszeit stattfinden! — Bernd",
        "Nehmen Sie Stellung zu dem verpflichtenden Sprachkurs nach Arbeitsende.",
        "Wägen Sie Vor- und Nachteile für die persönliche und berufliche Entwicklung ab.",
        "Erzählen Sie von Ihren Erfahrungen beim Erlernen von Fremdsprachen für den Beruf.",
        "Unterbreiten Sie einen Vorschlag für flexible Lernzeiten oder Online-Module."
    ),
    (
        "schr-f-19-auslandsdienst", 19, "6-monatiger Auslandsdienst zur Einarbeitung", "Auslandseinsatz / Mobilität", 100,
        "Für die Eröffnung eines Standorts in Italien soll jede Abteilung eine Fachkraft auswählen, die für sechs Monate dorthin entsendet wird, um die neuen Kollegen vor Ort einzuarbeiten.",
        "Liebe Kolleginnen und Kollegen, ein Auslandseinsatz ist eine riesige Chance, aber für Kolleginnen und Kollegen mit Familie oder pflegebedürftigen Angehörigen kaum machbar. Wie sollte die Auswahl erfolgen? — Sven",
        "Äußern Sie Ihre Haltung zu der sechsmonatigen Entsendung von Mitarbeitern.",
        "Nennen Sie Vor- und Nachteile eines solchen Auslandseinsatzes.",
        "Berichten Sie von Ihren Erfahrungen mit interkultureller Arbeit und Auslandsaufenthalten.",
        "Schlagen Sie Kriterien für eine faire und freiwillige Auswahl der Entsendeten vor."
    ),
    (
        "schr-f-20-firmenkita-247", 20, "24/7 Firmen-Kita für Schichtarbeiter", "Betriebliche Kinderbetreuung", 100,
        "Um Mitarbeitende im Schichtdienst zu entlasten, plant die Unternehmensleitung eine werkseigene Kindertagesstätte mit einer 24-Stunden-Rundumbetreuung auf dem Betriebsgelände einzurichten.",
        "Hallo Team, für alle, die in der Nacht- oder Frühschicht arbeiten, wäre eine betriebsnahe Kita eine unglaubliche Erleichterung! Einige sorgen sich jedoch um die Kosten und die kindliche Entwicklung nachts. Was denkt ihr? — Melanie",
        "Äußern Sie Ihre Meinung zur Einrichtung einer 24h-Betriebskita.",
        "Diskutieren Sie Vor- und Nachteile flexibler Betreuungsangebote für Eltern und Betrieb.",
        "Schildern Sie die Vereinbarkeit von Beruf und Familie aus Ihrer eigenen Erfahrung.",
        "Machen Sie Vorschläge für die konkrete Umsetzung und pädagogische Gestaltung."
    ),
    (
        "schr-f-21-kantinenschliessung", 21, "Schließung der Kantine und Essensmarken", "Verpflegung & Betriebsklima", 100,
        "Aufgrund gestiegener Betriebskosten soll die eigene Kantine geschlossen werden. Stattdessen erhalten alle Angestellten Essensmarken (Gutscheine) für nahegelegene Bäckereien und Restaurants.",
        "Liebe Kollegen, die Kantine war nicht nur ein Ort zum Essen, sondern unser zentraler Treffpunkt für den informellen Austausch zwischen den Abteilungen. Mit Essensmarken zerstreut sich das ganze Team! — Claudia",
        "Nehmen Sie Stellung zur Schließung der Firmenkantine zugunsten von Essensmarken.",
        "Nennen Sie Vor- und Nachteile von Essensgutscheinen im Vergleich zu einer Kantine vor Ort.",
        "Berichten Sie von der Mittagspausenkultur an Ihren bisherigen Arbeitsplätzen.",
        "Schlagen Sie Alternativen vor, um Verpflegung und sozialen Zusammenhalt zu sichern."
    ),

    # --- PÁGINA 101 ---
    (
        "schr-f-22-urlaubstage-jahresende", 22, "Urlaubsverfall: Alle Tage bis Jahresende nehmen", "Urlaubsregelung", 101,
        "Die Personalabteilung hat angekündigt, dass Resturlaub künftig nicht mehr in das Folgejahr übertragen werden darf. Alle Urlaubstage müssen bis zum 31. Dezember vollständig genommen werden, sonst verfallen sie ersatzlos.",
        "Hallo zusammen, gerade im Dezember herrscht bei uns Hochbetrieb. Wenn jetzt alle gleichzeitig ihren Resturlaub nehmen müssen, bricht das operative Geschäft zusammen! Das ist völlig weltfremd. — Patrick",
        "Äußern Sie Ihre Ansicht zur strikten Frist für den Urlaub bis Jahresende.",
        "Erläutern Sie die Vor- und Nachteile für die Personalplanung und die Mitarbeiter.",
        "Berichten Sie, wie Urlaubsübertragungen in Ihrem Heimatland geregelt sind.",
        "Schlagen Sie eine flexiblere Übergangsfrist für Resturlaub vor."
    ),
    (
        "schr-f-23-byod-verbot", 23, "Verbot privater Geräte am Arbeitsplatz (BYOD-Verbot)", "IT-Sicherheit / Datenschutz", 101,
        "Aus Gründen der Cyber-Sicherheit und des Datenschutzes verbietet die IT-Leitung ab sofort die Nutzung jeglicher privater Laptops, Tablets, Smartphones und USB-Sticks am Arbeitsplatz und im Firmen-WLAN.",
        "Liebe Kollegen, Sicherheit geht vor, das verstehe ich. Aber viele von uns nutzen private Tablets für schnelle Recherchen oder Notizen. Wird unsere tägliche Arbeit dadurch nicht unnötig verlangsamt? — Sebastian",
        "Äußern Sie Ihre Meinung zum Verbot privater Hardware im Unternehmen.",
        "Wägen Sie Sicherheitsaspekte gegen Arbeitsflexibilität und Komfort ab.",
        "Erzählen Sie von Ihren Erfahrungen mit Datenschutz und Sicherheitsregeln im Betrieb.",
        "Unterbreiten Sie einen Vorschlag für einen sicheren und modernen Mittelweg."
    ),
    (
        "schr-f-24-samstagsarbeit", 24, "Verpflichtende Samstagsarbeit zweimal pro Jahr", "Arbeitszeit & Wochenendarbeit", 101,
        "Für die jährliche Großinventur und das Software-Update plant das Unternehmen, alle Angestellten zweimal im Jahr an Samstagen zur Arbeit zu verpflichten. Als Ausgleich gibt es Freizeitausgleich an Werktagen.",
        "Hallo Team, zwei Samstage im Jahr klingen zunächst machbar, aber viele haben Wochenend-Verpflichtungen oder Nebenjobs. Sollte so etwas nicht auf freiwilliger Basis mit Zuschlag geregelt werden? — Miriam",
        "Nehmen Sie Stellung zur Verpflichtung zu zwei Samstagsdiensten pro Jahr.",
        "Nennen Sie Vor- und Nachteile für das Unternehmen und das Privatleben.",
        "Berichten Sie von Erfahrungen mit Samstags- oder Schichtarbeit.",
        "Schlagen Sie ein freiwilliges Bonussystem für Wochenendeinsätze vor."
    ),
    (
        "schr-f-25-erste-hilfe", 25, "Verpflichtende Erste-Hilfe-Kurse für alle", "Arbeitssicherheit & Gesundheit", 101,
        "Die Geschäftsleitung beschließt, dass alle Mitarbeiterinnen und Mitarbeiter alle zwei Jahre einen ganztägigen Erste-Hilfe-Kurs während der Arbeitszeit absolvieren müssen, um die Betriebssicherheit zu erhöhen.",
        "Liebe Kolleginnen und Kollegen, Lebensrettung geht uns alle an, nicht nur die offiziellen Ersthelfer. Ich finde die Idee klasse, aber manche Kollegen befürchten, dass dadurch wichtige Arbeitszeit verloren geht. Was meint ihr? — Heike",
        "Äußern Sie Ihre Haltung zur Erste-Hilfe-Schulung für die gesamte Belegschaft.",
        "Diskutieren Sie den Nutzen für die Sicherheit im Betrieb gegen den zeitlichen Aufwand.",
        "Schildern Sie eigene Erfahrungen mit Notfallsituationen oder Schulungen.",
        "Geben Sie Empfehlungen für eine effiziente und praxisnahe Durchführung der Kurse."
    ),
    (
        "schr-f-26-firmenhandy-bereitschaft", 26, "Diensthandy mit Bereitschaftspflicht", "Diensthandy & Freizeit", 101,
        "Alle Beschäftigten sollen ein modernes Firmen-Smartphone erhalten. Im Gegenzug wird erwartet, dass wichtige Anrufe und Nachrichten auch an Samstagen und Feiertagen zeitnah beantwortet werden.",
        "Hallo zusammen, ein kostenloses Firmenhandy ist verlockend, aber die ständige Erwartung, am Wochenende ranzugehen, zerstört jede Erholung. Das ist die schleichende Aushöhlung des Arbeitszeitgesetzes! — Dirk",
        "Äußern Sie Ihre Meinung zur Koppelung von Firmenhandy und Wochenendbereitschaft.",
        "Nennen Sie Vor- und Nachteile von Diensthandys für Arbeitnehmer.",
        "Berichten Sie von Ihrem persönlichen Umgang mit dienstlicher Erreichbarkeit.",
        "Schlagen Sie klare Abschaltzeiten und geregelte Vertretungspläne vor."
    ),
    (
        "schr-f-27-dienstkleidung", 27, "Verpflichtende Dienstkleidung in Firmenfarben", "Corporate Identity / Dresscode", 101,
        "Um ein einheitliches Erscheinungsbild gegenüber Kunden zu gewährleisten, sollen alle Mitarbeiterinnen und Mitarbeiter künftig einheitliche Poloshirts und Hosen in den Firmenfarben Weiß und Rot tragen.",
        "Liebe Kollegen, im Lager oder Service mag Dienstkleidung sinnvoll sein, aber in der Buchhaltung und IT sieht uns doch gar kein Kunde! Ich möchte mich am Arbeitsplatz individuell und wohl fühlen. Was denkt ihr? — Andreas",
        "Nehmen Sie Stellung zu der Pflicht von Dienstkleidung in Firmenfarben.",
        "Wägen Sie Einheitlichkeit und Markenauftritt gegen persönliche Freiheit ab.",
        "Berichten Sie von Kleidungsvorschriften an früheren Arbeitsstellen.",
        "Formulieren Sie einen Kompromiss (z. B. nur bei direktem Kundenkontakt)."
    ),

    # --- PÁGINA 102 ---
    (
        "schr-f-28-bueromoebel-ergonomie", 28, "Ergonomische Büromöbel und Stehtische", "Gesundheit am Arbeitsplatz", 102,
        "Das Unternehmen erwägt eine Großinvestition in elektrische Steh-Sitz-Tische und ergonomische Stühle für alle Bildschirmarbeitsplätze, um Haltungsschäden und Krankheitsausfällen vorzubeugen.",
        "Hallo Team, endlich tut die Firma etwas für unsere Rücken! Allerdings gibt es Stimmen, die das Geld lieber in Gehaltserhöhungen oder Weiterbildung investiert sehen würden. Wie steht ihr dazu? — Nicole",
        "Äußern Sie Ihre Meinung zur Anschaffung ergonomischer Büromöbel.",
        "Nennen Sie Vor- und Nachteile dieser gesundheitlichen Investition.",
        "Berichten Sie von Ihren Erfahrungen mit körperlicher Belastung am Schreibtisch.",
        "Schlagen Sie zusätzliche Maßnahmen zur Förderung der Mitarbeitergesundheit vor."
    ),
    (
        "schr-f-29-gesundheitscheck", 29, "Jährlicher Gesundheitscheck auf Firmenkosten", "Betriebsärztliche Vorsorge", 102,
        "Einmal pro Jahr soll allen Beschäftigten während der Arbeitszeit ein freiwilliger, umfassender Gesundheits-Check-up durch den Betriebsarzt angeboten werden. Die Kosten übernimmt vollständig das Unternehmen.",
        "Liebe Kolleginnen und Kollegen, Vorsorgeuntersuchungen sind enorm wichtig, aber einige Kollegen haben Bedenken, dass vertrauliche Gesundheitsdaten an die Personalabteilung gelangen könnten. Was meint ihr? — Svenja",
        "Äußern Sie Ihre Ansicht zu dem betrieblichen Gesundheitscheck.",
        "Diskutieren Sie Chancen für die Prävention und Bedenken bezüglich des Datenschutzes.",
        "Erzählen Sie von medizinischer Vorsorge in Ihrem Heimatland.",
        "Machen Sie Vorschläge für die Wahrung der strikten ärztlichen Schweigepflicht."
    ),
    (
        "schr-f-30-firmenchat-slack", 30, "Einführung eines firmenweiten Instant-Chats", "Interne Kommunikation", 102,
        "Um die zeitraubende E-Mail-Flut einzudämmen, soll für das gesamte Unternehmen ein moderner Instant-Messaging-Dienst (wie Slack oder Teams) als Standard-Kommunikationskanal eingeführt werden.",
        "Hallo zusammen, Chat-Nachrichten sind schnell und unkompliziert. Ich habe allerdings die Sorge, dass man durch ständige Benachrichtigungen alle zwei Minuten aus der Arbeit gerissen wird! — Florian",
        "Nehmen Sie Stellung zur Einführung eines internen Chat-Tools anstelle von E-Mails.",
        "Wägen Sie Schnelligkeit gegen Ablenkung und Informationsüberflutung ab.",
        "Berichten Sie von Ihren bevorzugten Kommunikationswegen bei der Arbeit.",
        "Schlagen Sie klare Kommunikationsregeln (z. B. feste Ruhezeiten) vor."
    ),
    (
        "schr-f-31-papierlose-abrechnung", 31, "Rein papierlose Lohnabrechnung im Online-Portal", "Digitalisierung & Umwelt", 102,
        "Aus Umweltschutz- und Kostengründen stellt die Personalabteilung die monatlichen Gehaltsabrechnungen ab dem nächsten Quartal nicht mehr in Papierform per Post zu, sondern ausschließlich digital über ein Mitarbeiterportal.",
        "Liebe Kollegen, Papier zu sparen ist absolut richtig. Doch nicht jeder Kollege im Werk hat zu Hause einen Drucker oder kennt sich mit Online-Portalen sicher aus. Ist das für alle zumutbar? — Kerstin",
        "Äußern Sie Ihre Haltung zur Umstellung auf rein digitale Abrechnungen.",
        "Nennen Sie Vor- und Nachteile der Digitalisierung der Personaldokumente.",
        "Berichten Sie von Ihren Erfahrungen mit Online-Behörden und digitalen Portalen.",
        "Schlagen Sie Hilfsangebote und Schulungen für weniger technikaffine Kollegen vor."
    ),
    (
        "schr-f-32-zigarettenpause", 32, "Zigarettenpausen nur noch mit Ausstempeln", "Pausenregelung & Gleichbehandlung", 102,
        "Aus Gründen der Gleichbehandlung von Rauchern und Nichtrauchern plant die Geschäftsführung, dass für jede Zigarettenpause zwingend ausgestempelt werden muss. Die Fehlzeiten müssen nachgearbeitet werden.",
        "Hallo Team, Nichtraucher arbeiten durch, während Raucher mehrmals täglich für zehn Minuten verschwinden. Dass diese Zeit nachgearbeitet werden soll, finde ich nur fair. Trotzdem gibt es hitzige Diskussionen. Was denkt ihr? — Jan",
        "Äußern Sie Ihre Meinung zur Zeiterfassungspflicht bei Raucherpausen.",
        "Diskutieren Sie Vor- und Nachteile für das Betriebsklima und die Gerechtigkeit.",
        "Schildern Sie Regelungen zu Raucherpausen aus Ihren früheren Erfahrungen.",
        "Machen Sie einen Vorschlag für eine einvernehmliche und gesunde Pausenregelung."
    ),

    # --- PÁGINA 103 ---
    (
        "schr-f-33-obstkorb", 33, "Frisches Bio-Obst im Büro für 5 € monatlich", "Gesunde Ernährung im Büro", 103,
        "Die Firma plant, wöchentlich frische Bio-Obstkörbe in allen Teeküchen aufzustellen. Um die Kosten zu decken, soll jeder Mitarbeitende einen symbolischen Betrag von 5 Euro pro Monat beisteuern.",
        "Liebe Kollegen, frische Äpfel und Bananen am Arbeitsplatz sind ein toller Vitaminschub. Aber warum übernimmt ein profitables Unternehmen diese 5 Euro nicht komplett als Geste der Wertschätzung? — Carsten",
        "Äußern Sie Ihre Ansicht zur Obstkorb-Initiative und der Kostenbeteiligung.",
        "Wägen Sie die gesundheitlichen Vorteile gegen den monatlichen Eigenanteil ab.",
        "Berichten Sie von Verpflegungsangeboten an früheren Arbeitsstellen.",
        "Schlagen Sie eine faire Finanzierung oder Sponsoring durch den Betrieb vor."
    ),
    (
        "schr-f-34-glaswaende", 34, "Transparente Bürowände aus Glas", "Arbeitsplatzgestaltung", 103,
        "Im Rahmen der Renovierung sollen alle Trennwände zwischen den Abteilungen und Gängen aus transparentem Glas gebaut werden, um Licht, Modernität und offene Kommunikation zu symbolisieren.",
        "Hallo zusammen, Glaswände sehen im Katalog schick aus, aber man fühlt sich wie im Aquarium unter ständiger Beobachtung. Wo bleibt da die Privatsphäre bei vertraulichen Telefonaten? — Bettina",
        "Nehmen Sie Stellung zum Einbau transparenter Glaswände im Büro.",
        "Diskutieren Sie Vor- und Nachteile von optischer Offenheit versus Privatsphäre.",
        "Beschreiben Sie, wie Ihre ideale Büroaufteilung aussehen sollte.",
        "Schlagen Sie Lösungen vor (z. B. Sichtschutzfolien oder Vorhänge nach Bedarf)."
    ),
    (
        "schr-f-35-clean-desk", 35, "Clean-Desk-Policy: Schreibtisch täglich komplett leeren", "Ordnung am Arbeitsplatz", 103,
        "Ab kommendem Monat gilt eine strikte Clean-Desk-Policy: Vor Verlassen des Büros müssen alle Akten, Notizen und persönlichen Gegenstände weggeschlossen werden, sodass der Schreibtisch völlig leer ist.",
        "Liebe Kolleginnen und Kollegen, aufgeräumte Büros sind für den Datenschutz gut, aber ein persönliches Foto der Familie oder eine Zimmerpflanze machen den Schreibtisch doch erst menschlich! Was meint ihr dazu? — Holger",
        "Äußern Sie Ihre Haltung zur strikten Clean-Desk-Regel.",
        "Nennen Sie Vor- und Nachteile für Datenschutz, Ordnung und Wohlbefinden.",
        "Erzählen Sie, wie an Ihrem Arbeitsplatz mit Dokumenten und Ordnung verfahren wird.",
        "Schlagen Sie praxistaugliche Regeln vor, die Sicherheit und Gemütlichkeit verbinden."
    ),
    (
        "schr-f-36-englisch-firmensprache", 36, "Englisch als verbindliche Firmensprache", "Sprachregelung & Internationalität", 103,
        "Um sich für internationale Kunden und Fachkräfte zu öffnen, plant die Geschäftsleitung, Englisch als offizielle Arbeitssprache für alle Meetings, E-Mails und Protokolle im Betrieb einzuführen.",
        "Hallo Team, internationale Ausrichtung ist wichtig, aber viele langjährige Kollegen sprechen kein fließendes Englisch. Wenn jetzt alles auf Englisch läuft, schließen wir wertvolle Mitarbeiter aus! — Dagmar",
        "Äußern Sie Ihre Meinung zur Einführung von Englisch als alleiniger Firmensprache.",
        "Wägen Sie internationale Wettbewerbsfähigkeit gegen Sprachbarrieren im Team ab.",
        "Berichten Sie von Ihren eigenen Erfahrungen mit Fremdsprachen im Arbeitsumfeld.",
        "Schlagen Sie ein schrittweises Modell mit gezielter Sprachförderung vor."
    ),
    (
        "schr-f-37-essverbot-schreibtisch", 37, "Essverbot am Schreibtisch und Computer", "Hygiene & Pausenkultur", 103,
        "Wegen Krümeln in den Tastaturen und Essensgerüchen in den Büroräumen verbietet die Geschäftsleitung ab sofort den Verzehr von Mahlzeiten und Snacks am Bildschirmarbeitsplatz.",
        "Liebe Kollegen, ein Schnitzel am Schreibtisch muss nicht sein, aber darf man jetzt nicht mal mehr einen Apfel oder ein Brötchen essen, während man eine lange E-Mail liest? Das geht zu weit! — Ralf",
        "Nehmen Sie Stellung zum Verbot von Snacks und Essen am Arbeitsplatz.",
        "Diskutieren Sie Vor- und Nachteile bezüglich Hygiene, Geruch und Flexibilität.",
        "Schildern Sie die Pausengewohnheiten an Ihren früheren Arbeitsplätzen.",
        "Machen Sie Vorschläge für eine saubere und dennoch praxisnahe Regelung."
    ),

    # --- PÁGINA 104 ---
    (
        "schr-f-38-konfliktmanagement", 38, "Verpflichtendes Konfliktmanagement-Seminar", "Teamentwicklung & Zusammenarbeit", 104,
        "Nach mehreren internen Spannungen zwischen Abteilungen ordnet die Geschäftsführung ein verpflichtendes zweitägiges Konfliktmanagement- und Deeskalationstraining für alle Mitarbeiter an.",
        "Hallo zusammen, Konflikte müssen gelöst werden, keine Frage. Aber ob ein verordnetes Pflichtseminar wirklich tiefsitzende Reibungen löst, bezweifle ich. Oft sorgt so etwas für noch mehr Unmut. — Tanja",
        "Äußern Sie Ihre Ansicht zu dem verordneten Konfliktlösungs-Training.",
        "Nennen Sie Vor- und Nachteile von verpflichtenden psychologischen Teamtrainings.",
        "Berichten Sie von Ihren Erfahrungen mit Konfliktlösungen im beruflichen Alltag.",
        "Schlagen Sie alternative, wirksame Wege zur Verbesserung des Betriebsklimas vor."
    ),
    (
        "schr-f-39-dienstrad", 39, "Dienstrad-Leasing und Reparaturzuschuss", "Nachhaltige Mobilität", 104,
        "Die Firma führt ein Dienstrad-Programm ein: Jeder Mitarbeitende kann über Gehaltsumwandlung ein hochwertiges Fahrrad oder E-Bike leasen und erhält jährlich 100 Euro Zuschuss zu Inspektion und Reparatur.",
        "Liebe Kolleginnen und Kollegen, das ist ein fantastisches Signal für Umwelt und Fitness! Doch wie steht es um sichere Stellplätze und Duschen bei uns im Gebäude? Das muss bedacht werden! — Tobias",
        "Nehmen Sie Stellung zu dem Dienstrad-Leasingangebot der Firma.",
        "Diskutieren Sie die Vor- und Nachteile für die Gesundheit, die Umwelt und den Betrieb.",
        "Erzählen Sie von Ihren eigenen Mobilitätsgewohnheiten auf dem Weg zur Arbeit.",
        "Schlagen Sie begleitende Maßnahmen (z. B. überdachte Abstellanlagen, Ladestationen) vor."
    ),
    (
        "schr-f-40-sommerkleidung-kurz", 40, "Verbot kurzer Kleidung bei Sommerhitze", "Dresscode bei Hitze", 104,
        "Trotz sommerlicher Temperaturen von über 30 Grad erinnert die Geschäftsleitung daran, dass kurze Hosen, Sandalen und ärmellose Shirts im gesamten Unternehmen strikt untersagt sind.",
        "Hallo Team, wir schwitzen in den nicht klimatisierten Büros, sollen aber in langen Hosen und geschlossenen Schuhen arbeiten. Wenn kein Kundenkontakt besteht, sollte lockere Kleidung erlaubt sein! — Philipp",
        "Äußern Sie Ihre Meinung zum Verbot von leichter Sommerkleidung.",
        "Wägen Sie professionelles Auftreten gegen Gesundheit und Wohlbefinden bei Hitze ab.",
        "Berichten Sie von Kleidungsvorschriften im Sommer in Ihrem Heimatland.",
        "Schlagen Sie eine hitzeangepasste Kleiderordnung für die Sommermonate vor."
    ),
    (
        "schr-f-41-azubi-betreuung", 41, "Patenschaften: Jeder Mitarbeiter betreut Auszubildende", "Ausbildung & Nachwuchsförderung", 104,
        "Um die Ausbildungsqualität zu verbessern, soll jeder feste Mitarbeiter künftig für jeweils drei Monate die persönliche Patenschaft für einen Auszubildenden übernehmen und ihn intensiv im Alltag anleiten.",
        "Liebe Kollegen, junge Menschen auszubilden ist eine lohnende Aufgabe. Aber neben dem normalen Tagesgeschäft fehlt oft die Zeit für eine sorgfältige Betreuung. Werden unsere Ziele angepasst? — Andrea",
        "Nehmen Sie Stellung zu dem verpflichtenden Patenschafts-Modell.",
        "Nennen Sie Vor- und Nachteile für Auszubildende und erfahrene Mitarbeiter.",
        "Berichten Sie von Ihren eigenen Erfahrungen während der Ausbildung oder Einarbeitung.",
        "Unterbreiten Sie Vorschläge für Schulungen und Zeitanrechnungen für die Paten."
    ),
    (
        "schr-f-42-pausenhof-garten", 42, "Grüner Pausenhof statt Firmenparkplatz", "Betriebsgelände & Erholung", 104,
        "Die Geschäftsleitung schlägt vor, die Hälfte der bisherigen Parkplätze auf dem Firmengelände abzureißen und in einen begrünten Erholungsgarten mit Sitzbänken für die Mittagspause umzuwandeln.",
        "Hallo zusammen, ein Garten mit Bäumen für die Pause wäre wunderschön. Aber wo sollen dann die Kollegen parken, die jeden Tag von auswärts mit dem Auto anreisen müssen? — Marcel",
        "Äußern Sie Ihre Meinung zum Umbau der Parkplätze in einen Erholungshof.",
        "Wägen Sie Erholungswert und Klimaschutz gegen den Verlust von Stellplätzen ab.",
        "Beschreiben Sie, wie Sie Ihre Mittagspausen am liebsten verbringen.",
        "Schlagen Sie einen Kompromiss vor, der Grünflächen und Parkmöglichkeiten vereint."
    ),
    (
        "schr-f-43-dienstreisen-online", 43, "Kurze Dienstreisen nur noch virtuell", "Reiserichtlinie & Klimaschutz", 104,
        "Aus Kosten- und Umweltschutzgründen sollen alle innerdeutschen Dienstreisen unter 300 km gestrichen werden. Besprechungen mit Kunden und Partnern dürfen nur noch per Videokonferenz stattfinden.",
        "Liebe Kolleginnen und Kollegen, Videokonferenzen sparen enorm viel Zeit und Stress. Doch manche Kunden erwarten das persönliche Händeschütteln, um Vertrauen aufzubauen. Was verliert man dadurch? — Jürgen",
        "Nehmen Sie Stellung zu der Pflicht, kurze Dienstreisen virtuell durchzuführen.",
        "Diskutieren Sie Vor- und Nachteile von Online-Meetings im Kundenkontakt.",
        "Berichten Sie von eigenen Erfahrungen mit Dienstreisen und Videocalls.",
        "Schlagen Sie Kriterien vor, wann ein persönliches Treffen weiterhin erlaubt sein sollte."
    ),
    (
        "schr-f-44-baumpflanzen", 44, "Gemeinsame Baumpflanz-Aktion im Stadtwald", "Corporate Social Responsibility", 104,
        "Die Geschäftsleitung lädt alle Angestellten ein, an einem Freitag an einer gemeinsamen Baumpflanz-Aktion im Stadtwald teilzunehmen. Der Tag gilt als voll bezahlte Arbeitszeit.",
        "Hallo Team, sich aktiv für den Klimawald vor Ort einzusetzen und dabei die Kollegen mal ganz anders kennenzulernen, finde ich großartig. Wer von euch ist dabei? — Sarah",
        "Äußern Sie Ihre Meinung zu dem bezahlten Umwelttag im Stadtwald.",
        "Nennen Sie Vor- und Nachteile solcher gemeinnützigen Firmenaktionen.",
        "Berichten Sie von Umwelt- und Nachhaltigkeitsprojekten, an denen Sie teilgenommen haben.",
        "Schlagen Sie weitere nachhaltige Ideen für den betrieblichen Alltag vor."
    ),

    # --- PÁGINA 105 ---
    (
        "schr-f-45-betriebsausflug-samstag", 45, "Pflicht-Betriebsausflug am Samstag", "Teambuilding & Freizeit", 105,
        "Der diesjährige Betriebsausflug soll an einem Samstag stattfinden, wobei die Teilnahme für alle Mitarbeiter verpflichtend ist. Als Ausgleich gewährt das Unternehmen einen freien Tag innerhalb der nächsten zwei Wochen.",
        "Liebe Kollegen, ein freier Tag unter der Woche ist nett, aber das Wochenende ist für viele heilig für Kinder und Hobbys. Kann ein Teamausflug Pflicht sein, wenn er auf den Samstag fällt? — Dominik",
        "Nehmen Sie Stellung zur Verpflichtung zu einem Wochenend-Betriebsausflug.",
        "Wägen Sie Teambildung gegen den Eingriff in das private Wochenende ab.",
        "Berichten Sie von Betriebsausflügen und Firmenfeiern an früheren Arbeitsstellen.",
        "Schlagen Sie eine flexiblere oder freiwillige Gestaltung des Ausflugs vor."
    ),
    (
        "schr-f-46-kamera-pflicht", 46, "Kamera-Pflicht bei allen Online-Meetings", "Videokonferenzen / Netiquette", 105,
        "Die Unternehmensführung führt die Regel ein, dass während aller internen Online-Besprechungen die Webcam dauerhaft eingeschaltet sein muss, um die Aufmerksamkeit und Zusammenarbeit zu verbessern.",
        "Hallo zusammen, stundenlang in die Kamera starren zu müssen führt zur berüchtigten Zoom-Müdigkeit. Außerdem fühlt man sich im Homeoffice in seiner Privatsphäre kontrolliert. Wie seht ihr das? — Miriam",
        "Äußern Sie Ihre Meinung zur dauerhaften Kamera-Pflicht in Online-Meetings.",
        "Diskutieren Sie Vor- und Nachteile von eingeschalteten Kameras für die Meeting-Kultur.",
        "Schildern Sie Ihre eigenen Erfahrungen und Gewohnheiten bei Videokonferenzen.",
        "Formulieren Sie Regeln für eine respektvolle und zweckmäßige Kameranutzung."
    ),
    (
        "schr-f-47-urlaubssperre-praemie", 47, "Urlaubssperre im August/September mit 500 € Bonus", "Urlaubssperre & Belastung", 105,
        "Wegen eines überraschenden Großauftrags verhängt die Geschäftsleitung eine Urlaubssperre für die Monate August und September. Als Entschädigung zahlt die Firma jedem Beschäftigten eine Prämie von 500 Euro.",
        "Liebe Kolleginnen und Kollegen, 500 Euro sind ein schönes Geld, aber gebuchte Familienurlaube kurzfristig zu stornieren, verursacht riesigen Ärger zu Hause. Ist diese Urlaubssperre verhältnismäßig? — Thorsten",
        "Nehmen Sie Stellung zu der kurzfristigen Urlaubssperre mit finanzieller Entschädigung.",
        "Wägen Sie geschäftliche Dringlichkeit gegen die Erholungsbedürfnisse der Mitarbeiter ab.",
        "Berichten Sie von Situationen mit hohem Arbeitsaufkommen und Termindruck.",
        "Schlagen Sie Alternativen (z. B. studentische Aushilfen oder Projektprämien) vor."
    ),
    (
        "schr-f-48-ueberstunden-freizeit", 48, "Überstundenausgleich ausschließlich in Freizeit", "Überstundenvergütung", 105,
        "Aufgrund geänderter Vergütungsrichtlinien können geleistete Überstunden ab sofort nicht mehr finanziell ausbezahlt werden. Mehrarbeit kann ausschließlich in Form von Freizeit (Gleittagen) abgebaut werden.",
        "Hallo Team, viele von uns haben sich durch Überstundenauszahlungen ein willkommenes Zusatzeinkommen erwirtschaftet. Der reine Freizeitausgleich nimmt uns diese finanzielle Flexibilität! — Lars",
        "Äußern Sie Ihre Ansicht zur Streichung der Überstundenauszahlung.",
        "Nennen Sie Vor- und Nachteile von Freizeitausgleich im Vergleich zu Geldvergütung.",
        "Berichten Sie, wie Überstunden an Ihren früheren Arbeitsplätzen geregelt wurden.",
        "Schlagen Sie ein Wahlmodell zwischen Freizeitausgleich und Auszahlung vor."
    ),
    (
        "schr-f-49-kurzarbeit", 49, "Kurzarbeit um 50 % wegen Auftragsmangel", "Krisenmanagement & Kurzarbeit", 105,
        "Wegen der schwierigen Wirtschaftslage plant die Unternehmensführung, für die nächsten sechs Monate Kurzarbeit anzumelden. Die Arbeitszeit und das Gehalt werden um 50 % reduziert, um Entlassungen zu vermeiden.",
        "Liebe Kollegen, Kurzarbeit ist ein schwerer Schlag für unsere Haushaltskassen, aber immer noch besser, als wenn Kollegen gekündigt werden müssen. Wie können wir diese Krise gemeinsam überstehen? — Susanne",
        "Nehmen Sie Stellung zur Einführung von Kurzarbeit im Unternehmen.",
        "Diskutieren Sie Vor- und Nachteile von Kurzarbeit gegenüber Kündigungen.",
        "Berichten Sie von Erfahrungen mit wirtschaftlichen Krisen im Berufsleben.",
        "Schlagen Sie Weiterbildungsmaßnahmen während der Kurzarbeitszeit vor."
    ),
    (
        "schr-f-50-betriebsferien-weihnachten", 50, "Betriebsferien zwischen Weihnachten und Neujahr", "Betriebsruhe & Urlaubsanspruch", 105,
        "Das Werk soll zwischen dem 24. Dezember und dem 2. Januar komplett geschlossen bleiben. Alle Beschäftigten müssen dafür verbindlich zwei Tage ihres Jahresurlaubs einsetzen.",
        "Hallo zusammen, fast alle Firmen machen zwischen den Jahren Betriebsferien. Doch wer seinen Urlaub lieber im Sommer für eine Fernreise spart, fühlt sich bevormundet. Ist eine Zwangsschließung gerecht? — Timo",
        "Äußern Sie Ihre Meinung zur Festlegung von Betriebsferien zum Jahreswechsel.",
        "Wägen Sie Ruhe für den gesamten Betrieb gegen individuelle Urlaubsfreiheit ab.",
        "Erzählen Sie von Feiertags- und Urlaubsregelungen in Ihrem Herkunftsland.",
        "Machen Sie einen Vorschlag für Notbesetzungen oder flexible Zeiterfassungsmodelle."
    ),
    (
        "schr-f-51-innenhof-freizeit", 51, "Gestaltung des Innenhofs in der Freizeit", "Mitarbeiterengagement / Pausengestaltung", 105,
        "Der verfallene Innenhof soll in eine grüne Oase für die Mittagspausen verwandelt werden. Die Geschäftsleitung bittet die Belegschaft, an zwei Samstagen freiwillig bei den Pflanz- und Renovierungsarbeiten zu helfen.",
        "Liebe Kollegen, ein schöner Hof nützt uns allen. Aber sollte der Umbau nicht von professionellen Gärtnern auf Firmenkosten erledigt werden, statt die Freizeit der Mitarbeiter einzufordern? — Daniela",
        "Nehmen Sie Stellung zu dem Aufruf zur freiwilligen Wochenendarbeit für den Innenhof.",
        "Nennen Sie Vor- und Nachteile von Teameinsätzen für die Arbeitsumgebung.",
        "Berichten Sie von ehrenamtlichen oder gemeinschaftlichen Projekten im Beruf.",
        "Schlagen Sie vor, wie das Projekt während der regulären Arbeitszeit umgesetzt werden kann."
    ),
    (
        "schr-f-52-oepnv-jahresticket", 52, "Kostenloses ÖPNV-Abo bei Verzicht aufs Privatauto", "Betrieblicher Klimaschutz", 105,
        "Um aktiv zum Umweltschutz beizutragen, schenkt das Unternehmen jedem Beschäftigten ein unbegrenztes Nahverkehrs-Jahresabonnement, sofern dieser sich verpflichtet, das private Auto für den Arbeitsweg stehenzulassen.",
        "Hallo Team, das ist gelebter Klimaschutz und spart Hunderte Euro Spritkosten! Doch was ist mit Kollegen vom Land, wo der letzte Bus um 18 Uhr fährt? Schließt man die nicht ungerecht aus? — Gregor",
        "Äußern Sie Ihre Meinung zu der Prämie für den Verzicht auf das Auto.",
        "Wägen Sie Umweltentlastung gegen die Realität ländlicher Pendler ab.",
        "Berichten Sie von Ihren täglichen Mobilitätsentscheidungen.",
        "Schlagen Sie Ergänzungen wie Park-and-Ride-Modelle oder Fahrgemeinschaften vor."
    ),
    (
        "schr-f-53-urlaubstag-fortbildung", 53, "Ein Urlaubstag für hochwertige Fortbildungen", "Investition in Weiterbildung", 105,
        "Die Geschäftsführung bietet teure Zertifikatslehrgänge an. Die Firma übernimmt die hohen Seminarkosten (bis zu 2.000 €), verlangt jedoch, dass die Teilnehmer einen Tag ihres Jahresurlaubs dafür aufwenden.",
        "Liebe Kolleginnen und Kollegen, die Firma zahlt Tausende Euro für unsere Qualifikation, da ist ein opferter Urlaubstag doch eine faire Eigenleistung, die sich für die Karriere lohnt! Oder seht ihr das anders? — Florian",
        "Nehmen Sie Stellung zu der Bedingung, einen Urlaubstag für Weiterbildung einzusetzen.",
        "Diskutieren Sie Vor- und Nachteile dieses Co-Finanzierungsmodells.",
        "Schildern Sie Erfahrungen mit beruflichen Fortbildungen und Eigenleistungen.",
        "Schlagen Sie klare Vereinbarungen über Bildungszeit und Kostenübernahme vor."
    ),
    (
        "schr-f-54-papierverbrauch-limit", 54, "Strenges Kopier- und Drucklimit pro Mitarbeiter", "Umweltschutz im Büro", 105,
        "Um Papier und Ressourcen zu schonen, führt die IT-Abteilung ein persönliches Druckkontingent von maximal 50 Seiten pro Monat und Mitarbeiter ein. Zusätzliche Ausdrucke müssen gesondert genehmigt werden.",
        "Hallo zusammen, Papier sparen ist ein Gebot der Stunde. Aber wenn man vor einer wichtigen Präsentation oder einem Kundenmeeting um jede Farbseite betteln muss, behindert das die Arbeit enorm! — Simone",
        "Äußern Sie Ihre Haltung zu festen Druckkontingenten am Arbeitsplatz.",
        "Nennen Sie Vor- und Nachteile von Restriktionen beim Papierverbrauch.",
        "Berichten Sie von Ihren Erfahrungen mit dem papierlosen Büro.",
        "Schlagen Sie digitale Alternativen vor, die Arbeitsabläufe nicht ausbremsen."
    ),
    (
        "schr-f-55-kleiderspende", 55, "Betriebliche Kleiderspenden-Aktion für Kinder", "Soziales Engagement", 105,
        "Der Betriebsrat organisiert eine zweiwöchige Spendensammlung im Unternehmen: Mitarbeitende können gut erhaltene Kinderkleidung und Spielsachen spenden, die einem lokalen Kinderheim zugutekommen.",
        "Liebe Kollegen, eine wunderbare Initiative direkt bei uns im Haus! Das stärkt den Zusammenhalt und hilft Familien in Not. Wer hilft bei der Organisation der Sammelstelle im Foyer? — Christine",
        "Äußern Sie Ihre Ansicht zu karitativen Aktionen am Arbeitsplatz.",
        "Erläutern Sie die Vor- und Nachteile von sozialem Engagement im Firmenrahmen.",
        "Berichten Sie von Hilfsprojekten oder Spendenaktionen aus Ihrem Umfeld.",
        "Machen Sie Vorschläge für die logistische Durchführung und Information der Kollegen."
    ),

    # --- PÁGINA 106 ---
    (
        "schr-f-56-ausflug-eigenes-essen", 56, "Betriebsausflug: Eigenes Essen mitbringen", "Sparmaßnahmen bei Firmenevents", 106,
        "Aus Budgetgründen beschließt das Unternehmen, dass beim kommenden Sommerausflug kein Catering bereitgestellt wird. Jeder Teilnehmende soll Verpflegung und Getränke für sich und das Team selbst zubereiten und mitbringen.",
        "Hallo Team, bisher hat die Firma bei Festen immer spendabel für Essen gesorgt. Wenn wir jetzt unser Essen selbst mitbringen müssen, fühlt sich das geizig an und drückt auf die Stimmung! Was meint ihr? — Volker",
        "Nehmen Sie Stellung zu der Sparmaßnahme beim Betriebsausflug.",
        "Diskutieren Sie Vor- und Nachteile eines Mitbring-Büfetts (Potluck) im Vergleich zum Catering.",
        "Berichten Sie von Teamevents an früheren Arbeitsplätzen.",
        "Schlagen Sie ein faires Konzept vor (z. B. Grillen mit Basisverpflegung durch die Firma)."
    ),
    (
        "schr-f-57-freizeitbad-jahreskarte", 57, "Kostenlose Jahreskarte fürs Freizeitbad gegen Stress", "Betriebliche Gesundheitsvorsorge", 106,
        "Um den arbeitsbedingten Alltagsstress abzubauen und die Fitness zu fördern, schenkt das Unternehmen allen Mitarbeitern eine kostenfreie Jahreskarte für das städtische Hallen- und Freizeitbad.",
        "Liebe Kolleginnen und Kollegen, schwimmen gehen nach Feierabend ist eine fantastische Möglichkeit, den Kopf frei zu bekommen und fit zu bleiben. Ein tolles Geschenk unseres Arbeitgebers! — Jessica",
        "Äußern Sie Ihre Meinung zu der Jahreskarte als betriebliche Gesundheitsförderung.",
        "Nennen Sie Vor- und Nachteile dieses spezifischen Freizeitangebots.",
        "Berichten Sie von Ihren persönlichen Methoden zur Stressbewältigung nach der Arbeit.",
        "Schlagen Sie weitere Ideen vor, um die Gesundheit der Belegschaft nachhaltig zu stärken."
    ),
    (
        "schr-f-58-geschaeftsreisen-bahn", 58, "Geschäftsreisen: Bahn statt Privat- oder Dienstwagen", "Nachhaltige Dienstreisen", 106,
        "Die neue Reiserichtlinie schreibt vor, dass für alle geschäftlichen Reisen innerhalb Deutschlands vorrangig die Bahn zu nutzen ist. Fahrten mit dem Pkw werden nur noch in begründeten Ausnahmefällen erstattet.",
        "Hallo zusammen, im Zug kann man arbeiten und schont die Umwelt, das stimmt. Aber bei den ständigen Verspätungen und Zugausfällen verpasst man wichtige Kundentermine. Ist die Bahn wirklich verlässlich genug? — Steffen",
        "Nehmen Sie Stellung zur Verpflichtung, Dienstreisen mit der Bahn durchzuführen.",
        "Wägen Sie Klimaschutz und Arbeitskomfort gegen Unpünktlichkeit und Flexibilität ab.",
        "Erzählen Sie von Ihren Erfahrungen mit geschäftlichen Zugfahrten.",
        "Formulieren Sie Ausnahmeregelungen für zeitkritische oder abgelegene Termine."
    ),
    (
        "schr-f-59-keine-getraenke-mehr", 59, "Kaffee und Getränke nicht mehr kostenlos bereitgestellt", "Kürzung von Mitarbeiter-Benefits", 106,
        "Im Zuge eines Sparprogramms stellt das Unternehmen ab sofort keinen kostenlosen Kaffee, Tee und Mineralwasser mehr zur Verfügung. Die Mitarbeiter sollen ihre Getränke künftig von zu Hause mitbringen.",
        "Liebe Kollegen, kostenloser Kaffee gehört doch zum absoluten Mindeststandard jedes modernen Betriebs! Diese Kleinigkeit spart der Firma kaum Geld, demotiviert uns aber alle gewaltig. Was denkt ihr? — Manuel",
        "Äußern Sie Ihre Haltung zur Streichung der kostenlosen Getränke.",
        "Diskutieren Sie den Einfluss von kleinen Mitarbeiter-Benefits auf Motivation und Stimmung.",
        "Berichten Sie von Standards und Extras an Ihren bisherigen Arbeitsplätzen.",
        "Schlagen Sie einen Kompromiss (z. B. Kaffee-Kasse oder Wasserspender) vor."
    ),
    (
        "schr-f-60-handyverbot-grosskueche", 60, "Handyverbot in der Großküche aus Hygienegründen", "Hygiene & Lebensmittelsicherheit", 106,
        "In der Betriebsküche und Kantinenvorbereitung gilt ab sofort ein striktes Mobiltelefonverbot aus Hygiene- und Sicherheitsgründen. Alle Handys müssen vor Schichtbeginn im Spind eingeschlossen werden.",
        "Hallo Team, Smartphones sind voller Keime und Bakterien, in der Lebensmittelzubereitung haben sie absolut nichts verloren. Ich finde diese Hygiene-Maßnahme völlig richtig und überfällig! — Fatma",
        "Nehmen Sie Stellung zum Handyverbot in der Lebensmittelverarbeitung.",
        "Wägen Sie Hygiene- und Sicherheitsanforderungen gegen die Erreichbarkeit in Pausen ab.",
        "Berichten Sie von Hygiene- und Sicherheitsvorschriften aus Ihrer Berufspraxis.",
        "Machen Sie Vorschläge für klare Notfallkommunikation bei eingeschlossenen Handys."
    ),
    (
        "schr-f-61-fahrgemeinschaft-zuschuss", 61, "Benzinzuschuss nur für Fahrgemeinschaften", "Pendlerförderung & Umweltschutz", 106,
        "Um das Verkehrsaufkommen und den CO2-Ausstoß zu verringern, zahlt die Firma einen monatlichen Tankzuschuss an Mitarbeitende, die in Fahrgemeinschaften anreisen. Einzelfahrer erhalten keinerlei Unterstützung.",
        "Liebe Kolleginnen und Kollegen, Fahrgemeinschaften zu belohnen ist ein guter Gedanke. Aber wer Schichtdienst hat oder auf dem Weg noch Kinder zur Kita bringen muss, kann keine Fahrgemeinschaft bilden und wird benachteiligt! — Christian",
        "Äußern Sie Ihre Meinung zum Tankzuschuss exklusiv für Fahrgemeinschaften.",
        "Diskutieren Sie Vor- und Nachteile von Fahrgemeinschaften für den Arbeitsalltag.",
        "Erzählen Sie, wie Sie Ihren täglichen Arbeitsweg bewältigen.",
        "Schlagen Sie eine faire Pendlerpauschale für alle umweltfreundlichen Wege vor."
    ),
    (
        "schr-f-62-energie-sparen-fleece", 62, "Heizung drosseln (Energie sparen) und Fleecejacken", "Energiesparen & Bürotemperatur", 106,
        "Um Energiekosten zu sparen, wird die Raumtemperatur in den Büros im Winter auf 19 Grad gesenkt. Allen Mitarbeitenden stellt die Firma dafür kostenlos warme Fleecejacken mit Firmenlogo zur Verfügung.",
        "Hallo zusammen, 19 Grad sind beim stundenlangen Sitzen am Computer eisig kalt! Mit klammen Fingern tippt es sich schlecht, da hilft auch eine Fleecejacke nur begrenzt. Geht das Sparen hier auf Kosten unserer Gesundheit? — Beate",
        "Nehmen Sie Stellung zur Absenkung der Heiztemperatur und der Bereitstellung von Fleecejacken.",
        "Wägen Sie Energiekosten und Klimaschutz gegen Gesundheit und Konzentration ab.",
        "Berichten Sie von Temperatur- und Klimaverhältnissen an früheren Arbeitsplätzen.",
        "Unterbreiten Sie praxistaugliche Vorschläge für Energieeffizienz ohne Frieren im Büro."
    ),
    (
        "schr-f-63-teambildung-wochenende", 63, "Teambuilding-Event am Wochenende in anderer Stadt", "Teamentwicklung & Reise", 106,
        "Die Geschäftsführung plant ein zweitägiges Teambuilding-Event am Wochenende mit Übernachtung in einer 200 km entfernten Stadt. Die Teilnahme ist erwünscht, die Reise- und Hotelkosten trägt die Firma.",
        "Liebe Kollegen, ein gemeinsamer Wochenendausflug in eine andere Stadt schweißt das Team sicher zusammen. Dennoch haben viele am Wochenende familiäre Pflichten und möchten ihre Freizeit selbst gestalten. Wie seht ihr das? — Alexander",
        "Äußern Sie Ihre Ansicht zu dem Wochenend-Teambuilding mit Hotelübernachtung.",
        "Diskutieren Sie Chancen für den Zusammenhalt gegen die Belastung des privaten Wochenendes.",
        "Berichten Sie von Teambuilding-Events und Ausflügen aus Ihrer Erfahrung.",
        "Schlagen Sie alternative Formate während der regulären Arbeitswoche vor."
    ),
    (
        "schr-f-64-gleitzeit-abschaffung", 64, "Gleitzeit wird abgeschafft (feste Arbeitszeit 8:30–17:00)", "Arbeitszeitmodell / Flexibilität", 104,
        "Wegen mangelnder Erreichbarkeit für Kunden schafft das Unternehmen die Gleitzeitregelung ab. Alle Angestellten müssen ab sofort verbindlich von 8:30 bis 17:00 Uhr anwesend sein.",
        "Hallo Team, die Abschaffung der Gleitzeit wirft uns um Jahrzehnte zurück! Gerade für Eltern und Pendler war die flexible Einteilung ein unschätzbarer Vorteil. Wir müssen uns gegen diesen Rückschritt wehren! — Sandra",
        "Nehmen Sie Stellung zur Abschaffung der Gleitzeit zugunsten starrer Kernzeiten.",
        "Wägen Sie Kundenorientierung gegen Flexibilität und Lebensqualität der Beschäftigten ab.",
        "Schildern Sie Ihre Erfahrungen mit verschiedenen Arbeitszeitmodellen.",
        "Schlagen Sie ein Modell mit Kernarbeitszeiten vor, das beiden Seiten gerecht wird."
    ),
    (
        "schr-f-65-weiterbildung-nur-online", 65, "Weiterbildungen nur noch online / als E-Learning", "Digitale Fortbildung", 104,
        "Aus Budget- und Effizienzgründen streicht die Unternehmensleitung alle externen Präsenzseminare. Fortbildungen werden künftig ausschließlich über eine interne E-Learning-Plattform angeboten.",
        "Liebe Kollegen, Online-Kurse sind zeitlich flexibel, aber der persönliche Austausch mit Dozenten und Kollegen aus anderen Firmen fehlt völlig. Man klickt sich oft nur schnell durch die Folien. Was meint ihr? — Daniel",
        "Äußern Sie Ihre Meinung zur ausschließlichen Nutzung von Online-Fortbildungen.",
        "Nennen Sie Vor- und Nachteile von E-Learning im Vergleich zu Präsenzseminaren.",
        "Berichten Sie von Ihren Erfahrungen mit digitalen Lernangeboten im Beruf.",
        "Schlagen Sie ein Blended-Learning-Konzept vor, das Online- und Präsenzteile verbindet."
    ),
    (
        "schr-f-66-buero-mit-hunden", 66, "Bürohunde im Unternehmen erlaubt", "Haustiere am Arbeitsplatz", 104,
        "Die Firmenleitung beschließt, dass Beschäftigte nach Voranmeldung ihre gut erzogenen Hunde mit ins Büro bringen dürfen, um das Betriebsklima und das Wohlbefinden zu fördern.",
        "Hallo zusammen, Hunde im Büro bauen nachweislich Stress ab und heben die Stimmung! Aber was ist mit Kollegen, die Allergien haben oder Angst vor Hunden haben? Wir brauchen klare Regeln. — Florian",
        "Äußern Sie Ihre Haltung zu Hunden am Arbeitsplatz.",
        "Wägen Sie Entspannung und Freude gegen Allergien, Ängste und Hygiene ab.",
        "Berichten Sie von Ihren Erfahrungen mit Haustieren im beruflichen Umfeld.",
        "Formulieren Sie konkrete Richtlinien für ein harmonisches Miteinander von Mensch und Tier."
    )
]

def main():
    variants = []
    for item in RAW_TOPICS:
        fid, num, title, topic, page, scenario, colleague_post, lp1, lp2, lp3, lp4 = item
        v = make_forum(fid, num, title, topic, page, scenario, colleague_post, lp1, lp2, lp3, lp4)
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
