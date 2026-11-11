"""Generate the MediSoft Facebook posts (1080 x 1350, 4:5 feed format) as HTML pages.

Style follows the approved MediSoft A4 flyer: navy + blue, Plus Jakarta Sans for French,
Kufam / Alexandria for Arabic, real software screenshots. Edit the wording below, then:
  python3 scripts/build_medisoft_flyers.py && node scripts/export_medisoft_flyers.cjs
"""
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent / "flyers/medisoft/src"

PHONE, EMAIL, WEB = "0550 35 34 31", "contact@mediserv.net", "mediserv.net"

# 24x24 line icons (stroke only).
I = {
    "pulse": '<path d="M4 26 H14 L18 16 L24 34 L30 10 L34 26 H44" fill="none" stroke="#5B9BFF" stroke-width="4.2" stroke-linecap="round" stroke-linejoin="round"/>',
    "patient": '<circle cx="9" cy="8" r="3.5"/><path d="M3 20c0-3.5 2.7-6 6-6s6 2.5 6 6M16 7h5M16 11h5M18 15h3"/>',
    "calendar": '<rect x="3" y="5" width="18" height="16" rx="3"/><path d="M3 10h18M8 3v4M16 3v4M7.5 14h3M13.5 14h3M7.5 17.5h3"/>',
    "rx": '<rect x="4" y="3" width="16" height="18" rx="3"/><path d="M9 17V8h3a2.5 2.5 0 0 1 0 5H9M12 13l4 4"/>',
    "receipt": '<path d="M6 3h12v18l-3-2-3 2-3-2-3 2z"/><path d="M9 8h6M9 12h6M9 16h3"/>',
    "tooth": '<path d="M7 3C4.5 3 3 5 3 7.5c0 3 1.5 4.5 2 7 .5 3 1 6.5 3 6.5s1.6-5 4-5 2 5 4 5 2.5-3.5 3-6.5c.5-2.5 2-4 2-7C21 5 19.5 3 17 3c-2 0-3 1-5 1S9 3 7 3z"/>',
    "box": '<path d="M12 2.5l8.5 4.7v9.6L12 21.5l-8.5-4.7V7.2z"/><path d="M3.5 7.2L12 12l8.5-4.8M12 12v9.5"/>',
    "wifi": '<path d="M2 9a15 15 0 0 1 20 0M5 12.5a10 10 0 0 1 14 0M8.5 16a5 5 0 0 1 7 0"/><circle cx="12" cy="19.5" r=".8"/>',
    "screens": '<rect x="2" y="4" width="13" height="10" rx="2"/><path d="M9 14v3h11a2 2 0 0 0 2-2v-6a2 2 0 0 0-2-2h-5"/>',
    "mobile": '<rect x="6" y="2" width="12" height="20" rx="3"/><path d="M11 18h2"/>',
    "shield": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
    "alert": '<path d="M10.3 4.2L2.5 18a2 2 0 0 0 1.7 3h15.6a2 2 0 0 0 1.7-3L13.7 4.2a2 2 0 0 0-3.4 0z"/><path d="M12 10v4M12 17.5h.01"/>',
    "lang": '<path d="M4 5h9M8.5 3v2M6 5c1 4 4 7 7 8M11 5c-1 4-4 7-7 8M13 21l4-10 4 10M14.5 17h5"/>',
    "tv": '<rect x="2" y="4" width="20" height="13" rx="2"/><path d="M8 21h8M12 17v4M6.5 8.5h4v4h-4z"/>',
    "card": '<rect x="2" y="5" width="20" height="14" rx="3"/><path d="M2 10h20M6 15h4"/>',
    "phone": '<path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2z"/>',
    "mail": '<rect x="2.5" y="5" width="19" height="14" rx="2.5"/><path d="M3 6.5l9 6.5 9-6.5"/>',
    "web": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c-3 3-3 15 0 18M12 3c3 3 3 15 0 18"/>',
    "gift": '<rect x="3" y="8" width="18" height="5" rx="1"/><path d="M5 13v8h14v-8M12 8v13M12 8c-2-4-6-4-6-1.5S9 8 12 8zM12 8c2-4 6-4 6-1.5S15 8 12 8z"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
}


def svg(name, vb=24):
    return f'<svg viewBox="0 0 {vb} {vb}">{I[name]}</svg>'


