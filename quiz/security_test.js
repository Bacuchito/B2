/* Pruebas de regresión de seguridad y robustez del visor.
   Reproduce los hallazgos críticos de la auditoría del 17/10/2026:
     C1  XSS por el parámetro ?room= (y por el room guardado en localStorage)
     C2  esc() no escapaba comillas: ruptura del atributo value="..." del modal
     C3  XSS desde la evaluación de la pareja en Firestore (score_total)
     C5  una evaluación malformada rompía la pantalla de esa tarea
   Y comprueba la sincronización de la que depende el uso entre dos personas:
     S1  la sala por defecto es aleatoria, nunca la constante "sergio-diana"
     S2  si la escritura falla, la insignia lo dice en vez de mentir
     S3  un borrador escrito sin conexión se sube al abrir la tarea
     S9  el borrador es de cada perfil: cambiar de perfil no mezcla el trabajo
     S10 la nube devuelve tu redacción y tu evaluación si el navegador no las tiene
     S11 una copia local vieja se refresca con la de la nube, sin pisar ediciones sin enviar
   Uso: node quiz/security_test.js quiz/B2_quiz.html
*/
const fs = require("fs");

const file = process.argv[2] || "quiz/B2_quiz.html";
const html = fs.readFileSync(file, "utf8");
/* Script de la app = bloque <script> inline más largo (el <head> tiene uno
   minúsculo que aplica el tema antes del primer pintado). */
const bloques = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
const script = bloques.reduce((a, b) => (b.length > a.length ? b : a), "");
const PAYLOAD = '<img src=x onerror="globalThis.__pwn()">';

/* ---------- DOM simulado (registra los nodos por id, como el real) ---------- */class El {
  constructor(tag) {
    this.tagName = tag;
    this.children = [];
    this._html = "";
    this.textContent = "";
    this.className = "";
    this.style = {};
    this.value = "";
    this.onclick = null;
    this.open = false;
    this._id = "";
  }
  set innerHTML(v){ this._html = String(v); this.children = []; }
  get innerHTML(){ return this._html; }
  set id(v){ this._id = v; if (v) registro[v] = this; }
  get id(){ return this._id; }
  appendChild(c){ this.children.push(c); return c; }
  querySelector(){ return new El("input"); }
  querySelectorAll(){ return []; }
  html(){ return (this._html || "") + this.children.map(c => c.html()).join(""); }
  texto(){ return (this._html || "") + (this.textContent || "") + this.children.map(c => c.texto()).join(" "); }
}

let registro = {};
function montar(search, storeInicial, conFirebase, falloEscritura) {
  registro = {};
  const store = storeInicial || {};
  if (conFirebase) store.b2quiz_firebase = JSON.stringify({ apiKey: "fake", projectId: "fake" });
  const avisos = [];
  const escritos = [];
  let snapshotCb = null;

  const document = {
    getElementById: id => registro[id] || (registro[id] = new El("div")),
    createElement: tag => new El(tag),
    documentElement: new El("html"),
    querySelector: () => null,
    querySelectorAll: () => [],
  };
  const localStorage = {
    getItem: k => (k in store ? store[k] : null),
    setItem: (k, v) => { store[k] = String(v); },
    removeItem: k => { delete store[k]; },
  };
  const window = { scrollTo(){}, location: { search: search, href: "http://x/B2_quiz.html" + search } };
  const docRef = {
    set(payload){
      escritos.push(payload || {});
      if (falloEscritura) {
        return { then(){ return { catch(cb){ cb && cb({ message: "permission-denied" }); return this; } }; } };
      }
      return { then(cb){ cb && cb(); return { catch(){} }; }, catch(){} };
    },
    get(){ return Promise.resolve({ exists: false, data: () => ({}) }); },
    onSnapshot(cb){ snapshotCb = cb; return () => { snapshotCb = null; }; },
    collection(){ return { doc: () => docRef }; },
  };
  const firebase = {
    apps: [],
    initializeApp(){ this.apps.push({}); },
    firestore(){ return { collection: () => ({ doc: () => docRef }) }; },
  };

  const fn = new Function("document", "window", "localStorage", "confirm", "alert", "firebase", script);
  fn(document, window, localStorage, () => true, m => avisos.push(String(m)), conFirebase ? firebase : undefined);
  return { registro, store, window, avisos, escritos, empujarSnapshot: d => snapshotCb && snapshotCb({ exists: true, data: () => d }) };
}

