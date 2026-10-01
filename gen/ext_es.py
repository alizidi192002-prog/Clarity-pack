"""Spanish section (/es/): simulators, worked budgets in euros, products.

Loaded by gen/build.py as an extension. Product links live in gen/es_links.json.
"""
import datetime, html, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://alizidi192002-prog.github.io/Clarity-pack"
STORE = "https://claritydigital8.gumroad.com/"
START = datetime.date(2026, 10, 1)
FIRST, PER_DAY = 6, 2
NB = chr(160)
KEYS = ("presupuesto2027", "navidad", "boda", "autonomos", "pack")


def links():
    try:
        d = json.load(open(os.path.join(HERE, "es_links.json"), encoding="utf-8"))
    except Exception:
        d = {}
    return {k: (d.get(k) or STORE) for k in KEYS}


def eur(v):
    return f"{v:,.0f}".replace(",", ".") + NB + "€"


def page(title, desc, body, depth, path, today, schema=None, og="article"):
    up = "../" * depth
    es_root = "../" * (depth - 1) if depth > 1 else ""
    ld = '<script type="application/ld+json">%s</script>' % json.dumps(schema, ensure_ascii=False) if schema else ""
    t, d = html.escape(title, quote=True), html.escape(desc, quote=True)
    alt = f'<link rel="alternate" hreflang="es" href="{BASE}/es/"><link rel="alternate" hreflang="en" href="{BASE}/"><link rel="alternate" hreflang="fr" href="{BASE}/fr/">' if path == "es/index.html" else ""
    return f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{t}</title><meta name="description" content="{d}">
<link rel="canonical" href="{BASE}/{path}">{alt}
<meta property="og:title" content="{t}"><meta property="og:description" content="{d}"><meta property="og:type" content="{og}"><meta property="og:locale" content="es_ES">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Inter:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{up}style.css">{ld}</head><body>
<header class="site"><div class="wrap"><a class="logo" href="{es_root}index.html"><span class="m">CP</span>ClarityPaperCo</a>
<nav><a href="{es_root}index.html#simuladores">Simuladores</a><a href="{es_root}presupuestos/index.html">Ejemplos</a><a href="{es_root}index.html#plantillas">Plantillas</a></nav></div></header>
<main><div class="wrap">{body}</div></main>
<footer><div class="wrap">© {today.year} ClarityPaperCo — plantillas sencillas para organizar tu dinero. Contenido informativo, no es asesoramiento financiero. · <a href="{up}index.html">English</a> · <a href="{up}fr/index.html">Français</a></div></footer>
</body></html>"""


def cta(title, text, href, label, pack=None):
    a = f' <a class="btn alt" href="{pack}">Pack 4 plantillas 14,99{NB}€</a>' if pack else ""
    return f'<div class="cta"><div><strong>{title}</strong>{text}</div><a class="btn" href="{href}">{label}</a>{a}</div>'


NC = ' class="n"'


def table(head, rows, total=None):
    h = "".join(f'<th{NC if i else ""}>{c}</th>' for i, c in enumerate(head))
    b = "".join("<tr>" + "".join(f'<td{NC if i else ""}>{c}</td>' for i, c in enumerate(r)) + "</tr>" for r in rows)
    t = "<tr>" + "".join(f'<th{NC if i else ""}>{c}</th>' for i, c in enumerate(total)) + "</tr>" if total else ""
    return f'<div class="tablewrap"><table><tr>{h}</tr>{b}{t}</table></div>'


def card(href, k, t, p):
    return f'<a class="card" href="{href}"><div class="k">{html.escape(k)}</div><h3>{html.escape(t)}</h3><p>{html.escape(p)}</p></a>'


def salary_page(m, L, today):
    R = lambda v: int(round(v))
    def rows(lst):
        return [(n, eur(R(m * s))) for n, s in lst], sum(R(m * s) for _, s in lst)
    nr, nt = rows([("Alquiler o hipoteca", .25), ("Supermercado", .10), ("Luz, agua y teléfono", .06), ("Transporte", .05)])
    wr, wt = rows([("Restaurantes y salidas", .10), ("Ocio y vacaciones", .08), ("Compras", .07), ("Suscripciones", .05)])
    sr, st = rows([("Fondo de emergencia", .10), ("Proyectos (coche, entrada…)", .05), ("Ahorro a largo plazo", .05)])
    if m < 1400:
        tip = f"Con {eur(m)} al mes, los gastos básicos suelen superar la mitad del presupuesto, sobre todo por la vivienda. Es normal: empieza con 60/25/15 o 70/20/10 y sube el ahorro en cuanto desaparezca un gasto."
    elif m < 2200:
        tip = f"Con {eur(m)} al mes la regla 50/30/20 suele encajar. La palanca principal es la vivienda: si tu alquiler supera claramente {eur(R(m * .33))}, recorta primero en caprichos antes que en ahorro."
    else:
        tip = f"Con {eur(m)} al mes a menudo puedes ahorrar más del 20 %. Mantén tu nivel de gasto estable cuando suban los ingresos y destina la diferencia al ahorro."
    title = f"Presupuesto con {eur(m)} al mes: la regla 50/30/20 (ejemplo detallado)"
    desc = f"Cómo repartir un sueldo de {eur(m)} netos al mes con la regla 50/30/20: {eur(m * .5)} para lo básico, {eur(m * .3)} para caprichos y {eur(m * .2)} para ahorro, con un ejemplo por partida."
    body = f"""<h1>{title}</h1><p class="meta">Actualizado el {today.strftime('%d/%m/%Y')} · 4 min de lectura</p>
