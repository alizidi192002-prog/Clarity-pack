"""Embeddable calculators: _site/embed/<name>.html plus an "Embed this calculator" box.

After the build, each calculator page's .calc block and its scripts are copied into a small
iframe-ready page (noindex). The calculator page gets a box with a copy-paste snippet: an
iframe plus a normal text link back to the calculator, so sites that embed it link to us.
"""
import atexit, html, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "_site")
BASE = "https://alizidi192002-prog.github.io/Clarity-pack"
CALCS = {  # calculator page -> (embed name, iframe height)
    "calculators/50-30-20-calculator.html": ("50-30-20", 790),
    "calculators/hourly-to-salary-calculator.html": ("hourly-to-salary", 800),
    "calculators/debt-snowball-avalanche-calculator.html": ("debt-payoff", 1050),
    "calculators/paycheck-budget-calculator.html": ("paycheck-budget", 1500),
}


def _block(s, start):
    """Return the balanced <div ...>...</div> starting at index start."""
    depth, i = 0, start
    for m in re.finditer(r"<div\b|</div>", s[start:]):
        depth += 1 if m.group(0) == "<div" else -1
        if depth == 0:
            return s[start:start + m.end()]
    return ""


def _write():
    try:
        os.makedirs(os.path.join(OUT, "embed"), exist_ok=True)
        n = 0
        for rel, (name, hgt) in CALCS.items():
            f = os.path.join(OUT, rel)
            if not os.path.isfile(f):
                continue
            s = open(f, encoding="utf-8").read()
            i = s.find('<div class="calc">')
            calc = _block(s, i) if i >= 0 else ""
            if not calc:
                continue
            h1 = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
            title = re.sub(r"<[^>]+>", "", h1.group(1)) if h1 else "Calculator"
            main = re.search(r"<main>.*</main>", s, re.S).group(0)
            scripts = "".join(x for x in re.findall(r"<script\b.*?</script>", main, re.S) if "ld+json" not in x)
            page_url = f"{BASE}/{rel}"
            embed = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} | ClarityPaperCo</title><meta name="robots" content="noindex">
<link rel="canonical" href="{page_url}"><base target="_blank">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600&family=Inter:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../style.css"><style>body{{background:transparent}}.wrap{{padding:8px 4px}}h2{{margin:0 0 12px}}.credit{{font-size:13px;margin-top:10px;color:var(--muted,#667)}}</style></head>
<body><div class="wrap"><h2>{html.escape(title)}</h2>{calc}
<p class="credit">Free calculator by <a href="{page_url}">ClarityPaperCo</a></p></div>{scripts}</body></html>"""
            open(os.path.join(OUT, "embed", name + ".html"), "w", encoding="utf-8").write(embed)
            snippet = (f'<iframe src="{BASE}/embed/{name}.html" width="100%" height="{hgt}" style="border:0;max-width:720px" '
                       f'loading="lazy" title="{html.escape(title)}"></iframe>\n'
                       f'<p><a href="{page_url}">{html.escape(title)}</a> by ClarityPaperCo</p>')
            box = (f'<div class="box" id="embed"><strong>Add this calculator to your site.</strong> It\'s free. Copy the code below '
                   f'and paste it into any page or blog post (WordPress: use a "Custom HTML" block).'
                   f'<textarea readonly rows="4" style="width:100%;margin-top:10px;font:13px/1.4 monospace;padding:8px;border-radius:8px" '
                   f'onclick="this.select()">{html.escape(snippet)}</textarea>'
                   f'<button type="button" class="btn" style="margin-top:8px;border:0;cursor:pointer" '
                   f'onclick="var t=this.previousElementSibling;t.select();try{{navigator.clipboard.writeText(t.value)}}catch(e){{document.execCommand(\'copy\')}};this.textContent=\'Copied\'">Copy code</button></div>')
            if 'id="embed"' not in s:
                s = s.replace("</div></main>", box + "</div></main>", 1)
                open(f, "w", encoding="utf-8").write(s)
            n += 1
        print("embeds:", n)
    except Exception as e:
        print("embeds skipped:", repr(e))


def build(B):
    atexit.register(_write)
    return ""
