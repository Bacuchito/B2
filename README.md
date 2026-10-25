# B2 Beruf — Test

> **README de arranque para Gemini Argon** (el agente de Google Antigravity que
> trabaja en este repositorio). Responde a las cinco preguntas de arquitectura y
> añade el ranking de agentes que merecen la pena y sus system prompts (las
> instrucciones fijas que definen a cada agente) listos para pegar.
>
> Estado comprobado antes de escribir esto: build OK · 95/95 humo · 52/52
> seguridad · 75/75 diseño · 5/5 rúbrica · corrector OK.

---

## 1. Qué es esto

Dos personas concretas —**Sergio** (español) y **Diana** (ruso)— preparan el
**telc Deutsch-Test für den Beruf B2**. Este repositorio es su mesa de examen:
presenta las preguntas de exámenes reales recopilados, deja responderlas y las
corrige con la frase literal que justifica cada respuesta, el grado de duda y una
marca de segunda lectura. Añade un módulo de Schreiben que evalúa redacciones con
un LLM (modelo de lenguaje) usando la rúbrica oficial de telc.

Existe porque **el documento de origen no trae clave de respuestas**. Todo lo que
verás marcado como respuesta lo dedujo alguien leyendo el texto, y la app lo dice
en lugar de disimularlo.

| Hecho | Valor |
|---|---|
| Entregable | `quiz/B2_quiz.html`, un único fichero autocontenido (1,7 MB) |
| Ítems de opción | **722** en 34 ficheros JSON (641 con clave + 81 sin clave) |
| Tareas de escritura | **111** (13 Beschwerde + 98 Forumsbeitrag) |
| Tarjetas de Sprechen T2 | **104** (mazo de Smalltalk) |
| Situaciones de Sprechen T3 | **67**, una entrada por situación |
| Modeltests | **7** tests de 52 ítems (364 ítems) |
| Ítems con segunda lectura | **226** de los 358 ítems originales (los Modeltests van aparte) |
| Servidor / base de datos | **ninguno** |
| Dependencias externas | **ninguna** (ni `package.json` ni `pip install`) |

---

## 2. Las cinco preguntas, respondidas

### 2.1 ¿Dev Agents o App Agents?

**Las dos cosas, pero no son el mismo oficio y no comparten contrato.**

| | Dev Agents | App Agents |
|---|---|---|
| Dónde viven | Antigravity / terminal, sobre el repo | dentro de `quiz/template.html`, en el navegador |
| Qué producen | **datos y código**: `quiz/data/*.json`, extractores, tests | **juicios** sobre lo que escribe el alumno |
| Qué los valida | `build.py` + `smoke_test.js` + `security_test.js` + `design_audit.js` | `validate_evaluation_json` en `prompt_schreiben.py` |
| Tienen sistema de ficheros | sí | no |
| Hoy existen | sí (scripts en `quiz/make_*.py`) | **uno solo**: el examinador de Schreiben |

La línea divisoria es esta: **un Dev Agent nunca escribe contenido de examen por
su cuenta; un App Agent nunca genera contenido de examen.** El Dev Agent deduce y
propone; el `build.py` (validador del contrato de datos) acepta o rechaza. El App
Agent solo juzga un texto ajeno y su salida pasa por un validador mecánico escrito
en Python.

**Conclusión operativa:** se construyen **Dev Agents ahora**. Los App Agents
solo donde exista un validador determinista detrás. El examinador de Schreiben lo
tiene; un examinador de Sprechen no lo tiene (nadie puede validar por máquina una
conversación) y por eso queda fuera del primer lote — ver §4.

### 2.2 ¿Qué formato de examen?

**telc Deutsch-Test für den Beruf B2 (DTB B2). No Goethe, no ÖSD, no entrenamiento
genérico.**

Esto no es un detalle: la rúbrica que usa el examinador es la de telc y está
calibrada contra el *Übungstest DTB B2*, pp. 40-41.

| Criterio | Puntos (escala de la app) | Peso oficial |
|---|---|---|
| I. Kommunikative Aufgabenbewältigung | 34 | 14 de 41 |
| II. Kommunikative Gestaltung | 22 | 9 de 41 |
| III. Formale Richtigkeit | 22 | 9 de 41 |
| IV. Spektrum sprachlicher Mittel | 22 | 9 de 41 |

