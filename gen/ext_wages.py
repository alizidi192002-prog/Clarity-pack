"""Hourly wage -> salary pages ($10-$60/hr) and a converter calculator.

Loaded automatically by gen/build.py (any gen/ext_*.py with build(B) is run).
build(B) writes its pages with B.write and returns an HTML snippet for the home page.
"""
import datetime

START = datetime.date(2026, 10, 1)
FIRST, PER_DAY = 6, 2
ORDER = [20, 15, 25, 18, 30, 22, 17, 16, 35, 40, 19, 21, 23, 24, 26, 28, 45, 50, 12, 13, 14, 27, 29, 31, 32, 33, 34,
         36, 37, 38, 39, 42, 44, 48, 55, 60, 10, 11, 41, 43, 46, 47, 49, 51, 52, 53, 54, 56, 57, 58, 59]


def usd(v, cents=False):
    return "${:,.2f}".format(v) if cents else "${:,.0f}".format(v)


def wage_page(B, w, live=()):
    year, month, biweek, week, day = w * 2080, w * 2080 / 12, w * 80, w * 40, w * 8
    rows = [("Per year (40 h/week, 52 weeks)", usd(year)), ("Per month", usd(month)), ("Every two weeks", usd(biweek)),
            ("Per week", usd(week)), ("Per day (8 hours)", usd(day))]
    pt = [(h, usd(w * h * 52), usd(w * h * 52 / 12)) for h in (40, 35, 30, 25, 20)]
    vac = [("52 weeks (paid time off)", usd(year)), ("50 weeks (2 weeks unpaid)", usd(w * 2000)), ("48 weeks (4 weeks unpaid)", usd(w * 1920))]
    m = month
    mr = round(m)
    nd, wt = round(m * .5), round(m * .3)
    split = [("Needs (50%)", usd(nd)), ("Wants (30%)", usd(wt)), ("Savings & debt (20%)", usd(mr - nd - wt))]
    title = f"${w} an Hour Is How Much a Year? (Salary, Monthly & Weekly Pay)"
    desc = f"${w} an hour is {usd(year)} a year for a full-time job (40 hours a week). See the monthly, biweekly, weekly and daily pay, part-time amounts and a sample budget."
    lower = [x for x in live if x < w]
    higher = [x for x in live if x > w]
    prev_next = []
    if lower:
        prev_next.append(f'<a href="{lower[-1]}-dollars-an-hour.html">${lower[-1]} an hour</a>')
    if higher:
        prev_next.append(f'<a href="{higher[0]}-dollars-an-hour.html">${higher[0]} an hour</a>')
    body = f"""<h1>${w} an hour is how much a year?</h1><p class="meta">Updated {B.TODAY.isoformat()} · 3 min read</p>
<p class="lede">If you make <strong>${w} an hour</strong> and work full time (40 hours a week, 52 weeks a year), you earn about <strong>{usd(year)} a year</strong> before taxes. That's about {usd(month)} a month or {usd(week)} a week.</p>
<h2>${w} an hour, by pay period</h2>
{B.table(["Pay period", "Gross pay"], rows)}
<p>These are gross amounts (before taxes and deductions). Your take-home pay will be lower and depends on where you live, your filing status and your benefits.</p>
<h2>If you work fewer hours</h2>
{B.table(["Hours per week", "Per year", "Per month"], pt)}
<h2>If some weeks are unpaid</h2>
{B.table(["Weeks paid", "Per year"], vac)}
<h2>What a budget could look like</h2>
<p>As an illustration, here is the 50/30/20 rule applied to {usd(month)} a month. Use your real take-home pay for your own budget, which will be smaller than this gross figure.</p>
{B.table(["Bucket", "Per month"], split, ("Total", usd(mr)))}
<div class="box"><strong>Quick math:</strong> hourly wage × 2,080 = yearly salary for a 40-hour week. Yearly salary ÷ 2,080 = hourly wage. Try other numbers in the <a href="../calculators/hourly-to-salary-calculator.html">hourly to salary calculator</a>.</div>
<p>{" · ".join(prev_next)} · <a href="index.html">all hourly wages</a> · <a href="../budgets/index.html">budgets by monthly income</a></p>
{B.cta("Paycheck to Paycheck Budget Planner", "Assign every bill to the paycheck that covers it and see what's left from each one. Weekly, biweekly or monthly pay.", B.G + "ljdxzm", "Get it — €4.99")}"""
    return f"wages/{w}-dollars-an-hour.html", title, desc, body


