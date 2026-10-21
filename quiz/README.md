# Test B2 Beruf — Lesen, Hören, Sprachbausteine y Schreiben

Aplicación web **offline** para practicar el examen **telc Deutsch-Test für den
Beruf B2**. Presenta las preguntas, permite responderlas y muestra la respuesta
correcta con explicación, la **frase del texto que la justifica** y un **nivel de
confianza**. Incluye además el módulo de **Schreiben** con evaluación por IA y los
ejercicios de huecos de **Sprachbausteine** (Teil 1 y Teil 2).

> ⚠ **Las respuestas correctas no existen en el documento original.** Las he
> deducido leyendo el texto. Por eso cada respuesta lleva la cita literal que la
> sostiene y una marca de confianza: para que puedas distinguir un acierto de una
> duda en lugar de fiarte a ciegas.

---

## Uso

Abre **`B2_quiz.html`** con doble clic. Es un único fichero autocontenido: no
necesita servidor, ni Internet, ni instalar nada. Los datos van incrustados.

- Elige una variante en la barra lateral.
- En **Lesen Teil 1** verás los 8 anuncios (a-h) arriba y una fila de letras bajo
  cada persona: pulsa la letra que corresponda. Los anuncios que **tú** ya has
  asignado salen en azul con `✓` y el resumen cuenta cuántos llevas; los libres,
  en ámbar. Ese estado es tu progreso, nunca la solución: la app no dice qué
  anuncios son correctos hasta que respondes.
- Con la ventana ancha (**≥1280px**) la app se pone en modo *mesa de examen*: la
  referencia —los anuncios o el texto de lectura— se queda en la columna
  izquierda, fija y con su propio scroll, y la hoja de preguntas pasa a la
  derecha. Se responde sin subir y bajar a mirar el anuncio. Por debajo de ese
  ancho sigue siendo una sola columna, y el botón **Mesa de examen** de la
  cabecera lo fuerza o lo apaga cuando el ancho no compensa (se recuerda).
- En el modo mesa, pasar el ratón (o el foco) por una letra enciende su anuncio y
  escribe debajo cuál es. Las letras que ya tiene asignadas **otro** enunciado
  salen con el filete discontinuo.
- Se responde con ratón o con teclado: Tab entra en la fila de letras y las
  flechas recorren y eligen. Bajo cada respuesta corregida hay **Borrar esta
  respuesta**, para deshacerla sin borrar el ejercicio entero.
- En **Lesen Teil 2** el texto de lectura está en un panel plegable.
- Al responder aparece la corrección con la cita y la confianza.
- El progreso se guarda en el navegador (`localStorage`). «Reiniciar» lo borra.

---

## Estructura

```
quiz/
├─ B2_quiz.html          ← el entregable (generado, no editar a mano)
├─ template.html         ← plantilla de la app: HTML + CSS + JS
├─ build.py              ← valida los datos y genera B2_quiz.html
├─ SPEC.md               ← contrato de datos que siguen los extractores
├─ make_quiz_sources.py  ← parte el Markdown en bloques por página
├─ make_sprachbausteine.py  ← extrae los Sprachbausteine (Teil 1 y 2)
├─ make_sprechen_t2.py    ← extrae el mazo de Smalltalk (Sprechen Teil 2)
├─ sprechen_t2_es.json    ← traducción al español de las 104 tarjetas (a mano)
├─ make_sprechen_t3.py    ← extrae las 67 situaciones (Sprechen Teil 3)
├─ merge_t3_ayuda.py      ← funde los cuatro bloques de ayuda de T3
├─ sprechen_t3_ayuda.json ← ayuda ES/RU, títulos y ejemplos de T3 (a mano)
├─ merge_sprachbausteine_respuestas.py  ← funde las respuestas deducidas
├─ sprachbausteine_respuestas.json  ← respuestas de los Sprachbausteine (a mano)
├─ _resp_*.json          ← deducción por grupos; el merge los funde en el anterior
├─ smoke_test.js         ← ejecuta el visor con un DOM simulado
├─ design_audit.js       ← audita el diseño: contraste WCAG, rejilla de 4pt, áreas táctiles, foco, físicas
├─ verified.json         ← respuestas confirmadas por una 2ª lectura
├─ data/                 ← un JSON por bloque (la fuente de verdad)
└─ src/                  ← Markdown por bloque, entrada de los extractores
```

## Reconstruir

