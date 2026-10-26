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
    /* Los rotulos de familia son adorno del menu, no entradas del grupo. */
    if (clases(c).includes("nav-group")) continue;
    if (dentro) out.push(c);
  }
  return out;
};
const toggleDe = i => cabeceras()[i].children[0];

/* Se espera una cabecera por sección CON datos, no un número fijo: el menú crece
   cuando se añade una parte del examen (Sprachbausteine, por ejemplo). */
const seccionesConDatos = () => (window.DATA.sections || []).filter(s => (s.variants || []).length > 0).length;

check("hay una cabecera plegable por sección",
      cabeceras().length > 0 && cabeceras().length === seccionesConDatos(),
      `cabeceras: ${cabeceras().length} · secciones con datos: ${seccionesConDatos()}`);
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

/* ---------- familias plegables ---------- */
/* La barra agrupa por examen (LESEN, SPRACHBAUSTEINE, SCHREIBEN, HÖREN,
   SPRECHEN, MODELTEST) y cada cabecera pliega la familia entera. */
const grupos = () => ids.nav.children.filter(c => clases(c).includes("nav-group"));

check("cada familia del examen tiene su cabecera", grupos().length === 6,
      `familias: ${grupos().map(g => g.children[0].textContent).join(", ")}`);

const totalLesen = window.DATA.sections.slice(0, 5)
  .reduce((a, s) => a + (s.variants || []).length, 0);
check("la cabecera de familia cuenta todas sus entradas",
      grupos().length > 0 && Number(grupos()[0].children[1].textContent) === totalLesen,
      `contador: ${grupos()[0] && grupos()[0].children[1].textContent} · entradas: ${totalLesen}`);

const numeroDe = i => cabeceras()[i].children[cabeceras()[i].children.length - 1].textContent;
const numeroAntes = numeroDe(5);

grupos()[0].onclick();
check("plegar una familia esconde sus cabeceras",
      cabeceras().slice(0, 5).every(c => c.hidden) && cabeceras().slice(5).every(c => !c.hidden),
      `visibles tras plegar: ${cabeceras().filter(c => !c.hidden).length}`);
check("las entradas de la familia plegada también se esconden",
      [0, 1, 2, 3, 4].every(i => entradasDe(i).every(e => e.hidden)),
      `visibles: ${[0, 1, 2, 3, 4].reduce((a, i) => a + entradasDe(i).filter(e => !e.hidden).length, 0)}`);
check("la numeración no cambia al plegar una familia",
      numeroDe(5) === numeroAntes && numeroAntes === "06",
      `antes ${numeroAntes} · ahora ${numeroDe(5)}`);

grupos()[0].onclick();
check("volver a pulsar la familia la despliega",
      cabeceras().slice(0, 5).every(c => !c.hidden),
      `visibles: ${cabeceras().filter(c => !c.hidden).length}`);

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

/* ---------- Sprachbausteine: banco de palabras + texto con huecos ---------- */
{
  const idxSb = cabeceras().findIndex(c => /Sprachbausteine Teil 1/i.test(c.children[0].collectText()));
  check("la sección de Sprachbausteine Teil 1 está en el menú", idxSb >= 0,
        `cabeceras: ${cabeceras().length} · encontrada en: ${idxSb}`);
  if (idxSb >= 0) {
    const entradas = entradasDe(idxSb);
    check("el Teil 1 trae sus variantes", entradas.length >= 10, `variantes: ${entradas.length}`);
    if (entradas.length) {
      entradas[0].onclick();
      const texto = ids.main.collectText();
      check("el banco de palabras se pinta con su etiqueta",
            /Wörter/.test(texto), (texto.match(/Wörter[^<]{0,40}/) || ["(sin banco)"])[0]);
      check("el texto del ejercicio se pinta con sus huecos marcados",
            /class="gap"/.test(texto) && /gap-line/.test(texto),
            (texto.match(/class="gap"[\s\S]{0,70}/) || ["(sin huecos)"])[0]);
      const huecos = ["46", "47", "48", "49", "50", "51"].filter(n => new RegExp('gap-n">' + n + "<").test(texto));
      check("los seis huecos están en la hoja", huecos.length === 6, `huecos: ${huecos.join(",")}`);
    }
  }
}

