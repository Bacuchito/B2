/* Prueba de humo del visor: ejecuta el script del HTML con un DOM simulado
   para detectar errores de ejecución que un simple chequeo de sintaxis no ve.

   Uso: node smoke_test.js <B2_quiz.html>
*/
const fs = require("fs");

const file = process.argv[2];
const html = fs.readFileSync(file, "utf8");
/* El script de la app es el bloque <script> inline más largo (hay un script
   minúsculo en el <head> que aplica el tema antes del primer pintado). */
const bloques = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
const script = bloques.reduce((a, b) => (b.length > a.length ? b : a), "");

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
["nav", "main", "stats", "reset", "doubt", "btn-ai-config", "modal-container", "header-title", "lang-btn-es", "lang-btn-ru", "user-btn-sergio", "user-btn-diana"].forEach(id => { ids[id] = new El("div"); });

const document = {
  getElementById: id => ids[id] || (ids[id] = new El("div")),
  createElement: tag => new El(tag),
  documentElement: new El("html"),
};

const store = {};
const localStorage = {
  getItem: k => (k in store ? store[k] : null),
  setItem: (k, v) => { store[k] = String(v); },
  removeItem: k => { delete store[k]; },
  clear: () => { Object.keys(store).forEach(k => delete store[k]); },
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

/* ---------- menú plegable: acordeón por sección ---------- */
/* El menú tenía 140 entradas seguidas: para llegar a Schreiben había que bajar
   toda la lista. Ahora cada cabecera pliega su grupo y solo el grupo donde
   estás aparece desplegado. */
const clases = el => String(el.className).split(/\s+/);
const cabeceras = () => ids.nav.children.filter(c => clases(c).includes("sec"));
const abiertas = () => cabeceras().filter(c => clases(c).includes("open"));
/* Entradas que cuelgan de la cabecera i, en el orden del DOM. */
const entradasDe = i => {
  const out = [];
  let dentro = false;
  for (const c of ids.nav.children) {
    if (clases(c).includes("sec")) { dentro = c === cabeceras()[i]; continue; }
    if (dentro) out.push(c);
  }
  return out;
};
const toggleDe = i => cabeceras()[i].children[0];

check("hay una cabecera plegable por sección", cabeceras().length === 7,
      `cabeceras: ${cabeceras().length}`);
check("al abrir la app solo está desplegado el grupo donde estás",
      abiertas().length === 1, `desplegadas: ${abiertas().length}`);
check("el grupo desplegado deja ver sus entradas",
      entradasDe(0).length > 0 && entradasDe(0).every(e => !e.hidden),
      `visibles: ${entradasDe(0).filter(e => !e.hidden).length}/${entradasDe(0).length}`);
check("los grupos plegados esconden sus entradas sin borrarlas del DOM",
      entradasDe(1).length > 0 && entradasDe(1).every(e => e.hidden),
      `escondidas: ${entradasDe(1).filter(e => e.hidden).length}/${entradasDe(1).length}`);
check("la cabecera cuenta las entradas que esconde",
      Number(cabeceras()[1].children[0].children[1].textContent) === entradasDe(1).length,
      `contador: ${cabeceras()[1].children[0].children[1].textContent} · entradas: ${entradasDe(1).length}`);

toggleDe(1).onclick();
check("pulsar otra cabecera abre ese grupo y cierra el anterior",
      abiertas().length === 1 && abiertas()[0] === cabeceras()[1] &&
      entradasDe(1).every(e => !e.hidden) && entradasDe(0).every(e => e.hidden),
      `desplegadas: ${abiertas().length} · visibles en el grupo 2: ${entradasDe(1).filter(e => !e.hidden).length}`);

toggleDe(1).onclick();
check("volver a pulsar la cabecera abierta pliega el menú entero",
      abiertas().length === 0 && cabeceras().every((_, i) => entradasDe(i).every(e => e.hidden)),
      `desplegadas: ${abiertas().length}`);

const stats = ids.stats.innerHTML;
check("las estadísticas se calcularon", /respondidas/.test(stats), stats.slice(0, 90));

const mainText = ids.main.collectText();
check("el enunciado de Lesen se pintó", /Moutasem|fragt sich|Firmenausweis|Text|Lesen/i.test(mainText),
      mainText.slice(0, 120));
check("los anuncios se pintaron", /Anzeigen|Auf ins Abenteuer|Umgangsformen/i.test(mainText));
check("las opciones de respuesta se pintaron", /letters|opt|Falsch|Richtig|[a-h]\)/i.test(mainText));