```powershell
$py = "C:\Users\sergi\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe"
$node = "C:\Users\sergi\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\node\bin\node.exe"

& $py quiz\make_quiz_sources.py out\B2_ohne_antworten.md quiz\src
& $py quiz\make_schreiben.py
& $py quiz\make_full_forums.py
& $py quiz\merge_sprachbausteine_respuestas.py quiz
& $py quiz\make_sprachbausteine.py out\B2_ohne_antworten.md quiz
& $py quiz\merge_t3_ayuda.py quiz\src\t3_ayuda_1.json quiz\src\t3_ayuda_2.json quiz\src\t3_ayuda_3.json quiz\src\t3_ayuda_4.json quiz\sprechen_t3_ayuda.json
& $py quiz\make_sprechen_t3.py out\B2_ohne_antworten.md quiz\sprechen_t3_draft.json quiz\sprechen_t3_ayuda.json quiz\data\sprechen_t3.json
& $py quiz\build.py quiz\data quiz\template.html quiz\B2_quiz.html
& $node quiz\smoke_test.js quiz\B2_quiz.html
& $node quiz\security_test.js quiz\B2_quiz.html
& $node quiz\design_audit.js quiz\template.html
```

Los dos primeros regeneran el catálogo de Schreiben. Ojo con el reparto:
`make_schreiben.py` escribe **solo** `data/schreiben_beschwerde.json` (13 tareas
de las pp. 66-77) y `make_full_forums.py` **solo** `data/schreiben_forum.json`
(98 temas de las pp. 98-106, en el orden de la tabla del PDF y numerados 1-98).
La lista `foren` que sigue dentro de `make_schreiben.py` es un subconjunto
antiguo de 8 temas: no la vuelvas a volcar sobre el fichero.

En los Forumsbeiträge, `num` es la posición en el PDF y manda el orden del menú;
los `id` **no** siguen esa numeración (se dejaron como estaban para no perder
borradores ni evaluaciones ya guardados, que van por `id`).

`build.py` **valida antes de generar** y no escribe el HTML si hay errores.
`smoke_test.js` ejecuta el visor con un DOM simulado: detecta errores de ejecución
que un simple chequeo de sintaxis no ve.
`security_test.js` cubre los cuatro fallos críticos de la auditoría del 17/10/2026
(inyección por `?room=`, ruptura del atributo `value` del modal, evaluación de la
pareja con datos maliciosos y evaluación malformada que rompía la pantalla).
`design_audit.js` no abre ningún navegador: lee el CSS, resuelve los tokens, compone
las transparencias sobre el fondo real y comprueba **75 reglas de diseño en los dos
temas** (contraste mínimo 4.5:1 sobre la superficie real de cada texto, en oscuro y
en claro; espaciado múltiplo de 4; áreas táctiles de 28px/44px; foco visible;
movimiento reducido; relieve; un solo degradado de fondo; el segundo tema por tokens
y no por filtros; y estados de presión).

## Sistema de diseño

Todo el aspecto vive en el bloque `<style>` de `template.html` y sale de tokens
(valores con nombre reutilizables). Para cambiar el tema **no hay que tocar los
componentes**: basta el bloque `:root`.

| Grupo | Tokens | Para qué |
|---|---|---|
| Color | `--bg`, `--panel`, `--panel2`, `--panel3`, `--line` | Fondos y superficies |
| Texto | `--txt`, `--dim`, `--dim-2` | Tres niveles de jerarquía |
| Acento | `--acc`, `--acc-fill-1/2`, `--acc-ink`, `--on-acc` | Relleno del botón (con tinta **oscura**, 5.6:1) y texto de acento |
| Semánticos | `--ok`, `--bad`, `--warn`, `--violet-ink` y sus `-ink` | Aciertos, fallos, avisos |
| Rellenos de estado | `--bien-fill`, `--mal-fill` y sus `-ink` | Letras corregidas: sólidos y oscuros, 6.2:1 y 7.4:1 |
| Espaciado | `--sp-1` … `--sp-8` (4, 8, 12, 16, 24, 32, 48, 64) | Rejilla de 4/8pt |
| Tipografía | `--fs-micro` … `--fs-h2` (11, 12, 13, 15, 17, 20) | Seis pasos, sin tallas sueltas |
| Movimiento | `--dur-1/2/3`, `--ease`, `--spring` | Duraciones y curvas elásticas |
| Relieve | `--sh-1/2/3`, `--bisel`, `--hundido`, `--lit` | Sombra de fuera (altura) + filo de dentro (material); `--hundido` para los huecos |
| Brillo | `--glow`, `--halo` | Azul, y solo en el foco, en lo elegido y en la acción principal |
| Radios | `--r-1` … `--r-4`, `--r-pill` | 4 / 8 / 12 / 18 px, los de la referencia |
| Grosores | `--b-sutil`, `--b-std`, `--b-fuerte` | 0.5 / 1 / 1.5 px |
| Estructura | `--header-h`, `--nav-w`, `--read-w` | Alto de cabecera, ancho del índice y medida de lectura |
| Mesa de examen | `--desk-ref`, `--desk-work` | Ancho máximo de la columna de referencia (fluida con `clamp`) y tope de la hoja de preguntas a partir de 1280px |

