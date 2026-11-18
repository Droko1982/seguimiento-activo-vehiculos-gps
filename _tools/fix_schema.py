"""One-off: consolidate the business entity in JSON-LD on hand-written pages.

- City pages: per-city "LocalBusiness" nodes (no real address) become a Service whose
  provider is the single organization https://gpscarro.com/#organization.
- Nested LocalBusiness/Organization providers become a reference to that organization.
Run from the repository root:  python -I _tools/fix_schema.py
"""
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from site_common import BRAND, ORG_ID, PRICE_INSTALL, PRICE_MONTH  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOCK = re.compile(r'(<script type="application/ld\+json">)(.*?)(</script>)', re.S)
ORG_REF = {"@type": "Organization", "@id": ORG_ID, "name": BRAND, "url": "https://gpscarro.com/", "telephone": "+573160592569"}


def offers():
    return [{"@type": "Offer", "name": "Instalación GPS", "price": str(PRICE_INSTALL), "priceCurrency": "COP"},
            {"@type": "Offer", "name": "Mensualidad GPS", "price": str(PRICE_MONTH), "priceCurrency": "COP"}]


def is_type(node, t):
    v = node.get("@type")
    return v == t or (isinstance(v, list) and t in v)


def fix_nested(node):
    if isinstance(node, dict):
        for k, v in list(node.items()):
            if k in ("provider", "seller", "brand_owner") and isinstance(v, dict) and (
                    is_type(v, "LocalBusiness") or is_type(v, "Organization")):
                node[k] = dict(ORG_REF)
            else:
                fix_nested(v)
    elif isinstance(node, list):
        for x in node:
            fix_nested(x)


def city_service(lb, url):
    addr = lb.get("address", {}) if isinstance(lb.get("address"), dict) else {}
    city = addr.get("addressLocality") or lb.get("name", "").split(" - ")[-1]
    region = addr.get("addressRegion")
    area = {"@type": "City", "name": city}
    if region and region != city:
        area["containedInPlace"] = {"@type": "AdministrativeArea", "name": region}
    if isinstance(lb.get("geo"), dict):
        area["geo"] = lb["geo"]
    svc = {"@context": "https://schema.org", "@type": "Service", "name": f"Rastreo GPS vehicular en {city}",
           "serviceType": "Rastreo y monitoreo GPS vehicular", "url": lb.get("url", url), "provider": dict(ORG_REF),
           "areaServed": area, "offers": offers()}
    if lb.get("description"):
        svc["description"] = lb["description"]
    return svc


def main():
    ratings = []
    changed = 0
    for path in sorted(glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True)):
        rel = os.path.relpath(path, ROOT).replace("\\", "/")
        if rel.startswith("_tools/") or rel == "index.html":
            continue
        s = open(path, encoding="utf-8").read()
        if "SA:GENERATED" in s:
            continue
        canon = re.search(r'<link rel="canonical" href="([^"]+)"', s)
        url = canon.group(1) if canon else ""

        def repl(m):
            raw = m.group(2)
            try:
                data = json.loads(raw)
            except Exception:
                return m.group(0)
            new = data
            if isinstance(data, dict) and is_type(data, "LocalBusiness"):
                if rel.startswith("ciudades/"):
                    new = city_service(data, url)
                else:  # en/index.html: the English home describes the same single entity
                    data["@id"] = ORG_ID
                    data["name"] = BRAND
                    new = data
            fix_nested(new)
            if "aggregateRating" in json.dumps(new):
                ratings.append(rel)
            if new == data and json.dumps(new) == json.dumps(json.loads(raw)):
                return m.group(0)
            indent = "\n" if "\n" in raw else ""
            txt = json.dumps(new, ensure_ascii=False, indent=2 if indent else None,
                             separators=None if indent else (",", ":"))
            return m.group(1) + indent + txt + indent + m.group(3)

        t = BLOCK.sub(repl, s)
        if t != s:
            open(path, "w", encoding="utf-8", newline="").write(t)
            changed += 1
    print("pages updated:", changed)
    print("pages with aggregateRating:", sorted(set(ratings)))


if __name__ == "__main__":
    main()
