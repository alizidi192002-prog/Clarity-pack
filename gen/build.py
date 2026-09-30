#!/usr/bin/env python3
"""ClarityPaperCo site builder (runs in GitHub Actions, stdlib only).

Copies docs/ to _site/, then generates:
  - programmatic budget pages (released a few per day, see RELEASE_*)
  - calculators
  - index.html, budgets/index.html and sitemap.xml
Articles are plain HTML files in docs/articles/; index cards are built from their
<title>, <meta name="description"> and optional <meta name="section">.
"""
import datetime, html, json, os, re, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "docs")
OUT = os.path.join(ROOT, "_site")
BASE = "https://alizidi192002-prog.github.io/Clarity-pack"
G = "https://claritydigital8.gumroad.com/l/"
STORE = "https://claritydigital8.gumroad.com/"
GSV = '<meta name="google-site-verification" content="3QsNRygAzDRQhArNOHVWrSI-IxsKXUPM9EzUp-nBTPM" />'
TODAY = datetime.date.fromisoformat(os.environ["FAKE_TODAY"]) if os.environ.get("FAKE_TODAY") else datetime.datetime.utcnow().date()
RELEASE_START = datetime.date(2026, 10, 1)
RELEASE_FIRST = 6      # pages live on day one
RELEASE_PER_DAY = 2    # extra pages each day after


def money(v):
    return "${:,.0f}".format(v)


def page(title, desc, body, depth=0, path="", schema=None, og="article"):
    up = "../" * depth
    ld = '<script type="application/ld+json">%s</script>' % json.dumps(schema) if schema else ""
    gsv = GSV if path == "" else ""
    t, d = html.escape(title, quote=True), html.escape(desc, quote=True)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{t}</title><meta name="description" content="{d}">
<link rel="canonical" href="{BASE}/{path}">
<meta property="og:title" content="{t}"><meta property="og:description" content="{d}"><meta property="og:type" content="{og}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Inter:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{up}style.css">{ld}{gsv}</head><body>
<header class="site"><div class="wrap"><a class="logo" href="{up}index.html"><span class="m">CP</span>ClarityPaperCo</a>
<nav><a href="{up}index.html#guides">Guides</a><a href="{up}index.html#calculators">Calculators</a><a href="{up}budgets/index.html">By income</a><a href="{STORE}">Templates</a><a href="{up}fr/index.html" hreflang="fr">FR</a></nav></div></header>
<main><div class="wrap">{body}</div></main>
<footer><div class="wrap">© {TODAY.year} ClarityPaperCo — simple money spreadsheets for real life. Guides are for general information, not financial advice.</div></footer>
</body></html>"""


def cta(title, text, href, label, alt=True):
    a = f' <a class="btn alt" href="{G}zpdnkk">All 14 templates €19.99</a>' if alt else ""
    return f'<div class="cta"><div><strong>{title}</strong>{text}</div><a class="btn" href="{href}">{label}</a>{a}</div>'


NC = ' class="n"'


def table(head, rows, total=None):
    h = "".join(f'<th{NC if i else ""}>{c}</th>' for i, c in enumerate(head))
    b = "".join("<tr>" + "".join(f'<td{NC if i else ""}>{c}</td>' for i, c in enumerate(r)) + "</tr>" for r in rows)
    t = "<tr>" + "".join(f'<th{NC if i else ""}>{c}</th>' for i, c in enumerate(total)) + "</tr>" if total else ""
    return f'<div class="tablewrap"><table><tr>{h}</tr>{b}{t}</table></div>'


# ------------------------------------------------------------------ programmatic pages
def salary_page(m):
    needs, wants, save = m * .5, m * .3, m * .2
    yearly, biweekly, weekly = m * 12, m * 12 / 26, m * 12 / 52
    # example split of the needs half (guideline shares of income)
    ex = [("Rent or mortgage", .25), ("Groceries", .10), ("Utilities & phone", .06), ("Transport", .05)]
    R = lambda v: int(round(v))
    ex_rows = [(n, money(R(m * s))) for n, s in ex]
    ex_tot = sum(R(m * s) for _, s in ex)
    wx = [("Dining out & takeout", .10), ("Entertainment & hobbies", .08), ("Shopping", .07), ("Subscriptions", .05)]
    wx_rows = [(n, money(R(m * s))) for n, s in wx]
    wx_tot = sum(R(m * s) for _, s in wx)
    sx = [("Emergency fund", .10), ("Extra debt payments", .05), ("Retirement / investing", .05)]
    sx_rows = [(n, money(R(m * s))) for n, s in sx]
    sx_tot = sum(R(m * s) for _, s in sx)
    if m < 3000:
        tip = f"On {money(m)} a month, needs often take more than half, especially rent. That's normal. Try 60/20/20 or even 65/25/10 for a while, and grow the savings share as soon as a bill goes away or your income rises."
    elif m < 5000:
        tip = f"{money(m)} a month is a common take-home range, and the 50/30/20 split usually fits. The biggest lever is housing: if rent is well above {money(m * .3)}, cut back in wants before you touch savings."
    else:
        tip = f"With {money(m)} a month you can usually push savings past 20%. Many people at this level use 50/20/30 instead, keeping lifestyle spending flat as income grows and sending the difference to savings and investing."
    title = f"50/30/20 Budget on {money(m)} a Month (With Example Breakdown)"
    desc = f"How to split {money(m)} a month with the 50/30/20 rule: {money(needs)} for needs, {money(wants)} for wants, {money(save)} for savings, plus a sample category breakdown."
    body = f"""<h1>{title}</h1><p class="meta">Updated {TODAY.isoformat()} · 4 min read</p>