### Lenguaje de piezas (dos temas)

**Esta rama (`UXUI`) es un experimento**: cambia el material de la app. En `main`
el mundo es la hoja de examen impresa; aquí son dos mundos con la misma lengua de
piezas, uno para cada uno: **Diana trabaja en claro y Sergio en oscuro**, y cambiar
de perfil cambia el tema (además del idioma). El botón de tema sigue mandando si
alguno quiere cambiarlo en ese momento.

| | Oscuro — «taller nocturno» | Claro — «Calma» |
|---|---|---|
| Mesa y piezas | carbón `#25262a` y `#313239` | marfil `#EDEBE3` y `#FAF9F4` |
| Acento | azul `#4d8df6`, tinta **oscura** (5,6:1) | verde bosque `#0F5132`, tinta **marfil** (6,2-8,9:1) |
| De dónde viene la altura | del **filo claro** de arriba: una sombra negra sobre carbón casi no se ve | del **borde** y una sombra corta: un filo blanco sobre marfil tampoco se ve |
| Estados | verde y rojo claros con brillo | verde bosque y terracota, y **menta** `#B7D9C1` en los tintes |

- **Una sola luz**: el fondo lleva un único degradado cenital fijo. No hay texturas
  ni patrones, y se comprueba que sea el único degradado de fondo.
- **Relieve solo en lo que se pulsa.** Cada pieza lleva su sombra de fuera (altura)
  y su filo claro arriba (material): letras a–h, botones, conmutadores, pestañas,
  filas pulsables, el número del ítem. El texto —los anuncios alemanes, la cita,
  la explicación— se queda plano: el relieve en un párrafo largo solo estorba.
- **Tres mecanismos, y cada bloque usa uno**: pieza con filo (`--panel` + `--bisel`),
  hueco hundido (`--sunken` + `--hundido`) para campos, carriles y celdas, o banda
  con tinte y filo en el color del estado (`.fb`, `.note`, insignias).
- **Lo que flota de verdad** —modal, popover de error, enlace de salto— es lo único
  que lleva sombra profunda (`--sh-3`).
- **El brillo del acento** (`--glow`, `--halo`) está reservado al foco, a lo elegido
  y a la acción principal. Con desplazamiento, nunca como cerco de desplazamiento cero.
- **Los controles dicen lo que está encendido.** En un control segmentado (perfil,
  idioma, pestañas de Schreiben) la opción activa se **rellena con el acento** —azul
  en oscuro, verde en claro—, no con una pastilla clara, y el relleno es un **mando
  que se desliza** de una opción a otra con curva de resorte. El JS mide la opción
  encendida y le pasa su posición y su ancho al CSS (`--mando-x`, `--mando-w`); si no
  se puede medir, se quita la clase `con-mando` y la opción activa se marca con su
  propio relleno, así que nunca se queda sin señal. Y el tema es un **interruptor**:
  pista con el mando redondo, el **icono dentro del mando** (luna si estás en oscuro,
  sol si estás en claro: enseña el estado, no la acción) y la pista encendida cuando
  el modo oscuro está activo.
- **Los formularios sí llevan borde**: un campo necesita un límite definido.
- **Dos temas por tokens**: el oscuro en `:root` y el claro en
  `[data-theme="paper"]`. El lenguaje de piezas es el mismo; cambian los valores.
  Cualquier color escrito a mano en un componente rompe el segundo tema, así que los
  filos de estado (`--line-ok/-bad/-warn/-acc`) y los rellenos (`--bien-fill`,
  `--mal-fill`) también son tokens.

