// Screenshots of live project sites through Chrome's DevTools protocol.
// Hides cookie banners, scrolls once so scroll-triggered animations run, then captures.
import { spawn } from "node:child_process";
import { writeFileSync, mkdirSync } from "node:fs";

const OUT = process.argv[2];
const SITES = JSON.parse(process.argv[3]);
const CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const PORT = 9333;
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
mkdirSync(OUT, { recursive: true });

const chrome = spawn(CHROME, ["--headless=new", "--disable-gpu", "--hide-scrollbars", `--remote-debugging-port=${PORT}`,
  `--user-data-dir=${OUT}/.profile`, "--no-first-run", "about:blank"], { stdio: "ignore" });

let last;
async function json(path, method = "GET") {
  for (let i = 0; i < 50; i++) {
    try { const t = await (await fetch(`http://127.0.0.1:${PORT}${path}`, { method, signal: AbortSignal.timeout(5000) })).text(); try { return JSON.parse(t); } catch { return t; } } catch (e) { last = e; await sleep(200); }
  }
  throw new Error("DevTools request failed: " + path + " " + (last && last.cause ? last.cause.message : last));
}

function connect(wsUrl) {
  const ws = new WebSocket(wsUrl);
  let id = 0; const waiting = new Map();
  ws.onmessage = (e) => { const m = JSON.parse(e.data); if (m.id && waiting.has(m.id)) { waiting.get(m.id)(m); waiting.delete(m.id); } };
  const send = (method, params = {}) => new Promise((res) => { const i = ++id; waiting.set(i, res); ws.send(JSON.stringify({ id: i, method, params })); });
  return new Promise((res) => { ws.onopen = () => res({ send, close: () => ws.close() }); });
}

const PREPARE = (scroll) => `(async () => {
  const sleep = (ms) => new Promise(r => setTimeout(r, ms));
  for (const el of document.querySelectorAll('body *')) {
    const cs = getComputedStyle(el);
    if ((cs.position === 'fixed' || cs.position === 'sticky') && /cookie|consent|gdpr|privacy preferences/i.test(el.textContent || '') && el.textContent.length < 3000) el.remove();
  }
  document.querySelectorAll('#termly-code-snippet-support, .termly-styles-root, [id*="cookie" i], [class*="cookie-banner" i], [class*="cky-" i], #cmplz-cookiebanner-container').forEach(e => e.remove());
  if (${scroll}) {
    const h = document.documentElement.scrollHeight;
    for (let y = 0; y < h; y += 500) { window.scrollTo(0, y); await sleep(120); }
    window.scrollTo(0, 0); await sleep(1500);
  } else if (${Number(process.env.SCROLL_Y || 0)} > 0) {
    const t = ${Number(process.env.SCROLL_Y || 0)};
    for (let y = 0; y <= t; y += 250) { window.scrollTo(0, y); await sleep(120); }
    window.scrollTo(0, t); await sleep(3000);
  } else { await sleep(800); }
  return document.documentElement.scrollHeight;
})()`;

async function shoot(site, view) {
  const target = await json(`/json/new?about:blank`, "PUT");
  const cdp = await connect(target.webSocketDebuggerUrl);
  await cdp.send("Page.enable");
  await cdp.send("Emulation.setDeviceMetricsOverride", { width: view.w, height: view.h, deviceScaleFactor: 1, mobile: view.mobile });
  if (view.mobile) await cdp.send("Emulation.setUserAgentOverride", { userAgent: "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1" });
  await cdp.send("Page.navigate", { url: site.url });
  await sleep(Number(process.env.LOAD_WAIT || 7000));
  const r = await cdp.send("Runtime.evaluate", { expression: PREPARE(!!view.maxH), awaitPromise: true, returnByValue: true });
  const fullH = Math.min(r.result?.result?.value || view.h, view.maxH || view.h);
  // Full pages: clip the whole document. Screen-sized shots: whatever is in the viewport (it may be scrolled).
  const shot = await cdp.send("Page.captureScreenshot", view.maxH
    ? { format: "png", captureBeyondViewport: true, clip: { x: 0, y: 0, width: view.w, height: fullH, scale: 1 } }
    : { format: "png" });
  writeFileSync(`${OUT}/${site.name}-${view.name}.png`, Buffer.from(shot.result.data, "base64"));
  cdp.close();
  await json(`/json/close/${target.id}`).catch(() => {});
  console.log("saved", `${site.name}-${view.name}.png`, view.maxH ? `(${fullH}px tall)` : "");
}

const ONLY = process.argv[4] ? process.argv[4].split(",") : null;
const VIEWS = [
  { name: "desktop", w: 1440, h: 900, mobile: false },
  { name: "full", w: 1440, h: 900, mobile: false, maxH: 6000 },
  { name: "mobile", w: 390, h: 844, mobile: true },
  { name: "tall", w: 1440, h: 2400, mobile: false },
  { name: "long", w: 1440, h: 900, mobile: false, maxH: 17000 },
];
try {
  await json("/json/version");
  for (const site of SITES) for (const view of VIEWS.filter((v) => !ONLY || ONLY.includes(v.name))) {
    try { await Promise.race([shoot(site, view), sleep(Number(process.env.SHOT_TIMEOUT || 60000)).then(() => { throw new Error("timed out"); })]); }
    catch (e) { console.log("FAILED", site.name, view.name, e.message); }
  }
} finally { chrome.kill(); }