<p class="lede">If you take home {money(m)} a month, the 50/30/20 rule gives you a simple starting budget: half for needs, 30% for wants and 20% for savings or extra debt payments.</p>
<h2>The split</h2>
{table(["Bucket", "Share", "Per month"], [("Needs", "50%", money(needs)), ("Wants", "30%", money(wants)), ("Savings & debt", "20%", money(save))], ("Total", "100%", money(m)))}
<p>That's {money(yearly)} a year. If you're paid every two weeks, each paycheck is about {money(biweekly)}; weekly, about {money(weekly)}.</p>
<h2>Example: needs ({money(needs)})</h2>
{table(["Category", "Per month"], ex_rows, ("Subtotal", money(ex_tot)))}
<p>That leaves about {money(needs - ex_tot)} of the needs budget for insurance, childcare or minimum debt payments.</p>
<h2>Example: wants ({money(wants)})</h2>
{table(["Category", "Per month"], wx_rows, ("Subtotal", money(wx_tot)))}
<h2>Example: savings & debt ({money(save)})</h2>
{table(["Goal", "Per month"], sx_rows, ("Subtotal", money(sx_tot)))}
<div class="box"><strong>Tip for this income:</strong> {tip}</div>
<p>These amounts are a starting guideline, not a rule. Try it with your real bills in the free <a href="../calculators/50-30-20-calculator.html">50/30/20 calculator</a>, or see <a href="../articles/how-to-budget-biweekly-paycheck.html">how to budget a biweekly paycheck</a>.</p>
{cta("50/30/20 Monthly Budget Planner", "A ready spreadsheet that splits your income into needs, wants and savings, totals every category and flags anything over target.", STORE, "See the templates")}"""
    return f"budgets/50-30-20-budget-on-{m}-a-month.html", title, desc, body


WED = [("Venue", .22), ("Catering & drinks", .28), ("Photography & video", .10), ("Flowers & decor", .08), ("Attire & accessories", .07),
       ("Music & entertainment", .06), ("Rings", .05), ("Hair & makeup", .03), ("Invitations & stationery", .02), ("Transportation", .02),
       ("Favors & gifts", .02), ("Emergency buffer", .05)]


def wedding_page(t):
    rows = [(n, f"{int(p * 100)}%", money(t * p)) for n, p in WED]
    guests = [(g, money(t / g)) for g in (50, 75, 100, 150)]
    title = f"How to Budget a {money(t)} Wedding (Category Breakdown)"
    desc = f"A {money(t)} wedding budget broken down by category: venue, catering, photography, attire and more, plus cost per guest for 50 to 150 guests."
    body = f"""<h1>{title}</h1><p class="meta">Updated {TODAY.isoformat()} · 4 min read</p>
