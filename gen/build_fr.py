"""French section of the ClarityPaperCo site (/fr/). Called from gen/build.py.

Generates fr/index.html, fr/budgets/*, fr/simulateurs/* and lists any hand-written
articles found in docs/fr/articles/. Product links live in gen/fr_links.json.
"""
import datetime, html, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "https://alizidi192002-prog.github.io/Clarity-pack"
STORE = "https://claritydigital8.gumroad.com/"
RELEASE_START = datetime.date(2026, 10, 1)
RELEASE_FIRST = 6
RELEASE_PER_DAY = 2
NB = " "


def links():
    try:
        d = json.load(open(os.path.join(HERE, "fr_links.json"), encoding="utf-8"))
    except Exception:
        d = {}
    return {k: (d.get(k) or STORE) for k in ("budget2027", "noel", "mariage", "autoentrepreneur", "pack", "fiche", "planner_pdf")}


def eur(v):
    return f"{v:,.0f}".replace(",", NB) + NB + "€"


def page(title, desc, body, depth, path, today, schema=None, og="article"):
    up = "../" * depth
    fr_root = "../" * (depth - 1) if depth > 1 else ""
    ld = '<script type="application/ld+json">%s</script>' % json.dumps(schema, ensure_ascii=False) if schema else ""
    t, d = html.escape(title, quote=True), html.escape(desc, quote=True)
    alt = f'<link rel="alternate" hreflang="fr" href="{BASE}/{path}"><link rel="alternate" hreflang="en" href="{BASE}/">' if path == "fr/" else ""
    return f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{t}</title><meta name="description" content="{d}">
<link rel="canonical" href="{BASE}/{path}">{alt}
<meta property="og:title" content="{t}"><meta property="og:description" content="{d}"><meta property="og:type" content="{og}"><meta property="og:locale" content="fr_FR">
<link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Inter:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{up}style.css">{ld}</head><body>
<header class="site"><div class="wrap"><a class="logo" href="{fr_root}index.html"><span class="m">CP</span>ClarityPaperCo</a>
<nav><a href="{fr_root}index.html#guides">Guides</a><a href="{fr_root}index.html#simulateurs">Simulateurs</a><a href="{fr_root}budgets/index.html">Par revenu</a><a href="{fr_root}fiche-budget-gratuite.html">Gratuit</a><a href="{fr_root}index.html#tableurs">Tableurs</a></nav></div></header>
<main><div class="wrap">{body}</div></main>
<footer><div class="wrap">© {today.year} ClarityPaperCo — des tableurs simples pour gérer son argent. Contenu à titre informatif, ne constitue pas un conseil financier. · <a href="{up}index.html">English</a></div></footer>
</body></html>"""


def cta(title, text, href, label, pack=None):
    a = f' <a class="btn alt" href="{pack}">Pack 4 tableurs 14,99{NB}€</a>' if pack else ""
    return f'<div class="cta"><div><strong>{title}</strong>{text}</div><a class="btn" href="{href}">{label}</a>{a}</div>'


NC = ' class="n"'


def table(head, rows, total=None):
    h = "".join(f'<th{NC if i else ""}>{c}</th>' for i, c in enumerate(head))
    b = "".join("<tr>" + "".join(f'<td{NC if i else ""}>{c}</td>' for i, c in enumerate(r)) + "</tr>" for r in rows)
    t = "<tr>" + "".join(f'<th{NC if i else ""}>{c}</th>' for i, c in enumerate(total)) + "</tr>" if total else ""
    return f'<div class="tablewrap"><table><tr>{h}</tr>{b}{t}</table></div>'


# ------------------------------------------------------------------ pages programmatiques
def salary_page(m, L, today):
    R = lambda v: int(round(v))
    needs, wants, save = m * .5, m * .3, m * .2
    nx = [("Loyer ou crédit immobilier", .25), ("Courses", .10), ("Énergie, eau & téléphone", .06), ("Transport", .05)]
    wx = [("Restaurants & sorties", .10), ("Loisirs & vacances", .08), ("Shopping", .07), ("Abonnements", .05)]
    sx = [("Épargne de précaution", .10), ("Projets (voiture, apport…)", .05), ("Épargne long terme", .05)]
    def rows(lst):
        return [(n, eur(R(m * s))) for n, s in lst], sum(R(m * s) for _, s in lst)
    nr, nt = rows(nx)
    wr, wt = rows(wx)
    sr, st = rows(sx)
    if m < 1800:
        tip = f"Avec {eur(m)} par mois, les dépenses essentielles dépassent souvent la moitié du budget, surtout à cause du loyer. C'est normal : partez sur 60/25/15 ou 70/20/10 et augmentez la part d'épargne dès qu'une charge disparaît. Pensez aussi à vérifier vos droits (APL, prime d'activité) sur les sites officiels."
    elif m < 2800:
        tip = f"{eur(m)} par mois permet en général d'appliquer la règle 50/30/20. Le levier principal reste le logement : si votre loyer dépasse nettement {eur(R(m * .33))}, réduisez d'abord les envies avant de toucher à l'épargne."
    else:
        tip = f"Avec {eur(m)} par mois, vous pouvez souvent dépasser 20 % d'épargne. Beaucoup de ménages à ce niveau gardent leur train de vie stable quand les revenus augmentent et versent la différence vers l'épargne."
    title = f"Budget avec {eur(m)} par mois : la méthode 50/30/20 (exemple détaillé)"
    desc = f"Comment répartir un salaire de {eur(m)} net par mois avec la règle 50/30/20 : {eur(needs)} pour l'essentiel, {eur(wants)} pour les envies, {eur(save)} pour l'épargne, avec un exemple par poste."
    body = f"""<h1>{title}</h1><p class="meta">Mis à jour le {today.strftime('%d/%m/%Y')} · 4 min de lecture</p>
