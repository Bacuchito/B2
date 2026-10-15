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
  cada persona: pulsa la letra que corresponda.
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
├─ verified.json         ← respuestas confirmadas por una 2ª lectura
├─ data/                 ← un JSON por bloque (la fuente de verdad)
└─ src/                  ← Markdown por bloque, entrada de los extractores
```

## Reconstruir

```powershell
$py = "C:\Users\sergi\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe"
$node = "C:\Users\sergi\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\node\bin\node.exe"

& $py quiz\make_quiz_sources.py out\B2_ohne_antworten.md quiz\src
& $py quiz\build.py quiz\data quiz\template.html quiz\B2_quiz.html
& $node quiz\smoke_test.js quiz\B2_quiz.html
```

`build.py` **valida antes de generar** y no escribe el HTML si hay errores.
`smoke_test.js` ejecuta el visor con un DOM simulado: detecta errores de ejecución
que un simple chequeo de sintaxis no ve.

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
