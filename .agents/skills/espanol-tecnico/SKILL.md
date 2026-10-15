---
name: espanol-tecnico
description: >-
  Aplica el estándar de Español Técnico Simplificado (ETS / adaptado de la norma aeroespacial ASD-STE100).
  Elimina ambigüedad, rodeos y relleno en documentación técnica, prompts de agentes/NPCs,
  descripciones de herramientas y manuales. Fuerza frases cortas, modo imperativo directo,
  consistencia terminológica y explicación de tecnicismos. Usar cuando el usuario pida
  "español técnico", "simplificar documentación", "estilo técnico", "ets", "/ets", o
  redactar prompts claros sin ambigüedad.
argument-hint: "[documento | prompt | funcion | regla]"
license: MIT
---

# Español Técnico Simplificado (ETS)
> *Adaptación al español de la especificación aeroespacial ASD-STE100 para IA y desarrollo de software.*

El objetivo de ETS es **cero ambigüedad** y **cero relleno**. Una instrucción técnica debe tener un único significado posible tanto para humanos como para modelos de lenguaje.

---

## 1. Principios Fundamentales de Redacción

### A. Modo Imperativo Directo (Prohibida la pasiva refleja)
El español tiende a usar rodeos impersonales que oscurecen quién ejecuta la acción. En ETS se utiliza siempre la orden directa:
* ❌ *No usar:* *"Se procederá a realizar la inicialización de la base de datos", "Se debe comprobar el token"*.
* ✔ *Usar:* *"Inicializa la base de datos"*, *"Comprueba el token"*.

### B. Una Sola Acción por Oración
No encadenes múltiples acciones con conjunciones o comas.
* ❌ *No usar:* *"Guarda los cambios, ejecuta el comando de pruebas y si falla revisa los registros del servidor"*.
* ✔ *Usar:*  
  1. Guarda los cambios.  
  2. Ejecuta el comando de pruebas.  
  3. Si las pruebas fallan, revisa los registros del servidor.

### C. Límites Estrictos de Longitud
* Máximo **20 palabras** por paso o instrucción de procedimiento.
* Máximo **25 palabras** por frase explicativa o descriptiva.

### D. Lista Negra de Términos Vagos
Prohibido usar palabras indeterminadas que den lugar a interpretación subjetiva:
* ❌ *adecuado, apropiado, correcto* → ✔ Específica el criterio exacto (*"valor mayor que 0"*, *"estado 200 OK"*, *"cadena de texto no vacía"*).
* ❌ *normalmente, usualmente, por lo general* → ✔ Define la condición explícita (*"si el modo depuración está activo"*, *"en entorno local"*).
* ❌ *etc., y demás, entre otros* → ✔ Enumera todos los elementos o indica la categoría completa.
* ❌ *fácilmente, rápidamente, simplemente* → ✔ Elimina estas palabras vacías de relleno.

### E. Consistencia Terminológica (Un concepto = Un término)
Elige una sola palabra para cada concepto técnico y consérvala en todo el documento:
* Si llamas a un dato *"parámetro"*, prohíbe alternar con *"argumento"*, *"variable"* o *"propiedad"* dentro del mismo contexto.

---

## 2. Explicación Obligatoria de Tecnicismos
Cuando el texto esté destinado a comunicación con el usuario o a documentación general:
* Todo término técnico, anglicismo o acrónimo debe ir acompañado inmediatamente de una explicación sencilla entre paréntesis.
* Ejemplo: *"El adaptador utiliza un webhook (un mecanismo para que un servidor avise automáticamente a otro cuando ocurre un evento) para notificar cambios."*

---

## 3. Estructura Estándar de Procedimientos
Al redactar guías paso a paso o reglas de juego, estructura cada bloque en tres partes:
1. **Condición (si aplica):** *"Si la tirada de dados es menor que 10..."*
2. **Acción directa:** *"Aplica la penalización de fatiga..."*
3. **Resultado observable:** *"El valor de energía del personaje disminuye en 5 puntos."*
