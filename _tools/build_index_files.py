"""Build sitemap.xml, llms.txt and llms-full.txt from the pages on disk.

- sitemap.xml: every public page; <lastmod> = today for pages changed in the working
  tree (git), otherwise the previous value.
- llms.txt / llms-full.txt: plain-text summaries for AI assistants (llmstxt.org format).
Run from the repository root:  python -I _tools/build_index_files.py
"""
import glob
import html
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_pillars import FAQ_GROUPS  # noqa: E402
from site_common import (  # noqa: E402
    BASE, BRAND, FIRST_YEAR_TXT, PHONE_INTL, PRICE_INSTALL_TXT, PRICE_MONTH_TXT, TODAY, YEAR_AFTER_TXT,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "_tools", "data")
SKIP = {"404.html", "gracias.html"}


def pages():
    out = []
    for p in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True):
        rel = os.path.relpath(p, ROOT).replace("\\", "/")
        if rel.startswith("_") or rel in SKIP or os.path.basename(rel).startswith("google"):
            continue
        out.append(rel)
    return sorted(out)


def url_of(rel):
    return BASE + (rel[:-len("index.html")] if rel.endswith("index.html") else rel)


def meta(rel):
    s = open(os.path.join(ROOT, rel), encoding="utf-8").read()
    t = re.search(r"<title>(.*?)</title>", s, re.S)
    d = re.search(r'<meta name="description" content="([^"]*)"', s)
    return (html.unescape(t.group(1).strip()) if t else rel, html.unescape(d.group(1)) if d else "")


def changed_files():
    try:
        out = subprocess.run(["git", "status", "--porcelain", "-uall"], cwd=ROOT, capture_output=True, text=True).stdout
    except Exception:
        return set()
    res = set()
    for line in out.splitlines():
        path = line[3:].strip().strip('"')
        if " -> " in path:
            path = path.split(" -> ")[1]
        res.add(path)
    return res


def classify(rel):
    if rel == "index.html":
        return "1.0", "weekly"
    if rel in ("precios.html", "preguntas-frecuentes.html", "en/index.html"):
        return "0.9", "monthly"
    if rel.startswith("servicios/") or rel == "ciudades/index.html" or rel == "departamentos/index.html":
        return "0.9", "monthly"
    if rel.startswith(("departamentos/", "industrias/")):
        return "0.8", "monthly"
    if rel.startswith("ciudades/"):
        return "0.8", "monthly"
    if rel.startswith("blog/"):
        return "0.7", "monthly"
    if rel == "sobre-nosotros.html":
        return "0.6", "yearly"
    return "0.3", "yearly"


