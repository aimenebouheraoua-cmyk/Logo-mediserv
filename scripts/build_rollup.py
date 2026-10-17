"""Generate the MIDI software roll-up banner (85 x 200 cm) as an SVG.

One SVG unit = 1 mm. The MediServ logo is inlined from logo/mediserv-logo-white.svg.
Edit the TEXT block below to change wording, then re-run and re-export.
Usage: python3 scripts/build_rollup.py && node scripts/export_rollup.cjs
"""
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "rollup"

W, H = 850, 2000
NAVY, NAVY_DEEP, INK = "#1E2A4A", "#121A30", "#2B3A63"
CORAL, RED = "#FF6B6B", "#E63950"
MUTED = "#AEB8D6"

TEXT = {
    "kicker": "MEDICAL MANAGEMENT SOFTWARE",
    "name": "MIDI",
    "tagline": ["Your whole clinic,", "in one rhythm."],
    "features": [
        ("patient", "Patient records", "Complete history in one click"),
        ("calendar", "Appointments", "Smart scheduling & reminders"),
        ("rx", "Prescriptions", "Printed or digital in seconds"),
        ("bill", "Billing", "Invoices & payments"),
        ("chart", "Reports", "Live statistics & lab results"),
        ("shield", "Secure", "Encrypted, backed up daily"),
    ],
    "cta": "Request your free demo",
    "contact": ["www.your-website.com", "+000 000 000 000", "contact@your-email.com"],
}

# Simple 48x48 line icons, drawn in white on a coral disc.
ICONS = {
    "patient": '<circle cx="24" cy="16" r="7"/><path d="M10 40c0-8 6-13 14-13s14 5 14 13"/>',
    "calendar": '<rect x="8" y="11" width="32" height="29" rx="4"/><path d="M8 20h32M16 7v8M32 7v8M16 28h4M28 28h4M16 34h4"/>',
    "rx": '<rect x="8" y="18" width="32" height="13" rx="6.5" transform="rotate(-40 24 24)"/><path d="M19.5 18.5l9 9"/>',
    "bill": '<path d="M12 6h24v36l-4-3-4 3-4-3-4 3-4-3-4 3z"/><path d="M18 16h12M18 23h12M18 30h7"/>',
    "chart": '<path d="M8 40h32M13 34V24M21 34V14M29 34V20M37 34V9"/>',
    "shield": '<path d="M24 6l15 6v10c0 10-6 17-15 20-9-3-15-10-15-20V12z"/><path d="M17 24l5 5 9-10"/>',
}

PULSE = "M0 0 H110 L135 -55 L165 70 L195 -95 L222 40 L240 0 H350"


def logo(x, y, width):
    """Nest the white MediServ logo SVG at (x, y), scaled to `width` mm."""
    src = (ROOT / "logo/mediserv-logo-white.svg").read_text()
    vb = re.search(r'viewBox="([^"]+)"', src).group(1)
    inner = src.split("</title>", 1)[1].rsplit("</svg>", 1)[0]
    vw, vh = map(float, vb.split()[2:])
    return (f'<svg x="{x}" y="{y}" width="{width}" height="{width * vh / vw:.1f}" '
            f'viewBox="{vb}">{inner}</svg>')


def text(x, y, s, size, weight=400, fill="#FFFFFF", anchor="start", extra=""):
    return (f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
            f'text-anchor="{anchor}" {extra}>{escape(s)}</text>')