<p class="lede">Here's one way to split a {money(t)} wedding budget, based on a common percentage guideline. Move money between categories to match what matters most to you.</p>
<h2>Breakdown by category</h2>
{table(["Category", "Share", "Amount"], rows, ("Total", "100%", money(t)))}
<h2>Cost per guest</h2>
<p>Guest count changes almost everything, from catering to venue size.</p>
{table(["Guests", "Total budget per guest"], guests)}
<div class="box"><strong>Keep the buffer.</strong> The {money(t * .05)} emergency line is there because at least one vendor usually ends up above the first quote.</div>
<p>For how to adjust the split, read <a href="../articles/wedding-budget-breakdown-by-percentage.html">wedding budget breakdown by percentage</a>.</p>
{cta("Wedding Budget Planner", "Spreadsheet with this split already set up: planned vs quoted vs paid, a vendor payment schedule and a guest list with RSVPs.", G + "odsqq", "Get it — €6.99")}"""
    return f"budgets/wedding-budget-{t}.html", title, desc, body


XMAS = [("Gifts", .60), ("Food & hosting", .20), ("Decor, cards & wrapping", .10), ("Travel & events", .10)]


def xmas_page(t):
    rows = [(n, f"{int(p * 100)}%", money(t * p)) for n, p in XMAS]
    weeks = [(w, money(t / w)) for w in (6, 8, 10, 12)]
    title = f"How to Plan a {money(t)} Christmas Budget"
    desc = f"Split a {money(t)} Christmas budget between gifts, food, decor and travel, and see how much to save each week to pay for it in cash."
    body = f"""<h1>{title}</h1><p class="meta">Updated {TODAY.isoformat()} · 3 min read</p>
<p class="lede">A {money(t)} holiday budget goes further when you split it before you shop. Here's a simple starting split and a savings plan to pay for it without borrowing.</p>
<h2>Split the {money(t)}</h2>
{table(["Area", "Share", "Amount"], rows, ("Total", "100%", money(t)))}
<h2>How much to save each week</h2>
{table(["Weeks until you shop", "Save per week"], weeks)}
<p>With a gift budget of {money(t * .6)}, give each person a number before you buy anything. See <a href="../articles/how-much-to-spend-on-christmas-gifts.html">how much to spend on Christmas gifts</a> for a per-person example.</p>
{cta("Christmas & Holiday Budget Planner", "Gift list with bought and wrapped checkboxes, holiday expenses, and a summary that shows what's left.", G + "skpgb", "Get it — €4.99")}"""
    return f"budgets/christmas-budget-{t}.html", title, desc, body


def programmatic():
    s = [salary_page(m) for m in range(2000, 8001, 250)]
    w = [wedding_page(t) for t in range(5000, 50001, 5000)]
    x = [xmas_page(t) for t in (300, 400, 500, 600, 750, 1000, 1500, 2000)]
    order = []
    while s or w or x:  # interleave so every day mixes topics
        for lst in (s, s, w, x):
            if lst:
                order.append(lst.pop(0))
    days = max(0, (TODAY - RELEASE_START).days)
    n = RELEASE_FIRST + RELEASE_PER_DAY * days
    return order[:n], len(order)


# ------------------------------------------------------------------ calculators
FMT_JS = "function f(v){return (v<0?'-':'')+'$'+Math.abs(v).toLocaleString('en-US',{maximumFractionDigits:0})}"


def calc_503020():
    body = f"""<h1>50/30/20 Budget Calculator</h1><p class="lede">Enter your monthly take-home pay to see how much goes to needs, wants and savings, then compare with what you spend now.</p>
