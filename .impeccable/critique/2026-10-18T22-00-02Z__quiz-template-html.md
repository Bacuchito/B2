---
target: quiz/template.html
total_score: 25
max_score: 40
na_heuristics: 
p0_count: 0
p1_count: 4
target_identity: "file:C:\\Users\\sergi\\Documents\\Code\\B2\\quiz\\template.html"
target_fingerprint: "sha256:2b04ccb9deba67b687e4e085179d07235cc924bf5c7a08c6a4ba7fc08270d905"
target_path: "C:\\Users\\sergi\\Documents\\Code\\B2\\quiz\\template.html"
timestamp: 2026-10-18T22-00-02Z
slug: quiz-template-html
---
# Crítica de diseño — B2 Beruf Test (`quiz/template.html`)

Method: dual-agent (A: bd84df00-7c24-437b-83a5-66fcd660fe02 · B: 8f923860-50ae-4d34-8d80-052a206528bb)

## Puntuación de salud del diseño

| # | Heurística | Nota | Problema clave |
|---|---|---|---|
| 1 | Visibilidad del estado | 3 | `saveState()` se come todos los errores (`catch(e){}`, template.html:1705) → pérdida silenciosa; no hay `aria-live` y el veredicto no se anuncia. |
| 2 | Sistema ↔ mundo real | 4 | Partes telc, Leitpunkte, bandas y pesos, «Página 8 del PDF», 45 min, 150 palabras, alemán verbatim / ayuda ES-RU. |
| 3 | Control y libertad | 2 | Responder confirma al primer clic, sin deshacer y sin borrado por ítem; la evaluación del LLM no se cancela. |
| 4 | Consistencia | 3 | Borrado destructivo como `.btn.ghost` aunque `.btn.danger` existe (402); `correct/wrong` con hex fuera de tokens (361-364); `sec-count` significa «variantes» (1952) o «dudosas» (1999). |
| 5 | Prevención de errores | 2 | Borrado de variante sin `confirm()` (2154-2158) cuando el reinicio de sección sí confirma (1979); re-pulsar sobrescribe en silencio. |
| 6 | Reconocer > recordar | 1 | 8 anuncios alemanes que sostener en memoria mientras se responden 5 enunciados debajo. |
| 7 | Flexibilidad y eficiencia | 2 | Sin atajos de teclado, sin «siguiente sin responder»; siempre abre en `allVariants[0]` (1915). |
| 8 | Estética y minimalismo | 3 | 40 fichas idénticas, 5 controles en cabecera, etiqueta-chip en cada panel. |
| 9 | Recuperación de errores | 3 | Buen tratamiento del fallo; faltan `aria-live` y la ruta «sin clave API» es un `alert()` nativo (2603-2617). |
| 10 | Ayuda y documentación | 2 | Nada explica `confianza: mittel` ni `✓ 2ª lectura` en el primer contacto. |
| **Total** | | **25/40** | **Aceptable (20-27)**. Máximo 40: superficie Operate, ninguna heurística `n/a`. |

## Veredicto de especificidad

Contenido y semántica específicos; superficie e interacción central genéricas. Otro test podría reutilizar el armazón (cabecera pegajosa + índice plegable + pilas de tarjetas con chip + botones de opción en serie).

Tics genéricos concretos:
1. Vocabulario de emoji: `⚙ Configurar IA` (768), `✨ Evaluar con Examinador telc B2` (913), `💡 Redemittel` (903), `🏆 Redacción Modelo 100 pts` (946), pestañas `📝/📄/⭐/🔍` (943-946), `☁️/💾/🗑/⬇/⬆` (1007-1025), `↺ Reiniciar` (883). La app ya trae juego propio de SVG (762, 1401-1402).
2. Sopa de tarjetas con chip: `.panel` (248-250) + `.panel h3` (252-254) en «INSTRUCCIONES», «SITUACIÓN LABORAL Y TAREA OFICIAL TELC B2» y cada subbloque de Schreiben.
3. Cinco rejillas de respuesta idénticas: 5 enunciados × 8 fichas (4068-4086) = 40 cuadrados iguales, sin vínculo con el anuncio correspondiente.
4. Tres chips fantasma en versalitas de 11 px (`SOLO DUDOSAS`, `⚙ CONFIGURAR IA`, `ÍNDICE`; 397-399): la función firma con el menor énfasis de la interfaz.
5. Una receta de elevación repetida ~12 veces; `design_audit.js` la premia como consistencia (212-218).

