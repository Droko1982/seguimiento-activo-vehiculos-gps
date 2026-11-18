"""Validate every _tools/data/*.json file against CONTENT-BRIEF.md rules.

Run from the repository root:  python -I _tools/validate_data.py
Exit code 1 when an error is found.
"""
import glob
import json
import os
import re
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "_tools", "data")
KEPT = {"armenia", "bogota", "cucuta", "ibague", "monteria", "neiva", "pasto", "popayan", "santa-marta", "valledupar", "villavicencio"}
DEPTS = set("""amazonas antioquia arauca atlantico bolivar boyaca caldas caqueta casanare cauca cesar choco cordoba cundinamarca
guainia guaviare huila la-guajira magdalena meta narino norte-de-santander putumayo quindio risaralda san-andres-y-providencia
santander sucre tolima valle-del-cauca vaupes vichada""".split())

errors, warns = [], []
places, depts = [], []
for f in sorted(glob.glob(os.path.join(DATA, "*.json"))):
    data = json.load(open(f, encoding="utf-8"))
    (depts if os.path.basename(f).startswith("departamentos") else places).extend(data)

MASTER = set("""arauca armenia barranquilla bogota bucaramanga cali cartagena cucuta florencia ibague leticia manizales medellin mitu
mocoa monteria neiva pasto pereira popayan puerto-carreno puerto-inirida quibdo riohacha san-andres san-jose-del-guaviare santa-marta
sincelejo tunja valledupar villavicencio yopal soacha chia zipaquira facatativa fusagasuga girardot mosquera madrid funza cajica bello
itagui envigado rionegro sabaneta apartado turbo caucasia palmira buenaventura tulua cartago buga jamundi yumbo soledad malambo
sabanalarga floridablanca giron piedecuesta barrancabermeja san-gil villa-del-rosario los-patios ocana pamplona magangue turbaco
el-carmen-de-bolivar duitama sogamoso chiquinquira puerto-boyaca dosquebradas santa-rosa-de-cabal calarca la-dorada chinchina espinal
melgar pitalito garzon acacias granada-meta puerto-lopez aguazul aguachica cienaga maicao lorica cerete sahagun corozal ipiales tumaco
santander-de-quilichao puerto-asis saravena tame san-vicente-del-caguan""".split())
slugs = MASTER
seen = defaultdict(list)


def strings(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for v in o.values():
            yield from strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from strings(v)


def check_text(owner, obj):
    for s in strings(obj):
        if '"' in s or "“" in s or "”" in s:
            errors.append(f"{owner}: double quote in text")
        for price in re.findall(r"\$\s?[\d.]+", s):
            if price.replace(" ", "").rstrip(".") not in ("$120.000", "$47.600"):
                errors.append(f"{owner}: unexpected price {price}")
        if re.search(r"\b3\d{2}\s?\d{3}\s?\d{4}\b", s):
            errors.append(f"{owner}: phone number in text")
        for sent in re.split(r"(?<=[.!?])\s+", s):
            words = sent.split()
            if len(words) >= 9:
                seen[" ".join(words).lower()].append(owner)


for p in places:
    o = p.get("slug", "?")
    for k in ("slug", "name", "dept", "lat", "lon", "lead", "intro", "uses", "zones", "roads", "install_note", "faqs", "nearby"):
        if k not in p:
            errors.append(f"{o}: missing {k}")
    if p.get("dept") not in DEPTS:
        errors.append(f"{o}: bad dept {p.get('dept')}")
    if len(p.get("lead", "")) > 170:
        errors.append(f"{o}: lead too long")
    if len(p.get("intro", [])) != 2: errors.append(f"{o}: intro != 2")
    if len(p.get("uses", [])) != 4: errors.append(f"{o}: uses != 4")
    if len(p.get("faqs", [])) != 3: errors.append(f"{o}: faqs != 3")
    if not 3 <= len(p.get("roads", [])) <= 4: errors.append(f"{o}: roads count")
    if not 8 <= len(p.get("zones", [])) <= 14: errors.append(f"{o}: zones count")
    nb = p.get("nearby", [])
    if not 3 <= len(nb) <= 5: warns.append(f"{o}: nearby count {len(nb)}")
    for s in nb:
        if s not in slugs or s == o:
            errors.append(f"{o}: bad nearby {s}")
    if not (-5 < p.get("lat", 99) < 14 and -82 < p.get("lon", 0) < -66):
        errors.append(f"{o}: coordinates out of Colombia")
    check_text(o, p)

for d in depts:
    o = "dept:" + d.get("slug", "?")
    for k in ("slug", "name", "capital", "iso", "lat", "lon", "lead", "intro", "subregions", "roads", "uses", "faqs"):
        if k not in d:
            errors.append(f"{o}: missing {k}")
    if d.get("slug") not in DEPTS: errors.append(f"{o}: unknown slug")
    if d.get("capital") not in slugs: errors.append(f"{o}: capital {d.get('capital')} not a page")
    if len(d.get("intro", [])) != 3: errors.append(f"{o}: intro != 3")
    if len(d.get("uses", [])) != 4: errors.append(f"{o}: uses != 4")
    if len(d.get("faqs", [])) != 3: errors.append(f"{o}: faqs != 3")
    if not 3 <= len(d.get("subregions", [])) <= 6: errors.append(f"{o}: subregions count")
    check_text(o, d)

dups = {s: o for s, o in seen.items() if len(set(o)) > 1}
for s, o in list(dups.items())[:30]:
    warns.append(f"repeated sentence in {sorted(set(o))}: {s[:90]}")
cnt = defaultdict(int)
for p in places:
    cnt[p["slug"]] += 1
for s, c in cnt.items():
    if c > 1:
        errors.append(f"duplicate place slug {s}")

print(f"places={len(places)} departments={len(depts)} errors={len(errors)} warnings={len(warns)}")
for e in errors:
    print("ERROR", e)
for w in warns:
    print("WARN ", w)
sys.exit(1 if errors else 0)
