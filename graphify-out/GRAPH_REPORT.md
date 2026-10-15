# Graph Report - B2  (2026-10-15)

## Corpus Check
- 159 files · ~350,731 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1543 nodes · 3076 edges · 150 communities (96 shown, 13 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 62 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c6c07c8e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- handleGo
- modern-screenshot.umd.js
- el
- initPageChat
- pdf2md.py
- live-browser.js
- initGlobalBar
- renderDesignVisual
- What You Must Do When Invoked
- handleManualEditActivity
- mountSvelteComponentVariant
- smoke_test.js
- resumeSession
- handleKeyDown
- resolveLiveInjectionAnchor
- injectSvelteComponentsFromManifest
- createLiveBrowserSessionState
- actOnAgentTarget
- captureElementToBlob
- createLiveBrowserDomHelpers
- refreshParamsPanel
- connectSSE
- scheduleAcceptCleanup
- adapt.md
- syncEditBadgeHitProxies
- hideBar
- build.py
- live-browser-ignores.js
- inspect_pdf.py
- impeccable
- new-work.md
- onboard.md
- impeccable/SKILL.md
- fix_review.py
- fix_review2.py
- make_quiz_sources.py
- fix_review3.py
- make_index.py
- The Toolkit
- animate.md
- live.md
- Handle `generate`
- setLiveState
- Generate Report
- New visual work
- optimize.md
- Responsive Design
- Impeccable Asset Producer
- Scan mode (approach C: auto-extract, then confirm descriptive language)
- handleMouseMove
- critique.md
- Simplify the Design
- Hardening Dimensions
- Pipeline PDF → Markdown (sin dependencias)
- Desarrollo Guiado por Pruebas
- clarify.md
- Nielsen's 10 Heuristics
- Generate Combined Critique Report
- document.md
- polish.md
- quieter.md
- showAnnotOverlay
- Revisión de Código y Calidad
- Desglose Detallado de Tareas
- Depuración y Recuperación de Errores
- 1. Principios Fundamentales de Redacción
- Init flow
- showBar
- Planificación y Descomposición de Tareas
- Test B2 Beruf — Lesen y Hören
- 2. Las 5 Lentes de Auditoría (En este orden estricto)
- graphify reference: extra exports and benchmark
- Common Cognitive Load Violations
- iOS platform
- Operate mode depth (and Read notes)
- Shape
- Android platform
- colorize.md
- Persona-Based Design Testing
- doctor.md
- Extract Flow
- Ponytail: El Senior Developer Perezoso y Pragmático
- Entrevístame: Extraer la Intención Real
- Generate Report
- Cognitive Load Assessment
- Impeccable Finish Reviewer
- Impeccable Manual Edit Applier
- Regla: Comunicación Clara y Explicación de Tecnicismos
- graphify reference: query, path, explain
- Diagnostic Scan
- $impeccable hooks
- Visualize: Direction Comps & Asset Production
- Impeccable Documenter
- Region map
- graphify reference: add a URL and watch a folder
- graphify reference: commit hook and native CLAUDE.md integration
- graphify reference: incremental update and cluster-only
- Heuristics Scoring Guide
- Operate
- Read
- graphify reference: GitHub clone and cross-repo merge
- graphify reference: transcribe video and audio
- rules/graphify.md
- extraction-spec.md
- apple-design.md
- ets.md
- workflows/graphify.md
- ponytail.md
- h4_b.md

## God Nodes (most connected - your core abstractions)
1. `connectSSE()` - 34 edges
2. `setLiveState()` - 33 edges
3. `resumeSession()` - 33 edges
4. `showToast()` - 31 edges
5. `initGlobalBar()` - 30 edges
6. `el()` - 29 edges
7. `handleKeyDown()` - 27 edges
8. `cleanup()` - 27 edges
9. `buildInsertConfigureRow()` - 26 edges
10. `injectSvelteComponentsFromManifest()` - 26 edges

## Surprising Connections (you probably didn't know these)
- `enableInlineEdit()` --indirect_call--> `own()`  [INFERRED]
  .agents/skills/impeccable/scripts/live-browser.js → .agents/skills/impeccable/scripts/live-browser-dom.js
- `layoutFlowChildren()` --indirect_call--> `pickable()`  [INFERRED]
  .agents/skills/impeccable/scripts/live-browser.js → .agents/skills/impeccable/scripts/live-browser-dom.js

## Import Cycles
- None detected.

## Communities (150 total, 13 thin omitted)

### Community 0 - "handleGo"
Cohesion: 0.15
Nodes (20): applyEditing(), buildInsertPlaceholderSnapshotFromDom(), buildLocatorForLeaf(), buildPickedAnchorSnapshot(), captureAndEmit(), clearAnnotations(), copyEditContainerContext(), copyEditLeafContext() (+12 more)

### Community 1 - "modern-screenshot.umd.js"
Cohesion: 0.09
Nodes (55): ae(), be(), bt(), Ce(), s(), Ct(), de(), dt() (+47 more)

### Community 2 - "el"
Cohesion: 0.11
Nodes (37): bindConfigureCountPillTooltip(), bindConfigureInlineControlHover(), bindConfigureModifierPillHover(), buildConfigureActionControl(), buildConfigureCountControl(), buildConfigureRow(), buildConfigureSubmitButton(), buildConfigureTrailingCluster() (+29 more)

### Community 3 - "initPageChat"
Cohesion: 0.07
Nodes (57): agentHasWorkInFlight(), armPageChatForTyping(), attachSteerFocusDebug(), attachSteerFocusGuard(), buildSteerProcessingDots(), buildSteerQueueHint(), clearSteerAwaitTimer(), clearSteerFocusRecoverTimer() (+49 more)

### Community 4 - "pdf2md.py"
Cohesion: 0.08
Nodes (27): bytes, Diagnostico: distribucion de huecos entre fragmentos de texto. Objetivo: elegir…, build_font(), build_lines(), code_width(), decode_string(), _emit(), extract_runs() (+19 more)

### Community 5 - "live-browser.js"
Cohesion: 0.05
Nodes (62): applyGlobalBarLabelState(), applyLiveBarPreference(), applyPlaceholderSizingStyles(), buildSavingRow(), buildSvelteExpressionTextMap(), buildSveltePropValuesFromLiveElement(), buildSveltePropValuesV2(), cloneWithoutElements() (+54 more)

### Community 6 - "initGlobalBar"
Cohesion: 0.16
Nodes (23): agentStatusText(), barPaletteForTheme(), brandMarkSvg(), detectPageTheme(), ensureAgentPollTooltip(), hideAgentPollTooltip(), init(), initActionPicker() (+15 more)

### Community 7 - "renderDesignVisual"
Cohesion: 0.07
Nodes (43): buildCollapsible(), buildColorModels(), buildDesignHeader(), buildListHtml(), buildRadiiModels(), buildTypographyModels(), copyToClipboard(), cssSafe() (+35 more)

### Community 8 - "What You Must Do When Invoked"
Cohesion: 0.07
Nodes (26): For /graphify add and --watch, For /graphify query, For the commit hook and native CLAUDE.md integration, For --update and --cluster-only, /graphify, Honesty Rules, Interpreter guard for subcommands, Part A - Structural extraction for code files (+18 more)

### Community 9 - "handleManualEditActivity"
Cohesion: 0.09
Nodes (43): addManualContextText(), canRestoreManualEditElement(), clearStoredManualApplyState(), collectManualContextPieces(), walk(), contextElementForManualEdit(), directMixedTextRestoreNodes(), fetchPendingCount() (+35 more)

### Community 10 - "mountSvelteComponentVariant"
Cohesion: 0.17
Nodes (17): applyOriginalAttrsToSvelteAnchor(), commitAcceptedSvelteComponentToDom(), componentModuleCandidates(), describeMountFailure(), detectDevServerBase(), findInsertAnchorInDom(), findLiveElementForSvelteManifest(), getMountedSvelteComponentAnchor() (+9 more)

### Community 11 - "smoke_test.js"
Cohesion: 0.10
Nodes (13): checks, clicables, document, El, errors, fs, html, ids (+5 more)

### Community 12 - "resumeSession"
Cohesion: 0.17
Nodes (21): applySavedSessionMeta(), checkpointPayload(), clampVariantIndex(), clearHandled(), enterRecoveryWaitingForAnchor(), findActiveSessionSummary(), findAdoptableServerSession(), isSessionHandled() (+13 more)

### Community 13 - "handleKeyDown"
Cohesion: 0.25
Nodes (18): beginNewLiveConfiguration(), cancelInsertConfigure(), clearInsertPicking(), exitConfigureToPicking(), handleClick(), handleKeyDown(), hasTextRows(), hideActionPicker() (+10 more)

### Community 14 - "resolveLiveInjectionAnchor"
Cohesion: 0.62
Nodes (7): elementMatchesOriginalMarkup(), findLiveElementForOriginalMarkup(), findLiveElementFromAnchorSnapshot(), isUsableInjectionAnchor(), normalizeElementClassName(), parseOriginalMarkupElement(), resolveLiveInjectionAnchor()

### Community 15 - "injectSvelteComponentsFromManifest"
Cohesion: 0.13
Nodes (34): abortSvelteComponentInjection(), applyPlaceholderDimensions(), commitAcceptedVariantToDom(), completeParameterGenerationIfReady(), completeParameterPublication(), completeSourceInjection(), ensureInsertPlaceholder(), finalizeInsertSession() (+26 more)

### Community 16 - "createLiveBrowserSessionState"
Cohesion: 0.22
Nodes (15): createLiveBrowserSessionState(), clearHandled(), clearScrollY(), clearSession(), isHandled(), loadSession(), markHandled(), nextCheckpointRevision() (+7 more)

### Community 17 - "actOnAgentTarget"
Cohesion: 0.26
Nodes (18): actOnAgentTarget(), agentTargetBusyReason(), agentTargetOverlayGone(), agentTargetTaken(), claimAgentTarget(), claimAndActOnAgentTarget(), declineAgentTargetBusy(), declineAgentTargetUnresolvable() (+10 more)

### Community 18 - "captureElementToBlob"
Cohesion: 0.08
Nodes (36): averageRgb01(), beginEditPin(), bufferToBase64(), buildAnnotationsForCapture(), buildPinElement(), cancelEditingPin(), captureChromeNodes(), captureElementFromRenderedAncestor() (+28 more)

### Community 19 - "createLiveBrowserDomHelpers"
Cohesion: 0.12
Nodes (16): collectEditableTextRows(), visit(), createLiveBrowserDomHelpers(), cssId(), liveUiRoot(), makeFrozenAnchor(), own(), pickable() (+8 more)

### Community 20 - "refreshParamsPanel"
Cohesion: 0.16
Nodes (20): applyParamDefaults(), applyParamValue(), buildParamsPanel(), closedClipPath(), closeTunePopover(), formatRangeValue(), getVisibleVariantEl(), hideParamsPanel() (+12 more)

### Community 21 - "connectSSE"
Cohesion: 0.14
Nodes (24): abandonForeignSession(), abandonSupersededGo(), connectSSE(), discardOrphanedSession(), handleDiscard(), injectVariantsFromSource(), isFrameworkComponentPreviewMode(), isJsxSourceFile() (+16 more)

### Community 22 - "scheduleAcceptCleanup"
Cohesion: 0.31
Nodes (11): acceptedDomAlreadyClean(), clearHandledWrapperReloadStamp(), deferredRecoverySuperseded(), ensureAcceptedDomClean(), findAcceptedRuntimeWrappers(), handledWrapperReloadKey(), reloadAfterMissingAcceptedDom(), restoreAcceptedDomFromSnapshot() (+3 more)

### Community 23 - "adapt.md"
Cohesion: 0.08
Nodes (22): Assess Adaptation Challenge, Content Adaptation, Desktop Adaptation (Mobile → Desktop), Email Adaptation (Web → Email), Implement Adaptations, Layout Adaptation Techniques, Mobile Adaptation (Desktop → Mobile), Adaptation Strategies (+14 more)

### Community 24 - "syncEditBadgeHitProxies"
Cohesion: 0.27
Nodes (10): bindEditBadgeProxy(), editBadgeProxyTargets(), initEditBadge(), initEditBadgeHitProxies(), positionEditBadge(), proxyMouseEvent(), setImportantStyle(), styleEditBadgeProxy() (+2 more)

### Community 25 - "hideBar"
Cohesion: 0.36
Nodes (12): cancelEditing(), cancelEditingToPicking(), disableInlineEdit(), enterEditingMode(), handleServerLost(), hideAnnotOverlay(), hideBar(), hideConfigureBarTooltip() (+4 more)

### Community 26 - "build.py"
Cohesion: 0.47
Nodes (5): main(), norm_ws(), Valida los JSON de preguntas y construye el HTML autocontenido. Uso: python…, Normaliza espacios para comparar citas con el texto del que salen., validate()

### Community 27 - "live-browser-ignores.js"
Cohesion: 0.52
Nodes (6): globToRegex(), matchesScope(), normalizeIgnoreRule(), normalizeIgnoreValue(), pageCandidates(), resolveDetectIgnores()

### Community 28 - "inspect_pdf.py"
Cohesion: 0.38
Nodes (6): decompress_stream(), find_objects(), main(), Inspecciona la estructura interna del PDF para planear el extractor. Solo…, Extrae objetos de nivel superior por fuerza bruta: 'N G obj ... endobj'., Localiza 'stream...endstream' y descomprime si es FlateDecode.

### Community 29 - "impeccable"
Cohesion: 0.60
Nodes (5): impeccable script, check_download(), fetch_url(), probe_ok(), setup_help()

### Community 30 - "new-work.md"
Cohesion: 0.10
Nodes (17): Recommended Actions, Craft (deprecated alias), Apply, Live-mode signature params, Set the spatial thesis, Two isolated assessments, Verify, Visitor mode (+9 more)

### Community 31 - "onboard.md"
Cohesion: 0.09
Nodes (22): Assess Onboarding Needs, Context Over Ceremony, Contextual Help, Design Onboarding Experiences, Documentation & Help, Empty State Design, Feature Discovery & Adoption, Guided Tours & Walkthroughs (+14 more)

### Community 32 - "impeccable/SKILL.md"
Cohesion: 0.10
Nodes (15): Before you finish, Scope is sovereign, The amplification, The skeleton test, Why it reads flat, Craft floor, Refuse, Verify (+7 more)

### Community 35 - "make_quiz_sources.py"
Cohesion: 0.67
Nodes (3): load_pages(), main(), Parte el Markdown convertido en ficheros fuente por bloque de variantes. Uso:…

### Community 38 - "The Toolkit"
Cohesion: 0.10
Nodes (20): Animate complex properties, Assess What "Extraordinary" Means Here, For data-heavy interfaces, For functional UI, For performance-critical UI, For visual/marketing surfaces, Implement with Discipline, Interact with the device (+12 more)

### Community 39 - "animate.md"
Cohesion: 0.12
Nodes (14): Accessibility and control, Choose material by meaning, Find the job, Implement to the runtime, Set the motion thesis, Timing and easing, Verify, Visitor mode (+6 more)

### Community 40 - "live.md"
Cohesion: 0.07
Nodes (26): Step 1: Parse the request, Step 2: Reuse the page, then start, Step 3: Generate, Step 4: Accept and close, Cleanup, Exit, First-time setup, Handle `accept` (+18 more)

### Community 41 - "Handle `generate`"
Cohesion: 0.12
Nodes (16): 1. Read the screenshot (if present), 2. Wrap the element, 3. Load the action's reference, 4. Plan three variants: identity first, then mode, then axes, 5. Apply the freeform prompt (if present), 6. Deliver variants, 7. Parameters (composition-sized, 0-4 per variant), 8. Signal done (+8 more)

### Community 42 - "setLiveState"
Cohesion: 0.16
Nodes (23): cleanup(), cleanupAcceptedSession(), clearMountErrorCard(), clearScrollY(), clearSession(), discardedWrappers(), discardStateStyleId(), mountErrorCardBottomOffset() (+15 more)

### Community 43 - "Generate Report"
Cohesion: 0.13
Nodes (14): 1. Accessibility (A11y), 2. Performance, 3. Theming, 4. Responsive Design, 5. Implementation Integrity (CRITICAL), Audit Health Score, Detailed Findings by Severity, Diagnostic Scan (+6 more)

### Community 44 - "New visual work"
Cohesion: 0.14
Nodes (14): 1. Decide what is already true, 2. Ask what will change the work, 3. Choose the right amount of invention, 4. Commit the world, 5. Record the decision, 6. Build with full commitment, 7. Inspect and finish, Both paths (+6 more)

### Community 45 - "optimize.md"
Cohesion: 0.14
Nodes (13): Animation Performance, Assess Performance Issues, Core Web Vitals Optimization, Cumulative Layout Shift (CLS < 0.1), Interaction to Next Paint (INP < 200ms), Largest Contentful Paint (LCP < 2.5s), Loading Performance, Network Optimization (+5 more)

### Community 46 - "Responsive Design"
Cohesion: 0.20
Nodes (10): Breakpoints: Content-Driven, Detect Input Method, Not Just Screen Size, Layout Adaptation Patterns, Mobile-First: Write It Right, Picture Element for Art Direction, Responsive Design, Responsive Images: Get It Right, Safe Areas: Handle the Notch (+2 more)

### Community 47 - "Impeccable Asset Producer"
Cohesion: 0.15
Nodes (11): Act on the receipt, Assemble and review, Plan and asset review, Plan, capture, serve, Core Rule, Decision Comps, Impeccable Asset Producer, Input Contract (+3 more)

### Community 48 - "Scan mode (approach C: auto-extract, then confirm descriptive language)"
Cohesion: 0.15
Nodes (13): Component translation rules, Narrative mapping, Scan mode (approach C: auto-extract, then confirm descriptive language), Schema, Step 1: Find the design assets, Step 2: Auto-extract what can be auto-extracted, Step 2b: Stage the frontmatter, Step 3: Ask the user for qualitative language (+5 more)

### Community 49 - "handleMouseMove"
Cohesion: 0.29
Nodes (7): cursorForInsertAxis(), handleMouseMove(), hideHighlightTagTooltip(), setPageInteractionCursor(), shouldShowHighlightTagTooltip(), showHighlight(), syncPageInteractionCursor()

### Community 50 - "critique.md"
Cohesion: 0.17
Nodes (11): Action Summary, Ask the User, Assessment A: Design Review, Assessment B: Detector + Browser Evidence, Assessment Orchestration, Deliver the Report, Hard Invariants, Persist the Snapshot (+3 more)

### Community 51 - "Simplify the Design"
Cohesion: 0.17
Nodes (11): Assess Current State, Code Simplification, Content Simplification, Document Removed Complexity, Information Architecture, Interaction Simplification, Layout Simplification, Plan Simplification (+3 more)

### Community 52 - "Hardening Dimensions"
Cohesion: 0.17
Nodes (11): Accessibility Resilience, Assess Hardening Needs, Edge Cases & Boundary Conditions, Error Handling, Hardening Dimensions, Input Validation & Sanitization, Internationalization (i18n), Performance Resilience (+3 more)

### Community 53 - "Pipeline PDF → Markdown (sin dependencias)"
Cohesion: 0.17
Nodes (11): `analyze_gaps.py` — calibración del umbral de espacio, `inspect_pdf.py` — diagnóstico previo, Limitaciones conocidas, `make_index.py` — índice navegable, `pdf2md.py` — el conversor, Pipeline PDF → Markdown (sin dependencias), Por qué no se usó MarkItDown, Resultado (+3 more)

### Community 54 - "Desarrollo Guiado por Pruebas"
Cohesion: 0.18
Nodes (10): 1. Cuándo Usar, 2. Estado Actual de Este Proyecto (léelo antes de empezar), 3. El Ciclo, 4. El Patrón "Demuéstralo" (para bugs), 5. La Pirámide, 6. Cómo Escribir Buenas Pruebas, 7. Tabla Anti-Racionalización, 8. Banderas Rojas (+2 more)

### Community 55 - "clarify.md"
Cohesion: 0.18
Nodes (10): Actions and navigation, Audit the language, Errors and permissions, Forms, Help and instructional text, Loading, empty, and success states, Rewrite by function, Set the message hierarchy (+2 more)

### Community 56 - "Nielsen's 10 Heuristics"
Cohesion: 0.18
Nodes (11): 10. Help and Documentation, 1. Visibility of System Status, 2. Match Between System and Real World, 3. User Control and Freedom, 4. Consistency and Standards, 5. Error Prevention, 6. Recognition Rather Than Recall, 7. Flexibility and Efficiency of Use (+3 more)

### Community 57 - "Generate Combined Critique Report"
Cohesion: 0.18
Nodes (11): Design Health Score, Design Specificity Verdict, Generate Combined Critique Report, Minor Observations, Overall Impression, Persona Red Flags, Priority Issues, Questions to Consider (+3 more)

### Community 58 - "document.md"
Cohesion: 0.18
Nodes (10): Pitfalls, Seed mode, Step 1: Route through new-work's workshop, Step 2: Write seed DESIGN.md, Step 3: Confirm, Style guidelines, The frontmatter: token schema, The markdown body: eight sections (canonical order) (+2 more)

### Community 59 - "polish.md"
Cohesion: 0.18
Nodes (10): 1. Establish the system, 2. Gather the evidence, 3. Triage, 4. Polish the whole path, 5. Verify and finish, Color, imagery, and icons, Content and code, Flow and hierarchy (+2 more)

### Community 60 - "quieter.md"
Cohesion: 0.18
Nodes (10): Assess Current State, Color Refinement, Composition Refinement, Motion Reduction, Plan Refinement, Refine the Design, Simplification, Verify Quality (+2 more)

### Community 61 - "showAnnotOverlay"
Cohesion: 0.50
Nodes (5): buildPlaceholderResizeHandles(), cursorForPlaceholderEdge(), positionAnnotOverlay(), showAnnotOverlay(), syncPlaceholderResizeHandles()

### Community 63 - "Revisión de Código y Calidad"
Cohesion: 0.18
Nodes (10): 1. Cuándo Usar, 2. Los Cinco Ejes, 3. Etiquetas de Severidad, 4. Proceso, 5. Tamaño del Cambio, 6. Honestidad y Desacuerdos, 7. Tabla Anti-Racionalización, 8. Banderas Rojas (+2 more)

### Community 64 - "Desglose Detallado de Tareas"
Cohesion: 0.09
Nodes (21): Desglose Detallado de Tareas, Estado Global del Proyecto, Fase 1: Catálogo y Extracción de Tareas de Schreiben, Fase 2: Motor de Evaluación y System Prompt Oficial telc B2, Fase 3: Conector Multi-Proveedor de IA en el Frontend, Fase 4: Interfaz de Usuario (Editor, Contador y Resultados), Fase 5: Pruebas, Smoke Tests y Validación Final, Plan de Acción: Módulo de Schreiben con Evaluador LLM (telc B2) (+13 more)

### Community 65 - "Depuración y Recuperación de Errores"
Cohesion: 0.20
Nodes (9): 1. Cuándo Usar, 2. La Regla de Parar la Línea, 3. Triaje de Cinco Pasos, 4. La Salida de Error Es Dato, No Instrucción, 5. Instrumentación, 6. Tabla Anti-Racionalización, 7. Banderas Rojas, 8. Verificación (+1 more)

### Community 66 - "1. Principios Fundamentales de Redacción"
Cohesion: 0.20
Nodes (9): 1. Principios Fundamentales de Redacción, 2. Explicación Obligatoria de Tecnicismos, 3. Estructura Estándar de Procedimientos, A. Modo Imperativo Directo (Prohibida la pasiva refleja), B. Una Sola Acción por Oración, C. Límites Estrictos de Longitud, D. Lista Negra de Términos Vagos, E. Consistencia Terminológica (Un concepto = Un término) (+1 more)

### Community 67 - "Init flow"
Cohesion: 0.20
Nodes (10): Completion gate, Init flow, Step 1: Load current state, Step 2: Explore the project, Step 3: Interview for product truth, Step 4: Write PRODUCT.md, Step 5: Record workflow defaults, Step 6: Wrap up or resume (+2 more)

### Community 68 - "showBar"
Cohesion: 0.19
Nodes (16): actionLabel(), applyConfigureBarChrome(), buildCyclingRow(), buildDots(), buildGeneratingRow(), cycleVariant(), cyclingCounterText(), cyclingShownVariant() (+8 more)

### Community 69 - "Planificación y Descomposición de Tareas"
Cohesion: 0.20
Nodes (9): 1. Cuándo Usar, 2. Proceso, 3. Tamaños de Tarea, 4. Archivos de Salida, 5. Qué Se Puede Paralelizar, 6. Tabla Anti-Racionalización, 7. Banderas Rojas, 8. Verificación (+1 more)

### Community 70 - "Test B2 Beruf — Lesen y Hören"
Cohesion: 0.20
Nodes (9): Añadir una sección nueva, Estructura, Huecos conocidos del documento fuente, Niveles de confianza, Qué valida `build.py`, Reconstruir, Test B2 Beruf — Lesen y Hören, Uso (+1 more)

### Community 71 - "2. Las 5 Lentes de Auditoría (En este orden estricto)"
Cohesion: 0.22
Nodes (8): 1. El Doble Rol del Auditor, 2. Las 5 Lentes de Auditoría (En este orden estricto), Apple Design Skill: HIG & Craftsmanship Reviewer, Lente 1: Accesibilidad y Ergonomía Táctil (Crítico), Lente 2: Jerarquía, Espaciado y Ritmo (Grid de 8pt), Lente 3: Materiales y Acabados (Liquid & Frosted Glass), Lente 4: Dinamismo, Físicas y Micro-interacciones (Vida), Lente 5: Identidad y Anti-Plantilla (Des-IAficar)

### Community 72 - "graphify reference: extra exports and benchmark"
Cohesion: 0.22
Nodes (8): graphify reference: extra exports and benchmark, Step 6b - Wiki (only if --wiki flag), Step 7 - Neo4j export (only if --neo4j or --neo4j-push flag), Step 7a - FalkorDB export (only if --falkordb or --falkordb-push flag), Step 7b - SVG export (only if --svg flag), Step 7c - GraphML export (only if --graphml flag), Step 7d - MCP server (only if --mcp flag), Step 8 - Token reduction benchmark (only if total_words > 5000)

### Community 73 - "Common Cognitive Load Violations"
Cohesion: 0.22
Nodes (9): 1. The Wall of Options, 2. The Memory Bridge, 3. The Hidden Navigation, 4. The Jargon Barrier, 5. The Visual Noise Floor, 6. The Inconsistent Pattern, 7. The Multi-Task Demand, 8. The Context Switch (+1 more)

### Community 74 - "iOS platform"
Cohesion: 0.22
Nodes (9): Color & materials, Components & controls, iOS platform, Layout & structure, Motion, The iOS slop test, Touch targets, Typography (+1 more)

### Community 75 - "Operate mode depth (and Read notes)"
Cohesion: 0.22
Nodes (9): Color, Components, Layout, Motion, Operate mode depth (and Read notes), Product constraints, Product permissions, The product slop test (+1 more)

### Community 76 - "Shape"
Cohesion: 0.22
Nodes (8): Cadence, Confirm and stop, Phase 1: Discovery interview, Phase 2: Resolve the design direction, Phase 3: Write the brief, Round 1: purpose, people, and outcome, Round 2: material, behavior, and boundaries, Shape

### Community 78 - "Android platform"
Cohesion: 0.25
Nodes (8): Android platform, Color & theming, Components & motion, Layout & structure, The Android slop test, Touch targets, Typography, Verifying the build

### Community 79 - "colorize.md"
Cohesion: 0.25
Nodes (7): Apply at system scale, Audit before choosing, Choose a strategy, Contrast and perception, Live-mode signature params, Verify, Visitor mode

### Community 80 - "Persona-Based Design Testing"
Cohesion: 0.25
Nodes (8): 1. Impatient Power User: "Alex", 2. Confused First-Timer: "Jordan", 3. Accessibility-Dependent User: "Sam", 4. Deliberate Stress Tester: "Riley", 5. Distracted Mobile User: "Casey", Persona-Based Design Testing, Project-Specific Personas, Selecting Personas

### Community 81 - "doctor.md"
Cohesion: 0.25
Nodes (7): Monorepo notes, Opting out of the boot check, Step 1: Run the pass, Step 2: Act by severity, Step 3: Deprecated fields are binding, Step 4: Do not overclaim on truth drift, What this owns, and what it does not

### Community 82 - "Extract Flow"
Cohesion: 0.25
Nodes (7): Extract Flow, Step 1: Discover the Design System, Step 2: Identify Patterns, Step 3: Plan Extraction, Step 4: Extract & Enrich, Step 5: Migrate, Step 6: Document

### Community 83 - "Ponytail: El Senior Developer Perezoso y Pragmático"
Cohesion: 0.25
Nodes (7): 1. Persistencia y Modos, 2. La Escalera de Decisión (The Ladder), 3. Resolución de Bugs: Causa Raíz, No Síntomas, 4. Reglas de Oro, 5. Niveles de Intensidad, 6. Cuándo NO ser "Perezoso" (Límites Críticos), Ponytail: El Senior Developer Perezoso y Pragmático

### Community 84 - "Entrevístame: Extraer la Intención Real"
Cohesion: 0.29
Nodes (6): 1. Cuándo Usar, 2. Proceso, 3. Tabla Anti-Racionalización, 4. Banderas Rojas, 5. Verificación, Entrevístame: Extraer la Intención Real

### Community 85 - "Generate Report"
Cohesion: 0.29
Nodes (7): Audit Health Score, Detailed Findings by Severity, Executive Summary, Generate Report, Patterns & Systemic Issues, Platform Conformance Verdict, Positive Findings

### Community 86 - "Cognitive Load Assessment"
Cohesion: 0.29
Nodes (7): Cognitive Load Assessment, Cognitive Load Checklist, Extraneous Load: Bad Design, Germane Load: Learning Effort, Intrinsic Load: The Task Itself, The Working Memory Rule, Three Types of Cognitive Load

### Community 87 - "Impeccable Finish Reviewer"
Cohesion: 0.29
Nodes (6): Checks, in order, Disposition, Impeccable Finish Reviewer, Input Contract, Output Contract, Verdict Pass

### Community 88 - "Impeccable Manual Edit Applier"
Cohesion: 0.29
Nodes (6): Checks, Entry Atomicity, Impeccable Manual Edit Applier, Input Contract, Output Contract, Workflow

### Community 89 - "Regla: Comunicación Clara y Explicación de Tecnicismos"
Cohesion: 0.33
Nodes (5): 1. Directo y sin Relleno, 2. Explicación Obligatoria de Palabras Técnicas (Regla Clave), 3. Resumen Práctico, Ejemplos obligatorios:, Regla: Comunicación Clara y Explicación de Tecnicismos

### Community 90 - "graphify reference: query, path, explain"
Cohesion: 0.33
Nodes (5): For /graphify explain, For /graphify path, graphify reference: query, path, explain, Step 0 — Constrained query expansion (REQUIRED before traversal), Step 1 — Traversal

### Community 91 - "Diagnostic Scan"
Cohesion: 0.33
Nodes (6): 1. Accessibility (VoiceOver / TalkBack), 2. Performance, 3. Appearance & Theming, 4. Platform Conformance (CRITICAL), 5. Adaptivity, Diagnostic Scan

### Community 92 - "$impeccable hooks"
Cohesion: 0.33
Nodes (6): Constraints, Failure modes, Flow, $impeccable hooks, Routing, Triage findings

### Community 93 - "Visualize: Direction Comps & Asset Production"
Cohesion: 0.33
Nodes (5): After approval: the comp becomes a spec, Generate three compositional options, One approval point, Plates and provenance, Visualize: Direction Comps & Asset Production

### Community 94 - "Impeccable Documenter"
Cohesion: 0.40
Nodes (4): Impeccable Documenter, Input Contract, Output Contract, Workflow

### Community 95 - "Region map"
Cohesion: 0.40
Nodes (4): Containment, Painted material, Region map, What varies independently

### Community 96 - "graphify reference: add a URL and watch a folder"
Cohesion: 0.50
Nodes (3): For /graphify add, For --watch, graphify reference: add a URL and watch a folder

### Community 97 - "graphify reference: commit hook and native CLAUDE.md integration"
Cohesion: 0.50
Nodes (3): For git commit hook, For native CLAUDE.md integration, graphify reference: commit hook and native CLAUDE.md integration

### Community 98 - "graphify reference: incremental update and cluster-only"
Cohesion: 0.50
Nodes (3): For --cluster-only, For --update (incremental re-extraction), graphify reference: incremental update and cluster-only

### Community 99 - "Heuristics Scoring Guide"
Cohesion: 0.50
Nodes (4): Heuristics Scoring Guide, Issue Severity (P0–P3), Reference Material, Score Summary

### Community 100 - "Operate"
Cohesion: 0.50
Nodes (3): Comps, Directions, Operate

### Community 101 - "Read"
Cohesion: 0.50
Nodes (3): Comps, Directions, Read

## Knowledge Gaps
- **553 isolated node(s):** `fs`, `html`, `todas`, `ids`, `document` (+548 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 678 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **13 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Reference Material` connect `Heuristics Scoring Guide` to `Persona-Based Design Testing`, `critique.md`, `Cognitive Load Assessment`?**
  _High betweenness centrality (0.011) - this node is a cross-community bridge._
- **Why does `New visual work` connect `New visual work` to `new-work.md`?**
  _High betweenness centrality (0.009) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `initGlobalBar()` (e.g. with `hideAgentPollTooltip()` and `onDetectMessage()`) actually correct?**
  _`initGlobalBar()` has 7 INFERRED edges - model-reasoned connections that need verification._
- **What connects `fs`, `html`, `todas` to the rest of the system?**
  _553 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `modern-screenshot.umd.js` be split into smaller, more focused modules?**
  _Cohesion score 0.08959899749373433 - nodes in this community are weakly interconnected._
- **Should `el` be split into smaller, more focused modules?**
  _Cohesion score 0.1066066066066066 - nodes in this community are weakly interconnected._
- **Should `initPageChat` be split into smaller, more focused modules?**
  _Cohesion score 0.07017543859649122 - nodes in this community are weakly interconnected._