Las tres familias tipográficas son del sistema (`--font-ui`, `--font-read` serif y
`--font-mono`): la app sigue funcionando sin conexión y sin descargar fuentes.

**Reparto de las dos voces** — es lo que hace que la app no parezca una plantilla:

- **Sans (`--font-ui`) para la interfaz y para lo que se lee**: titulares, rótulos,
  anuncios, textos de examen, enunciados, el área de escritura. Es la voz de trabajo.
- **Serif (`--font-read`) solo para lo que se cita o se escribe**: la cita literal
  del bloque de corrección, la carta recibida, la redacción modelo, el texto anotado,
  la redacción de la pareja y las fichas de letra a–h. Es la voz del papel.

El titular de sección es sans de 20 px y la cabecera va a 17 px con los controles a
32 px: la barra queda tensa y el contenido manda.

## Bilingüismo (ES / RU)

La regla es una: **lo que es examen va en alemán; lo que es ayuda va traducido.**
Los textos alemanes (enunciados, opciones, pasajes, citas) no se tocan nunca,
porque son justo lo que hay que practicar.

| Qué | Dónde vive | Cómo se traduce |
|---|---|---|
| Interfaz (botones, avisos, errores) | `I18N` en `template.html` | Clave en `es` y en `ru`. `smoke_test.js` falla si una clave existe solo en un idioma. |
| Avisos del extractor (⚠) | `note_ru` junto a `note` en `quiz/data/*.json` | Se usa `note_ru` en ruso; si falta, cae al español. |
| Rótulos de variante | `label` en los datos | `localizeLabel()` traduce el andamiaje («Variante» → «Вариант», «nueva versión» → «новая версия», «test» → «тест») y deja intactos los nombres alemanes (Beschwerde, Protokoll, temas). |
| Partes del examen | `SECTIONS` en `build.py` | `localizeSection()` añade la glosa rusa al nombre alemán («Lesen Teil 1 · Чтение 1»). |
| Explicaciones de cada respuesta | `explain_ru` junto a `explain` en `quiz/data/*.json` | Se usa `explain_ru` en ruso; si falta, cae al español. `smoke_test.js` comprueba que las 226 la tengan. |

Para añadir la versión rusa de un aviso o de una explicación, escribe `"note_ru"`
o `"explain_ru"` justo debajo de su campo en español, en el JSON de la variante.
`smoke_test.js` comprueba que cada aviso (`note`) y cada explicación (`explain`)
tengan su versión rusa, y que el diccionario de la interfaz esté completo en los
dos idiomas.

## Seguridad y sincronización

- **La sincronización es opcional.** Sin configurar Firebase la app funciona en local
  y no sale nada del navegador.
- **El progreso de redacción es de cada perfil.** El borrador, la evaluación y los
  Leitpunkte se guardan con el perfil dentro de la clave (`sergio::schr-b-p66`), así
  que cambiar de perfil en el mismo navegador no mezcla el trabajo de los dos. Lo
  guardado con la clave antigua (solo el id) se migra solo al abrir la app, y se le
  asigna al perfil que estuviera abierto en ese momento.
- **Abrir la app en otro navegador recupera tu lado desde la nube.** Si este navegador
  no tiene tu borrador ni tu evaluación y la sala sí los tiene, la app los trae y los
  pinta. Además refresca una copia local que se quedó vieja: si no tienes nada sin
  enviar y la nube dice otra cosa, manda la nube. Lo que **nunca** ocurre es perder
  ediciones sin enviar: mientras el borrador local no coincida con lo último que se
  envió, la nube no lo toca. Un texto vaciado a propósito tampoco se rellena solo.
- **La sala es el único secreto.** Al abrir la app por primera vez se genera un
  identificador aleatorio (`b2-…`) y se guarda en el navegador; el fichero `index.html`
  de la raíz permite compartir el enlace corto `…/<repo>/?user=diana&room=b2-…`.
  Compártelo solo con Diana: quien tenga ese enlace puede leer y escribir vuestras
  redacciones, porque no hay login. El enlace se copia desde «⚙ Configurar IA».
