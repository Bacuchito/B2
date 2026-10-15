# Plan de Acción: Módulo de Schreiben con Evaluador LLM (telc B2)

> **Objetivo:** Integrar en el visor web offline [`quiz/B2_quiz.html`](./quiz/B2_quiz.html) el módulo de expresión escrita (*Schreiben*) para el examen telc Deutsch-Test für den Beruf B2. Permitirá redactar textos de examen (*Beschwerde* y *Forumsbeitrag*), recibir una evaluación pedagógica oficial con rúbrica telc B2, veredicto de aprobado/suspenso y una versión corregida y optimizada a nivel B2 nativo, conectándose a LLMs (Gemini, DeepSeek, OpenAI o local con Ollama).

---

## Estado Global del Proyecto

- [ ] **Fase 1:** Catálogo y Extracción de Tareas de Schreiben
- [ ] **Fase 2:** Motor de Evaluación y System Prompt Oficial telc B2
- [ ] **Fase 3:** Conector Multi-Proveedor de IA en el Frontend
- [ ] **Fase 4:** Interfaz de Usuario (Editor, Contador y Resultados)
- [ ] **Fase 5:** Pruebas, Smoke Tests y Validación Final

---

## Desglose Detallado de Tareas

### Fase 1: Catálogo y Extracción de Tareas de Schreiben
*Extraer las consignas de redacción del PDF y estructurarlas como fuente de verdad en el proyecto.*

- [ ] **1.1** Localizar e indexar todas las tareas de redacción presentes en [`out/B2_ohne_antworten.md`](./out/B2_ohne_antworten.md):
  - Tareas de correo formal / reclamación (*Beschwerde / Stellungnahme an Kunden oder Lieferanten*, ejercicios 21 de las pp. 66–77).
  - Tareas de foro profesional (*Forumsbeitrag / Diskussion im Intranet*).
- [ ] **1.2** Definir el esquema JSON formal en [`quiz/SPEC.md`](./quiz/SPEC.md) para el bloque `kind: "schreiben"`:
  - Campos requeridos: `id`, `title`, `type` (*email* o *forum*), `page`, `scenario` (situación previa), `leitpunkte` (los 4 puntos guía obligatorios) y `redemittel` (frases útiles sugeridas de apoyo).
- [ ] **1.3** Crear el extractor y generar [`quiz/data/schreiben.json`](./quiz/data/schreiben.json) con todas las tareas catalogadas.
- [ ] **1.4** Actualizar [`quiz/build.py`](./quiz/build.py) para validar la estructura del nuevo bloque y enlazar la sección `schreiben` en la generación del HTML.

---

### Fase 2: Motor de Evaluación y System Prompt Oficial telc B2
*Calibrar el rol y los criterios del LLM como examinador oficial de telc.*

- [ ] **2.1** Redactar el System Prompt del examinador basándose en la matriz de evaluación oficial de telc Deutsch B2 Beruf:
  - **I. Aufgabenbewältigung:** Cobertura de los 4 *Leitpunkte* y volumen de palabras (mínimo 150).
  - **II. Angemessenheit:** Saludo/despedida formal, registro profesional y adecuación sociolingüística.
  - **III. Korrektheit:** Morfosintaxis (*Nebensätze, Akkusativ/Dativ/Genitiv, Passiv, Konjunktiv II*) y ortografía.
  - **IV. Repertoire:** Vocabulario laboral B2 (*Nomen-Verb-Verbindungen*), conectores variados y cohesión.
- [ ] **2.2** Definir el contrato de salida estructurado en JSON de la IA:
  - `score_total` (puntuación estimada sobre 100 o escala telc).
  - `verdict` (`BESTANDEN` o `NICHT BESTANDEN`).
  - `criteria_breakdown`: Evaluación cualitativa y cuantitativa de los 4 criterios.
  - `critical_errors`: Lista de errores encontrados con extracto del texto original y explicación gramatical en español.
  - `corrected_version`: Texto completo reescrito con estilo profesional B2 nativo impecable.
- [ ] **2.3** Crear script de calibración local en `quiz/test_prompt.py` para probar la respuesta del prompt frente a dos casos de control:
  - Caso A: Texto deficiente de nivel A2/B1 (debe suspender con diagnóstico certero).
  - Caso B: Texto correcto de nivel B2 (debe aprobar y sugerir mejoras de estilo).

---

### Fase 3: Conector Multi-Proveedor de IA en el Frontend
*Permitir llamadas seguras y flexibles al LLM desde la web sin necesidad de montar servidores.*

- [ ] **3.1** Diseñar la arquitectura del cliente API en JavaScript dentro de [`quiz/template.html`](./quiz/template.html):
  - Almacenamiento seguro y privado de credenciales exclusivamente en `localStorage` del navegador.
- [ ] **3.2** Crear el módulo de configuración modal en la barra lateral con selector de proveedores:
  - **Google Gemini API** (endpoint de streaming / generateContent con API Key).
  - **DeepSeek API / OpenAI / OpenRouter** (endpoint `/v1/chat/completions`).
  - **Ollama Local** (`http://localhost:11434/api/chat` para ejecución 100% offline y gratuita).
- [ ] **3.3** Implementar gestor de errores y timeouts (mensajes claros si falta saldo, si la clave es errónea o si el servidor local no responde).

---

### Fase 4: Interfaz de Usuario (Editor, Contador y Resultados)
*Construir el entorno interactivo de examen en la aplicación web.*

- [ ] **4.1** Añadir la navegación de **Schreiben** en la barra lateral:
  - Categorías: *Beschwerden & E-Mails* y *Forumsbeiträge*.
- [ ] **4.2** Diseñar el panel de enunciados:
  - Contexto laboral claro, tarjeta destacada con los 4 *Leitpunkte* y pestaña desplegable de *Redemittel B2 útiles*.
- [ ] **4.3** Diseñar el panel del editor:
  - Área de texto amplia con tipografía optimizada para lectura.
  - **Contador dinámico de palabras:** Indicador en tiempo real con barra de progreso (rojo < 150 palabras, verde ≥ 150 palabras).
  - **Temporizador opcional de examen:** Cuenta atrás de 45 minutos con avisos sonoros/visuales.
  - Botón de acción: «Evaluar con Examinador telc B2» con animación de carga / progreso.
- [ ] **4.4** Diseñar el panel de resultados y diagnóstico:
  - Insignia grande de veredicto (*Bestanden / Nicht bestanden*).
  - Gráfico/tarjetas de puntuación en los 4 ejes.
  - Sección de errores detectados y correcciones gramaticales.
  - Vista comparativa lado a lado o conmutador: *Tu texto* vs *Versión profesional sugerida B2*.
- [ ] **4.5** Implementar persistencia de borradores e historial:
  - Autoguardado del borrador mientras escribes.
  - Registro de intentos pasados con fecha y calificación para seguir la evolución.

---

### Fase 5: Pruebas, Smoke Tests y Validación Final
*Asegurar que el entregable mantenga cero regresiones y funcione con un solo clic.*

- [ ] **5.1** Ejecutar [`quiz/build.py`](./quiz/build.py) para generar el archivo autocontenido final [`quiz/B2_quiz.html`](./quiz/B2_quiz.html).
- [ ] **5.2** Actualizar [`quiz/smoke_test.js`](./quiz/smoke_test.js) para verificar que los nuevos nodos del editor y modal de IA no rompan la app.
- [ ] **5.3** Realizar prueba real de redacción y evaluación con la IA.
- [ ] **5.4** Sincronizar el grafo con `graphify update .` y registrar el avance en git (`main`).
