"""Generate location pages for gpscarro.com from _tools/data/*.json.

Outputs:
  ciudades/gps-<slug>.html          one page per place in municipios-*.json and capitales-*.json
  ciudades/index.html               all cities grouped by department
  departamentos/gps-<slug>.html     one page per department
  departamentos/index.html          departments grouped by natural region

Run from the repository root:  python -I _tools/build_locations.py
"""
import glob
import json
import os
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from site_common import (  # noqa: E402
    BASE, BRAND, FIRST_YEAR_TXT, GA, LEAD_TRACKING, ORG_ID, PHONE_HUMAN, PRICE_INSTALL,
    PRICE_INSTALL_TXT, PRICE_MONTH, PRICE_MONTH_TXT, SA_CSS, TODAY, WEBSITE_ID, YEAR_AFTER_TXT,
    esc, footer_html, jsonld, nav_html, org_node, sticky_html, tel, wa,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "_tools", "data")

# Hand-written capital pages that stay as they are (only linked to).
KEPT = {
    "armenia": ("Armenia", "quindio"), "bogota": ("Bogotá", "cundinamarca"),
    "cucuta": ("Cúcuta", "norte-de-santander"), "ibague": ("Ibagué", "tolima"),
    "monteria": ("Montería", "cordoba"), "neiva": ("Neiva", "huila"), "pasto": ("Pasto", "narino"),
    "popayan": ("Popayán", "cauca"), "santa-marta": ("Santa Marta", "magdalena"),
    "valledupar": ("Valledupar", "cesar"), "villavicencio": ("Villavicencio", "meta"),
}

REGIONS = [
    ("Región Caribe", ["atlantico", "bolivar", "cesar", "cordoba", "la-guajira", "magdalena", "sucre"]),
    ("Región Andina", ["antioquia", "boyaca", "caldas", "cundinamarca", "huila", "norte-de-santander",
                       "quindio", "risaralda", "santander", "tolima"]),
    ("Región Pacífica", ["choco", "valle-del-cauca", "cauca", "narino"]),
    ("Orinoquía", ["arauca", "casanare", "meta", "vichada"]),
    ("Amazonía", ["amazonas", "caqueta", "guainia", "guaviare", "putumayo", "vaupes"]),
    ("Región Insular", ["san-andres-y-providencia"]),
]

FEATURES = [
    ("📍", "Ubicación en tiempo real", "Posición actualizada cada 30 segundos en la app y en la plataforma web."),
    ("🔒", "Apagado remoto del motor", "Inmoviliza el vehículo desde el celular, con el vehículo detenido o a baja velocidad."),
    ("🚧", "Geocercas", "Zonas virtuales con alerta y registro de cada entrada y salida."),
    ("⚡", "Alertas de velocidad", "Aviso inmediato cuando se supera el límite que tú definas."),
    ("🔑", "Encendido y apagado", "Historial con fecha, hora y lugar de cada encendido del motor."),
    ("🛣️", "Odómetro y mantenimiento", "Kilometraje recorrido y alertas para cambio de aceite y revisiones."),
    ("🗺️", "Historial de 12 meses", "Reproduce en el mapa cualquier recorrido del último año."),
    ("📱", "App Monitor-X", "Android e iPhone, varios vehículos en una sola cuenta, sin costo adicional."),
]

GUIDES = [
    ("blog/como-recuperar-carro-robado-gps.html", "🚨", "Qué hacer si te roban el vehículo", "Los pasos para usar el GPS y coordinar con la Policía."),
    ("blog/mejor-gps-carro-colombia-2026.html", "🏆", "Cómo elegir un GPS en Colombia", "Qué revisar antes de contratar: precio, permanencia y app."),
    ("blog/gps-vs-airtag-comparacion.html", "🆚", "GPS vehicular vs AirTag", "Por qué un rastreador de llaves no reemplaza un GPS."),
]


def norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return " ".join(s.replace("-", " ").replace(".", " ").split())


def load(pattern):
    out = []
    for f in sorted(glob.glob(os.path.join(DATA, pattern))):
        out.extend(json.load(open(f, encoding="utf-8")))
    return out


def money_offers():
    return [
        {"@type": "Offer", "name": "Instalación GPS (pago único)", "price": str(PRICE_INSTALL),
         "priceCurrency": "COP", "availability": "https://schema.org/InStock"},
        {"@type": "Offer", "name": "Mensualidad del servicio GPS", "price": str(PRICE_MONTH), "priceCurrency": "COP",
         "availability": "https://schema.org/InStock",
         "priceSpecification": {"@type": "UnitPriceSpecification", "price": str(PRICE_MONTH),
                                "priceCurrency": "COP", "unitText": "MES", "unitCode": "MON"}},
    ]


def pick_title(cands):
    for c in cands:
        if len(c) <= 60:
            return c
    return cands[-1]


def fit_desc(cands):
    for c in cands:
        if len(c) <= 158:
            return c
    return cands[-1][:155].rsplit(" ", 1)[0] + "."


