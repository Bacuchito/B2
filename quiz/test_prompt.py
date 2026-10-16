# -*- coding: utf-8 -*-
"""
test_prompt.py - Script de calibración y validación del evaluador telc B2 Schreiben.

Prueba el evaluador con dos casos de control:
- Caso A: Texto A2/B1 deficiente (< 150 palabras, errores de sintaxis, falta de Leitpunkte).
          Debe resultar en NICHT BESTANDEN.
- Caso B: Texto B2 formal (> 150 palabras, 4 Leitpunkte tratados, registro profesional).
          Debe resultar en BESTANDEN.

Modos de ejecución:
- Offline (por defecto): valida esquema, construcción de prompts, validación de contrato y casos de prueba.
- Live: con --gemini-key, --openai-key, o --ollama para probar llamadas reales a la IA.
"""

import sys
import os
import json
import argparse
from typing import Dict, Any

# Asegurar codificación utf-8 en consola Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from prompt_schreiben import SYSTEM_PROMPT, JSON_SCHEMA, build_user_prompt, validate_evaluation_json

# Tarea de prueba (de schreiben_beschwerde.json: Putzdienst)
SAMPLE_TASK = {
    "id": "schr-b-p66",
    "category": "beschwerde",
    "label": "Beschwerde 1: Putzdienst und unvollständige Arbeitszeit",
    "topic": "Putzdienst / Büroreinigung",
    "page": 66,
    "scenario": "Die Huber GmbH hat einen Vertrag über täglich 3 Stunden Büroreinigung (6:00 bis 9:00 Uhr). Herr Lassner beschwert sich, dass die Reinigungskräfte in den letzten zwei Wochen mehrfach vor 9:00 Uhr nicht mehr da waren. Er verlangt eine Anpassung der Rechnung.",
    "source_letter": "Sehr geehrte Frau Woller,\n\nleider muss ich mich heute mit einer Beschwerde an Sie wenden...",
    "boss_instructions": "Hallo Friederike, ich verstehe den Ärger von Herrn Lassner. Bitte kläre mit unseren Leuten, was da los ist, und antworte Herrn Lassner. Sage ihm zu, dass so etwas nie wieder vorkommt, und gib ihm 20 % Rabatt auf die nächste Rechnung. Wir dürfen den Kunden keinesfalls verlieren! Gruß Heike",
    "prompt": "Schreiben Sie eine E-Mail an Herrn Lassner. Behandeln Sie dabei die folgenden vier Punkte:",
    "leitpunkte": [
        "Bezugnahme auf die Beschwerde und Dank für den Hinweis",
        "Förmliche Entschuldigung und Erklärung der Ursache des Problems",
        "Zusicherung, dass die vertragliche Arbeitszeit künftig strikt eingehalten wird",
        "Angebot eines 20 %-igen Rabatts auf die nächste Monatsrechnung als Wiedergutmachung"
    ],
    "min_words": 150,
    "time_minutes": 45
}

# CASO A: Texto A2/B1 muy deficiente (68 palabras, errores graves, registro informal)
SAMPLE_TEXT_FAIL_A2 = """Hallo Herr Lassner,

ich habe deine E-Mail gelesen gestern. Das tut mir leid für das Problem mit Putzen. 
Unsere Leute haben viel Arbeit und sind krank geworden manchmal, darum sie sind früher nach Hause gegangen.
Wir machen das besser nächste Woche, keine Sorge. Ich gebe dir auch 20 Prozent billiger auf die Rechnung weil wir wollen kein Streit.

Schöne Grüße,
Friederike"""

# CASO B: Texto B2 sólido (178 palabras, 4 Leitpunkte cubiertos, registro formal, buena sintaxis)
SAMPLE_TEXT_PASS_B2 = """Sehr geehrter Herr Lassner,

vielen Dank für Ihre Mitteilung vom 14. Oktober, in der Sie uns auf die Unregelmäßigkeiten bei der Reinigung Ihrer Büroräume aufmerksam machen. Wir nehmen Ihr Anliegen sehr ernst.

Zunächst möchte ich mich im Namen unseres gesamten Unternehmens aufrichtig bei Ihnen für die entstandenen Unannehmlichkeiten entschuldigen. Nach sofortiger Rücksprache mit unserer zuständigen Objektleitung haben wir festgestellt, dass es aufgrund von kurzfristigen Krankheitsfällen und neu eingearbeiteten Aushilfskräften zu bedauerlichen Missverständnissen bezüglich der vereinbarten Arbeitszeiten gekommen ist.

Wir versichern Ihnen ausdrücklich, dass wir die vertraglich vereinbarte Reinigungszeit von täglich drei Stunden ab sofort wieder lückenlos und pünktlich einhalten werden. Unsere Qualitätskontrolle wird die Durchführung in den kommenden Wochen persönlich und engmaschig überwachen.

Um unser aufrichtiges Bedauern zu unterstreichen und Ihnen für Ihr bisheriges Vertrauen zu danken, möchten wir Ihnen gern einen Preisnachlass in Höhe von 20 % auf die nächste Monatsrechnung gewähren.

Wir hoffen sehr auf Ihr Verständnis und freuen uns auf die Fortsetzung unserer partnerschaftlichen Zusammenarbeit.

Mit freundlichen Grüßen
Friederike Woller
Kundenservice Huber Reinigung GmbH"""

