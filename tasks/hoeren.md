# Hören T1–T4

Rama: `main`. Base: `main` en `7f11feb`.

El material existe en `quiz/src/h1_*.md` … `h4_*.md` desde hace tiempo, pero no hay
JSON en `quiz/data/`. La app declara las secciones `hoeren-t1` … `hoeren-t4` en
`build.py` y no las enseña porque no hay datos.

## Contrato

- **Objetivo:** las cuatro secciones de Hören en la barra, con sus 30 variantes.
- **Qué se rechaza:** audio y Hören und Schreiben (Telefonnotiz). No hay ficheros
  de audio, y la nota telefónica es otro tipo de tarea.
- **Cierre:** los cuatro controles verdes y las cuatro secciones visibles.

## Regla de trabajo

Cada entrega deja la app funcionando. Se cierra con:

```powershell
python quiz\build.py quiz\data quiz\template.html quiz\B2_quiz.html
node quiz\smoke_test.js quiz\B2_quiz.html
node quiz\security_test.js quiz\B2_quiz.html
node quiz\design_audit.js quiz\template.html
```

Los Hörtexte son transcripciones de candidatos, no el audio oficial. Cada variante
lleva `note` y `note_ru` con ese aviso.

## Inventario

| Parte | Variantes | Ítems | Sin Hörtext |
|---|---|---|---|
| T1 | 8 | 48 | — |
| T2 | 7 | 28 | variante 7 |
| T3 | 7 | 28 | — |
| T4 | 8 | 40 | variante 7 |

Total: 144 ítems. 135 con clave, 9 sin clave (`kind: "ohne-key"`).

Cada ítem lleva `quote` literal del Hörtext, `confidence`, `explain` y `explain_ru`.
`build.py` ya avisa si la cita no aparece en el pasaje.

---

## Tarea H1: Hören T1, variantes 1–4

**Descripción:** `quiz/data/hoeren_t1.json` con las cuatro primeras variantes. Ítems
22–27: tres Richtig/Falsch y tres de elección a–c.
**Aceptación:**
- [ ] 4 variantes, 24 ítems, cada uno con cita, confianza y explicación ES/RU.
- [ ] `build.py` termina sin errores y avisa de menos de 3 citas no literales.
**Verificación:** los cuatro controles.
**Depende de:** —. **Archivos:** `quiz/data/hoeren_t1.json`. **Alcance:** M.

## Tarea H2: Hören T1, variantes 5–8

**Descripción:** completar `hoeren_t1.json` hasta las 8 variantes.
**Aceptación:**
- [ ] 8 variantes, 48 ítems.
- [ ] La sección sale en la barra con su orden y su contador.
**Verificación:** controles + captura de la sección en la app.
**Depende de:** H1. **Archivos:** `quiz/data/hoeren_t1.json`. **Alcance:** M.

## Tarea H3: Hören T2

**Descripción:** `quiz/data/hoeren_t2.json`, 7 variantes de emparejamiento (ítems
28–31, opciones a–f). La variante 7 no tiene Hörtext: va `ohne-key`.
**Aceptación:**
- [ ] 6 variantes con clave y 1 sin clave; 28 ítems.
- [ ] Las respuestas de cada variante son letras distintas y salen del pool.
**Verificación:** controles.
**Depende de:** H1. **Archivos:** `quiz/data/hoeren_t2.json`. **Alcance:** M.

## Tarea H4: Hören T3

**Descripción:** `quiz/data/hoeren_t3.json`, 7 variantes de elección (ítems 32–35).
Los bloques de `src` traen el Hörtext y las preguntas separados; se funden en una
variante.
**Aceptación:**
- [ ] 7 variantes, 28 ítems, cada uno con sus tres opciones.
- [ ] `build.py` no marca citas no literales.
**Verificación:** controles.
**Depende de:** H1. **Archivos:** `quiz/data/hoeren_t3.json`. **Alcance:** M.

## Tarea H5: Hören T4

**Descripción:** `quiz/data/hoeren_t4.json`, 8 variantes (ítems 36–40). La variante
7 no tiene Hörtext: va `ohne-key`.
**Aceptación:**
- [ ] 7 variantes con clave y 1 sin clave; 40 ítems.
- [ ] Los ítems Richtig/Falsch y de elección se pintan como en T1.
**Verificación:** controles + captura.
**Depende de:** H1. **Archivos:** `quiz/data/hoeren_t4.json`. **Alcance:** M.

## Tarea H6: Cierre

**Descripción:** actualizar `quiz/README.md` (sección nova, recuentos, huecos) y
escribir el registro. Repasar la barra en escritorio y móvil.
**Aceptación:**
- [ ] Los cuatro controles verdes.
- [ ] `README.md` dice qué Hören hay y qué falta.
**Verificación:** controles + captura 390.
**Depende de:** H2–H5. **Archivos:** `quiz/README.md`. **Alcance:** S.

---

## Puntos de control

| Después de | Se revisa | Si falla |
|---|---|---|
| H2 | T1 completo en la app, 8 variantes | se corrige antes de T2 |
| H5 | las cuatro partes | se repasa la que falle |

## Registro

- **H1** — 2 variantes, 12 ítems. `build.py` sin errores, citas literales.
  `smoke_test.js`: 130/130.
- **H2** — 8 variantes, 48 ítems. `build.py` 770 ítems (689 con clave), sin
  errores. Los cuatro controles verdes: smoke 130/130, seguridad 52/52, diseño
  77/77.
- **H3** — 7 variantes, 28 ítems (24 con clave, 4 sin clave). `build.py` 798
  ítems (713 con clave), sin errores ni citas rotas. Smoke 137/137, seguridad
  52/52, diseño 77/77.
- **H4** — 7 variantes, 28 ítems. `build.py` 826 ítems (741 con clave), sin
  errores ni citas rotas. Smoke 137/137, seguridad 52/52, diseño 77/77.
  Cuatro respuestas en `mittel` por doble lectura defendible.
- **H5** — variantes alternativas de T1: 6 entradas pequeñas con 8 ítems, mismo
  Hörtext y solo las preguntas reformuladas. `build.py` 834 ítems, smoke 137/137,
  seguridad 52/52, diseño 77/77.

## Fuera de alcance

- Audio: no hay ficheros en el repo.
- Hören und Schreiben (Telefonnotiz): otro tipo de tarea, otra decisión.
- Claves de Hören de los Modeltests: ya están donde toca.
