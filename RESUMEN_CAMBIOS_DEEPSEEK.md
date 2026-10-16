# Resumen Técnico de Cambios: Proyecto telc B2 Beruf (Sergio & Diana)

> **Documento preparado para revisión y análisis con DeepSeek / LLM externo.**  
> **Fecha:** Octubre 2026  
> **Rama Git:** `feature/russian-i18n`  
> **Estado:** 100% funcional, probado y verificado (32/32 smoke tests, 4/4 contract tests).

---

## 1. Contexto y Objetivos del Proyecto

La aplicación es un entorno de preparación y simulación del examen oficial **telc Deutsch-Test für den Beruf B2**.
Consta de tres grandes bloques pedagógicos:
1. **Lesen (Lectura):** Partes 1 a 4 y combinadas de lectura/escritura (ejercicios de selección múltiple con control de confianza y modo repaso).
2. **Hören (Audio):** Módulo de audición y preguntas asociadas *(estricta regla: no tocar nada de Hören)*.
3. **Schreiben (Expresión Escrita):** Módulo de redacción laboral profesional (*Beschwerde / Reklamation* y *Forumsbeitrag / Intranet*), con evaluación pedagógica oficial telc B2 mediante LLMs (Google Gemini 3.5 Flash Lite, DeepSeek, OpenAI u Ollama local).

### Requerimiento Específico:
Sergio y su novia Diana están preparando el examen juntos. Diana es rusoparlante nativa y Sergio es hispanohablante.
* **Separación de privacidad:** Las secciones de lectura (*Lesen*), audio (*Hören*) y respuestas a tests deben ser **100% privadas** y persistir localmente en el navegador de cada uno (`localStorage`). Nadie ve los aciertos ni fallos del otro en los tests.
* **Comparación compartida en redacción (*Schreiben*):** Sergio y Diana deben poder ver y comparar únicamente sus redacciones en tiempo real: ver qué ha escrito el otro, cuántas palabras lleva, cuándo actualizó por última vez y, si ya solicitó evaluación a la IA, consultar su veredicto, puntuación oficial y desglose de errores.
* **Soporte bilingüe ruso/español:**
  * Selector de perfil directo arriba en la cabecera: `[ 👤 Sergio | 👤 Диана ]`.
  * Al pulsar **Sergio**: la app se activa para Sergio y se traduce automáticamente al español (`es`).
  * Al pulsar **Диана**: la app se activa para Diana y se traduce automáticamente al ruso (`ru`).
  * Las explicaciones de errores, gramática y áreas de mejora que devuelve la IA al evaluar deben generarse en ruso si la evalúa Diana, o en español si la evalúa Sergio. El texto modelo y la versión corregida siempre deben ser en alemán formal B2.
* **Acceso por enlace directo sin passwords complejos:** Compartiendo un enlace URL (p. ej. alojado en GitHub Pages).
* **Tolerancia offline:** Si no hay internet o no se ha configurado la sincronización en la nube, la app debe funcionar de forma local sin errores ni excepciones.

---

## 2. Arquitectura de las Soluciones Implementadas

### A. Selector de Perfiles y Conmutación Dinámica de Idioma (Frontend)
* **Estado reactivo:**
  * `currentUser`: `"sergio"` o `"diana"`. Inicializado desde parámetros de URL (`?user=diana` / `?user=sergio`) o recuperado de `localStorage.getItem("b2quiz_user")`.
  * `currentLang`: `"es"` o `"ru"`. Vinculado al perfil del usuario (`sergio` $\rightarrow$ `es`, `diana` $\rightarrow$ `ru`), con posibilidad de alternar libremente con los botones de bandera `🇪🇸 ES` y `🇷🇺 RU`.
  * `currentRoomId`: identificador de la sala de sincronización (`sergio-diana` por defecto), configurable desde URL (`?room=...`) o desde el modal de ajustes.
* **Diccionarios i18n (`I18N.es` e `I18N.ru`):**
  * Más de 80 cadenas traducidas con precisión terminológica (ej. *«Порядок слов в предложении»*, *«Спряжение»*, *«Падежи и артикли»*).
  * Función de interpolación limpia `t(key, vars)`.
  * Función `setUser(user)` que actualiza el estado, persiste en `localStorage`, actualiza clases CSS `.active` y cambia el idioma al idioma nativo correspondiente.

