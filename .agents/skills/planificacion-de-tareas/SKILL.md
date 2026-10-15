---
name: planificacion-de-tareas
description: >-
  Descompone trabajo en tareas pequeñas, ordenadas y verificables con criterio de aceptación explícito.
  Usar con una especificación o requisitos claros, cuando una tarea se sienta demasiado grande o vaga,
  cuando el orden de implementación no sea obvio, o para repartir trabajo entre agentes o sesiones.
  Cubre rebanadas verticales, grafo de dependencias, tamaños de tarea y puntos de control.
license: MIT
---

# Planificación y Descomposición de Tareas

> Implementar sin plan es solo teclear.

## 1. Cuándo Usar

Tienes una especificación y necesitas unidades implementables. Una tarea se siente demasiado grande o vaga. Hay que repartir trabajo entre agentes. Necesitas comunicar alcance a una persona. El orden no es evidente.

**No usar** para cambios de un solo archivo con alcance obvio, o si la especificación ya trae tareas definidas.

## 2. Proceso

**Paso 1. Modo lectura.** Lee la especificación y el código relevante. Identifica patrones existentes. Traza dependencias. Anota riesgos e incógnitas. **No escribas código durante la planificación.**

**Paso 2. Grafo de dependencias.** En este proyecto el orden suele ser:

```
Esquema de base de datos (backend/db/schema.py)
    ├── Modelos y validación (models.py)
    │       ├── Rutas de la API (backend/routers/)
    │       │       └── Cliente de API y componentes de interfaz
    │       └── Lógica de validación
    └── Datos iniciales (backend/db/seed.py)
```

Implementa de abajo hacia arriba: primero los cimientos.

**Paso 3. Corta en rebanadas verticales.** No construyas toda la base de datos, luego toda la API, luego toda la interfaz.

```
Mal:  T1 esquema completo → T2 todos los endpoints → T3 toda la interfaz → T4 conectar
Bien: T1 crear personaje (esquema + endpoint + interfaz)
      T2 ver ficha        T3 subir afinidad
```

Cada rebanada entrega funcionalidad que funciona y se puede probar.

**Paso 4. Escribe cada tarea.**

```markdown
## Tarea N: [Título corto]

**Descripción:** Un párrafo sobre qué logra.

**Criterio de aceptación:**
- [ ] [Condición concreta y comprobable]

**Verificación:**
- [ ] Pruebas: python -m pytest tests/test_x.py -v
- [ ] Arranque: python -m uvicorn main:app --reload
- [ ] Manual: [qué mirar y qué debe mostrar]

**Dependencias:** [Números, o "Ninguna"]
**Archivos probables:** [rutas]
**Alcance:** [XS | S | M]
```

**Paso 5. Ordena y coloca puntos de control.** Dependencias satisfechas. Cada tarea deja el sistema funcionando. Verificación cada dos o tres tareas. Las tareas de mayor riesgo van primero, para fallar temprano.

## 3. Tamaños de Tarea

| Tamaño | Archivos | Alcance | Ejemplo |
|---|---|---|---|
| **XS** | 1 | Una función o un valor de configuración | Añadir una regla de validación |
| **S** | 1-2 | Un componente o un endpoint | Añadir un endpoint |
| **M** | 3-5 | Una rebanada de funcionalidad | Flujo de creación de personaje |
| **L** | 5-8 | Multi-componente | Búsqueda con filtros y paginación |
| **XL** | 8+ | **Demasiado grande. Divídelo.** | — |

Si es L o mayor, divídela. Divide más si: ocuparía más de una sesión enfocada, no puedes describir el criterio en 3 puntos o menos, toca dos subsistemas independientes, o aparece la palabra "y" en el título.

## 4. Archivos de Salida

Guarda el plan en `tasks/plan.md` y registra las tareas en la lista de tareas de la sesión. Crea `tasks/` si no existe.

**Nunca sobrescribas un plan incompleto.** Si `tasks/plan.md` ya existe con tareas sin marcar:

| Situación | Acción |
|---|---|
| Mismo trabajo, el usuario pidió revisarlo | Actualiza los archivos existentes. |
| Trabajo distinto | **Detente y pregunta.** Esas tareas pueden estar a medio construir en otra sesión. |

Nunca borres ni renombres los archivos de otro plan por tu cuenta.

## 5. Qué Se Puede Paralelizar

- **Seguro en paralelo:** rebanadas independientes, pruebas de funcionalidad ya implementada, documentación.
- **Secuencial:** migraciones de base de datos, estado compartido, cadenas de dependencias.
- **Necesita coordinación:** funcionalidades que comparten un contrato de API. Define el contrato primero.

## 6. Tabla Anti-Racionalización

| Racionalización | Realidad |
|---|---|
| "Ya lo iré resolviendo sobre la marcha." | Así terminas con un enredo y trabajo rehecho. Diez minutos de plan ahorran horas. |
| "Las tareas son obvias." | Escríbelas igual. Sacan a la luz dependencias ocultas y casos olvidados. |
| "Planificar es papeleo." | Planificar **es** la tarea. Implementar sin plan es solo teclear. |
| "Puedo tenerlo todo en la cabeza." | La ventana de contexto es finita. Los planes escritos sobreviven entre sesiones. |
| "El plan viejo está obsoleto, lo reemplazo." | Las tareas sin marcar pueden estar a medio construir. Sobrescribir destruye estado que no existe en otro sitio. |

## 7. Banderas Rojas

- Empezar a implementar sin lista de tareas escrita.
- Sobrescribir un plan con tareas sin marcar de otro trabajo sin preguntar.
- Tareas que dicen "implementa la funcionalidad" sin criterio de aceptación.
- Tareas sin paso de verificación.
- Todas las tareas son tamaño XL.
- Sin puntos de control entre tareas.
- El agente inventó el plan sin que el usuario lo aprobara.

## 8. Verificación

- [ ] Cada tarea tiene criterio de aceptación y paso de verificación con comando concreto.
- [ ] Dependencias identificadas y orden correcto.
- [ ] Tareas registradas en `tasks/plan.md` y en la lista de la sesión.
- [ ] No se sobrescribió ningún plan incompleto sin confirmación.
- [ ] Ninguna tarea toca más de 5 archivos.
- [ ] Hay puntos de control entre fases.
- [ ] El usuario revisó y aprobó el plan.

---

Adaptado de `planning-and-task-breakdown` de [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) (MIT).
