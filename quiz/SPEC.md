# SPEC — Extracción de preguntas y respuestas para el test B2

Estás construyendo los datos de una **página web de test** del examen
**telc Deutsch-Test für den Beruf B2**, a partir del texto de un PDF convertido
a Markdown.

**No existe ninguna clave oficial en el documento.** Las respuestas correctas
las deduces tú, leyendo el texto. Por eso cada respuesta debe ir acompañada de
la **frase literal que la justifica** y de un **nivel de confianza**.

---

## 1. Formatos de tarea que vas a encontrar

### `zuordnung` (Lesen Teil 1)
Cinco personas (1-5) y ocho anuncios (a-h). Hay que emparejar cada persona con
su anuncio. **Tres anuncios son distractores y no se usan.**
Ejemplo resuelto (variante 1, p. 8):

| Persona | Respuesta | Frase que lo justifica |
|---|---|---|
| 1. Moutasem fragt sich, wie er neue Kollegen korrekt ansprechen sollte. | **e** | „Duzen oder siezen? Welche Themen sollten Sie im Smalltalk vermeiden?" |
| 2. Selma wurde entlassen und will sich dagegen wehren. | **h** | „Seit einigen Jahren geht die Zahl der Kündigungsschutzklagen … zurück" |
| 3. Anka überlegt, eine Ausbildung im Fremdsprachenbereich zu machen. | **c** | „ist der geborene Fremdsprachenkorrespondent … diesen Beruf zu erlernen" |
| 4. Sean ist Professor für Biologie und sucht einen Job im internationalen Umfeld. | **b** | „arbeitet in den Bereichen … Meeresbiologie eng mit anderen Ländern zusammen" |
| 5. Yassin möchte erste Berufserfahrungen im Ausland sammeln. | **g** | „Du träumst von einem Job im Ausland, dann knüpfe erste Kontakte durch ein Praktikum." |

Fíjate en el razonamiento: `a) Auf ins Abenteuer!` habla de un **viaje de idiomas**,
no de trabajar en el extranjero → es distractor de la 5, no su respuesta.
`d) Nutzen Sie das Recht für sich!` es **derecho de familia** (divorcio, custodia),
no laboral → distractor de la 2, no su respuesta. `f) Souverän am Telefon` habla
de técnica telefónica, no de cómo tratar a colegas → distractor de la 1.

**Regla dura: las 5 respuestas deben ser 5 letras DISTINTAS de las 8.**

### `zuordnung` — Lesen Teil 3 (foro)

Forma distinta, misma mecánica: **4 posteos de un foro** (ítems **10-13**) y
**6 comentarios** (claves **a-f**). **Dos comentarios sobran.**

- `optionsLabel`: `"Kommentare"` (si se omite, la app pone «Anzeigen», que sería incorrecto aquí).
- Las 4 respuestas deben ser **4 letras distintas de las 6**.
- `intro` típica: «Lesen Sie die vier Aufgaben (10–13) und die sechs Kommentare
  (a–f). Welcher Kommentar passt zu welcher Aufgabe? Zwei Kommentare bleiben übrig.»

### `zuordnung` — Hören Teil 2

Otra forma: **4 audios** (ítems **28-31**) y **6 afirmaciones** (claves **a-f**).
**Dos afirmaciones sobran.**

- `optionsLabel`: `"Aussagen"`.
- Como no hay audio disponible, **`passage` lleva las transcripciones** de los
  cuatro audios, numeradas por ítem. El usuario decide emparejando con lo que lee.
- Si la variante **no trae transcripción** (ocurre en alguna), no inventes: deja
  `passage` vacío, pon `"note"` explicando que el original no la incluye y NO
  emitas ítems con respuesta inventada. Es mejor no ofrecer esa variante que
  ofrecerla mal.

### `text` (Lesen Teil 2 y Teil 4)
Un texto con dos o tres ítems. Los ítems son de dos tipos:
- `truefalse` → opciones `Richtig` / `Falsch`
- `choice` → opciones `a` / `b` / `c`

El texto puede repetirse en **varias variantes** con los mismos ítems reformulados.
Cada variante es una entrada independiente.

---

## 2. Esquema JSON exacto

```json
{
  "block": "t1_a",
  "section": "lesen-t1",
  "variants": [
    {
      "id": "t1-v1",
      "label": "Variante 1",
      "page": 8,
      "note": "",
      "kind": "zuordnung",
      "intro": "Sie suchen für fünf Personen (1-5) die passende Anzeige (a-h).",
      "passage": "",
      "options": [
        {
          "key": "a",
          "title": "Auf ins Abenteuer!",
          "text": "Du hast Lust auf Sonne, Strand und eine fremde Sprache? Eine Sprachreise ...",
          "distractor": "Es geht um eine Sprachreise, nicht um Berufserfahrung im Ausland."
        }
      ],
      "items": [
        {
          "n": 1,
          "type": "choice",
          "prompt": "Moutasem fragt sich, wie er neue Kollegen korrekt ansprechen sollte.",
          "answer": "e",
          "confidence": "hoch",
          "quote": "Duzen oder siezen? Welche Themen sollten Sie im Smalltalk vermeiden?",
          "explain": "Moutasem pregunta cómo dirigirse correctamente a colegas nuevos. El anuncio e trata justamente las formas de trato en la oficina y menciona explícitamente «Duzen oder siezen?»."
        }
      ]
    }
  ],
  "fixes": [
    "p.8: corregido «Hansson» → «Hansso» (errata del original)"
  ]
}
```

