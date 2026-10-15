import json
import re

def norm(s):
    return re.sub(r"\s+", " ", str(s or "")).strip()

# --- Variante 2 (p. 35) ---
v_p35 = {
    "id": "t3_b-p35",
    "label": "Variante 2 (Ausbildung und Familie)",
    "page": 35,
    "note": "Foro sobre compatibilidad de formación profesional (Ausbildung), familia, embarazo y edad.",
    "kind": "zuordnung",
    "optionsLabel": "Kommentare",
    "intro": "Lesen Sie die vier Aufgaben (10–13) und die sechs Kommentare (a–f). Welcher Kommentar passt zu welcher Aufgabe? Zwei Kommentare bleiben übrig.",
    "passage": "",
    "options": [
        {
            "key": "a",
            "title": "Susi, vor 1 Stunde",
            "text": "Solange du so nicht weniger arbeitest als im Vertrag vereinbart, müsstest du rechtlich auf der sicheren Seite sein. Wenn du es genau wissen willst, solltest du in diesem Fall einen Anwalt für Arbeitsrecht kontaktieren. Mit einer Rechtsschutzversicherung wird das auch nicht so teuer.",
            "distractor": ""
        },
        {
            "key": "b",
            "title": "Julia, vor 1 Stunde",
            "text": "Rein rechtlich kannst du das nicht ohne Zustimmung deiner Eltern machen. Sie müssen die Kündigung sogar unterschreiben. An deiner Stelle würde ich mir das aber noch mal überlegen. Ich kann deinen Vater jedenfalls gut verstehen. Er macht sich halt Sorgen um deine Zukunft.",
            "distractor": ""
        },
        {
            "key": "c",
            "title": "Jürgen, vor 2 Stunden",
            "text": "Hi, ich würde die Ausbildung auf keinen Fall abbrechen. Mit Berufen im Finanzbereich hast du gute Aussichten auf dem Arbeitsmarkt und verdienst später auch gutes Geld. Mach dir das nicht kaputt. Meine Tochter ist Steuerberaterin und sucht händeringend nach fähigen Mitarbeitern. Sie kann sich vor Aufträgen gar nicht retten.",
            "distractor": ""
        },
        {
            "key": "d",
            "title": "Jochen, vor 5 Stunden",
            "text": "Also ich würde noch warten, bis dein Kind etwas größer ist, und mich jetzt noch nicht um einen Ausbildungsplatz bewerben. Wenn es etwas selbstständiger ist, wird vieles leichter. Eine Ausbildung kannst du auch in drei oder vier Jahren noch machen. Dein Kind braucht dich jetzt.",
            "distractor": "Aconseja posponer la solicitud de formación profesional hasta que el niño crezca, pero Jacqueline ya ha comenzado su Ausbildung y Hans-Peter ya tiene a su hijo criado."
        },
        {
            "key": "e",
            "title": "Achim, vor 6 Stunden",
            "text": "Schutz von Leben und Gesundheit ist das oberste Gebot. Um dich und dein Kind zu schützen, darfst du während der Schwangerschaft keine körperlich anstrengenden Arbeiten verrichten und auch Tätigkeiten, bei denen du Lärm, Schmutz, Kälte usw. ausgesetzt bist, sind tabu.",
            "distractor": "Explica normas generales de protección de la salud durante el embarazo (Mutterschutz: prohibición de trabajo físico pesado o ruidoso), pero no responde a si interrumpir o no la formación."
        },
        {
            "key": "f",
            "title": "Peter, vor 12 Stunden",
            "text": "Warum das denn? Es gibt doch heutzutage Möglichkeiten, das Kind unterzubringen, während man arbeitet. Können dich deine Eltern vielleicht unterstützen? Sprich mal mit deinem Chef! Wenn der sieht, dass dir die Ausbildung wichtig ist, wird sich eine Lösung finden. Aber versuch auf jeden Fall, die Ausbildung durchzuziehen.",
            "distractor": ""
        }
    ],
    "items": [
        {
            "n": 10,
            "type": "choice",
            "prompt": "Inka: Ich bin Auszubildende in einem Büro und muss immer pünktlich Feierabend machen, weil ich meinen einjährigen Sohn von der Krippe abholen muss. Mein Chef sieht das gar nicht gern und droht mir jetzt sogar mit Kündigung. Was soll ich machen?",
            "answer": "a",
            "confidence": "hoch",
            "quote": "Solange du so nicht weniger arbeitest als im Vertrag vereinbart, müsstest du rechtlich auf der sicheren Seite sein. Wenn du es genau wissen willst, solltest du in diesem Fall einen Anwalt für Arbeitsrecht kontaktieren.",
            "explain": "Inka cumple con su jornada pero debe salir puntual para recoger a su hijo de la guardería y el jefe la amenaza con el despido. Susi (a) le aclara que mientras trabaje las horas contractuales está protegida legalmente y le recomienda consultar a un abogado laboralista."
        },
        {
            "n": 11,
            "type": "choice",
            "prompt": "Jacqueline: Hallo Leute! Vor ein paar Monaten habe ich mit einer Ausbildung begonnen. Und jetzt bin ich schwanger... Was soll ich bloß machen? Es wird bestimmt schwierig, Kind und Arbeit zu vereinbaren. Soll ich die Ausbildung abbrechen?",
            "answer": "f",
            "confidence": "hoch",
            "quote": "Aber versuch auf jeden Fall, die Ausbildung durchzuziehen.",
            "explain": "Jacqueline se ha quedado embarazada al poco de iniciar la formación y duda si abandonarla («Soll ich die Ausbildung abbrechen?»). Peter (f) la anima vehementemente a no dejarla («durchzuziehen»), buscar guardería o apoyo familiar y hablar con el jefe para buscar una solución."
        },
        {
            "n": 12,
            "type": "choice",
            "prompt": "Hans-Peter: Guten Abend, ich bin Ende 40 und mein Sohn ist inzwischen erwachsen. Jetzt möchte ich beruflich was ganz Neues machen und eine Ausbildung zum Steuerfachangestellten anfangen. Meint ihr, ich habe in meinem Alter noch Chancen, in diesem Beruf zu arbeiten?",
            "answer": "c",
            "confidence": "hoch",
            "quote": "Mit Berufen im Finanzbereich hast du gute Aussichten auf dem Arbeitsmarkt und verdienst später auch gutes Geld. Mach dir das nicht kaputt. Meine Tochter ist Steuerberaterin und sucht händeringend nach fähigen Mitarbeitern.",
            "explain": "Hans-Peter pregunta si a sus casi 50 años tiene posibilidades en el sector fiscal («Steuerfachangestellten»). Jürgen (c) confirma las excelentes perspectivas laborales en el ámbito financiero y cita a su hija asesora fiscal, que busca personal urgentemente."
        },
        {
            "n": 13,
            "type": "choice",
            "prompt": "Max: Hallo, ich mache momentan eine Ausbildung zum Einzelhandelskaufmann. Ich habe noch ein Jahr bis zum Abschluss und habe wirklich keine Lust mehr. Mein Vater möchte, dass ich die Ausbildung fertig mache. Ich bin noch nicht 18. Kann ich trotzdem einfach kündigen?",
            "answer": "b",
            "confidence": "hoch",
            "quote": "Rein rechtlich kannst du das nicht ohne Zustimmung deiner Eltern machen. Sie müssen die Kündigung sogar unterschreiben.",
            "explain": "Max es menor de edad («Ich bin noch nicht 18») y pregunta si puede rescindir su contrato por su cuenta contra el deseo de su padre. Julia (b) le advierte de que legalmente los menores no pueden rescindir la formación sin el consentimiento y la firma de sus padres."
        }
    ]
}

