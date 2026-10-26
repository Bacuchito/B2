---
name: segunda-opinion
description: Pide una revisión ciega a otro modelo antes de una decisión cara o difícil de comprobar. Usar cuando haya que contrastar un juicio propio, revisar un plan ajeno, o cuando el desacuerdo se pueda resolver abriendo un fichero o corriendo un test.
---

# Segunda opinión

Un revisor ciego, con otro modelo, que no ve mi conclusión.

## Cuándo

- Voy a aceptar o rechazar algo caro: un plan, un cambio grande, una decisión de producto.
- Mi juicio no lo puede comprobar un test.
- Alguien me pide revisar un documento ajeno y quiero saber si se me escapa algo.

No lo uses para charla, para estilo, ni para lo que ya cubre un control del repo
(`build.py`, `smoke_test.js`, `security_test.js`, `design_audit.js`).

## Las tres reglas

1. **Ciego.** El revisor no ve mi conclusión. Solo el artefacto y la pregunta.
   Prohíbele leer los ficheros donde escribí mi análisis (README, AGENTS, notas).
2. **Veredicto comprobable.** Exige fichero y línea, glob o campo de esquema.
   Si el desacuerdo no se puede resolver abriendo algo, la opinión no vale.
3. **Modelo distinto.** `mimo-v2.6-flash` es el que mejor rindió en la prueba
   (5 de 5 hallazgos verificables). No uses `kimi-k3`: es caro.

## Cómo se lanza

Un `workflow` con un solo agente. Sin `parallel` salvo que los modelos sean de
pago: los gratis fallan en silencio (`longcat`, `beam` devolvieron `null`).

```js
const schema = {
  type: "object",
  properties: {
    veredicto: { type: "string" },
    defectos: { type: "array", items: {
      type: "object",
      properties: {
        titulo: { type: "string" },
        evidencia: { type: "string" },
        severidad: { type: "string", enum: ["bloqueante", "importante", "menor"] }
      },
      required: ["titulo", "evidencia", "severidad"], additionalProperties: false } },
    lo_que_el_autor_mas_probablemente_ignoro: { type: "array", items: { type: "string" } }
  },
  required: ["veredicto", "defectos", "lo_que_el_autor_mas_probablemente_ignoro"],
  additionalProperties: false
};

const prompt = `Eres un revisor independiente. No existe ninguna revisión previa:
ignora cualquier conclusión que creas adivinar.

ARTEFACTO: <ruta absoluta>
REPOSITORIO: C:\\Users\\sergi\\Documents\\Code\\B2

PROHIBIDO leer <ficheros donde está mi análisis>.

MÉTODO: comprueba cada afirmación del artefacto contra el repo. Si puedes,
valida los ficheros de configuración contra su esquema real.

REGLAS: solo defectos demostrables (fichero y línea, glob, campo de esquema).
Cero opiniones de estilo. Severidad: bloqueante / importante / menor.
En el último campo, di qué dos cosas crees que el autor pasó por alto.

Responde en español, directo, sin relleno.`;

const r = await agent(prompt, {
  label: "revisor-ciego",
  provider: "opencode-go",
  model: "mimo-v2.6-flash",
  schema
});
return r ?? { error: "sin respuesta" };
```

## Qué hacer con el resultado

1. **Verifica cada hallazgo** antes de aceptarlo. En la primera prueba, 2 de 3
   divergencias se cayeron al abrir un fichero.
2. **Distingue el hecho de la severidad.** Los dos modelos coincidieron en el
   defecto y discreparon en si era bloqueante.
3. **Aplica** lo que sobreviva y di al usuario qué cambiaste.
4. **No reabras** una decisión ya cerrada en `AGENTS.md` §2.1.

## Lo que se aprendió (no repetir)

| Modelo | Resultado |
|---|---|
| `mimo-v2.6-flash` | encontró 2 errores reales en el README y un defecto de datos |
| `qwen3.7-plus` | un falso «bloqueante»: se fio del esquema y no de la documentación |
| `minimax-m3` | útil, pero copió conclusiones del README y mezcló caracteres chinos |
| `longcat-2.5-preview-free` | `null`, con esquema y sin él, solo y en grupo |
| `beam-free` | `null` |
| `kimi-k3` | caro |

Contaminación: si el análisis ya está escrito en el repo, el revisor lo lee y
deja de ser ciego. Para repetir en serio, copia el artefacto a una carpeta
aparte y prohíbe el resto del repo.