### B. Módulo de Schreiben: Pestañas Comparativas en Tiempo Real
* En la vista de redacción [`renderSchreiben()`](file:///c:/Users/sergi/Documents/Code/B2/quiz/template.html), se introdujo una barra de navegación con dos pestañas y un indicador de estado en la nube:
  ```html
  <div class="tab-pills">
    <button class="tab-pill active" id="tab-schreiben-mine">✏ Mi redacción (Sergio/Диана)</button>
    <button class="tab-pill" id="tab-schreiben-partner">👥 Redacción de Diana/Sergio</button>
  </div>
  <div class="cloud-badge" id="cloud-status-indicator">
    <span class="cloud-dot online"></span> Sincronizado en la nube (sergio-diana)
  </div>
  ```
* **Contenedor Propio (`#schreiben-mine-container`):**
  * Editor de texto con `textarea`.
  * Contador dinámico de palabras en tiempo real (<100 rojo, 100–149 amarillo, $\ge$150 verde).
  * Temporizador de 45 minutos con avisos.
  * Botón de evaluación telc B2 y botón de limpiar borrador.
  * Panel de diagnóstico y resultados propios con notas en 4 criterios, errores marcados con popovers interactivos y Musterlösung oficial de 100 puntos.
* **Contenedor de la Pareja (`#schreiben-partner-container`):**
  * Muestra la redacción en vivo del compañero/a en modo lectura limpia.
  * Insignia con el conteo de palabras de la pareja.
  * Timestamp relativo (*«Actualizado hace 3 min.»* / *«Обновлено 3 мин. назад»*).
  * Si la pareja aún no ha empezado: mensaje de espera respetuoso.
  * Si la pareja ya ha evaluado su redacción: banner de veredicto con calificación y botón desplegable para ver la evaluación completa de la pareja.

### C. Sincronización en la Nube (Firebase Firestore)
* **SDKs integrados en `<head>`:**
  * `firebase-app-compat.js` y `firebase-firestore-compat.js` vía CDN oficial de Google.
  * Envoltura con manejo defensivo de errores: si no hay red o no hay credenciales, `fbSyncStatus = "local"` y no emite excepciones de consola ni bloquea la app.
* **Esquema de Documentos en Firestore:**
  * Ruta: `/rooms/{roomId}/schreiben/{taskId}`
  * Campos soportados:
    * `sergio_text`: `string` (0 a 10.000 caracteres).
    * `sergio_words`: `int` (0 a 2.000).
    * `sergio_eval`: `map` (objeto JSON normalizado de la evaluación, máx. 50 claves).
    * `sergio_updated_at`: `timestamp` o `int` (milisegundos epoch).
    * `diana_text`: `string` (0 a 10.000 caracteres).
    * `diana_words`: `int` (0 a 2.000).
    * `diana_eval`: `map` (objeto JSON normalizado de la evaluación, máx. 50 claves).
    * `diana_updated_at`: `timestamp` o `int` (milisegundos epoch).
* **Escritura con Debounce:**
  * Al teclear en el `textarea`, se guarda en el `localStorage` local inmediatamente y se programa un envío diferido (`queueSchreibenSync`, 900 ms) hacia Firestore con merge `{ merge: true }`.
  * Sergio solo escribe en los campos `sergio_*`; Diana solo escribe en los campos `diana_*`.
* **Escuchador en tiempo real (`onSnapshot`):**
  * Al entrar en una tarea de redacción, `startListeningToTask(taskId, callback)` suscribe un listener al documento de la tarea.
  * Cuando llegan cambios remotos, se actualiza exclusivamente el contenedor de la pareja (`renderPartnerSchreibenView`). **El cursor y el foco del usuario que está escribiendo en su propio editor jamás se ven afectados ni interrumpidos**.

### D. Reglas de Seguridad de Producción ([`firestore.rules`](./firestore.rules))
El archivo [`firestore.rules`](./firestore.rules) fue generado siguiendo las mejores prácticas de seguridad de Google Firebase:
1. **Default Deny en la raíz:** `match /{document=**} { allow read, write: if false; }`.
2. **Protección de salas contra scraping:** En `/rooms/{roomId}`, `allow list: if false` para evitar enumerar o raspar nombres de salas activas.
3. **Validación estricta de IDs:** `isValidRoomId` e `isValidTaskId` exigen formato regex `^[a-zA-Z0-9_-]+$` de 1 a 64 caracteres.
4. **Validación de esquema con `hasOnly`:** Solo se permiten los 8 campos reconocidos, bloqueando polución de esquema.
5. **Límites de recursos:** Validación de longitud máxima de cadenas ($\le$ 10.000 caracteres) para neutralizar ataques de denegación de servicio por documentos de 1MB.
6. **Prohibición de borrado:** `allow delete: if false` en tareas y salas para impedir pérdida accidental o malintencionada de borradores.

### E. Evaluador LLM Pedagógico Bilingüe
* En [`quiz/prompt_schreiben.py`](./quiz/prompt_schreiben.py) y en [`quiz/template.html`](./quiz/template.html):
  * Soporte para **Google Gemini 3.5 Flash Lite** (`gemini-3.5-flash-lite`, recomendado por rapidez y bajo coste), Gemini 3.5 Flash, Gemini 3.1 Pro, DeepSeek Chat (`deepseek-chat`), OpenAI (`gpt-4o-mini`, etc.) y Ollama local.
  * Inyección contextual en el prompt del examinador:
    * Si la candidata es Diana (idioma ruso): *«Die Prüfungskandidatin lernt Deutsch und ihre Muttersprache ist RUSSISCH. Alle Erklärungen der Fehler im Feld rule_es, Stärken und Schwächen MÜSSEN AUF RUSSISCH verfasst werden...»*.
    * Si el candidato es Sergio (idioma español): las explicaciones gramaticales y pedagógicas se redactan en español.
    * En ambos casos, el texto de corrección profesional (*Korrektur*) y la redacción modelo (*Musterlösung*) se generan en alemán formal nivel B2.

---

## 3. Resumen de Archivos Afectados

| Archivo | Tipo de Cambio | Descripción |
|---|---|---|
| [`quiz/template.html`](file:///c:/Users/sergi/Documents/Code/B2/quiz/template.html) | Modificado | Inclusión de Firebase CDN, selectores de usuario/idioma en `<header>`, estilos CSS para pestañas comparativas e indicador de nube, módulo de sincronización Firestore, vista comparativa en `renderSchreiben()` y configuración en modal de IA. |
| [`quiz/B2_quiz.html`](file:///c:/Users/sergi/Documents/Code/B2/quiz/B2_quiz.html) | Reconstruido | Compilado autocontenido final de 673 KB que integra datos JSON, motor y plantilla unificada para uso en navegador o GitHub Pages. |
| [`quiz/smoke_test.js`](file:///c:/Users/sergi/Documents/Code/B2/quiz/smoke_test.js) | Modificado | Suite de pruebas de humo ampliada a 32 comprobaciones automáticas con DOM simulado (perfiles, idioma nativo, sincronización y pestañas). |
| [`firestore.rules`](file:///c:/Users/sergi/Documents/Code/B2/firestore.rules) | Creado | Reglas de seguridad de producción para Cloud Firestore con validación de tipos, rangos, longitudes y permisos. |
| [`quiz/prompt_schreiben.py`](file:///c:/Users/sergi/Documents/Code/B2/quiz/prompt_schreiben.py) | Modificado | Soporte de generación de prompts bilingües alemán-español y alemán-ruso con esquema JSON estructurado. |
| [`quiz/test_prompt.py`](file:///c:/Users/sergi/Documents/Code/B2/quiz/test_prompt.py) | Modificado | Tests unitarios offline para validar prompts y contratos pedagógicos telc B2 (4/4 tests). |

---

## 4. Resultados de las Pruebas Automatizadas

### A. Smoke Test del Visor (`node quiz/smoke_test.js quiz/B2_quiz.html`):
```text
  OK   sin excepciones al ejecutar
  OK   la barra lateral se rellenó  → nodos: 147
  OK   el panel principal se rellenó  → nodos: 10
  OK   las estadísticas se calcularon  → 0/226 respondidas · 0 correctas · 36 dudosas
  OK   el enunciado de Lesen se pintó
  OK   los anuncios se pintaron
  OK   las opciones de respuesta se pintaron
  OK   hay opciones pulsables en el panel  → pulsables dentro de main: 42
  OK   el clic repinta la vista  → antes 3886 chars, después 4527
  OK   aparece la corrección  → insignia de confianza presente
  OK   la respuesta se guardó  → b2quiz.v1
  OK   sección de Schreiben presente en el menú
  OK   el panel de Schreiben se pintó
  OK   el editor y botón de evaluación están presentes
  OK   el modal de IA se abrió y muestra proveedores
  OK   los resultados de evaluación se pintan correctamente  → insignia BESTANDEN presente
  OK   el texto del alumno anotado con errores está presente
  OK   la regla gramatical y corrección interactiva se muestran
  OK   el cambio a ruso se ejecuta correctamente  → idioma actual: ru
  OK   las estadísticas cambian a ruso
  OK   el panel de Schreiben y evaluación se actualizan a ruso
  OK   el veredicto de evaluación muestra сдано en ruso
  OK   la leyenda de tipos de error se muestra en ruso
  OK   el modal de IA se muestra completamente en ruso
  OK   el cambio de vuelta a español funciona  → idioma actual: es
  OK   los botones de perfil Sergio y Diana existen
  OK   al seleccionar Diana el perfil pasa a diana  → usuario: diana
  OK   al seleccionar Diana el idioma cambia automáticamente a ruso  → idioma: ru
  OK   al seleccionar Sergio el perfil pasa a sergio  → usuario: sergio
  OK   al seleccionar Sergio el idioma cambia automáticamente a español  → idioma: es
  OK   las pestañas de mi redacción y redacción de la pareja existen
  OK   el indicador de estado en la nube está presente

32/32 comprobaciones superadas
```

### B. Tests del Evaluador LLM (`python quiz/test_prompt.py`):
```text
=== TEST OFFLINE: EVALUADOR TELC B2 SCHREIBEN ===
[1/4] Verificando generación del prompt (ES y RU)... OK
[2/4] Validando contrato de evaluación para Caso A (A2 deficiente)... OK: NICHT BESTANDEN (38/100)
[3/4] Validando contrato de evaluación para Caso B (B2 sólido)... OK: BESTANDEN (92/100)
[4/4] Verificando robustez del validador de contratos frente a JSON corrupto... OK: 16 anomalías detectadas.
Todos los tests offline del evaluador telc B2 pasaron con éxito (4/4).
```

---

## 5. Instrucciones de Uso y Despliegue

### Probar en Local
1. Iniciar servidor local:
   ```bash
   python -m http.server 8080
   ```
2. Acceder como Sergio: `http://localhost:8080/quiz/B2_quiz.html?user=sergio`
3. Acceder como Diana (en ventana privada o incógnito): `http://localhost:8080/quiz/B2_quiz.html?user=diana`

### Despliegue en GitHub Pages
1. Alojar el repositorio en GitHub en la rama `feature/russian-i18n` (o fusionar en `main`).
2. Configurar **Settings** > **Pages** para servir desde la rama y carpeta correspondiente.
3. Diana puede acceder con su enlace directo: `https://<usuario>.github.io/<repo>/?user=diana`.

### Conexión a Firebase Firestore (Opcional, para sincronizar entre dispositivos)
1. Crear proyecto gratis en [console.firebase.google.com](https://console.firebase.google.com).
2. Crear base de datos Firestore y pegar el contenido de [`firestore.rules`](./firestore.rules) en la pestaña **Rules**.
3. Registrar app web y copiar el objeto `firebaseConfig`.
4. En la web del test, pulsar `⚙ Configurar IA`, bajar a **Sincronización en la Nube** y pegar la configuración.
