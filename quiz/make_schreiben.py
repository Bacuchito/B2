import json

redemittel_beschwerde = [
    "Sehr geehrte(r) Frau/Herr [Name], / Sehr geehrte Damen und Herren,",
    "vielen Dank für Ihre E-Mail, in der Sie uns auf die Unstimmigkeiten bei ... hinweisen.",
    "Wir bedauern sehr, dass Sie mit unserem Service / unserer Lieferung nicht zufrieden waren.",
    "Bitte entschuldigen Sie die entstandenen Unannehmlichkeiten.",
    "Der Grund für dieses Problem war, dass...",
    "Nach Rücksprache mit unserer zuständigen Abteilung können wir Ihnen mitteilen, dass...",
    "Wir möchten Ihnen folgenden Lösungsvorschlag unterbreiten: ...",
    "Gern schicken wir Ihnen umgehend einen Techniker vorbei / liefern wir die Ware erneut.",
    "Als kleine Entschädigung und Wiedergutmachung bieten wir Ihnen einen Rabatt von ... % an.",
    "Selbstverständlich übernehmen wir die anfallenden Kosten.",
    "Wir versichern Ihnen, dass wir alles tun werden, damit sich ein solcher Vorfall nicht wiederholt.",
    "Wir hoffen auf Ihr Verständnis und freuen uns weiterhin auf eine gute Zusammenarbeit.",
    "Mit freundlichen Grüßen"
]

redemittel_forum = [
    "Ich möchte mich an der aktuellen Diskussion zum Thema «...» beteiligen.",
    "In unserem Unternehmen wird zurzeit viel über die Frage diskutiert, ob...",
    "Meiner Ansicht / Meinung nach ist diese Maßnahme ein wichtiger Schritt, weil...",
    "Einerseits bietet dieses Modell entscheidende Vorteile, wie zum Beispiel...",
    "Andererseits darf man jedoch nicht übersehen, dass damit auch Nachteile verbunden sind, etwa...",
    "Ein weiterer Aspekt, der bedacht werden sollte, ist...",
    "Aus meiner persönlichen Erfahrung kann ich berichten, dass...",
    "In meinem Heimatland ist es in vielen Betrieben üblich, dass...",
    "Um eine für alle Beteiligten faire Lösung zu finden, schlage ich vor, dass...",
    "Zusammenfassend lässt sich sagen, dass ein ausgewogener Kompromiss notwendig ist.",
    "Ich bin gespannt auf die Meinungen der anderen Kolleginnen und Kollegen."
]