Específico de este producto: el bloque de corrección (4129-4137: veredicto + confianza + `✓ 2ª lectura` + cita alemana en serif cursiva entre `„…“` + explicación); la duda como objeto de primera clase; el mundo de papel aplicado a decisiones (filete doble 160, regla de margen roja 317-318, burbuja `.q .num`, raya de hueco de 56 px, sello rotado 492-500); la mesa de examen (724-740) con `main.desk` decidido por el render (2050-2051); y la honestidad como regla de maquetación (`.ad.used/.unused`, 2090-2096).

Diagnóstico en una frase: todo lo distintivo vive por debajo del pliegue o después de la primera respuesta; la pantalla que se ve —8 anuncios y cinco filas de `a b c d e f g h`— es la más genérica.

Escaneo determinista: 4 hallazgos (2 por objetivo), ambos `warning`/`slop`, ambos falsos positivos.
- `side-tab` (`border-bottom:3px`) en template.html:160: es el filete doble horizontal de la cabecera, no una barra lateral de tarjeta. Todos los `border-left/right` del archivo son de 1-2 px. La regla informa `line: 0`.
- `cream-palette` (`rgb(233,226,209)`) en template.html:22: 1 de 6 superficies con nombre, con variante oscura, documentada como mundo «Prüfungsbogen». Contraste remedido 4,84:1 / 6,96:1 / 15,44:1. Cumple el propio test de la regla y seguirá saltando.

Superposiciones: ninguna. Sin herramienta de navegador no hay inyección ni overlay visible; la evidencia son capturas medidas.

Corrección de evidencia: en un render real de 390 px (`Emulation.setDeviceMetricsOverride`) `scrollWidth` = `innerWidth` = 390 con 0 elementos desbordados. No hay desbordamiento horizontal en móvil; la captura `3-mobile.png` era un recorte de una ventana de ~500 px.

## Impresión general

No es una app con slop de CSS: es una app con una idea buena y una capa de superficie que la esconde. El problema real está en la composición y la jerarquía, que ninguna regla determinista mira. La mayor oportunidad: la mesa de examen ya existe y el portátil de 1440 no llega a verla.

## Lo que funciona

1. El bloque de corrección es el producto (4129-4137): cita + confianza + segunda lectura + explicación, con la cita vestida como texto fuente.
2. La honestidad como regla de maquetación: `.ad.used/.unused` enseña tus asignaciones y nunca la clave; `ourScaleNote` (934) dice en la interfaz que la app puntúa más dura que telc.
3. El mundo de papel aplicado a decisiones, no a texturas.

## Problemas prioritarios

**[P1] La mesa de examen detrás de una puerta de 1500 px.** Medido a 1440×1000: panel de referencia de 1366 px de alto, primera fila de letras en y=1815, documento de 2556. `main.desk` ya está en el DOM a 1440; solo lo bloquea `@media(min-width:1500px)` (724). Fix: bajar a `min-width:1280px` con columna de referencia fluida (`clamp(320px,40vw,600px)` en vez de `--desk-ref:600px`), conmutador «Mesa de examen» en cabecera y *peek* con `.ad.peek` (`--tint-acc`) + `scrollIntoView`. Comando: `$impeccable layout`.

**[P1] Teclado y lector de pantalla no pueden responder la mayoría de los ítems.** `.opt` es un `<div onclick>` sin `tabindex`/`role` (4095-4105) → todo lo que no sea emparejar es solo ratón. `renderMain()` vacía `main` (2046) y el foco cae al `<body>`; sin `aria-live`; las fichas se anuncian «a»…«h» (4075). `design_audit.js`, que lee CSS, no puede verlo. Fix: `<button role="radio">` en `<section role="radiogroup" aria-labelledby>`; `aria-live="polite"` en `.fb`; `data-key` estable y restaurar foco; enlace de salto. Comando: `$impeccable harden`.

**[P1] Las fichas a–h: 40 controles idénticos sin estado ni vínculo con la referencia.** `.letters button.sel` (359-360) y `.opt.sel` (339-340) son estados muertos (la rama exige `!answered`, 4082/4094/4100). Misclic irreversible salvo borrar todo (4083 confirma sin condición). `design_audit.js:119` valida el contraste de un estado inalcanzable. Fix: atenuar letras ya usadas (dato `used`, 2093-2096); `.peek` visible por fila (sustituye el `title` de 4076); `role="radiogroup"` + `aria-pressed`; borrado por ítem. Comando: `$impeccable clarify`.

**[P1] El contador de «correctas» es hindsight, no una nota.** `b.onclick` (4083) escribe sin condición, así que `0 correctas (0%)` (1909-1911) se infla pulsando la letra que la app acaba de marcar en verde. Fix: registrar solo el primer intento (`state.first[ansKey]`) y mostrar `respondidas · aciertos a la primera · 55 dudosas` + «resueltas tras ver la clave»; quitar el `%`. Comando: `$impeccable clarify`.

