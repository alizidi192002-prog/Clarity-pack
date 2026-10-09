"""Product pin feeds for Pinterest "Auto-publish Pins from RSS" (replaces the Zapier posting).

- Writes one landing page per product at templates/<slug>.html (on the claimed site) with a
  button to the product's Gumroad page. Pinterest requires every feed item to link to the
  claimed website, so pins link here, not straight to Gumroad.
- Reads pack/pins/schedule.json and, for every day from FEED_START to today (Africa/Algiers),
  adds that day's 3 pins as feed items. Days in new_pins_by_day are used as-is; later days follow
  the repost rule (slot 1 always a priority product: Christmas / 2027 / Bundle; Christmas only
  from September to 24 December). Titles for re-posts rotate through products_data titles.
- One feed per board, because Pinterest saves each feed to a single board:
    pins-products.xml          -> Budget Planner Spreadsheets & Finance Templates
    pins-products-debt.xml     -> Debt Payoff Planner
    pins-products-savings.xml  -> Savings Tracker Templates
    pins-products-business.xml -> Small Business Bookkeeping
    pins-products-ramadan.xml  -> Ramadan Planner & Zakat (seasonal, see RAMADAN below)
Every item has a unique link/guid (?pin=YYYY-MM-DD-slot), so each day's pins are new items.
"""
import datetime, html, json, os

from products_data import PRODUCTS, IMAGE_TO_PRODUCT, IMG

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "_site")
BASE = "https://alizidi192002-prog.github.io/Clarity-pack"
SCHEDULE = os.path.join(ROOT, "pack", "pins", "schedule.json")
FEED_START = datetime.date(2026, 10, 9)
KEEP_DAYS = 60
FEEDS = {
    "1149614311072230535": ("pins-products.xml", "Budget planner spreadsheets and finance templates"),
    "1149614311072245490": ("pins-products-debt.xml", "Debt payoff planners"),
    "1149614311072245491": ("pins-products-savings.xml", "Savings tracker templates"),
    "1149614311072245492": ("pins-products-business.xml", "Small business bookkeeping templates"),
    "ramadan": ("pins-products-ramadan.xml", "Ramadan planner and zakat calculator"),
}
# Seasonal Ramadan pins, one pin every few days (Ramadan 2027 starts ~8 Feb, Eid al-Fitr ~10 Mar).
# The 6 original pins go first (A titles, then B titles), then re-posts with rotating titles.
# For next year: move the dates and keep the same structure.
RAMADAN = dict(
    phases=[(datetime.date(2026, 12, 1), datetime.date(2026, 12, 31), 3),   # seeding: every 3 days
            (datetime.date(2027, 1, 1), datetime.date(2027, 3, 10), 2)],    # search season: every 2 days
    order=["ramadan/pin_ramadan_a.jpg", "ramadan/pin_zakat_a.jpg", "ramadan/pin_ramadanbundle_a.jpg",
           "ramadan/pin_ramadan_b.jpg", "ramadan/pin_zakat_b.jpg", "ramadan/pin_ramadanbundle_b.jpg"],
)
MAIN_BOARD = "1149614311072230535"


def algiers_today():
    if os.environ.get("FAKE_TODAY"):
        return datetime.date.fromisoformat(os.environ["FAKE_TODAY"])
    return (datetime.datetime.utcnow() + datetime.timedelta(hours=1)).date()


def christmas_active(d):
    return d.month >= 9 and (d.month < 12 or d.day <= 24)


def product_of(image_url):
    return IMAGE_TO_PRODUCT.get(image_url.split("/")[-1])