- **Las claves de API viven solo en tu `localStorage`** y viajan directamente al
  proveedor que elijas: no se comparten con la pareja ni con GitHub Pages.
  En el modal «⚙ Configurar IA» la cabecera dice el proveedor activo, si hay clave
  guardada (enmascarada) y si el navegador deja guardarla; con «Ver clave» se
  comprueba lo que hay dentro del campo. **«Probar conexión» también guarda**, así
  que probar no deja la clave a medias. Si el navegador bloquea el almacenamiento,
  la clave sigue funcionando durante esa sesión (queda en memoria) y el modal lo
  avisa en vez de perderla en silencio.
  Ojo: abrir la app como fichero local (`file://`) y abrirla desde el enlace web
  son **dos almacenes distintos**; lo guardado en uno no aparece en el otro.
  Si una prueba falla con «no he podido llegar al servidor», el problema es de red,
  clave o endpoint, no del guardado.
- La insignia de la nube dice la verdad: si una escritura falla, muestra
  «Sin sincronizar» en rojo. Un borrador escrito sin conexión se sube al volver a
  abrir la tarea (solo si la nube aún no tiene nada tuyo: nunca pisa un texto que sí llegó).
- `firestore.rules` valida tipos y rangos (incluidos `score_total` y `verdict` de las
  evaluaciones), impide listar salas y tareas, prohíbe borrar y no deja que un `set()`
  sin merge elimine campos que ya existían. **No separa por usuario**: eso exigiría
  autenticación (login anónimo + `request.auth.uid`).

## Cómo puntúa la escritura (Schreiben)

Los cuatro criterios y las bandas A/B/C/D son los de telc, y los pesos también
(Übungstest DTB B2, pp. 40-41): la tarea de escritura da 14 puntos al criterio I
—*Kommunikative Aufgabenbewältigung*— y 9 a cada uno de los II-IV —*Kommunikative
Gestaltung*, *Formale Richtigkeit*, *Spektrum sprachlicher Mittel*—, con bandas al
100 %, ~75 %, ~39 % y 0 %.

La app usa una escala de 100 puntos con esas mismas proporciones (**I = 34, II-IV = 22**).

El criterio I sigue el descriptor de telc para los Leitpunkte. Con uno menos, la banda
máxima es B; con dos menos, C; con tres o más, D. `smoke_test.js` fija ese mapeo, así
que el documento no puede separarse del código otra vez.

La app añade **dos reglas propias, más estrictas que el examen**:

- **D suspende**: un criterio en D suspende aunque la suma llegue a 60.
- **Longitud**: el criterio I no pasa de C con menos de 100 palabras, ni de B entre 100 y 149.

En el examen real esas dos reglas no existen: se aprueba con el 60 % de 240 puntos y un
subtest se puede compensar.

Los puntos los calcula la app a partir de las bandas que da el modelo
(`puntuarCriterios` en `template.html`), así que el mismo juicio da siempre el mismo
número y lo que escriba el modelo en `score` se ignora. El recuento de palabras también
lo hace la app: el modelo lo inflaba entre un 15 % y un 20 %.

---

### Cómo corrige los errores (el corrector)

`prompt_schreiben.py` define el contrato. A raíz de una redacción del foro con 5
marcas, de las que 2 estaban mal analizadas, el prompt exige que cada entrada
traiga un `change` —qué cambia exactamente— y prohíbe lo que falló:

- **Reescribir**: `corrected_version` es el texto del alumno con SOLO las
  correcciones listadas. La versión libre de 100 puntos es `musterloesung`.
- **Spans anchos**: se cita la palabra o el fragmento mínimo, no el párrafo
  (tope de 80 caracteres). El caso real marcó una oración de 101 caracteres por
  una sola mayúscula.
- **Alternativas** en `correction` («A / B»): una sola versión. Con dos opciones,
  una de ellas era idéntica al original.
- **Reglas inventadas**: si el cambio es solo de mayúsculas, la regla habla de
  mayúsculas. Antes inventó una «falta de declinación» en «für alle Beteiligten»,
  donde la terminación ya era correcta.

La lista de trampas del prompt (adjetivo sustantivado tras «alle», genitivo tras
«zum Thema», «und» entre subordinadas, coma de «Liebe Grüße») cierra los tres
fallos concretos: proponer «die» como relativo donde va el nominativo, inventar el
error de declinación y borrar la coma de la despedida al generalizar la regla de
«Mit freundlichen Grüßen».

`validate_evaluation_json(data, texto_del_alumno)` comprueba lo mecánico: cita
literal, span mínimo, corrección única, `change` presente, regla coherente con el
delta y cada corrección aplicada en `corrected_version`.

