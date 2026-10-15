---
name: apple-design
description: >-
  Auditor y director de diseño UI/UX basado en las Human Interface Guidelines (HIG) de Apple
  y el estándar de artesanía visual premium (Emil Kowalski / Dick Wu). Elimina el aspecto de
  plantilla o "look a IA" genérico. Aplica las 5 lentes de revisión: accesibilidad y ergonomía,
  ritmo y espaciado (grid de 8pt), materiales de vidrio esmerilado (frosted/liquid glass),
  micro-interacciones con físicas elásticas, y personalidad distintiva no clonada.
argument-hint: "[componente | pantalla | css | auditoria]"
license: MIT
---

# Apple Design Skill: HIG & Craftsmanship Reviewer

> *"El diseño no es solo cómo se ve, sino cómo se siente y cómo funciona."*  
> Combina la precisión técnica de las **Apple HIG** con el ojo de un director de diseño de estudio que rechaza las plantillas genéricas de IA.

---

## 1. El Doble Rol del Auditor

1. **Revisor Técnico Senior de HIG:**  
   Garantiza ergonomía, contrastes medibles, áreas táctiles estándar y coherencia visual en todos los estados (`default`, `hover`, `active`, `disabled`, `focus`).
2. **Director de Diseño de Estudio:**  
   Elimina los vicios visuales de la IA (tarjetas planas, bordes toscos, degradados clichés). Exige acabados de lujo, físicas elásticas y carácter propio.

---

## 2. Las 5 Lentes de Auditoría (En este orden estricto)

### Lente 1: Accesibilidad y Ergonomía Táctil (Crítico)
- **Áreas de toque mínimas:** En móvil, mínimo **44x44 pt** (`min-h-[44px] min-w-[44px]`); en escritorio, mínimo **28x28 pt**. Si el icono visual mide 16px, el área interactiva transparente debe medir 44px.
- **Contraste de color medible:**
  - Texto estándar (< 18 pt): Ratio mínimo **4.5:1** contra el fondo.
  - Texto grande (>= 18 pt o negrita >= 14 pt): Ratio mínimo **3:1**.
- **No depender únicamente del color:** Todo icono o estado debe tener soporte de texto o tooltip accesible.
- **Soporte de movimiento reducido:** Respeta `@media (prefers-reduced-motion)`.

### Lente 2: Jerarquía, Espaciado y Ritmo (Grid de 8pt)
- **Escala de espaciados armónica:** Usa múltiplos de 4 y 8 (4px, 8px, 12px, 16px, 24px, 32px, 48px). Prohibidos paddings arbitrarios como `p-[13px]`.
- **Jerarquía tipográfica legible:** 
  - Título principal claro.
  - Metadatos o texto secundario con atenuación intencional (color subordinado, tipografía mono o trackeada).
- **Respiración:** El contenido nunca debe estar ahogado contra los bordes de una tarjeta o modal.

### Lente 3: Materiales y Acabados (Liquid & Frosted Glass)
- **Cristal esmerilado realista:**  
  Un fondo translúcido premium combina tres capas:
  1. Fondo oscuro con opacidad sutil: `bg-[#0c0e14]/90` o `bg-black/80`.
  2. Desenfoque profundo: `backdrop-blur-xl` o `backdrop-blur-2xl`.
  3. Borde refractivo fino de 1px: En lugar de un borde gris plano, usa un borde sutil con gradiente o transparencia (`border border-white/10` o `border-[#c9954c]/30`).
- **Sombras multicapa:** Una sombra amplia suave para dar elevación atmosférica + una sombra corta para definir el plano.

### Lente 4: Dinamismo, Físicas y Micro-interacciones (Vida)
- **Feedback táctil instantáneo:**  
  Cada botón debe sentirse físico al hacer clic:
  - Presión elástica: `active:scale-[0.97]` o `active:scale-95`.
  - Transición suave: `transition-all duration-150 ease-out` o curvas cúbicas tipo resorte (`cubic-bezier(0.16, 1, 0.3, 1)`).
- **Estados de carga elegantes:** Sustituir bloqueos bruscos por indicadores discretos de pulso o spinners armónicos.

### Lente 5: Identidad y Anti-Plantilla (Des-IAficar)
- **Lista negra de clichés de IA:**
  - ❌ Sombras grises difusas estándar sin iluminación (`shadow-md` plana).
  - ❌ Degradados de color púrpura/cian aleatorios de landing page genérica.
  - ❌ Botones planos sin relieve ni borde de luz.
- **Fusión en Anime RPG v2:**
  - Conserva la temática de fantasía oscura, bordes dorados y estilo visual novel.
  - Aplica la precisión milimétrica de Apple en tipografía, alineación de iconos y feedback elástico.