def plan(S, start, end):
    """Return [(date, slot, image_url, board_id, product_key, title_or_None, desc_or_None)] in order."""
    by_day = {d["date"]: d["pins"] for d in S["new_pins_by_day"]}
    last = datetime.date.fromisoformat(S.get("last_scheduled_date") or max(by_day))
    pool = S["repost_pool"]
    prio = [p for p in pool if p.get("priority")]
    rest = [p for p in pool if not p.get("priority")]
    out = []
    d = start
    while d <= end:
        key = d.isoformat()
        if key in by_day:
            pins = [(p["image_url"], p["board_id"], p.get("title"), p.get("description")) for p in by_day[key]]
        elif d > last:
            n = (d - last).days - 1
            active = [p for p in prio if christmas_active(d) or product_of(p["image_url"]) != "christmas"]
            first = active[n % len(active)]
            pins = [(first["image_url"], first["board_id"], None, None)]
            for i in (2 * n, 2 * n + 1):
                p = rest[i % len(rest)]
                pins.append((p["image_url"], p["board_id"], None, None))
        else:
            pins = []
        for slot, (img, board, t, desc) in enumerate(pins, 1):
            out.append((d, slot, img, board, product_of(img), t, desc))
        d += datetime.timedelta(days=1)
    return out


def plan_ramadan(start, end):
    """Seasonal Ramadan pins: [(date, 'r', image_url, 'ramadan', product_key, None, None)]."""
    from products_data import IMG as _IMG
    days = []
    for a, b, step in RAMADAN["phases"]:
        d = a
        while d <= b:
            days.append(d)
            d += datetime.timedelta(days=step)
    out = []
    for i, d in enumerate(days):
        if start <= d <= end:
            img = _IMG + RAMADAN["order"][i % len(RAMADAN["order"])]
            out.append((d, "r", img, "ramadan", product_of(img), None, None))
    return out


def item(d, slot, img, prod, title, desc):
    url = f"{BASE}/templates/{prod['slug']}.html?pin={d.isoformat()}-{slot}"
    pub = datetime.datetime(d.year, d.month, d.day, 7, slot if isinstance(slot, int) else 30).strftime("%a, %d %b %Y %H:%M:%S +0000")
    if prod.get("bundle_only"):
        desc = f"{desc} Included in the Complete Budget Bundle (14 spreadsheets) — €19.99, instant download."
    else:
        desc = f"{desc} {prod['name']} — €{prod['price']}, instant download."
    return (f"<item><title>{html.escape(title[:100])}</title><link>{html.escape(url)}</link>"
            f"<description>{html.escape(desc[:480])}</description><guid isPermaLink=\"true\">{html.escape(url)}</guid>"
            f"<pubDate>{pub}</pubDate><enclosure url=\"{img}\" type=\"image/jpeg\" length=\"0\"/>"
            f"<media:content url=\"{img}\" medium=\"image\" type=\"image/jpeg\"/></item>")


def write_feeds(today):
    """Items up to tomorrow (Pinterest takes up to 24 h anyway). A feed that would still be
    empty also gets its next upcoming item, because Pinterest refuses to connect an empty feed."""
    S = json.load(open(SCHEDULE, encoding="utf-8"))
    used = {k: 0 for k in PRODUCTS}
    items = {b: [] for b in FEEDS}
    upcoming = {}
    oldest = today - datetime.timedelta(days=KEEP_DAYS)
    horizon = today + datetime.timedelta(days=1)
    rows = plan(S, FEED_START, today + datetime.timedelta(days=30))
    rows += plan_ramadan(FEED_START, today + datetime.timedelta(days=90))
    rows.sort(key=lambda r: (r[0], str(r[1])))
    for d, slot, img, board, pk, t, desc in rows:
        if pk is None:
            print("products feed: unknown image", img)
            continue
        prod = PRODUCTS[pk]
        if not t:
            t, desc = prod["titles"][used[pk] % len(prod["titles"])]
        used[pk] += 1
        b = board if board in FEEDS else MAIN_BOARD
        if d < oldest:
            continue
        if d <= horizon:
            items[b].insert(0, item(d, slot, img, prod, t, desc))
        elif b not in upcoming:
            upcoming[b] = item(d, slot, img, prod, t, desc)
    for b in FEEDS:
        if not items[b] and b in upcoming:
            items[b].append(upcoming[b])
    for board, (fname, name) in FEEDS.items():
        feed = ('<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/"><channel>'
                f"<title>ClarityPaperCo — {name}</title><link>{BASE}/templates/index.html</link>"
                "<description>Budget and planner spreadsheets for Excel and Google Sheets.</description>"
                + "".join(items[board]) + "</channel></rss>\n")
        open(os.path.join(OUT, fname), "w", encoding="utf-8").write(feed)
        print(fname, len(items[board]), "items")


