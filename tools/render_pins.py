import os, sys
from playwright.sync_api import sync_playwright
sys.path.insert(0, os.path.dirname(__file__))
from pins_data import P

OUT = os.path.join(os.path.dirname(__file__), "..", "pack", "pins", "v2")
os.makedirs(OUT, exist_ok=True)

SERIF = "'Liberation Serif','Tinos','DejaVu Serif',Georgia,serif"
SANS = "'Liberation Sans','Arimo','DejaVu Sans',Arial,sans-serif"
MONO = "'DejaVu Sans Mono',monospace"
GREEN, DARK, GOLD, CREAM = "#2f6f52", "#17332a", "#c08a2e", "#f6f1e7"

BASE = f"""*{{box-sizing:border-box;margin:0;padding:0}}
body{{width:1000px;height:1500px;overflow:hidden;font-family:{SANS}}}
.brand{{display:flex;align-items:center;gap:14px;font:700 28px {SERIF}}}
.logo{{width:48px;height:48px;border-radius:10px;background:{GREEN};color:#fff;display:flex;align-items:center;justify-content:center;font:700 18px {MONO}}}
table{{width:100%;border-collapse:collapse;font:22px {MONO}}}
th{{background:{GREEN};color:#fff;text-align:right;padding:18px 20px;font-weight:700}}
td{{padding:15px 20px;text-align:right;color:#46524c;border-bottom:1px solid #e6e8e3}}
th:first-child,td:first-child{{text-align:left}}
tr.tot td{{font-weight:700;color:{DARK};background:#eef4ef;border-bottom:none}}
"""

def table(p, n=6):
    h = "".join(f"<th>{c}</th>" for c in p["cols"])
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in p["rows"][:n])
    if p.get("total"):
        b += "<tr class='tot'>" + "".join(f"<td>{c}</td>" for c in p["total"]) + "</tr>"
    return f"<table><tr>{h}</tr>{b}</table>"

def brand(color="#1f2a24"):
    return f"<div class='brand' style='color:{color}'><div class='logo'>CP</div>ClarityPaperCo</div>"

def design_a(p):  # dark hook
    return f"""<style>{BASE}
body{{background:{DARK};color:#fff;padding:80px 70px}}
.cat{{font:700 22px {MONO};letter-spacing:5px;color:{GOLD};margin-top:70px}}
h1{{font:700 96px/1.02 {SERIF};margin-top:22px}}
.sub{{font:400 34px/1.3 {SANS};color:#cfe0d6;margin-top:26px}}
  .card table{{font-size:27px}} .card td{{padding:22px 22px}} .card th{{padding:24px 22px}}
.card{{background:#fff;border-radius:14px;overflow:hidden;margin-top:60px;transform:rotate(-2deg);box-shadow:0 30px 60px rgba(0,0,0,.35)}}
.cta{{position:absolute;left:70px;right:70px;bottom:80px;background:{GOLD};color:#1b1b1b;border-radius:14px;padding:30px;text-align:center;font:700 34px {SANS}}}
</style>{brand('#fff')}
<div class='cat'>{p['cat']}</div><h1>{p['hook']}</h1>
<div class='sub'>{p['name']} &middot; Excel &amp; Google Sheets</div>
<div class='card'>{table(p,6)}</div>
<div class='cta'>In the 14-template Bundle &nbsp;&rarr;&nbsp; €19.99</div>"""