LOGO = f'<div class="logo"><span class="mark">{svg("pulse", 48)}</span><span>Medi<b>Soft</b></span></div>'
TOP = f'<div class="top">{LOGO}<div class="audience">CABINETS MÉDICAUX<br>DENTAIRE · LABORATOIRES</div></div>'
FOOTER = f"""<div class="footer">
  <div>
    <div class="kicker">Démonstration gratuite</div>
    <h3>Demandez votre démonstration</h3>
    <div class="ar-h">اطلب عرضاً تجريبياً</div>
  </div>
  <div class="contacts">
    <div class="contact"><span>{svg("phone")}</span>{PHONE}</div>
    <div class="contact"><span>{svg("mail")}</span>{EMAIL}</div>
  </div>
</div>"""


def page(title, cls, body, css=""):
    return f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><title>{title}</title>
<link rel="stylesheet" href="style.css"><style>{css}</style></head>
<body><div class="post {cls}">
{body}
</div></body></html>
"""


def hero():
    css = """
    .badge { position: absolute; left: 64px; top: 176px; }
    h1 { position: absolute; left: 64px; top: 250px; font-size: 118px; font-weight: 800; letter-spacing: -5px; line-height: .95; }
    .hero-ar { position: absolute; left: 64px; top: 600px; font-size: 54px; font-weight: 700; }
    .lead { position: absolute; left: 64px; top: 720px; width: 330px; font-size: 25px; line-height: 1.45; color: #C9D6F2; }
    .lead b { color: #fff; }
    .lead .ar { margin-top: 18px; font-size: 22px; line-height: 1.6; text-align: right; color: #C9D6F2; }
    .laptop { position: absolute; left: 400px; top: 722px; width: 640px; }
    .phone { position: absolute; left: 884px; top: 790px; width: 166px; border-width: 7px; border-radius: 28px; }
    .phone img { border-radius: 21px; }
    .pulse-line { position: absolute; left: 0; top: 650px; width: 420px; height: 90px; overflow: visible; }
    """
    body = f"""{TOP}
<div class="badge"><i></i>FONCTIONNE MÊME SANS INTERNET</div>
<h1>Votre cabinet<br>bat au bon<br><span class="blue">rythme.</span></h1>
<div class="hero-ar ar-h">عيادتك تنبض بالإيقاع الصحيح</div>
<div class="lead"><b>Le logiciel de gestion</b> des cabinets médicaux, dentaires et laboratoires en Algérie.
  <div class="ar">برنامج تسيير العيادات الطبية وطب الأسنان والمخابر في الجزائر</div></div>
<div class="laptop shadow"><div class="screen"><img src="img/dashboard.png"></div><div class="base"></div></div>
<div class="phone"><img src="img/phone.png"></div>
{FOOTER}"""
    return page("MediSoft – Votre cabinet bat au bon rythme", "dark", body, css)


FEATURES = [
    ("patient", "Dossiers patients", "Antécédents, allergies, consultations et documents en un clic.", "ملف كامل لكل مريض"),
    ("calendar", "Rendez-vous & file d'attente", "Planning clair, rappels et salle d'attente en direct.", "المواعيد وقاعة الانتظار"),
    ("rx", "Ordonnances & certificats", "Imprimées en français ou en arabe, alerte allergie.", "الوصفات والشهادات الطبية"),
    ("receipt", "Caisse & reçus", "Encaissements, impayés et dépenses suivis au dinar près.", "الصندوق والإيصالات"),
    ("tooth", "Dentaire, ortho & implants", "Schéma dentaire, plans de traitement et séances.", "طب الأسنان والتقويم والزرع"),
    ("box", "Stock & laboratoire", "Alertes péremption, stock bas et travaux de labo.", "المخزون والمخبر"),
]


def features():
    css = """
    .head { position: absolute; left: 64px; top: 172px; right: 64px; }
    h2 { font-size: 60px; font-weight: 800; letter-spacing: -2.4px; line-height: 1.05; }
    .head .ar-h { margin-top: 14px; font-size: 40px; font-weight: 700; text-align: left; }
    .grid { position: absolute; left: 64px; right: 64px; top: 400px; display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }
    .card { background: #fff; border: 1.5px solid var(--line); border-left: 5px solid var(--blue); border-radius: 22px; padding: 22px 24px 18px; height: 186px; box-shadow: 0 10px 30px rgba(14,27,51,.05); }
    .card .row { display: flex; align-items: center; gap: 16px; }
    .card .icon { width: 54px; height: 54px; border-radius: 14px; }
    .card .icon svg { width: 28px; height: 28px; }
    .card h4 { font-size: 24px; font-weight: 700; letter-spacing: -.4px; line-height: 1.15; }
    .card p { margin-top: 12px; font-size: 18px; line-height: 1.4; color: var(--muted); }
    .card .ar { margin-top: 6px; font-size: 22px; font-weight: 600; text-align: left; }
    .chips { position: absolute; left: 64px; right: 64px; top: 1032px; justify-content: space-between; }
    """
    cards = "".join(
        f'<div class="card"><div class="row"><span class="icon">{svg(k)}</span><h4>{t}</h4></div>'
        f'<p>{d}</p><div class="ar">{a}</div></div>' for k, t, d, a in FEATURES)
    chips = "".join(f'<span class="chip">{svg(k)}{t}</span>' for k, t in
                    [("wifi", "Sans internet"), ("screens", "Multi-postes"), ("mobile", "Android & iPhone"), ("shield", "Sauvegarde auto")])
    body = f"""{TOP}
<div class="head"><h2>Tout votre cabinet,<br><span class="blue">un seul logiciel.</span></h2>
<div class="ar-h">كل عيادتك في برنامج واحد</div></div>
<div class="grid">{cards}</div>
<div class="chips">{chips}</div>
{FOOTER}"""
    return page("MediSoft – Tout votre cabinet, un seul logiciel", "light", body, css)


ALGERIA = [
    ("wifi", "Fonctionne sans internet", "Vos données restent au cabinet", "يعمل بدون إنترنت"),
    ("alert", "Alerte allergie", "En rouge, jusqu'à l'ordonnance", "تنبيه الحساسية"),
    ("lang", "Français & arabe", "Interface et ordonnances bilingues", "بالفرنسية والعربية"),
    ("tv", "Écran de salle d'attente", "Tickets numérotés + écran TV", "تذاكر مرقمة وشاشة الانتظار"),
    ("card", "CHIFA & nomenclature", "Nomenclature nationale intégrée", "بطاقة الشفاء والمدونة الوطنية"),
    ("screens", "Plusieurs PC & mobile", "PC, tablette et application Android", "عدة أجهزة وهاتف"),
]


def algeria():
    css = """
    .head { position: absolute; left: 64px; top: 176px; }
    .head .kicker { margin-bottom: 14px; }
    h2 { font-size: 76px; font-weight: 800; letter-spacing: -3px; line-height: 1; }
    .head .ar-h { margin-top: 16px; font-size: 46px; font-weight: 700; text-align: left; }
    .list { position: absolute; left: 64px; top: 432px; width: 600px; display: grid; gap: 14px; }
    .item { display: flex; align-items: center; gap: 20px; background: #fff; border: 1.5px solid var(--line); border-radius: 20px; padding: 14px 20px; height: 108px; }
    .item h4 { font-size: 25px; font-weight: 700; letter-spacing: -.4px; }
    .item p { font-size: 18px; color: var(--muted); margin-top: 3px; }
    .item .txt { flex: 1; }
    .item .ar { font-size: 20px; font-weight: 600; color: var(--blue); text-align: left; margin-top: 2px; }
    .phone { position: absolute; left: 708px; top: 400px; width: 314px; transform: rotate(3deg); }
    .glow { position: absolute; left: 640px; top: 420px; width: 460px; height: 640px; border-radius: 50%; background: radial-gradient(rgba(47,107,240,.30), transparent 65%); }
    """
    items = "".join(
        f'<div class="item"><span class="icon">{svg(k)}</span><div class="txt"><h4>{t}</h4><p>{d}</p>'
        f'<div class="ar">{a}</div></div></div>' for k, t, d, a in ALGERIA)
    body = f"""{TOP}
<div class="head"><div class="kicker">Trilingue · FR / EN / ع</div>
<h2>Pensé pour <span class="blue">l'Algérie.</span></h2>
<div class="ar-h">مصمم للجزائر</div></div>
<div class="glow"></div>
<div class="list">{items}</div>
<div class="phone"><img src="img/phone.png"></div>
{FOOTER}"""
    return page("MediSoft – Pensé pour l'Algérie", "light", body, css)


def pricing():
    css = """
    .head { position: absolute; left: 64px; right: 64px; top: 180px; text-align: center; }
    .head .kicker { margin-bottom: 18px; }
    h2 { font-size: 76px; font-weight: 800; letter-spacing: -3px; line-height: 1; }
    .head .ar-h { margin-top: 16px; font-size: 44px; font-weight: 700; direction: rtl; }
    .plans { position: absolute; left: 64px; right: 64px; top: 470px; display: grid; grid-template-columns: 1fr 1fr; gap: 28px; }
    .plan { border-radius: 30px; padding: 40px 36px; height: 450px; position: relative; }
    .plan.sub { background: rgba(255,255,255,.07); border: 1.5px solid rgba(255,255,255,.18); }
    .plan.life { background: #fff; color: var(--ink); box-shadow: 0 30px 70px rgba(3,10,30,.45); }
    .ribbon { position: absolute; top: -20px; right: 30px; background: var(--blue); color: #fff; font-size: 17px; font-weight: 800; letter-spacing: 3px; padding: 10px 20px; border-radius: 30px; }
    .plan h4 { font-size: 34px; font-weight: 800; letter-spacing: -.8px; }
    .plan .ar-t { font-family: 'Kufam'; font-size: 30px; font-weight: 700; margin-top: 4px; opacity: .85; }
    .price { margin-top: 34px; font-size: 92px; font-weight: 800; letter-spacing: -4px; line-height: 1; white-space: nowrap; }
    .price small { font-size: 30px; letter-spacing: 0; font-weight: 700; margin-left: 6px; }
    .plan.sub .price { color: #fff; }
    .plan.life .price { color: var(--blue); }
    .num { direction: ltr; unicode-bidi: isolate; }
    .price-ar { font-family: 'Alexandria'; direction: rtl; text-align: left; font-size: 26px; font-weight: 600; margin-top: 10px; opacity: .75; }
    .plan ul { list-style: none; margin-top: 34px; display: grid; gap: 16px; }
    .plan li { display: flex; gap: 12px; align-items: center; font-size: 22px; font-weight: 600; }
    .plan li svg { width: 30px; height: 30px; flex: none; padding: 5px; border-radius: 50%; background: var(--blue); fill: none; stroke: #fff; stroke-width: 3; stroke-linecap: round; stroke-linejoin: round; }
    .plan li .ar { font-size: 19px; font-weight: 500; opacity: .7; margin-left: auto; }
    .note { position: absolute; left: 64px; right: 64px; top: 976px; display: flex; justify-content: center; gap: 16px; align-items: center; font-size: 22px; font-weight: 600; color: #C9D6F2; }
    .note svg { width: 30px; height: 30px; fill: none; stroke: var(--sky); stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; }
    .note .ar { color: #fff; }
    .note2 { top: 1024px; }
    """
    tick = svg("check")
    body = f"""{TOP}
<div class="head"><div class="kicker">Tarifs MediSoft</div>
<h2>Choisissez votre <span class="blue">formule.</span></h2>
<div class="ar-h">اختر الصيغة المناسبة لك</div></div>
<div class="plans">
  <div class="plan sub">
    <h4>Abonnement annuel</h4><div class="ar-t">اشتراك سنوي</div>
    <div class="price">24 000<small>DA / an</small></div>
    <div class="price-ar"><span class="num">24 000</span> دج / سنة</div>
    <ul><li>{tick}Paiement chaque année<span class="ar">دفع سنوي</span></li>
        <li>{tick}Démo gratuite<span class="ar">عرض تجريبي مجاني</span></li></ul>
  </div>
  <div class="plan life"><span class="ribbon">MEILLEUR CHOIX</span>
    <h4>Licence à vie</h4><div class="ar-t">رخصة مدى الحياة</div>
    <div class="price">48 000<small>DA</small></div>
    <div class="price-ar"><span class="num">48 000</span> دج · دفعة واحدة</div>
    <ul><li>{tick}Un seul paiement<span class="ar">دفعة واحدة</span></li>
        <li>{tick}Le prix de 2 ans<span class="ar">بسعر سنتين</span></li></ul>
  </div>
</div>
<div class="note">{svg("shield")}Installation et accompagnement par l'équipe MediServ</div>
<div class="note note2"><span class="ar">التركيب والمرافقة من طرف فريق ميديسيرف</span></div>
{FOOTER}"""
    return page("MediSoft – Tarifs", "dark", body, css)


POSTS = {
    "01-hero": hero,
    "02-fonctionnalites": features,
    "03-pense-pour-algerie": algeria,
    "04-tarifs": pricing,
}


def main():
    for name, build in POSTS.items():
        path = SRC / f"medisoft-facebook-{name}.html"
        path.write_text(build())
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
