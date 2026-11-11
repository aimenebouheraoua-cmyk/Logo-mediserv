// Render flyers/medisoft/src/*.html to 1080 x 1350 PNGs in flyers/medisoft/.
// Usage: node scripts/export_medisoft_flyers.cjs
const { chromium } = require("playwright");
const { readdirSync } = require("node:fs");
const path = require("node:path");

(async () => {

const src = path.resolve("flyers/medisoft/src");
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
for (const file of readdirSync(src).filter((f) => f.endsWith(".html")).sort()) {
  await page.goto(`file://${src}/${file}`);
  await page.evaluate(() => document.fonts.ready);
  const out = `flyers/medisoft/${file.replace(/\.html$/, ".png")}`;
  await page.screenshot({ path: out });
  console.log(`wrote ${out}`);
}
await browser.close();
})();