<p class="lede">Vous touchez {eur(m)} net par mois ? La règle 50/30/20 donne un point de départ simple : la moitié pour les dépenses essentielles, 30 % pour les envies et 20 % pour l'épargne ou le remboursement de crédits.</p>
<h2>La répartition</h2>
{table(["Poste", "Part", "Par mois"], [("Essentiel", "50 %", eur(needs)), ("Envies", "30 %", eur(wants)), ("Épargne", "20 %", eur(save))], ("Total", "100 %", eur(m)))}
<p>Soit {eur(m * 12)} par an, et une épargne possible de {eur(save * 12)} sur douze mois.</p>
<h2>Exemple : l'essentiel ({eur(needs)})</h2>
{table(["Dépense", "Par mois"], nr, ("Sous-total", eur(nt)))}
<p>Il reste environ {eur(needs - nt)} pour les assurances, la mutuelle, la garde d'enfants ou les mensualités de crédit.</p>
<h2>Exemple : les envies ({eur(wants)})</h2>
{table(["Dépense", "Par mois"], wr, ("Sous-total", eur(wt)))}
<h2>Exemple : l'épargne ({eur(save)})</h2>
{table(["Objectif", "Par mois"], sr, ("Sous-total", eur(st)))}
<div class="box"><strong>Conseil pour ce revenu :</strong> {tip}</div>
<p>Ces montants sont des repères, pas une règle. Testez avec vos vrais chiffres dans le <a href="../simulateurs/budget-50-30-20.html">simulateur 50/30/20 gratuit</a>, ou calculez <a href="../simulateurs/objectif-epargne.html">combien épargner chaque mois</a> pour un projet.</p>
{cta("Budget 2027 — tableur mensuel & annuel", "12 onglets mensuels, prévu vs réel, taux d'épargne calculé automatiquement. En français et en euros.", L["budget2027"], f"Voir le tableur — 6,99{NB}€", L["pack"])}"""
    return f"fr/budgets/budget-{m}-euros-par-mois.html", title, desc, body


WED = [("Lieu de réception", .22), ("Traiteur & boissons", .28), ("Photo & vidéo", .10), ("Fleurs & décoration", .08), ("Tenues & accessoires", .07),
       ("DJ / musique & animations", .06), ("Alliances", .05), ("Coiffure & maquillage", .03), ("Faire-part & papeterie", .02), ("Transport", .02),
       ("Cadeaux invités", .02), ("Réserve imprévus", .05)]


def wedding_page(t, L, today):
    rows = [(n, f"{int(p * 100)} %", eur(t * p)) for n, p in WED]
    guests = [(g, eur(t / g)) for g in (50, 80, 100, 150)]
    title = f"Budget mariage de {eur(t)} : comment le répartir poste par poste"
    desc = f"Un mariage à {eur(t)} réparti par poste : lieu, traiteur, photographe, tenues, décoration… et le budget par invité pour 50 à 150 invités."
    body = f"""<h1>{title}</h1><p class="meta">Mis à jour le {today.strftime('%d/%m/%Y')} · 4 min de lecture</p>
