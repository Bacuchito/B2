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
    this.open = false;
    this.style = {};
    todas.push(this);
  }
  set innerHTML(v) { this._html = String(v); this.children = []; }
  get innerHTML() { return this._html; }
  appendChild(c) { this.children.push(c); return c; }
  /* cuenta recursiva de nodos, para comprobar que se pintó algo */
  count() { return 1 + this.children.reduce((a, c) => a + (c.count ? c.count() : 0), 0); }
  collectText() {
    return (this._html || "") + (this.textContent || "") +
      this.children.map(c => (c.collectText ? c.collectText() : "")).join(" ");
  }
}

const ids = {};
["nav", "main", "stats", "reset", "doubt"].forEach(id => { ids[id] = new El("div"); });

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

/* ---------- comprobaciones ---------- */
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
check("el enunciado se pintó", /Moutasem|fragt sich|Firmenausweis|Text|Lesen/i.test(mainText),
      mainText.slice(0, 120));
check("los anuncios se pintaron", /Anzeigen|Auf ins Abenteuer|Umgangsformen/i.test(mainText));
check("las opciones de respuesta se pintaron", /letters|opt|Falsch|Richtig|[a-h]\)/i.test(mainText));

/* ---------- simulacion de un clic ---------- */
/* Hay que pulsar una OPCION DE RESPUESTA, no el boton "Reiniciar" (que
   también tiene onclick). Se buscan los pulsables dentro del panel main. */
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

/* ---------- informe ---------- */
let bad = 0;
for (const c of checks) {
  console.log((c.ok ? "  OK   " : "  FALLA") + "  " + c.name + (c.detail ? "  → " + c.detail : ""));
  if (!c.ok) bad++;
}
console.log(`\n${checks.length - bad}/${checks.length} comprobaciones superadas`);
process.exit(bad ? 1 : 0);