PAGE_CSS = """*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Inter,-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;line-height:1.65;color:#0f172a;background:#fff}
a{color:#1e40af}
.lp-top{background:linear-gradient(135deg,#0f172a 0%,#1e3a8a 55%,#1e40af 100%);color:#fff}
.lp-brand{max-width:1200px;margin:0 auto;padding:12px 20px;display:flex;align-items:center;justify-content:space-between;gap:12px}
.lp-brand a{color:#fff;text-decoration:none;font-weight:800;font-size:1.15rem}
.lp-brand .lp-ph{font-size:.92rem;font-weight:600;opacity:.95}
.lp-hero{max-width:1200px;margin:0 auto;padding:26px 20px 46px}
.crumbs{font-size:.85rem;opacity:.85;margin-bottom:14px}
.crumbs a{color:#bfdbfe;text-decoration:none}
.crumbs a:hover{text-decoration:underline}
.lp-hero h1{font-size:clamp(1.8rem,4.4vw,2.8rem);line-height:1.15;font-weight:800;max-width:880px}
.lp-hero h1 span{color:#34d399}
.lead{font-size:1.12rem;max-width:760px;margin-top:14px;color:#e2e8f0}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:20px}
.chip{background:rgba(255,255,255,.13);border:1px solid rgba(255,255,255,.18);border-radius:999px;padding:6px 14px;font-size:.9rem;font-weight:600}
.chip.g{background:#10b981;border-color:#10b981}
.ctas{display:flex;flex-wrap:wrap;gap:12px;margin-top:24px}
.btn{display:inline-flex;align-items:center;gap:8px;border-radius:12px;padding:14px 22px;font-weight:700;font-size:1.02rem;text-decoration:none;transition:transform .15s}
.btn:hover{transform:translateY(-2px)}
.btn-wa{background:#25D366;color:#fff}
.btn-tel{background:#fff;color:#1e3a8a}
.btn-out{border:2px solid #1e40af;color:#1e40af;background:#fff}
.trust{margin-top:18px;font-size:.9rem;color:#cbd5e1}
.lp{max-width:1000px;margin:0 auto;padding:10px 20px 30px}
.lp section{padding:34px 0;border-bottom:1px solid #e2e8f0}
.lp section:last-child{border-bottom:0}
.lp h2{font-size:clamp(1.35rem,3vw,1.75rem);line-height:1.25;margin-bottom:14px;color:#0f172a}
.lp h3{font-size:1.05rem;margin-bottom:6px;color:#1e3a8a}
.lp p{margin-bottom:12px;color:#334155}
.prices{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px;margin:16px 0}
.pcard{border:2px solid #e2e8f0;border-radius:16px;padding:22px;background:#f8fafc}
.pcard.f{border-color:#10b981;background:#ecfdf5}
.pcard .amt{font-size:2rem;font-weight:800;color:#1e40af;line-height:1.1}
.pcard .per{font-size:.95rem;color:#475569;font-weight:600}
.pcard ul{margin:12px 0 0 0;padding-left:0;list-style:none}
.pcard li{padding:3px 0;color:#334155;font-size:.95rem}
.pcard li:before{content:'✓ ';color:#10b981;font-weight:800}
.note{background:#eff6ff;border-left:4px solid #1e40af;border-radius:8px;padding:12px 16px;color:#1e3a8a;font-size:.95rem;margin-top:10px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;margin-top:10px}
.card{border:1px solid #e2e8f0;border-radius:14px;padding:18px;background:#fff}
.card .ic{font-size:1.6rem;display:block;margin-bottom:6px}
.card p{font-size:.94rem;margin:0}
.tags{display:flex;flex-wrap:wrap;gap:8px;margin:8px 0 16px}
.tag{background:#f1f5f9;border:1px solid #e2e8f0;border-radius:999px;padding:5px 12px;font-size:.9rem;color:#334155;text-decoration:none}
a.tag{color:#1e40af;font-weight:600;background:#eff6ff;border-color:#bfdbfe}
a.tag:hover{background:#1e40af;color:#fff}
.roads{list-style:none;margin-top:6px}
.roads li{padding:10px 0;border-bottom:1px dashed #e2e8f0;color:#334155}
.roads li strong{color:#0f172a}
.steps{counter-reset:s;list-style:none;display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;margin-top:12px}
.steps li{counter-increment:s;background:#f8fafc;border-radius:12px;padding:16px 16px 16px 54px;position:relative;color:#334155;font-size:.95rem}
.steps li:before{content:counter(s);position:absolute;left:14px;top:14px;width:28px;height:28px;border-radius:50%;background:#1e40af;color:#fff;font-weight:800;display:flex;align-items:center;justify-content:center}
.feat{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:12px;margin-top:10px}
.feat div{background:#f8fafc;border-radius:12px;padding:14px}
.feat strong{display:block;color:#0f172a;margin-bottom:2px}
.feat span{font-size:.9rem;color:#475569}
details{border:1px solid #e2e8f0;border-radius:12px;padding:0;margin-bottom:10px;background:#fff}
summary{cursor:pointer;padding:15px 18px;font-weight:700;color:#0f172a;list-style:none;position:relative;padding-right:44px}
summary::-webkit-details-marker{display:none}
summary:after{content:'+';position:absolute;right:18px;top:12px;font-size:1.4rem;color:#1e40af}
details[open] summary:after{content:'−'}
details p{padding:0 18px 16px;margin:0}
.sub{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px}
.sub>div{border:1px solid #e2e8f0;border-radius:14px;padding:16px}
.sub h3{margin-bottom:10px}
.cta-final{background:linear-gradient(135deg,#1e3a8a,#1e40af);color:#fff;border-radius:20px;padding:30px;text-align:center;margin:30px 0 10px}
.cta-final h2{color:#fff}
.cta-final p{color:#dbeafe}
.cta-final .ctas{justify-content:center}
.guides{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px}
.guides a{border:1px solid #e2e8f0;border-radius:14px;padding:16px;text-decoration:none;display:block}
.guides a strong{display:block;color:#1e40af;margin:4px 0}
.guides a span{color:#475569;font-size:.9rem}
.reg h2{margin-top:6px}
.dgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px;margin:10px 0 20px}
.dgrid a{border:1px solid #e2e8f0;border-radius:12px;padding:14px;text-decoration:none;display:block;background:#fff}
.dgrid a:hover{border-color:#1e40af;box-shadow:0 6px 18px rgba(30,64,175,.12)}
.dgrid strong{color:#1e3a8a;display:block}
.dgrid span{color:#64748b;font-size:.88rem}
.search{width:100%;max-width:520px;padding:14px 16px;border:2px solid #cbd5e1;border-radius:12px;font-size:1rem;margin:8px 0 18px}
.search:focus{outline:none;border-color:#1e40af}
.dblock{margin-bottom:22px}
.dblock h3 a{text-decoration:none}
@media(max-width:600px){.lp-brand .lp-ph{display:none}.btn{width:100%;justify-content:center}}
"""