<p class="lede">Voici une façon de répartir un budget mariage de {eur(t)}, à partir d'une répartition en pourcentages couramment utilisée. Déplacez ensuite l'argent vers ce qui compte le plus pour vous.</p>
<h2>Répartition par poste</h2>
{table(["Poste", "Part", "Montant"], rows, ("Total", "100 %", eur(t)))}
<h2>Budget par invité</h2>
<p>Le nombre d'invités change presque tout, du traiteur à la taille de la salle.</p>
{table(["Invités", "Budget total par invité"], guests)}
<div class="box"><strong>Gardez la réserve.</strong> Les {eur(t * .05)} d'imprévus sont là parce qu'au moins un prestataire finit presque toujours au-dessus du premier devis.</div>
{cta("Budget Mariage — tableur complet", "Cette répartition déjà prête : prévu vs devis vs payé, échéancier des acomptes et liste des invités avec réponses et menus.", L["mariage"], f"Voir le tableur — 6,99{NB}€", L["pack"])}"""
    return f"fr/budgets/budget-mariage-{t}-euros.html", title, desc, body


XMAS = [("Cadeaux", .60), ("Repas de fêtes", .20), ("Déco, cartes & emballages", .10), ("Trajets & sorties", .10)]


def xmas_page(t, L, today):
    rows = [(n, f"{int(p * 100)} %", eur(t * p)) for n, p in XMAS]
    weeks = [(w, eur(t / w)) for w in (6, 8, 10, 12)]
    title = f"Budget de Noël de {eur(t)} : répartition et plan d'épargne"
    desc = f"Comment répartir un budget de Noël de {eur(t)} entre cadeaux, repas, déco et trajets, et combien mettre de côté chaque semaine pour le payer sans crédit."
    body = f"""<h1>{title}</h1><p class="meta">Mis à jour le {today.strftime('%d/%m/%Y')} · 3 min de lecture</p>
<p class="lede">Un budget de Noël de {eur(t)} va plus loin quand on le répartit avant d'acheter. Voici une répartition simple et un plan d'épargne pour tout payer sans découvert.</p>
<h2>Répartir les {eur(t)}</h2>
{table(["Poste", "Part", "Montant"], rows, ("Total", "100 %", eur(t)))}
<h2>Combien mettre de côté chaque semaine</h2>
{table(["Semaines avant les achats", "À épargner par semaine"], weeks)}
<p>Avec {eur(t * .6)} pour les cadeaux, fixez un montant par personne avant d'acheter quoi que ce soit, et notez chaque achat au fur et à mesure.</p>
{cta("Budget de Noël & des Fêtes", "Liste de cadeaux avec cases acheté / emballé, autres dépenses des fêtes et résumé de ce qu'il reste.", L["noel"], f"Voir le tableur — 4,99{NB}€", L["pack"])}"""
    return f"fr/budgets/budget-noel-{t}-euros.html", title, desc, body


def programmatic(L, today):
    s = [salary_page(m, L, today) for m in range(1400, 4001, 100)]
    w = [wedding_page(t, L, today) for t in range(5000, 40001, 5000)]
    x = [xmas_page(t, L, today) for t in (200, 300, 400, 500, 750, 1000)]
    order = []
    while s or w or x:
        for lst in (s, s, w, x):
            if lst:
                order.append(lst.pop(0))
    n = RELEASE_FIRST + RELEASE_PER_DAY * max(0, (today - RELEASE_START).days)
    return order[:n], len(order)


# ------------------------------------------------------------------ simulateurs
FMT = "function f(v){return Math.round(v).toLocaleString('fr-FR')+'\\u00a0€'}"


def sim_503020(L):
    body = f"""<h1>Simulateur budget 50/30/20</h1><p class="lede">Saisissez votre salaire net mensuel pour voir combien consacrer à l'essentiel, aux envies et à l'épargne, puis comparez avec vos dépenses actuelles.</p>