def cta_for(B, k, p):
    if p.get("bundle_only"):
        return B.cta(f'{p["name"]} is included in the Complete Bundle', "Get this spreadsheet plus 13 more (2027 budget, Christmas, wedding, paycheck, debt, savings...) in one download. Secure checkout on Gumroad.", p["link"], "Get the Bundle — €19.99", alt=False)
    if "alt" in p:  # products with their own companion bundle (Ramadan) or none
        extra = f' <a class="btn alt" href="{p["alt"][1]}">{html.escape(p["alt"][0])}</a>' if p["alt"] else ""
        return (f'<div class="cta"><div><strong>{html.escape(p["name"])} — €{p["price"]}</strong>Secure checkout on Gumroad, instant download.</div>'
                f'<a class="btn" href="{p["link"]}">Get it — €{p["price"]}</a>{extra}</div>')
    return B.cta(f'{p["name"]} — €{p["price"]}', "Secure checkout on Gumroad, instant download.", p["link"], f'Get it — €{p["price"]}', alt=(k != "bundle"))


def product_page(B, k, p):
    img = IMG + p["images"][0]
    feats = "".join(f"<li>{html.escape(f)}</li>" for f in p["features"])
    body = (f'<h1>{html.escape(p["name"])}</h1><p class="lede">{html.escape(p["blurb"])}</p>'
            f'<p><img src="{img}" alt="{html.escape(p["name"])} spreadsheet preview" width="500" style="width:100%;max-width:500px;height:auto;border-radius:10px"></p>'
            f"<h2>What's inside</h2><ul>{feats}</ul>"
            f'<p>Works in Excel, Google Sheets and Numbers. Instant download after purchase on Gumroad.</p>'
            + cta_for(B, k, p))
    path = f"templates/{p['slug']}.html"
    schema = {"@context": "https://schema.org", "@type": "Product", "name": p["name"], "description": p["blurb"], "image": img,
              "offers": {"@type": "Offer", "price": "19.99" if p.get("bundle_only") else p["price"], "priceCurrency": "EUR", "url": p["link"], "availability": "https://schema.org/InStock"}}
    page = B.page(f'{p["name"]} (Excel & Google Sheets) | ClarityPaperCo', p["blurb"], body, 1, path, schema, "product")
    page = page.replace('<meta property="og:type" content="product">',
                        f'<meta property="og:type" content="product"><meta property="og:image" content="{img}">', 1)
    B.write(path, page)
    return path


def build(B):
    cards, hub_cards = [], []
    order = ["bundle", "christmas", "budget2027", "paycheck", "wedding", "ramadanbundle", "ramadan", "zakat", "freelancer",
             "debt", "budget", "savings", "networth", "subscription", "bookkeeping", "metaads", "habit", "meal"]
    for k in order:
        p = PRODUCTS[k]
        path = product_page(B, k, p)
        tag = "In the Bundle" if p.get("bundle_only") else f"€{p['price']}"
        cards.append(B.card(path, tag, p["name"], p["blurb"][:90]))
        hub_cards.append(B.card(path.split("/")[-1], tag, p["name"], p["blurb"][:90]))
    hub = '<h1>Budget & Planner Spreadsheet Templates</h1><p class="lede">Ready-made spreadsheets for Excel and Google Sheets. Instant download.</p><div class="grid">' + "".join(hub_cards) + "</div>"
    B.write("templates/index.html", B.page("Budget & Planner Spreadsheet Templates | ClarityPaperCo",
            "Budget planner, debt payoff, savings, Christmas, wedding, Ramadan planner and zakat calculator spreadsheet templates for Excel and Google Sheets.", hub, 1, "templates/index.html", None, "website"))
    try:
        write_feeds(algiers_today())
    except Exception as e:  # never break the site build
        print("products feed skipped:", repr(e))
    return f'<h2 id="templates">Spreadsheet templates</h2><div class="grid">{"".join(cards[:6])}</div><p><a href="templates/index.html">All templates →</a></p>'
