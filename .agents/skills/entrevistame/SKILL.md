---
name: entrevistame
description: >-
  Extrae lo que el usuario realmente quiere, no lo que cree que debería querer. Entrevista de una pregunta
  a la vez, cada una con la hipótesis del agente adjunta, hasta ~95% de certeza. Usar cuando el pedido esté
  incompleto, cuando el usuario diga "entrevístame", "grill me", "interrógame", "antes de empezar", o antes
  de escribir cualquier plan, especificación o código.
license: MIT
---

# Entrevístame: Extraer la Intención Real

> Lo que la gente pide y lo que quiere son cosas distintas. Pide "un panel" porque eso se pide.

El momento más barato para hallar el hueco es antes de que exista plan, especificación (documento que fija requisitos y criterios de aceptación) o código.

## 1. Cuándo Usar

Falta al menos uno de estos datos: **quién** se beneficia, **para qué** lo quiere, **cómo** se mide el éxito, **qué límite** es innegociable, o **qué valor** prioriza si dos chocan.

**No usar si:** el pedido es cerrado ("renombra esta variable"), el usuario pidió velocidad, es consulta de información, o es operación mecánica.

**Requiere usuario vivo.** Sin nadie que responda, reporta el pedido ambiguo como bloqueo. No inventes la intención.

## 2. Proceso

**Paso 1. Hipótesis con confianza.** Escribe tu mejor lectura en una frase, más un porcentaje honesto.

```
HIPÓTESIS: Quieres responder "¿cómo vamos?" antes de jugar.
CONFIANZA: ~30% — falta: para quién, qué se mide, qué es éxito.
```

Si la confianza es menor al 70%, añade qué falta. Sin eso el usuario no sabe qué aclarar.

**Paso 2. Una pregunta por mensaje, con conjetura adjunta.**

```
P:         <una pregunta concreta>
CONJETURA: <tu hipótesis, con el razonamiento que la produjo>
```

Espera la reacción antes de la siguiente. Los lotes producen respuestas superficiales, y la tercera pregunta suele depender de la primera. La conjetura adjunta importa porque corregirla cuesta menos que generar desde cero. Riesgo: un usuario cortés acepta por no discutir. Mitígalo mostrándote dispuesto a equivocarte.

**Paso 3. Detecta "lo que debería querer".** Señales: vocabulario de manual ("escalable", "arquitectura limpia"), escudo en la convención ("como la mayoría de apps"), frases "debería...", palabras de moda como meta. Pregunta entonces:

> *"Si no tuvieras que justificarlo ante nadie, ¿qué querrías de verdad?"*

**Paso 4. Reformula con sus palabras.** Máximo 8 líneas, para corregir línea por línea.

```
- Resultado:        <una línea>
- Usuario:          <una línea>
- Por qué ahora:    <una línea>
- Éxito:            <una línea>
- Límite:           <una línea>
- Fuera de alcance: <una línea — qué NO se hará>

¿Sí, no o corrige?
```

**"Fuera de alcance" es obligatorio.** La mitad del desajuste es desacuerdo silencioso sobre lo que no se construye.

**Paso 5. Exige un sí explícito.** No son un sí: "lo que tú veas mejor" (delegación), "suena bien" (ambiguo), "vale, vamos" (salida cortés), o silencio y luego "ok". Ante esos, repregunta con dos opciones concretas. Repite hasta el sí explícito.

**Paso 6. Detén el turno.** Al confirmar: entrega la intención confirmada, ofrece los caminos siguientes, y para. No ejecutes herramientas ni arranques trabajo posterior en ese turno.

Estás listo cuando predices las tres reacciones siguientes del usuario.

## 3. Tabla Anti-Racionalización

| Racionalización | Realidad |
|---|---|
| "El pedido está claro." | Si no puedes escribir el resultado deseado en una frase, no lo está. Corre el paso 1. |
| "Preguntar mucho le hace perder tiempo." | 4-6 preguntas cuestan poco. Construir lo incorrecto cuesta muchísimo, y lo paga el usuario. |
| "Lo resuelvo mientras construyo." | Cambiar de rumbo con código ya escrito cuesta diez veces más. |
| "Dijo 'lo que tú veas', así que decido yo." | Eso es delegación, no decisión. Repregunta con dos opciones concretas. |
| "Doy varias opciones para que elija." | Las opciones sirven a quien ya sabe qué quiere. Preguntar estrecha; listar ensancha. |
| "Dijo sí, terminamos." | Si siguió a una reformulación vaga, el sí está hueco. Reformula concreto y reconfirma. |

## 4. Banderas Rojas

- Tres o más preguntas en un mensaje: es encuestar, no entrevistar.
- Pregunta sin conjetura adjunta.
- Aceptar "lo que tú veas mejor" como respuesta final.
- Producir plan, especificación o código antes de que confirme tu reformulación.
- Aceptar "escalable", "limpio" o "moderno" sin sondear.
- Tres rondas sin que la confianza suba: preguntas lo equivocado.
- Confianza bajo 70% sin motivo adjunto.
- Omitir la línea "Fuera de alcance".

## 5. Verificación

- [ ] Hipótesis con número de confianza en el primer turno.
- [ ] Cada confianza bajo 70% acompañada de su motivo de una línea.
- [ ] Preguntas de a una, cada una con conjetura.
- [ ] Sondéo "sin justificarlo ante nadie" ante respuestas de convención.
- [ ] Reformulación con los seis campos, incluido "Fuera de alcance".
- [ ] Sí explícito del usuario.
- [ ] Turno detenido sin arrancar trabajo posterior.

---

Adaptado de `interview-me` de [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) (MIT).
