---
name: desarrollo-guiado-por-pruebas
description: >-
  Desarrolla guiado por pruebas con el ciclo rojo-verde-refactor. Usar al implementar cualquier lógica,
  al corregir un bug o al cambiar comportamiento, y cuando pidan pruebas para una función. Cubre el patrón
  "demuéstralo", la pirámide de pruebas, el estado actual sin suite de este proyecto y las trampas de las
  pruebas falsas.
license: MIT
---

# Desarrollo Guiado por Pruebas

> Escribe una prueba que falle antes de escribir el código que la hace pasar.
> "Parece que funciona" no es estar terminado.

## 1. Cuándo Usar

Al implementar lógica o comportamiento nuevo. Al corregir un bug: primero reproduce el bug con una prueba. Al modificar funcionalidad existente. Al añadir casos límite.

**No usar** para configuración pura, documentación o contenido estático sin efecto en el comportamiento.

## 2. Estado Actual de Este Proyecto (léelo antes de empezar)

**Este repositorio todavía no tiene suite de pruebas.** Verificado en sesión:

| Elemento | Estado |
|---|---|
| `pytest` | **No instalado.** `python -m pytest` responde "No module named pytest". |
| Carpeta `tests/` | **No existe.** |
| `test_api.py` (raíz) | **No es una suite.** Guion manual que exige un servidor vivo en `localhost:8000`. |
| Configuración | Sin `pyproject.toml`, `pytest.ini`, `setup.cfg` ni `tox.ini`. |

**Consecuencia:** los comandos `pytest` de esta skill todavía no funcionan. Antes de la primera prueba, decide con el usuario cómo se establece la suite mínima.

**Instalar pytest pasa por `dependency-safety`** (regla de 14 días sobre PyPI). No instales por iniciativa propia.

**Alternativa mientras no haya suite:** una prueba mínima con la biblioteca estándar (`assert` o `unittest`). Es lo que pide `ponytail`. Una prueba real y pequeña vale más que ninguna.

## 3. El Ciclo

```
   ROJO              VERDE             REFACTOR
Prueba que   ──→  Código mínimo  ──→  Limpia sin cambiar  ──→  (repetir)
FALLA             hace pasar          comportamiento
```

**Paso 1. ROJO.** La prueba va primero y debe fallar. Una prueba que pasa de inmediato no demuestra nada.

```python
# tests/test_afinidad.py
from backend.services.progression import ajustar_afinidad

def test_la_afinidad_sube_con_interaccion_positiva():
    assert ajustar_afinidad(50, delta=10) == 60
```

**Paso 2. VERDE.** El código **mínimo** que la haga pasar. Sin sobreingeniería.

```python
def ajustar_afinidad(valor_actual: int, delta: int) -> int:
    return valor_actual + delta
```

**Paso 3. REFACTOR.** Con las pruebas en verde, mejora sin cambiar comportamiento. Ejecuta las pruebas tras cada paso.

El rango del sistema es -100 a +300. Añade el caso límite como prueba **antes** de implementarlo:

```python
def test_no_supera_el_maximo():  assert ajustar_afinidad(295, 10) == 300
def test_no_baja_del_minimo():   assert ajustar_afinidad(-95, -10) == -100
```

## 4. El Patrón "Demuéstralo" (para bugs)

No empieces intentando arreglar. Empieza escribiendo la prueba que lo reproduce.

1. Escribe la prueba. 2. Ejecútala: **falla**, confirmando el bug. 3. Arregla. 4. Ejecútala: **pasa**. 5. Corre la suite completa.

Vincula esto con `depuracion-y-recuperacion`: el paso 4 del triaje exige esta prueba.

**Truco:** para bugs complejos, delega la prueba a un subagente **sin decirle el arreglo**. Así no se sesga hacia tu solución.

## 5. La Pirámide

```
      ╱╲      Extremo a extremo (~5%)   Flujos completos
     ╱────╲   Integración (~15%)        Límites de API, base de datos
    ╱────────╲ Unitarias (~80%)         Lógica pura, milisegundos
```