def laptop(x, y, w):
    """A laptop showing a stylised MIDI dashboard. Screen is w x 0.62w."""
    h = w * 0.62
    sx, sy, sw, sh = x + 14, y + 14, w - 28, h - 28  # screen area inside the bezel
    side = 70
    parts = [
        # Bezel, screen, base.
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="#0B1122"/>',
        f'<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" rx="4" fill="#F4F6FB"/>',
        f'<path d="M{x - 45} {y + h + 4} H{x + w + 45} L{x + w + 25} {y + h + 26} H{x - 25} Z" fill="#C9D0E3"/>',
        f'<rect x="{x - 45}" y="{y + h}" width="{w + 90}" height="8" rx="4" fill="#E3E8F4"/>',
        f'<rect x="{x + w / 2 - 50}" y="{y + h}" width="100" height="6" rx="3" fill="#AEB8D6"/>',
        # Sidebar with the heart icon and menu items.
        f'<rect x="{sx}" y="{sy}" width="{side}" height="{sh}" rx="4" fill="{NAVY}"/>',
        f'<svg x="{sx + 17}" y="{sy + 14}" width="36" height="36" viewBox="0 0 100 100">'
        f'<path d="M50 90 C22 70 6 54 6 34 C6 19 17 8 31 8 C40 8 46 13 50 20 C54 13 60 8 69 8 C83 8 94 19 94 34 C94 54 78 70 50 90 Z" fill="{RED}"/></svg>',
    ]
    for i in range(6):
        fill = CORAL if i == 0 else INK
        parts.append(f'<rect x="{sx + 16}" y="{sy + 72 + i * 38}" width="38" height="20" rx="5" fill="{fill}"/>')
    cx = sx + side + 22  # content left edge
    cw = sx + sw - cx - 22
    parts.append(text(cx, sy + 40, "Good morning, Doctor", 20, 700, NAVY))
    parts.append(f'<rect x="{sx + sw - 170}" y="{sy + 20}" width="148" height="28" rx="14" fill="{RED}"/>')
    parts.append(text(sx + sw - 96, sy + 39, "+ New patient", 14, 600, "#FFFFFF", "middle"))
    # KPI cards.
    kpis = [("Patients today", "24"), ("Appointments", "38"), ("Revenue", "+12%")]
    kw = (cw - 2 * 14) / 3
    for i, (label, value) in enumerate(kpis):
        kx = cx + i * (kw + 14)
        parts.append(f'<rect x="{kx:.1f}" y="{sy + 64}" width="{kw:.1f}" height="74" rx="8" fill="#FFFFFF" stroke="#E1E6F2"/>')
        parts.append(text(f"{kx + 14:.1f}", sy + 88, label, 12, 500, "#6B7699"))
        parts.append(text(f"{kx + 14:.1f}", sy + 124, value, 30, 800, RED if i == 2 else NAVY))
    # Activity chart (pulse-shaped line) and appointment list.
    py = sy + 154
    pw = cw * 0.58
    ph = sh - (py - sy) - 18
    parts.append(f'<rect x="{cx}" y="{py}" width="{pw:.1f}" height="{ph:.1f}" rx="8" fill="#FFFFFF" stroke="#E1E6F2"/>')
    parts.append(text(cx + 14, py + 24, "Weekly activity", 13, 700, NAVY))
    base = py + ph - 26
    pts = [0, 0.35, 0.25, 0.6, 0.45, 0.8, 0.55, 0.9, 0.7]
    step = (pw - 28) / (len(pts) - 1)
    line = " ".join(f"{cx + 14 + i * step:.1f},{base - v * (ph - 70):.1f}" for i, v in enumerate(pts))
    area = f"{cx + 14},{base} {line} {cx + 14 + (len(pts) - 1) * step:.1f},{base}"
    parts.append(f'<polygon points="{area}" fill="{CORAL}" opacity="0.15"/>')
    parts.append(f'<polyline points="{line}" fill="none" stroke="{RED}" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"/>')
    lx, lw = cx + pw + 14, cw - pw - 14
    parts.append(f'<rect x="{lx:.1f}" y="{py}" width="{lw:.1f}" height="{ph:.1f}" rx="8" fill="#FFFFFF" stroke="#E1E6F2"/>')
    parts.append(text(f"{lx + 14:.1f}", py + 24, "Next appointments", 13, 700, NAVY))
    for i, t in enumerate(["09:00", "09:30", "10:15"]):
        ry = py + 44 + i * 36
        parts.append(f'<circle cx="{lx + 26:.1f}" cy="{ry + 10}" r="10" fill="{CORAL if i == 0 else "#D5DBEA"}"/>')
        parts.append(f'<rect x="{lx + 44:.1f}" y="{ry + 4}" width="{lw - 120:.1f}" height="12" rx="6" fill="#E6EAF4"/>')
        parts.append(text(f"{lx + lw - 14:.1f}", ry + 15, t, 12, 600, "#6B7699", "end"))
    return "\n".join(parts)