const abrirSchreiben = ids => {
  const b = ids.nav.children.find(c => />(E-Mail|Beitrag)</i.test(c._html || c.textContent || ""));
  if (b) b.onclick();
  return b;
};

const buscar = (nodo, prueba) => {
  if (prueba(nodo)) return nodo;
  for (const c of nodo.children || []) {
    const encontrado = buscar(c, prueba);
    if (encontrado) return encontrado;
  }
  return null;
};

/* ---------- comprobaciones ---------- */
const checks = [];
const check = (nombre, cond, detalle) => checks.push({ nombre, ok: !!cond, detalle: detalle || "" });

/* C1 · parámetro de URL */
{
  const h = montar("?room=" + encodeURIComponent(PAYLOAD), {}, true);
  const badge = (h.registro["cloud-status-indicator"] || new El("div")).html();
  check("un ?room= inválido no se refleja en el HTML",
    !/<img/i.test(badge), badge.slice(0, 90));
  check("un ?room= inválido no se usa como sala",
    h.store.b2quiz_room !== PAYLOAD, "b2quiz_room=" + h.store.b2quiz_room);
}

/* S1 · sala por defecto */
{
  const a = montar("", {}, true);
  const b = montar("", {}, true);
  const salaA = a.store.b2quiz_room || "";
  check("la sala por defecto es aleatoria y válida (nunca «sergio-diana»)",
    /^b2-[0-9a-z]{16}$/.test(salaA) && a.registro["cloud-status-indicator"].html().includes(salaA),
    "sala=" + salaA + " | " + a.registro["cloud-status-indicator"].html().slice(0, 70));
  check("dos navegadores generan salas distintas",
    salaA && b.store.b2quiz_room !== salaA, "A=" + salaA + " B=" + b.store.b2quiz_room);
}

/* C1 · valor ya guardado en localStorage */
{
  const h = montar("", { b2quiz_room: PAYLOAD }, true);
  const badge = (h.registro["cloud-status-indicator"] || new El("div")).html();
  check("un room inválido guardado en localStorage se ignora",
    !/<img/i.test(badge), badge.slice(0, 90));
}

/* Caso normal: no rompemos lo que funcionaba */
{
  const h = montar("?room=sala-prueba", {}, true);
  const badge = (h.registro["cloud-status-indicator"] || new El("div")).html();
  check("un room válido se sigue usando",
    h.store.b2quiz_room === "sala-prueba" && badge.includes("sala-prueba"),
    "b2quiz_room=" + h.store.b2quiz_room + " | " + badge.slice(0, 70));
}

/* C2 · contrato de esc() */
{
  const h = montar("");
  const esc = h.window.esc;
  check("esc() escapa comillas (seguro dentro de atributos)",
    typeof esc === "function" && esc('"') === "&quot;" && esc("'") === "&#39;" && esc("<b>") === "&lt;b&gt;",
    typeof esc === "function" ? esc('a"b') : "window.esc no expuesto");
}

/* C2 · ruptura del atributo value del modal */
{
  const h = montar("", { b2quiz_room: PAYLOAD.replace("<img", '" autofocus onfocus="x') }, true);
  const btn = h.registro["btn-ai-config"];
  if (btn && btn.onclick) btn.onclick();
  const modal = (h.registro["modal-container"] || new El("div")).innerHTML;
  check("el modal de IA no permite romper el atributo value",
    !/onfocus=|autofocus/.test(modal), (modal.match(/id="cfg-room-id"[^>]*/) || ["(sin input)"])[0]);
}