| Tamaño | Restricciones | Ejemplo en este proyecto |
|---|---|---|
| Pequeña | Un proceso, sin red ni base de datos | `ajustar_afinidad`, gacha, validaciones |
| Mediana | Solo `localhost` | Endpoints con `TestClient` y SQLite en memoria |
| Grande | Servicios externos | Flujo completo con el LLM real |

Las pequeñas deben ser la enorme mayoría: son rápidas, fiables y fáciles de depurar.

## 6. Cómo Escribir Buenas Pruebas

- **Prueba el estado, no las interacciones.** Verifica el resultado, no qué métodos se llamaron por dentro. Las pruebas de secuencia de llamadas se rompen al refactorizar sin que el comportamiento cambie.
- **DAMP sobre DRY.** Cada prueba debe leerse como una especificación por sí sola. Duplicar datos de entrada es aceptable si aclara.
- **Real antes que simulado.** Orden: implementación real > objeto falso en memoria > stub > simulación de llamadas. Simula solo lo lento, lo no determinista o lo que tiene efectos que no controlas.
- **Simula siempre el LLM.** Es lento, cuesta dinero y no es determinista. Prueba tu lógica, no el modelo.
- **Aísla el estado.** Nunca apuntes pruebas a `anime-rpg-v2/backend/anime_rpg.db`. Usa SQLite en memoria con un fixture que monte y desmonte.
- **Un concepto por prueba.** Y nombres que lean como especificación: `test_la_afinidad_no_baja_del_minimo`. Prohibidos `test_1`, `test_funciona`.

```python
from fastapi.testclient import TestClient
from backend.main import app

cliente = TestClient(app)

def test_crear_personaje_devuelve_201():
    respuesta = cliente.post("/characters", json={"nombre": "Kira"})
    assert respuesta.status_code == 201
```

`fastapi.testclient` necesita `httpx`. Verifica su fecha de publicación con `dependency-safety` antes de añadirlo.

## 7. Tabla Anti-Racionalización

| Racionalización | Realidad |
|---|---|
| "Escribo las pruebas cuando ya funcione." | No lo harás. Y probarán la implementación, no el comportamiento. |
| "Esto es demasiado simple para probarlo." | Lo simple se complica. La prueba documenta el comportamiento esperado. |
| "Las pruebas me frenan." | Te frenan ahora. Te aceleran cada vez que cambies el código después. |
| "Lo probé a mano." | Lo manual no persiste. Ese es justo el caso de `test_api.py`. |
| "El código se explica solo." | Las pruebas **son** la especificación: qué **debe** hacer, no qué hace. |
| "Es solo un prototipo." | Los prototipos se vuelven producción. |
| "Ejecuto las pruebas otra vez para estar seguro." | Tras una ejecución limpia, repetir sin cambio de código no aporta nada. |
| "No hay pytest, así que no puedo probar." | Falso. `assert` y `unittest` vienen en la biblioteca estándar. |

## 8. Banderas Rojas

- Escribir código sin ninguna prueba correspondiente.
- Usar un comando de pruebas por defecto sin comprobar cuál usa este repositorio.
- Pruebas que pasan a la primera ejecución: puede que no prueben lo que crees.
- "Todas las pruebas pasan" sin haberlas ejecutado.
- Correcciones de bug sin prueba de reproducción.
- Presentar `test_api.py` como si fuera la suite del proyecto.
- Saltarse o desactivar pruebas para que la suite pase.
- Apuntar las pruebas a la base de datos real del juego.

## 9. Verificación

- [ ] Cada comportamiento nuevo tiene su prueba.
- [ ] La suite completa pasa, con el comando propio del repositorio.
- [ ] Las correcciones de bug incluyen una prueba que fallaba antes del arreglo.
- [ ] Los nombres describen el comportamiento verificado.
- [ ] No se saltó ni desactivó ninguna prueba.
- [ ] Las pruebas de base de datos usan conexión en memoria, no `anime_rpg.db`.
- [ ] Las llamadas al LLM están simuladas.

---

Adaptado de `test-driven-development` de [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) (MIT).