def build_sitemap(all_pages):
    old = {}
    sm_path = os.path.join(ROOT, "sitemap.xml")
    if os.path.exists(sm_path):
        sm = open(sm_path, encoding="utf-8").read()
        for loc, lm in re.findall(r"<loc>([^<]+)</loc>.*?<lastmod>([^<]+)</lastmod>", sm, re.S):
            old[loc] = lm
    changed = changed_files()
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for rel in all_pages:
        u = url_of(rel)
        lm = TODAY if (rel in changed or u not in old) else old[u]
        pr, cf = classify(rel)
        lines.append("  <url>")
        lines.append(f"    <loc>{u}</loc>")
        if rel in ("index.html", "en/index.html"):
            lines.append(f'    <xhtml:link rel="alternate" hreflang="es" href="{BASE}"/>')
            lines.append(f'    <xhtml:link rel="alternate" hreflang="en" href="{BASE}en/"/>')
            lines.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE}"/>')
        lines.append(f"    <lastmod>{lm}</lastmod>")
        lines.append(f"    <changefreq>{cf}</changefreq>")
        lines.append(f"    <priority>{pr}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    open(sm_path, "w", encoding="utf-8", newline="\n").write("\n".join(lines) + "\n")
    return len(all_pages)


def load(pattern):
    out = []
    for f in sorted(glob.glob(os.path.join(DATA, pattern))):
        out.extend(json.load(open(f, encoding="utf-8")))
    return out


FACTS = f"""- Nombre: {BRAND} (sitio web: gpscarro.com)
- Qué es: servicio colombiano de rastreo y monitoreo GPS vehicular en tiempo real.
- Vehículos: carros, camionetas, motos, camiones, tractomulas, flotas, taxis, motos de domicilio, rent a car, maquinaria amarilla y agrícola.
- Precio: instalación {PRICE_INSTALL_TXT} COP (pago único) + mensualidad {PRICE_MONTH_TXT} COP. Primer año {FIRST_YEAR_TXT} COP; desde el segundo año {YEAR_AFTER_TXT} COP al año. Mismo precio en todo el país.
- El dispositivo GPS se entrega en préstamo (comodato). Sin cláusula de permanencia: al cancelar se devuelve el equipo sin costo.
- La mensualidad incluye: ubicación cada 30 segundos, rastreo 24/7, historial de 12 meses, geocercas, alertas ilimitadas (velocidad, encendido, zonas), apagado remoto del motor (con el vehículo detenido o a baja velocidad), odómetro y alertas de mantenimiento, app Monitor-X (Android e iPhone), plataforma web, plan de datos y soporte.
- Cobertura: los 32 departamentos de Colombia, con instalación a domicilio (casa, trabajo, parqueadero, bodega u obra). Funciona donde haya cobertura celular.
- Certificaciones: registro ante MinTIC; proveedor autorizado por la Policía Nacional para rastreo satelital de maquinaria amarilla.
- Contacto: WhatsApp y llamadas {PHONE_INTL} (asesor comercial). Atención y soporte 24/7, todos los días.
- Sitio corporativo de la empresa: https://www.seguimientoactivo.com"""


def build_llms(all_pages):
    depts = sorted(load("departamentos-*.json"), key=lambda d: d["name"])
    places = load("municipios-*.json") + load("capitales-*.json")
    lead_by_slug = {p["slug"]: p["lead"] for p in places}

    def links(prefix):
        return [r for r in all_pages if r.startswith(prefix)]

    def line(rel):
        t, d = meta(rel)
        return f"- [{t}]({url_of(rel)}): {d}"

    L = [f"# {BRAND} (gpscarro.com)", "",
         f"> Rastreo GPS vehicular en tiempo real para carros, motos, camiones y maquinaria en toda Colombia. "
         f"Instalación a domicilio {PRICE_INSTALL_TXT} COP y mensualidad {PRICE_MONTH_TXT} COP, sin permanencia. "
         f"App Monitor-X incluida. WhatsApp {PHONE_INTL}.", "",
         "## Datos clave", "", FACTS, "",
         "## Páginas principales", ""]
    for rel in ["index.html", "precios.html", "preguntas-frecuentes.html", "sobre-nosotros.html", "ciudades/index.html",
                "departamentos/index.html", "servicios/index.html", "industrias/index.html", "blog/index.html", "en/index.html"]:
        if rel in all_pages:
            L.append(line(rel))
    L += ["", "## Servicios por tipo de vehículo", ""] + [line(r) for r in links("servicios/") if not r.endswith("index.html")]
    L += ["", "## Industrias", ""] + [line(r) for r in links("industrias/") if not r.endswith("index.html")]
    L += ["", "## Guías del blog", ""] + [line(r) for r in links("blog/") if not r.endswith("index.html")]
    L += ["", "## Cobertura por departamento", ""]
    L += [f"- [GPS en {d['name']}]({BASE}departamentos/gps-{d['slug']}.html)" for d in depts]
    L += ["", "## Cobertura por ciudad y municipio", ""]
    for rel in links("ciudades/"):
        if rel.endswith("index.html"):
            continue
        t, _ = meta(rel)
        L.append(f"- [{t.split('|')[0].strip()}]({url_of(rel)})")
    L += ["", "## Optional", "", f"- [Versión completa para IA con todas las preguntas frecuentes]({BASE}llms-full.txt)",
          f"- [Mapa del sitio XML]({BASE}sitemap.xml)", f"- [Feed RSS del blog]({BASE}blog/rss.xml)", ""]
    open(os.path.join(ROOT, "llms.txt"), "w", encoding="utf-8", newline="\n").write("\n".join(L))

    F = [f"# {BRAND} (gpscarro.com) - información completa", "",
         f"> Documento de referencia para asistentes de IA y buscadores. Actualizado: {TODAY}.", "",
         "## Datos clave", "", FACTS, "",
         "## Cómo contratar", "",
         f"1. Escribir por WhatsApp al {PHONE_INTL} (o llamar) indicando tipo de vehículo y ciudad.",
         "2. Se agenda la instalación a domicilio; en ciudades principales normalmente en menos de 24 horas.",
         "3. El técnico instala el equipo oculto, prueba el corte de motor y activa la app Monitor-X.",
         "4. El cliente queda con soporte por WhatsApp.", "",
         "## Preguntas frecuentes", ""]
    for g, items in FAQ_GROUPS:
        F += [f"### {g}", ""]
        for q, a in items:
            F += [f"**{q}**", a, ""]
    F += ["## Cobertura por departamento", ""]
    for d in depts:
        F.append(f"### {d['name']} ({BASE}departamentos/gps-{d['slug']}.html)")
        F.append(d["lead"])
        muns = sorted({m for sr in d["subregions"] for m in sr["municipios"]})
        F.append("Municipios con instalación, entre otros: " + ", ".join(muns) + ".")
        F.append("")
    F += ["## Ciudades y municipios con página propia", ""]
    for rel in links("ciudades/"):
        if rel.endswith("index.html"):
            continue
        slug = rel[len("ciudades/gps-"):-5]
        t, dsc = meta(rel)
        F.append(f"- {t.split('|')[0].strip()} ({url_of(rel)}): {lead_by_slug.get(slug, dsc)}")
    F.append("")
    open(os.path.join(ROOT, "llms-full.txt"), "w", encoding="utf-8", newline="\n").write("\n".join(F))


if __name__ == "__main__":
    ps = pages()
    n = build_sitemap(ps)
    build_llms(ps)
    print(f"sitemap.xml: {n} URLs; llms.txt and llms-full.txt written")
