"""Generate Facebook post flyers (1080 x 1350, 4:5 feed format) for the MIDI software.

Reuses the colours, icons and laptop mock-up from build_rollup.py so the flyers match the roll-up.
Edit the TEXT block below to change wording, then re-run and re-export.
Usage: python3 scripts/build_flyers.py && node scripts/export_flyers.cjs
"""
import re
from html import escape
from pathlib import Path

from build_rollup import CORAL, ICONS, INK, MUTED, NAVY, NAVY_DEEP, PULSE, RED, laptop, text

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "flyers"

W, H = 1080, 1350
LIGHT, GREY = "#F4F6FB", "#6B7699"

TEXT = {
    "name": "MIDI",
    "kicker": "MEDICAL MANAGEMENT SOFTWARE",
    "tagline": ["Your whole clinic,", "in one rhythm."],
    "cta": "Request your free demo",
    "website": "www.your-website.com",
    "phone": "+000 000 000 000",
    "email": "contact@your-email.com",
    "features": [
        ("patient", "Patient records", "Full history in one click"),
        ("calendar", "Appointments", "Smart scheduling & reminders"),
        ("rx", "Prescriptions", "Printed or digital in seconds"),
        ("bill", "Billing", "Invoices & payments"),
        ("chart", "Reports", "Live statistics & lab results"),
        ("shield", "Secure", "Encrypted, backed up daily"),
    ],
    "before": ["Paper files everywhere", "Missed appointments", "Handwritten prescriptions",
               "Invoices lost or late", "Hours of paperwork"],
    "after": ["Every record in one click", "Reminders before visits", "Prescriptions in seconds",
              "Every invoice tracked", "More time for patients"],
}

CONTACT_ICONS = {
    "web": '<circle cx="24" cy="24" r="17"/><path d="M7 24h34M24 7c-6 6-6 28 0 34M24 7c6 6 6 28 0 34"/>',
    "phone": '<path d="M14 7h7l3 9-5 3c2 5 5 8 10 10l3-5 9 3v7c0 2-2 4-4 4C21 38 10 27 10 11c0-2 2-4 4-4z"/>',
    "mail": '<rect x="6" y="11" width="36" height="26" rx="4"/><path d="M7 13l17 13 17-13"/>',
}

DEFS = f"""<defs>
  <linearGradient id="navy" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="{NAVY}"/><stop offset="1" stop-color="{NAVY_DEEP}"/>
  </linearGradient>
  <linearGradient id="coral" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{CORAL}"/><stop offset="1" stop-color="{RED}"/>
  </linearGradient>
  <linearGradient id="coralh" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{CORAL}"/><stop offset="1" stop-color="{RED}"/>
  </linearGradient>
  <filter id="shadow" x="-20%" y="-20%" width="140%" height="160%">
    <feDropShadow dx="0" dy="10" stdDeviation="16" flood-color="{NAVY}" flood-opacity="0.10"/>
  </filter>
</defs>"""

HEART = ("M50 90 C22 70 6 54 6 34 C6 19 17 8 31 8 C40 8 46 13 50 20 "
         "C54 13 60 8 69 8 C83 8 94 19 94 34 C94 54 78 70 50 90 Z")


def logo(x, y, width, white=True):
    """Nest the MediServ logo SVG at (x, y), scaled to `width` px."""
    name = "mediserv-logo-white.svg" if white else "mediserv-logo.svg"
    src = (ROOT / "logo" / name).read_text()
    vb = re.search(r'viewBox="([^"]+)"', src).group(1)
    inner = src.split("</title>", 1)[1].rsplit("</svg>", 1)[0]
    vw, vh = map(float, vb.split()[2:])
    return (f'<svg x="{x}" y="{y}" width="{width}" height="{width * vh / vw:.1f}" '
            f'viewBox="{vb}">{inner}</svg>')


def runs(x, y, parts, size, weight=800, anchor="start", extra=""):
    """One line of text made of differently coloured runs: parts = [(string, fill), ...]."""
    spans = "".join(f'<tspan fill="{fill}">{escape(s)}</tspan>' for s, fill in parts)
    return (f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" '
            f'text-anchor="{anchor}" {extra}>{spans}</text>')


def icon(x, y, size, paths, stroke="#FFFFFF", width=3.6):
    return (f'<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="0 0 48 48" fill="none" '
            f'stroke="{stroke}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round">{paths}</svg>')


def disc_icon(cx, cy, r, paths, fill="url(#coral)"):
    s = r * 1.25
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"/>' + icon(cx - s / 2, cy - s / 2, s, paths)


def pill(cx, y, w, h, label, size=32, fill="url(#coral)", color="#FFFFFF"):
    return (f'<rect x="{cx - w / 2}" y="{y}" width="{w}" height="{h}" rx="{h / 2}" fill="{fill}"/>'
            + text(cx, y + h / 2 + size * 0.36, label, size, 800, color, "middle"))


