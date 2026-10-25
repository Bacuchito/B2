# Design

<!-- impeccable:design-schema 1 -->

## World

**Lesesaal**: la hoja de un examen impreso sobre la mesa de una biblioteca. Papel
marfil, tinta casi negra, una banda verde botella en la cabecera y latón como
único color saturado. Material de imprenta: filetes de 1 px, radios 0, ninguna
sombra. La pieza no se levanta: se separa con un filete.

Nació como reemplazo del mundo «taller nocturno» (carbón, azul y halos), que se
leyó como un panel de administración genérico. Lo que se rechaza de aquel mundo
está en la sección Prohibido.

## Color

Estrategia: **comprometida**. La banda verde es un campo, no un acento; el latón
aparece solo en la acción principal, la marca de duda y el filete de progreso.

| Token | Papel (por defecto) | Noche | Trabajo |
|---|---|---|---|
| `--bg` | `#E4DDC9` | `#12160F` | Mesa: el papel tostado del fondo |
| `--sheet` | `#FCFAF3` | `#1C2217` | La hoja del examen |
| `--panel` | `#FCFAF3` | `#191E15` | Superficie de piezas |
| `--panel3` | `#EDE8D9` | `#151A11` | Hueco: carriles y chips |
| `--line` | `rgba(26,24,20,.16)` | `rgba(239,231,210,.16)` | Filete |
| `--line-2` | `rgba(26,24,20,.30)` | `rgba(239,231,210,.30)` | Filete marcado |
| `--txt` | `#1A1814` | `#EFE7D2` | Tinta |
| `--dim` | `#4E4A40` | `#C2B9A1` | Tinta secundaria |
| `--dim-2` | `#625E52` | `#A79E86` | Tinta terciaria |
| `--band` | `#14382B` | `#152B1E` | Banda de cabecera |
| `--on-band` | `#EFE6CC` | `#EFE6CC` | Tinta sobre la banda |
| `--acc` | `#8A6A1E` | `#C9A44A` | Latón |
| `--acc-fill-1` | `#A8842C` | `#C9A44A` | Relleno de la acción principal |
| `--on-acc` | `#1A1814` | `#14170F` | Tinta sobre el latón |
| `--ok` / `--bad` / `--warn` | `#1F6B4A` / `#9E3B24` / `#8A6414` | `#57C08D` / `#E0705C` / `#D9A94E` | Acierto, fallo, aviso |

Contraste mínimo 4.5:1 en texto normal, medido por `design_audit.js` en los dos
temas sobre la superficie real de cada texto.

## Tipografía

- `--font-d` (Bahnschrift, DIN): rótulos, cifras, titulares y números. Va en
  versalitas, con `font-stretch:87.5%` y `letter-spacing` entre `.06em` y `.12em`.
- `--font-read` (Palatino): lo que se lee como examen. Enunciados, cartas del
  cliente, citas, el área de escritura.
- `--font-ui` (sistema): el resto del texto de interfaz.
- Escala: 11 / 12 / 13 / 15 / 17 / `--fs-h2` 22. Todo pasa por tokens.

## Material

- **Ninguna sombra.** `--sh-1/2/3`, `--bisel`, `--hundido`, `--halo` y `--lit`
  valen `none`. La auditoría lo exige.
- **Ningún radio.** `--radius` y `--r-1..4` valen 0.
- **Un solo degradado en toda la app**: la luz de `body::before`.
- La pieza se separa con `border-top:1px solid var(--line)`, no con altura.

## Componentes

- **Cabecera**: banda `--band`, 62 px, filete de tinta de 2 px abajo. Los
  controles se pintan solos porque `header` redefine dentro los tokens de tinta y
  filete. Perfil en caja con la opción encendida invertida; idioma en dos letras
  con filete debajo; ajustes y tema como cuadrados de 36 px con icono.
- **Índice**: secciones numeradas con un contador de CSS (`01`, `02`…), filas con
  filete y la abierta invertida. Nada de tarjetas.
- **Hoja**: `main` es el papel. Titular en DIN versalitas, línea de datos en
  micro, tira de progreso de una casilla por ítem (solo en bloques de 20 o menos).
- **Preguntas**: dos columnas con filete central en modo mesa; celdas a–h de 44 px
  cuadradas, la elegida invertida, la acertada en verde macizo, la fallada tachada.
- **Insignias de confianza**: sello cuadrado con una marca delante que codifica la
  forma (llena, media, hueca). El color acompaña; no informa solo.
- **Corrección**: filete de color a la izquierda y cita sangrada. Sin tarjeta.

## Estados

| Estado | Señal |
|---|---|
| Enlace o botón activo | Se invierte: tinta de fondo, papel de letra |
| Foco de teclado | Filete de latón de 2 px con 2 px de separación |
| Acierto | Verde macizo **y** ✓ |
| Fallo | Rojo **y** tachado |
| Duda | Forma de la marca (llena, media, hueca) **y** palabra |

## Temas

Dos, por tokens: papel (por defecto) y noche. Cambiar de tema no recarga; el
botón recuerda la elección en `localStorage`. Cambiar de perfil no toca el tema.

## Prohibido

Esto es el mundo anterior, y volver a cualquiera de estas cosas rompe el
contrato:

- Sombras, halos, biseles, degradados de relieve o `backdrop-filter`.
- Radios mayores que 0.
- Tarjetas: fondo propio, borde completo y relleno por los cuatro lados.
- Tintes de color como fondo de bloques de texto (el aviso es un filete).
- Rellenar de latón más de una pieza por pantalla.
- Codificar un estado solo con color.
- Un control que solo existe con el ratón.