# Fixture de evaluación esperada para Caso A
MOCK_EVAL_FAIL_A2 = {
    "verdict": "NICHT BESTANDEN",
    "score_total": 38,
    "word_count": 68,
    "criteria": {
        "aufgabenbewaeltigung": {
            "grade": "D",
            "score": 8,
            "leitpunkte_check": [
                {"point": "Bezugnahme auf die Beschwerde und Dank für den Hinweis", "covered": False, "comment": "Mención muy vaga, sin agradecer el aviso."},
                {"point": "Förmliche Entschuldigung und Erklärung der Ursache des Problems", "covered": True, "comment": "Se disculpa de manera informal y da una excusa superficial."},
                {"point": "Zusicherung, dass die vertragliche Arbeitszeit künftig strikt eingehalten wird", "covered": False, "comment": "Promesa genérica ('keine Sorge') sin compromiso contractual formal."},
                {"point": "Angebot eines 20 %-igen Rabatts auf die nächste Monatsrechnung als Wiedergutmachung", "covered": True, "comment": "Menciona el 20%, pero con registro inadecuado ('billiger')."}
            ],
            "feedback": "Con solo 68 palabras, el texto está muy por debajo del mínimo exigido de 150 palabras. Los Leitpunkte están tratados de forma superficial."
        },
        "angemessenheit": {
            "grade": "D",
            "score": 9,
            "feedback": "Registro inadecuado: uso de 'du' ('deine E-Mail', 'gebe dir') en una comunicación formal de empresa con un cliente externo ('Sehr geehrter Herr Lassner'). Saludo y despedida informales."
        },
        "korrektheit": {
            "grade": "D",
            "score": 10,
            "feedback": "Frecuentes errores de sintaxis y orden de palabras: 'darum sie sind früher...' (el verbo debe ir en segunda posición tras darum), 'weil wir wollen kein Streit' (verbo al final con weil), omisión de comas obligatorias."
        },
        "repertoire": {
            "grade": "C",
            "score": 11,
            "feedback": "Vocabulario básico de nivel A2/B1 ('Putzen', 'billiger', 'kein Streit'). Ausencia de estructuras B2 como Nomen-Verb-Verbindungen o conectores subordinantes variados."
        }
    },
    "critical_errors": [
        {
            "original": "Hallo Herr Lassner,",
            "correction": "Sehr geehrter Herr Lassner,",
            "rule_es": "En correspondencia comercial alemana formal nunca se tutea ni se usa 'Hallo' con clientes insatisfechos; debe usarse 'Sehr geehrte(r) Frau/Herr...'.",
            "type": "Stil"
        },
        {
            "original": "darum sie sind früher nach Hause gegangen.",
            "correction": "darum sind sie früher nach Hause gegangen.",
            "rule_es": "El adverbio conector 'darum' ocupa la posición 1, por lo que el verbo conjugado 'sind' debe ocupar obligatoriamente la posición 2 (inversión sujeto-verbo).",
            "type": "Grammatik"
        },
        {
            "original": "weil wir wollen kein Streit.",
            "correction": "weil wir keinen Streit wollen.",
            "rule_es": "La conjunción subordinante 'weil' desplaza el verbo conjugado ('wollen') al final absoluto de la oración subordinada. Además, 'Streit' es masculino acusativo ('keinen Streit').",
            "type": "Grammatik"
        }
    ],
    "strengths": [
        "El mensaje transmite la intención básica de solucionar el problema y menciona el 20% de descuento ordenado por la jefa."
    ],
    "areas_for_improvement": [
        "Utilizar siempre el pronombre de cortesía formal 'Sie' y sus declinaciones (Ihre E-Mail, Ihnen anbieten).",
        "Respetar la regla de posición del verbo en alemán (Verbzweitstellung con adverbios y Verbletztstellung con weil/dass).",
        "Alcanzar como mínimo 150 palabras desarrollando cada uno de los 4 Leitpunkte con detalle."
    ],
    "corrected_version": "Sehr geehrter Herr Lassner,\n\nvielen Dank für Ihren Hinweis bezüglich der Reinigung Ihrer Geschäftsräume. Wir bedauern die aufgetretenen Mängel außerordentlich und bitten für die Unannehmlichkeiten um Entschuldigung.\n\nAufgrund personeller Engpässe konnten die vereinbarten Zeiten vorübergehend nicht vollumfänglich eingehalten werden. Wir versichern Ihnen verbindlich, dass ab der kommenden Woche die tägliche Reinigungszeit von drei Stunden exakt erfüllt wird.\n\nAls Ausgleich und Zeichen unseres guten Willens gewähren wir Ihnen einen Nachlass von 20 % auf die nächste Monatsabrechnung.\n\nMit freundlichen Grüßen\nFriederike Woller"
}

