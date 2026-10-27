"""v4 pins: two NEW looks (d = bold question on colour, e = before/after) for every product, to stop
re-posting the same images. Output: pack/pins/v4/<key>_d.jpg and <key>_e.jpg"""
import os, sys
from playwright.sync_api import sync_playwright
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "gen"))
from products_data import PRODUCTS

OUT = os.path.join(os.path.dirname(__file__), "..", "pack", "pins", "v4")
os.makedirs(OUT, exist_ok=True)
SERIF = "'Liberation Serif','Tinos','DejaVu Serif',Georgia,serif"
SANS = "'Liberation Sans','Arimo','DejaVu Sans',Arial,sans-serif"
MONO = "'DejaVu Sans Mono',monospace"

V = {
 "christmas": ("Is your Christmas budget out of control?", ["Gifts bought on impulse", "Surprise January credit card bill", "No idea what is left"], ["Gift list with bought / wrapped boxes", "Food, decor & travel in one budget", "See what is left at a glance"], "#7a1f2b"),
 "budget2027": ("Ready to start 2027 with a real plan?", ["Money gone before month end", "Budget on a scrap of paper", "Goals with no numbers"], ["12 monthly budget tabs", "Budget vs actual, auto totals", "Savings rate on a yearly view"], "#1f3a5f"),
 "bundle": ("14 budget spreadsheets. One download.", ["Buying one template at a time", "Tools that do not talk to each other", "Starting from scratch every time"], ["2027 budget, paycheck, debt, savings", "Wedding, Christmas, net worth, bills", "Excel and Google Sheets"], "#2f6f52"),
 "paycheck": ("Which paycheck pays which bill?", ["Rent due before payday", "Bills pile up at month end", "Guessing what is left"], ["Weekly, biweekly or monthly pay", "Every bill assigned to a paycheck", "Leftover shown per paycheck"], "#8a4b14"),
 "wedding": ("Wedding budget getting away from you?", ["Deposits you forgot about", "Vendors quoting new totals", "Arguments about money"], ["Every vendor, deposit and balance", "Estimated vs actual cost", "Guest and payment tracking"], "#5b3a6e"),
 "freelancer": ("Who still owes you money?", ["Unpaid invoices lost in email", "Tax bill surprise", "Irregular income, no plan"], ["Invoice log with overdue flags", "Tax set-aside calculated", "Monthly income at a glance"], "#17332a"),
 "debt": ("What is your debt-free date?", ["Minimum payments forever", "Not sure which debt to attack", "No end in sight"], ["Snowball vs avalanche side by side", "Debts ranked automatically", "Debt-free date calculated"], "#1f3a5f"),
 "budget": ("Where does all your money go?", ["Paycheck gone in a week", "No idea what you spend on food", "Budgets you quit after 2 weeks"], ["50/30/20 split done for you", "Auto totals and overspend flags", "12 monthly tabs plus a year view"], "#8a4b14"),
 "subscription": ("How much do your subscriptions really cost?", ["Forgotten free trials", "Annual charges you did not see", "Paying for apps you never open"], ["Weekly, monthly and annual bills", "True yearly cost shown", "Find what to cancel"], "#7a1f2b"),
 "habit": ("Can you track 10 habits in 10 seconds?", ["Streaks lost after a busy week", "Apps you stop opening", "No view of the month"], ["One row per habit, one tap a day", "Monthly view with streaks", "Works offline in Sheets or Excel"], "#2f6f52"),
 "meal": ("What is for dinner this week?", ["5 pm panic: what to cook?", "Food thrown away", "Three trips to the shop"], ["Weekly plan in one page", "Grocery list built for you", "Spend less on food"], "#8a4b14"),
 "savings": ("Saving for three things at once?", ["One savings pot for everything", "Dipping into the emergency fund", "No progress you can see"], ["Sinking funds for each goal", "Progress bars and targets", "Emergency fund, vacation, car"], "#1f3a5f"),
 "networth": ("What are you actually worth today?", ["Accounts in five places", "Only checking the balance", "No view of progress"], ["Assets and debts in one sheet", "Net worth month by month", "See your real progress"], "#5b3a6e"),
 "bookkeeping": ("Is your business really making a profit?", ["Receipts in a shoebox", "Tax time panic", "Income and expenses mixed up"], ["Income and expenses in one sheet", "Monthly profit calculated", "Ready for your accountant"], "#17332a"),
 "metaads": ("Which of your ads actually makes money?", ["Spend without knowing ROAS", "Metrics in five tabs", "Scaling the wrong ad"], ["ROAS, CPA and CTR calculated", "Campaign comparison", "Spot winners and losers fast"], "#7a1f2b"),
}
GOLD = "#e9b949"
BASE = f"*{{box-sizing:border-box;margin:0;padding:0}} body{{width:1000px;height:1500px;overflow:hidden;font-family:{SANS};position:relative}}"
def brand(c): return f"<div style='display:flex;align-items:center;gap:14px;font:700 28px {SERIF};color:{c}'><div style='width:48px;height:48px;border-radius:10px;background:{GOLD};color:#222;display:flex;align-items:center;justify-content:center;font:700 18px {MONO}'>CP</div>ClarityPaperCo</div>"
def price(k):
    p = PRODUCTS[k]
    return ("In the 14-template Bundle  →  €19.99" if p.get("bundle_only") else f"€{p['price']}  ·  Instant download")

