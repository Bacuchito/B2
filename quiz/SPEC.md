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

---

## 6. Formato de tarea: `smalltalk` (Sprechen Teil 2)

Mazo de cartas para el Smalltalk de la prueba oral. **No es un ejercicio que se
corrija**: no hay `answer`, ni `quote`, ni `confidence`, porque no hay nada que
acertar. Cada variante es un mazo completo y la app lo pinta como tarjetas.

```json
{
  "block": "sprechen_t2",
  "section": "sprechen-t2",
  "variants": [{
    "id": "spr-t2-smalltalk",
    "label": "Alle Karten",
    "page": 182,
    "kind": "smalltalk",
    "intro": "Teil 2 der mündlichen Prüfung …",
    "time_minutes": 3,
    "cards": [
      {
        "n": 6,
        "de": "Ich habe noch fünf Tage Resturlaub. Was passiert mit diesen Tagen?",
        "alt": ["Ich habe vom Urlaub in diesem Jahr noch 5 Tage übrig. …"],
        "ru": "У меня осталось пять дней неиспользованного отпуска. …",
        "es": "Me quedan cinco días de vacaciones sin gastar. …"
      }
    ]
  }]
}
```

| Campo | Obligatorio | Contenido |
|---|---|---|
| `kind` | sí | `"smalltalk"` |
| `intro` | sí | Instrucción del examen, **en alemán** (con quién se habla, cuánto dura) |
| `time_minutes` | no | Duración de la tarjeta en el examen (3 en el Teil 2) |
| `cards` | sí | Las tarjetas |
| `cards[].n` | sí | Número de la tarjeta, **1..N sin huecos**: es el número del documento |
| `cards[].de` | sí | La pregunta, **en alemán, verbatim** |
| `cards[].alt` | no | Otras formulaciones del mismo tema, si el documento las trae (separadas por « / ») |
| `cards[].ru` | sí | Traducción rusa (ayuda) |
| `cards[].es` | sí | Traducción española (ayuda) |

Regla de una tarjeta: **el alemán no se inventa ni se resume**. Si el documento trae
dos formulaciones del mismo tema, van las dos en la misma tarjeta (`alt`), para que
`n` siga señalando el mismo sitio del PDF.

---

## 7. Formato de tarea: `situation` (Sprechen Teil 3)

Las **67 situaciones** de «Lösungswege diskutieren» de las pp. 188-200. Tampoco se
corrigen: no hay `answer`, `quote` ni `confidence`, porque el ejercicio es hablar y
acordar una solución, no acertar una letra. **Cada situación es una variante**: así
el menú las lista por separado y cada una tiene su propia página.

```json
{
  "block": "sprechen_t3",
  "section": "sprechen-t3",
  "variants": [{
    "id": "spr-t3-01",
    "label": "1 · Würmer im Mehl der Konditorei",
    "page": 188,
    "kind": "situation",
    "n": 1,
    "titel": "Würmer im Mehl der Konditorei",
    "de": "Sie arbeiten in einer Konditorei. Heute haben Sie Würmer/ kleine Tierchen im Mehl im Lager gefunden. …",
    "es": "Trabajas en una pastelería. Hoy has encontrado gusanos o bichitos en la harina del almacén. …",
    "ru": "Вы работаете в кондитерской. Сегодня вы обнаружили в муке на складе червяков …",
    "punkte": [
      {"de": "Chef: Wie kontaktieren?", "es": "Jefe: ¿cómo contactarlo?", "ru": "Шеф: как с ним связаться?"}
    ],
    "beispiele": ["Ich rufe den Chef sofort an und erkläre ihm ruhig, was im Lager passiert ist."]
  }]
}
```

| Campo | Obligatorio | Contenido |
|---|---|---|
| `kind` | sí | `"situation"` |
| `n` | sí | Número de la situación, **1..67 sin huecos** en toda la sección |
| `label` | sí | `«n · título»`: lo que se ve en el menú |
| `page` | sí | Página del PDF donde empieza la situación |
| `titel` | sí | Título corto en alemán |
| `de` | sí | Descripción **verbatim** del documento |
| `es` | sí | Traducción española (ayuda) |
| `ru` | sí | Traducción rusa (ayuda) |
| `punkte` | sí | Stichpunkte, cada uno con `de`, `es` y `ru` |
| `beispiele` | sí | Frases de ejemplo **en alemán** (mínimo 2) |

