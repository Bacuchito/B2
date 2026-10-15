/* Prueba de humo del visor: ejecuta el script del HTML con un DOM simulado
   para detectar errores de ejecución que un simple chequeo de sintaxis no ve.

   Uso: node smoke_test.js <B2_quiz.html>
*/
const fs = require("fs");

const file = process.argv[2];
const html = fs.readFileSync(file, "utf8");
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];

/* ---------- DOM mínimo ---------- */
const todas = [];   // registro de nodos creados, para poder simular clics

class El {
  constructor(tag) {
    this.tagName = tag;
    this.children = [];
    this._html = "";
    this.textContent = "";
    this.className = "";
    this.onclick = null;
    this.onchange = null;
    this.oninput = null;
    this.open = false;
    this.style = {};
    this.value = "";
    todas.push(this);
  }
  set innerHTML(v) { this._html = String(v); this.children = []; }
  get innerHTML() { return this._html; }
  appendChild(c) { this.children.push(c); return c; }
  querySelector(sel) {
    // selector básico para input
    return this.children.find(c => c.tagName === "input") || new El("input");
  }
  count() { return 1 + this.children.reduce((a, c) => a + (c.count ? c.count() : 0), 0); }
  collectText() {
    return (this._html || "") + (this.textContent || "") +
      this.children.map(c => (c.collectText ? c.collectText() : "")).join(" ");
  }
}

const ids = {};
["nav", "main", "stats", "reset", "doubt", "btn-ai-config", "modal-container"].forEach(id => { ids[id] = new El("div"); });

const document = {
  getElementById: id => ids[id] || (ids[id] = new El("div")),
  createElement: tag => new El(tag),
};

const store = {};
const localStorage = {
  getItem: k => (k in store ? store[k] : null),
  setItem: (k, v) => { store[k] = String(v); },
};

const window = { scrollTo: () => {} };

let errors = [];
try {
  const fn = new Function("document", "window", "localStorage", "confirm", script);
  fn(document, window, localStorage, () => true);
} catch (e) {
  errors.push("excepción al renderizar: " + e.message + "\n" + (e.stack || "").split("\n")[1]);
}

/* ---------- comprobaciones de lectura (Lesen) ---------- */
const checks = [];
function check(name, cond, detail) {
  checks.push({ name, ok: !!cond, detail: detail || "" });
}

check("sin excepciones al ejecutar", errors.length === 0, errors.join("\n"));

const navNodes = ids.nav.children.length;
const mainNodes = ids.main.children.length;
check("la barra lateral se rellenó", navNodes > 0, `nodos: ${navNodes}`);
check("el panel principal se rellenó", mainNodes > 0, `nodos: ${mainNodes}`);

const stats = ids.stats.innerHTML;
check("las estadísticas se calcularon", /respondidas/.test(stats), stats.slice(0, 90));

const mainText = ids.main.collectText();
check("el enunciado de Lesen se pintó", /Moutasem|fragt sich|Firmenausweis|Text|Lesen/i.test(mainText),
      mainText.slice(0, 120));
check("los anuncios se pintaron", /Anzeigen|Auf ins Abenteuer|Umgangsformen/i.test(mainText));
check("las opciones de respuesta se pintaron", /letters|opt|Falsch|Richtig|[a-h]\)/i.test(mainText));

/* ---------- simulación de clic en preguntas ---------- */
function descendientes(el, out) {
  out = out || [];
  for (const c of el.children) { out.push(c); descendientes(c, out); }
  return out;
}
const clicables = descendientes(ids.main).filter(e => typeof e.onclick === "function");
check("hay opciones pulsables en el panel", clicables.length > 0,
      `pulsables dentro de main: ${clicables.length}`);

