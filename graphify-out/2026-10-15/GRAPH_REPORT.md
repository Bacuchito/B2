# Graph Report - B2  (2026-10-15)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 787 nodes · 2355 edges · 38 communities (34 shown, 4 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 63 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- connectSSE
- modern-screenshot.umd.js
- el
- initPageChat
- pdf2md.py
- live-browser.js
- initGlobalBar
- renderDesignVisual
- applyEditing
- handleManualEditActivity
- injectSvelteComponentsFromManifest
- smoke_test.js
- resumeSession
- captureElementToBlob
- resolveLiveInjectionAnchor
- startVariantObserver
- createLiveBrowserSessionState
- actOnAgentTarget
- onAnnotDown
- createLiveBrowserDomHelpers
- refreshParamsPanel
- injectVariantsFromSource
- scheduleAcceptCleanup
- handleGo
- syncEditBadgeHitProxies
- sendEvent
- build.py
- live-browser-ignores.js
- inspect_pdf.py
- impeccable
- buildColorModels
- documentRefSegment
- enableInlineEdit
- fix_review.py
- fix_review2.py
- make_quiz_sources.py
- fix_review3.py
- make_index.py

## God Nodes (most connected - your core abstractions)
1. `connectSSE()` - 34 edges
2. `setLiveState()` - 33 edges
3. `resumeSession()` - 33 edges
4. `showToast()` - 31 edges
5. `initGlobalBar()` - 30 edges
6. `el()` - 29 edges
7. `cleanup()` - 27 edges
8. `handleKeyDown()` - 27 edges
9. `injectSvelteComponentsFromManifest()` - 26 edges
10. `buildInsertConfigureRow()` - 26 edges

## Surprising Connections (you probably didn't know these)
- `enableInlineEdit()` --indirect_call--> `own()`  [INFERRED]
  .agents/skills/impeccable/scripts/live-browser.js → .agents/skills/impeccable/scripts/live-browser-dom.js
- `layoutFlowChildren()` --indirect_call--> `pickable()`  [INFERRED]
  .agents/skills/impeccable/scripts/live-browser.js → .agents/skills/impeccable/scripts/live-browser-dom.js
- `main()` --calls--> `norm()`  [INFERRED]
  quiz/build.py → quiz/_validate_ls_c.py

## Import Cycles
- None detected.

## Communities (38 total, 4 thin omitted)

### Community 0 - "connectSSE"
Cohesion: 0.07
Nodes (79): abandonForeignSession(), abandonSupersededGo(), abortSvelteComponentInjection(), beginNewLiveConfiguration(), cancelEditing(), cancelEditingToPicking(), cancelInsertConfigure(), cleanup() (+71 more)

### Community 1 - "modern-screenshot.umd.js"
Cohesion: 0.09
Nodes (55): ae(), be(), bt(), Ce(), s(), Ct(), de(), dt() (+47 more)

### Community 2 - "el"
Cohesion: 0.08
Nodes (55): actionLabel(), applyConfigureBarChrome(), bindConfigureCountPillTooltip(), bindConfigureInlineControlHover(), bindConfigureModifierPillHover(), buildConfigureActionControl(), buildConfigureCountControl(), buildConfigureRow() (+47 more)

### Community 3 - "initPageChat"
Cohesion: 0.08
Nodes (54): armPageChatForTyping(), attachSteerFocusDebug(), attachSteerFocusGuard(), buildSteerProcessingDots(), buildSteerQueueHint(), clearSteerAwaitTimer(), clearSteerFocusRecoverTimer(), collapsePageChat() (+46 more)

### Community 4 - "pdf2md.py"
Cohesion: 0.08
Nodes (27): bytes, Diagnostico: distribucion de huecos entre fragmentos de texto. Objetivo: elegir…, build_font(), build_lines(), code_width(), decode_string(), _emit(), extract_runs() (+19 more)

### Community 5 - "live-browser.js"
Cohesion: 0.07
Nodes (49): applyGlobalBarLabelState(), applyPlaceholderSizingStyles(), bufferToBase64(), buildPlaceholderResizeHandles(), collectFontCssText(), computeInsertPosition(), createInsertPlaceholder(), cursorForPlaceholderEdge() (+41 more)

### Community 6 - "initGlobalBar"
Cohesion: 0.10
Nodes (32): agentHasWorkInFlight(), agentStatusText(), applyLiveBarPreference(), barPaletteForTheme(), brandMarkSvg(), buildDesignHeader(), buildParamsPanel(), buildSavingRow() (+24 more)

