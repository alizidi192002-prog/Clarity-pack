"""Holiday season pages: a Christmas gift budget calculator, gift budget guides by recipient
and a Black Friday budget guide. All live at once (seasonal content needs time to be indexed).
"""

GIFT_PRODUCT = "skpgb"  # Christmas & Holiday Budget Planner (G + id)

RECIP = [
    ("kids", "Kids", "each child", (50, 150, 300),
     "Kids notice fairness more than price. Set one amount per child and keep it the same for siblings, or match it to age if they're far apart.",
     ["Use the four-gift idea (something they want, something they need, something to wear, something to read) to keep the list short.",
      "Count stocking stuffers inside the per-child amount, not on top of it. They add up fast.",
      "Grandparents and relatives often buy too. Agree on who gets the big gift so it isn't doubled."]),
    ("your-partner", "Your Partner", "your partner", (50, 150, 400),
     "Agree on a number together before December. It removes the guessing and nobody feels the gifts were uneven.",
     ["Shared experiences (a dinner, a concert, a weekend away) can replace a big object and count for both of you.",
      "If money is tight this year, set a low limit and make it a game: best gift under the limit wins.",
      "Joint money? Each of you gets a small personal gift budget so the surprise stays a surprise."]),
    ("parents", "Your Parents", "each parent (or per couple)", (30, 75, 150),
     "Many parents would rather you didn't overspend. A thoughtful gift at a modest price usually lands better than an expensive one.",
     ["Pool with your siblings for one bigger gift instead of several small ones.",
      "Photos, a family dinner you host, or help with a task they've put off are gifts that cost little.",
      "Decide whether the amount is per parent or per couple before you shop."]),
    ("friends", "Friends", "each friend", (15, 30, 60),
     "With friends, the list is what grows. Decide who's on it first, then set a small amount per person.",
     ["A friends' Secret Santa with one price limit replaces many gifts with one.",
      "Homemade food, a shared outing or a card with a real note are fine for most friendships.",
      "Close friends can have a higher amount than the wider group. Write both numbers down."]),
    ("coworkers", "Coworkers", "each coworker", (10, 20, 30),
     "At work, smaller is safer. Follow any office rule, and never feel you have to match a boss or a big spender.",
     ["Office Secret Santa usually has a fixed limit. Stick to it exactly.",
      "Cards or a shared treat for the team (cookies, coffee) cover everyone for one small amount.",
      "Gifts usually go down the chain, not up. You don't need to buy for your manager."]),
    ("teachers", "Teachers", "each teacher", (10, 25, 40),
     "Check the school's rules first. Some schools limit gift value, and a group gift from the class is common.",
     ["A class group gift (everyone adds a few dollars) gives the teacher one useful gift card.",
      "A handwritten note from your child is often the part teachers keep.",
      "Remember assistants, coaches and bus drivers if you want to include them. Add them to the list now."]),
]


def gift_page(B, slug, who, each, tiers, lede, tips):
    m = B.money
    rows = [("Tight budget", m(tiers[0])), ("Middle", m(tiers[1])), ("Generous", m(tiers[2]))]
    title = f"How Much to Spend on Christmas Gifts for {who}"
    desc = f"How much to spend on Christmas gifts for {who.lower()}: a simple way to set the amount for {each}, three budget levels, and tips to stay on budget."
    body = f"""<h1>{title}</h1><p class="meta">Updated {B.TODAY.isoformat()} · 3 min read</p>
<p class="lede">There's no right amount. What matters is choosing a number for {each} before you shop, so the total fits your budget. Here's a simple way to set it.</p>
<h2>Three budget levels for {each}</h2>
{B.table(["If your budget is", "Amount for " + each], rows)}
<p>These are example levels to help you choose, not rules. Pick the one that fits your total holiday budget, then use it for everyone in this group.</p>
<h2>Start from your total, not the gift</h2>
<p>Write your total holiday budget first. Take off food, decorations and travel, then split what's left between the people on your list. If the amounts come out too small, shorten the list or lower the level, rather than raising the total. The <a href="../calculators/christmas-gift-budget-calculator.html">Christmas gift budget calculator</a> does this for you.</p>
<div class="box"><strong>Tip:</strong> {lede}</div>
<h2>Ways to keep it within budget</h2>
<ul>{"".join(f"<li>{t}</li>" for t in tips)}</ul>
<p>See also: <a href="../articles/how-much-to-spend-on-christmas-gifts.html">how much to spend on Christmas gifts overall</a> and <a href="black-friday-budget.html">how to make a Black Friday budget</a>.</p>
{B.cta("Christmas & Holiday Budget Planner", "Gift list with an amount per person, bought and wrapped checkboxes, holiday expenses and what's left.", B.G + GIFT_PRODUCT, "Get it — €4.99")}"""
    return f"holidays/christmas-gifts-for-{slug}.html", title, desc, body


