// Render rollup/midi-rollup.svg to a PNG preview and a print-size PDF (850 x 2000 mm).
// Usage: node scripts/export_rollup.cjs
const { chromium } = require("playwright");
const { readFileSync } = require("node:fs");

(async () => {

const svg = readFileSync("rollup/midi-rollup.svg", "utf8");
const html = (w, h) => `<html><body style="margin:0">${svg.replace(/width="850mm" height="2000mm"/, `width="${w}" height="${h}"`)}</body></html>`;

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 850, height: 2000 }, deviceScaleFactor: 1.2 });
await page.setContent(html("850", "2000"));
await page.screenshot({ path: "rollup/midi-rollup-preview.png" });

await page.setContent(html("850mm", "2000mm"));
await page.pdf({ path: "rollup/midi-rollup.pdf", width: "850mm", height: "2000mm", printBackground: true, pageRanges: "1" });
await browser.close();
})();