**[P2] Primer contacto y final de sesión.** La cabecera grita `0/358 · 0 correctas · 55 dudosas` antes de preguntar nada, y el alivio (cita, confianza, segunda lectura) solo llega después de responder. Al final, el último elemento es un borrado sin confirmación (2154-2158) mientras el reinicio de sección sí confirma (1979). Fix: explicar `confianza` y `✓ 2ª lectura` en el primer contacto; etiquetar el porqué del «55 dudosas»; `bClear` como `.btn danger` con `confirm()`; tarjeta de cierre con balance de variante y `Siguiente variante →`. Comando: `$impeccable onboard`.

## Banderas por persona

**Alex (repetidor impaciente).** Abre en Lesen Teil 1 Variante 1 por 300.ª vez (1915); el único `onkeydown` del archivo es el del índice (1962); ~40 tabulaciones por variante y el foco vuelve al `<body>` tras cada respuesta (2046); sin «siguiente sin responder» ni borrado por ítem. Falla: reanudar, borrado por ítem, salto al siguiente, teclado.

**Sam (depende de accesibilidad).** Sin enlace de salto: 8 controles de cabecera + 10 secciones antes del ítem. En Lesen Teil 2 `.opt` es un `<div onclick>` no enfocable (4095-4105) → no puede responder. Veredicto mudo (sin `aria-live`), fichas sin etiqueta de grupo. Contraste, `prefers-reduced-motion` (743-747) y anillo de foco (146) sí cumplen: los fallos son semánticos.

**Riley (probador de estrés).** Pulsa todas las letras tras ver el verde: el contador sube al 100 % mientras `state.answers` guarda solo el último clic. «Mostrar todas» sin confirmación (2149-2153). Borrado accidental sin confirmar ni deshacer. `saveState()` falla en silencio (1705) y la cabecera sigue informando de progreso que no sobrevivirá a recargar. Falla: integridad de la nota, guardas destructivas, persistencia muda, escala (98 entradas).

## Observaciones menores

- La captura «móvil» del turno anterior no era válida (recorte de ~500 px); `.design/desk-390.png` demuestra que a 390 px la maqueta funciona. Riesgo no cubierto: Schreiben y banco de palabras nunca renderizados a ese ancho.
- Falso positivo de B: el «tirón vacío de 508 px» al final es un artefacto de la captura de 3000 px de alto; `nav{height:calc(100vh - 57px)}` (185) hace que en ventanas más altas que el contenido el documento mida una pantalla. A 1000 px de alto el documento son 2556 y el contenido lo llena.
- `--read-w:68ch` (≈495 px) dentro de una tarjeta de 896 px deja 368 px (41 %) del interior vacío a 1440, más 224 px de canalón muerto.
- Etiqueta del índice partida a mitad de palabra: «SCHREIBEN: BESCHWERDE-E-» / «MAIL».
- Política de confirmaciones desigual: `confirm()` en reinicio de sección (1979), borrador (916) y evaluación (964); no en borrado de variante ni en «mostrar todas».
- `--fs-h2:32px` no baja de 860 px (74 vs 696-715).
- Las mayúsculas son la única señal de «silencio» (397-399, 188-192, 240-244, 252-254): cuatro trabajos con un mismo tratamiento.
- La función firma es una etiqueta que cambia de texto (`Solo dudosas` ↔ `Ver todas`, 4163) con el contador en otro sitio.
- Las filas Richtig/Falsch pintan una columna `•` (4102) junto a etiquetas que ya lo dicen.
- El temporizador de 45 min existe solo para Schreiben: la lectura no tiene concepto de sesión.

## Preguntas para pensar

1. Si la promesa es «la clave se dedujo y aquí está la duda», ¿por qué la evidencia solo se ve después de responder? ¿Cómo sería un modo «estudiar la clave», con cada anuncio anotado con su cita y su confianza, sin responder nada?
2. ¿Y si Lesen Teil 1 se respondiera pulsando el anuncio en vez de decodificar a→h? ¿Se mantienen las letras porque telc las usa o porque venían en el PDF?
3. La cabecera informa de una nota que se puede inflar pulsando lo que la app ya reveló. ¿Es una nota o un estado de ánimo?
4. Schreiben se sincroniza por Firebase pero las respuestas de lectura no. ¿Cómo sería una sesión compartida («Sergio 3/5 · Diana 5/5 · 2 en desacuerdo»), si el desacuerdo entre vosotros es justo la señal que esta app existe para mostrar?
5. ¿Significa algo una barra de progreso a 358 ítems cuando se estudia por secciones y nunca se pretende terminar el conjunto?
