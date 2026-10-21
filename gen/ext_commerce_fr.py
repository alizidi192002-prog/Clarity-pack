"""French "outils pour petits commerces" products (Clarity Digital) — landing pages + Pinterest feed.

- Writes one French landing page per product at outils/<slug>.html (on the claimed site, so
  Pinterest accepts the link) with a button to the Gumroad page.
- Writes _site/pins-commerce-fr.xml: ONE new pin per day from FEED_START (Africa/Algiers date),
  rotating carte -> grille -> guide, alternating the a/b image and rotating titles. Each item has
  a unique link/guid (?pin=YYYY-MM-DD-c). Connect this feed once in Pinterest
  (Paramètres > Création groupée d'épingles > Publication automatique > flux RSS) to its own board.
- Kept separate from the English product feeds on purpose: nothing here touches ext_products.py.
"""
import datetime, html, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "_site")
BASE = "https://alizidi192002-prog.github.io/Clarity-pack"
IMG = "https://raw.githubusercontent.com/alizidi192002-prog/Clarity-pack/main/pack/pins/commerce/"
G = "https://claritydigital8.gumroad.com/l/"
FEED = "pins-commerce-fr.xml"
FEED_START = datetime.date(2026, 10, 21)
KEEP_DAYS = 60

P = {
 "carte": dict(slug="modele-carte-restaurant", name="Modèle de carte de restaurant", price="7", link=G + "carte-restaurant",
   images=["pin_carte_a.jpg", "pin_carte_b.jpg"],
   blurb="Une carte claire et élégante pour votre restaurant, bistrot ou café, à modifier en 10 minutes dans votre navigateur, sans Canva ni logiciel.",
   features=["Modèle A4 qui s'ouvre dans Chrome, Edge, Firefox ou Safari", "4 thèmes : Crème, Ardoise, Olive, Bleu", "Entrées, plats, desserts et encadré « Formule midi »", "Export PDF prêt à imprimer + mode d'emploi en français"],
   titles=[
    ("Modèle de carte de restaurant à personnaliser – PDF A4 à imprimer", "Une carte claire pour votre restaurant ou bistrot, modifiable en 10 minutes dans le navigateur. 4 thèmes, export PDF, sans Canva."),
    ("Carte de restaurant en 10 minutes, sans Canva", "Cliquez sur un texte, tapez le vôtre, enregistrez en PDF. Modèle de menu A4 pour restaurants, bistrots et cafés."),
    ("Template menu restaurant français – entrées, plats, desserts", "Modèle de carte A4 avec rubriques entrées, plats, desserts et formule midi. 4 thèmes de couleurs, PDF prêt à imprimer."),
    ("Idée de carte pour bistrot : un menu simple et élégant", "Un modèle de carte de bistrot à personnaliser dans le navigateur, à imprimer ou à partager en PDF sur Instagram et Google."),
   ]),
 "grille": dict(slug="grille-tarifaire-salon-institut", name="Grille tarifaire salon & institut", price="5", link=G + "grille-tarifaire",
   images=["pin_grille_a.jpg", "pin_grille_b.jpg"],
   blurb="Affichez vos prestations et vos prix proprement, en salle ou en ligne : une grille tarifaire A4 à modifier dans votre navigateur.",
   features=["Grille A4 modifiable dans le navigateur", "4 thèmes : Rose, Noir & or, Sauge, Lavande", "Prestations avec durée et prix, encadré carte fidélité", "Export PDF prêt à imprimer + mode d'emploi en français"],
   titles=[
    ("Grille tarifaire salon de coiffure – modèle à personnaliser", "Prestations, durées et prix sur une grille A4 élégante. Modifiable dans le navigateur, 4 thèmes, export PDF."),
    ("Modèle de tarifs pour institut de beauté et onglerie", "Une liste de prix claire pour votre institut, onglerie ou barbier. À personnaliser en 10 minutes, PDF prêt à imprimer."),
    ("Affiche tarifs coiffure : un modèle simple et chic", "Affichez vos tarifs en salle ou partagez-les en ligne. Grille tarifaire A4, 4 thèmes, sans logiciel de graphisme."),
    ("Liste de prix esthéticienne – template PDF à imprimer", "Soins, épilation, ongles : une grille de prix claire avec durée et tarif. Modèle à personnaliser, export PDF."),
   ]),
 "mariage": dict(slug="pack-mariage-a-personnaliser", name="Pack Mariage à personnaliser", price="12", link=G + "pack-mariage",
   images=["pin_mariage_a.jpg", "pin_mariage_b.jpg"],
   blurb="Panneau de bienvenue, menu et plan de table assortis, à personnaliser en 20 minutes dans votre navigateur, sans Canva.",
   features=["Panneau de bienvenue, menu et plan de table", "4 thèmes : Ivoire & or, Sauge, Terracotta, Bleu nuit", "Tables et invités ajoutés en un clic", "Export PDF A4, à agrandir chez un imprimeur + mode d'emploi en français"],
   titles=[
    ("Plan de table mariage à personnaliser – modèle PDF élégant", "Un plan de table assorti au menu et au panneau de bienvenue. Modifiable dans le navigateur, 4 thèmes, PDF prêt à imprimer."),
    ("Panneau de bienvenue mariage : modèle à imprimer", "Prénoms, date et petit mot : votre panneau de bienvenue en 10 minutes, sans Canva. Pack mariage avec menu et plan de table."),
    ("Menu de mariage à personnaliser – idée déco de table", "Cocktail, entrée, plat, dessert : un menu de mariage élégant à modifier dans le navigateur et à imprimer en PDF."),
    ("Papeterie de mariage DIY : bienvenue, menu, plan de table", "Trois modèles assortis pour votre mariage, 4 thèmes de couleurs. Personnalisez, enregistrez en PDF, imprimez."),
   ]),
 "cv": dict(slug="modeles-cv-francais", name="3 modèles de CV en français", price="7", link=G + "modeles-cv",
   images=["pin_cv_a.jpg", "pin_cv_b.jpg"],
   blurb="Trois styles de CV dans un seul fichier : Moderne, Classique et Minimal. Remplissez une fois, changez de style en un clic, exportez en PDF.",
   features=["3 styles : Moderne, Classique, Minimal", "4 couleurs, photo en option", "Profil, expériences, formation, compétences, langues", "Export PDF A4 + mode d'emploi en français"],
   titles=[
    ("Modèle de CV moderne en français – à remplir et exporter en PDF", "Un CV propre en 15 minutes, sans Word ni Canva. 3 styles, 4 couleurs, photo en option."),
    ("CV simple et efficace : 3 modèles dans un seul fichier", "Moderne, Classique, Minimal : remplissez votre CV une fois et changez de style en un clic. Export PDF A4."),
    ("Exemple de CV pour assistante commerciale – modèle PDF", "Un exemple de CV clair avec profil, expériences et compétences. Modèle à personnaliser dans le navigateur."),
    ("Modèle de CV sans photo ou avec photo – format A4", "Choisissez avec ou sans photo, 4 couleurs, 3 mises en page. Vos données restent sur votre ordinateur."),
   ]),
 "guide": dict(slug="guide-fiche-google-30-minutes", name="Guide : optimiser sa fiche Google en 30 minutes", price="9", link=G + "fiche-google-30-minutes",
   images=["pin_guide_a.jpg", "pin_guide_b.jpg"],
   blurb="Six étapes de 5 minutes pour une fiche Google claire et complète : catégories, horaires, description, photos et avis. Pour les petits commerces.",
   features=["Trouver et revendiquer votre fiche", "Nom, catégories, coordonnées, horaires et attributs", "Description avec exemples, photos, avis et modèles de réponses", "Routine de 10 minutes par mois + checklist à imprimer (PDF, 10 pages)"],
   titles=[
    ("Optimiser sa fiche Google en 30 minutes – guide pour commerces", "6 étapes de 5 minutes : catégories, horaires, photos, avis. Guide PDF de 10 pages pour restaurants, salons et artisans."),
    ("Vos clients vous trouvent-ils sur Google Maps ?", "Complétez votre fiche Google étape par étape et soyez visible quand on cherche votre commerce. Guide PDF + checklist."),
    ("Fiche Google : comment répondre aux avis (modèles inclus)", "Demander des avis, répondre aux bons comme aux mauvais : modèles de réponses et routine mensuelle. Guide PDF pour petits commerces."),
    ("Référencement local : la checklist Google pour petits commerces", "Une checklist simple pour une fiche Google complète : nom, catégorie, horaires, photos, avis. Guide de 10 pages."),
   ]),
}
ORDER = ["carte", "grille", "guide"]
# From LAUNCH2 (set the day the 2 new Gumroad products go live) the daily pin rotates over 5 products.
# Days before LAUNCH2 keep the old 3-product rotation, so already-published pins never change.
LAUNCH2 = datetime.date(2026, 10, 22)  # Pack Mariage + CV live on Gumroad 21/10
ORDER2 = ["mariage", "carte", "cv", "grille", "guide"]


