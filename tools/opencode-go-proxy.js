/**
 * Proxy CORS mínimo para OpenCode Go (o cualquier endpoint compatible con OpenAI
 * que no permita llamadas desde el navegador).
 *
 * Por qué hace falta: opencode.ai contesta al preflight con 403 y sin
 * Access-Control-Allow-Origin, así que una página estática (GitHub Pages) no
 * puede llamarlo: el navegador corta la petición antes de enviarla. Desde Python
 * o curl sí funciona, porque ahí no existe CORS. Gemini y DeepSeek directo
 * (api.deepseek.com) sí permiten CORS; OpenCode, no.
 *
 * Despliegue (gratis, ~2 minutos):
 *   1. dash.cloudflare.com → Workers & Pages → Create → Worker.
 *   2. Pega este fichero entero y pulsa Deploy.
 *   3. Settings → Variables and Secrets → añade un SECRETO:
 *        OC_KEY = tu clave de OpenCode (oc_sk_…)
 *      Opcional:
 *        ALLOW_ORIGIN = https://bacuchito.github.io   (restringe quién puede usarlo)
 *        TARGET_URL   = otro endpoint si algún día cambias de proveedor
 *   4. En la app: Proveedor «DeepSeek / OpenAI / OpenRouter»,
 *      Endpoint Base = https://<tu-worker>.workers.dev
 *      (la app añade /chat/completions sola),
 *      Nombre del modelo = deepseek-v4.1-flash,
 *      API Key = cualquier texto (p. ej. «worker»): la clave real vive en el Worker,
 *      no en el navegador.
 *
 * La clave nunca llega al navegador ni al HTML: se queda como secreto del Worker.
 */

export default {
  async fetch(request, env) {
    const origen = env.ALLOW_ORIGIN || "*";
    const cors = {
      "Access-Control-Allow-Origin": origen,
      "Access-Control-Allow-Headers": "authorization, content-type, x-opencode-session",
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Max-Age": "86400",
      "Vary": "Origin",
    };

    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: cors });
    }
    if (request.method !== "POST") {
      return new Response(JSON.stringify({ error: { message: "Solo POST" } }), {
        status: 405, headers: { ...cors, "Content-Type": "application/json" },
      });
    }
    if (!env.OC_KEY) {
      return new Response(JSON.stringify({
        error: { message: "Falta el secreto OC_KEY en el Worker" },
      }), { status: 500, headers: { ...cors, "Content-Type": "application/json" } });
    }

    const destino = env.TARGET_URL
      || "https://opencode.ai/inference/go/openai/v1/chat/completions";
    const cuerpo = await request.text();

    const arriba = await fetch(destino, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + env.OC_KEY,
        // OpenCode Go pide identificar al cliente y una sesión estable.
        "User-Agent": "b2-quiz-proxy/1.0",
        "x-opencode-session": request.headers.get("x-opencode-session") || "b2-quiz-proxy",
      },
      body: cuerpo,
    });

    return new Response(arriba.body, {
      status: arriba.status,
      headers: {
        ...cors,
        "Content-Type": arriba.headers.get("content-type") || "application/json",
      },
    });
  },
};