Reglas:

1. **El alemán de `de` y `punkte[].de` no se inventa**: sale del documento. Se
   corrigen solo erratas evidentes y cada corrección se anota en `fixes`.
2. `es` y `ru` son ayuda y **no se enseñan solas**: la app las deja detrás de un
   «Ver». Los `beispiele` también van plegados.
3. `beispiele` es material nuestro para practicar, no texto del examen. No se
   presenta como oficial.
4. Si una situación trae dos formulaciones separadas por « / », se conservan las dos
   en `de`: el documento las une en el mismo caso.

---

## 8. Formato de tarea: `ohne-key` (Hören de los Modeltests)

Bloques de comprensión auditiva de los que **solo existe el enunciado y las opciones**:
no hay audio, ni transcripción, ni clave. No se puede deducir la respuesta, así que
la app deja elegir pero no corrige. Se usa en Hören T1-T4 y en Hören und Schreiben
(ítem 41) de los siete Modeltests, salvo los Modeltests 13 (22–40), 14 (22–41) y
15 (22–41): sus Hörtexte llegaron en imágenes y esos bloques son
`text`/`zuordnung` con `answer`.

```json
{
  "id": "mt11-hoeren-t1",
  "label": "Hören Teil 1",
  "page": 12,
  "kind": "ohne-key",
  "intro": "Sie hören drei Gespräche. …",
  "items": [
    {
      "n": 22,
      "type": "truefalse",
      "prompt": "Luisa hat noch keine Erfahrungen mit dem Imbiss-Bereich.",
      "options": [{"key": "Richtig", "text": "Richtig"}, {"key": "Falsch", "text": "Falsch"}]
    }
  ]
}
```

| Campo | Obligatorio | Contenido |
|---|---|---|
| `kind` | sí | `"ohne-key"` |
| `intro` | sí | Instrucción del examen, en alemán |
| `items[].n` | sí | Número del ítem del examen |
| `items[].type` | sí | `choice` o `truefalse` |
| `items[].prompt` | sí | Enunciado, en alemán |
| `items[].options` | sí | Opciones, si no hay `options` a nivel de variante |
| `options` | solo T2 | Banco global a-f; los ítems solo llevan `n` y `prompt` |
| `optionsLabel` | no | `"Aussagen"` en Hören T2 |

Reglas:

1. **Nada de `answer`, `quote`, `confidence` ni `explain`**: no hay información para
   deducir la respuesta. Inventarla sería peor que no corregir.
2. La app muestra un aviso («sin audio ni clave») y marca la elección sin veredicto.
   Esos ítems no cuentan en las estadísticas ni en «Solo dudosas».
3. `intro` puede decir que se trata de una práctica sin audio; el aviso lo pone la app.

---

## 9. Modeltests 11–17 (zona especial)

Cada test es una sección propia (`modeltest-11` … `modeltest-17`) y un fichero
`quiz/data/modeltest_N.json` con 12 variantes: Lesen T1-T4, Lesen und Schreiben,
Hören T1-T4, Hören und Schreiben y Sprachbausteine T1-T2. Los ítems conservan la
numeración del examen (1-20, 22-41, 46-57).

- **Sin clave oficial**: los PDF no traen Lösungsschlüssel; las 32 respuestas de
  Lesen y Sprachbausteine de cada test se deducen y llevan `quote`, `confidence` y
  `explain`/`explain_ru`, como el resto de la app.
- **Hören sin clave**: `kind: "ohne-key"` (apartado 8). Los Modeltests 13 (22–40),
  14 (22–41) y 15 (22–41) son la excepción: sus Hörtexte se transcribieron y ahora
  llevan respuesta.
- **Lesen T3 con `allowNone: true`**: una de las cuatro preguntas no tiene consejo;
  su `answer` es `"x"` y su `quote` va vacía. Sólo puede haber una `x`.
- Schreiben y Sprechen quedan fuera de esta zona.