def head(title, desc, canonical, geo=None, extra_jsonld=""):
    geo_meta = ""
    if geo:
        region, place, lat, lon = geo
        geo_meta = (f'<meta name="geo.region" content="{esc(region)}">\n<meta name="geo.placename" content="{esc(place)}">\n'
                    f'<meta name="geo.position" content="{lat};{lon}">\n<meta name="ICBM" content="{lat}, {lon}">\n')
    return f"""<!DOCTYPE html>
<html lang="es-CO">
<head>
<meta charset="UTF-8">
<!-- SA:GENERATED by _tools/build_locations.py - edit the data/templates, not this file -->
<meta name="viewport" content="width=device-width, initial-scale=1.0">
{GA}
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<link rel="canonical" href="{canonical}">
{geo_meta}<meta property="og:type" content="website">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:locale" content="es_CO">
<meta property="og:url" content="{canonical}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{BASE}og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{BASE}og-image.png">
<meta name="theme-color" content="#1e40af">
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>📍</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" media="print" onload="this.media='all'">
<link rel="alternate" type="application/rss+xml" title="Blog de {BRAND}" href="{BASE}blog/rss.xml">
{extra_jsonld}
<style>
{PAGE_CSS}
{SA_CSS}
</style>
</head>
"""


def top(p, crumbs, wa_text, current="ciudades"):
    crumb_html = " › ".join(
        f'<a href="{esc(h)}">{esc(t)}</a>' if h else f'<span aria-current="page">{esc(t)}</span>' for t, h in crumbs)
    return (f'<body>\n{nav_html(p, current, wa_text)}\n<header class="lp-top">'
            f'<div class="lp-brand"><a href="{p or "./"}">📍 {BRAND}</a>'
            f'<a class="lp-ph" href="{tel()}">📞 {PHONE_HUMAN}</a></div>'
            f'<div class="lp-hero"><nav class="crumbs" aria-label="Ruta de navegación">{crumb_html}</nav>')


def ctas(wa_text):
    return (f'<div class="ctas"><a class="btn btn-wa" href="{esc(wa(wa_text))}" target="_blank" rel="noopener">💬 Cotizar por WhatsApp</a>'
            f'<a class="btn btn-tel" href="{tel()}">📞 Llamar {PHONE_HUMAN}</a></div>')


def price_section(where):
    return f"""<section id="precios"><h2>Precio del GPS en {esc(where)} (2026)</h2>
<p>El precio es el mismo en todo el país y no hay costos escondidos: pagas la instalación una sola vez y luego una mensualidad fija que incluye el plan de datos del equipo, la plataforma y la app.</p>
<div class="prices">
<div class="pcard"><div class="per">Instalación · pago único</div><div class="amt">{PRICE_INSTALL_TXT}</div>
<ul><li>Dispositivo GPS en préstamo (comodato)</li><li>Instalación profesional y oculta</li><li>Configuración y activación</li><li>Capacitación en la app Monitor-X</li></ul></div>
<div class="pcard f"><div class="per">Mensualidad · servicio completo</div><div class="amt">{PRICE_MONTH_TXT}<span style="font-size:1rem">/mes</span></div>
<ul><li>Rastreo 24/7, ubicación cada 30 segundos</li><li>Historial de recorridos de 12 meses</li><li>Alertas ilimitadas y geocercas</li><li>Soporte técnico incluido</li></ul></div>
</div>
<p class="note">Primer año: <strong>{FIRST_YEAR_TXT}</strong> (instalación + 12 mensualidades). Desde el segundo año: <strong>{YEAR_AFTER_TXT}</strong> al año. Sin cláusula de permanencia: si cancelas, devuelves el equipo sin costo. <a href="{{P}}precios.html">Ver precios en detalle</a>.</p>
</section>"""


