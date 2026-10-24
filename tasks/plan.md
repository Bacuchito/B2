# Rediseño visual — B2 Beruf

Rama: `rediseno` (local, sin remoto). Base: `personal` en `9ca1f56`.

Mundo elegido por Sergio: **Lesesaal**. Verde botella, papel marfil, latón y DIN.
Sustituye al mundo «taller nocturno» (carbón, azul y halos).

## Contrato de dirección

- **THESIS:** una clave de respuestas presentada como la hoja de un examen impreso.
  Lo que se rechaza es el panel de administración oscuro con tarjetas y sombras.
- **OWN-WORLD:** papel marfil (`--bg`), tinta casi negra, banda verde botella
  (`--panel`), filetes de 1 px, radios 0, cero sombras. DIN para rótulos y números;
  Palatino para el texto que se lee.
- **STORY:** el visitante entiende en un vistazo que esto es un examen alemán serio,
  con su clave y su nivel de duda, y empieza a responder sin aprender nada nuevo.
- **FIRST VIEWPORT:** banda verde con perfiles y contadores; barra de progreso de
  cinco casillas; navegación numerada a la izquierda; hoja blanca a la derecha con
  la tarea en Palatino y las opciones en celdas a–h.
- **FORM:** sistema impreso alemán (Kursbuch, formulario oficial), posición 1 de 7.
- **FINISH:** el build termina con `design_audit.js` verde, capturas a 1440 y 390,
  y `DESIGN.md` escrito desde el mundo construido.

## Regla de trabajo

Cada tarea deja la app funcionando y se cierra con los cuatro controles:

```powershell
python quiz\build.py quiz\data quiz\template.html quiz\B2_quiz.html
node quiz\smoke_test.js quiz\B2_quiz.html
node quiz\security_test.js quiz\B2_quiz.html
node quiz\design_audit.js quiz\template.html
```

Se avanza por pasos. Sergio mira una captura antes de pasar al siguiente.

---

## Tarea 1: tokens y material

**Descripción:** sustituir el bloque `:root` de `template.html` por la paleta
Lesesaal. Radios a 0, sombras a `none`, filetes a 1 px. Cambiar solo valores, no
nombres de token: `design_audit.js` lee `--bg`, `--panel`, `--txt`, `--line`,
`--sheet`, `--acc-fill-1/2`, `--sh-*`, `--sp-*`, `--fs-*`.

**Aceptación:**
- [ ] La app compila y el HTML conserva las 722 preguntas.
- [ ] No queda ningún azul `#4d8df6` ni halo en el HTML generado.
- [ ] `design_audit.js` solo falla en contrastes de componentes aún sin migrar.

**Verificación:** los cuatro controles + captura 1440.
**Dependencias:** ninguna. **Archivos:** `quiz/template.html`. **Alcance:** S.

## Tarea 2: cabecera

**Descripción:** banda verde botella con el monograma, los dos perfiles, los tres
idiomas, los contadores y las acciones.

**Aceptación:**
- [ ] Perfil activo, idioma activo y contadores se ven sin pasar el ratón.
- [ ] «98 dudosas» se lee sobre verde (contraste ≥4.5:1).
- [ ] Contraste y foco pasan la auditoría.

**Verificación:** controles + captura. **Depende de:** 1. **Archivos:** `quiz/template.html`. **Alcance:** S.

## Tarea 3: navegación y progreso

**Descripción:** navegación numerada por secciones con recuento a la derecha, y
barra de progreso de cinco casillas que sustituye la línea de metro.

**Aceptación:**
- [ ] Cada sección muestra número, nombre y número de ítems.
- [ ] La casilla en curso se distingue sin color.
- [ ] Se pliega y despliega como hoy; `smoke_test.js` no falla.

**Verificación:** controles + captura. **Depende de:** 1. **Archivos:** `quiz/template.html`. **Alcance:** M.

## Tarea 4: hoja de examen

**Descripción:** cabecera de la hoja (título DIN, fuente, ítems, tiempo), bloque de
tarea en Palatino, dos columnas con filete central y celdas de opción a–h.

**Aceptación:**
- [ ] Los ocho anuncios y los cinco ítems caben sin scroll horizontal a 1280 px.
- [ ] Las celdas miden 28 px de lado mínimo y 44 px en pantalla táctil.
- [ ] La columna de referencia sigue fija en modo mesa.

**Verificación:** controles + captura 1440 y 1280. **Depende de:** 1. **Archivos:** `quiz/template.html`. **Alcance:** M.

## Tarea 5: estados y duda

**Descripción:** acierto, fallo, seleccionada, hover y foco con la gramática nueva.
Sustituir las tres rayitas por una sola marca de duda.

**Aceptación:**
- [ ] Acierto y fallo no dependen solo del color: llevan marca o tachado.
- [ ] La marca de duda aparece solo donde `confidence` no es alta.
- [ ] Hover y foco visibles por teclado en todas las celdas.

**Verificación:** controles + una captura con acierto, fallo y duda. **Depende de:** 4. **Archivos:** `quiz/template.html`. **Alcance:** S.

## Tarea 6: Schreiben

**Descripción:** editor de redacción, criterios y caja de corrección con el mundo
nuevo. Es la pantalla más densa de la app.

**Aceptación:**
- [ ] Veredicto, puntuación y criterios se leen en jerarquía clara.
- [ ] El aviso de «sin clave» y los estados de error mantienen su texto.
- [ ] Ninguna cadena de la interfaz pierde su pareja ES/RU.

**Verificación:** controles + captura. **Depende de:** 1. **Archivos:** `quiz/template.html`. **Alcance:** M.

## Tarea 7: Sprechen y Modeltests

**Descripción:** mazo de Smalltalk, mesa de trabajo, situaciones de T3 y tarjetas
de los siete Modeltests.

**Aceptación:**
- [ ] La tarjeta de Smalltalk se lee como ficha, no como tarjeta genérica.
- [ ] Las situaciones pliegan ayuda ES/RU como hoy.
- [ ] Un Modeltest completo se navega sin saltos de layout.

**Verificación:** controles + captura. **Depende de:** 1. **Archivos:** `quiz/template.html`. **Alcance:** M.

## Tarea 8: tema noche

**Descripción:** segundo tema del mismo mundo: papel a carbón verdoso, banda más
oscura, latón como único acento.

**Aceptación:**
- [ ] Cambiar de tema no recarga ni parpadea.
- [ ] Contraste ≥4.5:1 en ambos temas.
- [ ] La elección sobrevive al cierre.

**Verificación:** controles + captura de cada tema. **Depende de:** 5. **Archivos:** `quiz/template.html`. **Alcance:** S.

## Tarea 9: móvil y cierre

**Descripción:** revisar a 390 px, corregir, pasar la auditoría completa y escribir
`DESIGN.md` con los tokens y las reglas del mundo construido.

**Aceptación:**
- [ ] Los cuatro controles verdes, sin excepciones.
- [ ] Captura 1440 y 390 revisadas una vez, arregladas en un solo lote.
- [ ] `DESIGN.md` describe lo construido, no lo planeado.

**Verificación:** los cuatro controles + dos capturas. **Depende de:** 2–8. **Archivos:** `quiz/template.html`, `DESIGN.md`. **Alcance:** M.

---

## Puntos de control

| Después de | Sergio ve | Si dice que no |
|---|---|---|
| T1 | la app entera recoloreada | se cambia la paleta, no el layout |
| T5 | Lesen completo con estados | se ajusta antes del resto |
| T7 | las cuatro superficies | se rehace la que falle |
| T9 | escritorio y móvil | cierre bloqueado |
