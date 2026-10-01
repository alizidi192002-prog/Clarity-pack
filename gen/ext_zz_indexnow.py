"""IndexNow: after the daily scheduled build, tell Bing, Yandex, Seznam and Naver which URLs exist.

Runs only in GitHub Actions on the daily schedule (GITHUB_EVENT_NAME == "schedule"), so pushes
and local builds never ping. The key file is docs/ae461bb794648037d95aeee25d2e8889.txt (served at the site root).
"""
import atexit, json, os, re, urllib.request

KEY = "ae461bb794648037d95aeee25d2e8889"
HOST = "alizidi192002-prog.github.io"
BASE = "https://alizidi192002-prog.github.io/Clarity-pack"
SITEMAP = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "_site", "sitemap.xml")


def _ping():
    try:
        urls = re.findall(r"<loc>(.*?)</loc>", open(SITEMAP, encoding="utf-8").read())[:10000]
        data = json.dumps({"host": HOST, "key": KEY, "keyLocation": f"{BASE}/{KEY}.txt", "urlList": urls}).encode()
        req = urllib.request.Request("https://api.indexnow.org/indexnow", data=data, headers={"Content-Type": "application/json; charset=utf-8"})
        with urllib.request.urlopen(req, timeout=30) as r:
            print("IndexNow:", r.status, len(urls), "urls")
    except Exception as e:  # never fail the build because of a ping
        print("IndexNow skipped:", repr(e))


def build(B):
    if os.environ.get("GITHUB_ACTIONS") == "true" and os.environ.get("GITHUB_EVENT_NAME") == "schedule":
        atexit.register(_ping)
    return ""