def features_section():
    items = "".join(f"<div><strong>{i} {esc(t)}</strong><span>{esc(d)}</span></div>" for i, t, d in FEATURES)
    return f'<section><h2>Funciones incluidas en la mensualidad</h2><div class="feat">{items}</div></section>'


def faq_section(title, faqs):
    items = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in faqs)
    return f'<section id="preguntas"><h2>{esc(title)}</h2>{items}</section>'


def guides_section(p):
    items = "".join(f'<a href="{p}{h}"><span>{i}</span><strong>{esc(t)}</strong><span>{esc(d)}</span></a>' for h, i, t, d in GUIDES)
    return f'<section><h2>Guías útiles antes de instalar</h2><div class="guides">{items}</div></section>'


def faq_jsonld(faqs):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}


def crumbs_jsonld(url, crumbs):
    items = []
    for i, (name, href) in enumerate(crumbs, 1):
        items.append({"@type": "ListItem", "position": i, "name": name, "item": href})
    return {"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": items}


def std_faqs(where):
    return [
        (f"¿Cuánto cuesta el GPS para carro o moto en {where}?",
         f"La instalación cuesta {PRICE_INSTALL_TXT} (pago único) y la mensualidad {PRICE_MONTH_TXT}. La instalación incluye el dispositivo en préstamo, "
         "el montaje oculto y la configuración; la mensualidad incluye rastreo 24/7 cada 30 segundos, historial de 12 meses, alertas, "
         "app Monitor-X y soporte. El primer año suma " + FIRST_YEAR_TXT + "."),
        ("¿Hay cláusula de permanencia o contrato mínimo?",
         "No. Puedes cancelar cuando quieras. El equipo GPS es prestado mientras tengas el servicio; si cancelas, lo devuelves y no pagas multas ni costos adicionales."),
        (f"¿Qué hago si me roban el vehículo en {where}?",
         "Abre la app Monitor-X para ver la ubicación en tiempo real, llama a la Policía al 123 y comparte la posición con la patrulla. "
         "Si el vehículo está detenido o va despacio, puedes apagar el motor desde la app. No intentes recuperarlo por tu cuenta."),
    ]


# ------------------------------------------------------------------ place page