Bandas oficiales: 100 %, ~75 %, ~39 %, 0 %. Se aprueba con 60.

Además la app aplica **dos reglas propias, más estrictas que el examen**: un
criterio en banda D suspende aunque la suma llegue a 60, y el criterio I no pasa
de C si falta un Leitpunkt o el texto baja de 100 palabras (ni de B entre 100 y
149). En el examen real esas reglas no existen.

**Consecuencia para los agentes:** si algún día se quiere Goethe o ÖSD, es una
**rúbrica nueva**, no un retoque del prompt. Los Redemittel, los criterios y los
tipos de tarea cambian.

### 2.3 ¿Cuál es el stack exacto?

**Web estática de un solo fichero, con Python solo como herramienta de
construcción. Nada del stack habitual: no hay React, ni Next, ni FastAPI, ni
SQLite.**

| Pieza | Realidad en este repo |
|---|---|
| Entregable | `quiz/B2_quiz.html` — un HTML con CSS, JS y datos incrustados. **Generado: no se edita a mano.** |
| Fuente de la app | `quiz/template.html` — HTML + CSS + JS en un fichero, sin bundler |
| Datos | `quiz/data/*.json`, contrato en `quiz/SPEC.md` |
| Build | `quiz/build.py`, Python de biblioteca estándar. **Valida y se niega a escribir si hay errores.** |
| Tests | Node sin dependencias (`smoke_test.js`, `security_test.js`, `design_audit.js`) + Python (`test_prompt.py`, `test_correccion.py`, `tools/test_pdf2md.py`) |
| Backend | **ninguno** |
| Persistencia | `localStorage` por perfil; Firebase Firestore opcional y solo para compartir redacciones |
| IA | el navegador llama **directo** al proveedor con la clave de cada uno |
| Despliegue | GitHub Pages con `index.html` en la raíz como enlace corto |

El "banco de preguntas" es JSON bajo contrato, no una base de datos. Si un agente
propone SQLite, está proponiendo otro proyecto.

Rutas de los intérpretes en esta máquina (las que usan los scripts):

```
python  C:\Users\sergi\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe
node    C:\Users\sergi\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\node\bin\node.exe
```

### 2.4 ¿Qué partes del examen cubre?

**Diez secciones vivas. Hören no está: está declarado y vacío.** Ese hueco se
dice, no se rellena.

| Bloque | Contenido | Estado |
|---|---|---|
| Lesen Teil 1 | 55 ítems (personas ↔ anuncios) | vivo |
| Lesen Teil 2 | 43 ítems | vivo |
| Lesen Teil 3 | 44 ítems (posteos ↔ comentarios) | vivo |
| Lesen Teil 4 | 56 ítems | vivo |
| Lesen und Schreiben | 28 ítems | vivo |
| Sprachbausteine Teil 1 | 72 huecos | vivo |
| Sprachbausteine Teil 2 | 60 huecos | vivo |
| Schreiben: Beschwerde-E-Mail | 13 tareas | vivo, con examinador |
| Schreiben: Forumsbeitrag | 98 tareas | vivo, con examinador |
| Sprechen Teil 2 | 104 tarjetas de Smalltalk | vivo, **mazo: no se corrige** |
| Sprechen Teil 3 | 67 situaciones de «Lösungswege» | vivo, **se habla: no se corrige** |
| Modeltest 11–17 | 364 ítems (283 con clave + 81 Hören sin clave) | vivo, **respuestas deducidas; Hören sin clave salvo el 13, 14 y 15** |
| Hören Teil 1-4 | — | **sin datos**: `build.py` reserva las etiquetas, `quiz/data/` no tiene ningún JSON |
| Sprechen Teil 1 | — | sin datos |

Detalles que un agente debe respetar al tocar esto:

- **Lesen Teil 1**: las 5 respuestas son **5 letras distintas** de las 8; tres
  anuncios son distractores. `build.py` rechaza lo contrario.
- **Lesen Teil 3 y Hören Teil 2**: 4 letras distintas de 6, dos sobran.
- **Sprachbausteine Teil 1**: seis respuestas, letras distintas, cada palabra se
  usa una sola vez.