# --- Variante 3 (p. 36) ---
v_p36 = {
    "id": "t3_b-p36",
    "label": "Variante 3 (Arbeitszeit und Familie)",
    "page": 36,
    "note": "Foro sobre trabajo en sábado, ampliación de jornada parcial a completa y excedencias.",
    "kind": "zuordnung",
    "optionsLabel": "Kommentare",
    "intro": "Lesen Sie die vier Aufgaben (10–13) und die sechs Kommentare (a–f). Welcher Kommentar passt zu welcher Aufgabe? Zwei Kommentare bleiben übrig.",
    "passage": "",
    "options": [
        {
            "key": "a",
            "title": "Thilo, vor 45 Minuten",
            "text": "In meinen Augen ist Familie das Wichtigste auf der Welt. Es ist doch auch ein Gewinn, wenn man mehr Zeit mit seinen Kindern verbringen kann und weniger gestresst ist. Ich würde mich auf jeden Fall für Teilzeit entscheiden.",
            "distractor": ""
        },
        {
            "key": "b",
            "title": "Henny, vor 1 Stunde",
            "text": "Also ich finde es nicht gut, wenn Geschäfte und Supermärkte an Samstagen so lange geöffnet sind. Ihr müsst doch bedenken, dass dort auch Menschen arbeiten müssen. Sie wollen doch ebenfalls Wochenende haben und zu ihren Familien. Ich bin ganz klar gegen längere Ladenöffnungszeiten.",
            "distractor": "Opina en contra de los horarios comerciales prolongados en sábado para los dependientes de tiendas; no responde a ninguna de las consultas individuales de oficina/jornada."
        },
        {
            "key": "c",
            "title": "Angela, vor 6 Stunden",
            "text": "Jeder Arbeitnehmer hat einen Rechtsanspruch auf Teilzeitarbeit. Allerdings musst du länger als sechs Monate bei dem Unternehmen beschäftigt sein. Man muss sich das aber genau überlegen, da man nicht nur kurz- oder mittelfristig weniger verdient, sondern auch weniger Rentenansprüche hat. Schau doch mal im Internet, wie viel das ausmacht.",
            "distractor": ""
        },
        {
            "key": "d",
            "title": "Ratna, vor 2 Stunden",
            "text": "Seit Kurzem haben Arbeitnehmer das Recht, eine befristete Zeit weniger zu arbeiten, aber das gilt bestimmt nicht rückwirkend. Soviel ich weiß, hast du also keinen Anspruch, in die Vollzeit zurückzukehren. Sprich doch einfach mal mit deinem Chef.",
            "distractor": ""
        },
        {
            "key": "e",
            "title": "Alex, vor 30 Minuten",
            "text": "Der Samstag ist ein normaler Werktag und deshalb kann der Arbeitgeber anordnen, dass an diesem Tag auch gearbeitet wird. Dabei spielt es keine Rolle, ob du Kinder hast oder nicht. Oft ist es aber auch so, dass du dann an einem anderen Tag in der Woche frei bekommst.",
            "distractor": ""
        },
        {
            "key": "f",
            "title": "Gerhard, vor 3 Stunden",
            "text": "Also ich würde mir das gut überlegen. Wenn du bisher gut über die Runden gekommen bist, könntest du dir doch etwas mehr Freizeit gönnen. Meines Erachtens geht es hier auch um mehr Lebensqualität. Das Leben ist zu kurz, um nur zu arbeiten.",
            "distractor": "Reflexión filosófica sobre valorar el tiempo libre y la calidad de vida, pero sin asesorar sobre consecuencias legales o financieras concretas."
        }
    ],
    "items": [
        {
            "n": 10,
            "type": "choice",
            "prompt": "Soma: Meine Kinder sind unter der Woche ganztags in der Kita, damit ich Vollzeit arbeiten kann. Jetzt soll ich in den nächsten Wochen samstags ins Büro kommen. Ich habe aber niemanden, der da auf meine Kinder aufpassen kann. Kann der Arbeitgeber das verlangen?",
            "answer": "e",
            "confidence": "hoch",
            "quote": "Der Samstag ist ein normaler Werktag und deshalb kann der Arbeitgeber anordnen, dass an diesem Tag auch gearbeitet wird. Dabei spielt es keine Rolle, ob du Kinder hast oder nicht.",
            "explain": "Soma pregunta si su empresa puede obligarla a acudir en sábado teniendo hijos pequeños. Alex (e) responde directamente que el sábado es día laborable («Werktag») y el empleador puede ordenar trabajar en él con independencia de las cargas familiares."
        },
        {
            "n": 11,
            "type": "choice",
            "prompt": "Reinhold: Ich arbeite seit zwölf Jahren 20 Stunden die Woche und würde jetzt gerne, weil die Kinder aus dem Haus sind, meine Arbeitszeit aufstocken und wieder Vollzeit arbeiten. Habe ich ein Recht darauf ?",
            "answer": "d",
            "confidence": "hoch",
            "quote": "Soviel ich weiß, hast du also keinen Anspruch, in die Vollzeit zurückzukehren. Sprich doch einfach mal mit deinem Chef.",
            "explain": "Reinhold lleva doce años a media jornada y pregunta si tiene derecho legal a pasar a jornada completa. Ratna (d) le aclara que la nueva regulación de jornada reducida temporal no opera con carácter retroactivo para su caso antiguo, por lo que no existe ese derecho automático."
        },
        {
            "n": 12,
            "type": "choice",
            "prompt": "Mandy: Seit zwei Jahren arbeite ich Vollzeit in einem Unternehmen und dieser Job macht mir auch viel Spaß. Aus familiären Gründen würde ich gerne eine dreijährige Auszeit nehmen. Ich überlege, ob ich mir das finanziell leisten kann.",
            "answer": "c",
            "confidence": "hoch",
            "quote": "Man muss sich das aber genau überlegen, da man nicht nur kurz- oder mittelfristig weniger verdient, sondern auch weniger Rentenansprüche hat.",
            "explain": "Mandy evalúa una pausa de tres años o reducción laboral por motivos familiares y duda del impacto económico. Angela (c) explica el derecho a reducir jornada pero advierte del impacto en los ingresos y especialmente en la reducción de las futuras pensiones de jubilación («weniger Rentenansprüche»)."
        },
        {
            "n": 13,
            "type": "choice",
            "prompt": "Nici: Ich bekomme jetzt das zweite Kind und werde danach wahrscheinlich erst mal Teilzeit arbeiten. Jetzt habe ich ziemlich große Angst, dass ich in meiner Karriere den Anschluss verpasse. Soll ich vielleicht doch so schnell wie möglich wieder Vollzeit arbeiten?",
            "answer": "a",
            "confidence": "hoch",
            "quote": "In meinen Augen ist Familie das Wichtigste auf der Welt. Es ist doch auch ein Gewinn, wenn man mehr Zeit mit seinen Kindern verbringen kann und weniger gestresst ist. Ich würde mich auf jeden Fall für Teilzeit entscheiden.",
            "explain": "Nici duda entre optar por la jornada reducida tras su segundo hijo o volver rápido a jornada completa por miedo a frenar su carrera. Thilo (a) le aconseja priorizar a la familia y decantarse sin dudar por el tiempo parcial («Ich würde mich auf jeden Fall für Teilzeit entscheiden»)."
        }
    ]
}