def place_page(pl, depts, names, file_exists):
    slug, name = pl["slug"], pl["name"]
    d = depts[pl["dept"]]
    dname = d["name"]
    url = f"{BASE}ciudades/gps-{slug}.html"
    p = "../"
    where = name
    title = pick_title([
        f"GPS en {name}, {dname} | Rastreo desde $47.600/mes",
        f"GPS en {name} | Rastreo Vehicular desde $47.600/mes",
        f"GPS en {name} | Rastreo Vehicular $47.600",
        f"GPS {name} | Rastreo Vehicular",
    ])
    desc = fit_desc([
        f"GPS para carros, motos y camiones en {name}, {dname}. Instalación a domicilio {PRICE_INSTALL_TXT} y mensualidad {PRICE_MONTH_TXT}, sin permanencia. WhatsApp {PHONE_HUMAN}.",
        f"GPS para carros, motos y camiones en {name}. Instalación a domicilio {PRICE_INSTALL_TXT}, mensualidad {PRICE_MONTH_TXT}, sin permanencia. WhatsApp {PHONE_HUMAN}.",
        f"Rastreo GPS en {name}: instalación {PRICE_INSTALL_TXT}, mensualidad {PRICE_MONTH_TXT}, sin permanencia. WhatsApp {PHONE_HUMAN}.",
    ])
    wa_text = f"Hola, estoy en {name} ({dname}) y quiero cotizar un GPS para mi vehículo"
    crumbs = [("Inicio", "../"), ("Cobertura", "./"), (dname, f"../departamentos/gps-{d['slug']}.html"), (f"GPS {name}", None)]
    crumbs_ld = [("Inicio", BASE), ("Cobertura", BASE + "ciudades/"),
                 (dname, f"{BASE}departamentos/gps-{d['slug']}.html"), (f"GPS {name}", url)]
    local_faqs = [(f["q"], f["a"]) for f in pl["faqs"]]
    faqs = local_faqs + std_faqs(where)
    place_ld = {"@type": "City", "name": name,
                "containedInPlace": {"@type": "AdministrativeArea", "name": dname},
                "geo": {"@type": "GeoCoordinates", "latitude": pl["lat"], "longitude": pl["lon"]}}
    graph = [
        org_node(),
        {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": title, "description": desc,
         "inLanguage": "es-CO", "isPartOf": {"@id": WEBSITE_ID}, "breadcrumb": {"@id": url + "#breadcrumb"},
         "about": {"@id": url + "#service"}, "dateModified": TODAY},
        {"@type": "Service", "@id": url + "#service", "name": f"Rastreo GPS vehicular en {name}",
         "serviceType": "Rastreo y monitoreo GPS vehicular", "provider": {"@id": ORG_ID},
         "areaServed": place_ld, "offers": money_offers(),
         "description": pl["lead"]},
        crumbs_jsonld(url, crumbs_ld),
        faq_jsonld(faqs),
    ]
    metro = f" · {esc(pl['metro'])}" if pl.get("metro") else ""
    out = [head(title, desc, url, (d["iso"], name, pl["lat"], pl["lon"]), jsonld(graph))]
    out.append(top(p, crumbs, wa_text))
    out.append(f'<h1>GPS para carros y motos en <span>{esc(name)}</span></h1>'
               f'<p class="lead">{esc(pl["lead"])}</p>'
               f'<div class="chips"><span class="chip">📍 {esc(name)}, {esc(dname)}{metro}</span>'
               f'<span class="chip">Instalación {PRICE_INSTALL_TXT}</span><span class="chip g">{PRICE_MONTH_TXT}/mes</span>'
               f'<span class="chip">Sin permanencia</span></div>'
               + ctas(wa_text) +
               '<p class="trust">✓ Certificado MinTIC · ✓ Proveedor autorizado de la Policía Nacional para maquinaria amarilla · ✓ Instalación a domicilio</p>'
               '</div></header>\n<main class="lp">')
    out.append(f'<section><h2>Rastreo GPS en {esc(name)}: lo que debes saber</h2>'
               + "".join(f"<p>{esc(x)}</p>" for x in pl["intro"]) + "</section>")
    out.append(price_section(name).replace("{P}", p))
    out.append(f'<section><h2>¿Quién usa GPS en {esc(name)}?</h2><div class="cards">'
               + "".join(f'<div class="card"><span class="ic">{u["icon"]}</span><h3>{esc(u["title"])}</h3><p>{esc(u["text"])}</p></div>' for u in pl["uses"])
               + "</div></section>")
    out.append(f'<section><h2>Cobertura en {esc(name)}: zonas y vías</h2>'
               f'<p>Instalamos a domicilio en cualquier sector de {esc(name)} y el GPS reporta donde haya cobertura celular. Estas son algunas de las zonas donde más atendemos:</p>'
               '<div class="tags">' + "".join(f'<span class="tag">{esc(z)}</span>' for z in pl["zones"]) + "</div>"
               f'<h3>Vías principales</h3><ul class="roads">'
               + "".join(f'<li><strong>{esc(r["name"])}:</strong> {esc(r["note"])}</li>' for r in pl["roads"]) + "</ul></section>")
    out.append(f'<section id="instalacion"><h2>Instalación a domicilio en {esc(name)}</h2><p>{esc(pl["install_note"])}</p>'
               '<ol class="steps">'
               f'<li>Escríbenos por WhatsApp al {PHONE_HUMAN} con el tipo de vehículo y tu ubicación.</li>'
               '<li>Acordamos el día y el lugar: casa, trabajo, parqueadero o bodega.</li>'
               '<li>El técnico instala el equipo de forma oculta y prueba el corte de motor.</li>'
               '<li>Activamos la app Monitor-X en tu celular y te enseñamos a usarla.</li></ol></section>')
    out.append(features_section())
    out.append(faq_section(f"Preguntas frecuentes sobre GPS en {name}", faqs))
    # nearby
    near = []
    for s in pl.get("nearby", []):
        if s in names and file_exists(f"ciudades/gps-{s}.html"):
            near.append(f'<a class="tag" href="gps-{s}.html">GPS {esc(names[s])}</a>')
    out.append(f'<section><h2>GPS en municipios cercanos a {esc(name)}</h2><div class="tags">{"".join(near)}</div>'
               f'<p>También instalamos en el resto de <a href="../departamentos/gps-{d["slug"]}.html">{esc(dname)}</a>. '
               'Consulta la <a href="./">cobertura completa por ciudad</a> o los <a href="../departamentos/">32 departamentos</a>.</p></section>')
    out.append(guides_section(p))
    out.append(f'<div class="cta-final"><h2>Protege tu vehículo en {esc(name)} hoy</h2>'
               f'<p>Instalación {PRICE_INSTALL_TXT} · Mensualidad {PRICE_MONTH_TXT} · Sin permanencia. Te responde un asesor comercial.</p>'
               + ctas(wa_text) + "</div>")
    out.append("</main>\n" + footer_html(p) + "\n" + sticky_html(wa_text) + "\n" + LEAD_TRACKING + "\n</body>\n</html>\n")
    return "".join(out)


# ------------------------------------------------------------- department page