def algiers_today():
    if os.environ.get("FAKE_TODAY"):
        return datetime.date.fromisoformat(os.environ["FAKE_TODAY"])
    return (datetime.datetime.utcnow() + datetime.timedelta(hours=1)).date()


def page(p):
    feats = "".join(f"<li>{html.escape(f)}</li>" for f in p["features"])
    img = IMG + p["images"][0]
    return f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(p['name'])} | Clarity Digital</title><meta name="description" content="{html.escape(p['blurb'])}">
<meta property="og:title" content="{html.escape(p['name'])}"><meta property="og:description" content="{html.escape(p['blurb'])}"><meta property="og:image" content="{img}"><meta property="og:type" content="product">
<link rel="canonical" href="{BASE}/outils/{p['slug']}.html">
<style>body{{margin:0;font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;background:#f4efe6;color:#13233f;line-height:1.6}}main{{max-width:640px;margin:0 auto;padding:32px 16px 56px}}
.k{{font-size:13px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#e5603f}}h1{{font-family:Georgia,serif;font-size:32px;line-height:1.15;margin:8px 0 12px}}
p.l{{color:#4b5470;font-size:17px}}img{{width:100%;max-width:420px;display:block;margin:20px auto;border-radius:12px;box-shadow:0 18px 40px -20px rgba(0,0,0,.4)}}
li{{margin:6px 0}}.btn{{display:block;text-align:center;background:#e5603f;color:#fff;text-decoration:none;font-weight:800;padding:16px;border-radius:14px;font-size:18px;margin:24px 0 8px}}
.n{{text-align:center;color:#6b7280;font-size:14px}}a.o{{color:#13233f}}</style></head><body><main>
<div class="k">Outils pour petits commerces</div><h1>{html.escape(p['name'])}</h1><p class="l">{html.escape(p['blurb'])}</p>
<img src="{img}" alt="{html.escape(p['name'])}"><h2>Ce que vous recevez</h2><ul>{feats}</ul>
<a class="btn" href="{p['link']}">Télécharger — {p['price']} €</a><p class="n">Paiement sécurisé sur Gumroad · téléchargement immédiat</p>
<p class="n">Besoin d'un site pour votre commerce ? <a class="o" href="https://alizidi192002-prog.github.io/Demo/lien/">Clarity Digital — maquette gratuite</a></p>
</main></body></html>"""


def item(d, k, n):
    p = P[k]
    img = IMG + p["images"][(n // 1) % 2]
    t, desc = p["titles"][n % len(p["titles"])]
    url = f"{BASE}/outils/{p['slug']}.html?pin={d.isoformat()}-c"
    pub = datetime.datetime(d.year, d.month, d.day, 9, 0).strftime("%a, %d %b %Y %H:%M:%S +0000")
    desc = f"{desc} {p['name']} — {p['price']} €, téléchargement immédiat."
    return (f"<item><title>{html.escape(t[:100])}</title><link>{html.escape(url)}</link>"
            f"<description>{html.escape(desc[:480])}</description><guid isPermaLink=\"true\">{html.escape(url)}</guid>"
            f"<pubDate>{pub}</pubDate><enclosure url=\"{img}\" type=\"image/jpeg\" length=\"0\"/>"
            f"<media:content url=\"{img}\" medium=\"image\" type=\"image/jpeg\"/></item>")


def write_feed(today):
    horizon = today + datetime.timedelta(days=1)
    oldest = today - datetime.timedelta(days=KEEP_DAYS)
    items, d, i, j = [], FEED_START, 0, 0
    while d <= horizon:
        if LAUNCH2 and d >= LAUNCH2:
            k, n = ORDER2[j % len(ORDER2)], j // len(ORDER2); j += 1
        else:
            k, n = ORDER[i % len(ORDER)], i // len(ORDER); i += 1
        if d >= oldest:
            items.insert(0, item(d, k, n))
        d += datetime.timedelta(days=1)
    feed = ('<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/"><channel>'
            f"<title>Clarity Digital — Outils pour petits commerces</title><link>{BASE}/outils/index.html</link>"
            "<description>Modèles et guides pour restaurants, salons et petits commerces.</description>"
            + "".join(items) + "</channel></rss>\n")
    open(os.path.join(OUT, FEED), "w", encoding="utf-8").write(feed)
    print(FEED, len(items), "items")


def build(B):
    cards = ""
    for k in (ORDER2 if LAUNCH2 else ORDER):
        p = P[k]
        B.write(f"outils/{p['slug']}.html", page(p))
        cards += f'<li><a href="{p["slug"]}.html">{html.escape(p["name"])}</a> — {p["price"]} €</li>'
    B.write("outils/index.html", f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Outils pour petits commerces | Clarity Digital</title></head><body style="font-family:system-ui;max-width:640px;margin:40px auto;padding:0 16px"><h1>Outils pour petits commerces</h1><ul>{cards}</ul></body></html>')
    try:
        write_feed(algiers_today())
    except Exception as e:  # never break the site build
        print("commerce feed skipped:", repr(e))
    return ""
