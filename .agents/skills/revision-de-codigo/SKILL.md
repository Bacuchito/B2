---
name: revision-de-codigo
description: >-
  Revisión de código multi-eje antes de fusionar cualquier cambio. Usar antes de hacer merge, al terminar
  una funcionalidad, al evaluar código de otro agente o de un humano, al revisar un diff o un pull request,
  y tras corregir un bug. Cubre cinco ejes (corrección, legibilidad, arquitectura, seguridad, rendimiento),
  etiquetas de severidad, tamaño de cambio y verificación real.
license: MIT
---

# Revisión de Código y Calidad

> Aprueba un cambio cuando **mejora** la salud del código, aunque no sea perfecto.
> Aprobar sin revisar y bloquear por estilo personal dañan igual.

## 1. Cuándo Usar

Antes de fusionar cualquier cambio. Al terminar una funcionalidad. Al evaluar código de otro agente o de un humano. Tras corregir un bug, revisando también su prueba de regresión.

## 2. Los Cinco Ejes

**Corrección.** ¿Cumple lo que pide la tarea? ¿Maneja casos límite (nulo, vacío, cero)? ¿Maneja rutas de error, no solo el camino feliz? ¿Las pruebas verifican lo correcto? ¿Hay errores de índice o condiciones de carrera?

**Legibilidad.** ¿Los nombres describen el contenido? Prohibido `temp`, `data`, `result` sin contexto. ¿El flujo es directo, sin ternarios anidados? ¿Cabe en menos líneas? Mil líneas donde bastan cien es un fallo. ¿Las abstracciones se ganan su complejidad? No generalices hasta el tercer caso de uso. ¿Quedan restos muertos: variables sin uso, adaptadores de compatibilidad, comentarios `# eliminado`?

**Arquitectura.** ¿Sigue los patrones existentes? ¿Respeta los límites entre módulos? ¿Las dependencias fluyen sin ciclos? ¿El refactor reduce complejidad o solo la traslada? Cuenta los conceptos que el lector debe sostener: si el número no baja, no es más limpio. ¿Lógica de una funcionalidad se filtró a un módulo compartido? ¿Se duplicó un ayudante que ya existía?

**Seguridad.** Consulta `cybersecurity-audit`. ¿Se valida la entrada? ¿Los secretos quedan fuera del código y de los registros? ¿Se comprueban autenticación y autorización? ¿Las consultas SQL usan parámetros? ¿La salida se codifica contra inyección de HTML? ¿Los datos externos se tratan como no confiables?

**Rendimiento.** ¿Consultas dentro de un bucle (problema N+1)? ¿Bucles sin límite o lecturas sin paginar? ¿Operaciones síncronas que deberían ser asíncronas? ¿Re-renderizados innecesarios?

## 3. Etiquetas de Severidad

| Etiqueta | Significado | Acción del autor |
|---|---|---|
| **Crítico:** | Vulnerabilidad, pérdida de datos, funcionalidad rota. | Obligatorio antes de fusionar. |
| *(sin prefijo)* | Cambio obligatorio. | Obligatorio antes de fusionar. |
| **Opcional:** | Sugerencia. | A criterio del autor. |
| **Nit:** | Detalle menor de estilo. | Puede ignorarse. |
| **FYI** | Solo información. | Ninguna acción. |

**Empieza por lo que importa.** Corrección y seguridad primero. No entierres un defecto real bajo diez detalles cosméticos: un problema estructural y diez nits, el estructural **es** la revisión.

## 4. Proceso

1. **Entiende el contexto.** Qué busca el cambio y qué comportamiento debería cambiar.
2. **Revisa las pruebas primero.** Deben probar comportamiento, no estructura interna.
3. **Prueba de mutación.** Invierte una condición nueva (quita una negación, cambia `and` por `or`). Ejecuta la suite. Restaura el archivo. Si sigue en verde, falta una prueba: nombra el caso ausente.
4. **Recorre los cinco ejes** por archivo modificado.
5. **Verifica la verificación.** ¿Corrieron las pruebas? ¿Compila? ¿Hubo comprobación manual?
6. **Higiene de código muerto.** Lístalo y **pregunta antes de borrar**: "¿Elimino estos elementos ya sin uso: [lista]?"

## 5. Tamaño del Cambio

```
~100 líneas cambiadas  → Bien. Revisable de una sentada.
~300 líneas cambiadas  → Aceptable si es un único cambio lógico.
~1000 líneas cambiadas → Demasiado grande. Divídelo.
```

Vigila también el tamaño del archivo. Cerca de 1000 líneas totales es señal de inspección. Si el cambio engorda un archivo ya grande, propón extraer módulos **antes** de añadir más.

Separa el refactor de la funcionalidad nueva: son dos cambios. El mensaje de commit va en imperativo ("Elimina el RPC de FizzBuzz"), y el cuerpo explica qué cambia y por qué. Anti-patrones: "arregla bug", "fase 1", "mueve código de A a B".

## 6. Honestidad y Desacuerdos

Jerarquía: hechos técnicos sobre opiniones; la guía de estilo manda en estilo; el diseño se evalúa con principios de ingeniería; la consistencia con el código existente vale si no degrada el proyecto.

- **No apruebes por complacencia.** "LGTM" sin evidencia no ayuda.
- **No suavices problemas reales.** Llamar "preocupación menor" a un bug que llegará a producción es deshonesto.
- **Cuantifica.** "Esta consulta N+1 añade ~50 ms por elemento" supera a "podría ser lento".
- **Discute el código, no a la persona.**
- **Acepta la anulación con elegancia.** Si el autor tiene contexto completo y discrepa, cede.

## 7. Tabla Anti-Racionalización

| Racionalización | Realidad |
|---|---|
| "Funciona, es suficiente." | Código ilegible o inseguro acumula deuda que se compone. |
| "Lo escribí yo, sé que está bien." | El autor es ciego a sus propias suposiciones. |
| "Ya lo limpiaremos después." | Después nunca llega. Exige la limpieza antes de fusionar. |
| "El código de IA probablemente está bien." | Necesita **más** escrutinio: es convincente incluso cuando está mal. |
| "Pasan las pruebas, entonces está bien." | No detectan arquitectura ni seguridad. |
| "El refactor lo deja más limpio." | Trasladar complejidad no es reducirla. Busca la versión donde ramas enteras desaparecen. |
| "Es un añadido pequeño a este archivo." | Un diff pequeño puede empujar el archivo más allá del límite sano. |

## 8. Banderas Rojas

- Fusiones sin ninguna revisión.
- Revisión que solo comprueba si pasan las pruebas.
- Cambios sensibles a seguridad sin revisión de seguridad.
- Diffs gigantes "imposibles de revisar bien".
- Correcciones de bug sin prueba de regresión.
- Comentarios sin etiqueta de severidad.
- Aceptar "lo arreglo luego".
- Un ayudante nuevo que duplica uno canónico existente.

## 9. Verificación

- [ ] Hallazgos **Críticos** resueltos.
- [ ] Cambios obligatorios resueltos o aplazados con justificación explícita.
- [ ] Las pruebas pasan y la compilación termina sin errores.
- [ ] La prueba de mutación sobre al menos una condición nueva se mantuvo en rojo.
- [ ] El código muerto se listó y se preguntó antes de borrarlo.
- [ ] La historia de verificación quedó documentada.

---

Adaptado de `code-review-and-quality` de [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) (MIT).