<p class="lede">¿Cobras {eur(m)} netos al mes? La regla 50/30/20 te da un punto de partida sencillo: la mitad para gastos básicos, un 30 % para caprichos y un 20 % para ahorro o deudas.</p>
<h2>El reparto</h2>
{table(["Partida", "Parte", "Al mes"], [("Básicos", "50 %", eur(m * .5)), ("Caprichos", "30 %", eur(m * .3)), ("Ahorro", "20 %", eur(m * .2))], ("Total", "100 %", eur(m)))}
<p>Son {eur(m * 12)} al año (en 12 pagas) y un ahorro posible de {eur(m * .2 * 12)} en doce meses.</p>
<h2>Ejemplo: básicos ({eur(m * .5)})</h2>
{table(["Gasto", "Al mes"], nr, ("Subtotal", eur(nt)))}
<p>Quedan unos {eur(m * .5 - nt)} para seguros, guardería o cuotas de préstamos.</p>
<h2>Ejemplo: caprichos ({eur(m * .3)})</h2>
{table(["Gasto", "Al mes"], wr, ("Subtotal", eur(wt)))}
<h2>Ejemplo: ahorro ({eur(m * .2)})</h2>
{table(["Objetivo", "Al mes"], sr, ("Subtotal", eur(st)))}
<div class="box"><strong>Consejo para este sueldo:</strong> {tip}</div>
<p>Son cifras orientativas, no una regla. Prueba con tus números en el <a href="../simuladores/presupuesto-50-30-20.html">simulador 50/30/20 gratis</a> o calcula <a href="../simuladores/objetivo-de-ahorro.html">cuánto ahorrar al mes</a> para un proyecto.</p>
{cta("Presupuesto 2027 — plantilla mensual y anual", "12 pestañas mensuales, previsto vs real y tasa de ahorro automática. En español y en euros.", L["presupuesto2027"], f"Ver la plantilla — 6,99{NB}€", L["pack"])}"""
    return f"es/presupuestos/presupuesto-{m}-euros-al-mes.html", title, desc, body


WED = [("Lugar de celebración", .22), ("Catering y bebidas", .28), ("Foto y vídeo", .10), ("Flores y decoración", .08), ("Vestuario y complementos", .07),
       ("Música y animación", .06), ("Anillos", .05), ("Peluquería y maquillaje", .03), ("Invitaciones y papelería", .02), ("Transporte", .02),
       ("Detalles para invitados", .02), ("Imprevistos", .05)]


def wedding_page(t, L, today):
    rows = [(n, f"{int(p * 100)} %", eur(t * p)) for n, p in WED]
    guests = [(g, eur(t / g)) for g in (50, 80, 100, 150)]
    title = f"Presupuesto de boda de {eur(t)}: cómo repartirlo por partidas"
    desc = f"Una boda de {eur(t)} repartida por partidas: lugar, catering, fotógrafo, vestuario, decoración… y el presupuesto por invitado de 50 a 150 invitados."
    body = f"""<h1>{title}</h1><p class="meta">Actualizado el {today.strftime('%d/%m/%Y')} · 4 min de lectura</p>