def black_friday(B):
    m = B.money
    plan = [("Winter coat (need)", 120, "Must have"), ("Headphones (planned since summer)", 80, "Must have"), ("Gifts: 3 people on the list", 150, "Must have"),
            ("Kitchen appliance", 90, "Only if 30%+ off"), ("Video game", 40, "Only if 30%+ off"), ("Buffer for a real surprise deal", 20, "Optional")]
    rows = [(a, m(b), c) for a, b, c in plan]
    tot = sum(b for _, b, _ in plan)
    title = "How to Make a Black Friday Budget (With a Shopping Plan)"
    desc = "Set a Black Friday budget before the sales start: a spending limit, a must-have list with target prices, and rules that stop impulse buys. Worked example included."
    body = f"""<h1>{title}</h1><p class="meta">Updated {B.TODAY.isoformat()} · 4 min read</p>
<p class="lede">Black Friday saves money only on things you were going to buy anyway. A budget made before the sales start is what turns discounts into savings instead of extra spending.</p>
<h2>1. Set one spending limit</h2>
<p>Pick a total you can pay in cash this month, without a balance on a credit card afterwards. Write it down. Everything below has to fit inside it.</p>
<h2>2. List what you'll buy and at what price</h2>
<p>For each item, write the normal price and the price at which you'll buy. If it doesn't reach that price, you don't buy it. Here's an example with a {m(tot)} limit:</p>
{B.table(["Item", "Max price", "Rule"], rows, ("Total", m(tot), ""))}
<h2>3. Rules that stop impulse buys</h2>
<ul><li>Nothing that isn't on the list, however good the discount looks.</li><li>Check the price history: many "deals" are the normal price.</li><li>Wait 24 hours before anything over a set amount, for example {m(50)}.</li><li>Unsubscribe from store emails you don't need until December.</li></ul>
<h2>4. Count gifts inside your Christmas budget</h2>
<p>Gifts bought on Black Friday are part of the Christmas budget, not extra. Take them off your gift list when you buy them. To set an amount per person, use the <a href="../calculators/christmas-gift-budget-calculator.html">Christmas gift budget calculator</a>.</p>
<div class="box"><strong>Check after:</strong> add up what you spent the next day. Anything over the limit comes out of next month's wants, not savings.</div>
{B.cta("Christmas & Holiday Budget Planner", "Track every gift and holiday expense against your limit, with what's left updated as you go.", B.G + GIFT_PRODUCT, "Get it — €4.99")}"""
    return "holidays/black-friday-budget.html", title, desc, body


