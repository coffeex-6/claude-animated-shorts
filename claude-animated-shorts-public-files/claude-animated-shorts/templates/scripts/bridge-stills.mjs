// usage: node scripts/bridge-stills.mjs <outPrefix> <frame,frame,...> [scale]
// Optional env: REMOTION_TMP, CHROME_PATH, REMOTION_BROWSER_EXECUTABLE,
// BRIDGE_ENTRY, BRIDGE_COMPOSITION_ID.
import fs from "node:fs";
import path from "node:path";

if (process.env.REMOTION_TMP) {
  fs.mkdirSync(process.env.REMOTION_TMP, { recursive: true });
  process.env.TEMP = process.env.TMP = process.env.REMOTION_TMP;
}

const candidates = [
  process.env.CHROME_PATH,
  process.env.REMOTION_BROWSER_EXECUTABLE,
  "C:/Program Files/Google/Chrome/Application/chrome.exe",
  "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
  process.env.LOCALAPPDATA ? path.join(process.env.LOCALAPPDATA, "Google/Chrome/Application/chrome.exe") : null,
  process.env.PROGRAMFILES ? path.join(process.env.PROGRAMFILES, "Google/Chrome/Application/chrome.exe") : null,
  process.env["PROGRAMFILES(X86)"] ? path.join(process.env["PROGRAMFILES(X86)"], "Google/Chrome/Application/chrome.exe") : null
].filter(Boolean);
const browserExecutable = candidates.find(p => fs.existsSync(p));
if (!browserExecutable) {
  throw new Error("Chrome was not found. Install Google Chrome or set CHROME_PATH to the full chrome.exe path.");
}

const { bundle } = await import("@remotion/bundler");
const { renderStill, selectComposition } = await import("@remotion/renderer");

const [prefix, frames, scale = "0.5"] = process.argv.slice(2);
if (!prefix || !frames) {
  throw new Error("Usage: node scripts/bridge-stills.mjs <outPrefix> <frame,frame,...> [scale]");
}
const chromiumOptions = { gl: "angle" };
const serveUrl = await bundle({
  entryPoint: path.resolve(process.env.BRIDGE_ENTRY || "src/index.ts"),
  publicDir: path.resolve("public")
});
const compositionId = process.env.BRIDGE_COMPOSITION_ID || "BridgeShort";
const composition = await selectComposition({ serveUrl, id: compositionId, browserExecutable, chromiumOptions });
const onBrowserLog = (l) => {
  if (l.type === "error" || l.type === "warning") console.log(`[${l.type}]`, l.text.slice(0, 300));
};
for (const f of frames.split(",").map(Number)) {
  if (!Number.isInteger(f) || f < 0 || f >= composition.durationInFrames) {
    throw new Error(`Frame ${f} is outside composition duration (${composition.durationInFrames} frames).`);
  }
  const t0 = Date.now();
  await renderStill({
    composition, serveUrl, frame: f, output: `${prefix}${f}.jpg`,
    imageFormat: "jpeg", jpegQuality: 88, scale: Number(scale),
    browserExecutable, chromiumOptions, timeoutInMilliseconds: 180000, onBrowserLog
  });
  console.log("still", f, ((Date.now() - t0) / 1000).toFixed(1) + "s");
}