```powershell
& $py quiz\test_correccion.py   # regresión del corrector con el caso real
& $py quiz\test_prompt.py       # contrato de la rúbrica y del JSON

# prueba en vivo contra Gemini, con el texto real (necesita clave):
& $py quiz\test_correccion.py --gemini-key $env:GEMINI_API_KEY --model gemini-3.5-flash --save resp.json
```

---

## Verificación de las respuestas

Como **no hay clave oficial**, cada respuesta pasa dos filtros:

1. **Marca de confianza** (`hoch` / `mittel` / `niedrig`) puesta por quien la deduce.
2. **Segunda lectura independiente**: un revisor resuelve el ejercicio por su cuenta
   **antes** de ver el JSON y reporta solo los desacuerdos. Las respuestas que
   coinciden se anotan en `verified.json` y la app las marca con la insignia
   **«✓ 2ª lectura»**.

Esto vale también para los **Sprachbausteine**: el documento tampoco trae su clave
(lo dice `GUIA_B2.md`), así que sus 132 huecos se deducen del alemán y viven en
`quiz/sprachbausteine_respuestas.json`. `merge_sprachbausteine_respuestas.py` comprueba
lo comprobable —respuesta dentro de las opciones, cita literal, sin repetir letras en
el Teil 1— y lo que no puede comprobar es la gramática: eso es la marca de confianza.
Las variantes que el PDF dejó incompletas (la 8 del Teil 2, sin las opciones b y c) se
descartan en vez de ofrecerse mal.

El botón **«Solo dudosas»** filtra las respuestas de confianza media o baja para
revisarlas contra el texto original.

## Qué valida `build.py`

- Campos obligatorios presentes.
- `confidence` ∈ {`hoch`, `mittel`, `niedrig`}.
- `quote` y `explain` no vacíos.
- **En `zuordnung`: las 5 respuestas son letras distintas** y están entre los
  anuncios a-h. Es la regla que delata un emparejamiento mal hecho.
- `answer` existe entre las opciones del ítem.
- `kind: "text"` tiene `passage`, y avisa si es sospechosamente corto
  (¿texto truncado?).
- Avisa si no quedan exactamente 3 anuncios sin usar.
- Detecta `id` duplicados en todo el proyecto.
- **Cobertura del bloque Beschwerde**: cada «Variante N» de la parte de lectura
  (`ls_*.json`, variantes 1-9 de las pp. 66-77) tiene que tener su tarea de
  redacción con ese `source_variant`. Faltaban las variantes 3, 8 y 9 y el HTML
  se generaba igual: ahora el build se niega y las nombra.
- **Orden del bloque Forumsbeitrag**: el menú se ordena por (página, `num`), y
  `num` es la posición en la tabla del PDF (pp. 98-106). Un `num` repetido, con
  huecos o ausente detiene el build.
- **Ejercicios de huecos (Sprachbausteine)**: la respuesta tiene que estar en el banco
  de palabras (Teil 1) o entre las tres opciones del hueco (Teil 2), y en el Teil 1
  las seis respuestas han de ser **letras distintas**, porque cada palabra se usa una
  sola vez.
- **Citas literales**: la `quote` tiene que aparecer en el `passage` del que sale. En
  los huecos del Teil 1 vale la frase del texto con el hueco marcado, porque ahí la
  opción es una sola palabra y no puede contener la cita.
- **Coherencia entre variantes**: si el mismo enunciado lleva respuestas distintas,
  distingue tres casos — conflicto real (mismo texto y mismas opciones → aviso),
  cambio de versión del texto (informativo) y opciones distintas (informativo).
- **Mazo de Smalltalk (`kind: "smalltalk"`)**: cada tarjeta necesita su alemán y su
  ayuda en español y en ruso (no hay dónde caer si falta una), la numeración tiene
  que ser 1..N sin huecos ni repetidos, y avisa si el mazo trae menos de 20 tarjetas.
  Aquí no se validan `quote` ni `confidence`: no hay respuesta que deducir.
- **Situaciones de Sprechen T3 (`kind: "situation"`)**: cada una es una variante y
  lleva título, descripción alemana, ayuda ES/RU, al menos un Stichpunkt traducido a
  los dos idiomas y dos ejemplos de habla en alemán. La numeración de la sección es
  1..67 sin huecos. Tampoco hay clave: el ejercicio es discutir una solución, no
  acertar una letra.

## Smalltalk (Sprechen Teil 2)