- **Smalltalk (Sprechen T2)**: no lleva clave, cita ni confianza porque no hay
  nada que acertar. Lo que se guarda es la baraja y las notas de cada carta.
- **Situationen (Sprechen T3)**: tampoco se corrigen. Cada situación es una entrada
  del menú; la descripción alemana y los Stichpunkte van a la vista, y la ayuda
  ES/RU y los ejemplos quedan detrás de un «Ver».
- **Hören**: si algún día entra, entra **con transcripción**. Dos variantes del
  PDF no la traen y quedan fuera a propósito (pp. 149 y 176).

### 2.5 ¿Cómo se orquesta la IA?

**Corrección importante: hoy no hay orquestador.** Hay **una llamada, un prompt y
un validador mecánico**. DeepSeek, Gemini y Ollama no son agentes: son proveedores
intercambiables de esa única llamada.

La cadena real:

```
quiz/prompt_schreiben.py   ← aquí vive el system prompt y el JSON_SCHEMA
        │  (lo importa build.py y lo incrusta en el HTML)
        ▼
quiz/template.html         ← cliente: elige proveedor y llama
        │  Gemini generateContent · OpenAI-compatible (DeepSeek/OpenRouter)
        │  · Ollama local
        ▼
respuesta JSON estricto    ← si el modelo no puede con el esquema, se reintenta
        │                     sin esquema y se limpia el texto
        ▼
validate_evaluation_json() ← valida lo mecánico: cita literal, span mínimo,
                             corrección única, `change` presente, regla coherente
        ▼
puntuarCriterios()         ← la app recalcula puntos y palabras; el `score` que
                             escriba el modelo se ignora
```

Lo que esto significa en la práctica:

1. **La IA no puntúa.** Opina por bandas; el número lo calcula la app. Se
   descubrió que el modelo inflaba el recuento de palabras entre un 15 % y un 20 %.
2. **La IA no reescribe.** `corrected_version` es el texto del alumno con las
   correcciones listadas y nada más. La versión libre es `musterloesung`.
3. **La validación no es otra opinión de LLM.** Es código Python que comprueba
   hechos.

**Lo que se va a añadir** (y es de lo que trata este README) es la capa de arriba:
Dev Agents que se ejecutan en Antigravity sobre los ficheros y producen datos
verificables. La llamada del navegador no cambia.

---

## 3. Reglas que ningún agente puede romper

Estas no son consejos de estilo. Cada una tiene un test detrás o un fallo real
detrás.

1. **El alemán del examen va verbatim. La ayuda va traducida.** Enunciados,
   opciones, pasajes y citas no se tocan nunca. `smoke_test.js` falla si una clave
   de interfaz existe solo en un idioma, y si un `note` o un `explain` no tiene su
   versión rusa.
2. **Sin clave oficial: toda respuesta lleva `quote` literal + `confidence`.** Si
   el texto no sostiene la respuesta, no hay ítem. `hoch` exige una frase que
   responda directamente; `mittel` es por eliminación; `niedrig` es «revísalo tú».
3. **No se inventa lo que el PDF no trae.** Se documenta el hueco
   (`quiz/README.md`, tabla de huecos conocidos) y se sigue.
4. **`quiz/B2_quiz.html` no se edita a mano.** Se regenera con `build.py`.
5. **Nada se da por bueno sin los cuatro controles.** `build.py` valida y no
   escribe si hay errores; los otros tres no abren navegador.
6. **Los puntos y las palabras los calcula la app**, no el modelo.
7. **Ninguna clave de API entra en el repo.** Viven en el `localStorage` de cada
   navegador y viajan directas al proveedor.
8. **Español directo y sin relleno; los tecnicismos se explican.** Es la regla
   permanente del repo (`.agents/rules/comunicacion_clara.md`) y vale para todo lo
   que escriba un agente, incluidos los commits.

---

## 4. Qué agentes merecen la pena (y en qué orden)

### El criterio

Un agente vale la pena si **trabajo repetitivo × salida verificable por máquina**
es alto y **capacidad de inventar sin que nadie lo note** es baja.

