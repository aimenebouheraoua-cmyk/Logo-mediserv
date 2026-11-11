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

## MIDI roll-up banner

`rollup/midi-rollup.svg` / `.pdf` is an 85 × 200 cm roll-up for the MIDI software (1 SVG unit = 1 mm), with a PNG preview in `rollup/midi-rollup-preview.png`. Wording lives in the `TEXT` block of `scripts/build_rollup.py`; the website, phone, email and QR code are placeholders to replace before printing.

```sh
python3 scripts/build_rollup.py        # writes rollup/midi-rollup.svg
node scripts/export_rollup.cjs         # renders the preview PNG and print PDF
```

## MediSoft Facebook posts

`flyers/medisoft/medisoft-facebook-*.png` are four 1080 × 1350 (4:5) feed posts in French and Arabic, in the style of the approved MediSoft A4 flyer: hero, fonctionnalités, « Pensé pour l'Algérie » and tarifs (24 000 DA / an, 48 000 DA à vie). Ready-to-paste captions are in `flyers/medisoft/captions.md`.

The pages are HTML in `flyers/medisoft/src/` (shared `style.css`, bundled Google Fonts, real software screenshots in `img/`). Wording lives in `scripts/build_medisoft_flyers.py`.

```sh
python3 scripts/build_medisoft_flyers.py   # writes flyers/medisoft/src/*.html
node scripts/export_medisoft_flyers.cjs     # renders flyers/medisoft/*.png
```
