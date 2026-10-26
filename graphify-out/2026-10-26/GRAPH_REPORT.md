# Graph Report - B2  (2026-10-25)

## Corpus Check
- 87 files · ~2,953,679 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 415 nodes · 563 edges · 34 communities (20 shown, 6 thin omitted)
- Extraction: 92% EXTRACTED · 7% INFERRED · 1% AMBIGUOUS · INFERRED: 42 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5c8e65c0`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- renderSchreiben
- pdf2md.py
- design_audit.js
- smoke_test.js
- Respuesta con cita literal y nivel de confianza
- validate_evaluation_json
- make_sprachbausteine.py
- security_test.js
- Lexer
- make_sprechen_t2.py
- Inline error-annotation correction view (dark mode)
- Handler
- Magnified crop of a single highlighted term inside a dark-mode text panel (no app chrome visible)
- build.py
- inspect_pdf.py
- fix_review.py
- make_full_forums.py
- fix_review2.py
- make_quiz_sources.py
- merge_sprachbausteine_respuestas.py
- pdf2md.py: conversor PDF a Markdown propio
- fix_review3.py
- Mazo de Smalltalk de Sprechen Teil 2 (no se corrige)
- make_index.py
- Modo mesa de examen a partir de 1280 px
- Design

## God Nodes (most connected - your core abstractions)
1. `PDF` - 18 edges
2. `validate_evaluation_json()` - 13 edges
3. `El` - 10 edges
4. `Lexer` - 10 edges
5. `build_user_prompt()` - 9 edges
6. `Design` - 9 edges
7. `renderSchreiben` - 9 edges
8. `Handler` - 8 edges
9. `build_font()` - 8 edges
10. `main()` - 8 edges

## Surprising Connections (you probably didn't know these)
- `Validación mecánica de la evaluación (validate_evaluation_json)` --semantically_similar_to--> `errorValido`  [INFERRED] [semantically similar]
  README.md → quiz/template.html
- `Rúbrica telc B2 Beruf con dos reglas propias más estrictas` --semantically_similar_to--> `Escala de 100 puntos (I=34, II-IV=22)`  [INFERRED] [semantically similar]
  README.md → quiz/README.md
- `Validación mecánica de la evaluación (validate_evaluation_json)` --semantically_similar_to--> `Corrector: contrato contra reescritura, spans anchos y reglas inventadas`  [INFERRED] [semantically similar]
  README.md → quiz/README.md
- `Sistema de tokens :root y [data-theme=claro]` --semantically_similar_to--> `applyTheme`  [INFERRED] [semantically similar]
  uxui/prototipo.html → quiz/template.html
- `Mando deslizante del control segmentado` --semantically_similar_to--> `colocarMandos`  [INFERRED] [semantically similar]
  uxui/prototipo.html → quiz/template.html

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Flujo de evaluación LLM de Schreiben (3 pasadas + caza de errores + puntuación de la app)** — quiz_template_evaluatewithllm, quiz_template_evaluarunapasada, quiz_template_cazarerrores, quiz_template_combinarpasadas, quiz_template_puntuarcriterios, quiz_template_renderevaluationresult [EXTRACTED 1.00]
- **Lenguaje de piezas con dos temas por tokens (mando deslizante e interruptor)** — quiz_readme_dos_temas_tokens, uxui_prototipo_dos_temas, uxui_prototipo_tokens, uxui_prototipo_mando_deslizante, uxui_prototipo_interruptor_tema, quiz_template_colocarmandos, quiz_template_applytheme [INFERRED 0.85]
- **Sincronización de redacciones por perfil en una sala compartida** — resumen_cambios_deepseek_privacidad_separacion, resumen_cambios_deepseek_sincronizacion_firestore, resumen_cambios_deepseek_esquema_documentos, resumen_cambios_deepseek_reglas_seguridad, quiz_template_progkey, quiz_template_pushschreibentofirestore, quiz_template_startlisteningtotask [INFERRED 0.85]

## Communities (34 total, 6 thin omitted)

### Community 0 - "renderSchreiben"
Cohesion: 0.07
Nodes (47): Redirección de enlace corto conservando ?user y ?room, Catálogo de tareas de Schreiben (13 Beschwerde + 98 Forumsbeitrag), Conector multi-proveedor de IA (Gemini, DeepSeek/OpenAI, Ollama), Contrato de salida JSON del evaluador, Editor de Schreiben con contador de palabras y temporizador de 45 min, Módulo de Schreiben con evaluador LLM, System Prompt del examinador telc B2 Beruf, Corrector: contrato contra reescritura, spans anchos y reglas inventadas (+39 more)

### Community 1 - "pdf2md.py"
Cohesion: 0.09
Nodes (23): Diagnostico: distribucion de huecos entre fragmentos de texto. Objetivo: elegir…, build_font(), build_lines(), code_width(), decode_string(), _emit(), extract_runs(), Font (+15 more)

### Community 2 - "design_audit.js"
Cohesion: 0.06
Nodes (33): altRule, baseBg, colorOf(), contrast(), contrastChecks, durUses, failed, findRule() (+25 more)

### Community 3 - "smoke_test.js"
Cohesion: 0.06
Nodes (26): abiertas(), anunciosActuales(), anunciosIniciales, bloques, cabeceras(), checks, clases(), clicables (+18 more)

### Community 4 - "Respuesta con cita literal y nivel de confianza"
Cohesion: 0.06
Nodes (35): Requisitos de accesibilidad (contraste 4.5:1, rejilla 4 px, 28/44 px), Bilingüismo ES/RU vinculante, Entregable: un único HTML autocontenido, Perfiles de Sergio (español) y Diana (ruso), Principios de producto, Propósito: publicar la clave de respuestas que el original no trae, Contrato de datos de quiz/SPEC.md, Dos temas por tokens (oscuro y paper) (+27 more)

### Community 5 - "validate_evaluation_json"
Cohesion: 0.10
Nodes (31): build_user_prompt(), count_words(), _norm_ws(), _only_case_diff(), _only_punct_diff(), Any, prompt_schreiben.py - Definición oficial del System Prompt y Contrato JSON para…, Cuenta palabras igual que la app: secuencias de letras, dígitos, '_' y '-'. (+23 more)

### Community 6 - "make_sprachbausteine.py"
Cohesion: 0.11
Nodes (28): dividir_subvariantes(), es_linea_de_opciones(), es_nota(), es_titular(), etiqueta_extra(), frase_del_hueco(), leer_opciones_t1(), leer_opciones_t2() (+20 more)

### Community 7 - "security_test.js"
Cohesion: 0.11
Nodes (8): bloques, checks, El, fs, html, montar(), registro, script

### Community 8 - "Lexer"
Cohesion: 0.22
Nodes (5): bytes, Keyword, Lexer, PdfString, Operador o palabra clave suelta, p.ej. 'BT' o 'true'.

### Community 9 - "make_sprechen_t2.py"
Cohesion: 0.21
Nodes (13): aplicar_correcciones(), bloque_crudo(), limpiar(), main(), Extrae las 104 tarjetas de Smalltalk (Sprechen Teil 2) del PDF convertido. El…, Devuelve las líneas del bloque de Smalltalk, sin cabecera ni cola., Agrupa por número de tarjeta. Devuelve [(n, [lineas…]), …]., Une las líneas de una tarjeta en un párrafo y quita las costuras. (+5 more)

### Community 10 - "Inline error-annotation correction view (dark mode)"
Cohesion: 0.22
Nodes (11): Inline error-annotation correction view (dark mode), Dark mode theme (dark grey background, serif body text), Two-tier color-coded error taxonomy (blue span = wording/form error, red span = logic/cohesion error), Word-form error: 'Mitarbeite' instead of 'Mitarbeiter' (missing final -r), Clause-link error: 'und diese nicht noch mehr Arbeit ... leisten können' (dangling demonstrative / broken causal connector), Numbered badge markers linking each highlighted span to an error explanation list, Numbered marker [1] on blue-highlighted span 'viele Mitarbeite schon', Numbered marker [2] on red-highlighted span 'und diese nicht noch mehr Arbeit' (+3 more)

### Community 11 - "Handler"
Cohesion: 0.31
Nodes (3): BaseHTTPRequestHandler, Handler, Proxy local para OpenCode Go (el «Worker» de andar por casa). Por qué hace…

### Community 12 - "Magnified crop of a single highlighted term inside a dark-mode text panel (no app chrome visible)"
Cohesion: 0.39
Nodes (9): Crop/truncation state: text cut at both edges, no margins, no header, no controls, no visible error state, Marking treatment: rounded taupe highlight block with a 4 px gold underline rule (x100-413, y302-305), Clipped white text fragment '...nd' at the left edge (tail of the preceding word, most likely 'und'), Trailing hyphen after 'Life-', implying a compound continuation (e.g. '-Balance') that is cut off, Unresolved context: zoom on an inline annotation/marked term in running text vs. chart-label or legend crop (no app shell visible to confirm), Magnified crop of a single highlighted term inside a dark-mode text panel (no app chrome visible), Dark-mode surface palette: near-black blue-grey background #36373F (RGB 54,55,63) with warm highlight fill, Highlighted literal 'World-Life-' set in serif, pale gold (#FFEFA2) on taupe block (#4E4842) (+1 more)

### Community 13 - "build.py"
Cohesion: 0.36
Nodes (7): main(), norm_ws(), Valida los JSON de preguntas y construye el HTML autocontenido. Uso: python…, Validación de las tarjetas de Smalltalk (Sprechen Teil 2)., Normaliza espacios para comparar citas con el texto del que salen., validate(), validate_smalltalk()

### Community 14 - "inspect_pdf.py"
Cohesion: 0.38
Nodes (6): decompress_stream(), find_objects(), main(), Inspecciona la estructura interna del PDF para planear el extractor. Solo…, Extrae objetos de nivel superior por fuerza bruta: 'N G obj ... endobj'., Localiza 'stream...endstream' y descomprime si es FlateDecode.

### Community 16 - "make_full_forums.py"
Cohesion: 0.50
Nodes (4): main(), make_forum(), make_full_forums.py - Generador del catálogo exhaustivo de Forumsbeiträge (telc…, Un tema de Forumsbeitrag. Sin `colleague_post`: la aportación del compañero era…

### Community 18 - "make_quiz_sources.py"
Cohesion: 0.67
Nodes (3): load_pages(), main(), Parte el Markdown convertido en ficheros fuente por bloque de variantes. Uso:…

### Community 19 - "merge_sprachbausteine_respuestas.py"
Cohesion: 0.67
Nodes (3): main(), norm_ws(), merge_sprachbausteine_respuestas.py - Consolida las respuestas deducidas. Los…

### Community 20 - "pdf2md.py: conversor PDF a Markdown propio"
Cohesion: 0.67
Nodes (4): Validador de ancho de avance real (Run.x1), Limitaciones conocidas del conversor, pdf2md.py: conversor PDF a Markdown propio, Umbral de espacio de 0.18 em

### Community 33 - "Design"
Cohesion: 0.20
Nodes (9): Color, Componentes, Design, Estados, Material, Prohibido, Temas, Tipografía (+1 more)

## Ambiguous Edges - Review These
- `Clause-link error: 'und diese nicht noch mehr Arbeit ... leisten können' (dangling demonstrative / broken causal connector)` → `Two-tier color-coded error taxonomy (blue span = wording/form error, red span = logic/cohesion error)`  [AMBIGUOUS]
  02_err2.png · relation: semantically_similar_to
- `Crop/truncation state: text cut at both edges, no margins, no header, no controls, no visible error state` → `Unresolved context: zoom on an inline annotation/marked term in running text vs. chart-label or legend crop (no app shell visible to confirm)`  [AMBIGUOUS]
  10_wlb4x.png · relation: conceptually_related_to
- `Unresolved context: zoom on an inline annotation/marked term in running text vs. chart-label or legend crop (no app shell visible to confirm)` → `Magnified crop of a single highlighted term inside a dark-mode text panel (no app chrome visible)`  [AMBIGUOUS]
  10_wlb4x.png · relation: references
- `Possible typo/variant: term intended as 'Work-Life' (as in 'Work-Life-Balance') rather than 'World-Life'` → `Highlighted literal 'World-Life-' set in serif, pale gold (#FFEFA2) on taupe block (#4E4842)`  [AMBIGUOUS]
  10_wlb4x.png · relation: semantically_similar_to

## Knowledge Gaps
- **79 isolated node(s):** `fs`, `html`, `bloques`, `script`, `todas` (+74 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 191 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `Clause-link error: 'und diese nicht noch mehr Arbeit ... leisten können' (dangling demonstrative / broken causal connector)` and `Two-tier color-coded error taxonomy (blue span = wording/form error, red span = logic/cohesion error)`?**
  _Edge tagged AMBIGUOUS (relation: semantically_similar_to) - confidence is low._
- **What is the exact relationship between `Crop/truncation state: text cut at both edges, no margins, no header, no controls, no visible error state` and `Unresolved context: zoom on an inline annotation/marked term in running text vs. chart-label or legend crop (no app shell visible to confirm)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `Unresolved context: zoom on an inline annotation/marked term in running text vs. chart-label or legend crop (no app shell visible to confirm)` and `Magnified crop of a single highlighted term inside a dark-mode text panel (no app chrome visible)`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._
- **What is the exact relationship between `Possible typo/variant: term intended as 'Work-Life' (as in 'Work-Life-Balance') rather than 'World-Life'` and `Highlighted literal 'World-Life-' set in serif, pale gold (#FFEFA2) on taupe block (#4E4842)`?**
  _Edge tagged AMBIGUOUS (relation: semantically_similar_to) - confidence is low._
- **Why does `buildUserPromptClient` connect `renderSchreiben` to `Respuesta con cita literal y nivel de confianza`?**
  _High betweenness centrality (0.013) - this node is a cross-community bridge._
- **Why does `Evaluador LLM bilingüe: explicaciones en el idioma del alumno` connect `Respuesta con cita literal y nivel de confianza` to `renderSchreiben`?**
  _High betweenness centrality (0.013) - this node is a cross-community bridge._
- **What connects `fs`, `html`, `bloques` to the rest of the system?**
  _79 weakly-connected nodes found - possible documentation gaps or missing edges._