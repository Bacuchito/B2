# Regla: Comunicación Clara y Explicación de Tecnicismos

Esta regla es **obligatoria y permanente** para todas las herramientas de Inteligencia Artificial que trabajen en este proyecto (Antigravity, Claude Code, Cline, Codex, Cursor, etc.).

---

## 1. Directo y sin Relleno
- Comunica de forma directa, concisa y orientada a la acción.
- Evita párrafos ceremoniales, disculpas innecesarias, introducciones vacías o textos inflados.

---

## 2. Explicación Obligatoria de Palabras Técnicas (Regla Clave)
Cada vez que menciones una palabra técnica, anglicismo de desarrollo, concepto de arquitectura o término de programación, **debes incluir inmediatamente una explicación breve y sencilla en lenguaje terrenal** (entre paréntesis o en una aclaración corta).

### Ejemplos obligatorios:
* **En vez de:** *"He añadido un debounce en el input..."*  
  **Debes decir:** *"He añadido un debounce (un temporizador que espera a que dejes de escribir antes de enviar la petición) en el input..."*

* **En vez de:** *"El endpoint devuelve un payload JSON..."*  
  **Debes decir:** *"El endpoint (la ruta de la API que responde a una solicitud) devuelve un payload (el paquete de datos con la información) en formato JSON..."*

* **En vez de:** *"Aplicamos memoization con useMemo para evitar re-renders..."*  
  **Debes decir:** *"Aplicamos memoization (guardar en memoria el resultado para no tener que recalcularlo desde cero) con useMemo para evitar re-renders (volver a pintar el componente en la pantalla sin necesidad)..."*

* **En vez de:** *"El linter ha detectado un memory leak..."*  
  **Debes decir:** *"El linter (la herramienta que revisa automáticamente errores y estilo de código) ha detectado un memory leak (una fuga de memoria, cuando el programa retiene memoria RAM que ya no necesita y no la libera)..."*

---

## 3. Resumen Práctico
- Explica qué se hizo, por qué se hizo y qué significa en términos fáciles de entender.
- Mantén la precisión técnica sin asumir que el usuario tiene que descifrar la jerga.