<div class="calc">
<div class="row"><label>Monthly take-home pay</label><input id="inc" type="number" value="4000"></div>
<h3>What you spend now (optional)</h3>
<div class="row"><label>Needs (rent, bills, groceries, transport)</label><input id="n" type="number" value="2300"></div>
<div class="row"><label>Wants (eating out, fun, shopping)</label><input id="w" type="number" value="1100"></div>
<div class="row"><label>Savings & extra debt payments</label><input id="s" type="number" value="600"></div>
<div class="result" id="res"></div></div>
<p>See <a href="../budgets/index.html">worked 50/30/20 examples by monthly income</a>.</p>
{cta("50/30/20 Monthly Budget Planner", "Track every expense by bucket with automatic totals and over-budget flags.", STORE, "See the templates")}
<script>{FMT_JS}
function c(){{const i=+inc.value||0,t=[i*.5,i*.3,i*.2],a=[+n.value||0,+w.value||0,+s.value||0],l=['Needs (50%)','Wants (30%)','Savings (20%)'];
let h='';for(let k=0;k<3;k++){{const d=k<2?t[k]-a[k]:a[k]-t[k];h+=`<div class="stat"><div class="l">${{l[k]}}</div><div class="v">${{f(t[k])}}</div><div class="l ${{d<0?'neg':''}}">You: ${{f(a[k])}} (${{d<0?(k<2?'over':'short'):'ok'}} ${{f(Math.abs(d))}})</div></div>`}}
res.innerHTML=h}}document.querySelectorAll('input').forEach(e=>e.addEventListener('input',c));c();</script>"""
    return "calculators/50-30-20-calculator.html", "50/30/20 Budget Calculator (Free)", "Free 50/30/20 budget calculator: see how much of your take-home pay should go to needs, wants and savings, and compare with your real spending.", body


def calc_debt():
    debts = [("Credit card", 3400, 22.9, 100), ("Car loan", 8200, 6.5, 250), ("Medical bill", 900, 0, 50), ("", 0, 0, 0)]
    rows = "".join(f'<div class="row bill"><input class="dn" value="{a}" placeholder="Debt" style="text-align:left"><div style="display:flex;gap:6px"><input class="db" type="number" value="{b or ""}" placeholder="Balance"><input class="dr" type="number" step="0.1" value="{r or ""}" placeholder="APR %"><input class="dm" type="number" value="{m or ""}" placeholder="Min"></div></div>' for a, b, r, m in debts)
    body = f"""<h1>Debt Snowball vs Avalanche Calculator</h1><p class="lede">Enter your debts (balance, interest rate, minimum payment) and how much extra you can pay each month. See how long each method takes and how much interest you pay.</p>
