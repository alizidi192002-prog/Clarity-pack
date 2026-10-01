"""French and Spanish Pinterest feeds (_site/pins-fr.xml, _site/pins-es.xml).

After the build, every live /fr/ and /es/ page gets its own 1000x1500 pin image, drawn with
Pillow from the page's title, description and section headings, saved under _site/pins/img/.
Each feed item links to the page and uses that image. If Pillow cannot be loaded the feeds
are skipped and the rest of the build is unaffected.
"""
import atexit, datetime, html, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "_site")
BASE = "https://alizidi192002-prog.github.io/Clarity-pack"
GREEN, INK, MUTED, GOLD, PAPER, GROUND, RULE = (47, 111, 82), (28, 38, 32), (90, 102, 95), (184, 128, 50), (255, 255, 255), (238, 240, 235), (220, 224, 218)
LANG = {
    "fr": {"kick": [("mariage", "MARIAGE"), ("noel", "NOËL"), ("auto-entrepreneur", "AUTO-ENTREPRENEUR"), ("epargne", "ÉPARGNE"),
                    ("simulateur", "SIMULATEUR GRATUIT"), ("fiche", "FICHE GRATUITE"), ("budgets/", "BUDGET MENSUEL"), ("", "BUDGET")],
           "foot": "Gratuit · en français", "site": "ClarityPaperCo",
           "tags": "#budget #budgetfamilial #economiser #gestionbudget #finances"},
    "es": {"kick": [("boda", "BODA"), ("navidad", "NAVIDAD"), ("autonomo", "AUTÓNOMOS"), ("ahorro", "AHORRO"),
                    ("simulador", "SIMULADOR GRATIS"), ("presupuestos/", "PRESUPUESTO MENSUAL"), ("", "PRESUPUESTO")],
           "foot": "Gratis · en español", "site": "ClarityPaperCo",
           "tags": "#presupuesto #ahorro #finanzaspersonales #ahorrardinero #economia"},
}
FONTS = {
    "serif": ["/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"],
    "sans": ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"],
    "body": ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"],
    "mono": ["/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf"],
}


def _pil():
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "-q", "Pillow"], check=False)
        from PIL import Image, ImageDraw, ImageFont
    return Image, ImageDraw, ImageFont


def _font(ImageFont, kind, size):
    for p in FONTS[kind]:
        if os.path.isfile(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default(size)


def _wrap(d, text, font, width):
    nb = chr(160)
    text = re.sub(r"(\d)[   ](?=\d{3}\b)", "\\1" + nb, text)
    text = re.sub(r"[  ](?=[€:?!;%])", nb, text)
    lines, cur = [], ""
    for w in text.split(" "):
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def _clean(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s))).strip()


def make_pin(PIL, path, kicker, title, sub, bullets, foot):
    Image, ImageDraw, ImageFont = PIL
    W, H, M = 1000, 1500, 115
    im = Image.new("RGB", (W, H), GROUND)
    d = ImageDraw.Draw(im)
    d.rectangle([50, 50, W - 50, H - 50], fill=PAPER, outline=RULE, width=2)
    d.rounded_rectangle([M, 115, M + 48, 163], 8, fill=GREEN)
    d.text((M + 24, 139), "CP", font=_font(ImageFont, "mono", 20), fill=PAPER, anchor="mm")
    d.text((M + 62, 139), "ClarityPaperCo", font=_font(ImageFont, "serif", 26), fill=INK, anchor="lm")
    d.text((M, 255), kicker, font=_font(ImageFont, "mono", 22), fill=GREEN, anchor="lm")
    y, tw = 300, W - 2 * M
    for size in (84, 74, 64, 56, 50):
        f = _font(ImageFont, "serif", size)
        tl = _wrap(d, title, f, tw)
        if len(tl) <= 4:
            break
    tl = tl[:5]
    for ln in tl:
        d.text((M, y), ln, font=f, fill=INK)
        y += int(size * 1.12)
    y += 30
    fb = _font(ImageFont, "body", 30)
    for ln in _wrap(d, sub, fb, tw)[:4]:
        d.text((M, y), ln, font=fb, fill=MUTED)
        y += 42
    y += 40
    fs = _font(ImageFont, "sans", 32)
    for b in bullets[:4]:
        bl = _wrap(d, b, fs, tw - 35)[:2]
        if y + 46 * len(bl) > H - 260:
            break
        d.rectangle([M, y + 14, M + 14, y + 28], fill=GOLD)
        for ln in bl:
            d.text((M + 32, y), ln, font=fs, fill=INK)
            y += 46
        y += 18
    d.line([M, H - 200, W - M, H - 200], fill=RULE, width=2)
    d.text((M, H - 140), foot, font=_font(ImageFont, "sans", 30), fill=GOLD, anchor="lm")
    d.text((W - M, H - 140), "→", font=_font(ImageFont, "sans", 40), fill=GREEN, anchor="rm")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    im.save(path, "JPEG", quality=88, optimize=True)


def _write():
    try:
        PIL = _pil()
        sm = open(os.path.join(OUT, "sitemap.xml"), encoding="utf-8").read()
        now = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S +0000")
        for lg, cfg in LANG.items():
            items = []
            for u in re.findall(r"<loc>(.*?)</loc>", sm):
                rel = u[len(BASE) + 1:]
                if not rel.startswith(lg + "/") or rel.endswith("index.html") or rel.endswith("/"):
                    continue
                f = os.path.join(OUT, rel)
                if not os.path.isfile(f):
                    continue
                s = open(f, encoding="utf-8").read()
                t = re.search(r"<title>(.*?)</title>", s, re.S)
                dm = re.search(r'<meta name="description" content="(.*?)"', s, re.S)
                h1 = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
                title = _clean(h1.group(1)) if h1 else (_clean(t.group(1)).split(" | ")[0] if t else rel)
                desc = _clean(dm.group(1)) if dm else title
                sub = re.split(r"(?<=[.!?])\s", desc)[0]
                bullets = [_clean(x) for x in re.findall(r"<h2[^>]*>(.*?)</h2>", s, re.S)]
                kicker = next(k for key, k in cfg["kick"] if key in rel)
                slug = rel.replace("/", "-").replace(".html", "")
                img_rel = f"pins/img/{slug}.jpg"
                make_pin(PIL, os.path.join(OUT, img_rel), kicker, title, sub, bullets, cfg["foot"])
                img = f"{BASE}/{img_rel}"
                pin_title = (_clean(t.group(1)).split(" | ")[0] if t else title)[:100]
                items.append(f"<item><title>{html.escape(pin_title)}</title><link>{u}</link>"
                             f"<description>{html.escape((desc + ' ' + cfg['tags'])[:480])}</description>"
                             f'<guid isPermaLink="true">{u}</guid><pubDate>{now}</pubDate>'
                             f'<enclosure url="{img}" type="image/jpeg" length="0"/><media:content url="{img}" medium="image" type="image/jpeg"/></item>')
            feed = ('<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/"><channel>'
                    f"<title>ClarityPaperCo ({lg})</title><link>{BASE}/{lg}/</link><description>{cfg['foot']}</description>"
                    + "".join(items) + "</channel></rss>\n")
            open(os.path.join(OUT, f"pins-{lg}.xml"), "w", encoding="utf-8").write(feed)
            print(f"pins-{lg}.xml:", len(items), "items")
    except Exception as e:
        print("pins-fr/es skipped:", repr(e))


def build(B):
    atexit.register(_write)
    return ""