/* ---------- Sprechen Teil 2: mazo de tarjetas y mesa de trabajo ----------
   El Smalltalk no se contesta: se habla. Lo que se comprueba aquí es que el mazo
   entra como UNA entrada de menú, que las dos mitades suman las 104 tarjetas, y
   que la mesa saca cartas al azar sin repetir hasta agotar y guarda las notas. */
{
  const idxSpr = cabeceras().findIndex(c => /Sprechen Teil 2/i.test(c.children[0].collectText()));
  check("la sección de Sprechen Teil 2 está en el menú", idxSpr >= 0,
        `cabeceras: ${cabeceras().length}`);
  if (idxSpr >= 0) {
    const entradas = entradasDe(idxSpr);
    check("el mazo entra como una sola entrada, no como 104", entradas.length === 1,
          `entradas: ${entradas.length}`);
    if (entradas.length) {
      check("la entrada del menú anuncia las 104 tarjetas",
            /104 tarjetas/.test(String(entradas[0]._html)), String(entradas[0]._html).slice(0, 90));
      entradas[0].onclick();

      const tarjetas = () => descendientes(ids.main).filter(e => /\bst-card\b/.test(String(e.className)));
      const ayudas = () => descendientes(ids.main).filter(e => String(e.className) === "st-help");
      const boton = txt => descendientes(ids.main).find(e => e.textContent === txt && /btn|st-toggle/.test(String(e.className)));
      const textoMain = () => ids.main.collectText();

      check("la primera mitad pinta 52 tarjetas", tarjetas().length === 52, `tarjetas: ${tarjetas().length}`);
      check("cada tarjeta lleva su ayuda plegada", ayudas().length === 52, `ayudas: ${ayudas().length}`);
      check("el alemán de la tarjeta va verbatim",
            /Ich finde, wir als Praktikant\*innen/.test(textoMain()));
      check("la ayuda trae español y ruso",
            /Creo que nosotros/.test(textoMain()) && /Я считаю/.test(textoMain()));

      const pills = descendientes(ids.main).filter(e => /^tab-pill( active)?$/.test(String(e.className)));
      check("el mazo se parte en dos pestañas", pills.length === 2, `pestañas: ${pills.length}`);
      if (pills.length === 2) {
        pills[1].onclick();
        check("la segunda mitad trae las otras 52 tarjetas",
              tarjetas().length === 52 && /Nächsten Monat muss ich in eine Wohnung umziehen/.test(textoMain()),
              `tarjetas: ${tarjetas().length}`);
        check("la segunda pestaña no repite las tarjetas de la primera",
              !/Ich finde, wir als Praktikant\*innen/.test(textoMain()),
              "la tarjeta 1 no debería estar en la mitad 53–104");
        pills[0].onclick();
      }

      /* La mesa: apagada por defecto, y al encenderla aparece vacía. */
      check("la mesa de trabajo empieza apagada", !/st-mesa/.test(String(ids.main.collectText())),
            "la pieza de la mesa ya estaba pintada");
      boton("Mesa de trabajo").onclick();
      check("al encender la mesa aparece el panel", /La mesa está vacía/.test(textoMain()));
      check("la mesa cuenta las sacadas", /0 de 104 sacadas/.test(textoMain()));

      /* Sorteo sin repetición. El primer clic crea el mazo; los demás suman. */
      const clave = Object.keys(window.quizState.smalltalk || {})[0] || "";
      check("el estado del mazo se guarda por perfil", /^sergio::/.test(clave), `clave: ${clave}`);
      for (let i = 0; i < 6; i++) {
        const b = boton("Sacar una al azar") || boton("Otra al azar");
        b.onclick();
      }
      const deck = window.quizState.smalltalk[clave] || { drawn: [], notes: {} };
      check("sacar seis veces deja seis cartas distintas",
            deck.drawn.length === 6 && new Set(deck.drawn).size === 6, `sacadas: ${deck.drawn}`);
      check("la mesa muestra la carta que ha salido", tarjetas().some(e => /on-desk/.test(String(e.className))),
            `en la mesa: ${tarjetas().filter(e => /on-desk/.test(String(e.className))).length}`);

      /* Las notas de la carta se guardan sin repintar (repintar perdería el foco). */
      const nota = descendientes(ids.main).find(e => e.tagName === "textarea");
      check("hay un cuadro de notas para la carta de la mesa", !!nota,
            nota ? "encontrado" : "no encontrado");
      if (nota) {
        nota.oninput({ target: { value: "Zwei Ideen: Fahrtkosten und Steuer" } });
        check("la nota se guarda en el progreso del perfil",
              (window.quizState.smalltalk[clave].notes || {})[String(deck.top)] ===
                "Zwei Ideen: Fahrtkosten und Steuer",
              `notas: ${JSON.stringify(window.quizState.smalltalk[clave].notes).slice(0, 60)}`);
      }

      /* Devolver: la carta vuelve a la baraja, así que la cuenta baja. */
      boton("Devolver a la baraja").onclick();
      check("devolver la carta la quita de la mesa y de lo visto",
            window.quizState.smalltalk[clave].top === null &&
            window.quizState.smalltalk[clave].drawn.length === 5,
            `top: ${window.quizState.smalltalk[clave].top} · sacadas: ${window.quizState.smalltalk[clave].drawn.length}`);

      /* Mazo agotado: el botón cambia a barajar, no a sacar otra. */
      const st = window.quizState.smalltalk[clave];
      st.drawn = []; for (let n = 1; n <= 104; n++) st.drawn.push(n);
      st.top = null;
      descendientes(ids.main).filter(e => /^tab-pill( active)?$/.test(String(e.className)))[0].onclick();
      check("con el mazo agotado la mesa avisa y ofrece barajar",
            /Mazo agotado/.test(textoMain()) && !!boton("Barajar de nuevo"),
            (textoMain().match(/Mazo agotado[^<]{0,40}/) || ["(sin aviso)"])[0]);
    }
  }
}