<div class="calc">
<div class="row"><label>Revenu net mensuel</label><input id="inc" type="number" value="2200"></div>
<h3>Vos dépenses actuelles (facultatif)</h3>
<div class="row"><label>Essentiel (loyer, factures, courses, transport)</label><input id="n" type="number" value="1250"></div>
<div class="row"><label>Envies (sorties, loisirs, shopping)</label><input id="w" type="number" value="600"></div>
<div class="row"><label>Épargne & remboursements anticipés</label><input id="s" type="number" value="350"></div>
<div class="result" id="res"></div></div>
<p>Voir des <a href="../budgets/index.html">exemples détaillés par niveau de salaire</a>.</p>
{cta("Budget 2027 — tableur mensuel & annuel", "Suivez chaque dépense, avec écarts en rouge et taux d'épargne automatique.", L["budget2027"], f"Voir le tableur — 6,99{NB}€", L["pack"])}
<script>{FMT}
function c(){{const i=+inc.value||0,t=[i*.5,i*.3,i*.2],a=[+n.value||0,+w.value||0,+s.value||0],l=['Essentiel (50 %)','Envies (30 %)','Épargne (20 %)'];
let h='';for(let k=0;k<3;k++){{const d=k<2?t[k]-a[k]:a[k]-t[k];h+=`<div class="stat"><div class="l">${{l[k]}}</div><div class="v">${{f(t[k])}}</div><div class="l ${{d<0?'neg':''}}">Vous : ${{f(a[k])}} (${{d<0?(k<2?'dépassement':'manque'):'ok'}} ${{f(Math.abs(d))}})</div></div>`}}
res.innerHTML=h}}document.querySelectorAll('input').forEach(e=>e.addEventListener('input',c));c();</script>"""
    return "fr/simulateurs/budget-50-30-20.html", "Simulateur budget 50/30/20 (gratuit)", "Simulateur gratuit de la règle 50/30/20 : combien consacrer à l'essentiel, aux envies et à l'épargne selon votre salaire net.", body


def sim_epargne(L):
    body = f"""<h1>Simulateur d'objectif d'épargne</h1><p class="lede">Combien mettre de côté chaque mois pour atteindre votre objectif : apport, voiture, mariage, voyage ou épargne de précaution ?</p>
<div class="calc">
<div class="row"><label>Objectif (€)</label><input id="g" type="number" value="10000"></div>
<div class="row"><label>Déjà épargné (€)</label><input id="h" type="number" value="1500"></div>
<div class="row"><label>Dans combien de mois ?</label><input id="m" type="number" value="24"></div>
<div class="row"><label>Taux annuel du placement (%)</label><input id="r" type="number" step="0.1" value="0"></div>
<div class="result" id="res"></div></div>
<div class="box">Le taux est facultatif : laissez 0 pour un calcul sans intérêts, ou saisissez le taux actuel de votre livret ou placement.</div>
{cta("Budget 2027 — tableur mensuel & annuel", "Planifiez votre épargne mois par mois et suivez votre taux d'épargne sur l'année.", L["budget2027"], f"Voir le tableur — 6,99{NB}€", L["pack"])}
<script>{FMT}
function c(){{const G=+g.value||0,H=+h.value||0,M=Math.max(1,+m.value||1),r=(+r_.value||0)/1200;const fv=H*Math.pow(1+r,M);const need=Math.max(0,G-fv);
const p=r?need*r/(Math.pow(1+r,M)-1):need/M;const paid=H+p*M;
res.innerHTML=`<div class="stat"><div class="l">À épargner par mois</div><div class="v">${{f(p)}}</div><div class="l">pendant ${{M}} mois</div></div><div class="stat"><div class="l">Vos versements</div><div class="v">${{f(paid)}}</div><div class="l">apport compris</div></div><div class="stat"><div class="l">Intérêts gagnés</div><div class="v">${{f(Math.max(0,G-paid))}}</div><div class="l">estimation</div></div>`}}
const r_=document.getElementById('r');document.querySelectorAll('input').forEach(e=>e.addEventListener('input',c));c();</script>"""
    return "fr/simulateurs/objectif-epargne.html", "Simulateur d'objectif d'épargne (gratuit)", "Calculez combien épargner chaque mois pour atteindre un objectif à une date donnée, avec ou sans intérêts.", body


def free_page(L):
    body = f"""<h1>Fiche budget mensuel gratuite à imprimer</h1>