### Community 7 - "renderDesignVisual"
Cohesion: 0.10
Nodes (30): buildCollapsible(), buildListHtml(), buildRadiiModels(), copyToClipboard(), cssSafe(), designEmptyMessage(), escapeHtml(), fontStack() (+22 more)

### Community 8 - "applyEditing"
Cohesion: 0.11
Nodes (27): addManualContextText(), applyEditing(), buildLocatorForLeaf(), canRestoreManualEditElement(), collectManualContextPieces(), walk(), contextElementForManualEdit(), copyEditContainerContext() (+19 more)

### Community 9 - "handleManualEditActivity"
Cohesion: 0.18
Nodes (25): clearStoredManualApplyState(), fetchPendingCount(), handleManualEditActivity(), hidePendingApplyDock(), manualApplyLoadingText(), manualApplyStateKey(), manualEditEventForCurrentPage(), numberOrNull() (+17 more)

### Community 10 - "injectSvelteComponentsFromManifest"
Cohesion: 0.14
Nodes (23): applyOriginalAttrsToSvelteAnchor(), clearMountErrorCard(), commitAcceptedSvelteComponentToDom(), componentModuleCandidates(), describeMountFailure(), detectDevServerBase(), findLiveElementForSvelteManifest(), getMountedSvelteComponentAnchor() (+15 more)

### Community 11 - "smoke_test.js"
Cohesion: 0.10
Nodes (13): checks, clicables, document, El, errors, fs, html, ids (+5 more)

### Community 12 - "resumeSession"
Cohesion: 0.16
Nodes (20): applySavedSessionMeta(), clampVariantIndex(), clearHandled(), findActiveSessionSummary(), findAdoptableServerSession(), findAnyVariantsWrapper(), findInsertAnchorInDom(), isSessionHandled() (+12 more)

### Community 13 - "captureElementToBlob"
Cohesion: 0.13
Nodes (19): averageRgb01(), captureChromeNodes(), captureElementFromRenderedAncestor(), captureElementToBlob(), compileShader(), cssColorToRgb01(), dominantRgb01(), findBackdropAncestor() (+11 more)

### Community 14 - "resolveLiveInjectionAnchor"
Cohesion: 0.16
Nodes (19): buildSvelteExpressionTextMap(), buildSveltePropValuesFromLiveElement(), buildSveltePropValuesV2(), cloneWithoutElements(), collectTextNodes(), collectVisibleTexts(), cssEscapeIdent(), elementMatchesOriginalMarkup() (+11 more)

### Community 15 - "startVariantObserver"
Cohesion: 0.23
Nodes (18): applyPlaceholderDimensions(), commitAcceptedVariantToDom(), ensureInsertPlaceholder(), findVariantsWrapper(), handleAccept(), isInsertGeneratingSession(), isVariantShown(), pickVariantContent() (+10 more)

### Community 16 - "createLiveBrowserSessionState"
Cohesion: 0.22
Nodes (15): createLiveBrowserSessionState(), clearHandled(), clearScrollY(), clearSession(), isHandled(), loadSession(), markHandled(), nextCheckpointRevision() (+7 more)

### Community 17 - "actOnAgentTarget"
Cohesion: 0.29
Nodes (17): actOnAgentTarget(), agentTargetBusyReason(), agentTargetOverlayGone(), agentTargetTaken(), claimAgentTarget(), claimAndActOnAgentTarget(), declineAgentTargetBusy(), declineAgentTargetUnresolvable() (+9 more)

### Community 18 - "onAnnotDown"
Cohesion: 0.20
Nodes (17): beginEditPin(), buildAnnotationsForCapture(), buildPinElement(), cancelEditingPin(), clampPlaceholderSize(), finalizeEditingPin(), initAnnotOverlay(), localCoords() (+9 more)

### Community 19 - "createLiveBrowserDomHelpers"
Cohesion: 0.16
Nodes (11): createLiveBrowserDomHelpers(), cssId(), liveUiRoot(), makeFrozenAnchor(), own(), pickable(), rectIsUsableAnchor(), uiAppend() (+3 more)

### Community 20 - "refreshParamsPanel"
Cohesion: 0.21
Nodes (15): applyParamDefaults(), applyParamValue(), closedClipPath(), getVisibleVariantEl(), hideParamsPanel(), openTunePopover(), parseVariantParams(), popoverDirection() (+7 more)

### Community 21 - "injectVariantsFromSource"
Cohesion: 0.21
Nodes (14): discardOrphanedSession(), enterRecoveryWaitingForAnchor(), injectVariantsFromSource(), isFrameworkComponentPreviewMode(), isJsxSourceFile(), isSvelteComponentManifestPath(), normalizeSessionPath(), probeJsxWrapperForOrphan() (+6 more)