/* ---------- el panel de anuncios no puede ser la solución ---------- */
function descendientes(el, out) {
  out = out || [];
  for (const c of el.children) { out.push(c); descendientes(c, out); }
  return out;
}
const letraDelAnuncio = a => (String(a._html).match(/class="k">([a-z])\)/) || [])[1];
const esUsado = a => String(a.className).split(/\s+/).includes("used");
const anunciosActuales = () => descendientes(ids.main).filter(e => /^ad\s+(used|unused)$/.test(e.className));

const anunciosIniciales = anunciosActuales();
const usadosIniciales = anunciosIniciales.filter(esUsado);
check("el panel de anuncios existe", anunciosIniciales.length > 0,
      `anuncios pintados: ${anunciosIniciales.length}`);
/* El fallo original: «used» salía de itemAnswerLetter (la clave), así que los 5
   anuncios correctos llevaban ✓ antes de responder nada. */
check("ningún anuncio sale marcado antes de responder (no revela la clave)",
      anunciosIniciales.length > 0 && usadosIniciales.length === 0,
      `marcados con ✓ sin responder: ${usadosIniciales.map(letraDelAnuncio).join(",") || "ninguno"}`);
check("el resumen del panel cuenta tus asignaciones, no las de la clave",
      /0 asignadas/.test(mainText),
      (mainText.match(/Anzeigen[^<]{0,60}/) || ["(sin resumen)"])[0]);
/* Mesa de examen a dos columnas: la clase la pone el render solo si hay
   referencia (anuncios o texto) que poner al lado; el CSS la usa a ≥1500px. */
check("la mesa de examen se activa cuando hay anuncios que poner al lado",
      ids.main.className === "desk", `clase de main: «${ids.main.className}»`);

/* ---------- simulación de clic en preguntas ---------- */
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

  /* Ahora sí: el ✓ tiene que marcar lo que ha pulsado el usuario, y solo eso. */
  const asignada = String(clicables[0].textContent || "").toLowerCase();
  const marcados = anunciosActuales().filter(esUsado);
  check("tras responder se marca el anuncio asignado (y solo ese)",
        marcados.length === 1 && letraDelAnuncio(marcados[0]) === asignada,
        `letra pulsada: ${asignada} · marcados: ${marcados.map(letraDelAnuncio).join(",") || "ninguno"}`);
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
  check("al cambiar a una variante sin referencia se vuelve a una columna",
        ids.main.className === "", `clase de main: «${ids.main.className}»`);
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
      student_text: "Sehr geehrte Damen und Herren,\nIch danke Sie für Ihren Hinweis und möchte mich entschuldigen.",
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
check("los resultados de evaluación se pintan correctamente", /BESTANDEN|Aufgabenbewältigung/i.test(evalText), evalText.match(/BESTANDEN[^<]*/i) ? "insignia BESTANDEN presente" : "");
check("el texto del alumno anotado con errores está presente", /Tu texto con análisis|Ich danke Sie/i.test(evalText));
check("la regla gramatical y corrección interactiva se muestran", /Danken rige dativo|Ich danke Ihnen/i.test(evalText));

/* ---------- guardado de la clave de IA ---------- */
/* El síntoma que reportó Sergio: pegaba la clave, guardaba, y no se quedaba.
   Aquí se comprueba la ida y vuelta real contra el almacenamiento, el estado
   que ve el usuario y que los campos no inviten al gestor de contraseñas. */