```
valor = (aburrimiento del trabajo × frecuencia) / (riesgo de invención ÷ detección)
```

Si la detección es imposible, el valor es cero por muy listo que sea el agente.
Ese es el motivo de que el número 1 no sea el más vistoso, sino el que tiene el
validador más duro.

### El ranking

| # | Agente | Qué produce | Cómo se verifica | Riesgo | Veredicto |
|---|---|---|---|---|---|
| 1 | **Segunda lectura** (revisor ciego) | desacuerdos; alimenta `quiz/verified.json` | comparación contra datos que **no ha visto**; el diff es el resultado | medio | **Hazlo ya** |
| 2 | **Extractor de bloques** | `quiz/data/<bloque>.json` | `build.py` rechaza si incumple el contrato | alto si improvisa | **Hazlo ya** |
| 3 | **Traductor de ayuda ES/RU** | `explain_ru`, `note_ru`, claves de `I18N` | `smoke_test.js` falla si falta una | bajo | **Hazlo ya** |
| 4 | Calibrador del examinador | casos de control A2/B2 | `test_correccion.py`, `test_prompt.py` | bajo | después |
| 5 | Arreglador de diseño | CSS corregido por tokens | `design_audit.js` (75 reglas) | bajo | después |
| 6 | Triaje de incoherencias | informe de variantes en conflicto | avisos de `build.py` | bajo | opcional |
| 7 | Examinador de Sprechen | juicio de una conversación | **ninguno** | alto | espera |
| 8 | Generador de audio Hören | TTS | no hay fuente que copiar | inaceptable | **no** |
| 9 | Reescribidor de redacciones | texto «pulido» | ninguno | **ya falló** | **no** |

### Los tres primeros, con su porqué

**1. Segunda lectura.** Es el producto entero. Cada respuesta deducida se marca
con `quote` + `confidence`; si un revisor independiente la resuelve **por su
cuenta y antes de ver el JSON**, coincide o no. Hoy hay **226 de 358 ítems
marcados**, en 54 de 202 variantes: quedan **132** sin segunda lectura. Ojo con
la resta: `verified.json` guarda 225 números, pero marcan 226 ítems porque dos
variantes repiten número (errata del PDF, `t2_b-p23` y `t4_c-p51`) y un solo
número marca los dos. Ese trabajo es aburrido, repetible, y el resultado es un
diff — exactamente lo que un agente hace bien y un humano hace mal por cansancio.
Además el fallo se detecta sin discusión: o las respuestas coinciden o no.

**2. Extractor de bloques.** Convierte páginas del PDF en JSON bajo `SPEC.md`.
`build.py` rechaza lo mecánico —campos vacíos, opciones que no existen, letras
repetidas en un emparejamiento, cobertura de variantes, orden del PDF— y **avisa**
de lo que no puede juzgar: una cita parafraseada. La diferencia importa: un aviso
no detiene el build. Así que este agente sigue siendo el punto débil; la cita hay
que comprobarla, no confiar en que el validador la cace.

**3. Traductor de ayuda.** Texto mecánico, sin hechos que inventar, y el test lo
comprueba clave por clave. Es el mejor primer agente para probar que el bucle
funciona: si rompe algo, se ve en 5 segundos.

Los tres son Dev Agents. Ninguno escribe en `quiz/B2_quiz.html`.

### Los que no, y por qué

- **Explicador de Lesen** («¿por qué fallaste?»): el `explain` y la `quote` ya lo
  dicen. Añadir un modelo encima solo añade una opinión que puede contradecir la
  evidencia guardada.
- **Audio de Hören con TTS**: no hay audio oficial. Se generaría una voz que
  lee una transcripción que los candidatos recordaron. Es inventar material de
  examen.
- **Reescritor de redacciones**: ya se intentó. `corrected_version` se convirtió
  en una versión pulida que cambiaba argumentos y borraba la coma de «Liebe
  Grüße». El prompt actual lo prohíbe y hay test de regresión.
- **Examinador de Sprechen**: valioso para Diana y Sergio, pero sin validador. Se
  puede construir como *compañero de práctica que hace preguntas*, nunca como
  *examinador que puntúa*.

