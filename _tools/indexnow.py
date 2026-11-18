"""Notify Bing (which powers ChatGPT search and Copilot), Yandex, Seznam and Naver
of new/updated URLs through IndexNow. Run AFTER the site is deployed (the key file
must be reachable at https://gpscarro.com/<key>.txt).

Usage (from the repository root):
  python -I _tools/indexnow.py            # submit every URL in sitemap.xml
  python -I _tools/indexnow.py URL [URL]  # submit specific URLs
"""
import json
import os
import re
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOST = "gpscarro.com"
KEY = "806e517e35fe49a89f459d199b2ba7dd"


def main():
    urls = sys.argv[1:]
    if not urls:
        sm = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
        urls = re.findall(r"<loc>([^<]+)</loc>", sm)
    body = json.dumps({"host": HOST, "key": KEY, "keyLocation": f"https://{HOST}/{KEY}.txt", "urlList": urls[:10000]}).encode()
    req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body, method="POST",
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print("IndexNow:", r.status, f"({len(urls)} URLs)")
    except urllib.error.HTTPError as e:
        print("IndexNow error:", e.code, e.read()[:300])


if __name__ == "__main__":
    main()