beschwerden = [
    {
        "id": "schr-b-p66",
        "category": "beschwerde",
        "kind": "schreiben",
        "label": "Beschwerde 1: Putzdienst und unvollständige Arbeitszeit",
        "topic": "Putzdienst / Büroreinigung",
        "page": 66,
        "source_variant": 1,
        "scenario": "Die Huber GmbH hat einen Vertrag über täglich 3 Stunden Büroreinigung (6:00 bis 9:00 Uhr). Herr Lassner beschwert sich, dass die Reinigungskräfte in den letzten zwei Wochen mehrfach vor 9:00 Uhr nicht mehr da waren. Er verlangt eine Anpassung der Rechnung.",
        "source_letter": "Sehr geehrte Frau Woller,\n\nleider muss ich mich heute mit einer Beschwerde an Sie wenden. Wir haben einen Vertrag mit Ihrer Firma für die Reinigung unserer Büroräume. In diesem Vertrag sind täglich 3 Stunden Arbeit bei uns festgelegt, und zwar von 6.00 Uhr bis 9.00 Uhr morgens.\n\nIn den letzten zwei Wochen war unsere Sekretärin einige Male bereits vor 9 Uhr im Büro, von Ihrem Putzdienst war aber niemand zu sehen. Wie kann das sein?\n\nWenn wir 3 Stunden bezahlen, erwarten wir auch, dass Ihr Personal drei Stunden bei uns arbeitet. Wenn Sie für die Reinigung unserer Räume weniger als die vereinbarte Zeit benötigen, sollten Sie uns darüber informieren, damit wir den Vertrag ändern.\n\nIch bitte um umgehende Stellungnahme und natürlich die Angleichung der Rechnung an die tatsächlich geleisteten Arbeitsstunden.\n\nMit freundlichen Grüßen\nTheo Lassner",
        "boss_instructions": "Hallo Friederike, ich verstehe den Ärger von Herrn Lassner. Bitte kläre mit unseren Leuten, was da los ist, und antworte Herrn Lassner. Sage ihm zu, dass so etwas nie wieder vorkommt, und gib ihm 20 % Rabatt auf die nächste Rechnung. Wir dürfen den Kunden keinesfalls verlieren! Gruß Heike",
        "prompt": "Sie sind Mitarbeiter(in) bei der Reinigungsfirma. Ihr(e) Vorgesetzte(r) hat Sie gebeten, dem Kunden zu antworten. Schreiben Sie eine E-Mail an Herrn Lassner. Behandeln Sie dabei die folgenden vier Punkte:",
        "leitpunkte": [
            "Bezugnahme auf die Beschwerde und Dank für den Hinweis",
            "Förmliche Entschuldigung und Erklärung der Ursache des Problems",
            "Zusicherung, dass die vertragliche Arbeitszeit künftig strikt eingehalten wird",
            "Angebot eines 20 %-igen Rabatts auf die nächste Monatsrechnung als Wiedergutmachung"
        ],
        "min_words": 150,
        "time_minutes": 45,
        "redemittel": redemittel_beschwerde
    },
    {
        "id": "schr-b-p67",
        "category": "beschwerde",
        "kind": "schreiben",
        "label": "Beschwerde 2: Lieferverzögerung Tischlampen",
        "topic": "Lieferverzögerung Büromöbel",
        "page": 67,
        "source_variant": 2,
        "scenario": "Frau Berger hat 25 Tischlampen für neu renovierte Büros bestellt. Die Lieferung wurde für diese Woche zugesagt, ist aber am Freitagnachmittag noch nicht eingetroffen. Am Montag soll der Betrieb starten. Wenn die Lampen bis Montagmittag nicht da sind, wird sie stornieren.",
        "source_letter": "Sehr geehrter Herr Richter,\n\nvergangene Woche habe ich bei Ihnen 25 Tischlampen Modell TS 13 150 07 für unsere neuen Büroräume bestellt. Mir wurde telefonisch zugesagt, dass die Lampen noch diese Woche geliefert werden, aber jetzt ist schon Freitagnachmittag und sie sind leider noch immer nicht eingetroffen.\n\nDas ist ärgerlich, da wir am Wochenende unsere Renovierungsarbeiten beenden und die Büros dann vollständig neu einrichten werden. Dazu würden natürlich auch die Lampen gehören, da wir am Montag unseren Bürobetrieb in funktionstüchtigen Räumen wieder aufnehmen wollen. Ich habe bereits mehrfach versucht, Sie telefonisch zu erreichen, und habe Nachrichten auf Ihrem Anrufbeantworter hinterlassen, aber ich wurde leider nicht zurückgerufen.\n\nWenn Ihre Lampen also bis Montagmittag, 13:00 Uhr, nicht bei uns eingetroffen sind, werde ich die Bestellung bei Ihnen stornieren. Ich bitte um eine schnelle Antwort!\n\nMit freundlichen Grüßen\nEvelyn Berger",
        "boss_instructions": "Bitte antworten Sie Frau Berger sofort. Entschuldigen Sie sich für die Verzögerung beim Zulieferer. Versichern Sie ihr, dass die Lampen per Expresskurier am Montagmorgen vor 10:00 Uhr eintreffen und wir die Expresskosten sowie einen Preisnachlass übernehmen.",
        "prompt": "Schreiben Sie eine E-Mail an Frau Berger. Behandeln Sie dabei die folgenden vier Punkte:",
        "leitpunkte": [
            "Bezug auf die Bestellung und Entschuldigung für die Nicht-Erreichbarkeit",
            "Erklärung der Ursache des Lieferverzugs beim Hersteller",
            "Verbindliche Zusage der Expresslieferung am Montag vor 10:00 Uhr",
            "Angebot einer kostenlosen Montage und eines Preisnachlasses als Ausgleich"
        ],
        "min_words": 150,
        "time_minutes": 45,
        "redemittel": redemittel_beschwerde
    },
    {
        "id": "schr-b-p68",
        "category": "beschwerde",
        "kind": "schreiben",
        "label": "Beschwerde 3: Lieferverzögerung Tischlampen – Fassung 2",
        "topic": "Lieferverzögerung Büromöbel",
        "page": 68,
        "source_variant": 2,
        "scenario": "Frau Lutz hat 15 Tischlampen (Modell TS 13 150 07) für ihre neuen Büroräume bestellt und bis Freitagnachmittag nicht erhalten. Sie hat eine Frist bis Montagmittag, 12:00 Uhr, gesetzt, droht mit Stornierung und hat bereits einen Ersatzlieferanten gefunden.",
        "source_letter": "Sehr geehrter Herr Phillips,\n\nvergangene Woche habe ich bei Ihnen 15 Tischlampen Modell TS 13 150 07 für unsere neuen Büroräume bestellt. Mir wurde telefonisch zugesagt, dass die Lampen noch diese Woche geliefert werden, aber jetzt ist schon Freitagnachmittag und sie sind leider noch immer nicht eingetroffen.\n\nDas ist sehr ärgerlich, da wir am Wochenende unsere Renovierungsarbeiten beenden und die Büros dann vollständig neu einrichten werden. Dazu würden natürlich auch die Lampen gehören, da wir am Montag unseren Bürobetrieb in funktionstüchtigen Räumen wieder aufnehmen wollen.\n\nIch habe bereits mehrfach versucht, Sie telefonisch zu erreichen, und habe Nachrichten auf Ihrem Anrufbeantworter hinterlassen, aber ich wurde leider nicht zurückgerufen. Inzwischen habe ich einen Lieferanten gefunden, der uns kurzfristig andere Tischlampen liefern könnte.\n\nWenn Ihre Lampen also bis Montagmittag, 12:00 Uhr, nicht bei uns eingetroffen sind, werde ich die Bestellung bei Ihnen stornieren. Ich bitte um eine schnelle Antwort!\n\nMit freundlichen Grüßen\nBetta Lutz",
        "boss_instructions": "Hallo, ich habe schon wieder eine Beschwerde einer Kundin vorliegen. Sie hat ihre bestellten Tischlampen nicht bekommen. Bitte antworten Sie Frau Lutz und erklären Sie ihr, warum wir im Moment Lieferschwierigkeiten haben. Versuchen Sie auch, sie davon zu überzeugen, noch bis nächste Woche zu warten und den Auftrag nicht zu stornieren. Bieten Sie ihr außerdem ein ähnliches Modell an, das wir auf Lager haben. Danke!",
        "prompt": "Schreiben Sie eine E-Mail an Frau Lutz. Behandeln Sie dabei die folgenden vier Punkte:",
        "leitpunkte": [
            "Dank für die Nachricht und Verständnis für den Ärger über die Verzögerung",
            "Erklärung der aktuellen Lieferschwierigkeiten und Entschuldigung dafür",
            "Bitte, den Auftrag nicht zu stornieren und noch bis nächste Woche zu warten",
            "Angebot eines ähnlichen Lampenmodells, das sofort auf Lager ist"
        ],
        "min_words": 150,
        "time_minutes": 45,
        "redemittel": redemittel_beschwerde
    },
    {
        "id": "schr-b-p69",
        "category": "beschwerde",
        "kind": "schreiben",
        "label": "Beschwerde 4: Website-Entwurf – Farben und vertauschte Namen",
        "topic": "Webdesign-Agentur und Korrekturwünsche",
        "page": 69,
        "source_variant": 3,
        "scenario": "Der Kunde Franz Stiller beanstandet den Entwurf für seine neue Firmenwebsite: Das Farbschema entspricht nicht der Absprache und auf der Seite mit den Ansprechpartnern sind Namen vertauscht. Intern sind die vertauschten Namen unser Fehler, weitere Korrekturen soll der Kunde aber bezahlen.",
        "source_letter": "Sehr geehrte Frau Spindler,\n\nvielen Dank für Ihren Entwurf für unsere neue Firmenwebsite. Ich habe ihn gemeinsam mit dem Team gesichtet und dabei ist uns aufgefallen, dass Ihre Agentur die Vorgaben an zwei Stellen leider nicht umgesetzt hat:\n\nZum einen hatten wir besprochen, dass das Farbschema grau orange sein sollte. Da statt Grau Blau gewählt wurde, glaube ich, dass es zu einem Missverständnis gekommen ist. Zum anderen sind auf der Seite mit den Ansprechpartnern die Namen einiger Mitarbeiter vertauscht worden. Im Anhang schicke ich Ihnen noch einmal eine Auflistung der Namen mit den dazugehörigen Bildern. Könnten Sie diese beiden Punkte bitte bis Anfang nächster Woche nachbessern? Eine kurze Rückmeldung wäre nett.\n\nMit freundlichen Grüßen\nFranz Stiller",
        "boss_instructions": "Hallo Frau Holsten, ich habe heute Mittag die untenstehende Mail bekommen. Die vertauschten Namen sind unser Fehler und die verbessern wir auch; bitte bestätigen Sie dem Kunden das. Aber mehr ist nun wirklich nicht drin: Das ist schon das fünfte Mal, dass er Korrekturwünsche hat, obwohl wir uns immer an die Vorgaben gehalten haben. So viele Korrekturen waren nicht vereinbart! Wenn wir das noch machen sollen, geht das nur gegen zusätzliche Bezahlung. Ich rechne mit 200 € extra. Bitte teilen Sie ihm dies mit und lassen Sie sich von ihm sein Okay geben.",
        "prompt": "Schreiben Sie eine E-Mail an Herrn Stiller. Behandeln Sie dabei die folgenden vier Punkte:",
        "leitpunkte": [
            "Dank für die Rückmeldung und Zusage, die vertauschten Namen zu korrigieren",
            "Höfliche Klärung des Farbproblems: Wir haben uns an die vereinbarten Vorgaben gehalten",
            "Hinweis auf die fünfte Korrekturrunde und auf den bereits überschrittenen Leistungsumfang",
            "Nennung des zusätzlichen Honorars von 200 € und Bitte um das Okay des Kunden"
        ],
        "min_words": 150,
        "time_minutes": 45,
        "redemittel": redemittel_beschwerde
    },
    {
        "id": "schr-b-p70",
        "category": "beschwerde",
        "kind": "schreiben",
        "label": "Beschwerde 5: Defekte Spülmaschine und Wasserschaden",
        "topic": "Gerätedefekt und Folgeschaden",
        "page": 70,
        "source_variant": 4,
        "scenario": "Herr Krüger kaufte eine Spülmaschine für die Teeküche. Beim ersten Spülgang lief Wasser aus und beschädigte das Parkett. In zwei Tagen findet ein wichtiges Meeting statt. Er verlangt sofortige Reparatur und Kostenübernahme für den Parkettaustausch.",
        "source_letter": "Sehr geehrte Frau Sturm,\n\nvor einer Woche haben wir bei Ihnen eine Spülmaschine für unsere Teeküche gekauft. Sie wurde sehr schnell geliefert und auch gleich eingebaut. Leider muss ich Ihnen heute aber mitteilen, dass sie bereits defekt ist. Beim Spülen ist Wasser ausgelaufen und nun ist unser Parkett beschädigt.\n\nIch bitte Sie, uns umgehend einen Techniker zu schicken, der das Gerät repariert. Wir brauchen die Spülmaschine spätestens übermorgen, da wir ein großes Meeting unserer Außendienstmitarbeiter haben und viele Personen bewirten müssen.\n\nAußerdem müssen wir einen Teil des Parketts austauschen. Die Kosten dafür werden wir Ihnen in Rechnung stellen.\n\nBitte schicken Sie mir so schnell wie möglich einen Terminvorschlag für die Reparatur und eine Bestätigung der Kostenübernahme. Vielen Dank!\n\nMit freundlichen Grüßen\nClaudio Krüger",
        "boss_instructions": "Hallo Frau Retterstein, organisieren Sie bitte sofort einen Techniker für Herrn Krüger. Entschuldigen Sie sich für die Unannehmlichkeiten und sagen Sie zu, dass wir die Reparatur und die Forderungen prüfen. Weisen Sie aber vorsorglich darauf hin, dass die Reparatur eventuell Ersatzteile erfordert. Danke!",
        "prompt": "Schreiben Sie eine E-Mail an Herrn Krüger. Behandeln Sie dabei die folgenden vier Punkte:",
        "leitpunkte": [
            "Bezugnahme auf die E-Mail von Herrn Krüger und Bedauern über den Wasserschaden",
            "Förmliche Entschuldigung für die Unannehmlichkeiten mit dem Neugerät",
            "Terminvereinbarung für den Technikerbesuch am Folgetag zur Fehlerbehebung",
            "Zusage zur unbürokratischen Prüfung der Kostenübernahme für das Parkett"
        ],
        "min_words": 150,
        "time_minutes": 45,
        "redemittel": redemittel_beschwerde
    },
    {
        "id": "schr-b-p71",
        "category": "beschwerde",
        "kind": "schreiben",
        "label": "Beschwerde 6: Probleme beim Firmenumzug",
        "topic": "Umzugsdienstleistung und Transportschäden",
        "page": 71,
        "source_variant": 5,
        "scenario": "Beim Büroumzug von Hanau nach Frankfurt kamen die Möbelpacker 30 Minuten zu spät und nur zu dritt statt zu viert. Die Möbel sind noch nicht fertig aufgebaut, Glasplatten sind zerbrochen und Schränke verkratzt. Herr Zaun fordert Nachbesserung am Mittwoch und Schadensersatz.",
        "source_letter": "Sehr geehrte Frau Börne,\n\nam Wochenende ist unser Büro mit Hilfe Ihres Unternehmens von Hanau nach Frankfurt umgezogen. Leider waren wir mit Ihrem Service überhaupt nicht zufrieden.\n\nIhre Mitarbeiter kamen eine halbe Stunde zu spät und nur zu dritt statt wie vereinbart zu viert. Deshalb dauerte der ganze Umzug natürlich länger als geplant und einige Arbeiten sind auch noch nicht abgeschlossen: Es sind noch nicht alle Möbel aufgebaut, deshalb konnten wir noch nicht unsere Sachen einräumen.\n\nBitte schicken Sie uns deshalb am Mittwochmorgen noch zwei Personen, die den Möbelaufbau erledigen. Des Weiteren sind Glasplatten zu Bruch gegangen und einige Schränke sind verkratzt. Ich gehe davon aus, dass Ihre Firma die Kosten dafür übernimmt.\n\nMit freundlichen Grüßen\nThomas Zaun",
        "boss_instructions": "Hallo Frau Kühne, da ist wohl was schiefgegangen. Bitte schreiben Sie Herrn Zaun und erklären Sie die Fehler. Sagen Sie zu, dass am Mittwochmorgen pünktlich zwei Monteure kommen und alles fertig aufbauen. Natürlich übernehmen wir die Verantwortung für die Schäden. Die Firma hat das erste Mal bei uns gebucht!",
        "prompt": "Schreiben Sie eine E-Mail an Herrn Zaun. Behandeln Sie dabei die folgenden vier Punkte:",
        "leitpunkte": [
            "Bezug auf den Umzug und aufrichtige Entschuldigung für die Verzögerung",
            "Erklärung der Ursachen (plötzlicher Personalausfall und Verkehrsbehinderung)",
            "Bestätigung des Termins am Mittwochmorgen mit zwei erfahrenen Monteuren",
            "Zusage der Schadensregulierung über die Betriebshaftpflichtversicherung"
        ],
        "min_words": 150,
        "time_minutes": 45,
        "redemittel": redemittel_beschwerde
    },
    {
        "id": "schr-b-p71b",
        "category": "beschwerde",
        "kind": "schreiben",
        "label": "Beschwerde 7: Firmenumzug – Fassung 2 (Herr Lozano)",
        "topic": "Umzugsdienstleistung und Transportschäden",
        "page": 71,
        "source_variant": 5,
        "scenario": "Beim Büroumzug von Hanau nach Frankfurt kamen die Möbelpacker 30 Minuten zu spät und nur zu dritt statt zu viert. Die Möbel sind noch nicht fertig aufgebaut, Glasplatten sind zerbrochen und Schränke verkratzt. Herr Lozano fordert Nachbesserung am Mittwoch und Schadensersatz.",
        "source_letter": "Sehr geehrte Frau Prince,\n\nam Wochenende ist unser Büro mit Hilfe Ihres Unternehmens von Hanau nach Frankfurt umgezogen. Leider waren wir mit Ihrem Service überhaupt nicht zufrieden.\n\nIhre Mitarbeiter kamen eine halbe Stunde zu spät und nur zu dritt statt wie vereinbart zu viert. Deshalb dauerte der ganze Umzug natürlich länger als geplant und einige Arbeiten sind auch noch nicht abgeschlossen: Es sind noch nicht alle Möbel aufgebaut, deshalb konnten wir noch nicht unsere Sachen einräumen.\n\nBitte schicken Sie uns deshalb am Mittwochmorgen noch zwei Personen, die den Möbelaufbau erledigen. Des Weiteren sind Glasplatten zu Bruch gegangen und einige Schränke sind verkratzt. Ich gehe davon aus, dass Ihre Firma die Kosten dafür übernimmt.\n\nMit freundlichen Grüßen\nMatteo Lozano",
        "boss_instructions": "Hallo Frau Kühne, da ist wohl was schiefgegangen. Bitte schreiben Sie Herrn Lozano und erklären Sie die Fehler. Sagen Sie zu, dass am Mittwochmorgen pünktlich zwei Monteure kommen und alles fertig aufbauen. Natürlich übernehmen wir die Verantwortung für die Schäden. Die Firma hat das erste Mal bei uns gebucht!",
        "prompt": "Schreiben Sie eine E-Mail an Herrn Lozano. Behandeln Sie dabei die folgenden vier Punkte:",
        "leitpunkte": [
            "Bezug auf den Umzug und aufrichtige Entschuldigung für die Verzögerung",
            "Erklärung der Ursachen (plötzlicher Personalausfall und Verkehrsbehinderung)",
            "Bestätigung des Termins am Mittwochmorgen mit zwei erfahrenen Monteuren",
            "Zusage der Schadensregulierung über die Betriebshaftpflichtversicherung"
        ],
        "min_words": 150,
        "time_minutes": 45,
        "redemittel": redemittel_beschwerde
    },
    {
        "id": "schr-b-p72",
        "category": "beschwerde",
        "kind": "schreiben",
        "label": "Beschwerde 8: Kopiergerät defekt und Streit über Rechnungen",
        "topic": "Bürogeräte und Kundendienst",
        "page": 72,
        "source_variant": 6,
        "scenario": "Herr Schmidt (Mova GmbH) beschwert sich über wiederholte Papierstaus an einem fast neuen Druckgerät. Trotz dreier Technikereinsätze trat wieder ein Fehler auf, wodurch eine Ausschreibung verpasst wurde. Er fordert ein Ersatzgerät und weigert sich, die Rechnungen der Techniker zu bezahlen.",
        "source_letter": "Sehr geehrte Frau Aichele,\n\nvorgestern wurde von einem Ihrer Mitarbeiter unser fast neues Druck- und Kopiergerät der Marke Lexios zum dritten Mal innerhalb von zwei Wochen geprüft, da bei diesem immer wieder Papierstaus aufgetreten sind. Gestern kam es schon wieder zu einer Fehlermeldung, was zur Folge hatte, dass wir Unterlagen nicht fristgerecht einreichen konnten. Aus diesem Grund haben wir eine für uns sehr wichtige Ausschreibung verpasst. Von einer Schadensersatzforderung sehen wir vorerst ab, wir fordern Sie aber auf, uns umgehend auf Ihre Kosten ein anderes Gerät zu liefern. Es handelt sich hier nämlich eindeutig um einen technischen Fehler, den wir nicht zu verantworten haben. Die Rechnungen für die drei vorangegangenen Technikereinsätze werden wir natürlich nicht bezahlen.\n\nIch erwarte Ihre umgehende Rückmeldung.\n\nMit freundlichen Grüßen\nBenno Schmidt",
        "boss_instructions": "Hallo, laut Techniker lag der Fehler erneut an falscher Bedienung. Antworte Herrn Schmidt bitte und weise ihn höflich darauf hin, dass die Verantwortung nicht bei uns liegt. Gerne kommt noch einmal ein Techniker kostenfrei zur Mitarbeitereinweisung vorbei. Die Kosten für die Geräteüberprüfungen bleiben aber bei Mova.",
        "prompt": "Schreiben Sie eine E-Mail an Herrn Schmidt. Behandeln Sie dabei die folgenden vier Punkte:",
        "leitpunkte": [
            "Dank für die Rückmeldung und Bedauern über die verpasste Ausschreibung",
            "Höfliche Erläuterung des Technikerbefunds (Bedienerfehler / Papierspezifikation)",
            "Angebot einer kostenlosen Schulung der Mitarbeitenden vor Ort",
            "Stellungnahme und Begründung bezüglich der bestehenden Prüfungsrechnungen"
        ],
        "min_words": 150,
        "time_minutes": 45,
        "redemittel": redemittel_beschwerde
    },
    {
        "id": "schr-b-p73",
        "category": "beschwerde",
        "kind": "schreiben",
        "label": "Beschwerde 9: Kopiergerät defekt – Fassung 2 (Cavone GmbH)",
        "topic": "Bürogeräte und Kundendienst",
        "page": 73,
        "source_variant": 6,
        "scenario": "Frau Zeller (Cavone GmbH) beschwert sich über wiederholte Fehlermeldungen am neuen ABC-Druck-, Kopier- und Faxgerät. Weil ein Fax mit wichtigen Unterlagen nicht fristgerecht rausging, ging ein wichtiger Deal verloren. Sie fordert ein Ersatzgerät auf unsere Kosten und will die Prüfungsrechnungen nicht bezahlen.",
        "source_letter": "Sehr geehrter Herr Brenner,\n\nvor drei Tagen hat einer Ihrer Mitarbeiter das neue ABC-Druck-, Kopier- und Faxgerät inspiziert. Dies war das zweite Mal innerhalb einer Woche, dass beim Versenden eines Faxes ein Fehlerzeichen auftrat.\n\nLeider kam gestern wieder eine Fehlermeldung, und wir sollten einige wichtige Unterlagen zum Treffen per Fax verschicken. Wir konnten diese jedoch nicht rechtzeitig versenden. Deshalb haben wir einen für uns sehr wichtigen Deal verloren. Wir sehen derzeit von Schadensersatzansprüchen ab, bitten Sie jedoch, uns umgehend und auf Ihre Kosten ein anderes Gerät zuzusenden.\n\nOffensichtlich handelt es sich hierbei um einen technischen Fehler, für den wir keine Verantwortung übernehmen.\n\nSelbstverständlich übernehmen wir auch keine Rechnungen für vorangegangene technische Arbeiten.\n\nIch hoffe, dass wir schnellstmöglich eine Antwort von Ihnen erhalten.\n\nMit freundlichen Grüßen\nVala Zeller",
        "boss_instructions": "Guten Morgen, vor einer Stunde erhielt ich diese E-Mail von der Cavone GmbH. Nach Angaben unseres Technikers lag der Fehler wiederum bei der Cavone GmbH. Bitte antworten Sie Frau Zeller und weisen Sie sie höflich darauf hin, dass es nicht in unserer Verantwortung liegt, das Problem zu lösen. Der Techniker kommt gerne wieder ins Unternehmen und führt die Mitarbeiter kostenlos durch den Prozess. Teilen Sie ihr außerdem mit, dass die Kosten für die Untersuchung des Geräts weiterhin ihr Unternehmen trägt.",
        "prompt": "Schreiben Sie eine E-Mail an Frau Zeller. Behandeln Sie dabei die folgenden vier Punkte:",
        "leitpunkte": [
            "Dank für die Rückmeldung und Bedauern über den verlorenen Deal",
            "Höfliche Erläuterung des Technikerbefunds: Der Fehler lag nicht bei uns",
            "Angebot einer kostenlosen Einweisung der Mitarbeitenden durch unseren Techniker",
            "Klare Stellungnahme zu den Kosten der Geräteuntersuchung und zu den Rechnungen"
        ],
        "min_words": 150,
        "time_minutes": 45,
        "redemittel": redemittel_beschwerde
    },
    {
        "id": "schr-b-p74",
        "category": "beschwerde",
        "kind": "schreiben",
        "label": "Beschwerde 10: Falsche Rechnung und fehlender Rabatt",
        "topic": "Rechnungsstellung und Konditionen",
        "page": 74,
        "source_variant": 7,
        "scenario": "Ein langjähriger Stammkunde stellt Unstimmigkeiten in der Rechnung fest: 200 statt 100 Pinsel berechnet, teurere rote statt grüner Farbe aufgeführt und der vereinbarte Stammkundenrabatt von 10 % fehlt.",
        "source_letter": "Sehr geehrte Frau Hoffner,\n\nwir haben Ihre Lieferung erhalten und sind mit allen Artikeln absolut zufrieden. Leider muss ich Sie darauf hinweisen, dass die Rechnung einige Unstimmigkeiten beinhaltet: Zunächst wurden statt 100 Stück Pinsel Größe M 200 Stück berechnet. Außerdem wurden 20 Töpfe roter Farbe berechnet. Wir hatten aber grüne Farbe bestellt und geliefert bekommen, die preislich niedriger liegt. Wir bitten Sie, dies zu korrigieren. Des Weiteren waren wir überrascht, dass unser üblicher Rabatt von 10 % in dieser Rechnung nicht gewährt wurde. Das ist wahrscheinlich ein Versehen.\n\nWir bitten um Berichtigung der Rechnung und erneute Zusendung.\n\nMit freundlichen Grüßen\nKarl Schmidt",
        "boss_instructions": "Hallo, Herr Schmidt ist ein wichtiger Stammkunde. Bitte entschuldige dich bei ihm. Der Fehler lag an der Umstellung unserer Buchhaltungssoftware. Schicke ihm sofort eine korrigierte Rechnung mit den 10 % Rabatt und lege als Entschuldigung einen Gutschein über 50 Euro bei.",
        "prompt": "Schreiben Sie eine E-Mail an Herrn Schmidt. Behandeln Sie dabei die folgenden vier Punkte:",
        "leitpunkte": [
            "Dank für den freundlichen Hinweis und Bedauern über die Fehler in der Rechnung",
            "Erklärung der Ursache (technische Umstellung der Abrechnungssoftware)",
            "Zusicherung der sofortigen Rechnungskorrektur (100 Pinsel, grüne Farbe, 10 % Rabatt)",
            "Beigabe eines Einkaufsgutscheins als Zeichen der Wertschätzung für die Treue"
        ],
        "min_words": 150,
        "time_minutes": 45,
        "redemittel": redemittel_beschwerde
    },
    {
        "id": "schr-b-p75",
        "category": "beschwerde",
        "kind": "schreiben",
        "label": "Beschwerde 11: Falsche Rechnung – Fassung 2 (Lacke und Farben)",
        "topic": "Rechnungsstellung und Konditionen",
        "page": 75,
        "source_variant": 7,
        "scenario": "Der langjährige Kunde Joachim Schmidt (Firma Lacke und Farben) beanstandet die Rechnung: 200 statt 100 Pinsel Größe S berechnet, 50 Töpfe roter statt grüner Farbe aufgeführt und der übliche Rabatt von 10 % fehlt.",
        "source_letter": "Sehr geehrte Frau Klein,\n\nwir haben Ihre Lieferung wie gewohnt zu unserer vollsten Zufriedenheit erhalten. Alle Artikel entsprechen absolut unseren Vorstellungen.\n\nLeider muss ich Sie darauf hinweisen, dass in der beigelegten Rechnung einige Unstimmigkeiten aufgetreten sind. Zunächst wurden statt der 100 Stück Pinsel Größe S 200 Stück berechnet. Außerdem wurden 50 Töpfe rote Farbe aufgeführt. Wir hatten aber grüne Farbe bestellt und geliefert bekommen, die preislich niedriger liegt. Wir bitten das zu korrigieren. Ferner waren wir verwundert, dass uns der übliche Rabatt von 10 % in dieser Rechnung nicht gewährt wurde. Dies ist wahrscheinlich ein Versehen.\n\nWir bitten um Berichtigung der Rechnung und erneute Zusendung.\n\nMit freundlichen Grüßen\nJoachim Schmidt",
        "boss_instructions": "Hallo, ich habe gestern die unten stehende Mail erhalten. Bitte kümmere dich darum und antworte dem Kunden höflich. Die Firma Lacke und Farben ist ein langjähriger, guter Kunde; wir können es uns nicht leisten, ihn zu verlieren. Du kannst ihm ruhig von unseren Computerproblemen berichten und wie wir sie gelöst haben. Selbstverständlich kriegt er den Rabatt wie immer.",
        "prompt": "Schreiben Sie eine E-Mail an Herrn Schmidt. Behandeln Sie dabei die folgenden vier Punkte:",
        "leitpunkte": [
            "Dank für den sachlichen Hinweis und Bedauern über die Fehler in der Rechnung",
            "Erklärung der Ursache (Computerproblem bei der Rechnungsstellung) und der Lösung",
            "Zusage der korrigierten Rechnung (100 Pinsel Größe S, grüne Farbe)",
            "Bestätigung des gewohnten Rabatts von 10 % und Dank für die langjährige Treue"
        ],
        "min_words": 150,
        "time_minutes": 45,
        "redemittel": redemittel_beschwerde
    },
    {
        "id": "schr-b-p76",
        "category": "beschwerde",
        "kind": "schreiben",
        "label": "Beschwerde 12: Mangelhafte Lieferung – beschädigte Hosen, fehlende T-Shirts",
        "topic": "Reklamation von Textilien und Nachlieferung",
        "page": 76,
        "source_variant": 8,
        "scenario": "Der Kunde Matthias Schramm beanstandet zwei Punkte: Die Verpackungen der Hosen (Größe M und L) wurden beim Transport beschädigt, sodass die Ware verschmutzt ist, und von 100 bezahlten T-Shirts mit Aufdruck wurde nur die Hälfte geliefert. Er fordert 60 % Preisnachlass und kostenlose Nachlieferung bis zum 10.05.",
        "source_letter": "Sehr geehrter Herr Mayer,\n\nleider müssen wir Ihnen mitteilen, dass Ihre Lieferung nicht zu unserer Zufriedenheit ausgefallen ist. Wir müssen zwei Punkte beanstanden. Erstens wurden die Verpackungen der Hosen (Größe M und L) beim Transport beschädigt, sodass der Inhalt verschmutzt ist. In diesem Zustand können wir die Waren auf keinen Fall in den regulären Verkauf geben, sondern sie nur mit einem Rabatt anbieten. Wir halten daher einen Preisnachlass von 60 % für angemessen. Des Weiteren teilen wir Ihnen mit, dass von den T-Shirts mit Aufdruck statt der bezahlten 100 Stück nur die Hälfte geliefert wurde. Wegen der beginnenden Sommersaison bitten wir um schnellstmögliche Nachlieferung der fehlenden Stückzahl auf Ihre Kosten spätestens bis zum 10.05. Wir hoffen, dass sich derartige Vorkommnisse in Zukunft vermeiden lassen, und bitten um prompte Erledigung.\n\nMit freundlichen Grüßen\nMatthias Schramm",
        "boss_instructions": "Hallo, mich erreichte die untenstehende E-Mail. Bitte kümmern Sie sich darum und antworten Sie dem Kunden höflich. Entschuldigen Sie sich für die verschmutzte Ware. Der geforderte Rabatt von 60 % ist unverschämt; bieten Sie ihm eine andere Lösung an. Die Nachlieferung der T-Shirts ist wegen unserer Mitarbeitersituation leider erst bis zum 12.05. möglich. Erklären Sie den Grund.",
        "prompt": "Schreiben Sie eine E-Mail an Herrn Schramm. Behandeln Sie dabei die folgenden vier Punkte:",
        "leitpunkte": [
            "Entschuldigung für die beschädigte und verschmutzte Ware",
            "Ablehnung des geforderten Rabatts von 60 % und Angebot einer anderen Lösung",
            "Erklärung, warum die Nachlieferung der T-Shirts erst bis zum 12.05. möglich ist",
            "Höflicher Ausblick auf die weitere Zusammenarbeit und Bitte um Verständnis"
        ],
        "min_words": 150,
        "time_minutes": 45,
        "redemittel": redemittel_beschwerde
    },
    {
        "id": "schr-b-p77",
        "category": "beschwerde",
        "kind": "schreiben",
        "label": "Beschwerde 13: Pflanzenlieferung – unpassende Auswahl für die Messe",
        "topic": "Pflanzendekoration für Veranstaltungen",
        "page": 77,
        "source_variant": 9,
        "scenario": "Frau Talheim beanstandet die Pflanzen- und Blumenauswahl für ihre Ausstellung zum Thema Nachhaltigkeit: importierte exotische Pflanzen im Eingangsbereich und Orchideen in den Sträußen für den Umweltpreis. Sie musste kurzfristig Ersatz bei einem Aussteller beschaffen und verlangt die Erstattung dieser Kosten.",
        "source_letter": "Sehr geehrter Herr Herrmann,\n\nleider müssen wir Ihnen mitteilen, dass Ihre Pflanzen- und Blumenauswahl für unsere letzte Veranstaltung gänzlich unpassend war. Wie Sie wissen, war das Thema unserer Ausstellung in der vergangenen Woche: „Nachhaltigkeit & Umweltverträglichkeit im Gartenbau – Lokal und Regional“. Und Sie haben im Eingangsbereich aus dem fernen Ausland importierte exotische Pflanzen platziert, was verständlicherweise zu Beschwerden von Seiten der Besucher geführt hat. Zudem wollten wir den diesjährigen Umweltpreis zusammen mit Blumensträußen vergeben. Diese waren aber mit Orchideen bestückt. Wie passt das zum Thema „regional“? In dieser Situation haben wir daher entschieden, kurzfristigen Ersatz für die Sträuße von einem Aussteller zu beschaffen. Wir bitten Sie, diese zusätzlichen Kosten zu ersetzen. Solche Vorkommnisse müssen in Zukunft unter allen Umständen vermieden werden. Wir erwarten Ihre Vorschläge und stehen für ein Gespräch jederzeit zur Verfügung.\n\nMit freundlichen Grüßen\nGabi Talheim",
        "boss_instructions": "Hallo, die folgende E-Mail ist gestern bei mir eingegangen. Was war denn da los? Bitte antworten Sie der Kundin höflich und machen Sie Vorschläge für unsere weitere Zusammenarbeit. Wir schätzen Frau Talheim als langjährige Kundin und möchten sie deshalb nicht verlieren. Teilen Sie ihr bitte auch mit, was wir ihr als Entschädigung für die entstandenen Unannehmlichkeiten anbieten.",
        "prompt": "Schreiben Sie eine E-Mail an Frau Talheim. Behandeln Sie dabei die folgenden vier Punkte:",
        "leitpunkte": [
            "Entschuldigung für die unpassende Pflanzen- und Blumenauswahl",
            "Erklärung, wie es zu dem Fehler kam, und Zusage, dass er sich nicht wiederholt",
            "Zusage, die zusätzlichen Kosten für den kurzfristigen Ersatz zu übernehmen",
            "Konkretes Entschädigungsangebot und Vorschläge für die weitere Zusammenarbeit"
        ],
        "min_words": 150,
        "time_minutes": 45,
        "redemittel": redemittel_beschwerde
    }
]