### Campos

**Variante**
| Campo | Obligatorio | Contenido |
|---|---|---|
| `id` | sí | `t1-v1`, `t2-v3`… único en todo el proyecto |
| `label` | sí | p. ej. `Variante 1`, `Variante 1 (nueva versión 08.2024)` |
| `page` | sí | página del PDF donde empieza |
| `note` | no | aviso del compilador, p. ej. `"no procede de un examen real"` |
| `kind` | sí | `zuordnung` o `text` |
| `intro` | sí | instrucción breve **en alemán**, como en el examen |
| `passage` | solo `text` | **el texto COMPLETO**, limpio de números de página y encabezados. Nunca resumido. |
| `options` | solo `zuordnung` | los 8 anuncios |
| `items` | sí | las preguntas |

**Item**
| Campo | Obligatorio | Contenido |
|---|---|---|
| `n` | sí | número de ítem del examen (1-5, 6, 7, 8, 9) |
| `type` | sí | `choice` o `truefalse` |
| `prompt` | sí | el enunciado, **en alemán, verbatim** |
| `options` | solo `text` | `[{"key":"a","text":"…"}]` o `Richtig`/`Falsch` |
| `answer` | sí | la clave: `"e"`, `"b"`, `"Richtig"`… |
| `confidence` | sí | `hoch`, `mittel` o `niedrig` |
| `quote` | sí | **frase literal del texto** que justifica la respuesta |
| `explain` | sí | por qué, **en español**, 1-3 frases |

---

## 3. Reglas

1. **No inventes.** Si el texto no permite decidir, usa `"confidence": "niedrig"` y
   explica la duda en `explain`.
2. **`quote` debe ser literal**, copiada del texto. Es lo que permite al usuario
   verificar tu razonamiento.
3. **`explain` en español.** El `prompt`, las `options` y el `passage` **en alemán**.
4. En `zuordnung`, **las respuestas han de ser letras distintas** (tantas como ítems),
   porque cada opción se usa como máximo una vez. Sobran siempre algunas: son los
   distractores, y hay que explicarlos en `distractor`.
5. **Transcribe el `passage` completo**, no un resumen. Quita solo los números de
   página sueltos y los encabezados repetidos (`Testformat…`).
6. **Erratas evidentes del OCR:** puedes corregirlas, pero **anota cada corrección**
   en el array `fixes`. Si dudas, déjalo como está.
7. **Una variante = una entrada.** Si el mismo texto aparece con los ítems
   reformulados (marca `Новый вариант`), es **otra variante** con su propia `id`.
   Fíjate en si cambian el orden o los nombres de las personas: entonces cambian
   las respuestas.
8. **Explicación de distractores:** en `zuordnung`, rellena `distractor` en los
   anuncios **no usados**, y opcionalmente en los usados, diciendo por qué no
   encajan con nadie o con quién se confunden.
9. JSON válido, UTF-8, sin comas finales, sin comentarios.

---

## 4. Niveles de confianza

| Nivel | Cuándo |
|---|---|
| `hoch` | El texto contiene una frase que responde directamente. |
| `mittel` | Se deduce por eliminación o por el sentido global, sin frase explícita. |
| `niedrig` | El texto es ambiguo, está incompleto o dos opciones son defendibles. |

Sé **honesto** con esto: es lo que permite al usuario distinguir tus aciertos de
tus dudas en lugar de fiarse a ciegas.

---

## 5. Formato de tarea: `schreiben` (Produktion)

Tareas abiertas de expresión escrita del examen telc Deutsch-Test für den Beruf B2, evaluadas interactivamente por un LLM integrado.

### Categorías
1. `beschwerde`: Respuesta formal por correo electrónico a una reclamación o queja de un cliente o proveedor (ejercicios de *Lesen und Schreiben*, ítem 21).
2. `forum`: Publicación argumentativa formal (*Stellungnahme*) para el foro o intranet de la empresa.

### Esquema de Variant para `kind: "schreiben"`
| Campo | Obligatorio | Tipo / Descripción |
|---|---|---|
| `id` | sí | Identificador único (ej. `schr-b-p66`, `schr-f-homeoffice`) |
| `label` | sí | Título visual de la tarea |
| `page` | sí | Página de referencia en el PDF |
| `kind` | sí | `"schreiben"` |
| `category` | sí | `"beschwerde"` o `"forum"` |
| `topic` | sí | Tema profesional (ej. `"Putzdienst / Reinigung"`, `"Homeoffice"`) |
| `scenario` | sí | Situación que motiva el texto. En `forum` es el **texto literal** de la tabla del PDF (pp. 98-106); en `beschwerde`, un resumen del caso |
| `source_letter` | solo `beschwerde` | Carta de queja completa recibida del cliente/proveedor |
| `boss_instructions`| solo `beschwerde` | Indicaciones o notas internas del superior |
| `prompt` | sí | Enunciado formal del examen en alemán |
| `leitpunkte` | sí | Array de **4 puntos guía obligatorios** (*Leitpunkte*) que deben desarrollarse |
| `min_words` | sí | Longitud mínima requerida (150 palabras) |
| `time_minutes` | sí | Tiempo oficial asignado (45 minutos) |
| `redemittel` | opcional | Array de expresiones modelo B2 recomendadas para este tipo de texto |