/* S4 · configuración de Firebase tal cual la da la consola de Google */
{
  const h = montar("");
  const parsear = h.window.parseFirebaseConfig;
  const google = [
    "// Import the functions you need from the SDKs you need",
    'import { initializeApp } from "firebase/app";',
    "const firebaseConfig = {",
    '  apiKey: "AIzaFalsa",',
    '  authDomain: "x.firebaseapp.com",',
    '  projectId: "x",',
    '  appId: "1:2:web:3",',
    "};",
  ].join("\n");
  let cfg = null, error = null;
  try { cfg = parsear ? parsear(google) : null; } catch (e) { error = e; }
  check("acepta el fragmento JavaScript de la consola de Firebase (claves sin comillas)",
    cfg && cfg.projectId === "x" && cfg.apiKey === "AIzaFalsa",
    error ? error.message : (cfg ? "projectId=" + cfg.projectId : "no devolvió nada"));

  let puro = null;
  try { puro = parsear ? parsear('{"apiKey":"a","projectId":"p"}') : null; } catch (e) {}
  check("sigue aceptando JSON puro", !!puro && puro.projectId === "p", "");

  let fallo = null;
  try { parsear ? parsear("esto no es una configuración") : null; } catch (e) { fallo = e; }
  check("una configuración sin objeto { … } se rechaza con error",
    !!fallo, fallo ? fallo.message : "no lanzó error");
}

/* S5 · importar una copia de seguridad del progreso */
{
  const h = montar("", {}, false);
  const antes = h.window.quizState;
  antes.schreiben_drafts["basura"] = "debe desaparecer";
  let r = null, error = null;
  try {
    r = h.window.aplicarProgreso({ answers: { "t1-v1": "a" }, schreiben_drafts: { "schr-b-p66": "texto importado" } });
  } catch (e) { error = e; }
  const s = h.window.quizState;
  check("importar progreso sustituye los datos y reengancha quizState",
    !error && s !== antes && s.answers["t1-v1"] === "a" &&
    s.schreiben_drafts["sergio::schr-b-p66"] === "texto importado" && !s.schreiben_drafts["basura"] && r && r.respuestas === 1,
    error ? error.message : "respuestas=" + Object.keys(s.answers).length + " borradores=" + Object.keys(s.schreiben_drafts).length);
  check("tras importar, el progreso queda guardado en localStorage",
    /texto importado/.test(h.store["b2quiz.v1"] || ""), (h.store["b2quiz.v1"] || "").slice(0, 60));

  /* Una exportación antigua (clave sin perfil) se le asigna a quien la exportó,
     aunque la importe el otro perfil. */
  const h2 = montar("?user=diana", {}, false);
  h2.window.aplicarProgreso({ answers: {}, schreiben_drafts: { "schr-b-p66": "de Sergio" } }, "sergio");
  const claves2 = Object.keys(h2.window.quizState.schreiben_drafts);
  check("una exportación antigua se queda con el perfil que la exportó",
    claves2.length === 1 && claves2[0] === "sergio::schr-b-p66", "claves: " + claves2.join(","));
}

/* S6 · no hay «Reiniciar» global: borrar todo vive dentro de ⚙ Configurar IA */
{
  check("el botón global de reiniciar ya no está en la barra",
    !/id="reset"/.test(html), /id="reset"/.test(html) ? "todavía aparece en el HTML" : "eliminado");

  const h = montar("", {}, false);
  h.window.quizState.answers["t1-v1"] = "a";
  h.window.quizState.schreiben_drafts["sergio::schr-b-p66"] = "un borrador";
  const abrir = h.registro["btn-ai-config"];
  if (abrir && abrir.onclick) abrir.onclick();
  const borrar = h.registro["btn-delete-all-progress"];
  check("borrar todo el progreso está dentro de ⚙ Configurar IA",
    !!(borrar && typeof borrar.onclick === "function"),
    borrar && borrar.onclick ? "enganchado" : "sin manejador");
  if (borrar && borrar.onclick) borrar.onclick();
  const s = h.window.quizState;
  check("borrar todo deja el progreso vacío y el estado reenganchado",
    Object.keys(s.answers).length === 0 && Object.keys(s.schreiben_drafts).length === 0,
    "respuestas=" + Object.keys(s.answers).length + " borradores=" + Object.keys(s.schreiben_drafts).length);
}

