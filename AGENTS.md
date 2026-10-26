# AGENTS.md — puerta de entrada para cualquier agente

Este repo tiene skills, reglas y un grafo. **Cargarlos es obligatorio, y no basta
con saber que existen**: el catálogo de skills da títulos, no instrucciones. Antes
de la primera acción de cada tarea, pasa por esta puerta.

## 1. Antes de responder cualquier cosa sobre el código

```powershell
graphify query "<la pregunta en lenguaje natural>"
```

Devuelve nodos con fichero y línea. Solo después lee con `read`/`grep` lo que el
grafo señale. El grafo es `graphify-out/`; qué entra en él lo decide
`.graphifyignore`. Se actualiza solo en cada commit (hook `post-commit`) salvo los
documentos, que piden `graphify update` a mano.

## 2. Carga la skill antes de empezar, no después

Antes de tocar nada de una tarea, recorre estos cinco pasos en orden.

1. Lee el catálogo de skills: nombre y una línea de descripción de cada una.
2. Elige las que encajan. Una o dos, no todas.
3. Abre la respuesta con una línea visible: `Skills cargadas: X, Y`.
4. Carga cada una con la herramienta `skill`.
5. Empieza el trabajo.
6. Si dos skills empatan, pregunta antes de elegir. Anota la respuesta en §2.1.

Si ninguna encaja, escribe `Skills cargadas: ninguna` y el motivo en la misma
línea. La línea visible es el control: deja que el usuario vea un salto sin leer
el código.

Ejemplo. Tarea: «cambia el espaciado del panel de Schreiben».

- Carga `impeccable`: cambios de CSS, layout y componentes.
- Cierra con `design_audit.js`: el control del repo, no una skill.

La tabla siguiente es la pista. El procedimiento es la regla.

| Si la tarea es… | Carga |
|---|---|
| Escribir o reescribir documentación, prompts, mensajes | `espanol-tecnico` |
| Cualquier cambio o revisión de CSS, layout, componentes | `impeccable` |
| Una pregunta sobre el repo, su arquitectura o sus ficheros | `graphify` |
| Elegir librería, refactorizar, arreglar un bug | `ponytail` |
| Un test rojo, un servidor que no arranca, un error raro | `depuracion-y-recuperacion` |
| Implementar lógica o cambiar comportamiento | `desarrollo-guiado-por-pruebas` |
| Revisar un diff o preparar un merge | `revision-de-codigo` |
| Descomponer algo grande, repartir trabajo | `planificacion-de-tareas` |
| Contrastar un juicio propio o revisar un plan ajeno | `segunda-opinion` |
| Un pedido incompleto o ambiguo | `entrevistame` |

### 2.1 Desempates ya decididos

Pregunta una vez. Anota aquí la respuesta. No vuelvas a preguntar lo mismo.

| Caso | Decisión |
|---|---|
| Cambios de UI/UX en la app | `impeccable` para construir y auditar. `apple-design` solo para crítica con las HIG de Apple o para quitar aire de plantilla. |

## 3. Reglas que no se negocian

1. El alemán del examen va verbatim; la ayuda va traducida (ES/RU).
2. Toda respuesta lleva `quote` literal + `confidence`. Sin cita, no hay ítem.
3. No se inventa lo que el PDF no trae: se documenta el hueco.
4. `quiz/B2_quiz.html` no se edita a mano; se regenera con `build.py`.
5. Nada se da por bueno sin los cuatro controles: `build.py`, `smoke_test.js`,
   `security_test.js`, `design_audit.js`.
6. Ninguna clave de API entra en el repo.
7. El estilo de las respuestas al usuario lo fija §5. Español directo y sin
   relleno (`.agents/rules/comunicacion_clara.md`).
8. No edites estos ficheros sin permiso explícito: `graphify-out/` (generado),
   `out/B2_ohne_antworten.md` (la fuente de los exámenes), `firestore.rules` y
   cualquier fichero de claves (`tools/.oc_key`, `.env*`). Leerlos sí puedes:
   `out/B2_ohne_antworten.md` es justo de donde se deducen las respuestas.

## 4. El contexto largo

`README.md` es el brief completo: stack, partes del examen cubiertas, deuda
conocida y los system prompts de los agentes. `PRODUCT.md` dice para quién es y
qué no se puede romper. `quiz/README.md` es el manual técnico de los datos.

## 5. Cómo respondo al usuario

Estas reglas valen **solo para lo que escribo en el chat**. Los documentos del
repo (README, PRODUCT, SPEC, este fichero) mantienen su propio registro.

- Respuesta por defecto: **20 líneas o menos**. El detalle largo solo si lo pide.
- Frase de **25 palabras como máximo**.
- Una acción por frase.
- Orden directa. Evita el «se» impersonal.
- Cero relleno: fuera «básicamente», «simplemente», «cabe destacar».
- Explica cada tecnicismo la primera vez, entre paréntesis y en lenguaje llano.
- Si la respuesta necesita más de 20 líneas, dilo antes de empezar.

Fuente completa: `.agents/skills/espanol-tecnico/SKILL.md`.

## 6. Flujo de trabajo

El bucle tiene cuatro pasos. No te saltes el 1 ni el 4.

1. **Puerta.** ¿Toca código? `graphify query` antes de `grep`. ¿Qué skills?
   Declaradas en la primera línea, según §2.
2. **Plan.** Tarea no trivial: propón plan y espera el OK. Si el juicio es caro
   o no lo puede comprobar un test, pide `segunda-opinion` antes de decidir.
   Después clasifica el trabajo:
   - **Pequeño** si se retoma con la petición y el `git diff`. Sin documento;
     el plan vive en el chat.
   - **Grande** si no. Un solo documento en `tasks/<nombre>.md`, creado antes
     del primer cambio. Parte de `tasks/TEMPLATE.md`.
3. **Cierre de tarea.** Di qué cambiaste, en qué ficheros y qué control pasaste.
   Si no hay control posible, dilo en vez de insinuar que lo hay. En trabajo
   grande, anota en el documento el resultado observado de cada control, fallos
   incluidos, y el veredicto por tarea.
4. **Cierre de sesión.** Controles verdes, `graphify update` si tocaste
   documentos, y qué queda sin commitear.

Dato que no está en el repo: pregunta. No lo inventes. Si la tarea obliga a
editar una zona prohibida (§3.8), pide permiso antes de tocarla.
