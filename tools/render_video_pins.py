"""Short hook video pins (10 s, 2:3). Output pack/pins/video/<key>.mp4"""
import os, sys, glob, subprocess, shutil, tempfile
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "..", "pack", "pins", "video"); os.makedirs(OUT, exist_ok=True)
SERIF = "'Liberation Serif','Tinos',Georgia,serif"; SANS = "'Liberation Sans',Arial,sans-serif"; MONO = "'DejaVu Sans Mono',monospace"
V = {
 "christmas": dict(col="#7a1f2b", hook=["Stop", "overspending", "this", "Christmas."], cols=["Person", "Budget", "Spent"],
   rows=[["Mom", 60, 54], ["Dad", 50, 0], ["Sara", 25, 22], ["Tree & lights", 90, 85]], name="Christmas & Holiday Budget Planner", cta="€4.99 · Excel & Google Sheets"),
 "budget2027": dict(col="#1f3a5f", hook=["Start", "2027", "with a", "real plan."], cols=["Category", "Planned", "Actual"],
   rows=[["Housing", 1200, 1200], ["Groceries", 450, 412], ["Transport", 220, 198], ["Savings", 600, 650]], name="2027 Budget Planner", cta="€6.99 · Excel & Google Sheets"),
 "debt": dict(col="#17332a", hook=["Your", "debt-free", "date?", "Find out."], cols=["Debt", "Balance", "Min"],
   rows=[["Credit card", 3400, 95], ["Car loan", 8200, 240], ["Student loan", 14500, 160], ["Personal loan", 4800, 150]], name="Debt Snowball & Avalanche Tracker", cta="In the 14-template Bundle · €19.99"),
 "paycheck": dict(col="#8a4b14", hook=["Which", "paycheck", "pays which", "bill?"], cols=["Bill", "Amount", "Paycheck"],
   rows=[["Rent", 950, 1], ["Car", 240, 1], ["Phone", 60, 2], ["Groceries", 300, 2]], name="Paycheck to Paycheck Budget Planner", cta="€4.99 · Excel & Google Sheets"),
 "freelancer": dict(col="#5b3a6e", hook=["Who still", "owes you", "money?", ""], cols=["Client", "Invoice", "Status"],
   rows=[["Studio A", 1200, "Paid"], ["Shop B", 450, "Overdue"], ["Agency C", 800, "Sent"], ["Client D", 300, "Overdue"]], name="Freelancer Income & Invoice Tracker", cta="€6.99 · Excel & Google Sheets"),
}
def page(v):
    words = "".join(f"<span class='w' style='animation-delay:{0.4+i*0.55}s'>{w}</span> " for i, w in enumerate(v["hook"]) if w)
    head = "".join(f"<th>{c}</th>" for c in v["cols"])
    rows = "".join(f"<tr style='animation-delay:{4.0+i*0.7}s'>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for i, r in enumerate(v["rows"]))
    return f"""<html><head><style>
*{{box-sizing:border-box;margin:0;padding:0}} body{{width:720px;height:1080px;overflow:hidden;background:{v['col']};font-family:{SANS};color:#fff;position:relative}}
.brand{{position:absolute;left:50px;top:50px;font:700 22px {SERIF}}}
.hook{{position:absolute;left:50px;right:40px;top:150px;font:700 84px/1.05 {SERIF}}}
.w{{display:inline-block;opacity:0;transform:translateY(30px);animation:in .5s forwards}}
@keyframes in{{to{{opacity:1;transform:none}}}}
.hook{{animation:up 0.6s 3.2s forwards}} @keyframes up{{to{{top:70px;font-size:50px;opacity:.95}}}}
.card{{position:absolute;left:40px;right:40px;top:330px;background:#fff;border-radius:16px;overflow:hidden;opacity:0;animation:in .6s 3.4s forwards;box-shadow:0 20px 50px rgba(0,0,0,.35)}}
table{{width:100%;border-collapse:collapse;font:24px {MONO};color:#333}} th{{background:#2f6f52;color:#fff;padding:18px;text-align:right}} td{{padding:18px;text-align:right;border-bottom:1px solid #eee}}
th:first-child,td:first-child{{text-align:left}} tr{{opacity:0;animation:in .4s forwards}} tr:first-child{{opacity:1;animation:none}}
.cta{{position:absolute;left:40px;right:40px;bottom:60px;opacity:0;animation:in .6s 7.4s forwards;text-align:center}}
.cta .n{{font:700 34px/1.2 {SERIF}}} .cta .b{{margin-top:22px;background:#e9b949;color:#1b1b1b;border-radius:14px;padding:22px;font:700 26px {SANS}}}
</style></head><body><div class='brand'>ClarityPaperCo</div><div class='hook'>{words}</div>
<div class='card'><table><tr>{head}</tr>{rows}</table></div>
<div class='cta'><div class='n'>{v['name']}</div><div class='b'>{v['cta']}</div></div></body></html>"""
with sync_playwright() as pw:
    for k, v in V.items():
        tmp = tempfile.mkdtemp()
        br = pw.chromium.launch(); ctx = br.new_context(viewport={"width": 720, "height": 1080}, record_video_dir=tmp, record_video_size={"width": 720, "height": 1080})
        pg = ctx.new_page(); pg.set_content(page(v)); pg.wait_for_timeout(10500); ctx.close(); br.close()
        webm = glob.glob(tmp + "/*.webm")[0]
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", webm, "-t", "10", "-vf", "fps=30,format=yuv420p", "-c:v", "libx264", "-preset", "veryfast", "-crf", "26", "-movflags", "+faststart", os.path.join(OUT, f"{k}.mp4")], check=True)
        shutil.rmtree(tmp)
print("ok")