<p class="lede">Un budget simple sur une page, à remplir à la main en 10 minutes environ, et un journal pour suivre vos dépenses du mois. PDF gratuit, format A4.</p>
<div class="cta"><div><strong>Télécharger la fiche gratuite</strong>Saisissez 0 au moment de payer sur Gumroad et le PDF est à vous. Sans abonnement.</div><a class="btn" href="{L["fiche"]}">La recevoir gratuitement</a></div>
<h2>Ce que contient la fiche</h2>
<ul><li>Revenus : chaque source du mois et le total</li><li>Factures : date, montant et case « payé » pour chacune</li><li>Dépenses courantes : dix postes avec prévu et réel</li><li>Épargne : objectif prévu et réellement épargné</li><li>Bilan du mois : revenus, factures, dépenses, épargne et reste</li><li>Page 2 : journal des dépenses</li></ul>
<h2>Comment l'utiliser</h2>
<p>En début de mois, notez vos revenus prévus, puis attribuez chaque euro : d'abord les factures, puis l'épargne, puis les dépenses courantes. Revenus moins tout le prévu doit être positif ou nul. Pendant le mois, cochez les factures payées et, une fois par semaine, notez vos dépenses réelles à côté du prévu. En fin de mois, remplissez le bilan et ajustez le mois suivant.</p>
<div class="box"><strong>Astuce :</strong> crayon pour le prévu, stylo pour le réel : vous voyez l'écart d'un coup d'œil.</div>
<p>Vous préférez l'écran ? Essayez le <a href="simulateurs/budget-50-30-20.html">simulateur 50/30/20</a> ou lisez <a href="articles/comment-faire-un-budget-mensuel.html">comment faire un budget mensuel</a>.</p>
{cta("Toute l'année sur papier ?", "Le Planner Budget 2027 à imprimer : 20 pages A4 avec 12 budgets mensuels et mini-calendriers, suivi des factures, suivi d'épargne en 100 cases et suivi des dettes.", L["planner_pdf"], f"Voir le planner — 4,99{NB}€")}"""
    return "fr/fiche-budget-gratuite.html", "Fiche budget mensuel gratuite à imprimer (PDF)", "Téléchargez une fiche budget mensuel gratuite à imprimer : revenus, factures à cocher, dépenses prévu vs réel, épargne et journal des dépenses. PDF A4.", body


def card(href, k, t, p):
    return f'<a class="card" href="{href}"><div class="k">{html.escape(k)}</div><h3>{html.escape(t)}</h3><p>{html.escape(p)}</p></a>'


def read_articles(src):
    d = os.path.join(src, "fr", "articles")
    arts = []
    for fn in sorted(os.listdir(d)) if os.path.isdir(d) else []:
        if fn.endswith(".html"):
            s = open(os.path.join(d, fn), encoding="utf-8").read()
            t = re.search(r"<title>(.*?)</title>", s, re.S)
            ds = re.search(r'<meta name="description" content="(.*?)"', s, re.S)
            sec = re.search(r'<meta name="section" content="(.*?)"', s)
            dp = re.search(r'"datePublished":\s*"([\d-]+)"', s)
            arts.append({"path": "articles/" + fn, "title": html.unescape(t.group(1)).split(" | ")[0].strip() if t else fn,
                         "desc": html.unescape(ds.group(1)) if ds else "", "sec": sec.group(1) if sec else "Guide", "date": dp.group(1) if dp else "2026-09-30"})
    arts.sort(key=lambda a: (a["date"], a["path"]))
    return arts


def build(out, src, today):
    """Write the French pages into `out`; return [(path, lastmod)] for the sitemap."""
    L = links()
    urls = []

    def write(path, content):
        full = os.path.join(out, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        open(full, "w", encoding="utf-8").write(content)
        urls.append((path, today.isoformat()))

    sims = []
    for fn in (sim_503020, sim_epargne):
        p, t, d, b = fn(L)
        write(p, page(t + " | ClarityPaperCo", d, b, 2, p, today, {"@context": "https://schema.org", "@type": "WebApplication", "name": t, "inLanguage": "fr", "applicationCategory": "FinanceApplication", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"}}, "website"))
        sims.append((p[3:], t.replace(" (gratuit)", ""), d.split(":")[0] if ":" in d else d))

    fp, ft, fd, fb = free_page(L)
    write(fp, page(ft + " | ClarityPaperCo", fd, fb, 1, fp, today))

    live, total = programmatic(L, today)
    groups = {"Budget selon votre salaire": [], "Budgets mariage": [], "Budgets de Noël": []}
    for p, t, d, b in live:
        sch = {"@context": "https://schema.org", "@type": "Article", "headline": t, "description": d, "inLanguage": "fr", "datePublished": today.isoformat(), "author": {"@type": "Organization", "name": "ClarityPaperCo"}}
        write(p, page(t + " | ClarityPaperCo", d, b, 2, p, today, sch))
        key = "Budgets mariage" if "mariage" in p else "Budgets de Noël" if "noel" in p else "Budget selon votre salaire"
        groups[key].append((p[11:], t))
    hub = '<h1>Exemples de budgets en euros</h1><p class="lede">Des exemples chiffrés : comment répartir un salaire net avec la règle 50/30/20, et comment organiser un mariage ou Noël avec un budget fixe.</p>'
    for g, items in groups.items():
        if items:
            hub += f"<h2>{g}</h2><ul>" + "".join(f'<li><a href="{p}">{html.escape(t)}</a></li>' for p, t in items) + "</ul>"
    write("fr/budgets/index.html", page("Exemples de budgets en euros | ClarityPaperCo", "Exemples de budgets 50/30/20 de 1 400 € à 4 000 € par mois, budgets mariage et budgets de Noël, avec des chiffres concrets.", hub, 2, "fr/budgets/index.html", today, og="website"))

    arts = read_articles(src)
    for a in arts:
        urls.append(("fr/" + a["path"], a["date"]))
    n_ex = sum(len(v) for v in groups.values())
    prods = [("Budget annuel", "Budget 2027 — mensuel & annuel", f"12 onglets mensuels, prévu vs réel, bilan annuel. 6,99{NB}€", L["budget2027"]),
             ("Fêtes", "Budget de Noël & des Fêtes", f"Liste de cadeaux, repas, déco et ce qu'il reste. 4,99{NB}€", L["noel"]),
             ("Mariage", "Budget Mariage", f"Répartition, devis, acomptes et liste des invités. 6,99{NB}€", L["mariage"]),
             ("Indépendants", "Suivi Factures — Auto-entrepreneur", f"Factures, retards, charges et montant à mettre de côté. 6,99{NB}€", L["autoentrepreneur"])]
    guides = "".join(card(a["path"], a["sec"], a["title"], a["desc"]) for a in arts)
    guides_html = f'<h2 id="guides">Guides</h2><div class="grid">{guides}</div>' if guides else '<span id="guides"></span>'
    body = f"""<h1>Gérer son budget simplement, en euros</h1>
