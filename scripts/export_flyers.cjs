// Render flyers/*.svg to 1080 x 1350 PNGs for Facebook posts.
// Usage: node scripts/export_flyers.cjs
const { chromium } = require("playwright");
const { readFileSync, readdirSync } = require("node:fs");

(async () => {

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 1 });
for (const file of readdirSync("flyers").filter((f) => f.endsWith(".svg")).sort()) {
  const svg = readFileSync(`flyers/${file}`, "utf8");
  await page.setContent(`<html><body style="margin:0">${svg}</body></html>`);
  await page.evaluate(() => document.fonts.ready);
  const out = `flyers/${file.replace(/\.svg$/, ".png")}`;
  await page.screenshot({ path: out });
  console.log(`wrote ${out}`);
}
await browser.close();
})();
