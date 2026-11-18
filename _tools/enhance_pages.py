"""Apply the site-wide nav, footer, sticky mobile CTA and shared CSS to every page.

Idempotent: blocks are wrapped in <!-- SA:... --> markers and replaced on re-runs.
Run from the repository root:  python -I _tools/enhance_pages.py
"""
import glob
import html as htmlmod
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from site_common import SA_CSS, esc, footer_html, nav_html, sticky_html, tel, wa  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CURRENT = {"servicios": "servicios", "ciudades": "ciudades", "departamentos": "ciudades",
           "industrias": "industrias", "blog": "blog"}
ROOT_CURRENT = {"precios.html": "precios", "preguntas-frecuentes.html": "faq"}

NAV_RE = re.compile(r'(<!-- SA:NAV -->)?<nav class="sa-nav".*?</nav>(<!-- /SA:NAV -->)?', re.S)
FOOT_RE = re.compile(r'(<!-- SA:FOOTER -->)?<footer class="sa-footer".*?</footer>(<!-- /SA:FOOTER -->)?', re.S)
STICKY_RE = re.compile(r'<!-- SA:STICKY -->.*?<!-- /SA:STICKY -->', re.S)
CSS_RE = re.compile(r'/\* SA:CSS \*/.*?/\* /SA:CSS \*/', re.S)


def h1_text(s):
    m = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
    if not m:
        return ""
    t = re.sub(r"<[^>]+>", "", m.group(1))
    return " ".join(htmlmod.unescape(t).split())


def ensure_css(s):
    block = "/* SA:CSS */\n" + SA_CSS + "\n/* /SA:CSS */"
    if CSS_RE.search(s):
        return CSS_RE.sub(lambda m: block, s, count=1)
    head_end = s.find("</head>")
    idx = s.rfind("</style>", 0, head_end)
    if idx == -1:
        return s.replace("</head>", "<style>\n" + block + "\n</style>\n</head>", 1)
    return s[:idx] + block + "\n" + s[idx:]


def ensure_sticky(s, block):
    if STICKY_RE.search(s):
        return STICKY_RE.sub(lambda m: block, s, count=1)
    idx = s.rfind("</body>")
    return s[:idx] + block + "\n" + s[idx:]


def en_sticky():
    text = "Hello, I found gpscarro.com and I would like a quote for GPS tracking"
    return ('<!-- SA:STICKY --><div class="sa-sticky" aria-label="Quick contact">'
            f'<a class="sa-st-wa" href="{esc(wa(text))}" target="_blank" rel="noopener">💬 WhatsApp</a>'
            f'<a class="sa-st-tel" href="{tel()}">📞 Call</a></div><!-- /SA:STICKY -->')


def main():
    changed = 0
    files = sorted(glob.glob(os.path.join(ROOT, "*.html")) + glob.glob(os.path.join(ROOT, "*", "*.html")))
    for path in files:
        rel = os.path.relpath(path, ROOT).replace("\\", "/")
        if rel.startswith(("_tools/", "google")) or os.path.basename(rel).startswith("google"):
            continue
        s = open(path, encoding="utf-8").read()
        if "SA:GENERATED" in s:
            continue
        orig = s
        parts = rel.split("/")
        if rel == "404.html":
            prefix, current = "/", None
        elif len(parts) == 1:
            prefix, current = "", ROOT_CURRENT.get(rel)
        else:
            prefix, current = "../", CURRENT.get(parts[0])
        title = h1_text(s)
        wa_text = (f"Hola, vi la página '{title}' en gpscarro.com y quiero cotizar un GPS"
                   if title else "Hola, vi gpscarro.com y quiero cotizar un GPS para mi vehículo")
        s = ensure_css(s)
        if rel.startswith("en/"):
            s = ensure_sticky(s, en_sticky())
        else:
            if rel != "index.html":
                s = NAV_RE.sub(lambda m: nav_html(prefix, current), s, count=1)
                s = FOOT_RE.sub(lambda m: footer_html(prefix), s, count=1)
            s = ensure_sticky(s, sticky_html(wa_text))
        if s != orig:
            open(path, "w", encoding="utf-8", newline="").write(s)
            changed += 1
    print("pages updated:", changed)


if __name__ == "__main__":
    main()