if (typeof window.saveAIConfig === "function") {
  const previo = window.getAIConfig();
  const clave = "sk-prueba-1234";
  const cfg = Object.assign({}, previo, {
    provider: "openai_compatible", customKey: clave,
    customEndpoint: "https://api.deepseek.com", customModel: "deepseek-chat"
  });
  const guardado = window.saveAIConfig(cfg);
  const leido = window.getAIConfig();
  check("guardar y releer la clave de IA conserva la clave",
    guardado === true && leido.customKey === clave && leido.provider === "openai_compatible",
    `guardado=${guardado} proveedor=${leido.provider} clave=${leido.customKey}`);

  check("aiKeyOf devuelve la clave del proveedor elegido y ninguna en Ollama",
    window.aiKeyOf({ provider: "gemini", geminiKey: "g" }) === "g" &&
    window.aiKeyOf({ provider: "openai_compatible", customKey: "c" }) === "c" &&
    window.aiKeyOf({ provider: "ollama" }) === "");

  check("la clave se enmascara dejando los cuatro últimos",
    window.maskKey("sk-abcdef1234") === "••••••1234" && window.maskKey("") === "",
    window.maskKey("sk-abcdef1234"));

  check("el estado del modal dice si hay clave guardada o no",
    /clave guardada/.test(window.aiStatusText({ provider: "gemini", geminiKey: "AIzaSy1234" })) &&
    /sin clave/.test(window.aiStatusText({ provider: "gemini", geminiKey: "" })),
    window.aiStatusText({ provider: "gemini", geminiKey: "AIzaSy1234" }));

  const estadoGuardado = window.storageOk();
  check("el navegador deja guardar ajustes (si no, el modal lo avisaría)",
    estadoGuardado === true, `storageOk=${estadoGuardado}`);

  if (aiConfigBtn && typeof aiConfigBtn.onclick === "function") {
    try { aiConfigBtn.onclick(); } catch (e) { errors.push("excepción al abrir el modal de IA: " + e.message); }
    const modalHtml = ids["modal-container"].innerHTML;
    check("los campos de clave se libran del gestor de contraseñas del navegador",
      /id="cfg-gemini-key"[^>]*autocomplete="new-password"/.test(modalHtml) &&
      /id="cfg-custom-key"[^>]*autocomplete="new-password"/.test(modalHtml),
      "autocomplete=new-password presente");
    check("el modal muestra el estado del guardado y el botón para ver la clave",
      /id="ai-status-text"/.test(modalHtml) && /id="btn-reveal-keys"/.test(modalHtml));
    check("el modal recuerda la clave guardada en el campo",
      /id="cfg-custom-key"[^>]*value="sk-prueba-1234"/.test(modalHtml));
  }

  check("el estado del modal incluye si el navegador deja guardar",
    /se puede guardar/.test(window.aiStatusText({ provider: "gemini", geminiKey: "AIzaSy1" })),
    window.aiStatusText({ provider: "gemini", geminiKey: "AIzaSy1" }));

  check("un fallo de red se traduce a un mensaje entendible",
    /no he podido llegar al servidor/.test(window.errorDeRed(new TypeError("Failed to fetch"))) &&
    window.errorDeRed(new Error("HTTP 401")) === "HTTP 401",
    window.errorDeRed(new TypeError("Failed to fetch")).slice(0, 60));

  /* Si el navegador pierde lo guardado, la clave debe seguir viva en memoria
     durante la sesión (antes desaparecía sin más). */
  const enMemoria = window.getAIConfig().customKey;
  localStorage.removeItem("b2quiz.ai_config");
  check("la clave sobrevive en memoria aunque el almacenamiento se pierda",
    enMemoria === clave && window.getAIConfig().customKey === clave,
    `antes=${enMemoria} despues=${window.getAIConfig().customKey}`);

  window.saveAIConfig(previo);
}