**Empezar con tres.** Un orquestador y tres sub-agentes; los demás, cuando estos
lleven 20 ejecuciones sin sorpresas.

---

## 5. System prompts listos para pegar

Se usan así: el **Agente 0** es el que se abre al empezar la sesión en
Antigravity. Los demás se invocan desde él, o se pegan a mano cuando toque. El
repo ya trae `.agents/skills`, `.agents/workflows` y `.agents/rules` con la
convención de agentes; si tu versión de Antigravity no los carga sola, pega la
regla que corresponda en el prompt del momento (la de comunicación clara es la
primera que hace falta).

### AGENTE 0 — Orquestador

```text
Eres el orquestador del repo B2 (telc Deutsch-Test für den Beruf B2, preparación de Sergio y Diana).
No escribes contenido de examen. Decides qué sub-agente corre, con qué entrada exacta, y bloqueas lo que no pasa los controles.

CONTEXTO OBLIGATORIO (léelo antes de actuar, no lo resumas):
- README.md (este fichero), PRODUCT.md, quiz/SPEC.md, quiz/README.md
- Reglas duras del README §3. Si una tarea las incumple, la rechazas y lo dices.

LISTA BLANCA DE TAREAS: segunda lectura, extraer bloque, traducir ayuda, calibrar examinador, arreglar diseño, escribir test.
Cualquier otra cosa: pregunta antes de hacerla.

PROCEDIMIENTO
1. `git status` y di en una línea qué está sin commitear.
2. Elige UNA tarea de la lista blanca y declara su entrada exacta: fichero, página del PDF, sección, variantes.
3. Delega en el sub-agente con su prompt, sin reescribirlo.
4. Ejecuta los controles que toquen y pega la salida literal, no un resumen.
5. Si un control falla: devuelve el error literal al sub-agente y repite. Nunca "arregles" el dato para que el test pase.
6. No hagas commit hasta que los cinco controles estén verdes.

PROHIBIDO
- Inventar enunciados, opciones, respuestas, citas o audio.
- Editar quiz/B2_quiz.html a mano.
- Añadir dependencias (npm, pip) o un package.json.
- Tocar firestore.rules sin que se te pida.
- Escribir una clave de API en cualquier fichero.

SALIDA DE CADA TURNO (JSON, sin prosa alrededor):
{"tarea":"","agente":"","entrada":"","ficheros":[],"controles":[{"cmd":"","resultado":"OK|FALLA"}],"siguiente":""}
```

### AGENTE 1 — Extractor de bloques

```text
Eres el extractor de un bloque de examen para quiz/data/. Trabajas bajo el contrato de quiz/SPEC.md.

ENTRADA: las páginas N-M de out/B2_ohne_antworten.md y la clave de sección destino de build.py (el diccionario SECTIONS).
SALIDA: un único JSON por bloque, con el esquema de SPEC.md.

REGLA CERO: el documento NO trae clave de respuestas. Las deduces leyendo el texto. Por eso cada ítem lleva:
- quote: la frase literal del pasaje que sostiene la respuesta. Tiene que aparecer DENTRO del passage (build.py lo comprueba).
- confidence: "hoch" solo si hay una frase que responde directamente; "mittel" por eliminación o sentido global; "niedrig" si el texto es ambiguo.
- explain en español y explain_ru en ruso. El alemán no se toca nunca.
- note / note_ru si hay algo que el compilador deba saber.

REGLAS DE FORMA
- zuordnung (Lesen T1): 5 respuestas, 5 letras DISTINTAS de las 8.
- zuordnung (Lesen T3, Hören T2): 4 letras distintas de 6.
- Sprachbausteine T1: 6 respuestas, letras distintas, cada palabra una sola vez.
- id único en todo el proyecto. Nada de ids duplicados.

SI FALTA MATERIAL: si el original no trae el texto del que deducir (caso de las páginas 149 y 176), NO emitas ítems. Deja "note" explicando qué falta y sigue con lo demás. Es mejor no ofrecer una variante que ofrecerla inventada.

CIERRE: valida sin tocar el entregable y pega la salida literal:
  python quiz\build.py quiz\data quiz\template.html $env:TEMP\B2_check.html
Si falla, corrige y repite. Si hay avisos, explícalos uno por uno.
```

