"""Short hook video pins (10 s, 2:3) for the remaining 5 Etsy listings. Output pack/pins/video/<key>.mp4"""
import os, glob, subprocess, shutil, tempfile
from playwright.sync_api import sync_playwright
HERE = os.path.dirname(__file__)
OUT = os.path.join(HERE, "..", "pack", "pins", "video"); os.makedirs(OUT, exist_ok=True)
SERIF = "'Liberation Serif','Tinos',Georgia,serif"; SANS = "'Liberation Sans',Arial,sans-serif"; MONO = "'DejaVu Sans Mono',monospace"
V = {
 "subscription": dict(col="#1b4b4f", hook=["Stop paying", "for subs", "you", "forgot."], cols=["Service", "Monthly", "Renews"],
   rows=[["Netflix", "€15", "Nov 12"], ["Spotify", "€11", "Nov 18"], ["Gym", "€35", "Dec 1"], ["Cloud 2TB", "€10", "Nov 25"]],
   name="Subscription & Bill Tracker", cta="€4.49 · Excel & Google Sheets"),
 "sinking": dict(col="#3f2f5c", hook=["Save for", "big goals,", "a little", "at a time."], cols=["Goal", "Target", "Saved"],
   rows=[["Vacation", 1500, 900], ["Car repair", 800, 650], ["Holiday gifts", 400, 250], ["New laptop", 1200, 300]],
   name="Sinking Funds Tracker", cta="€4.49 · Excel & Google Sheets"),
 "networth": dict(col="#0f2d3d", hook=["What are", "you really", "worth?", "Find out."], cols=["Account", "Type", "Value"],
   rows=[["Checking", "Asset", "€2,400"], ["Savings", "Asset", "€8,600"], ["Investments", "Asset", "€15,200"], ["Mortgage", "Debt", "-€180,000"]],
   name="Net Worth Tracker", cta="€4.99 · Excel & Google Sheets"),
 "502030": dict(col="#6e3b1f", hook=["The", "50/30/20", "rule,", "made simple."], cols=["Category", "%", "Amount"],
   rows=[["Needs", "50%", "€1,500"], ["Wants", "30%", "€900"], ["Savings", "20%", "€600"]],
   name="50/30/20 Budget Planner", cta="€4.49 · Excel & Google Sheets"),
 "bundle": dict(col="#1f4f3a", hook=["14 templates.", "One", "download.", "€19.99"], cols=["Included", "Files"],
   rows=[["Budget planners", 3], ["Debt & savings", 3], ["Bills & net worth", 2], ["Business & life", 6]],
   name="Complete Budget & Planner Bundle", cta="€19.99 · 14 templates in one download"),
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