### Community 22 - "scheduleAcceptCleanup"
Cohesion: 0.31
Nodes (11): acceptedDomAlreadyClean(), clearHandledWrapperReloadStamp(), deferredRecoverySuperseded(), ensureAcceptedDomClean(), findAcceptedRuntimeWrappers(), handledWrapperReloadKey(), reloadAfterMissingAcceptedDom(), restoreAcceptedDomFromSnapshot() (+3 more)

### Community 23 - "handleGo"
Cohesion: 0.24
Nodes (11): buildInsertPlaceholderSnapshotFromDom(), buildPickedAnchorSnapshot(), completeParameterPublication(), handleGo(), handleInsertCreate(), mountedParameterCount(), resolveScrollLockAnchorTop(), saveSession() (+3 more)

### Community 24 - "syncEditBadgeHitProxies"
Cohesion: 0.27
Nodes (10): bindEditBadgeProxy(), editBadgeProxyTargets(), initEditBadge(), initEditBadgeHitProxies(), positionEditBadge(), proxyMouseEvent(), setImportantStyle(), styleEditBadgeProxy() (+2 more)

### Community 25 - "sendEvent"
Cohesion: 0.29
Nodes (7): captureAndEmit(), checkpointPayload(), maybePrefetchPage(), reportVariantMounted(), reportVariantMountFailed(), sendCheckpoint(), sendEvent()

### Community 26 - "build.py"
Cohesion: 0.32
Nodes (6): main(), norm_ws(), Valida los JSON de preguntas y construye el HTML autocontenido. Uso: python…, Normaliza espacios para comparar citas con el texto del que salen., validate(), norm()

### Community 27 - "live-browser-ignores.js"
Cohesion: 0.52
Nodes (6): globToRegex(), matchesScope(), normalizeIgnoreRule(), normalizeIgnoreValue(), pageCandidates(), resolveDetectIgnores()

### Community 28 - "inspect_pdf.py"
Cohesion: 0.38
Nodes (6): decompress_stream(), find_objects(), main(), Inspecciona la estructura interna del PDF para planear el extractor. Solo…, Extrae objetos de nivel superior por fuerza bruta: 'N G obj ... endobj'., Localiza 'stream...endstream' y descomprime si es FlateDecode.

### Community 29 - "impeccable"
Cohesion: 0.60
Nodes (5): impeccable script, check_download(), fetch_url(), probe_ok(), setup_help()

### Community 30 - "buildColorModels"
Cohesion: 0.33
Nodes (6): buildColorModels(), buildTypographyModels(), findProseDescription(), humanizeKey(), normalizeCssColor(), splitFontFamily()

### Community 31 - "documentRefSegment"
Cohesion: 0.40
Nodes (6): documentRefClassSuffix(), documentRefIdSuffix(), documentRefSegment(), elementMatchesManualRefSegment(), indexAmongSameTag(), normalizeDocumentRefToken()

### Community 32 - "enableInlineEdit"
Cohesion: 0.40
Nodes (5): collectEditableTextRows(), visit(), enableInlineEdit(), onInlineInput(), wrapMixedContentTextNodes()

### Community 35 - "make_quiz_sources.py"
Cohesion: 0.67
Nodes (3): load_pages(), main(), Parte el Markdown convertido en ficheros fuente por bloque de variantes. Uso:…

## Knowledge Gaps
- **12 isolated node(s):** `checks`, `clicables`, `document`, `errors`, `fs` (+7 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 65 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `enableInlineEdit()` connect `enableInlineEdit` to `connectSSE`, `createLiveBrowserDomHelpers`, `live-browser.js`?**
  _High betweenness centrality (0.015) - this node is a cross-community bridge._
- **Why does `layoutFlowChildren()` connect `createLiveBrowserDomHelpers` to `connectSSE`, `live-browser.js`?**
  _High betweenness centrality (0.015) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `initGlobalBar()` (e.g. with `hideAgentPollTooltip()` and `onDetectMessage()`) actually correct?**
  _`initGlobalBar()` has 7 INFERRED edges - model-reasoned connections that need verification._
- **What connects `checks`, `clicables`, `document` to the rest of the system?**
  _12 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `connectSSE` be split into smaller, more focused modules?**
  _Cohesion score 0.07160493827160494 - nodes in this community are weakly interconnected._
- **Should `modern-screenshot.umd.js` be split into smaller, more focused modules?**
  _Cohesion score 0.08959899749373433 - nodes in this community are weakly interconnected._
- **Should `el` be split into smaller, more focused modules?**
  _Cohesion score 0.07609427609427609 - nodes in this community are weakly interconnected._