# --- Variante 4 (p. 37) ---
v_p37 = {
    "id": "t3_b-p37",
    "label": "Variante 4 (Urlaub und Dienstplan)",
    "page": 37,
    "note": "Foro sobre días de vacaciones legales, turnos de trabajo imprevistos, anulación de vacaciones concedidas y trabajo en fin de semana durante prácticas.",
    "kind": "zuordnung",
    "optionsLabel": "Kommentare",
    "intro": "Lesen Sie die vier Aufgaben (10–13) und die sechs Kommentare (a–f). Welcher Kommentar passt zu welcher Aufgabe? Zwei Kommentare bleiben übrig.",
    "passage": "",
    "options": [
        {
            "key": "a",
            "title": "Cécile, vor 3 Stunden",
            "text": "Leider muss ich dich enttäuschen. Die Regelung ist gesetzeskonform. Das Minimum liegt sogar nur bei 20 Tagen. Sei froh, dass du mehr hast. Bei manchen Arbeitgebern erhöht sich der Urlaubsanspruch mit längerer Firmenzugehörigkeit.",
            "distractor": ""
        },
        {
            "key": "b",
            "title": "Limit, vor 5 Stunden",
            "text": "Meines Wissens gibt es keine gesetzliche Regelung dafür, aber sprich doch einfach mal mit eurem Chef. Dem ist vielleicht gar nicht klar, dass du das nicht so toll findest, wenn du immer erst so kurz vorher weißt, an welchen Tagen du arbeiten musst und wann du frei hast.",
            "distractor": ""
        },
        {
            "key": "c",
            "title": "Susanne, vor 3 Stunden",
            "text": "Urlaub muss immer rechtzeitig beantragt werden, aber der Arbeitgeber ist nicht unbedingt verpflichtet, ihn zu gewähren. Wann Urlaub genommen werden darf, entscheidet der Chef. Aufgrund dringender betrieblicher Gründe kann ein Urlaubsantrag auch abgelehnt werden.",
            "distractor": "Trata de la solicitud inicial de vacaciones y la posibilidad patronal de denegarla por motivos de servicio; no responde al caso de Hans, cuyas vacaciones ya estaban aprobadas formalmente."
        },
        {
            "key": "d",
            "title": "Nico, vor 30 Minuten",
            "text": "Schau doch mal in deinen Arbeitsvertrag, da ist das sicher geregelt. Soviel ich weiß, gibt es keine gesetzlichen Einschränkungen für angestellte Arbeitnehmer. Allerdings darfst du keine sieben Tage am Stück arbeiten. Der Samstag gilt in Deutschland als normalen Wochentag.",
            "distractor": ""
        },
        {
            "key": "e",
            "title": "Greta, vor 2 Stunden",
            "text": "Ich arbeite auch im Einzelhandel und bei uns ist es so geregelt, dass man einen festen Wochentag freibekommt, wenn man immer samstags arbeitet. Das kommt mir entgegen. So kann ich entspannt unter der Woche einkaufen oder ins Schwimmbad gehen.",
            "distractor": "Comenta su experiencia personal librando entre semana en el comercio, pero no responde a si es legal exigir turnos sin antelación o trabajar en sábado."
        },
        {
            "key": "f",
            "title": "Michele, vor 6 Stunden",
            "text": "Das kann dein Chef nicht einfach so machen. Personelle Engpässe reichen für den Widerruf eines Urlaubsantrags nicht aus. Wenn du deinen Urlaub tatsächlich nicht antrittst, muss der Arbeitgeber alle Kosten tragen, die dir durch die Urlaubsverschiebung entstehen.",
            "distractor": ""
        }
    ],
    "items": [
        {
            "n": 10,
            "type": "choice",
            "prompt": "Thia: Voll gemein, ich habe nur 25 Urlaubstage! Mein Freund hat hingegen 30 Tage im Jahr. Ich frage mich, ob mir nicht auch mehr Tage zustehen. Kennt sich von euch da jemand aus?",
            "answer": "a",
            "confidence": "hoch",
            "quote": "Leider muss ich dich enttäuschen. Die Regelung ist gesetzeskonform. Das Minimum liegt sogar nur bei 20 Tagen. Sei froh, dass du mehr hast.",
            "explain": "Thia se queja de tener solo 25 días de vacaciones. Cécile (a) le aclara que 25 días se ajusta plenamente a la ley, ya que el mínimo legal en Alemania es de 20 días laborables para jornadas de 5 días."
        },
        {
            "n": 11,
            "type": "choice",
            "prompt": "Marilena: Ich arbeite im Einzelhandel und bei uns gilt jede Woche ein anderer Dienstplan. Wir bekommen den Plan immer erst am Ende der Vorwoche und deshalb können wir unsere Freizeit natürlich auch nicht richtig planen. Ist das erlaubt?",
            "answer": "b",
            "confidence": "hoch",
            "quote": "Meines Wissens gibt es keine gesetzliche Regelung dafür, aber sprich doch einfach mal mit eurem Chef. Dem ist vielleicht gar nicht klar, dass du das nicht so toll findest, wenn du immer erst so kurz vorher weißt, an welchen Tagen du arbeiten musst",
            "explain": "Marilena recibe el cuadrante horario a finales de la semana previa impidiéndole organizar su vida personal. Limit (b) le comenta la ausencia de una regulación rígida y le aconseja hablar con el jefe para comunicarle el problema de los avisos con tan poco margen."
        },
        {
            "n": 12,
            "type": "choice",
            "prompt": "Hans: Ich habe nach der Genehmigung meines Urlaubs diesen gebucht und jetzt hat mein Chef gemerkt, dass ein anderer Kollege schon vorher zur selben Zeit Urlaub eingereicht hat. Jetzt will er mir meinen wieder streichen. Darf er das?",
            "answer": "f",
            "confidence": "hoch",
            "quote": "Das kann dein Chef nicht einfach so machen. Personelle Engpässe reichen für den Widerruf eines Urlaubsantrags nicht aus.",
            "explain": "Hans ya tenía sus vacaciones autorizadas y contratadas y el jefe pretende cancelárselas. Michele (f) le confirma que una empresa no puede anular unilateralmente unas vacaciones ya concedidas por falta de personal y que debería asumir los costes derivados."
        },
        {
            "n": 13,
            "type": "choice",
            "prompt": "Lisa: Ich mache zurzeit ein Pflichtpraktikum in einem Unternehmen und arbeite von Montag bis Freitag acht Stunden täglich. Jetzt soll ich nächsten Samstag auch noch kommen. Bin ich dazu verpflichtet? Ich fühle mich ein bisschen ausgenutzt!",
            "answer": "d",
            "confidence": "hoch",
            "quote": "Allerdings darfst du keine sieben Tage am Stück arbeiten. Der Samstag gilt in Deutschland als normalen Wochentag.",
            "explain": "Lisa hace prácticas de lunes a viernes (8h/día) y le ordenan trabajar el sábado. Nico (d) explica que el sábado es día laborable ordinario («Werktag»), pero recuerda el límite legal de que no se pueden encadenar siete días consecutivos sin descanso."
        }
    ]
}

out_data = {
    "block": "t3_b",
    "section": "lesen-t3",
    "variants": [v_p35, v_p36, v_p37]
}

# Validaciones internas de zuordnung
for v in out_data["variants"]:
    opts_map = {o["key"]: o["text"] for o in v["options"]}
    ans_seen = set()
    for it in v["items"]:
        ans = it["answer"]
        assert ans in opts_map, f"Item answer {ans} not in options"
        assert ans not in ans_seen, f"Duplicate answer {ans} in {v['id']}"
        ans_seen.add(ans)
        # Check that quote is in the matched option text
        q = norm(it["quote"])
        opt_text = norm(opts_map[ans])
        assert q in opt_text, f"Quote '{q}' not in comment {ans} for {v['id']}"

with open(r"quiz\data\t3_b.json", "w", encoding="utf-8") as f:
    json.dump(out_data, f, ensure_ascii=False, indent=1)

print("t3_b.json generado y validado con éxito!")