### AGENTE 2 — Segunda lectura (verificador ciego)

```text
Eres el revisor de segunda lectura. Tu valor depende de una sola cosa: que resuelvas el ejercicio por tu cuenta ANTES de ver la respuesta que ya existe.

PROHIBIDO ABRIR, hasta haber escrito tu fichero de respuestas: quiz/data/*.json, quiz/verified.json, quiz/B2_quiz.html, quiz/_resp_*.json.
Solo puedes leer: out/B2_ohne_antworten.md y quiz/SPEC.md.

PROCEDIMIENTO
1. Lee el bloque en el Markdown de origen.
2. Resuelve cada ítem como si fueras el alumno: lee el texto, elige, y anota la frase que lo justifica.
3. Escribe respuestas_segunda_lectura_<bloque>.json con: {"block":"","items":[{"id":"","n":1,"answer":"","quote":"","confidence":""}]}
4. Solo entonces compara con el JSON existente.
5. Reporta ÚNICAMENTE los desacuerdos, cada uno con: id, n, tu respuesta, la suya, la cita que te sostiene y una frase de por qué crees que la otra está mal.

NO CORRIJAS NADA. No toques quiz/data ni quiz/verified.json. Informa y para: el orquestador decide.

Si en un ítem no estás seguro, dilo con "niedrig" y explica la duda. Un desacuerdo infundado cuesta más que uno que no reportas.
```

### AGENTE 3 — Examinador telc (envoltorio)

```text
El examinador ya está escrito en quiz/prompt_schreiben.py. NO lo reescribas ni lo "mejores" por gusto: cada línea de ahí cierra un fallo real.

Tu trabajo es uno de estos tres:
(a) añadir un caso de control a quiz/test_correccion.py o quiz/test_prompt.py;
(b) corregir el prompt SOLO si un caso de control falla, y demostrarlo con el test antes y después;
(c) revisar que una salida real cumple validate_evaluation_json.

FALLOS YA COMETIDOS (no repetir):
- corrected_version convertido en reescritura libre: cambiaba argumentos y borraba la coma de "Liebe Grüße". corrected_version es el texto del alumno con SOLO las correcciones listadas.
- Spans anchos: se marcó una oración de 101 caracteres por una mayúscula. Cita la palabra o el fragmento mínimo; tope 80 caracteres.
- Alternativas "A / B" en correction: una sola versión.
- Reglas inventadas: "falta de declinación" en "für alle Beteiligten" (la terminación era correcta); pronombre relativo donde iba el nominativo.
- Reescribir las explicaciones en alemán cuando el alumno es Sergio (español) o Diana (ruso). El texto modelo y el corregido van en alemán; las explicaciones van en el idioma del alumno.

Si dudas entre dos diagnósticos, elige el que puedas citar. Sin cita, no hay error.
```

### AGENTE 4 — Traductor de ayuda ES/RU

```text
Eres el traductor de la AYUDA. Nunca del examen.

LO QUE NO SE TOCA: enunciados, opciones, pasajes, citas, títulos de anuncios, nombres de tareas alemanas (Beschwerde, Forumsbeitrag, Leitpunkt) y los textos de las tarjetas de Smalltalk y de las situaciones de Sprechen T3. Son el material que hay que practicar.

LO QUE SÍ TRADUCES: claves de I18N en quiz/template.html (es y ru), explain_ru y note_ru en quiz/data/*.json, y la ayuda de las 104 tarjetas de Sprechen T2 (en sprechen_t2_es.json) y de las 67 situaciones de T3 (título, descripción, Stichpunkte; los ejemplos en alemán no se traducen).

CÓMO: frases cortas, registro directo, terminología constante. Nada de traducción literal del alemán que suene a traducción. En ruso, usa los términos que ya emplea el fichero (no inventes sinónimos nuevos para lo mismo).

CIERRE: `node quiz/smoke_test.js quiz/B2_quiz.html`. Falla si una clave existe solo en un idioma o si un note/explain se queda sin versión rusa. Pega la salida.
```

### AGENTE 5 — Arreglador de diseño (opcional)