/* S7 · reiniciar un bloque entero (por ejemplo Lesen Teil 1) sin tocar el resto */
{
  const h = montar("", {}, false);
  const nav = h.registro["nav"];
  const secciones = h.window.DATA.sections.filter(s => (s.variants || []).some(v => v.kind !== "schreiben"));
  const secA = secciones[0], secB = secciones[1];
  const claves = sec => {
    const ks = [];
    sec.variants.filter(v => v.kind !== "schreiben").forEach(v =>
      (v.items || []).forEach((it, i) => ks.push(v.id + "#" + i)));
    return ks;
  };
  const clavesA = claves(secA), clavesB = claves(secB);
  check("sin respuestas no aparece el botón de reiniciar bloque",
    !buscar(nav, e => e.className === "sec-reset"), "secciones: " + secciones.length);

  clavesA.slice(0, 3).forEach(k => { h.window.quizState.answers[k] = "a"; });
  clavesB.slice(0, 2).forEach(k => { h.window.quizState.answers[k] = "a"; });
  const variante = buscar(nav, e => e.tagName === "button" && e.onclick && e.className !== "sec-reset");
  if (variante) variante.onclick();            // fuerza un render con las respuestas ya puestas

  const bReset = buscar(nav, e => e.className === "sec-reset");
  check("con respuestas aparece el botón de reiniciar en el encabezado del bloque",
    !!(bReset && typeof bReset.onclick === "function"), bReset ? "«" + (bReset.textContent || "") + "»" : "no apareció");

  if (bReset && bReset.onclick) bReset.onclick();
  const quedanA = clavesA.filter(k => h.window.quizState.answers[k] !== undefined).length;
  const quedanB = clavesB.filter(k => h.window.quizState.answers[k] !== undefined).length;
  check("reiniciar el bloque borra solo ese bloque, no los demás",
    quedanA === 0 && quedanB === 2, "bloque A: " + quedanA + " · bloque B: " + quedanB);
}

/* S8 · la configuración se pega a mano una vez por navegador, y el HTML no lleva
   ninguna clave incrustada (para que GitHub no vuelva a avisar de un secreto) */
{
  const h = montar("?user=diana&room=sala-prueba", {}, false);
  abrirSchreiben(h.registro);
  const badge = (h.registro["cloud-status-indicator"] || new El("div")).html();
  check("sin pegar la configuración, la app avisa de que va en modo local",
    /cloud-dot offline/.test(badge), badge.replace(/<[^>]*>/g, "").slice(0, 70));

  check("el HTML compilado no contiene ninguna clave incrustada",
    !/AIza[0-9A-Za-z_\-]{25,}/.test(html),
    (html.match(/AIza[0-9A-Za-z_\-]{0,14}/) || ["ninguna"])[0]);

  const h2 = montar("", { b2quiz_firebase: '{"apiKey":"AIzaFalsa","projectId":"p"}' }, false);
  const btn = h2.registro["btn-ai-config"];
  if (btn && btn.onclick) btn.onclick();
  const modal = (h2.registro["modal-container"] || new El("div")).innerHTML;
  check("el modal recuerda la configuración ya pegada",
    /AIzaFalsa/.test(modal), /AIzaFalsa/.test(modal) ? "se muestra" : "no aparece en el modal");
}