def feature(x, y, icon, title, sub):
    return "\n".join([
        f'<circle cx="{x + 38}" cy="{y + 38}" r="38" fill="url(#coral)"/>',
        f'<svg x="{x + 14}" y="{y + 14}" width="48" height="48" viewBox="0 0 48 48" fill="none" '
        f'stroke="#FFFFFF" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round">{ICONS[icon]}</svg>',
        text(x + 94, y + 34, title, 30, 700),
        text(x + 94, y + 66, sub, 19, 400, MUTED),
    ])


def main():
    t = TEXT
    body = [
        f'<rect width="{W}" height="{H}" fill="url(#bg)"/>',
        # Faint oversized pulse line behind the hero.
        f'<path d="{PULSE}" transform="translate(-60 470) scale(2.8)" fill="none" stroke="#FFFFFF" '
        'stroke-opacity="0.05" stroke-width="9" stroke-linejoin="round" stroke-linecap="round"/>',
        logo(185, 95, 480),
        text(W / 2, 330, t["kicker"], 24, 700, CORAL, "middle", 'letter-spacing="6"'),
        text(W / 2, 545, t["name"], 250, 900, "#FFFFFF", "middle", 'letter-spacing="-6"'),
        # Coral pulse underline.
        f'<path d="{PULSE}" transform="translate(250 615) scale(1 0.42)" fill="none" stroke="url(#coralh)" '
        'stroke-width="9" stroke-linejoin="round" stroke-linecap="round" vector-effect="non-scaling-stroke"/>',
        text(W / 2, 715, t["tagline"][0], 50, 600, "#FFFFFF", "middle"),
        text(W / 2, 778, t["tagline"][1], 50, 600, CORAL, "middle"),
        laptop(140, 850, 570),
    ]
    fy, col = 1280, [70, 455]
    for i, (icon, title, sub) in enumerate(t["features"]):
        body.append(feature(col[i % 2], fy + (i // 2) * 125, icon, title, sub))
    # Call to action band; kept above ~1850 mm so the base cassette does not hide it.
    cy = 1670
    body += [
        f'<rect x="50" y="{cy}" width="{W - 100}" height="190" rx="28" fill="url(#coral)"/>',
        text(85, cy + 66, t["cta"], 42, 800),
        f'<rect x="85" y="{cy + 86}" width="80" height="5" rx="2.5" fill="#FFFFFF" opacity="0.7"/>',
    ]
    for i, line in enumerate(t["contact"]):
        body.append(text(85, cy + 125 + i * 26, line, 21, 600 if i == 0 else 500))
    # QR code placeholder: replace with the real QR before printing.
    qx, qy, qs = W - 85 - 150, cy + 20, 150
    body += [
        f'<rect x="{qx}" y="{qy}" width="{qs}" height="{qs}" rx="12" fill="#FFFFFF"/>',
        f'<rect x="{qx + 14}" y="{qy + 14}" width="{qs - 28}" height="{qs - 28}" rx="6" fill="none" '
        f'stroke="{NAVY}" stroke-width="2" stroke-dasharray="8 6"/>',
        text(qx + qs / 2, qy + qs / 2 + 9, "QR CODE", 22, 800, NAVY, "middle"),
        # Footer zone, partly hidden by the stand's base.
        text(W / 2, 1915, "MediServ · MIDI", 20, 500, MUTED, "middle", 'letter-spacing="3"'),
    ]
    defs = f"""<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{NAVY}"/><stop offset="1" stop-color="{NAVY_DEEP}"/>
  </linearGradient>
  <linearGradient id="coral" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{CORAL}"/><stop offset="1" stop-color="{RED}"/>
  </linearGradient>
  <linearGradient id="coralh" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{CORAL}"/><stop offset="1" stop-color="{RED}"/>
  </linearGradient>
</defs>"""
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}mm" height="{H}mm" '
           f'font-family="Inter, sans-serif">\n<title>MIDI roll-up</title>\n{defs}\n' + "\n".join(body) + "\n</svg>\n")
    OUT.mkdir(exist_ok=True)
    (OUT / "midi-rollup.svg").write_text(svg)
    print(f"wrote {OUT / 'midi-rollup.svg'}")


if __name__ == "__main__":
    main()
