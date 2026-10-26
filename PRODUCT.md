# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Dos personas concretas, Sergio y Diana, que preparan el examen **telc Deutsch-Test
für den Beruf B2** y practican juntas en el portátil. Diana lee en ruso y Sergio en
español, de ahí los dos perfiles del encabezado. No hay público anónimo ni cuentas
de terceros.

## Product Purpose

Presentar las preguntas de exámenes reales recopilados (Lesen, Hören,
Sprachbausteine y Schreiben), dejar responderlas y corregirlas con la respuesta
deducida, la cita literal que la justifica y un nivel de confianza; y evaluar las
redacciones con los cuatro criterios de telc. Existe porque el documento de origen
**no trae clave de respuestas**.

## Positioning

Una clave de respuestas que no existe en el original: cada respuesta se publica con
su evidencia (la frase literal del texto), su grado de duda y una marca de segunda
lectura independiente. La app enseña la duda en lugar de esconderla. Ningún producto
de plantilla podría copiar eso sin hacer antes el mismo trabajo de deducción.

## Operating Context

- Sesiones de estudio en portátil. La app se abre con doble clic como fichero local
  o desde el enlace de GitHub Pages: son dos almacenes distintos.
- Con la ventana ancha (**≥1280 px**) se activa el **modo mesa de examen**: la
  referencia (los anuncios o el texto) queda fija en la columna izquierda y la hoja
  de preguntas en la derecha, para responder sin subir y bajar. El conmutador de la
  cabecera lo fuerza o lo apaga y recuerda la elección.
- Son 722 ítems (641 con clave y 81 de Hören sin clave) y 111 tareas de escritura
  (13 Beschwerde, 98 Forumsbeitrag).
- 104 tarjetas de **Smalltalk (Sprechen Teil 2)**: un mazo que se hojea entero en dos
  mitades y una **mesa de trabajo** que saca una carta al azar para hablarla en voz
  alta, con un cuadro de notas por carta.
- **67 situaciones de Sprechen Teil 3** («Lösungswege diskutieren»), una entrada por
  situación: la página enseña el caso y sus Stichpunkte, y deja la ayuda ES/RU y los
  ejemplos detrás de un «Ver».
- **Siete Modeltests** (11–17), cada uno con sus 12 bloques y 52 ítems. Las respuestas
  de Lesen y Sprachbausteine están deducidas porque los PDF no traen clave; Hören se
  ofrece con enunciados y opciones, sin corregir.
- El progreso vive en `localStorage`, por perfil. La sincronización con Firebase es
  opcional y solo sirve para compartir las redacciones entre los dos.
- La evaluación de Schreiben la hace un LLM con la clave de API propia de cada uno
  (en `localStorage`, viaja directa al proveedor elegido).

## Capabilities and Constraints

- **Sin clave oficial.** Cada respuesta lleva `quote` literal, `confidence`
  (`hoch`/`mittel`/`niedrig`) y, si pasó la segunda lectura, la insignia «✓ 2ª
  lectura» (`verified.json`). El botón «Solo dudosas» filtra lo que hay que revisar.
- **Regla de idioma:** lo que es examen va en alemán verbatim; lo que es ayuda va
  traducido (ES/RU). `smoke_test.js` falla si el diccionario está incompleto en un
  idioma.
- **Hören no tiene audio**, solo transcripciones. Las dos variantes sin transcripción
  quedan fuera en lugar de ofrecerse inventadas.
- **El Smalltalk no se corrige**: no lleva clave, cita ni confianza porque no hay nada
  que acertar. Lo único que se guarda es la baraja (qué cartas ya salieron) y tus
  notas de cada carta, por perfil. La ayuda ES/RU de cada carta va plegada.
- **Las situaciones de Sprechen T3 tampoco se corrigen**: cada una es una entrada y
  una página. La descripción alemana y los Stichpunkte van a la vista; la ayuda
  (ES/RU) y los ejemplos de habla en alemán solo se ven al pulsar «Ver».
- **Los Modeltests separan clave y no clave**: Lesen y Sprachbausteine llevan quote,
  confidence y explicación ES/RU deducidas; Hören (`kind: "ohne-key"`) muestra
  enunciados y opciones sin answer, no corrige y no cuenta en las estadísticas.
  Lesen T3 admite una `x` para la pregunta sin consejo. Los Modeltests 13, 14 y 15
  son la excepción: sus Hörtexte llegaron aparte y su Hören se corrige (13: 22–40;
  14 y 15: 22–41).
- El entregable es **un único HTML autocontenido** generado por `build.py` desde
  `template.html`; los datos viven en `quiz/data/*.json` bajo el contrato de
  `SPEC.md`.
- **Controles obligatorios** antes de dar algo por bueno: `build.py` (valida y no
  escribe si hay errores), `smoke_test.js`, `security_test.js`, `design_audit.js`.
- El documento fuente tiene huecos y erratas conocidas, documentados en
  `quiz/README.md`; no se rellenan con invenciones.
- **Vinculante por decisión del usuario:** el bilingüismo ES/RU y el contrato de
  datos con sus tests. **No declarado vinculante** (queda abierto a cambio): el
  empaquetado en un solo fichero y el mundo visual de hoja de examen.

## Brand Commitments

- Nombre en uso: «B2 Beruf — Test».
- Voz: honesta sobre la incertidumbre; alemán para el material de examen, español y
  ruso para la ayuda.
- No hay logotipo, marca registrada ni material de terceros que condicione el
  aspecto, y el usuario no ha declarado vinculante la dirección visual actual.

## Evidence on Hand

- `out/B2_ohne_antworten.md`: el PDF convertido a Markdown, sin respuestas (fuente).
- `quiz/data/*.json`: ítems con `quote`, `explain`, `confidence`; `explain_ru` y
  `note_ru` para el ruso.
- `quiz/verified.json`: las respuestas confirmadas por la segunda lectura.
- `quiz/sprachbausteine_respuestas.json` y `quiz/_resp_*.json`: las 132 respuestas
  deducidas de los huecos.
- `DESIGN.md`: el mundo visual, sus tokens y lo que queda prohibido.
- `quiz/README.md` y `quiz/SPEC.md`: contrato de datos y sistema de diseño
  documentado.
- `AUDITORIA_B2.md`: auditoría interna, en disco y fuera del repositorio público.
- **Ausencias que no se deben inventar:** no hay clave oficial, no hay audio de
  Hören, no hay usuarias ni testimonios externos.

## Product Principles

1. La duda se muestra, nunca se disimula: toda respuesta lleva su cita, su confianza
   y, cuando la hay, su segunda lectura.
2. El examen manda: alemán verbatim para el contenido, traducción solo para la ayuda.
3. Se abre y ya está: sin servidor, sin cuenta y sin instalar nada.
4. El progreso es de quien estudia y sobrevive al cierre, separado por perfil.
5. Nada entra en el entregable sin pasar validación, humo, seguridad y diseño.

## Accessibility & Inclusion

`design_audit.js` exige contraste ≥4.5:1, espaciado múltiplo de 4 px, áreas táctiles
de 28/44 px, foco visible y respeto a `prefers-reduced-motion`. Diana estudia en
ruso: la ayuda debe seguir existiendo en los dos idiomas, no solo en español.