/* C6 · una «corrección» idéntica al original no es una corrección */
{
  const RUIDO = "Xylophonpruefgeraet";   // no aparece ni en el enunciado ni en los Redemittel
  const h = montar("", {}, false);
  h.window.quizState.schreiben_drafts["sergio::schr-b-p66"] =
    "Sehr geehrte Damen und Herren, darum sie sind früher gegangen. Mit freundlichen Grüßen";
  h.window.quizState.schreiben_evals["sergio::schr-b-p66"] = {
    verdict: "BESTANDEN", score_total: 80,
    critical_errors: [
      { original: "darum sie sind", correction: "deshalb sind sie", rule_es: "Verbos", type: "Grammatik" },
      { original: RUIDO, correction: RUIDO, rule_es: "Ruido", type: "Zeichensetzung" },
      { original: "früher gegangen", correction: "früher gegangen ", rule_es: "Espacios", type: "Stil" }
    ]
  };
  abrirSchreiben(h.registro);
  const texto = (h.registro["main"] || new El("div")).texto();
  check("se descartan las correcciones vacías (idénticas o con espacios de más)",
    /Verbos/.test(texto) && !texto.includes(RUIDO) && !/Espacios/.test(texto),
    "real: " + /Verbos/.test(texto) + " · idéntica: " + texto.includes(RUIDO) + " · espacios: " + /Espacios/.test(texto));

  const h2 = montar("", {}, false);
  h2.window.quizState.schreiben_drafts["sergio::schr-b-p66"] = "… unserer zuständigen abteilung geschrieben.";
  h2.window.quizState.schreiben_evals["sergio::schr-b-p66"] = {
    verdict: "BESTANDEN", score_total: 80,
    critical_errors: [
      { original: "zuständigen abteilung", correction: "zuständigen Abteilung", rule_es: "Mayúsculas", type: "Rechtschreibung" }
    ]
  };
  abrirSchreiben(h2.registro);
  const texto2 = (h2.registro["main"] || new El("div")).texto();
  check("una diferencia solo de mayúsculas SÍ se conserva",
    /Mayúsculas/.test(texto2) && /zuständigen abteilung/.test(texto2),
    "regla: " + /Mayúsculas/.test(texto2) + " · original en minúscula: " + /zuständigen abteilung/.test(texto2));
}

/* C3 · evaluación de la pareja recibida por Firestore */
{
  const h = montar("?user=sergio&room=sala-prueba", {}, true);
  abrirSchreiben(h.registro);
  h.empujarSnapshot({
    diana_text: "Sehr geehrte Damen und Herren, hier ist mein Text.",
    diana_words: 8,
    diana_updated_at: Date.now(),
    diana_eval: { verdict: "BESTANDEN", score_total: PAYLOAD },
  });
  const cont = h.registro["schreiben-partner-container"] || new El("div");
  const html = cont.html();
  check("una evaluación de la pareja con payload no inyecta HTML",
    html.length > 0 && !/<img/i.test(html), html.slice(0, 120) || "(contenedor vacío)");
}

/* C5 · evaluación malformada en la tarea propia */
{
  const h = montar("", {}, false);
  h.window.quizState.schreiben_evals = {
    "sergio::schr-b-p66": { verdict: "BESTANDEN", score_total: 88, critical_errors: [null] },
  };
  h.window.quizState.schreiben_drafts = { "sergio::schr-b-p66": "Sehr geehrte Damen und Herren, ein Text." };
  let excepcion = null;
  try { abrirSchreiben(h.registro); } catch (e) { excepcion = e; }
  const main = h.registro["main"] || new El("div");
  check("una evaluación malformada no rompe la pantalla",
    !excepcion && main.children.length > 0 && main.texto().length > 100,
    excepcion ? excepcion.constructor.name + ": " + excepcion.message
              : "nodos en main: " + main.children.length + " | chars: " + main.texto().length);
}

/* S2 · la insignia no miente si la escritura falla */
{
  const h = montar("?user=sergio&room=sala-prueba", {}, true, true);
  abrirSchreiben(h.registro);
  const limpiar = buscar(h.registro["main"], e => /Limpiar texto/.test(e.textContent || ""));
  if (limpiar && limpiar.onclick) limpiar.onclick();
  const badge = (h.registro["cloud-status-indicator"] || new El("div")).html();
  check("si la escritura falla, la insignia lo dice",
    !/Sincronizado en la nube/.test(badge) && /sincroniz/i.test(badge), badge.slice(0, 90));
}

