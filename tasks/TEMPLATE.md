# <Nombre del trabajo>

Rama: `<rama>`. Base: `<rama>` en `<commit>`.

## Contrato

- **Objetivo:** <qué se construye, en una frase>.
- **Qué se rechaza:** <lo que este trabajo no hace>.
- **Cierre:** <cómo se sabe que terminó>.

## Regla de trabajo

Cada tarea deja <el proyecto> funcionando. Se cierra con:

```powershell
<los controles del repo>
```

<Quién> revisa <qué> antes de pasar a la siguiente tarea.

---

## Tarea 1: <título>

**Descripción:** <qué cambia, en una o dos frases>.
**Aceptación:**
- [ ] <resultado observable>.
- [ ] <resultado observable>.
**Verificación:** <control o captura>.
**Depende de:** <ID o —>. **Archivos:** <rutas>. **Alcance:** S (una sesión) o M (varias).

---

## Puntos de control

| Después de | Se revisa | Si falla |
|---|---|---|
| T1 | <qué> | <qué se corrige> |

## Registro

Escribe una línea por tarea al cerrarla, con el resultado observado, fallos incluidos.

- **T1** — `<comando>`: <resultado>. Commit `<sha>`.

## Fuera de alcance

- <qué no se hará y por qué>.