<div class="calc"><style>.row.bill{{grid-template-columns:1fr 300px}}@media(max-width:560px){{.row.bill{{grid-template-columns:1fr}}}}</style>
<h3>Debts: balance · APR % · minimum</h3>{rows}
<div class="row"><label>Extra payment per month</label><input id="x" type="number" value="200"></div>
<div class="result" id="res"></div></div>
<div class="box"><strong>Snowball</strong> pays the smallest balance first (quick wins). <strong>Avalanche</strong> pays the highest interest first (usually less interest overall).</div>
{cta("Debt Snowball & Avalanche Tracker", "Spreadsheet that ranks your debts both ways and tracks every payment until you're debt-free.", STORE, "See the templates")}
<script>{FMT_JS}
function sim(ds,extra,key){{ds=ds.map(d=>({{...d}}));let m=0,int=0;while(ds.some(d=>d.b>0.005)&&m<600){{m++;let pool=extra;ds.forEach(d=>{{if(d.b>0){{const i=d.b*d.r/1200;int+=i;d.b+=i}}}});
ds.forEach(d=>{{if(d.b>0){{const p=Math.min(d.m,d.b);d.b-=p;pool+=d.m-p}}else pool+=d.m}});ds.filter(d=>d.b>0).sort(key).forEach(d=>{{const p=Math.min(pool,d.b);d.b-=p;pool-=p}})}}return [m,int]}}
function c(){{const ds=[...document.querySelectorAll('.row.bill')].map(r=>({{b:+r.querySelector('.db').value||0,r:+r.querySelector('.dr').value||0,m:+r.querySelector('.dm').value||0}})).filter(d=>d.b>0);
const e=+x.value||0;if(!ds.length){{res.innerHTML='';return}}const S=sim(ds,e,(a,b)=>a.b-b.b),A=sim(ds,e,(a,b)=>b.r-a.r);
const st=(l,v)=>`<div class="stat"><div class="l">${{l}}</div><div class="v">${{v[0]>=600?'50+ yrs':v[0]+' mo'}}</div><div class="l">Interest: ${{f(v[1])}}</div></div>`;
res.innerHTML=st('Snowball',S)+st('Avalanche',A)+`<div class="stat"><div class="l">Avalanche saves</div><div class="v">${{f(S[1]-A[1])}}</div><div class="l">in interest</div></div>`}}
document.querySelectorAll('input').forEach(e=>e.addEventListener('input',c));c();</script>"""
    return "calculators/debt-snowball-avalanche-calculator.html", "Debt Snowball vs Avalanche Calculator (Free)", "Free debt payoff calculator: compare the snowball and avalanche methods, see your debt-free date and total interest.", body


# ------------------------------------------------------------------ articles from docs/
SECTIONS = {"how-to-budget-biweekly-paycheck.html": "Budgeting", "how-much-to-spend-on-christmas-gifts.html": "Holidays",
            "wedding-budget-breakdown-by-percentage.html": "Weddings", "how-to-make-a-budget-for-2027.html": "Yearly planning"}


def read_articles():
    arts = []
    d = os.path.join(SRC, "articles")
    for fn in sorted(os.listdir(d)) if os.path.isdir(d) else []:
        if not fn.endswith(".html"):
            continue
        s = open(os.path.join(d, fn), encoding="utf-8").read()
        t = re.search(r"<title>(.*?)</title>", s, re.S)
        ds = re.search(r'<meta name="description" content="(.*?)"', s, re.S)
        sec = re.search(r'<meta name="section" content="(.*?)"', s)
        dp = re.search(r'"datePublished":\s*"([\d-]+)"', s)
        title = html.unescape(t.group(1)).replace(" | ClarityPaperCo", "").strip() if t else fn
        arts.append({"path": "articles/" + fn, "title": title, "desc": html.unescape(ds.group(1)) if ds else "",
                     "sec": sec.group(1) if sec else SECTIONS.get(fn, "Guide"), "date": dp.group(1) if dp else "2026-09-30"})
    arts.sort(key=lambda a: (a["date"], a["path"]))
    return arts


def card(href, k, t, p):
    return f'<a class="card" href="{href}"><div class="k">{html.escape(k)}</div><h3>{html.escape(t)}</h3><p>{html.escape(p)}</p></a>'


def main():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    shutil.copytree(SRC, OUT)
    urls = [("", TODAY.isoformat())]

    def write(path, content):
        full = os.path.join(OUT, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        open(full, "w", encoding="utf-8").write(content)
        urls.append((path, TODAY.isoformat()))

    # calculators (keep hand-made paycheck calculator from docs/)
    calcs = [("calculators/paycheck-budget-calculator.html", "Paycheck Budget Calculator", "See what's left from each paycheck after its bills.")]
    urls.append(("calculators/paycheck-budget-calculator.html", TODAY.isoformat()))
    for fn in (calc_503020, calc_debt):
        p, t, d, b = fn()
        write(p, page(t + " | ClarityPaperCo", d, b, 1, p, {"@context": "https://schema.org", "@type": "WebApplication", "name": t, "applicationCategory": "FinanceApplication", "offers": {"@type": "Offer", "price": "0"}}, "website"))
        calcs.append((p, t.replace(" (Free)", ""), d.split(":")[1].strip().capitalize() if ":" in d else d))

    # programmatic pages
    live, total = programmatic()
    groups = {"Budget by monthly income": [], "Wedding budgets": [], "Christmas budgets": []}
    for p, t, d, b in live:
        sch = {"@context": "https://schema.org", "@type": "Article", "headline": t, "description": d, "datePublished": TODAY.isoformat(), "author": {"@type": "Organization", "name": "ClarityPaperCo"}}
        write(p, page(t + " | ClarityPaperCo", d, b, 1, p, sch))
        key = "Wedding budgets" if "wedding" in p else "Christmas budgets" if "christmas" in p else "Budget by monthly income"
        groups[key].append((p, t))
    hub = '<h1>Budgets by income and occasion</h1><p class="lede">Worked examples with real numbers: how to split a monthly income with the 50/30/20 rule, and how to plan a wedding or Christmas on a set budget.</p>'
    for g, items in groups.items():
        if items:
            hub += f'<h2>{g}</h2><ul>' + "".join(f'<li><a href="../{p}">{html.escape(t)}</a></li>' for p, t in items) + "</ul>"
    write("budgets/index.html", page("Budgets by Income and Occasion | ClarityPaperCo", "Worked budget examples: 50/30/20 budgets from $2,000 to $8,000 a month, wedding budgets and Christmas budgets with real numbers.", hub, 1, "budgets/index.html", og="website"))

    # articles
    arts = read_articles()
    for a in arts:
        urls.append((a["path"], a["date"]))
    guides = "".join(card(a["path"], a["sec"], a["title"], a["desc"]) for a in arts)
    calc_cards = "".join(card(p, "Calculator", t, d) for p, t, d in calcs)
    body = f"""<h1>Simple money guides and free budget calculators</h1>