```text
Eres el arreglador de diseño de quiz/template.html.

NO diseñas: reparas lo que design_audit.js marca.
- Todo sale de tokens del bloque :root (papel) y de [data-theme="dark"] (noche). Un color escrito a mano rompe el segundo tema.
- Espaciado múltiplo de 4. Contraste mínimo 4.5:1 sobre la superficie real de cada texto.
- Áreas táctiles 28/44 px, foco visible, respeto a prefers-reduced-motion.
- Ninguna sombra ni radio: la pieza se separa con un filete de 1 px. El texto largo se queda plano.

PROHIBIDO: tocar el JS de datos, cambiar la estructura de la pantalla, meter una fuente descargada o una imagen nueva.

CIERRE: `node quiz/design_audit.js quiz/template.html` (75 reglas) y pega la salida.
```

---

## 6. Arrancar sin romper nada

Desde la raíz del repo, en PowerShell:

```powershell
# 1. Validar los datos y comprobar la generación (escribe en un temporal, no toca el entregable)
python quiz\build.py quiz\data quiz\template.html $env:TEMP\B2_check.html

# 2. Los tres controles que no abren navegador
node quiz\smoke_test.js quiz\B2_quiz.html        # ejecuta el visor con un DOM simulado
node quiz\security_test.js quiz\B2_quiz.html     # los cuatro fallos críticos de la auditoría
node quiz\design_audit.js quiz\template.html     # 77 reglas de diseño en los dos temas

# 3. La rúbrica y el corrector
python quiz\test_prompt.py                       # contrato del prompt y del JSON
python quiz\test_correccion.py                   # regresión del corrector con el caso real

# 4. Solo cuando todo esté verde: regenerar el entregable de verdad
python quiz\build.py quiz\data quiz\template.html quiz\B2_quiz.html
```

Prueba en vivo del examinador (necesita clave, no la commitees):

```powershell
python quiz\test_correccion.py --gemini-key $env:GEMINI_API_KEY --model gemini-3.5-flash --save resp.json
```

Reconstrucción completa desde el PDF (rara vez hace falta, y en este orden):

```powershell
python quiz\make_quiz_sources.py out\B2_ohne_antworten.md quiz\src
python quiz\make_schreiben.py
python quiz\make_full_forums.py
python quiz\merge_sprachbausteine_respuestas.py quiz
python quiz\make_sprachbausteine.py out\B2_ohne_antworten.md quiz
```

Ojo con el reparto: `make_schreiben.py` escribe **solo**
`data/schreiben_beschwerde.json` (13 tareas, pp. 66-77) y `make_full_forums.py`
**solo** `data/schreiben_forum.json` (98 temas, pp. 98-106). La lista `foren` que
sigue dentro de `make_schreiben.py` es un subconjunto antiguo de 8 temas: no la
vuelvas a volcar sobre el fichero.

### El grafo del proyecto

`graphify-out/` es el mapa navegable del repo. Se actualiza solo: el hook
`post-commit` (instalado con `graphify hook install`) reextrae los ficheros de
código que cambian en cada commit, en segundo plano, y deja el registro en
`~/.cache/graphify-rebuild.log`. Los documentos **no** los toca el hook: para eso,
`graphify update` a mano.

Qué entra y qué no lo decide `.graphifyignore` (no `.gitignore`: graphify ignora
lo que ya está en el índice de Git). Fuera quedan `.agents/`, `graphify-out/`, el
desempaquetado del `.asar`, el PDF convertido, el HTML generado y `quiz/src/`: sin
ese filtro, el grafo tenía 2.796 nodos de los que el 90 % no era la aplicación.
Tras la limpieza: **76 ficheros → 405 nodos, 554 aristas, 33 comunidades**, con el
92 % de las aristas extraídas literalmente del texto.

**Regla para cualquier agente que llegue aquí:** antes de recorrer el código a
`grep`, pregunta al grafo. `graphify query "<pregunta>"` devuelve los nodos con su
fichero y su línea; luego se lee lo que haga falta. Es el camino corto y deja
rastro (`graphify-out/cache/`).

Dos cosas que sorprenden al mirarlo y conviene saber de antemano:

- **`out/` no está en el grafo y no puede estarlo.** graphify se salta por nombre
  cualquier carpeta llamada `out` (la trata como artefacto de build, igual que
  `dist` o `build`). Renombrarla rompería el README y todos los scripts, así que
  se asume: el grafo cubre el código (`quiz/`, `tools/`, `uxui/`) y los documentos
  de la raíz, no el texto de los exámenes.
- **El hook solo reextrae código.** Los documentos y las imágenes necesitan
  `graphify update` a mano.

---

## 7. Deuda conocida (no la tapes con invenciones)

| Deuda | Estado |
|---|---|
| **Hören no tiene datos** | `build.py` reserva las etiquetas; `quiz/data/` no tiene ningún JSON de Hören. La app no lo muestra. |
| **132 ítems sin segunda lectura** | 226 de 358 marcados (225 números en `verified.json`). Es el trabajo del Agente 2. |
| **Numeración repetida** | `t2_b-p23` (6, 6, 7) y `t4_c-p51` (14, 15, 15, 16, 17, 18): errata del PDF, se copia literal. Un número marca dos ítems en la insignia y en la respuesta guardada. `build.py` lo avisa. |
| **Sin clave oficial en el original** | Por diseño. `confidence` + `verified.json` son la respuesta. |
| **Hören sin audio** | Si entra, entra con transcripción. Las pp. 149 y 176 no la traen y quedan fuera. |
| **Firestore no separa usuarios** | No hay login: la sala es un secreto compartido por enlace. El aislamiento «Sergio escribe lo suyo» es del cliente, no de las reglas. |
| **Erratas del original** | p. 18, anuncio `h)` truncado. Se respeta y se anota en `fixes`. |
| **Un solo fichero de 1,2 MB** | Vinculante para abrir con doble clic; el mundo visual de hoja de examen no lo es. |

---

## 8. Mapa del repositorio

```
B2/
├─ README.md              ← este fichero
├─ PRODUCT.md             ← producto, usuarios, principios, restricciones
├─ PLAN_SCHREIBEN.md      ← plan del módulo de escritura (5 fases, cerradas)
├─ AUDITORIA_B2.md        ← auditoría interna
├─ firestore.rules        ← reglas de seguridad de la sincronización opcional
├─ index.html             ← enlace corto, conserva ?user= y ?room=
├─ out/                   ← el PDF convertido: la fuente de verdad del contenido
│  ├─ B2_ohne_antworten.md       (sin respuestas)
│  ├─ REDEMITTEL_B2.md, GUIA_B2.md, PLANTILLA_FORUMSBEITRAG.md
├─ quiz/                  ← la app
│  ├─ B2_quiz.html               entregable generado
│  ├─ template.html              fuente (HTML+CSS+JS)
│  ├─ build.py                   valida y genera
│  ├─ SPEC.md                    contrato de datos
│  ├─ README.md                  manual técnico completo (léelo antes de tocar datos)
│  ├─ prompt_schreiben.py        system prompt + JSON_SCHEMA + validador
│  ├─ data/                      34 JSON, la fuente de verdad de las preguntas
│  ├─ src/                       Markdown por bloque, entrada de los extractores
│  ├─ make_*.py                  extractores
│  ├─ smoke_test.js, security_test.js, design_audit.js
│  └─ test_prompt.py, test_correccion.py
├─ tools/                 ← pdf2md.py (conversor propio), proxy local, análisis
├─ .agents/               ← skills, workflows y reglas: la convención de agentes del repo
├─ .graphifyignore        ← qué entra en el grafo del proyecto (no confundir con .gitignore)
└─ graphify-out/          ← el grafo (generado, no editar): graph.json, graph.html, GRAPH_REPORT.md
```

---

## 9. Lo que hay que recordar

1. **No hay clave de respuestas.** La cita y la confianza son el producto.
2. **telc, no Goethe.** La rúbrica está calibrada y tiene tests.
3. **Sin servidor, sin base de datos, sin dependencias.** Un HTML y JSON.
4. **La IA opina; el código decide.** Puntos y palabras se recalculan fuera del modelo.
5. **Tres agentes primero**: segunda lectura, extractor, traductor. Los demás,
   cuando estos lleven veinte ejecuciones sin sorpresas.
