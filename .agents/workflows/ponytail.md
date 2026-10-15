---
name: ponytail
description: Activa el modo de máxima simplicidad y pragmatismo (YAGNI, diff mínimo, cero sobreingeniería)
---

# Workflow: ponytail

Activa la skill `ponytail`.

1. Revisa el nivel de intensidad especificado por el usuario (`lite`, `full` [por defecto], o `ultra`).
2. Aplica la Escalera del Senior Dev a la tarea:
   - ¿Hace falta? (YAGNI)
   - ¿Ya existe en el repo?
   - Stdlib / APIs nativas primero.
   - Diff mínimo comprobado.
3. Causa raíz sobre síntomas para corrección de bugs (`grep` a llamadores).
4. No recortar diseño visual ni controles de seguridad.