foren = [
    {
        "id": "schr-f-homeoffice",
        "category": "forum",
        "kind": "schreiben",
        "label": "Forum 1: Homeoffice und mobiles Arbeiten",
        "topic": "Homeoffice vs. Präsenzpflicht",
        "page": 102,
        "scenario": "In Ihrem Unternehmen plant die Geschäftsleitung, die bestehende Homeoffice-Regelung einzuschränken. Mitarbeiter sollen künftig wieder mindestens vier Tage pro Woche im Büro anwesend sein, um Teamgeist und Kommunikation zu stärken. Im Intranet-Forum diskutieren die Beschäftigten darüber.",
        "prompt": "Schreiben Sie einen Beitrag für das Diskussionsforum Ihrer Firma. Behandeln Sie dabei die folgenden vier Punkte:",
        "leitpunkte": [
            "Äußern Sie Ihre persönliche Meinung zu der geplanten Präsenzpflicht.",
            "Nennen Sie je zwei Vor- und Nachteile von Homeoffice für Arbeitnehmer und Betrieb.",
            "Beschreiben Sie Ihre eigenen Arbeitsgewohnheiten und Erfahrungen.",
            "Machen Sie konkrete Vorschläge für ein flexibles und faires Hybridmodell."
        ],
        "min_words": 150,
        "time_minutes": 45,
        "redemittel": redemittel_forum
    },
    {
        "id": "schr-f-weiterbildung",
        "category": "forum",
        "kind": "schreiben",
        "label": "Forum 2: Weiterbildung am Wochenende",
        "topic": "Betriebliche Fortbildung",
        "page": 99,
        "scenario": "Die Geschäftsführung möchte Fortbildungen und Seminare künftig ausschließlich an Samstagen oder außerhalb der regulären Arbeitszeit anbieten, damit keine Arbeitszeit verloren geht. Die Kursgebühren übernimmt die Firma, die Freizeit müssen die Mitarbeiter investieren.",
        "prompt": "Schreiben Sie einen Beitrag für das Diskussionsforum Ihrer Firma. Behandeln Sie dabei die folgenden vier Punkte:",
        "leitpunkte": [
            "Nehmen Sie Stellung zum Vorschlag von Schulungen in der Freizeit.",
            "Erläutern Sie Vor- und Nachteile dieser Regelung für Mitarbeiter und Unternehmen.",
            "Berichten Sie über Erfahrungen mit Fortbildungen in Ihrem bisherigen Berufsleben.",
            "Schlagen Sie alternative Arbeitszeit- oder Vergütungsmodelle für Weiterbildungen vor."
        ],
        "min_words": 150,
        "time_minutes": 45,
        "redemittel": redemittel_forum
    },
    {
        "id": "schr-f-jobticket",
        "category": "forum",
        "kind": "schreiben",
        "label": "Forum 3: Kostenloses Jobticket gegen Parkplatzgebühr",
        "topic": "Betriebliche Mobilität und Umwelt",
        "page": 99,
        "scenario": "Das Unternehmen plant, allen Beschäftigten ein kostenloses Jobticket für den öffentlichen Nahverkehr zur Verfügung zu stellen. Zur Finanzierung und aus Umweltschutzgründen soll das Parken auf dem firmeneigenen Parkplatz künftig 50 Euro monatlich kosten.",
        "prompt": "Schreiben Sie einen Beitrag für das Diskussionsforum Ihrer Firma. Behandeln Sie dabei die folgenden vier Punkte:",
        "leitpunkte": [
            "Beziehen Sie Stellung zu der Einführung von Parkplatzgebühren für Mitarbeiter.",
            "Wägen Sie Vor- und Nachteile von Jobtickets und PKW-Nutzung ab.",
            "Schildern Sie Ihre eigene Pendelsituation und Mobilitätserfahrungen.",
            "Formulieren Sie Kompromissvorschläge für Kolleginnen und Kollegen im ländlichen Raum."
        ],
        "min_words": 150,
        "time_minutes": 45,
        "redemittel": redemittel_forum
    },
    {
        "id": "schr-f-krankmeldung",
        "category": "forum",
        "kind": "schreiben",
        "label": "Forum 4: Ärztliche Krankmeldung ab Tag 1",
        "topic": "Krankmeldung und Fehlzeiten",
        "page": 98,
        "scenario": "Aufgrund hoher Fehlzeiten an Freitagen und Montagen plant das Management, dass alle Mitarbeiterinnen und Mitarbeiter im Krankheitsfall bereits ab dem ersten Tag ein ärztliches Attest (AU-Bescheinigung) vorlegen müssen.",
        "prompt": "Schreiben Sie einen Beitrag für das Diskussionsforum Ihrer Firma. Behandeln Sie dabei die folgenden vier Punkte:",
        "leitpunkte": [
            "Geben Sie Ihre Meinung zur Pflicht der Krankschreibung ab dem ersten Krankheitstag ab.",
            "Stellen Sie Vor- und Nachteile für die Firma, die Beschäftigten und Arztpraxen dar.",
            "Erzählen Sie von Regelungen an früheren Arbeitsplätzen oder in Ihrem Heimatland.",
            "Schlagen Sie Maßnahmen vor, um Vertrauen und Gesundheit am Arbeitsplatz zu fördern."
        ],
        "min_words": 150,
        "time_minutes": 45,
        "redemittel": redemittel_forum
    },
    {
        "id": "schr-f-4tage-woche",
        "category": "forum",
        "kind": "schreiben",
        "label": "Forum 5: Einführung einer 4-Tage-Woche (10 Std./Tag)",
        "topic": "Flexible Arbeitszeitmodelle",
        "page": 104,
        "scenario": "Die Personalabteilung regt an, ein Modell der 4-Tage-Woche zu testen: 40 Wochenstunden verteilt auf 4 Tage zu je 10 Stunden Arbeitszeit, mit einem zusätzlichen freien Wochentag. Es wird diskutiert, ob dieses Modell verpflichtend oder freiwillig sein soll.",
        "prompt": "Schreiben Sie einen Beitrag für das Diskussionsforum Ihrer Firma. Behandeln Sie dabei die folgenden vier Punkte:",
        "leitpunkte": [
            "Bewerten Sie das Konzept einer 4-Tage-Woche mit 10-Stunden-Arbeitstagen.",
            "Diskutieren Sie Vor- und Nachteile hinsichtlich Konzentration, Erholung und Familie.",
            "Berichten Sie, wie sich dieses Modell auf Ihren persönlichen Arbeitsalltag auswirken würde.",
            "Schlagen Sie praxistaugliche Rahmenbedingungen (z. B. Kernzeiten, Freiwilligkeit) vor."
        ],
        "min_words": 150,
        "time_minutes": 45,
        "redemittel": redemittel_forum
    },
    {
        "id": "schr-f-privattelefonate",
        "category": "forum",
        "kind": "schreiben",
        "label": "Forum 6: Smartphone-Nutzung am Arbeitsplatz",
        "topic": "Handynutzung während der Arbeitszeit",
        "page": 98,
        "scenario": "Die Geschäftsführung möchte private Mobiltelefone während der Arbeitszeit komplett verbieten. Handys sollen während der Schicht im Spind des Aufenthaltsraums bleiben und dürfen nur in den Pausen benutzt werden.",
        "prompt": "Schreiben Sie einen Beitrag für das Diskussionsforum Ihrer Firma. Behandeln Sie dabei die folgenden vier Punkte:",
        "leitpunkte": [
            "Nehmen Sie Stellung zum generellen Smartphone-Verbot am Arbeitsplatz.",
            "Wägen Sie Vor- und Nachteile (Ablenkung vs. familiäre Notfälle/Erreichbarkeit) ab.",
            "Schildern Sie Ihre eigenen Erfahrungen mit Smartphone-Nutzung im Berufsleben.",
            "Machen Sie Vorschläge für eine angemessene und vertrauensvolle Betriebsvereinbarung."
        ],
        "min_words": 150,
        "time_minutes": 45,
        "redemittel": redemittel_forum
    },
    {
        "id": "schr-f-hunde-buero",
        "category": "forum",
        "kind": "schreiben",
        "label": "Forum 7: Hunde im Büro erlauben",
        "topic": "Tiere am Arbeitsplatz",
        "page": 105,
        "scenario": "Mehrere Kolleginnen und Kollegen haben beantragt, ihre Hunde mit ins Büro bringen zu dürfen. In der Belegschaft gibt es dazu sowohl große Zustimmung als auch erhebliche Bedenken wegen Allergien und Hygiene.",
        "prompt": "Schreiben Sie einen Beitrag für das Diskussionsforum Ihrer Firma. Behandeln Sie dabei die folgenden vier Punkte:",
        "leitpunkte": [
            "Beziehen Sie klar Position zum Thema «Bürohunde».",
            "Nennen Sie Vor- und Nachteile für das Arbeitsklima, die Gesundheit und Tierhalter.",
            "Beschreiben Sie Ihre eigenen Erfahrungen oder die Haltung zu Haustieren in Ihrem Heimatland.",
            "Formulieren Sie konkrete Regeln und Voraussetzungen für eine eventuelle Genehmigung."
        ],
        "min_words": 150,
        "time_minutes": 45,
        "redemittel": redemittel_forum
    },
    {
        "id": "schr-f-kantine",
        "category": "forum",
        "kind": "schreiben",
        "label": "Forum 8: Nur noch vegetarisches/veganes Essen in der Kantine",
        "topic": "Ernährung und Nachhaltigkeit im Betrieb",
        "page": 100,
        "scenario": "Die Betriebsleitung schlägt vor, aus Gründen des Klimaschutzes und der Mitarbeitergesundheit den Speiseplan der Firmenkantine komplett auf fleischlose (vegetarische und vegane) Kost umzustellen.",
        "prompt": "Schreiben Sie einen Beitrag für das Diskussionsforum Ihrer Firma. Behandeln Sie dabei die folgenden vier Punkte:",
        "leitpunkte": [
            "Äußern Sie Ihre Meinung zu einer rein vegetarischen/veganen Betriebskantine.",
            "Stellen Sie Vor- und Nachteile für Gesundheit, Umwelt und persönliche Wahlfreiheit dar.",
            "Erzählen Sie von Ihren eigenen Verpflegungsgewohnheiten während des Arbeitstages.",
            "Schlagen Sie ausgewogene Kompromisse vor (z. B. Veggie-Tage, Kennzeichnung von Fleischqualität)."
        ],
        "min_words": 150,
        "time_minutes": 45,
        "redemittel": redemittel_forum
    }
]

data_beschwerde = {
    "block": "schreiben_beschwerde",
    "section": "schreiben-beschwerde",
    "variants": beschwerden
}

with open(r"quiz\data\schreiben_beschwerde.json", "w", encoding="utf-8") as f:
    json.dump(data_beschwerde, f, ensure_ascii=False, indent=1)

# OJO: este script NO escribe el catálogo de foros. La lista `foren` de arriba es
# un subconjunto antiguo (8 temas) y volcarla encima borraba los 66 temas que
# genera make_full_forums.py. Para los foros: python quiz/make_full_forums.py
print(f"OK: {len(beschwerden)} Beschwerden en quiz/data/schreiben_beschwerde.json "
      f"(los foros los genera make_full_forums.py)")
