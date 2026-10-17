# Test B2 Beruf — Lesen y Hören

Aplicación web **offline** para practicar el examen **telc Deutsch-Test für den
Beruf B2**. Presenta las preguntas, permite responderlas y muestra la respuesta
correcta con explicación, la **frase del texto que la justifica** y un **nivel de
confianza**.

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
- En una pantalla ancha (**≥1500px**) la app se pone en modo *mesa de examen*: la
  referencia —los anuncios o el texto de lectura— se queda en la columna
  izquierda, fija y con su propio scroll, y la hoja de preguntas pasa a la
  derecha. Se responde sin subir y bajar a mirar el anuncio. Por debajo de ese
  ancho sigue siendo una sola columna.
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
las transparencias sobre el fondo real y comprueba 44 reglas de diseño (contraste
mínimo 4.5:1, espaciado múltiplo de 4, áreas táctiles de 28px/44px, foco visible,
movimiento reducido, cristal, sombras multicapa y estados de presión).

## Sistema de diseño

Todo el aspecto vive en el bloque `<style>` de `template.html` y sale de tokens
(valores con nombre reutilizables). Para cambiar el tema **no hay que tocar los
componentes**: basta el bloque `:root`.

| Grupo | Tokens | Para qué |
|---|---|---|
| Color | `--bg`, `--panel`, `--panel2`, `--panel3`, `--line` | Fondos y superficies |
| Texto | `--txt`, `--dim`, `--dim-2` | Tres niveles de jerarquía |
| Acento | `--acc`, `--acc-fill-1/2`, `--acc-ink` | Rellenos (texto blanco) y texto de acento |
| Semánticos | `--ok`, `--bad`, `--warn`, `--violet-ink` y sus `-ink` | Aciertos, fallos, avisos |
| Espaciado | `--sp-1` … `--sp-8` (4, 8, 12, 16, 24, 32, 48, 64) | Rejilla de 4/8pt |
| Tipografía | `--fs-micro` … `--fs-h2` (11, 12, 13, 15, 17, 20, 27) | Seis pasos, sin tallas sueltas |
| Movimiento | `--dur-1/2/3`, `--ease`, `--spring` | Duraciones y curvas elásticas |
| Elevación | `--sh-1/2/3`, `--lit` | Sombra amplia + corta, borde de luz |
| Estructura | `--header-h`, `--nav-w`, `--read-w` | Alto de cabecera, ancho del índice y medida de lectura |
| Mesa de examen | `--desk-ref`, `--desk-work` | Ancho de la columna de referencia y tope de la hoja de preguntas a partir de 1500px |

Las tres familias tipográficas son del sistema (`--font-ui`, `--font-read` serif
para textos largos y `--font-mono`): la app sigue funcionando sin conexión y sin
descargar fuentes.

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

## Verificación de las respuestas

Como **no hay clave oficial**, cada respuesta pasa dos filtros:

1. **Marca de confianza** (`hoch` / `mittel` / `niedrig`) puesta por quien la deduce.
2. **Segunda lectura independiente**: un revisor resuelve el ejercicio por su cuenta
   **antes** de ver el JSON y reporta solo los desacuerdos. Las respuestas que
   coinciden se anotan en `verified.json` y la app las marca con la insignia
   **«✓ 2ª lectura»**.

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
- **Coherencia entre variantes**: si el mismo enunciado lleva respuestas distintas,
  distingue tres casos — conflicto real (mismo texto y mismas opciones → aviso),
  cambio de versión del texto (informativo) y opciones distintas (informativo).

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
