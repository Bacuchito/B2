# Pipeline PDF → Markdown (sin dependencias)

Conversión de `Без ответов Alle Information от 21.09.26.pdf` (209 páginas, examen
alemán telc **Deutsch-Test für den Beruf B2**) a Markdown legible y navegable.

## Por qué no se usó MarkItDown

[MarkItDown](https://github.com/microsoft/markitdown) era la opción natural, pero
**no se pudo instalar**: esta máquina no tiene salida a Internet.

| Comprobación | Resultado |
|---|---|
| `https://pypi.org`, `files.pythonhosted.org`, `github.com`, `google.com` | TLS bloqueado — *"error inesperado de recepción"* |
| `http://pypi.org/simple/` | HTTP **403** |
| Caché de `pip` | **0 wheels** |
| `pypdf` / `pdfminer` / `PyMuPDF` | ausentes en el runtime de DSH, Python 3.11 del sistema, `~/.hub-global` y `node_modules` |
| `pdftotext` / poppler / LibreOffice | ausentes |

El PDF **sí tiene capa de texto**, así que se escribió un conversor propio.

## Scripts

### `pdf2md.py` — el conversor

Python puro, **solo `zlib` de la stdlib**. Componentes:

1. **Parser de objetos PDF** con descenso recursivo (`Lexer.parse_object`).
   - Ensambla **referencias indirectas** `N G R` → `[n, g, R]`. Sin esto el árbol
     de páginas y los `/Widths` quedaban rotos.
   - Extrae objetos de **object streams** (`/ObjStm`, `FlateDecode`). Imprescindible:
     los `ToUnicode` viven ahí.
   - Descarta falsos positivos de `N 0 obj` que caigan dentro de un `stream`.
2. **Árbol de páginas** real: `Catalog → Pages → Kids`, con atributos heredables
   (`/Resources` vía `/Parent`).
3. **Fuentes**:
   - `TrueType` + `/WinAnsiEncoding` → decodificación `cp1252` y `/Differences`.
   - `Type0` + `/Identity-H` (2 bytes) → **CMap `/ToUnicode`** (`bfchar` y `bfrange`,
     incluidas las formas con array).
   - Anchos reales desde `/Widths` (fuentes simples) y `/W` + `/DW` (CID).
4. **Extracción de texto** siguiendo el *text matrix*: `BT/ET`, `Tm`, `Td`, `TD`,
   `T*`, `TL`, `Tc`, `Tw`, `Tz`, `Tf`, `Tj`, `TJ`, `'`, `"`.
5. **Reconstrucción de líneas**: agrupa fragmentos por coordenada `y` (tolerancia
   `0.45 em`) y los ordena por `x`.

Validador clave — **el ancho de avance real** (`Run.x1`) en lugar de una estimación.
La primera versión estimaba `len(texto) × 0.5 em` y producía espacios basura
(`Arbeitsm arkt`, `Mu ltiple-Cho ice`). Con el avance real desaparecieron.

### Umbral de espacio: por qué 0.18 em

Medido con `analyze_gaps.py` sobre 40 páginas (33.484 huecos):

| hueco/em | casos | significado |
|---|---|---|
| 0.00 | 32.697 | kerning o espacio ya presente → **sin espacio** |
| 0.20 | 9 | mixto |
| 0.25 | 778 | frontera de palabra real sin glifo → **con espacio** |

El umbral 0.18 acierta en **33.475 / 33.484 = 99,97 %**. Subirlo rompería 778
fronteras reales para arreglar 9. **No tocar.**

### `make_index.py` — índice navegable

Extrae la primera línea significativa de cada página (priorizando encabezados `###`
y palabras clave como `TOP`, `Teil`, `LESEN`, `Вариант`).

### `inspect_pdf.py` — diagnóstico previo

Histograma de tipos de objeto, subtipos de fuente, presencia de `ToUnicode` y
capacidad de descompresión. Útil antes de tocar el conversor.

### `analyze_gaps.py` — calibración del umbral de espacio

Distribución de huecos entre fragmentos contiguos.

## Uso

```powershell
$py = "C:\Users\sergi\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\python\python.exe"
$pdf = "$env:USERPROFILE\Downloads\Без ответов Alle Information от 21.09.26.pdf"

& $py tools\pdf2md.py   $pdf out\B2_ohne_antworten.md
& $py tools\make_index.py out\B2_ohne_antworten.md out\INDICE.txt
```

`chunks/` se genera partiendo el Markdown por rangos de página para poder leerlo
en paralelo.

## Resultado

| Métrica | Valor |
|---|---|
| Páginas | 209 / 209 |
| Caracteres | 492.181 |
| Páginas vacías | 1 (p.181, en blanco en el original) |
| Umlauts `ä ö ü ß` | todos correctos |
| `U+FFFD` | 0 |
| Errores de espacio | ~0,03 % |

Idioma: **92,9 % alemán / 7,1 % ruso** (el ruso son las notas del autor).

## Prueba del extractor

```powershell
& $py tools\test_pdf2md.py
```

Cubre el fallo corregido en `extract_runs`: se ignoraba el estado gráfico
`q`/`Q`, así que la fuente elegida dentro de un bloque `q...Q` se filtraba a los
textos siguientes. En las páginas con la capa de texto mezclada (la tabla de
Forumsbeitrag, pp. 98-106) eso hacía que texto ASCII escrito con una fuente
Type0 se leyera como códigos de dos bytes y **se perdiera en silencio**: por eso
faltaban trozos como «nehmen, da keine neuen Mitarbeitenden». Sin el arreglo la
prueba falla en las tres comprobaciones.

## Limitaciones conocidas

- **Diseño multicolumna** (p. ej. p.1, tablas) se lee en orden de coordenadas, no
  en orden de columnas: los encabezados pueden quedar intercalados con las celdas.
- **Sin OCR**: si el PDF fuese un escaneo sin capa de texto, este conversor no
  extraería nada. `pdf2md.py` lo detecta (páginas casi vacías) pero no lo resuelve.
- Solo soporta `FlateDecode`. Un PDF con `LZWDecode`, `ASCII85Decode` o cifrado
  requeriría añadir filtros.
- **Celdas de tabla partidas**: cuando el texto de una celda sigue en la página
  siguiente (p. ej. la fila 110101 de la tabla de Forumsbeitrag), hay que unir a
  mano el fragmento del principio de la página siguiente.
