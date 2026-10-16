// Render logo/*.svg to PNG with headless Chromium. Usage: node scripts/export_png.cjs
const { chromium } = require("playwright");
const { readFileSync } = require("node:fs");

(async () => {

const exports = [
  ["logo/mediserv-logo.svg", "logo/mediserv-logo.png", 4, "transparent"],
  ["logo/mediserv-logo-white.svg", "logo/mediserv-logo-white.png", 4, "transparent"],
  ["logo/mediserv-icon.svg", "logo/mediserv-icon-512.png", 5.12, "transparent"],
  ["logo/mediserv-icon.svg", "logo/favicon-64.png", 0.64, "transparent"],
];

const browser = await chromium.launch();
for (const [src, out, scale] of exports) {
  const svg = readFileSync(src, "utf8");
  const [, w, h] = svg.match(/viewBox="0 0 ([\d.]+) ([\d.]+)"/).map(Number);
  const page = await browser.newPage({ viewport: { width: Math.round(w * scale), height: Math.round(h * scale) } });
  const sized = svg.replace(/width="[\d.]+" height="[\d.]+"/, 'width="100%" height="100%"');
  await page.setContent(`<html><body style="margin:0;background:transparent">${sized}</body></html>`);
  await page.screenshot({ path: out, omitBackground: true });
  await page.close();
}
await browser.close();
})();
