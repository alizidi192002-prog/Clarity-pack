"""Pinterest RSS feed (_site/pins.xml) for "Auto-publish Pins from RSS".

After the build finishes, every English page in the sitemap becomes one feed item with a
matching pin image from pack/pins (served from raw.githubusercontent.com). Pinterest creates
a pin for each new item (new guid), so new pages become new pins automatically.
"""
import atexit, datetime, html, os, re, zlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "_site")
BASE = "https://alizidi192002-prog.github.io/Clarity-pack"
IMG = "https://raw.githubusercontent.com/alizidi192002-prog/Clarity-pack/main/pack/pins/"
IMAGES = {
    "wedding": ["v3/pin_wedding_a.jpg", "v3/pin_wedding_b.jpg"],
    "christmas": ["v3/pin_christmas_a.jpg", "v3/pin_christmas_b.jpg"],
    "budget": ["v2/budget_a.jpg", "v2/budget_b.jpg", "v2/budget_c.jpg"],
    "paycheck": ["v3/pin_paycheck_a.jpg", "v3/pin_paycheck_b.jpg"],
    "debt": ["v2/debt_a.jpg", "v2/debt_b.jpg", "v2/debt_c.jpg"],
    "savings": ["v2/savings_a.jpg", "v2/savings_b.jpg", "v2/savings_c.jpg"],
    "freelancer": ["v3/pin_freelancer_a.jpg", "v3/pin_freelancer_b.jpg"],
    "year": ["v3/pin_budget2027_a.jpg", "v3/pin_budget2027_b.jpg"],
    "subscription": ["v2/subscription_a.jpg", "v2/subscription_b.jpg"],
    "networth": ["v2/networth_a.jpg", "v2/networth_b.jpg"],
    "meal": ["v2/meal_a.jpg", "v2/meal_b.jpg"],
    "bookkeeping": ["v2/bookkeeping_a.jpg", "v2/bookkeeping_b.jpg"],
    "bundle": ["v3/pin_bundle_a.jpg", "v3/pin_bundle_b.jpg"],
}
RULES = [("wedding", "wedding"), ("christmas", "christmas"), ("holiday", "christmas"), ("black-friday", "christmas"), ("santa", "christmas"),
         ("wages/", "paycheck"), ("hourly", "paycheck"), ("paycheck", "paycheck"), ("debt", "debt"), ("emergency", "savings"),
         ("sinking", "savings"), ("saving", "savings"), ("freelanc", "freelancer"), ("invoice", "freelancer"), ("irregular", "freelancer"),
         ("2027", "year"), ("new-year", "year"), ("year-end", "year"), ("subscription", "subscription"), ("net-worth", "networth"),
         ("meal", "meal"), ("grocer", "meal"), ("bookkeeping", "bookkeeping"), ("roas", "bookkeeping"), ("free-printable", "year"),
         ("50-30-20", "budget"), ("budget", "budget")]
TAGS = {"wedding": "#weddingbudget #weddingplanning #budgeting", "christmas": "#christmasbudget #holidaybudget #budgeting",
        "paycheck": "#paycheckbudget #salary #budgeting", "debt": "#debtpayoff #debtfree #budgeting", "savings": "#savingmoney #emergencyfund #budgeting",
        "freelancer": "#freelancer #smallbusiness #invoicing", "year": "#budgetplanner #2027goals #budgeting", "bookkeeping": "#smallbusiness #bookkeeping",
        "budget": "#budgeting #503020rule #moneytips", "bundle": "#budgetplanner #budgeting #moneytips"}


def topic(path):
    for k, t in RULES:
        if k in path:
            return t
    return "bundle"


FEEDS = {  # file -> topics; everything not listed goes to pins.xml
    "pins-debt.xml": {"debt"},
    "pins-wedding.xml": {"wedding"},
    "pins-christmas.xml": {"christmas"},
    "pins-paycheck.xml": {"paycheck"},
}
NAMES = {"pins.xml": "budget guides and calculators", "pins-debt.xml": "debt payoff", "pins-wedding.xml": "wedding budget",
         "pins-christmas.xml": "Christmas and holiday budget", "pins-paycheck.xml": "paycheck and hourly wages"}


def feed_for(tp):
    for f, tps in FEEDS.items():
        if tp in tps:
            return f
    return "pins.xml"


def _write_feed():
    try:
        sm = open(os.path.join(OUT, "sitemap.xml"), encoding="utf-8").read()
        locs = [u for u in re.findall(r"<loc>(.*?)</loc>", sm) if "/fr/" not in u and "/es/" not in u and not u.endswith("index.html") and u.rstrip("/") != BASE]
        now = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S +0000")
        items = {f: [] for f in NAMES}
        for u in locs:
            rel = u[len(BASE) + 1:]
            f = os.path.join(OUT, rel)
            if not os.path.isfile(f):
                continue
            s = open(f, encoding="utf-8").read()
            t = re.search(r"<title>(.*?)</title>", s, re.S)
            d = re.search(r'<meta name="description" content="(.*?)"', s, re.S)
            title = html.unescape(t.group(1)).replace(" | ClarityPaperCo", "").strip() if t else rel
            desc = html.unescape(d.group(1)) if d else title
            tp = topic(rel)
            imgs = IMAGES[tp]
            img = IMG + imgs[zlib.crc32(rel.encode()) % len(imgs)]
            desc = f"{desc} {TAGS.get(tp, TAGS['bundle'])}"
            items[feed_for(tp)].append(f"<item><title>{html.escape(title[:100])}</title><link>{u}</link><description>{html.escape(desc[:480])}</description>"
                         f'<guid isPermaLink="true">{u}</guid><pubDate>{now}</pubDate>'
                         f'<enclosure url="{img}" type="image/jpeg" length="0"/><media:content url="{img}" medium="image" type="image/jpeg"/></item>')
        for f, its in items.items():
            feed = ('<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/"><channel>'
                    f"<title>ClarityPaperCo — {NAMES[f]}</title><link>{BASE}/</link>"
                    "<description>Budget guides, free calculators and worked budget examples.</description>"
                    + "".join(its) + "</channel></rss>\n")
            open(os.path.join(OUT, f), "w", encoding="utf-8").write(feed)
            print(f, len(its), "items")
    except Exception as e:
        print("pins.xml skipped:", repr(e))


def build(B):
    atexit.register(_write_feed)
    return ""