<p class="lede">Plain-English guides for budgeting a paycheck, planning the holidays and paying for big life events — with free calculators and ready-made spreadsheets.</p>
<h2 id="calculators">Free calculators</h2><div class="grid">{calc_cards}</div>
<h2 id="guides">Guides</h2><div class="grid">{guides}</div>
<h2 id="budgets">Budgets by income</h2><p><a href="budgets/index.html">See {sum(len(v) for v in groups.values())} worked examples</a> — 50/30/20 budgets by monthly income, wedding budgets and Christmas budgets.</p>
{cta("Every spreadsheet in one download", "14 templates: 2027 budget, paycheck budget, debt payoff, savings, net worth, bills, Christmas, wedding, freelancer invoices and more. Excel & Google Sheets.", G + "zpdnkk", "Get it — €19.99", alt=False)}"""
    open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(
        page("ClarityPaperCo — Budget Guides & Free Money Calculators", "Plain-English budgeting guides, free paycheck, 50/30/20 and debt payoff calculators, and simple spreadsheet templates for Excel and Google Sheets.", body, 0, "", og="website"))

    fr_note = ""
    try:
        import sys
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import build_fr
        fr_urls, fr_live, fr_total = build_fr.build(OUT, SRC, TODAY)
        urls.extend(fr_urls)
        fr_note = f", fr {fr_live}/{fr_total} pages"
    except Exception as e:  # never let the French section break the English site
        print("French section skipped:", repr(e))

    seen, sm = set(), []
    for u, d in urls:
        if u not in seen:
            seen.add(u)
            sm.append(f"<url><loc>{BASE}/{u}</loc><lastmod>{d}</lastmod></url>")
    open(os.path.join(OUT, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(sm) + "</urlset>\n")
    open(os.path.join(OUT, ".nojekyll"), "w").write("")
    print(f"built: {len(arts)} articles, {len(live)}/{total} budget pages, {len(calcs)} calculators, {len(sm)} urls{fr_note}")


if __name__ == "__main__":
    main()