def dept_page(d, depts, places_by_dept, name_to_slug, names, file_exists):
    slug, name = d["slug"], d["name"]
    url = f"{BASE}departamentos/gps-{slug}.html"
    p = "../"
    title = pick_title([
        f"GPS en {name} | Rastreo Vehicular en Todo el Departamento",
        f"GPS en {name} | Rastreo Vehicular desde $47.600/mes",
        f"GPS en {name} | Rastreo Vehicular",
    ])
    cap = names.get(d["capital"], "")
    desc = fit_desc([
        f"GPS vehicular en {name}: {cap} y municipios del departamento. Instalación a domicilio {PRICE_INSTALL_TXT}, mensualidad {PRICE_MONTH_TXT}, sin permanencia. WhatsApp {PHONE_HUMAN}.",
        f"GPS vehicular en {name}. Instalación a domicilio {PRICE_INSTALL_TXT}, mensualidad {PRICE_MONTH_TXT}, sin permanencia. WhatsApp {PHONE_HUMAN}.",
    ])
    wa_text = f"Hola, estoy en {name} y quiero cotizar un GPS para mi vehículo"
    crumbs = [("Inicio", "../"), ("Departamentos", "./"), (f"GPS {name}", None)]
    crumbs_ld = [("Inicio", BASE), ("Departamentos", BASE + "departamentos/"), (f"GPS {name}", url)]
    faqs = [(f["q"], f["a"]) for f in d["faqs"]] + std_faqs(name)[:2]
    graph = [
        org_node(),
        {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": title, "description": desc,
         "inLanguage": "es-CO", "isPartOf": {"@id": WEBSITE_ID}, "breadcrumb": {"@id": url + "#breadcrumb"},
         "about": {"@id": url + "#service"}, "dateModified": TODAY},
        {"@type": "Service", "@id": url + "#service", "name": f"Rastreo GPS vehicular en {name}",
         "serviceType": "Rastreo y monitoreo GPS vehicular", "provider": {"@id": ORG_ID},
         "areaServed": {"@type": "AdministrativeArea", "name": name, "identifier": d["iso"],
                        "containedInPlace": {"@type": "Country", "name": "Colombia"}},
         "offers": money_offers(), "description": d["lead"]},
        crumbs_jsonld(url, crumbs_ld),
        faq_jsonld(faqs),
    ]
    out = [head(title, desc, url, (d["iso"], name, d["lat"], d["lon"]), jsonld(graph))]
    out.append(top(p, crumbs, wa_text))
    out.append(f'<h1>GPS vehicular en <span>{esc(name)}</span></h1><p class="lead">{esc(d["lead"])}</p>'
               f'<div class="chips"><span class="chip">📍 {esc(name)} · capital {esc(cap)}</span>'
               f'<span class="chip">Instalación {PRICE_INSTALL_TXT}</span><span class="chip g">{PRICE_MONTH_TXT}/mes</span><span class="chip">Sin permanencia</span></div>'
               + ctas(wa_text) +
               '<p class="trust">✓ Certificado MinTIC · ✓ Proveedor autorizado de la Policía Nacional para maquinaria amarilla · ✓ Instalación a domicilio</p>'
               '</div></header>\n<main class="lp">')
    out.append(f'<section><h2>Rastreo GPS en {esc(name)}</h2>' + "".join(f"<p>{esc(x)}</p>" for x in d["intro"]) + "</section>")
    # city pages in this department
    city_cards = []
    for s, n in places_by_dept.get(slug, []):
        if file_exists(f"ciudades/gps-{s}.html"):
            tag = " (capital)" if s == d["capital"] else ""
            city_cards.append(f'<a href="../ciudades/gps-{s}.html"><strong>GPS en {esc(n)}{tag}</strong><span>Zonas, vías e instalación a domicilio</span></a>')
    if city_cards:
        out.append(f'<section><h2>Ciudades de {esc(name)} con página de cobertura</h2><div class="dgrid">{"".join(city_cards)}</div></section>')
    subs = []
    for sr in d["subregions"]:
        chips = []
        for m in sr["municipios"]:
            s = name_to_slug.get((slug, norm(m)))
            if s and file_exists(f"ciudades/gps-{s}.html"):
                chips.append(f'<a class="tag" href="../ciudades/gps-{s}.html">{esc(m)}</a>')
            else:
                chips.append(f'<span class="tag">{esc(m)}</span>')
        subs.append(f'<div><h3>{esc(sr["name"])}</h3><div class="tags">{"".join(chips)}</div></div>')
    out.append(f'<section><h2>Municipios con instalación en {esc(name)}</h2>'
               f'<p>Instalamos a domicilio en la capital y en los municipios del departamento; en zonas rurales o apartadas acordamos la fecha por WhatsApp. El GPS reporta en cualquier lugar con cobertura celular.</p>'
               f'<div class="sub">{"".join(subs)}</div></section>')
    out.append(f'<section><h2>Corredores viales de {esc(name)}</h2><ul class="roads">'
               + "".join(f'<li><strong>{esc(r["name"])}:</strong> {esc(r["note"])}</li>' for r in d["roads"]) + "</ul></section>")
    out.append(f'<section><h2>Usos más comunes del GPS en {esc(name)}</h2><div class="cards">'
               + "".join(f'<div class="card"><span class="ic">{u["icon"]}</span><h3>{esc(u["title"])}</h3><p>{esc(u["text"])}</p></div>' for u in d["uses"])
               + "</div></section>")
    out.append(price_section(name).replace("{P}", p))
    out.append(features_section())
    out.append(faq_section(f"Preguntas frecuentes sobre GPS en {name}", faqs))
    others = "".join(f'<a class="tag" href="gps-{o["slug"]}.html">{esc(o["name"])}</a>'
                     for o in sorted(depts.values(), key=lambda x: norm(x["name"])) if o["slug"] != slug)
    out.append(f'<section><h2>GPS en otros departamentos</h2><div class="tags">{others}</div></section>')
    out.append(f'<div class="cta-final"><h2>Cotiza tu GPS en {esc(name)}</h2>'
               f'<p>Instalación {PRICE_INSTALL_TXT} · Mensualidad {PRICE_MONTH_TXT} · Sin permanencia.</p>' + ctas(wa_text) + "</div>")
    out.append("</main>\n" + footer_html(p) + "\n" + sticky_html(wa_text) + "\n" + LEAD_TRACKING + "\n</body>\n</html>\n")
    return "".join(out)


# ------------------------------------------------------------------ hub pages