/* S3 · borrador pendiente de subir (y con la clave antigua, ya migrada) */
{
  const h = montar("?user=sergio&room=sala-prueba",
    { "b2quiz.v1": JSON.stringify({ answers: {}, schreiben_drafts: { "schr-b-p66": "texto escrito sin conexión" } }) },
    true, false);
  abrirSchreiben(h.registro);
  h.empujarSnapshot({});   // la nube no tiene nada de Sergio todavía
  const subido = h.escritos.some(p => p.sergio_text === "texto escrito sin conexión");
  check("un borrador escrito sin conexión se sube al abrir la tarea",
    subido, "escrituras: " + JSON.stringify(h.escritos).slice(0, 110));

  const claves = Object.keys(h.window.quizState.schreiben_drafts || {});
  check("un progreso guardado con la clave antigua se migra a la clave con perfil",
    claves.length === 1 && claves[0] === "sergio::schr-b-p66", "claves: " + claves.join(","));
}

/* S9 · el borrador es de cada perfil: cambiar de perfil no mezcla el trabajo */
{
  const h = montar("?user=sergio&room=sala-prueba", {}, false);
  const editor = () => buscar(h.registro["main"], e => e.tagName === "textarea");
  abrirSchreiben(h.registro);
  const ta = editor();
  if (ta && ta.oninput) ta.oninput({ target: { value: "Mein Text als Sergio" } });

  const claves = Object.keys(h.window.quizState.schreiben_drafts || {});
  check("el borrador se guarda con el perfil dentro de la clave",
    claves.length === 1 && claves[0] === "sergio::schr-b-p66", "claves: " + claves.join(","));

  h.window.setUser("diana");
  h.window.setLanguage("es");   // el idioma no debe decidir qué borrador se carga
  abrirSchreiben(h.registro);
  const taDiana = editor();
  check("al pasar al perfil de Diana el editor no trae el texto de Sergio",
    !!taDiana && String(taDiana.value || "") === "",
    "editor de Diana: " + JSON.stringify(String((taDiana && taDiana.value) || "")));

  h.window.setUser("sergio");
  h.window.setLanguage("es");
  abrirSchreiben(h.registro);
  const taVuelta = editor();
  check("al volver al perfil de Sergio su borrador sigue intacto",
    !!taVuelta && taVuelta.value === "Mein Text als Sergio",
    "editor de Sergio: " + JSON.stringify(String((taVuelta && taVuelta.value) || "")));
}

/* S10 · la nube devuelve tu redacción y tu evaluación si este navegador no las tiene */
{
  const h = montar("?user=sergio&room=sala-prueba", {}, true);
  abrirSchreiben(h.registro);
  h.empujarSnapshot({
    sergio_text: "Sehr geehrte Damen und Herren, hier ist mein Text aus der Cloud.",
    sergio_words: 12, sergio_updated_at: Date.now(),
    sergio_eval: { verdict: "BESTANDEN", score_total: 81, critical_errors: [] },
    diana_text: "Text der Partnerin", diana_words: 3, diana_updated_at: Date.now()
  });
  const ta = buscar(h.registro["main"], e => e.tagName === "textarea");
  const claves = Object.keys(h.window.quizState.schreiben_drafts || {});
  check("sin borrador local, la nube rellena el editor",
    !!ta && /aus der Cloud/.test(String(ta.value || "")) && claves[0] === "sergio::schr-b-p66",
    "editor: " + JSON.stringify(String((ta && ta.value) || "").slice(0, 45)) + " | claves: " + claves.join(","));
  const clavesEval = Object.keys(h.window.quizState.schreiben_evals || {});
  check("sin evaluación local, la nube devuelve tu evaluación",
    clavesEval.length === 1 && clavesEval[0] === "sergio::schr-b-p66", "claves: " + clavesEval.join(","));
  check("lo que la nube te devuelve no se le devuelve a la nube (sin eco)",
    h.escritos.length === 0, "escrituras: " + JSON.stringify(h.escritos).slice(0, 90));

  const h2 = montar("?user=sergio&room=sala-prueba",
    { "b2quiz.v1": JSON.stringify({ answers: {}, schreiben_drafts: { "sergio::schr-b-p66": "Mi texto local" } }) },
    true, false);
  abrirSchreiben(h2.registro);
  h2.empujarSnapshot({ sergio_text: "Texto de la nube" });
  const ta2 = buscar(h2.registro["main"], e => e.tagName === "textarea");
  check("con borrador local, la nube no lo pisa",
    !!ta2 && String(ta2.value || "") === "Mi texto local",
    "editor: " + JSON.stringify(String((ta2 && ta2.value) || "")));
}