<p class="lede">Des simulateurs gratuits, des exemples de budgets chiffrés et des tableurs prêts à l'emploi pour gérer votre salaire, préparer Noël ou organiser un mariage.</p>
<h2 id="simulateurs">Simulateurs gratuits</h2><div class="grid">{"".join(card(p, "Simulateur", t, d) for p, t, d in sims)}</div>
<h2 id="imprimer">À imprimer</h2><div class="grid">{card("fiche-budget-gratuite.html", "Gratuit", "Fiche budget mensuel gratuite", "Une page pour préparer votre mois à la main, et un journal des dépenses. PDF A4.")}{card(L["planner_pdf"], f"À imprimer — 4,99{NB}€", "Planner Budget 2027 (PDF)", "20 pages A4 : 12 budgets mensuels, suivi des factures, de l'épargne et des dettes.")}</div>
<h2 id="exemples">Exemples de budgets</h2><p><a href="budgets/index.html">Voir les {n_ex} exemples</a> — budget selon votre salaire (méthode 50/30/20), budgets mariage et budgets de Noël.</p>
{guides_html}
<h2 id="tableurs">Tableurs en français</h2><div class="grid">{"".join(card(u, k, t, p) for k, t, p, u in prods)}</div>
{cta("Les 4 tableurs en un seul pack", "Budget 2027, Noël, mariage et suivi auto-entrepreneur. Excel, Google Sheets et Numbers.", L["pack"], f"Le pack — 14,99{NB}€")}"""
    full = os.path.join(out, "fr", "index.html")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(page("Budget facile — simulateurs gratuits et exemples en euros | ClarityPaperCo", "Simulateurs de budget gratuits, exemples de budgets chiffrés en euros et tableurs Excel / Google Sheets en français.", body, 1, "fr/", today, og="website"))
    urls.append(("fr/", today.isoformat()))
    return urls, len(live), total
