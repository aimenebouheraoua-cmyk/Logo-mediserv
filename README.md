# MediServ logo

A red heart with a white ECG pulse line, next to the "MediServ" wordmark (Inter Bold, converted to outlines).

| File | Use |
| --- | --- |
| `logo/mediserv-logo.svg` / `.png` | Main logo for light backgrounds |
| `logo/mediserv-logo-white.svg` / `.png` | Logo for dark backgrounds |
| `logo/mediserv-icon.svg`, `logo/mediserv-icon-512.png` | Icon only (app icon, social avatar) |
| `logo/favicon-64.png` | Favicon |

Colors: coral `#FF6B6B` → red `#E63950` (heart gradient, "Serv"), navy `#1E2A4A` ("Medi").

## Regenerating

```sh
pip install fonttools
python3 scripts/build_logo.py          # writes the SVGs
node scripts/export_png.cjs            # renders the PNGs (needs Playwright)
```
