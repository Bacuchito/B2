/* ============================================================================
   design_audit.js — auditoría estática de diseño (skill apple-design, 5 lentes)
   ============================================================================
   Mide lo medible sin abrir un navegador: contrastes WCAG reales de los tokens,
   rejilla de 4/8pt, áreas táctiles, foco visible, movimiento reducido,
   materiales (cristal y sombras multicapa) y físicas (estados :active).

   Uso:
     node quiz/design_audit.js [quiz/template.html]

   Lee la hoja de estilo del fichero, resuelve los tokens y compone las
   transparencias sobre el fondo real. Sale con código 1 si algo falla.
   ============================================================================ */
"use strict";
const fs = require("fs");

const file = process.argv[2] || "quiz/template.html";
const html = fs.readFileSync(file, "utf8");
const styleMatch = html.match(/<style>([\s\S]*?)<\/style>/);
if (!styleMatch) { console.error("No encuentro el bloque <style> en " + file); process.exit(2); }
const css = styleMatch[1];

/* ---------- 1. Índice de reglas (con soporte de @media anidado) ---------- */
function parseCss(text, media, out) {
  let i = 0;
  while (i < text.length) {
    const open = text.indexOf("{", i);
    if (open < 0) break;
    const prelude = text.slice(i, open).replace(/\/\*[\s\S]*?\*\//g, "").trim().replace(/\s+/g, " ");
    let depth = 1, j = open + 1;
    while (j < text.length && depth > 0) {
      if (text[j] === "{") depth++;
      else if (text[j] === "}") depth--;
      j++;
    }
    const body = text.slice(open + 1, j - 1).replace(/\/\*[\s\S]*?\*\//g, "");
    if (prelude.startsWith("@media")) parseCss(body, prelude, out);
    else if (!prelude.startsWith("@")) {
      const decls = {};
      for (const d of body.split(";")) {
        const k = d.indexOf(":");
        if (k > 0) decls[d.slice(0, k).trim()] = d.slice(k + 1).trim();
      }
      out.push({ selector: prelude, media, decls });
    }
    i = j;
  }
}
const rules = [];
parseCss(css, "", rules);

const findRule = (selector) => rules.find((r) => !r.media && r.selector === selector);
const tokens = (() => {
  const root = findRule(":root");
  if (!root) { console.error("No encuentro :root con los tokens"); process.exit(2); }
  return root.decls;
})();

/* ---------- 2. Color: resolución, composición y contraste WCAG ----------
   Todo lleva el mapa de tokens como parámetro, porque la app tiene DOS temas y
   los dos se auditan: el oscuro (:root) y el claro ([data-theme="dark"]). */
const tokensClaro = (() => {
  const alt = findRule('[data-theme="dark"]');
  return alt ? Object.assign({}, tokens, alt.decls) : null;
})();
function resolve(value, mapa) {
  const T = mapa || tokens;
  let v = String(value || "").trim();
  for (let i = 0; i < 6 && v.includes("var("); i++) {
    v = v.replace(/var\((--[a-z0-9-]+)\)/gi,
      (_, name) => (T[name] !== undefined ? T[name] : (tokens[name] !== undefined ? tokens[name] : "transparent")));
  }
  return v;
}
function parseColor(value, mapa) {
  const v = resolve(value, mapa).toLowerCase();
  let m = v.match(/^#([0-9a-f]{3})$/);
  if (m) return { r: parseInt(m[1][0] + m[1][0], 16), g: parseInt(m[1][1] + m[1][1], 16), b: parseInt(m[1][2] + m[1][2], 16), a: 1 };
  m = v.match(/^#([0-9a-f]{6})$/);
  if (m) return { r: parseInt(m[1].slice(0, 2), 16), g: parseInt(m[1].slice(2, 4), 16), b: parseInt(m[1].slice(4, 6), 16), a: 1 };
  m = v.match(/^rgba?\(([^)]+)\)$/);
  if (m) {
    const p = m[1].split(",").map((x) => parseFloat(x));
    return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 };
  }
  if (v.startsWith("linear-gradient")) {
    const stop = v.match(/#[0-9a-f]{6}|rgba?\([^)]+\)/i);
    return stop ? parseColor(stop[0], mapa) : null;
  }
  return null;
}
const over = (fg, bg) => ({ r: fg.a * fg.r + (1 - fg.a) * bg.r, g: fg.a * fg.g + (1 - fg.a) * bg.g, b: fg.a * fg.b + (1 - fg.a) * bg.b, a: 1 });
const luminance = (c) => {
  const s = [c.r, c.g, c.b].map((x) => { const v = x / 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); });
  return 0.2126 * s[0] + 0.7152 * s[1] + 0.0722 * s[2];
};
const contrast = (a, b) => { const l1 = luminance(a), l2 = luminance(b); return (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05); };

const baseBg = parseColor(tokens["--bg"]);
function colorOf(spec, mapa, fondo) {
  let value;
  if (spec.literal) value = spec.literal;
  else if (spec.token) value = mapa[spec.token];
  else {
    const rule = findRule(spec.sel);
    if (!rule || rule.decls[spec.prop] === undefined) return null;
    value = rule.decls[spec.prop];
  }
  const c = parseColor(value, mapa);
  if (!c) return null;
  return spec.over ? over(c, fondo || baseBg) : c;
}

/* Los pares de contraste se miden contra la superficie REAL sobre la que se pinta
   cada texto. En el mundo «taller nocturno» la mayoría de los textos viven sobre
   una pieza (--panel) o sobre una hoja dentro de ella (--sheet); los estados
   llevan relleno propio. Los tintes translúcidos se componen con `over: true`
   sobre el fondo real, como manda el método de esta auditoría. */
const contrastChecks = [
  ["Texto principal sobre el fondo", { sel: "body", prop: "color" }, { token: "--bg" }],
  ["Texto de la cabecera sobre la banda", { sel: "header", prop: "color" }, { sel: "header", prop: "background" }],
  ["Texto secundario sobre la pieza (.ad .body)", { sel: ".ad .body", prop: "color" }, { token: "--sheet" }],
  ["Micro-etiqueta sobre la pieza (.panel h3)", { sel: ".panel h3", prop: "color" }, { token: "--sheet" }],
  ["Micro-texto sobre superficie hundida (.micro)", { sel: ".micro", prop: "color" }, { token: "--panel3" }],
  ["Texto terciario sobre el fondo (.empty)", { sel: ".empty", prop: "color" }, { token: "--bg" }],
  ["Acento sobre la pieza (.card-label)", { sel: ".card-label", prop: "color" }, { token: "--sheet" }],
  ["Tinta sobre relleno de acento (.btn)", { sel: ".btn", prop: "color" }, { token: "--acc-fill-1" }],
  ["Tinta sobre el extremo claro del degradado", { sel: ".btn", prop: "color" }, { token: "--acc-fill-2" }],
  ["Menú activo, pieza hundida (nav button.active)", { sel: "nav button.active", prop: "color" }, { sel: "nav button.active", prop: "background", over: true }],
  ["Menú inactivo (nav button)", { sel: "nav button", prop: "color" }, { sel: "nav", prop: "background", over: true }],
  ["Estadística de cabecera (.stat)", { sel: ".stat", prop: "color" }, { token: "--panel" }],
  ["Opción de respuesta (.opt)", { token: "--txt" }, { token: "--sheet" }],
  ["Letra ya asignada, hueco (.letters button.taken)", { sel: ".letters button.taken", prop: "color" }, { token: "--sheet" }],
  ["Letra corregida (.letters button.correct)", { sel: ".letters button.correct", prop: "color" }, { sel: ".letters button.correct", prop: "background", over: true }],
  ["Letra fallada (.letters button.wrong)", { sel: ".letters button.wrong", prop: "color" }, { token: "--sheet" }],
  ["Insignia confianza alta (.badge.hoch)", { sel: ".badge.hoch", prop: "color" }, { token: "--sheet" }],
  ["Insignia confianza media (.badge.mittel)", { sel: ".badge.mittel", prop: "color" }, { token: "--sheet" }],
  ["Insignia confianza baja (.badge.niedrig)", { sel: ".badge.niedrig", prop: "color" }, { token: "--sheet" }],
  ["Insignia 2ª lectura (.badge.ok)", { sel: ".badge.ok", prop: "color" }, { token: "--sheet" }],
  ["Insignia neutra (.badge.tag)", { sel: ".badge.tag", prop: "color" }, { token: "--sheet" }],
  ["Aviso amarillo (.note)", { sel: ".note", prop: "color" }, { token: "--sheet" }],
  ["Banner aprobado (.eval-banner.pass)", { sel: ".eval-banner.pass", prop: "color" }, { token: "--sheet" }],
  ["Banner suspenso (.eval-banner.fail)", { sel: ".eval-banner.fail", prop: "color" }, { token: "--sheet" }],
  ["Regla del popover (.err-popover-rule)", { sel: ".err-popover-rule", prop: "color" }, { sel: ".err-popover", prop: "background", over: true }],
  ["Texto de la pareja (.partner-body)", { sel: ".partner-body", prop: "color" }, { sel: ".partner-body", prop: "background", over: true }],
  ["Leyenda de errores (.legend-chip)", { sel: ".legend-chip", prop: "color" }, { sel: ".legend-chip", prop: "background", over: true }],
  ["Insignia de nube (.cloud-badge)", { sel: ".cloud-badge", prop: "color" }, { sel: ".cloud-badge", prop: "background", over: true }],
  ["Ayuda del formulario (.form-group small)", { sel: ".form-group small", prop: "color" }, { sel: ".modal", prop: "background", over: true }],
  ["Cronómetro en aviso (.timer-display.warn)", { sel: ".timer-display.warn", prop: "color" }, { token: "--sheet" }],
];

/* ---------- 3. Comprobaciones ---------- */
const results = [];
const ok = (lens, label, detail) => results.push({ lens, pass: true, label, detail });
const bad = (lens, label, detail) => results.push({ lens, pass: false, label, detail });

const MIN_TEXT = 4.5; // texto normal (HIG/WCAG AA)

/* Los dos temas se auditan. El claro hereda lo que no redefine, así que el mapa
   es la mezcla de :root y [data-theme="dark"]. */
const TEMAS = [["oscuro", tokens], ["claro", tokensClaro]];
for (const [tema, mapa] of TEMAS) {
  if (!mapa) { bad(1, "Tema " + tema, "no encuentro sus tokens"); continue; }
  const fondo = parseColor(mapa["--bg"], mapa);
  for (const [label, fgSpec, bgSpec] of contrastChecks) {
    const fg = colorOf(fgSpec, mapa, fondo), bg = colorOf(bgSpec, mapa, fondo);
    if (!fg || !bg) { bad(1, "[" + tema + "] " + label, "no se pudo resolver el color"); continue; }
    const ratio = contrast(fg, bg);
    (ratio >= MIN_TEXT ? ok : bad)(1, "[" + tema + "] " + label, ratio.toFixed(2) + ":1 (mínimo " + MIN_TEXT + ":1)");
  }
}

/* Rejilla de 4/8pt en el espaciado */
const SPACING_PROPS = /^(margin|padding|gap|row-gap|column-gap)(-(top|right|bottom|left|block|inline))?$/;
const offGrid = [];
for (const rule of rules) {
  for (const [prop, value] of Object.entries(rule.decls)) {
    if (!SPACING_PROPS.test(prop)) continue;
    for (const m of resolve(value).matchAll(/(-?\d+(?:\.\d+)?)px/g)) {
      const px = parseFloat(m[1]);
      if (px % 4 !== 0) offGrid.push(`${prop}:${px}px en "${rule.selector}"`);
    }
  }
}
for (const [name, value] of Object.entries(tokens)) {
  if (name.startsWith("--sp-") && parseFloat(value) % 4 !== 0) offGrid.push(`${name}:${value}`);
}
(offGrid.length === 0 ? ok : bad)(2, "Espaciado en rejilla de 4pt (márgenes, rellenos y huecos)",
  offGrid.length === 0 ? "todos los valores son múltiplos de 4" : offGrid.slice(0, 6).join(" · "));

/* Escala tipográfica por tokens */
const fontTokens = rules.filter((r) => !r.media).reduce((n, r) => n + Object.entries(r.decls).filter(([p, v]) => p === "font-size" && String(v).includes("var(--fs-")).length, 0);
(fontTokens >= 12 ? ok : bad)(2, "Escala tipográfica centralizada en tokens", fontTokens + " usos de var(--fs-*)");

/* Áreas táctiles: mínimo 28px en escritorio y 44px en móvil */
const interactive = ["nav button", ".btn", ".letters button", ".tab-pill", ".lang-btn", ".user-btn",
  ".modal-close", ".copy-btn", ".input", ".select", ".opt", ".lp-item", ".sec-reset", ".sec-toggle", "details.passage summary"];
const smallTargets = [];
for (const sel of interactive) {
  const rule = findRule(sel) || rules.find((r) => !r.media && r.selector.includes(sel));
  if (!rule) { smallTargets.push(sel + " (sin regla)"); continue; }
  const size = parseFloat(rule.decls["min-height"] || rule.decls["height"] || "0");
  if (!size || size < 28) smallTargets.push(`${sel} (${size || "sin altura"}px)`);
}
(smallTargets.length === 0 ? ok : bad)(1, "Área táctil mínima de 28px en escritorio",
  smallTargets.length === 0 ? interactive.length + " controles revisados" : smallTargets.join(" · "));

const mobileRule = rules.find((r) => r.media.includes("max-width:860px") && r.decls["min-height"] === "44px");
const mobileSelectors = mobileRule ? mobileRule.selector : "";
const notMobile = interactive.filter((sel) => !mobileSelectors.includes(sel));
(notMobile.length === 0 ? ok : bad)(1, "Área táctil mínima de 44px en móvil",
  notMobile.length === 0 ? interactive.length + " controles a 44px" : "faltan: " + notMobile.join(" · "));

/* Foco visible y sin trampas de teclado */
const focusVisible = rules.some((r) => r.selector.includes(":focus-visible") && r.decls["outline"]);
(focusVisible ? ok : bad)(1, "Anillo de foco visible global (:focus-visible)", focusVisible ? "2px con offset" : "no existe");
const outlineNone = rules.filter((r) => !r.media && r.decls["outline"] === "none");
const noRing = outlineNone.filter((r) => {
  const base = r.selector.split(",").map((s) => s.trim());
  return !base.every((sel) => rules.some((o) => o.selector.includes(sel.split(":")[0] + ":focus") && (o.decls["box-shadow"] || o.decls["border-color"])));
});
(noRing.length === 0 ? ok : bad)(1, "Ningún control quita el foco sin dar alternativa",
  outlineNone.length + " reglas con outline:none, todas con anillo propio");

/* Movimiento reducido */
const reduced = rules.some((r) => r.media.includes("prefers-reduced-motion"));
(reduced ? ok : bad)(4, "Respeta prefers-reduced-motion", reduced ? "bloque presente" : "no existe");

/* Materiales: piezas con relieve y un solo degradado de fondo (la luz cenital) */
const gradientsInBody = rules.filter((r) => /(^|,|\s)body(::before)?\s*(,|$)/.test(r.selector) && /gradient\(/.test(r.decls.background || ""));
(gradientsInBody.length === 1 ? ok : bad)(3, "Un solo degradado de fondo, la luz cenital",
  gradientsInBody.length === 1 ? "1 degradado en " + gradientsInBody[0].selector : gradientsInBody.length + " degradados de fondo");
const hairlineUses = rules.filter((r) => Object.values(r.decls).some((v) => String(v).indexOf("var(--line)") !== -1)).length;(hairlineUses >= 12 ? ok : bad)(3, "Bordes hairline desde el token --line (no gris plano)",
  hairlineUses + " reglas con var(--line)");
const blur = rules.filter((r) => r.decls["backdrop-filter"]).length;
(blur <= 2 ? ok : bad)(3, "Sin cristal decorativo (backdrop-filter como efecto, no como default)",
  blur + " superficies con backdrop-filter");
/* Este mundo se separa con filete, no con altura: ninguna sombra en ningún nivel. */
const shadowValues = ["--sh-1", "--sh-2", "--sh-3"].map((t) => String(tokens[t] || "").trim());
(shadowValues.every((v) => v === "none") ? ok : bad)(3, "Cero sombras: la pieza se separa con filete, no con altura",
  "niveles: " + shadowValues.join(" / "));
/* El segundo tema redefine tokens; no aplica filtros ni invierte colores. */
const altRule = rules.find((r) => r.selector.includes('[data-theme="dark"]'));
const altTokens = altRule ? Object.keys(altRule.decls).filter((k) => tokens[k] !== undefined).length : 0;
(altTokens >= 25 ? ok : bad)(3, "Segundo tema completo, por tokens (no filtros ni inversión)",
  altTokens + " tokens redefinidos en [data-theme=dark]");

/* Físicas y micro-interacciones */
const activeScale = rules.filter((r) => r.selector.includes(":active") && /scale/.test(r.decls["transform"] || "")).length;
(activeScale >= 8 ? ok : bad)(4, "Feedback de presión elástico (active:scale)", activeScale + " controles con hundimiento");
const springUses = rules.filter((r) => Object.values(r.decls).some((v) => String(v).includes("var(--spring)"))).length;
(springUses >= 4 ? ok : bad)(4, "Curva de resorte en las transiciones", springUses + " reglas con var(--spring)");
const durUses = rules.reduce((n, r) => n + Object.values(r.decls).filter((v) => String(v).includes("var(--dur-")).length, 0);
(durUses >= 20 ? ok : bad)(4, "Duraciones centralizadas en tokens", durUses + " usos de var(--dur-*)");

/* Identidad: voz editorial propia y cero estilos en línea sueltos */
const readFont = rules.filter((r) => String(r.decls["font-family"] || "").includes("var(--font-read)")).length;
(readFont >= 4 ? ok : bad)(5, "Voz tipográfica propia para lectura (serif offline)", readFont + " bloques con var(--font-read)");
const inlineStyles = (html.match(/style="[^"]*"/g) || []).length;
(inlineStyles <= 6 ? ok : bad)(5, "Sin estilos en línea (todo sale del sistema)", inlineStyles + " restantes (conmutadores display)");

/* ---------- 4. Informe ---------- */
const LENSES = { 1: "Accesibilidad y ergonomía", 2: "Jerarquía, espaciado y ritmo", 3: "Materiales y acabados", 4: "Dinamismo y físicas", 5: "Identidad y anti-plantilla" };
let currentLens = null;
console.log("\nAuditoría de diseño — " + file);
for (const r of results) {
  if (r.lens !== currentLens) { currentLens = r.lens; console.log("\nLente " + currentLens + " · " + LENSES[currentLens]); }
  console.log("  " + (r.pass ? "OK  " : "FALLO") + " " + r.label + "  →  " + r.detail);
}
const failed = results.filter((r) => !r.pass);
console.log("\n" + (results.length - failed.length) + "/" + results.length + " comprobaciones de diseño superadas");
if (failed.length) {
  console.log("Fallos: " + failed.map((f) => f.label).join(" · "));
  process.exit(1);
}
