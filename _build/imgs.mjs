// List the images a page shows once its scripts have run (img sources and CSS backgrounds), largest first.
// Usage: node imgs.mjs <url>
import { spawn } from "node:child_process";
import { mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const PORT = 9336;
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const chrome = spawn("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  ["--headless=new", "--disable-gpu", `--remote-debugging-port=${PORT}`, `--user-data-dir=${mkdtempSync(join(tmpdir(), "imgs-"))}`, "about:blank"],
  { stdio: "ignore" });

async function http(path, method = "GET") {
  for (let i = 0; i < 50; i++) {
    try { const t = await (await fetch(`http://127.0.0.1:${PORT}${path}`, { method, signal: AbortSignal.timeout(5000) })).text();
          try { return JSON.parse(t); } catch { return t; } } catch { await sleep(200); }
  }
  throw new Error("Chrome DevTools not reachable");
}

const LIST = `(async () => {
  for (let y = 0; y < document.documentElement.scrollHeight; y += 600) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 150)); }
  await new Promise(r => setTimeout(r, 2000));
  const seen = new Map();
  for (const img of document.images) if (img.currentSrc && img.naturalWidth >= 400) seen.set(img.currentSrc, img.naturalWidth * img.naturalHeight);
  for (const el of document.querySelectorAll("*")) {
    const m = getComputedStyle(el).backgroundImage.match(/url\\("?([^")]+)"?\\)/);
    if (m && !seen.has(m[1])) seen.set(m[1], el.offsetWidth * el.offsetHeight);
  }
  return [...seen].sort((a, b) => b[1] - a[1]).map(([u]) => u).filter(u => !/logo|icon|\\.svg/i.test(u)).slice(0, 20);
})()`;

try {
  const target = await http("/json/new?about:blank", "PUT");
  const ws = new WebSocket(target.webSocketDebuggerUrl);
  await new Promise((r) => (ws.onopen = r));
  let id = 0; const waiting = new Map();
  ws.onmessage = (e) => { const m = JSON.parse(e.data); if (waiting.has(m.id)) { waiting.get(m.id)(m); waiting.delete(m.id); } };
  const send = (method, params = {}) => new Promise((res) => { const i = ++id; waiting.set(i, res); ws.send(JSON.stringify({ id: i, method, params })); });
  await send("Emulation.setDeviceMetricsOverride", { width: 1440, height: 900, deviceScaleFactor: 1, mobile: false });
  await send("Page.navigate", { url: process.argv[2] });
  await sleep(8000);
  const r = await send("Runtime.evaluate", { expression: LIST, awaitPromise: true, returnByValue: true });
  for (const u of r.result.result.value || []) console.log(u);
  ws.close();
} finally { chrome.kill(); }