def calculator(B):
    body = f"""<h1>Hourly to Salary Calculator</h1><p class="lede">Convert an hourly wage into yearly, monthly, biweekly and weekly pay, or a yearly salary back into an hourly rate.</p>
<div class="calc">
<div class="row"><label>Hourly wage ($)</label><input id="h" type="number" step="0.01" value="22"></div>
<div class="row"><label>Hours per week</label><input id="hw" type="number" value="40"></div>
<div class="row"><label>Paid weeks per year</label><input id="wk" type="number" value="52"></div>
<div class="result" id="res"></div>
<h3>Or start from a yearly salary</h3>
<div class="row"><label>Yearly salary ($)</label><input id="sal" type="number" value="55000"></div>
<div class="result" id="res2"></div></div>
<p>All amounts are before taxes. See <a href="../wages/index.html">pay tables for $10 to $60 an hour</a>.</p>
{B.cta("Paycheck to Paycheck Budget Planner", "Plan every paycheck: bills, spending and what's left over.", B.G + "ljdxzm", "Get it — €4.99")}
<script>function f(v){{return '$'+v.toLocaleString('en-US',{{maximumFractionDigits:0}})}}function f2(v){{return '$'+v.toLocaleString('en-US',{{minimumFractionDigits:2,maximumFractionDigits:2}})}}
function c(){{const H=+h.value||0,W=+hw.value||0,K=+wk.value||0,y=H*W*K;
res.innerHTML=[['Per year',f(y)],['Per month',f(y/12)],['Every 2 weeks',f(y/26)],['Per week',f(H*W)]].map(a=>`<div class="stat"><div class="l">${{a[0]}}</div><div class="v">${{a[1]}}</div></div>`).join('');
const S=+sal.value||0,hrs=W*K||2080;res2.innerHTML=`<div class="stat"><div class="l">Hourly rate</div><div class="v">${{f2(S/hrs)}}</div><div class="l">at ${{W}} h/week, ${{K}} weeks</div></div><div class="stat"><div class="l">Per month</div><div class="v">${{f(S/12)}}</div></div>`}}
document.querySelectorAll('input').forEach(e=>e.addEventListener('input',c));c();</script>"""
    return "calculators/hourly-to-salary-calculator.html", "Hourly to Salary Calculator (Free)", "Free hourly to salary calculator: convert your hourly wage to yearly, monthly, biweekly and weekly pay, or a salary back to an hourly rate.", body


def build(B):
    p, t, d, b = calculator(B)
    B.write(p, B.page(t + " | ClarityPaperCo", d, b, 1, p, {"@context": "https://schema.org", "@type": "WebApplication", "name": t, "applicationCategory": "FinanceApplication", "offers": {"@type": "Offer", "price": "0"}}, "website"))
    n = FIRST + PER_DAY * max(0, (B.TODAY - START).days)
    live = sorted(ORDER[:n])
    for w in live:
        p, t, d, b = wage_page(B, w, live)
        sch = {"@context": "https://schema.org", "@type": "Article", "headline": t, "description": d, "datePublished": B.TODAY.isoformat(), "author": {"@type": "Organization", "name": "ClarityPaperCo"}}
        B.write(p, B.page(t + " | ClarityPaperCo", d, b, 1, p, sch))
    rows = "".join(f'<tr><td><a href="{w}-dollars-an-hour.html">${w} an hour</a></td><td class="n">{usd(w * 2080)}</td><td class="n">{usd(w * 2080 / 12)}</td></tr>' for w in live)
    hub = f"""<h1>Hourly wage to yearly salary</h1><p class="lede">How much is your hourly pay per year, month and week? Full-time figures (40 hours a week, 52 weeks), before taxes.</p>
<div class="tablewrap"><table><tr><th>Hourly wage</th><th class="n">Per year</th><th class="n">Per month</th></tr>{rows}</table></div>
<p>Don't see your number? Use the <a href="../calculators/hourly-to-salary-calculator.html">hourly to salary calculator</a>.</p>"""
    B.write("wages/index.html", B.page("Hourly Wage to Salary Table | ClarityPaperCo", "Hourly wage to yearly salary table: what $10 to $60 an hour comes to per year, month and week for a full-time job.", hub, 1, "wages/index.html", og="website"))
    return f"""<h2 id="wages">Hourly wage to salary</h2><div class="grid">{B.card("calculators/hourly-to-salary-calculator.html", "Calculator", "Hourly to Salary Calculator", "Convert hourly pay to yearly, monthly and weekly pay, and back.")}{B.card("wages/index.html", "Pay tables", f"{len(live)} hourly wages explained", "What $10 to $60 an hour means per year, month and week.")}</div>"""