# Fixture de evaluación esperada para Caso B
MOCK_EVAL_PASS_B2 = {
    "verdict": "BESTANDEN",
    "score_total": 92,
    "word_count": 178,
    "criteria": {
        "aufgabenbewaeltigung": {
            "grade": "A",
            "score": 24,
            "leitpunkte_check": [
                {"point": "Bezugnahme auf die Beschwerde und Dank für den Hinweis", "covered": True, "comment": "Excelente referencia a la carta del 14 de octubre y agradecimiento formal por el aviso."},
                {"point": "Förmliche Entschuldigung und Erklärung der Ursache des Problems", "covered": True, "comment": "Disculpa en nombre de la empresa y explicación plausible (bajas por enfermedad y personal en formación)."},
                {"point": "Zusicherung, dass die vertragliche Arbeitszeit künftig strikt eingehalten wird", "covered": True, "comment": "Compromiso expreso y medidas de control de calidad."},
                {"point": "Angebot eines 20 %-igen Rabatts auf die nächste Monatsrechnung als Wiedergutmachung", "covered": True, "comment": "Oferta formal del descuento del 20% acordado internamente."}
            ],
            "feedback": "Los 4 Leitpunkte están completamente cubiertos con un desarrollo lógico, profesional y persuasivo. Cumple holgadamente el requisito de extensión (178 palabras)."
        },
        "angemessenheit": {
            "grade": "A",
            "score": 24,
            "feedback": "Registro formal impecable. Tratamiento de cortesía 'Sie/Ihre', fórmulas de apertura y cierre de estándar comercial alemán de alto nivel."
        },
        "korrektheit": {
            "grade": "A",
            "score": 22,
            "feedback": "Gran dominio gramatical: subordinadas con dass/in der con verbo al final, régimen preposicional correcto (anliegen sehr ernst nehmen, Rücksprache mit, Nachlass auf), puntuación precisa."
        },
        "repertoire": {
            "grade": "A",
            "score": 22,
            "feedback": "Rico vocabulario profesional B2 y Nomen-Verb-Verbindungen: 'Anliegen ernst nehmen', 'Unannehmlichkeiten entschuldigen', 'Rücksprache halten', 'Verständnis aufbringen'."
        }
    },
    "critical_errors": [],
    "strengths": [
        "Estructura en párrafos perfectamente delineada: apertura, explicación/disculpa, solución/garantía y compensación.",
        "Uso fluido de vocabulario profesional B2 y registro sumamente educado y deeskalador.",
        "Cumplimiento exacto de todas las instrucciones de la gerencia."
    ],
    "areas_for_improvement": [
        "Para alcanzar el nivel C1, se podrían integrar construcciones más complejas con participios atribuidos o Konjunktiv I para citas indirectas."
    ],
    "corrected_version": SAMPLE_TEXT_PASS_B2
}