def calculator(B):
    ppl = [("Partner", 1, 150), ("Kids", 2, 120), ("Parents & family", 4, 40), ("Friends", 3, 25), ("Coworkers & teachers", 3, 15), ("", 0, 0)]
    rows = "".join(f'<div class="row gp"><input class="gn" value="{a}" placeholder="Group" style="text-align:left"><div style="display:flex;gap:6px"><input class="gc" type="number" min="0" value="{c or ""}" placeholder="People"><input class="ga" type="number" min="0" value="{v or ""}" placeholder="$ each"></div></div>' for a, c, v in ppl)
    body = f"""<h1>Christmas Gift Budget Calculator</h1><p class="lede">Enter your total holiday budget and who you're buying for. See what the gifts add up to, what's left for food and decorations, and how much to save each week until Christmas.</p>
<div class="calc"><style>.row.gp{{grid-template-columns:1fr 220px}}@media(max-width:480px){{.row.gp{{grid-template-columns:1fr}}}}</style>
<div class="row"><label>Total holiday budget ($)</label><input id="tot" type="number" value="1500"></div>
<div class="row"><label>Food, decorations & travel ($)</label><input id="oth" type="number" value="350"></div>
<div class="row"><label>Already saved ($)</label><input id="sav" type="number" value="300"></div>
<h3>Gifts: group · people · $ each</h3>{rows}
<div class="result" id="res"></div></div>
<p>Not sure what to give each person? See gift budgets for <a href="../holidays/christmas-gifts-for-kids.html">kids</a>, <a href="../holidays/christmas-gifts-for-your-partner.html">your partner</a>, <a href="../holidays/christmas-gifts-for-parents.html">parents</a>, <a href="../holidays/christmas-gifts-for-friends.html">friends</a>, <a href="../holidays/christmas-gifts-for-coworkers.html">coworkers</a> and <a href="../holidays/christmas-gifts-for-teachers.html">teachers</a>.</p>
{B.cta("Christmas & Holiday Budget Planner", "The same plan in a spreadsheet: every person on your list, bought and wrapped checkboxes, and what's left.", B.G + GIFT_PRODUCT, "Get it — €4.99")}
<script>function f(v){{return (v<0?'-':'')+'$'+Math.abs(v).toLocaleString('en-US',{{maximumFractionDigits:0}})}}
function c(){{let g=0;document.querySelectorAll('.row.gp').forEach(r=>{{g+=(+r.querySelector('.gc').value||0)*(+r.querySelector('.ga').value||0)}});
const T=+tot.value||0,O=+oth.value||0,S=+sav.value||0,left=T-O-g,now=new Date(),y=now.getMonth()==11&&now.getDate()>20?now.getFullYear()+1:now.getFullYear(),
wk=Math.max(1,Math.ceil((new Date(y,11,20)-now)/6048e5)),need=Math.max(0,Math.min(T,O+g)-S);
const st=(l,v,s,neg)=>`<div class="stat"><div class="l">${{l}}</div><div class="v">${{v}}</div><div class="l ${{neg?'neg':''}}">${{s}}</div></div>`;
res.innerHTML=st('Gifts total',f(g),'all groups')+st(left<0?'Over budget':'Left in budget',f(Math.abs(left)),left<0?'lower amounts or shorten the list':'after gifts and other costs',left<0)
+st('Save per week',f(need/wk),wk+' weeks until Dec 20')}}
document.querySelectorAll('input').forEach(e=>e.addEventListener('input',c));c();</script>"""
    return "calculators/christmas-gift-budget-calculator.html", "Christmas Gift Budget Calculator (Free)", "Free Christmas gift budget calculator: split your holiday budget by person, see what's left and how much to save each week until Christmas.", body


def build(B):
    art = lambda t, d: {"@context": "https://schema.org", "@type": "Article", "headline": t, "description": d, "datePublished": B.TODAY.isoformat(), "author": {"@type": "Organization", "name": "ClarityPaperCo"}}
    p, t, d, b = calculator(B)
    B.write(p, B.page(t + " | ClarityPaperCo", d, b, 1, p, {"@context": "https://schema.org", "@type": "WebApplication", "name": t, "applicationCategory": "FinanceApplication", "offers": {"@type": "Offer", "price": "0"}}, "website"))
    cards = []
    for r in RECIP:
        p, t, d, b = gift_page(B, *r)
        B.write(p, B.page(t + " | ClarityPaperCo", d, b, 1, p, art(t, d)))
        cards.append(B.card(p, "Gifts", "For " + r[1].lower(), f"Budget levels for {r[2]}."))
    p, t, d, b = black_friday(B)
    B.write(p, B.page(t + " | ClarityPaperCo", d, b, 1, p, art(t, d)))
    return f"""<h2 id="holidays">Christmas & holiday budget</h2><div class="grid">{B.card("calculators/christmas-gift-budget-calculator.html", "Calculator", "Christmas Gift Budget Calculator", "Split your holiday budget by person and see what to save each week.")}{B.card("holidays/black-friday-budget.html", "Guide", "Black Friday budget", "A spending limit and a shopping plan before the sales start.")}{"".join(cards)}</div>"""