def pulse(x, y, sx=1.0, sy=1.0, stroke="url(#coralh)", width=9, opacity=1.0):
    return (f'<path d="{PULSE}" transform="translate({x} {y}) scale({sx} {sy})" fill="none" '
            f'stroke="{stroke}" stroke-opacity="{opacity}" stroke-width="{width}" '
            'stroke-linejoin="round" stroke-linecap="round" vector-effect="non-scaling-stroke"/>')


def svg(title, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
            f'font-family="Inter, sans-serif">\n<title>{escape(title)}</title>\n{DEFS}\n'
            + "\n".join(body) + "\n</svg>\n")


def flyer_launch(t):
    """Hero post: product name, tagline, laptop mock-up, call to action."""
    body = [
        f'<rect width="{W}" height="{H}" fill="url(#navy)"/>',
        pulse(-120, 560, 3.6, 3.6, "#FFFFFF", 10, 0.05),
        logo(W / 2 - 150, 64, 300),
        text(W / 2, 222, t["kicker"], 22, 700, CORAL, "middle", 'letter-spacing="6"'),
        text(W / 2, 400, t["name"], 200, 900, "#FFFFFF", "middle", 'letter-spacing="-5"'),
        pulse(W / 2 - 175, 452, 1, 0.42),
        text(W / 2, 548, t["tagline"][0], 52, 600, "#FFFFFF", "middle"),
        text(W / 2, 610, t["tagline"][1], 52, 600, CORAL, "middle"),
        laptop(210, 668, 660),
        pill(W / 2, 1150, 560, 86, t["cta"] + "  →", 32),
        text(W / 2, 1296, f'{t["website"]}   ·   {t["phone"]}', 24, 500, MUTED, "middle"),
    ]
    return svg("MIDI launch post", body)