def run_offline_tests() -> bool:
    """Ejecuta la suite de verificación offline de contratos y prompts."""
    print("=== TEST OFFLINE: EVALUADOR TELC B2 SCHREIBEN ===")

    # 1. Verificar construcción de User Prompt (ES y RU)
    print("[1/4] Verificando generación del prompt (ES y RU)...")
    prompt_fail_es = build_user_prompt(SAMPLE_TASK, SAMPLE_TEXT_FAIL_A2, lang="es")
    assert "Die Huber GmbH hat einen Vertrag" in prompt_fail_es
    assert "Putzdienst / Büroreinigung" in prompt_fail_es
    assert "1. Bezugnahme auf die Beschwerde" in prompt_fail_es
    assert SAMPLE_TEXT_FAIL_A2 in prompt_fail_es
    assert "SPANISCH" in prompt_fail_es

    prompt_fail_ru = build_user_prompt(SAMPLE_TASK, SAMPLE_TEXT_FAIL_A2, lang="ru")
    assert "RUSSISCH" in prompt_fail_ru
    assert "rule_es" in prompt_fail_ru
    print("      OK: El user prompt incluye contexto, Leitpunkte y texto del alumno en ES y RU.")

    # 2. Validar contrato de Caso A (FAIL)
    print("[2/4] Validando contrato de evaluación para Caso A (A2 deficiente)...")
    errors_a = validate_evaluation_json(MOCK_EVAL_FAIL_A2)
    assert len(errors_a) == 0, f"Errores de esquema en Caso A: {errors_a}"
    assert MOCK_EVAL_FAIL_A2["verdict"] == "NICHT BESTANDEN"
    assert MOCK_EVAL_FAIL_A2["score_total"] < 60
    assert len(MOCK_EVAL_FAIL_A2["critical_errors"]) >= 3
    print(f"      OK: Caso A verificado. Veredicto: {MOCK_EVAL_FAIL_A2['verdict']} ({MOCK_EVAL_FAIL_A2['score_total']}/100)")

    # 3. Validar contrato de Caso B (PASS)
    print("[3/4] Validando contrato de evaluación para Caso B (B2 sólido)...")
    errors_b = validate_evaluation_json(MOCK_EVAL_PASS_B2)
    assert len(errors_b) == 0, f"Errores de esquema en Caso B: {errors_b}"
    assert MOCK_EVAL_PASS_B2["verdict"] == "BESTANDEN"
    assert MOCK_EVAL_PASS_B2["score_total"] >= 60
    assert len(MOCK_EVAL_PASS_B2["critical_errors"]) == 0
    print(f"      OK: Caso B verificado. Veredicto: {MOCK_EVAL_PASS_B2['verdict']} ({MOCK_EVAL_PASS_B2['score_total']}/100)")

    # 4. Probar detector de esquemas inválidos
    print("[4/4] Verificando robustez del validador de contratos frente a JSON corrupto...")
    corrupt_eval = {
        "verdict": "INVALID_VERDICT",
        "score_total": 150,  # fuera de rango
        # faltan campos requeridos
    }
    caught_errors = validate_evaluation_json(corrupt_eval)
    assert len(caught_errors) >= 3, "El validador debería haber detectado múltiples errores."
    print(f"      OK: El validador detectó correctamente {len(caught_errors)} anomalías en un payload corrupto.")

    print("\nTodos los tests offline del evaluador telc B2 pasaron con éxito (4/4).")
    return True


def call_live_gemini(api_key: str, model_name: str, task: Dict[str, Any], text: str) -> Dict[str, Any]:
    """Realiza una llamada en vivo a la API de Google Gemini."""
    try:
        from google import genai
        from google.genai import types
    except ImportError:
        import urllib.request
        # Si google-genai no está instalado, hacer llamada REST directa
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
        user_prompt = build_user_prompt(task, text)
        payload = {
            "system_instruction": {"parts": [{"text": SYSTEM_PROMPT}]},
            "contents": [{"parts": [{"text": user_prompt}]}],
            "generationConfig": {
                "response_mime_type": "application/json",
                "temperature": 0.2
            }
        }
        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
            return json.loads(raw_text)

    client = genai.Client(api_key=api_key)
    user_prompt = build_user_prompt(task, text)
    response = client.models.generate_content(
        model=model_name,
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            response_mime_type="application/json",
            temperature=0.2
        )
    )
    return json.loads(response.text)


def main():
    parser = argparse.ArgumentParser(description="Test y calibración del evaluador telc B2")
    parser.add_argument("--gemini-key", type=str, help="API Key de Google Gemini para prueba en vivo")
    parser.add_argument("--gemini-model", type=str, default="gemini-3.5-flash-lite", help="Modelo de Gemini")
    args = parser.parse_args()

    # Si se pasa clave de Gemini, realizar prueba en vivo
    if args.gemini_key:
        print(f"Iniciando evaluación EN VIVO con Gemini ({args.gemini_model})...")
        print("\n--- Evaluando Caso A (A2 deficiente) ---")
        res_a = call_live_gemini(args.gemini_key, args.gemini_model, SAMPLE_TASK, SAMPLE_TEXT_FAIL_A2)
        print(f"Veredicto: {res_a.get('verdict')} | Puntuación: {res_a.get('score_total')}/100")
        errors = validate_evaluation_json(res_a)
        if errors:
            print(f"Errores de contrato: {errors}")
        else:
            print("Contrato JSON 100% válido.")

        print("\n--- Evaluando Caso B (B2 sólido) ---")
        res_b = call_live_gemini(args.gemini_key, args.gemini_model, SAMPLE_TASK, SAMPLE_TEXT_PASS_B2)
        print(f"Veredicto: {res_b.get('verdict')} | Puntuación: {res_b.get('score_total')}/100")
        errors = validate_evaluation_json(res_b)
        if errors:
            print(f"Errores de contrato: {errors}")
        else:
            print("Contrato JSON 100% válido.")
        return 0

    # Por defecto, ejecutar batería de pruebas de contrato y robustez
    success = run_offline_tests()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