/* ---------- Sprechen Teil 3: una página por situación ----------
   Las 67 son entradas separadas del menú. En cada página se ven el alemán y
   los Stichpunkte; la ayuda ES/RU y los ejemplos quedan plegados tras «Ver». */
{
  const idxSit = cabeceras().findIndex(c => /Sprechen Teil 3/i.test(c.children[0].collectText()));
  check("la sección de Sprechen Teil 3 está en el menú", idxSit >= 0,
        `cabeceras: ${cabeceras().length}`);
  if (idxSit >= 0) {
    const entradas = entradasDe(idxSit);
    const primera = entradas[0], ultima = entradas[entradas.length - 1];
    check("cada situación entra como una entrada separada",
          entradas.length === 67, `entradas: ${entradas.length}`);
    check("la primera entrada lleva su número y su título",
          !!primera && /1 · Würmer im Mehl/.test(String(primera._html)),
          primera ? String(primera._html).slice(0, 100) : "sin entradas");
    check("la última entrada es la 67",
          !!ultima && /67 · Kantine/.test(String(ultima._html)),
          ultima ? String(ultima._html).slice(0, 100) : "sin entradas");

    if (primera) {
      primera.onclick();
      const textoMain = () => ids.main.collectText();
      const detalles = descendientes(ids.main).filter(e => String(e.className) === "sit-help");

      check("la página muestra una sola situación, no la rejilla",
            /Würmer im Mehl/.test(textoMain()) && !/67 situaciones/.test(textoMain()));
      check("la descripción alemana va a la vista",
            /Würmer\/ kleine Tierchen im Mehl/.test(textoMain()));
      check("los Stichpunkte alemanes van a la vista",
            /Chef: Wie kontaktieren\?/.test(textoMain()));
      check("hay dos bloques plegados: ayuda y ejemplos",
            detalles.length === 2 && detalles.every(d => !d.open),
            `bloques: ${detalles.length} · abiertos: ${detalles.filter(d => d.open).length}`);
      check("el primer bloque se llama «Ver ayuda» y el segundo «Ver ejemplos»",
            detalles.length === 2 &&
            /Ver ayuda \(ES · RU\)/.test(detalles[0].children[0].textContent) &&
            /Ver ejemplos en alemán/.test(detalles[1].children[0].textContent),
            detalles.map(d => d.children[0].textContent).join(" · "));
      check("la ayuda plegada trae español y ruso",
            detalles.length === 2 &&
            /Trabajas en una pastelería/.test(detalles[0].collectText()) &&
            /Вы работаете в кондитерской/.test(detalles[0].collectText()));
      check("la ayuda plegada traduce los Stichpunkte",
            detalles.length === 2 &&
            /Jefe: ¿cómo contactarlo\?/.test(detalles[0].collectText()) &&
            /Шеф: как с ним связаться/.test(detalles[0].collectText()));
      check("los ejemplos plegados están en alemán",
            detalles.length === 2 &&
            /Ich rufe den Chef sofort an/.test(detalles[1].collectText()));

      const bSiguiente = descendientes(ids.main).find(e => e.textContent === "Siguiente");
      check("hay navegación a la situación siguiente", !!bSiguiente,
            bSiguiente ? "botón encontrado" : "sin botón");
      if (bSiguiente) {
        bSiguiente.onclick();
        check("pasar a la siguiente cambia de situación y de página",
              /Kaputter Backofen/.test(textoMain()) &&
              /Der Backofen ist kaputt/.test(textoMain()) &&
              !/Würmer im Mehl/.test(textoMain()),
              textoMain().slice(0, 120));
      }
      check("no se abre ninguna ventana modal",
            String(ids["modal-container"].innerHTML) === "" &&
            ids["modal-container"].children.length === 0);
    }
  }
}