def flyer_features(t):
    """Light post: six feature cards and a navy call-to-action band."""
    body = [
        f'<rect width="{W}" height="{H}" fill="{LIGHT}"/>',
        f'<path d="{HEART}" transform="translate(760 -60) scale(4.2)" fill="{CORAL}" opacity="0.08"/>',
        logo(70, 66, 250, white=False),
        text(70, 238, f'WHY {t["name"]}?', 24, 800, RED, "start", 'letter-spacing="5"'),
        runs(70, 318, [("Everything your clinic", NAVY)], 64),
        runs(70, 394, [("needs. ", NAVY), ("In one place.", RED)], 64),
    ]
    cw, ch, gap, top = 455, 192, 30, 452
    for i, (key, title, sub) in enumerate(t["features"]):
        x = 70 + (i % 2) * (cw + gap)
        y = top + (i // 2) * (ch + 24)
        body += [
            f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="26" fill="#FFFFFF" filter="url(#shadow)"/>',
            disc_icon(x + 66, y + 66, 36, ICONS[key]),
            text(x + 32, y + 144, title, 32, 800, NAVY),
            text(x + 32, y + 174, sub, 21, 500, GREY),
        ]
    by = 1124
    body += [
        f'<rect y="{by}" width="{W}" height="{H - by}" fill="url(#navy)"/>',
        pulse(560, by + 112, 1.6, 0.7, "#FFFFFF", 6, 0.07),
        text(70, by + 92, t["cta"], 42, 800),
        f'<rect x="70" y="{by + 116}" width="80" height="5" rx="2.5" fill="{CORAL}"/>',
        text(70, by + 166, t["website"], 25, 600, "#FFFFFF"),
        text(70, by + 202, t["phone"], 25, 500, MUTED),
        f'<circle cx="{W - 140}" cy="{by + 113}" r="64" fill="url(#coral)"/>',
        icon(W - 140 - 30, by + 113 - 30, 60, '<path d="M10 24h28M28 13l11 11-11 11"/>', width=4.5),
    ]
    return svg("MIDI features post", body)


def flyer_before_after(t):
    """Problem / solution post: paper workflow vs MIDI."""
    body = [
        f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>',
        text(W / 2, 150, "TIME TO GO DIGITAL", 24, 800, RED, "middle", 'letter-spacing="6"'),
        runs(W / 2, 240, [("Still drowning in", NAVY)], 70, anchor="middle"),
        runs(W / 2, 322, [("paper files?", RED)], 70, anchor="middle"),
    ]
    cw, top, ch = 455, 400, 640
    lx, rx = 70, 70 + cw + 30
    cross = '<path d="M16 16l16 16M32 16L16 32"/>'
    check = '<path d="M13 25l7 7 15-15"/>'
    body += [
        f'<rect x="{lx}" y="{top}" width="{cw}" height="{ch}" rx="30" fill="{LIGHT}"/>',
        text(lx + 40, top + 82, "Before", 40, 800, GREY),
        f'<rect x="{rx}" y="{top}" width="{cw}" height="{ch}" rx="30" fill="url(#navy)" filter="url(#shadow)"/>',
        runs(rx + 40, top + 82, [("With ", "#FFFFFF"), (t["name"], CORAL)], 40),
    ]
    for i, (a, b) in enumerate(zip(t["before"], t["after"])):
        y = top + 160 + i * 96
        body += [
            disc_icon(lx + 62, y, 22, cross, fill="#C9D0E3"),
            text(lx + 100, y + 9, a, 24, 600, GREY),
            disc_icon(rx + 62, y, 22, check),
            text(rx + 100, y + 9, b, 24, 600, "#FFFFFF"),
        ]
    body += [
        # Arrow badge between the two cards.
        f'<circle cx="{W / 2}" cy="{top + ch / 2}" r="40" fill="url(#coral)" stroke="#FFFFFF" stroke-width="8"/>',
        icon(W / 2 - 22, top + ch / 2 - 22, 44, '<path d="M10 24h28M28 13l11 11-11 11"/>', width=5),
        logo(70, 1120, 280, white=False),
        pill(W - 70 - 250, 1112, 500, 86, "Book a free demo", 32),
        text(W / 2, 1290, f'{t["website"]}   ·   {t["phone"]}', 24, 500, GREY, "middle"),
    ]
    return svg("MIDI before and after post", body)


def flyer_demo(t):
    """Offer post: coral background, big FREE DEMO, contact card with QR placeholder."""
    body = [
        f'<rect width="{W}" height="{H}" fill="url(#coral)"/>',
        f'<path d="{HEART}" transform="translate(-160 180) scale(8)" fill="#FFFFFF" opacity="0.07"/>',
        pulse(-60, 520, 3.4, 3.4, "#FFFFFF", 10, 0.12),
        # Colour logo on a white pill: the coral heart would vanish into the coral background.
        f'<rect x="{W / 2 - 185}" y="52" width="370" height="104" rx="52" fill="#FFFFFF" filter="url(#shadow)"/>',
        logo(W / 2 - 140, 69, 280, white=False),
        text(W / 2, 236, f'SEE {t["name"]} IN ACTION', 26, 800, "#FFFFFF", "middle", 'letter-spacing="6" opacity="0.9"'),
        text(W / 2, 430, "FREE", 210, 900, "#FFFFFF", "middle", 'letter-spacing="-4"'),
        text(W / 2, 620, "DEMO", 210, 900, NAVY, "middle", 'letter-spacing="-4"'),
        text(W / 2, 708, "At your clinic or online — no commitment.", 36, 600, "#FFFFFF", "middle"),
    ]
    cx, cy, cw, ch = 70, 790, W - 140, 410
    body += [
        f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="32" fill="#FFFFFF" filter="url(#shadow)"/>',
        text(cx + 50, cy + 92, "Book yours today", 44, 800, NAVY),
        f'<rect x="{cx + 50}" y="{cy + 116}" width="80" height="5" rx="2.5" fill="{RED}"/>',
    ]
    for i, (key, label) in enumerate([("web", t["website"]), ("phone", t["phone"]), ("mail", t["email"])]):
        y = cy + 190 + i * 74
        body += [
            f'<circle cx="{cx + 78}" cy="{y}" r="28" fill="{LIGHT}"/>',
            icon(cx + 78 - 17, y - 17, 34, CONTACT_ICONS[key], stroke=RED, width=3.4),
            text(cx + 124, y + 10, label, 28, 600, NAVY),
        ]
    # QR code placeholder: replace with the real QR before posting.
    qs = 240
    qx, qy = cx + cw - 50 - qs, cy + (ch - qs) / 2
    body += [
        f'<rect x="{qx}" y="{qy}" width="{qs}" height="{qs}" rx="16" fill="{LIGHT}"/>',
        f'<rect x="{qx + 16}" y="{qy + 16}" width="{qs - 32}" height="{qs - 32}" rx="8" fill="none" '
        f'stroke="{NAVY}" stroke-width="2.5" stroke-dasharray="10 8"/>',
        text(qx + qs / 2, qy + qs / 2 + 10, "QR CODE", 28, 800, NAVY, "middle"),
        text(W / 2, 1290, f'MediServ · {t["name"]}', 24, 600, "#FFFFFF", "middle", 'letter-spacing="3" opacity="0.85"'),
    ]
    return svg("MIDI free demo post", body)


FLYERS = {
    "01-launch": flyer_launch,
    "02-features": flyer_features,
    "03-before-after": flyer_before_after,
    "04-free-demo": flyer_demo,
}


def main():
    OUT.mkdir(exist_ok=True)
    for name, build in FLYERS.items():
        path = OUT / f"midi-facebook-{name}.svg"
        path.write_text(build(TEXT))
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