def design_d(k):
    q, pain, gain, col = V[k]
    chips = "".join(f"<li>{g}</li>" for g in gain)
    return f"""<style>{BASE} body{{background:{col};color:#fff;padding:80px 70px}}
h1{{font:700 112px/1.02 {SERIF};margin-top:120px}}
ul{{list-style:none;margin-top:70px}} li{{font:600 38px {SANS};background:rgba(255,255,255,.12);border-radius:14px;padding:26px 30px;margin-bottom:20px}}
.cta{{position:absolute;left:70px;right:70px;bottom:80px;background:{GOLD};color:#1b1b1b;border-radius:14px;padding:30px;text-align:center;font:700 34px {SANS}}}
.s{{font:400 30px {SANS};color:rgba(255,255,255,.8);margin-top:30px}}</style>
{brand('#fff')}<h1>{q}</h1><div class='s'>{PRODUCTS[k]['name'].split(' — ')[0]} · Excel &amp; Google Sheets</div><ul>{chips}</ul><div class='cta'>{price(k)}</div>"""

def design_e(k):
    q, pain, gain, col = V[k]
    a = "".join(f"<li>{x}</li>" for x in pain); b = "".join(f"<li>{x}</li>" for x in gain)
    return f"""<style>{BASE} body{{background:#f6f1e7;color:#1f2a24;padding:80px 60px}}
h2{{font:700 70px/1.06 {SERIF};margin:60px 0 50px;color:{col}}}
.box{{border-radius:18px;padding:36px 40px;margin-bottom:34px}}
.bad{{background:#fff;border:3px solid #e2c9c9}} .good{{background:{col};color:#fff}}
.lb{{font:700 24px {MONO};letter-spacing:4px;margin-bottom:18px}} .bad .lb{{color:#b04b4b}} .good .lb{{color:{GOLD}}}
ul{{list-style:none}} li{{font:600 36px/1.25 {SANS};margin-bottom:14px}}
.bad li:before{{content:'✕  ';color:#b04b4b}} .good li:before{{content:'✓  ';color:{GOLD}}}
.foot{{position:absolute;left:60px;right:60px;bottom:70px;display:flex;justify-content:space-between;align-items:center;border-top:2px solid #ddd6c6;padding-top:26px;font:700 34px {SANS};color:{col}}}</style>
{brand('#1f2a24')}<h2>{PRODUCTS[k]['name'].split(' — ')[0]}</h2>
<div class='box bad'><div class='lb'>WITHOUT IT</div><ul>{a}</ul></div>
<div class='box good'><div class='lb'>WITH IT</div><ul>{b}</ul></div>
<div class='foot'><span>{price(k)}</span><span style='font:600 24px {SANS};color:#46524c'>Excel &amp; Google Sheets</span></div>"""

with sync_playwright() as pw:
    br = pw.chromium.launch(); pg = br.new_page(viewport={"width": 1000, "height": 1500})
    for k in V:
        for t, fn in (("d", design_d), ("e", design_e)):
            pg.set_content("<html><body>" + fn(k) + "</body></html>"); pg.wait_for_timeout(50)
            pg.screenshot(path=os.path.join(OUT, f"{k}_{t}.jpg"), type="jpeg", quality=88)
    br.close()
print("done", len(V) * 2)