Las 104 preguntas del Teil 2 son un **mazo de tarjetas**, no un ejercicio corregible:
no llevan clave, cita ni confianza porque no se acierta, se habla. La página las
enseña todas en dos mitades (1–52 y 53–104) y tiene un **mesa de trabajo** que se
enciende con un interruptor: saca una carta al azar, no la repite hasta agotar el
mazo, deja devolverla a la baraja y guarda tus notas de esa carta por perfil.

- El alemán va verbatim del documento; las dos formulaciones separadas por « / » van
  en la misma tarjeta (campo `alt`), para que el número coincida con el del PDF.
- La ayuda (traducción ES y RU) va plegada detrás de un botón en cada carta. El ruso
  lo trae el documento en las 104; el español lo aporta `sprechen_t2_es.json`.
- Las erratas del original se corrigen en `CORRECCIONES` (dentro de
  `make_sprechen_t2.py`) y cada una se anota en `fixes`. El script falla si la errata
  ya no está: no corrige a ciegas.

## Situationen (Sprechen Teil 3)

Las 67 situaciones de «Lösungswege diskutieren» también se hablan, no se corrigen.
**Cada una es una entrada del menú y su propia página**, no una rejilla con ventana.
En la página se ve:

- la descripción alemana, **verbatim** del documento;
- los Stichpunkte en alemán.

La ayuda y los ejemplos **no salen solos**: quedan detrás de dos bloques plegables,
«Ver ayuda (ES · RU)» y «Ver ejemplos en alemán». Así se lee el caso y se habla sin
la traducción delante. Abajo hay **Anterior / Siguiente** para pasar de situación sin
volver al menú.

- El alemán lo extrae `make_sprechen_t3.py` del bloque de las pp. 188-200. El script
  cose los guiones de corte, quita números de página y enlaces, y falla si la
  numeración no es 1..67.
- Cada variante se queda con la página donde empieza su situación, para que el
  rótulo del PDF no mienta.
- Los Stichpunkte de las situaciones 14, 44, 56 y 59 venían mezclados por columnas en
  el PDF; se ordenan a mano en `STICHPUNKTE_MANUALES` sin cambiar el texto.
- La ayuda (títulos, traducciones y ejemplos) se escribe a mano en
  `quiz/src/t3_ayuda_*.json` y se funde con `merge_t3_ayuda.py`. Los ejemplos son
  nuestros, no del examen: sirven para practicar, no se presentan como material
  oficial.

## Niveles de confianza

| Nivel | Significado |
|---|---|
| `hoch` | El texto contiene una frase que responde directamente. |
| `mittel` | Se deduce por eliminación o por el sentido global. |
| `niedrig` | El texto es ambiguo o incompleto; **revísalo tú**. |

## Huecos conocidos del documento fuente

Hay contenido del PDF **que no se puede convertir en preguntas respondibles**
porque el original no trae el texto del que deducir la respuesta. Se documentan
aquí para no rellenarlos con invenciones:

| Página | Bloque | Qué falta |
|---|---|---|
| **149** | Hören Teil 2, variante 7 (test 160201/160221) | **No hay transcripción.** Solo las 6 afirmaciones (a–f) con glosas en ruso del compilador, que él mismo marca como poco fiables («*no encajaba en ningún sitio*»). |
| **176** | Hören Teil 4, variante 7 (test 140321/140301) | **Solo las preguntas** (36–40), sin una línea de transcripción. |

Además, el documento es una recopilación de exámenes reales, así que hay
**variantes incompletas** y **dos erratas del original** que se han respetado
(solo se corrigen y se anotan en `fixes` las que no cambian el sentido):

- p. 18, anuncio `h)` truncado a mitad de frase («…Auslandsaufenthalte können»).
- Las **transcripciones de Hören no son el audio oficial**, sino lo que los
  candidatos recordaban y transcribieron: sirven para practicar, no como texto
  normativo.

## Añadir una sección nueva

1. Añade el bloque a `BLOCKS` en `make_quiz_sources.py` y regenera `src/`.
2. Encarga el JSON siguiendo `SPEC.md`, con `section` igual a una de las claves
   de `SECTIONS` en `build.py` (`lesen-t3`, `hoeren-t1`…).
3. Deja el fichero en `data/` y vuelve a ejecutar `build.py`.

La sección aparece sola en la barra lateral, en el orden definido por `ORDER`.