<p class="lede">Esta es una forma de repartir un presupuesto de boda de {eur(t)} a partir de un reparto en porcentajes muy utilizado. Después, mueve el dinero hacia lo que más te importe.</p>
<h2>Reparto por partidas</h2>
{table(["Partida", "Parte", "Importe"], rows, ("Total", "100 %", eur(t)))}
<h2>Presupuesto por invitado</h2>
{table(["Invitados", "Presupuesto total por invitado"], guests)}
<div class="box"><strong>Guarda el colchón.</strong> Los {eur(t * .05)} de imprevistos están ahí porque casi siempre algún proveedor acaba por encima del primer presupuesto.</div>
{cta("Presupuesto de Boda — plantilla completa", "Este reparto ya preparado: previsto vs presupuestado vs pagado, calendario de señales y lista de invitados con confirmaciones y menús.", L["boda"], f"Ver la plantilla — 6,99{NB}€", L["pack"])}"""
    return f"es/presupuestos/presupuesto-boda-{t}-euros.html", title, desc, body


XMAS = [("Regalos", .60), ("Comidas y cenas", .20), ("Decoración y envoltorios", .10), ("Viajes y salidas", .10)]


def xmas_page(t, L, today):
    rows = [(n, f"{int(p * 100)} %", eur(t * p)) for n, p in XMAS]
    weeks = [(w, eur(-(-t // w))) for w in (6, 8, 10, 12)]
    title = f"Presupuesto de Navidad de {eur(t)}: reparto y plan de ahorro"
    desc = f"Cómo repartir un presupuesto de Navidad de {eur(t)} entre regalos, comidas, decoración y viajes, y cuánto ahorrar cada semana para pagarlo sin deudas."
    body = f"""<h1>{title}</h1><p class="meta">Actualizado el {today.strftime('%d/%m/%Y')} · 3 min de lectura</p>
<p class="lede">Un presupuesto de Navidad de {eur(t)} rinde más si lo repartes antes de comprar. Aquí tienes un reparto sencillo y un plan para ahorrarlo sin tirar de tarjeta.</p>
<h2>Repartir los {eur(t)}</h2>
{table(["Partida", "Parte", "Importe"], rows, ("Total", "100 %", eur(t)))}
<h2>Cuánto ahorrar cada semana</h2>
{table(["Semanas hasta las compras", "Ahorrar por semana"], weeks)}
<p>Con {eur(t * .6)} para regalos, fija un importe por persona antes de comprar nada y apunta cada compra.</p>
{cta("Presupuesto de Navidad y Fiestas", "Lista de regalos con casillas comprado / envuelto, otros gastos de las fiestas y lo que te queda.", L["navidad"], f"Ver la plantilla — 4,99{NB}€", L["pack"])}"""
    return f"es/presupuestos/presupuesto-navidad-{t}-euros.html", title, desc, body


FMT = "function f(v){return Math.round(v).toLocaleString('es-ES')+'\\u00a0€'}"


def sim_503020(L):
    body = f"""<h1>Simulador de presupuesto 50/30/20</h1><p class="lede">Escribe tu sueldo neto mensual para ver cuánto destinar a básicos, caprichos y ahorro, y compáralo con lo que gastas ahora.</p>
