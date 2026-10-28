// Screen-by-screen captures of a page: node walk.mjs <outdir> <url> <width> <height> [step] [maxShots]
import { spawn } from "node:child_process";
import { writeFileSync, mkdirSync } from "node:fs";
const [OUT, URL, W, H, STEP, MAX] = process.argv.slice(2);
const width = +W, height = +H, step = +(STEP || H), maxShots = +(MAX || 40);
const CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", PORT = +(process.env.PORT || 9334);   // PORT=… if 9334 is taken
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
mkdirSync(OUT, { recursive: true });
const chrome = spawn(CHROME, ["--headless=new", "--hide-scrollbars", `--remote-debugging-port=${PORT}`, `--user-data-dir=${OUT}/.profile`, "--no-first-run", "about:blank"], { stdio: "ignore" });
async function json(path, method = "GET") {
  for (let i = 0; i < 60; i++) { try { const t = await (await fetch(`http://127.0.0.1:${PORT}${path}`, { method, signal: AbortSignal.timeout(4000) })).text(); try { return JSON.parse(t); } catch { return t; } } catch { await sleep(250); } }
  throw new Error("devtools " + path);
}
try {
  const target = await json("/json/new?about:blank", "PUT");
  const ws = new WebSocket(target.webSocketDebuggerUrl); let id = 0; const wait = new Map();
  ws.onmessage = (e) => { const m = JSON.parse(e.data); if (m.id && wait.has(m.id)) { wait.get(m.id)(m); wait.delete(m.id); } };
  await new Promise((r) => (ws.onopen = r));
  const send = (method, params = {}) => new Promise((res) => { const i = ++id; wait.set(i, res); ws.send(JSON.stringify({ id: i, method, params })); });
  const mobile = width < 768;
  await send("Emulation.setDeviceMetricsOverride", { width, height, deviceScaleFactor: mobile ? 2 : 1, mobile });
  if (mobile) {   // look like an iPhone to the page, touch included
    await send("Emulation.setUserAgentOverride", { userAgent: "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1" });
    await send("Emulation.setTouchEmulationEnabled", { enabled: true, maxTouchPoints: 5 });
  }
  await send("Page.navigate", { url: URL });
  await sleep(6000);
  const evalv = async (x) => (await send("Runtime.evaluate", { expression: x, awaitPromise: true, returnByValue: true })).result?.result?.value;
  const total = await evalv("document.documentElement.scrollHeight");
  let n = 0;
  for (let y = 0; y < total && n < maxShots; y += step, n++) {
    await evalv(`(async()=>{ const go = (v) => window.lenis ? window.lenis.scrollTo(v, { immediate: true, force: true }) : window.scrollTo(0, v); for (let k=0;k<4;k++){ go(${y} - 300 + k*100); await new Promise(r=>setTimeout(r,90)); } go(${y}); await new Promise(r=>setTimeout(r,1400)); return 1; })()`);
    if (process.env.PROBE) console.log(y, JSON.stringify(await evalv(process.env.PROBE)));
    const shot = await Promise.race([send("Page.captureScreenshot", { format: "jpeg", quality: 70 }), sleep(15000).then(() => null)]);
    if (shot && shot.result) writeFileSync(`${OUT}/${String(n).padStart(2, "0")}_${y}.jpg`, Buffer.from(shot.result.data, "base64"));
    else console.log("timeout at", y);
  }
  console.log("total", total, "shots", n);
  ws.close();
} finally { chrome.kill(); }
