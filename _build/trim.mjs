// Trim empty margins (transparent or near-white) around logo images, using a canvas in headless Chrome.
// Usage: node trim.mjs <dir> <file> [<file> ...]   Writes <name>-trim.png next to each file.
// ALPHA_ONLY=1 keeps white pixels (for white-on-transparent logos) and trims transparency only.
import { spawn } from "node:child_process";
import { writeFileSync, mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const [dir, ...files] = process.argv.slice(2);
const PORT = 9335;
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const profile = mkdtempSync(join(tmpdir(), "trim-"));
const chrome = spawn("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  ["--headless=new", "--disable-gpu", `--remote-debugging-port=${PORT}`, `--user-data-dir=${profile}`,
   "--allow-file-access-from-files", "about:blank"], { stdio: "ignore" });

async function http(path, method = "GET") {
  for (let i = 0; i < 50; i++) {
    try { const t = await (await fetch(`http://127.0.0.1:${PORT}${path}`, { method, signal: AbortSignal.timeout(5000) })).text();
          try { return JSON.parse(t); } catch { return t; } } catch { await sleep(200); }
  }
  throw new Error("Chrome DevTools not reachable");
}

const TRIM = (src) => `new Promise((done) => {
  const img = new Image();
  img.onload = () => {
    const c = document.createElement("canvas"); c.width = img.naturalWidth; c.height = img.naturalHeight;
    const g = c.getContext("2d"); g.drawImage(img, 0, 0);
    const d = g.getImageData(0, 0, c.width, c.height).data;
    let x0 = c.width, y0 = c.height, x1 = -1, y1 = -1;
    for (let y = 0; y < c.height; y++) for (let x = 0; x < c.width; x++) {
      const i = (y * c.width + x) * 4;
      const ink = d[i + 3] > 16 && (${process.env.ALPHA_ONLY ? 'true' : 'false'} || !(d[i] > 242 && d[i + 1] > 242 && d[i + 2] > 242));
      if (ink) { if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y; }
    }
    const pad = Math.round(Math.max(x1 - x0, y1 - y0) * 0.03);
    x0 = Math.max(0, x0 - pad); y0 = Math.max(0, y0 - pad); x1 = Math.min(c.width - 1, x1 + pad); y1 = Math.min(c.height - 1, y1 + pad);
    const o = document.createElement("canvas"); o.width = x1 - x0 + 1; o.height = y1 - y0 + 1;
    o.getContext("2d").drawImage(c, x0, y0, o.width, o.height, 0, 0, o.width, o.height);
    done({ data: o.toDataURL("image/png"), from: [c.width, c.height], to: [o.width, o.height] });
  };
  img.src = ${JSON.stringify(src)};
})`;

try {
  const target = await http("/json/new?about:blank", "PUT");
  const ws = new WebSocket(target.webSocketDebuggerUrl);
  await new Promise((r) => (ws.onopen = r));
  let id = 0; const waiting = new Map();
  ws.onmessage = (e) => { const m = JSON.parse(e.data); if (waiting.has(m.id)) { waiting.get(m.id)(m); waiting.delete(m.id); } };
  const send = (method, params = {}) => new Promise((res) => { const i = ++id; waiting.set(i, res); ws.send(JSON.stringify({ id: i, method, params })); });
  await send("Page.navigate", { url: "file://" + join(dir, files[0]) });
  await sleep(800);
  for (const f of files) {
    const r = await send("Runtime.evaluate", { expression: TRIM("file://" + join(dir, f)), awaitPromise: true, returnByValue: true });
    const v = r.result.result.value;
    const out = f.replace(/\.[a-z]+$/, "-trim.png");
    writeFileSync(join(dir, out), Buffer.from(v.data.split(",")[1], "base64"));
    console.log(f, v.from.join("x"), "->", out, v.to.join("x"));
  }
  ws.close();
} finally { chrome.kill(); }