<div class="calc">
<div class="row"><label>Ingresos netos al mes</label><input id="inc" type="number" value="1600"></div>
<h3>Lo que gastas ahora (opcional)</h3>
<div class="row"><label>Básicos (alquiler, facturas, compra, transporte)</label><input id="n" type="number" value="950"></div>
<div class="row"><label>Caprichos (salidas, ocio, compras)</label><input id="w" type="number" value="450"></div>
<div class="row"><label>Ahorro y amortizaciones</label><input id="s" type="number" value="200"></div>
<div class="result" id="res"></div></div>
<p>Mira <a href="../presupuestos/index.html">ejemplos detallados por sueldo</a>.</p>
{cta("Presupuesto 2027 — plantilla mensual y anual", "Controla cada gasto, con diferencias en rojo y tasa de ahorro automática.", L["presupuesto2027"], f"Ver la plantilla — 6,99{NB}€", L["pack"])}
<script>{FMT}
function c(){{const i=+inc.value||0,t=[i*.5,i*.3,i*.2],a=[+n.value||0,+w.value||0,+s.value||0],l=['Básicos (50 %)','Caprichos (30 %)','Ahorro (20 %)'];
let h='';for(let k=0;k<3;k++){{const d=k<2?t[k]-a[k]:a[k]-t[k];h+=`<div class="stat"><div class="l">${{l[k]}}</div><div class="v">${{f(t[k])}}</div><div class="l ${{d<0?'neg':''}}">Tú: ${{f(a[k])}} (${{d<0?(k<2?'te pasas':'te falta'):'ok'}} ${{f(Math.abs(d))}})</div></div>`}}
res.innerHTML=h}}document.querySelectorAll('input').forEach(e=>e.addEventListener('input',c));c();</script>"""
    return "es/simuladores/presupuesto-50-30-20.html", "Simulador de presupuesto 50/30/20 (gratis)", "Simulador gratis de la regla 50/30/20: cuánto destinar a básicos, caprichos y ahorro según tu sueldo neto.", body


def sim_ahorro(L):
    body = f"""<h1>Simulador de objetivo de ahorro</h1><p class="lede">¿Cuánto tienes que ahorrar cada mes para llegar a tu objetivo: entrada de un piso, coche, boda, viaje o fondo de emergencia?</p>
