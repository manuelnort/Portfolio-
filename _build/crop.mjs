// Crop regions out of local images with Chrome: show the image at 1:1, capture a clip scaled to the output size.
// Usage: node crop.mjs specs.json   (specs: [{out, src, x, y, w, h, outW, outH}])
import { spawn } from "node:child_process";
import { readFileSync, writeFileSync, mkdtempSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const specs = JSON.parse(readFileSync(process.argv[2], "utf8"));
const PORT = 9334;
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const profile = mkdtempSync(join(tmpdir(), "crop-"));
const chrome = spawn("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  ["--headless=new", "--disable-gpu", "--hide-scrollbars", `--remote-debugging-port=${PORT}`, `--user-data-dir=${profile}`,
   "--allow-file-access-from-files", "about:blank"], { stdio: "ignore" });

async function http(path, method = "GET") {
  for (let i = 0; i < 50; i++) {
    try { const t = await (await fetch(`http://127.0.0.1:${PORT}${path}`, { method, signal: AbortSignal.timeout(5000) })).text();
          try { return JSON.parse(t); } catch { return t; } } catch { await sleep(200); }
  }
  throw new Error("Chrome DevTools not reachable");
}

try {
  const target = await http("/json/new?about:blank", "PUT");
  const ws = new WebSocket(target.webSocketDebuggerUrl);
  await new Promise((r) => (ws.onopen = r));
  let id = 0; const waiting = new Map();
  ws.onmessage = (e) => { const m = JSON.parse(e.data); if (waiting.has(m.id)) { waiting.get(m.id)(m); waiting.delete(m.id); } };
  const send = (method, params = {}) => new Promise((res) => { const i = ++id; waiting.set(i, res); ws.send(JSON.stringify({ id: i, method, params })); });

  for (const s of specs) {
    const html = `<html><body style="margin:0"><img id="i" src="file://${s.src}" style="display:block"></body></html>`;
    const page = join(profile, "page.html");
    writeFileSync(page, html);
    await send("Emulation.setDeviceMetricsOverride", { width: 1600, height: 1000, deviceScaleFactor: 1, mobile: false });
    await send("Page.navigate", { url: "file://" + page });
    let size;
    for (let i = 0; i < 50; i++) {
      await sleep(100);
      const r = await send("Runtime.evaluate", { expression: "(() => { const i = document.getElementById('i'); return i && i.complete && i.naturalWidth ? [i.naturalWidth, i.naturalHeight] : null })()", returnByValue: true });
      size = r.result?.result?.value; if (size) break;
    }
    if (!size) throw new Error("image did not load: " + s.src);
    if (s.x + s.w > size[0] || s.y + s.h > size[1]) throw new Error(`${s.out}: crop outside ${size[0]}x${size[1]}`);
    const shot = await send("Page.captureScreenshot", { format: "png", captureBeyondViewport: true,
      clip: { x: s.x, y: s.y, width: s.w, height: s.h, scale: s.outW / s.w } });
    writeFileSync(s.out, Buffer.from(shot.result.data, "base64"));
    console.log("cropped", s.out.split("/").pop());
  }
  ws.close();
} finally { chrome.kill(); }