/* S11 · una copia local vieja no puede subirse encima de una nube más nueva */
{
  const h = montar("?user=sergio&room=sala-prueba",
    { "b2quiz.v1": JSON.stringify({
        answers: {},
        schreiben_drafts: { "sergio::schr-b-p66": "version 1" },
        schreiben_pushed: { "sergio::schr-b-p66": "version 1" }
      }) }, true, false);
  abrirSchreiben(h.registro);
  h.empujarSnapshot({ sergio_text: "version 2 escrita en otro navegador" });
  const ta = buscar(h.registro["main"], e => e.tagName === "textarea");
  check("una copia local sin nada sin enviar se refresca con la de la nube",
    !!ta && String(ta.value || "") === "version 2 escrita en otro navegador",
    "editor: " + JSON.stringify(String((ta && ta.value) || "")));
  check("lo refrescado no se devuelve a la nube (sin eco)",
    h.escritos.length === 0, "escrituras: " + JSON.stringify(h.escritos).slice(0, 90));
}

/* S12 · con ediciones sin enviar, la nube no se impone */
{
  const h = montar("?user=sergio&room=sala-prueba",
    { "b2quiz.v1": JSON.stringify({
        answers: {},
        schreiben_drafts: { "sergio::schr-b-p66": "version 2 local sin enviar" },
        schreiben_pushed: { "sergio::schr-b-p66": "version 1" }
      }) }, true, false);
  abrirSchreiben(h.registro);
  h.empujarSnapshot({ sergio_text: "version 1 de la nube" });
  const ta = buscar(h.registro["main"], e => e.tagName === "textarea");
  check("con ediciones sin enviar, la nube no pisa el borrador local",
    !!ta && String(ta.value || "") === "version 2 local sin enviar",
    "editor: " + JSON.stringify(String((ta && ta.value) || "")));
}

/* S13 · vaciar el texto a propósito no se rellena solo */
{
  const h = montar("?user=sergio&room=sala-prueba",
    { "b2quiz.v1": JSON.stringify({
        answers: {},
        schreiben_drafts: {},
        schreiben_pushed: { "sergio::schr-b-p66": "" }
      }) }, true, false);
  abrirSchreiben(h.registro);
  h.empujarSnapshot({ sergio_text: "texto que se acaba de borrar" });
  const ta = buscar(h.registro["main"], e => e.tagName === "textarea");
  check("un texto vaciado a propósito no se rellena solo desde la nube",
    !!ta && String(ta.value || "") === "",
    "editor: " + JSON.stringify(String((ta && ta.value) || "")));
}

/* S14 · una copia sin registro que ya coincide con la nube queda anotada como
   sincronizada, y a partir de ahí una versión nueva de la nube sí se adopta.
   Es el caso de las copias que llegaron antes de existir esta marca. */
{
  const h = montar("?user=sergio&room=sala-prueba",
    { "b2quiz.v1": JSON.stringify({ answers: {}, schreiben_drafts: { "sergio::schr-b-p66": "version 1" } }) },
    true, false);
  abrirSchreiben(h.registro);
  h.empujarSnapshot({ sergio_text: "version 1" });                       // coinciden: se anota
  h.empujarSnapshot({ sergio_text: "version 2 desde otro navegador" });  // ahora manda la nube
  const ta = buscar(h.registro["main"], e => e.tagName === "textarea");
  check("una copia sin registro que coincide con la nube queda anotada y luego se refresca",
    !!ta && String(ta.value || "") === "version 2 desde otro navegador",
    "editor: " + JSON.stringify(String((ta && ta.value) || "")));
}

/* ---------- informe ---------- */
let malos = 0;
for (const c of checks) {
  console.log((c.ok ? "  OK   " : "  FALLA") + "  " + c.nombre + (c.detalle ? "  → " + c.detalle : ""));
  if (!c.ok) malos++;
}
console.log(`\n${checks.length - malos}/${checks.length} comprobaciones de seguridad superadas`);
process.exit(malos ? 1 : 0);