def design_b(p):  # cream checklist + stat
    checks = "".join(f"<li><span class='ck'>&#10003;</span>{c}</li>" for c in p["checks"])
    return f"""<style>{BASE}
body{{background:{CREAM};color:#1f2a24;padding:80px 70px}}
.rib{{display:inline-block;background:{GREEN};color:#fff;font:700 22px {MONO};letter-spacing:4px;padding:12px 22px;border-radius:8px;margin-top:60px}}
h1{{font:700 84px/1.05 {SERIF};margin-top:30px}}
.stat{{background:#fff;border-radius:18px;padding:40px 44px;margin-top:50px;box-shadow:0 10px 30px rgba(40,50,40,.08)}}
.sl{{font:400 26px {SANS};color:#6b766f}}
.sv{{font:700 88px {SERIF};color:{GREEN};margin-top:6px}}
.bar{{height:22px;border-radius:11px;background:#e7ebe5;margin-top:22px;overflow:hidden}}
.bar i{{display:block;height:100%;width:{p['progress']}%;background:{GOLD};border-radius:11px}}
.pl{{font:600 24px {SANS};color:#46524c;margin-top:14px}}
ul{{list-style:none;margin-top:48px}}
li{{font:700 36px {SANS};margin-bottom:26px;display:flex;align-items:center;gap:22px}}
.ck{{width:48px;height:48px;border-radius:50%;background:{GREEN};color:#fff;display:inline-flex;align-items:center;justify-content:center;font-size:28px;flex:none}}
.foot{{position:absolute;left:70px;right:70px;bottom:70px;display:flex;justify-content:space-between;align-items:flex-end;border-top:2px solid #ddd6c6;padding-top:28px}}
.pr{{font:700 54px {MONO};color:{GOLD}}} .nm{{font:600 26px/1.4 {SANS};color:#46524c;text-align:right}}
</style>{brand()}
<div class='rib'>{p['cat']} TEMPLATE</div><h1>{p['hook2']}</h1>
<div class='stat'><div class='sl'>{p['stat_label']}</div><div class='sv'>{p['stat']}</div>
<div class='bar'><i></i></div><div class='pl'>{p['progress_label']}</div></div>
<ul>{checks}</ul>
<div class='foot'><div class='pr'>€19.99</div><div class='nm'><b>Included in the Bundle</b><br>14 templates · Excel &amp; Google Sheets</div></div>"""

def design_c(p):  # spreadsheet window mockup
    letters = "".join(f"<span>{l}</span>" for l in "ABCD")
    return f"""<style>{BASE}
body{{background:#e3ece5;color:#1f2a24}}
.top{{padding:80px 70px 0}}
h1{{font:700 88px/1.03 {SERIF};margin-top:60px}}
.tag{{font:600 32px {SANS};color:{GREEN};margin-top:22px}}
.win{{margin:56px 50px 0;background:#fff;border-radius:16px;overflow:hidden;box-shadow:0 30px 70px rgba(20,50,30,.18)}}
.bar{{background:#f1f3f1;padding:18px 22px;display:flex;align-items:center;gap:10px;border-bottom:1px solid #e0e3df}}
.bar b{{width:16px;height:16px;border-radius:50%;background:#e0625a;display:inline-block}}
.bar b:nth-child(2){{background:#e8b33c}} .bar b:nth-child(3){{background:#5bb46a}}
.fn{{margin-left:18px;font:22px {SANS};color:#58625c}}
.fx{{padding:12px 22px;font:20px {MONO};color:#8a948e;border-bottom:1px solid #e0e3df}}
.cols{{display:grid;grid-template-columns:repeat(4,1fr);background:#f7f8f6;font:600 18px {MONO};color:#99a29c;text-align:center;border-bottom:1px solid #e0e3df}}
.cols span{{padding:8px;border-right:1px solid #e6e8e3}}
.band{{position:absolute;left:0;right:0;bottom:0;height:170px;background:{GREEN};color:#fff;display:flex;align-items:center;justify-content:space-between;padding:0 70px}}
.band .l{{font:700 34px {SANS}}} .band .l small{{display:block;font:400 26px {SANS};color:#cfe6d8;margin-top:8px}}
.band .r{{font:700 56px {MONO};color:#f3cf86}}
</style>
<div class='top'>{brand()}<h1>{p['name']}</h1><div class='tag'>{p['hook']}</div></div>
<div class='win'><div class='bar'><b></b><b></b><b></b><span class='fn'>{p['key'].title()} Tracker.xlsx</span></div>
<div class='fx'>fx&nbsp;&nbsp;=SUM(B2:B7)</div><div class='cols'>{letters}</div>{table(p,6)}</div>
<div class='band'><div class='l'>Included in the Bundle<small>14 templates · Excel &amp; Google Sheets</small></div><div class='r'>€19.99</div></div>"""

with sync_playwright() as pw:
    br = pw.chromium.launch()
    pg = br.new_page(viewport={"width": 1000, "height": 1500})
    for p in P:
        for tag, fn in (("a", design_a), ("b", design_b), ("c", design_c)):
            pg.set_content("<html><body>" + fn(p) + "</body></html>")
            pg.wait_for_timeout(50)
            pg.screenshot(path=os.path.join(OUT, f"{p['key']}_{tag}.jpg"), type="jpeg", quality=88)
    br.close()
print("done")