def dept_index(depts, names):
    url = BASE + "departamentos/"
    p = "../"
    title = "GPS en los 32 Departamentos de Colombia | Seguimiento Activo"
    desc = (f"Rastreo GPS vehicular en los 32 departamentos de Colombia. Instalación a domicilio {PRICE_INSTALL_TXT}, "
            f"mensualidad {PRICE_MONTH_TXT}, sin permanencia. WhatsApp {PHONE_HUMAN}.")
    wa_text = "Hola, quiero cotizar un GPS para mi vehículo"
    crumbs = [("Inicio", "../"), ("Departamentos", None)]
    items = []
    for i, (reg, slugs) in enumerate(REGIONS):
        for s in slugs:
            items.append({"@type": "ListItem", "position": len(items) + 1, "name": f"GPS en {depts[s]['name']}",
                          "url": f"{BASE}departamentos/gps-{s}.html"})
    graph = [org_node(),
             {"@type": "CollectionPage", "@id": url + "#webpage", "url": url, "name": title, "description": desc,
              "inLanguage": "es-CO", "isPartOf": {"@id": WEBSITE_ID}, "dateModified": TODAY,
              "mainEntity": {"@type": "ItemList", "numberOfItems": len(items), "itemListElement": items}},
             crumbs_jsonld(url, [("Inicio", BASE), ("Departamentos", url)])]
    out = [head(title, desc, url, ("CO", "Colombia", 4.5709, -74.2973), jsonld(graph)), top(p, crumbs, wa_text)]
    out.append('<h1>GPS vehicular en <span>los 32 departamentos</span> de Colombia</h1>'
               '<p class="lead">El servicio funciona igual en todo el país: mismo precio, misma app y soporte por WhatsApp. Elige tu departamento para ver municipios, vías y usos más comunes.</p>'
               + ctas(wa_text) + '</div></header>\n<main class="lp">')
    for reg, slugs in REGIONS:
        cards = "".join(
            f'<a href="gps-{s}.html"><strong>GPS en {esc(depts[s]["name"])}</strong><span>Capital: {esc(names.get(depts[s]["capital"], ""))}</span></a>'
            for s in sorted(slugs, key=lambda x: norm(depts[x]["name"])))
        out.append(f'<section class="reg"><h2>{esc(reg)}</h2><div class="dgrid">{cards}</div></section>')
    out.append('<section><h2>¿Tu municipio no aparece?</h2><p>Instalamos en todo el territorio nacional. Si tu municipio no tiene página propia, escríbenos y coordinamos la instalación en tu casa, finca, empresa u obra. El GPS reporta en cualquier lugar con cobertura celular.</p>'
               + ctas(wa_text) + "</section>")
    out.append("</main>\n" + footer_html(p) + "\n" + sticky_html(wa_text) + "\n" + LEAD_TRACKING + "\n</body>\n</html>\n")
    return "".join(out)


def city_index(depts, places_by_dept, file_exists):
    url = BASE + "ciudades/"
    p = "../"
    title = "GPS por Ciudad en Colombia | Cobertura en 100+ Municipios"
    total = sum(1 for v in places_by_dept.values() for s, _ in v if file_exists(f"ciudades/gps-{s}.html"))
    title = f"GPS por Ciudad en Colombia | Cobertura en {total} Municipios"
    desc = (f"Encuentra el GPS vehicular en tu ciudad: {total} municipios con página de cobertura en los 32 departamentos. "
            f"Instalación {PRICE_INSTALL_TXT}, mensualidad {PRICE_MONTH_TXT}.")
    wa_text = "Hola, quiero cotizar un GPS para mi vehículo"
    crumbs = [("Inicio", "../"), ("Cobertura por ciudad", None)]
    items = []
    blocks = []
    for d in sorted(depts.values(), key=lambda x: norm(x["name"])):
        links = []
        for s, n in sorted(places_by_dept.get(d["slug"], []), key=lambda x: (x[0] != d["capital"], norm(x[1]))):
            if not file_exists(f"ciudades/gps-{s}.html"):
                continue
            items.append({"@type": "ListItem", "position": len(items) + 1, "name": f"GPS en {n}", "url": f"{BASE}ciudades/gps-{s}.html"})
            links.append(f'<a class="tag" href="gps-{s}.html" data-n="{esc(norm(n + " " + d["name"]))}">{esc(n)}</a>')
        blocks.append(f'<div class="dblock" data-d="{esc(norm(d["name"]))}"><h3><a href="../departamentos/gps-{d["slug"]}.html">{esc(d["name"])} →</a></h3><div class="tags">{"".join(links)}</div></div>')
    graph = [org_node(),
             {"@type": "CollectionPage", "@id": url + "#webpage", "url": url, "name": title, "description": desc,
              "inLanguage": "es-CO", "isPartOf": {"@id": WEBSITE_ID}, "dateModified": TODAY,
              "mainEntity": {"@type": "ItemList", "numberOfItems": len(items), "itemListElement": items}},
             crumbs_jsonld(url, [("Inicio", BASE), ("Cobertura por ciudad", url)])]
    out = [head(title, desc, url, ("CO", "Colombia", 4.5709, -74.2973), jsonld(graph)), top(p, crumbs, wa_text)]
    out.append(f'<h1>GPS vehicular en <span>tu ciudad</span></h1><p class="lead">{total} ciudades y municipios con página de cobertura, en los 32 departamentos. Mismo precio en todo el país: instalación {PRICE_INSTALL_TXT} y mensualidad {PRICE_MONTH_TXT}.</p>'
               + ctas(wa_text) + '</div></header>\n<main class="lp">')
    out.append('<section><h2>Busca tu ciudad o municipio</h2>'
               '<label for="q" style="display:block;font-weight:600;color:#334155">Escribe el nombre:</label>'
               '<input id="q" class="search" type="search" placeholder="Ej: Soacha, Bello, Palmira, Ipiales..." autocomplete="off">'
               + "".join(blocks) +
               '<p id="nores" style="display:none">No encontramos ese municipio en la lista, pero igual instalamos allí. <a href="' + esc(wa(wa_text)) + '">Escríbenos por WhatsApp</a>.</p>'
               '</section>')
    out.append('<section><h2>¿No ves tu municipio?</h2><p>Atendemos todo el país. Si tu municipio no está en la lista, escríbenos y coordinamos la instalación a domicilio. '
               'También puedes ver la cobertura por <a href="../departamentos/">departamento</a>.</p>' + ctas(wa_text) + "</section>")
    out.append("</main>\n" + footer_html(p) + "\n" + sticky_html(wa_text) + "\n" + LEAD_TRACKING)
    out.append("""<script>
(function(){var q=document.getElementById('q');if(!q)return;
function n(s){return s.normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').toLowerCase().trim();}
q.addEventListener('input',function(){var v=n(q.value),any=false;
document.querySelectorAll('.dblock').forEach(function(b){var hit=false,dn=b.getAttribute('data-d');
b.querySelectorAll('a.tag').forEach(function(a){var ok=!v||a.getAttribute('data-n').indexOf(v)>-1||dn.indexOf(v)>-1;a.style.display=ok?'':'none';if(ok)hit=true;});
b.style.display=hit?'':'none';if(hit)any=true;});
document.getElementById('nores').style.display=any?'none':'block';});})();
</script>
</body>
</html>
""")
    return "".join(out)