if (clicables.length) {
  const antes = ids.main.collectText().length;
  try {
    clicables[0].onclick();
  } catch (e) {
    errors.push("excepción al pulsar una opción: " + e.message);
  }
  const despues = ids.main.collectText();
  check("el clic repinta la vista", despues.length !== antes,
        `antes ${antes} chars, después ${despues.length}`);
  check("aparece la corrección", /confianza:|Correcto|Incorrecto|correcta es/i.test(despues),
        despues.match(/confianza:[^<]*/i) ? "insignia de confianza presente" : "sin insignia");
  check("la respuesta se guardó", Object.keys(store).length > 0,
        Object.keys(store).join(",") || "localStorage vacío");
}

/* ---------- comprobaciones de Schreiben y AI Modal ---------- */
const schrBtn = ids.nav.children.find(c => />(E-Mail|Beitrag)</i.test(c._html || c.textContent));
check("sección de Schreiben presente en el menú", !!schrBtn, schrBtn ? (schrBtn.textContent || schrBtn._html).slice(0, 45) : "no encontrado");

if (schrBtn && typeof schrBtn.onclick === "function") {
  try {
    schrBtn.onclick();
  } catch (e) {
    errors.push("excepción al navegar a Schreiben: " + e.message);
  }
  const schrText = ids.main.collectText();
  check("el panel de Schreiben se pintó", /Situación laboral|Leitpunkte|Wörter/i.test(schrText), schrText.slice(0, 100));
  check("el editor y botón de evaluación están presentes", /Evaluar con Examinador telc/i.test(schrText));
}

/* Modal de configuración de IA */
const aiConfigBtn = ids["btn-ai-config"];
if (aiConfigBtn && typeof aiConfigBtn.onclick === "function") {
  try {
    aiConfigBtn.onclick();
  } catch (e) {
    errors.push("excepción al abrir modal de IA: " + e.message);
  }
  const modalText = ids["modal-container"].collectText();
  check("el modal de IA se abrió y muestra proveedores", /Configuración de Inteligencia Artificial|Google Gemini|DeepSeek/i.test(modalText));
}

/* ---------- comprobación de renderizado de resultados de evaluación ---------- */
try {
  const mockEval = {
    "schr-b-p66": {
      verdict: "BESTANDEN",
      score_total: 88,
      word_count: 172,
      criteria: {
        aufgabenbewaeltigung: { grade: "A", score: 23, feedback: "Todos los puntos tratados", leitpunkte_check: [{point: "Dank", covered: true, comment: "OK"}] },
        angemessenheit: { grade: "B", score: 21, feedback: "Registro formal adecuado" },
        korrektheit: { grade: "B", score: 22, feedback: "Gramática sólida" },
        repertoire: { grade: "A", score: 22, feedback: "Buen vocabulario B2" }
      },
      critical_errors: [
        { original: "Ich danke Sie", correction: "Ich danke Ihnen", rule_es: "Danken rige dativo.", type: "Grammatik" }
      ],
      strengths: ["Excelente cortesía"],
      areas_for_improvement: ["Más Nomen-Verb-Verbindungen"],
      corrected_version: "Sehr geehrter Herr Lassner..."
    }
  };
  if (window.quizState) {
    window.quizState.schreiben_evals = mockEval;
  }
  if (schrBtn && typeof schrBtn.onclick === "function") schrBtn.onclick();
} catch (e) {
  errors.push("excepción al pintar resultados de evaluación: " + e.message);
}
const evalText = ids.main.collectText();
check("los resultados de evaluación se pintan correctamente", /BESTANDEN|Aufgabenbewältigung|Correcciones gramaticales/i.test(evalText), evalText.match(/BESTANDEN[^<]*/i) ? "insignia BESTANDEN presente" : "");

/* ---------- informe ---------- */
let bad = 0;
for (const c of checks) {
  console.log((c.ok ? "  OK   " : "  FALLA") + "  " + c.name + (c.detail ? "  → " + c.detail : ""));
  if (!c.ok) bad++;
}
console.log(`\n${checks.length - bad}/${checks.length} comprobaciones superadas`);
process.exit(bad ? 1 : 0);