/* ---------- comprobación del sistema bilingüe (Ruso y Español) ---------- */
if (typeof window.setLanguage === "function") {
  try {
    window.setLanguage("ru");
  } catch (e) {
    errors.push("excepción al cambiar idioma a ruso: " + e.message);
  }
  check("el cambio a ruso se ejecuta correctamente", window.getLang && window.getLang() === "ru", `idioma actual: ${window.getLang ? window.getLang() : "desconocido"}`);
  
  const statsRu = ids.stats.innerHTML;
  check("las estadísticas cambian a ruso", /отвечено|верно|сомнительных/i.test(statsRu), statsRu.slice(0, 90));

  const ruMainText = ids.main.collectText();
  check("el panel de Schreiben y evaluación se actualizan a ruso", /Рабочая ситуация|Обязательные пункты плана|Текст с анализом/i.test(ruMainText), ruMainText.slice(0, 100));
  check("el veredicto de evaluación muestra сдано en ruso", /СДАНО/i.test(ruMainText));
  check("la leyenda de tipos de error se muestra en ruso", /Грамматика \/ Синтаксис/i.test(ruMainText));

  /* Todo lo que sale en pantalla tiene que existir en los dos idiomas: los
     rótulos del PDF, los avisos del extractor y el diccionario de la interfaz. */
  if (window.I18N && window.I18N.es && window.I18N.ru) {
    const faltanRu = Object.keys(window.I18N.es).filter(k => window.I18N.ru[k] === undefined);
    const faltanEs = Object.keys(window.I18N.ru).filter(k => window.I18N.es[k] === undefined);
    check("el diccionario ruso cubre todas las claves del español", faltanRu.length === 0, "faltan: " + faltanRu.join(", "));
    check("el diccionario español cubre todas las claves del ruso", faltanEs.length === 0, "faltan: " + faltanEs.join(", "));
  }
  if (typeof window.localizeLabel === "function") {
    const l1 = window.localizeLabel("Variante 2 (test 140321, 140301)");
    const l2 = window.localizeLabel("Beschwerde – Variante 1 (Putzdienst)");
    const l3 = window.localizeLabel("Text 2 – Variante 3 (alte Fassung bis 07.2024)");
    check("los rótulos traducen el andamiaje y respetan los nombres alemanes",
      l1 === "Вариант 2 (тест 140321, 140301)" &&
      l2 === "Beschwerde – Вариант 1 (Putzdienst)" &&
      l3 === "Текст 2 – Вариант 3 (alte Fassung bis 07.2024)",
      `${l1} · ${l2} · ${l3}`);
  }
  if (typeof window.localizeSection === "function") {
    check("las partes del examen llevan glosa rusa en el menú",
      window.localizeSection("Lesen Teil 1") === "Lesen Teil 1 · Чтение 1" &&
      window.localizeSection("Schreiben: Forumsbeitrag") === "Schreiben: Forumsbeitrag · Письмо: форум",
      window.localizeSection("Lesen Teil 1"));
  }
  if (typeof window.noteOf === "function") {
    check("el aviso ruso tiene prioridad y sin él se cae al español",
      window.noteOf({ note: "español", note_ru: "русский" }) === "русский" &&
      window.noteOf({ note: "español" }) === "español",
      window.noteOf({ note: "español", note_ru: "русский" }));
  }
  if (typeof window.explainOf === "function") {
    check("la explicación rusa tiene prioridad y sin ella se cae al español",
      window.explainOf({ explain: "español", explain_ru: "русский" }) === "русский" &&
      window.explainOf({ explain: "español" }) === "español",
      window.explainOf({ explain: "español", explain_ru: "русский" }));
  }
  if (window.DATA && Array.isArray(window.DATA.sections)) {
    const conAviso = [];
    const sinRuso = [];
    window.DATA.sections.forEach(s => (s.variants || []).forEach(v => {
      if (v.note) { conAviso.push(v.id); if (!v.note_ru) sinRuso.push(v.id); }
    }));
    check("cada aviso del extractor tiene su versión rusa",
      conAviso.length > 0 && sinRuso.length === 0,
      `${conAviso.length} avisos, sin ruso: ${sinRuso.slice(0, 4).join(", ")}`);

    const conExplain = [];
    const explainSinRuso = [];
    window.DATA.sections.forEach(s => (s.variants || []).forEach(v => {
      (v.items || []).forEach(it => {
        if (it.explain) {
          conExplain.push(v.id);
          if (!it.explain_ru) explainSinRuso.push(`${v.id}#${it.n}`);
        }
      });
    }));
    check("cada explicación de respuesta tiene su versión rusa",
      conExplain.length > 0 && explainSinRuso.length === 0,
      `${conExplain.length} explicaciones, sin ruso: ${explainSinRuso.slice(0, 4).join(", ")}`);

    /* Integración real: abrir una variante con aviso y leer lo que se pinta. */
    let objetivo = null;
    window.DATA.sections.forEach(s => (s.variants || []).forEach(v => {
      if (!objetivo && v.note && v.note_ru && v.kind !== "schreiben") objetivo = v;
    }));
    if (objetivo) {
      const etiqueta = window.localizeLabel ? window.localizeLabel(objetivo.label) : objetivo.label;
      const boton = todas.find(el => el.tagName === "button" &&
        typeof el.innerHTML === "string" && el.innerHTML.indexOf(etiqueta.slice(0, 18)) !== -1);
      if (boton && typeof boton.onclick === "function") {
        boton.onclick();
        const texto = ids.main.collectText();
        check("al abrir una variante en ruso el aviso sale traducido",
          texto.indexOf(objetivo.note_ru.slice(0, 30)) !== -1 &&
          texto.indexOf(objetivo.note.slice(0, 30)) === -1,
          `${objetivo.id}: ${texto.slice(0, 70)}`);
      } else {
        check("al abrir una variante en ruso el aviso sale traducido", false, "no encontré el botón del menú");
      }
    }
  }

  // Abrir modal en ruso
  if (aiConfigBtn && typeof aiConfigBtn.onclick === "function") {
    try {
      aiConfigBtn.onclick();
    } catch(e) {
      errors.push("excepción al abrir modal de IA en ruso: " + e.message);
    }
    const modalRu = ids["modal-container"].collectText();
    check("el modal de IA se muestra completamente en ruso", /Настройка искусственного интеллекта|Провайдер ИИ|Сохранить изменения/i.test(modalRu));
  }

  // Regresar a español
  try {
    window.setLanguage("es");
  } catch(e) {
    errors.push("excepción al regresar a español: " + e.message);
  }
  check("el cambio de vuelta a español funciona", window.getLang && window.getLang() === "es", `idioma actual: ${window.getLang ? window.getLang() : "desconocido"}`);

  /* ---------- comprobaciones de perfil de usuario (Sergio & Diana) ---------- */
  const btnUserSergio = ids["user-btn-sergio"];
  const btnUserDiana = ids["user-btn-diana"];
  check("los botones de perfil Sergio y Diana existen", btnUserSergio && btnUserDiana);

  if (btnUserDiana && typeof btnUserDiana.onclick === "function") {
    btnUserDiana.onclick();
    check("al seleccionar Diana el perfil pasa a diana", window.getUser && window.getUser() === "diana", `usuario: ${window.getUser ? window.getUser() : "desconocido"}`);
    check("al seleccionar Diana el idioma cambia automáticamente a ruso", window.getLang && window.getLang() === "ru", `idioma: ${window.getLang ? window.getLang() : "desconocido"}`);
  }

  if (btnUserSergio && typeof btnUserSergio.onclick === "function") {
    btnUserSergio.onclick();
    check("al seleccionar Sergio el perfil pasa a sergio", window.getUser && window.getUser() === "sergio", `usuario: ${window.getUser ? window.getUser() : "desconocido"}`);
    check("al seleccionar Sergio el idioma cambia automáticamente a español", window.getLang && window.getLang() === "es", `idioma: ${window.getLang ? window.getLang() : "desconocido"}`);
  }

  // Comprobar pestañas de redacción comparativa en Schreiben
  if (schrBtn && typeof schrBtn.onclick === "function") {
    schrBtn.onclick();
    const schreibenDomText = ids.main.collectText();
    check("las pestañas de mi redacción y redacción de la pareja existen", /Mi redacción|Redacción de Diana|Redacción de Sergio/i.test(schreibenDomText));
    check("el indicador de estado en la nube está presente", /Sincronizado en la nube|Modo local/i.test(schreibenDomText));
  }
}

/* ---------- informe ---------- */
let bad = 0;
for (const c of checks) {
  console.log((c.ok ? "  OK   " : "  FALLA") + "  " + c.name + (c.detail ? "  → " + c.detail : ""));
  if (!c.ok) bad++;
}
console.log(`\n${checks.length - bad}/${checks.length} comprobaciones superadas`);
process.exit(bad ? 1 : 0);