def main():
    depts_list = load("departamentos-*.json")
    places = load("municipios-*.json") + load("capitales-*.json")
    depts = {d["slug"]: d for d in depts_list}
    names = {k: v[0] for k, v in KEPT.items()}
    for pl in places:
        names[pl["slug"]] = pl["name"]
    places_by_dept = {}
    name_to_slug = {}
    for s, (n, dslug) in KEPT.items():
        places_by_dept.setdefault(dslug, []).append((s, n))
        name_to_slug[(dslug, norm(n))] = s
    for pl in places:
        places_by_dept.setdefault(pl["dept"], []).append((pl["slug"], pl["name"]))
        name_to_slug[(pl["dept"], norm(pl["name"]))] = pl["slug"]
    # common official-name aliases used in subregion lists
    alias = {("valle-del-cauca", "guadalajara de buga"): "buga", ("tolima", "el espinal"): "espinal",
             ("cordoba", "santa cruz de lorica"): "lorica", ("narino", "san andres de tumaco"): "tumaco",
             ("narino", "san juan de pasto"): "pasto", ("bolivar", "cartagena de indias"): "cartagena",
             ("cundinamarca", "bogota d c"): "bogota", ("cundinamarca", "bogota, d c"): "bogota",
             ("guainia", "inirida"): "puerto-inirida", ("santa marta", ""): None,
             ("magdalena", "santa marta d t c h"): "santa-marta", ("meta", "granada"): "granada-meta",
             ("cesar", "valledupar"): "valledupar", ("la-guajira", "riohacha"): "riohacha"}
    for k, v in alias.items():
        if v:
            name_to_slug[k] = v

    generated = set()

    def exists(rel):
        return rel in generated or os.path.exists(os.path.join(ROOT, rel))

    for pl in places:
        generated.add(f"ciudades/gps-{pl['slug']}.html")
    for d in depts_list:
        generated.add(f"departamentos/gps-{d['slug']}.html")

    os.makedirs(os.path.join(ROOT, "departamentos"), exist_ok=True)
    n = 0
    for pl in places:
        if pl["dept"] not in depts:
            print("WARN missing dept", pl["dept"], "for", pl["slug"])
            continue
        open(os.path.join(ROOT, "ciudades", f"gps-{pl['slug']}.html"), "w", encoding="utf-8", newline="\n").write(
            place_page(pl, depts, names, exists))
        n += 1
    for d in depts_list:
        open(os.path.join(ROOT, "departamentos", f"gps-{d['slug']}.html"), "w", encoding="utf-8", newline="\n").write(
            dept_page(d, depts, places_by_dept, name_to_slug, names, exists))
        n += 1
    if len(depts) == 32:
        open(os.path.join(ROOT, "departamentos", "index.html"), "w", encoding="utf-8", newline="\n").write(dept_index(depts, names))
        open(os.path.join(ROOT, "ciudades", "index.html"), "w", encoding="utf-8", newline="\n").write(
            city_index(depts, places_by_dept, exists))
        n += 2
    else:
        print(f"NOTE: only {len(depts)} departments loaded; hub pages not written")
    print(f"pages written: {n}  (places={len(places)}, departments={len(depts)})")


if __name__ == "__main__":
    main()