<div class="calc">
<div class="row"><label>Objetivo (€)</label><input id="g" type="number" value="8000"></div>
<div class="row"><label>Ya ahorrado (€)</label><input id="h" type="number" value="1000"></div>
<div class="row"><label>¿En cuántos meses?</label><input id="m" type="number" value="24"></div>
<div class="row"><label>Interés anual (%)</label><input id="r" type="number" step="0.1" value="0"></div>
<div class="result" id="res"></div></div>
<div class="box">El interés es opcional: deja 0 para un cálculo sin intereses o escribe el de tu cuenta de ahorro.</div>
{cta("Presupuesto 2027 — plantilla mensual y anual", "Planifica tu ahorro mes a mes y sigue tu tasa de ahorro durante el año.", L["presupuesto2027"], f"Ver la plantilla — 6,99{NB}€", L["pack"])}
<script>{FMT}
function c(){{const G=+g.value||0,H=+h.value||0,M=Math.max(1,+m.value||1),r=(+r_.value||0)/1200;const fv=H*Math.pow(1+r,M);const need=Math.max(0,G-fv);
const p=r?need*r/(Math.pow(1+r,M)-1):need/M;const paid=H+p*M;
res.innerHTML=`<div class="stat"><div class="l">Ahorrar al mes</div><div class="v">${{f(p)}}</div><div class="l">durante ${{M}} meses</div></div><div class="stat"><div class="l">Tus aportaciones</div><div class="v">${{f(paid)}}</div><div class="l">incluido lo ahorrado</div></div><div class="stat"><div class="l">Intereses</div><div class="v">${{f(Math.max(0,G-paid))}}</div><div class="l">estimación</div></div>`}}
const r_=document.getElementById('r');document.querySelectorAll('input').forEach(e=>e.addEventListener('input',c));c();</script>"""
    return "es/simuladores/objetivo-de-ahorro.html", "Simulador de objetivo de ahorro (gratis)", "Calcula cuánto ahorrar cada mes para alcanzar un objetivo en una fecha, con o sin intereses.", body


def build(B):
    L, today = links(), B.TODAY
    sims = []
    for fn in (sim_503020, sim_ahorro):
        p, t, d, b = fn(L)
        B.write(p, page(t + " | ClarityPaperCo", d, b, 2, p, today, {"@context": "https://schema.org", "@type": "WebApplication", "name": t, "inLanguage": "es", "applicationCategory": "FinanceApplication", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"}}, "website"))
        sims.append((p[3:], t.replace(" (gratis)", ""), d.split(":")[0]))
    s = [salary_page(m, L, today) for m in range(1000, 3001, 100)]
    w = [wedding_page(t, L, today) for t in range(5000, 40001, 5000)]
    x = [xmas_page(t, L, today) for t in (200, 300, 400, 500, 750, 1000)]
    order = []
    while s or w or x:
        for lst in (s, s, w, x):
            if lst:
                order.append(lst.pop(0))
    live = order[:FIRST + PER_DAY * max(0, (today - START).days)]
    groups = {"Presupuesto según tu sueldo": [], "Presupuestos de boda": [], "Presupuestos de Navidad": []}
    for p, t, d, b in live:
        sch = {"@context": "https://schema.org", "@type": "Article", "headline": t, "description": d, "inLanguage": "es", "datePublished": today.isoformat(), "author": {"@type": "Organization", "name": "ClarityPaperCo"}}
        B.write(p, page(t + " | ClarityPaperCo", d, b, 2, p, today, sch))
        key = "Presupuestos de boda" if "boda" in p else "Presupuestos de Navidad" if "navidad" in p else "Presupuesto según tu sueldo"
        groups[key].append((p[16:], t))
    hub = '<h1>Ejemplos de presupuestos en euros</h1><p class="lede">Ejemplos con cifras: cómo repartir un sueldo neto con la regla 50/30/20 y cómo organizar una boda o la Navidad con un presupuesto fijo.</p>'
    for g, items in groups.items():
        if items:
            hub += f"<h2>{g}</h2><ul>" + "".join(f'<li><a href="{p}">{html.escape(t)}</a></li>' for p, t in items) + "</ul>"
    B.write("es/presupuestos/index.html", page("Ejemplos de presupuestos en euros | ClarityPaperCo", "Ejemplos de presupuestos 50/30/20 de 1.000 € a 3.000 € al mes, presupuestos de boda y de Navidad con cifras concretas.", hub, 2, "es/presupuestos/index.html", today, og="website"))
    prods = [("Presupuesto anual", "Presupuesto 2027 — mensual y anual", f"12 pestañas mensuales, previsto vs real, resumen anual. 6,99{NB}€", L["presupuesto2027"]),
             ("Fiestas", "Presupuesto de Navidad y Fiestas", f"Lista de regalos, comidas, decoración y lo que queda. 4,99{NB}€", L["navidad"]),
             ("Boda", "Presupuesto de Boda", f"Reparto, presupuestos de proveedores, señales e invitados. 6,99{NB}€", L["boda"]),
             ("Autónomos", "Control de Facturas — Autónomos", f"Facturas, vencidas, gastos y lo que apartar. 6,99{NB}€", L["autonomos"])]
    n_ex = sum(len(v) for v in groups.values())
    body = f"""<h1>Organiza tu presupuesto fácilmente, en euros</h1>
<p class="lede">Simuladores gratis, ejemplos de presupuestos con cifras y plantillas listas para usar para gestionar tu sueldo, preparar la Navidad u organizar una boda.</p>
<h2 id="simuladores">Simuladores gratis</h2><div class="grid">{"".join(card(p, "Simulador", t, d) for p, t, d in sims)}</div>
<h2 id="ejemplos">Ejemplos de presupuestos</h2><p><a href="presupuestos/index.html">Ver los {n_ex} ejemplos</a> — presupuesto según tu sueldo (regla 50/30/20), bodas y Navidad.</p>
<h2 id="plantillas">Plantillas en español</h2><div class="grid">{"".join(card(u, k, t, p) for k, t, p, u in prods)}</div>
{cta("Las 4 plantillas en un solo pack", "Presupuesto 2027, Navidad, boda y control de facturas para autónomos. Excel, Google Sheets y Numbers.", L["pack"], f"El pack — 14,99{NB}€")}"""
    B.write("es/index.html", page("Presupuesto fácil — simuladores gratis y ejemplos en euros | ClarityPaperCo", "Simuladores de presupuesto gratis, ejemplos de presupuestos en euros y plantillas de Excel / Google Sheets en español.", body, 1, "es/index.html", today, og="website"))
    return ""