/* ---------- Modeltests: Hören sin clave y la x del Lesen T3 ----------
   La zona nueva mete 12 bloques por test. Hören no tiene audio ni clave: se
   puede elegir, pero no se corrige ni cuenta en las estadísticas. Lesen T3
   añade una x para la pregunta que no tiene consejo. */
{
  const idxMT = cabeceras().findIndex(c => /Modeltest 11/i.test(c.children[0].collectText()));
  check("la sección Modeltest 11 está en el menú", idxMT >= 0,
        `cabeceras: ${cabeceras().length}`);
  if (idxMT >= 0) {
    const entradas = entradasDe(idxMT);
    check("el Modeltest 11 trae sus 12 bloques", entradas.length === 12,
          `entradas: ${entradas.length}`);
    const porRotulo = (txt) => entradas.find(e => String(e._html).indexOf(txt) !== -1);

    const entradaH1 = porRotulo("Hören Teil 1");
    check("Hören Teil 1 está entre los bloques", !!entradaH1,
          entradaH1 ? String(entradaH1._html).slice(0, 80) : "no encontrado");
    if (entradaH1) {
      entradaH1.onclick();
      const textoH1 = () => ids.main.collectText();
      check("Hören avisa de que no hay clave", /sin audio ni clave/i.test(textoH1()),
            textoH1().slice(0, 110));
      const opciones = descendientes(ids.main).filter(e => /\bopt\b/.test(String(e.className)));
      check("Hören pinta sus opciones", opciones.length > 0, `opciones: ${opciones.length}`);
      if (opciones.length) {
        const statsAntes = ids.stats.innerHTML;
        opciones[0].onclick();
        const marcadas = descendientes(ids.main)
          .filter(e => /\b(correct|wrong)\b/.test(String(e.className)));
        check("elegir en Hören no marca acierto ni fallo", marcadas.length === 0,
              `marcadas: ${marcadas.length}`);
        const elegidas = descendientes(ids.main)
          .filter(e => /\bchosen\b/.test(String(e.className)));
        check("la opción elegida se marca sin veredicto", elegidas.length === 1,
              `elegidas: ${elegidas.length}`);
        check("elegir en Hören no cuenta como respondida", ids.stats.innerHTML === statsAntes,
              ids.stats.innerHTML === statsAntes ? "sin cambios" : "las estadísticas cambiaron");
      }
    }

    const entradaT3 = porRotulo("Lesen Teil 3");
    check("Lesen Teil 3 está entre los bloques", !!entradaT3,
          entradaT3 ? String(entradaT3._html).slice(0, 80) : "no encontrado");
    if (entradaT3) {
      entradaT3.onclick();
      const preguntas = descendientes(ids.main).filter(e => String(e.className) === "q");
      const qJulia = preguntas.find(q => /Julia/.test(q.collectText()));
      const botonX = qJulia
        ? descendientes(qJulia).find(e => String(e.textContent) === "x")
        : null;
      check("Lesen T3 ofrece la x para la pregunta sin consejo", !!botonX,
            botonX ? "botón x encontrado" : "sin botón x");
      if (botonX) {
        botonX.onclick();
        check("la x se guarda como respuesta",
              window.quizState.answers["mt11-lesen-t3#1"] === "x",
              `guardado: ${window.quizState.answers["mt11-lesen-t3#1"]}`);
        check("la x se corrige como acierto",
              /Correcto/.test(ids.main.collectText()),
              ids.main.collectText().slice(0, 120));
      }
    }

    /* Los siete tests, no solo el 11, tienen que estar y traer sus 12 bloques. */
    const indices = [11, 12, 13, 14, 15, 16, 17].map(n =>
      cabeceras().findIndex(c => new RegExp("Modeltest " + n + "\\b").test(c.children[0].collectText())));
    check("los siete Modeltests están en el menú", indices.every(i => i >= 0),
          `índices: ${indices.join(",")}`);
    check("cada Modeltest trae sus 12 bloques",
          indices.every(i => i >= 0 && entradasDe(i).length === 12),
          indices.map(i => i >= 0 ? entradasDe(i).length : "?").join(","));
  }
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
    /* La clave lleva el perfil delante: cada perfil tiene su propia evaluación. */
    "sergio::schr-b-p66": {
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

/* ---------- banda del criterio I según los Leitpunkte cubiertos ---------- */
/* El README decía «no pasa de C si falta un Leitpunkt» y el código permitía B.
   Estas comprobaciones fijan el mapeo que aplica la app de verdad: un point
   menos deja el criterio en B, dos en C y tres o más en D. */
try {
  const conLeitpunkte = (cubiertos) => ({
    grade: "A",
    feedback: "",
    leitpunkte_check: Array.from({ length: 4 }, (_, i) =>
      ({ point: "Leitpunkt " + (i + 1), covered: i < cubiertos, comment: "" }))
  });
  const criterioAlto = () => ({ grade: "A", feedback: "", leitpunkte_check: [] });

  const mapa = [
    ["cuatro Leitpunkte cubiertos mantienen el criterio I en A", 4, "A", 34],
    ["un Leitpunkt menos deja el criterio I en B", 3, "B", 26],
    ["dos Leitpunkte menos dejan el criterio I en C", 2, "C", 13],
    ["tres Leitpunkte menos ponen el criterio I en D", 1, "D", 0]
  ];
  mapa.forEach(([nombre, cubiertos, banda, puntos]) => {
    const res = window.puntuarCriterios(conLeitpunkte(cubiertos), criterioAlto(), criterioAlto(), criterioAlto(), 200, 4);
    const uno = res.criteria.aufgabenbewaeltigung;
    check(nombre, uno.grade === banda && uno.score === puntos, `banda=${uno.grade} puntos=${uno.score}`);
  });

  const sinLista = window.puntuarCriterios(criterioAlto(), criterioAlto(), criterioAlto(), criterioAlto(), 200, 4);
  check("sin lista de Leitpunkte no se aplica tope al criterio I",
        sinLista.criteria.aufgabenbewaeltigung.grade === "A",
        "banda=" + sinLista.criteria.aufgabenbewaeltigung.grade);

  const corto = window.puntuarCriterios(conLeitpunkte(4), criterioAlto(), criterioAlto(), criterioAlto(), 120, 4);
  check("menos de 150 palabras limitan el criterio I a B",
        corto.criteria.aufgabenbewaeltigung.grade === "B",
        "banda=" + corto.criteria.aufgabenbewaeltigung.grade);
} catch (e) {
  errors.push("excepción al comprobar la banda del criterio I: " + e.message);
}

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

/* ---------- corrector: fusión de errores y filtro de citas inventadas ---------- */
/* El caso que lo destapó: una tarjeta citaba «daß diese Person» y el alumno había
   escrito «dass». Ahora la cita se valida contra el texto antes de mostrarse, y
   los errores de las tres pasadas se unen en vez de tirarse. */
if (typeof window.fusionarErrores === "function" && typeof window.aplicarCorrecciones === "function") {
  const texto = "Liebe Kolleginnen und Kollegen,\n\nIch möchte mich beteiligen. Ich fühle das gut ist.";
  const pasada1 = [{ original: "Ich möchte", correction: "ich möchte", change: "solo mayúscula: I → i", rule_es: "Tras la coma de la fórmula de saludo se sigue en minúscula.", type: "Rechtschreibung" }];
  const pasada2 = [
    { original: "Ich fühle das gut ist.", correction: "Ich finde, dass das gut ist.", change: "fühle das gut → finde, dass das gut", rule_es: "Se usa finden; tras dass va el verbo al final.", type: "Grammatik" },
    { original: "Ich möchte", correction: "ich möchte", change: "duplicado", rule_es: "…", type: "Rechtschreibung" }
  ];
  const caza = [
    { original: "daß diese Person", correction: "dass diese Person", change: "daß → dass", rule_es: "dass con doble s.", type: "Rechtschreibung" },
    { original: "beteiligen", correction: "beteiligen", change: "no cambia nada", rule_es: "…", type: "Grammatik" }
  ];
  const fusion = window.fusionarErrores([pasada1, pasada2, caza], texto);
  check("el corrector une los errores de varias pasadas sin duplicados", fusion.length === 2, `fusionados: ${fusion.length}`);
  check("el corrector descarta la cita que no está en el texto (caso «daß»)", !fusion.some(e => /daß/.test(e.original)));
  const corregido = window.aplicarCorrecciones(texto, fusion);
  check("la versión corregida aplica las correcciones sobre el texto del alumno",
        /^Liebe Kolleginnen und Kollegen,\n\nich möchte mich beteiligen\. Ich finde, dass das gut ist\.$/.test(corregido),
        corregido.slice(0, 90));

  const combinado = window.combinarPasadas([{
    verdict: "BESTANDEN", score_total: 80, word_count: 10,
    criteria: {
      aufgabenbewaeltigung: { grade: "A", score: 34, leitpunkte_check: [], feedback: "" },
      angemessenheit: { grade: "A", score: 22, feedback: "" },
      korrektheit: { grade: "B", score: 17, feedback: "" },
      repertoire: { grade: "B", score: 17, feedback: "" }
    },
    critical_errors: pasada1, strengths: [], areas_for_improvement: [],
    corrected_version: "Liebe Kolleginnen und Kollegen,\n\nich möchte mich beteiligen. Ich fühle das gut ist."
  }], texto, 4, [pasada2, caza]);
  check("la evaluación combina los errores de todas las pasadas", (combinado.critical_errors || []).length === 2,
        `errores: ${(combinado.critical_errors || []).length}`);
  check("el texto corregido incluye las correcciones que solo trajo la caza de errores",
        /Ich finde, dass das gut ist\./.test(combinado.corrected_version || ""),
        String(combinado.corrected_version || "").slice(0, 80));
}

/* ---------- informe ---------- */
let bad = 0;
for (const c of checks) {
  console.log((c.ok ? "  OK   " : "  FALLA") + "  " + c.name + (c.detail ? "  → " + c.detail : ""));
  if (!c.ok) bad++;
}
console.log(`\n${checks.length - bad}/${checks.length} comprobaciones superadas`);
process.exit(bad ? 1 : 0);

