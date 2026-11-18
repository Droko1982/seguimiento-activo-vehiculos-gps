"""Shared constants and HTML fragments for gpscarro.com build scripts.

Used by build_locations.py (generated location pages) and enhance_pages.py
(site-wide nav/footer/sticky CTA on hand-written pages). Run scripts from the
repository root with:  python -I _tools/<script>.py
"""
import html
import json
from urllib.parse import quote

BASE = "https://gpscarro.com/"
PHONE_E164 = "+573160592569"
PHONE_WA = "573160592569"
PHONE_HUMAN = "316 059 2569"
PHONE_INTL = "+57 316 059 2569"
PRICE_INSTALL = 120000
PRICE_MONTH = 47600
PRICE_INSTALL_TXT = "$120.000"
PRICE_MONTH_TXT = "$47.600"
FIRST_YEAR_TXT = "$691.200"  # 120.000 + 12 x 47.600
YEAR_AFTER_TXT = "$571.200"  # 12 x 47.600
TODAY = "2026-11-18"
BRAND = "Seguimiento Activo GPS"
ORG_ID = BASE + "#organization"
WEBSITE_ID = BASE + "#website"


def esc(s):
    return html.escape(str(s), quote=True)


def wa(text):
    return f"https://wa.me/{PHONE_WA}?text={quote(text, safe='')}"


def tel():
    return f"tel:{PHONE_E164}"


def org_node():
    """Minimal Organization node repeated in each page graph (full one lives on the home page)."""
    return {
        "@type": ["Organization", "LocalBusiness"],
        "@id": ORG_ID,
        "name": BRAND,
        "alternateName": ["Seguimiento Activo", "GPS Carro Colombia", "gpscarro.com"],
        "url": BASE,
        "logo": BASE + "logo.png",
        "image": BASE + "og-image.png",
        "telephone": PHONE_E164,
        "priceRange": "$47.600 - $120.000 COP",
        "areaServed": {"@type": "Country", "name": "Colombia"},
        "address": {"@type": "PostalAddress", "addressCountry": "CO"},
    }


def jsonld(graph):
    data = {"@context": "https://schema.org", "@graph": graph}
    txt = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    return '<script type="application/ld+json">' + txt.replace("</", "<\\/") + "</script>"


GA = """<script async src="https://www.googletagmanager.com/gtag/js?id=G-GZVSB2S65V"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());gtag('config','G-GZVSB2S65V');</script>"""

LEAD_TRACKING = """<!-- SA: tracking GA4 de leads (WhatsApp / telefono / formulario) -->
<script>
(function(){
  function el(t){return (t && t.nodeType===1) ? t : (t && t.parentElement) || null;}
  function sect(a){var s=a.closest('section');return (s&&s.id)?s.id:'general';}
  document.addEventListener('click',function(e){
    if(typeof gtag!=='function')return;
    var n=el(e.target); if(!n||!n.closest)return;
    var a=n.closest('a[href]'); if(!a)return;
    var h=a.getAttribute('href')||'';
    if(h.indexOf('wa.me')>-1||h.indexOf('api.whatsapp.com')>-1){
      gtag('event','whatsapp_click',{event_category:'lead',event_label:location.pathname,
        page_path:location.pathname,page_section:sect(a),link_text:(a.textContent||'').trim().slice(0,60)});
    }else if(h.indexOf('tel:')===0){
      gtag('event','phone_click',{event_category:'lead',event_label:location.pathname,
        page_path:location.pathname});
    }
  },true);
  document.addEventListener('submit',function(){
    if(typeof gtag!=='function')return;
    gtag('event','form_submit',{event_category:'lead',event_label:location.pathname,
      page_path:location.pathname});
  },true);
})();
</script>"""

# --- Site-wide nav / footer / sticky bar (marker comments make injection idempotent) ---

SA_CSS = """/* === SA: navegacion, footer y barra de contacto global === */
.sa-nav{background:#1e40af;border-bottom:3px solid #10b981}
.sa-nav-in{max-width:1200px;margin:0 auto;padding:0 12px;display:flex;flex-wrap:wrap;align-items:center;gap:2px}
.sa-nav a{color:#fff;text-decoration:none;font-size:.9rem;font-weight:600;padding:12px 12px;white-space:nowrap;border-radius:6px;display:inline-block}
.sa-nav a:hover{background:rgba(255,255,255,.16)}
.sa-nav a[aria-current="page"]{background:rgba(255,255,255,.24)}
.sa-nav .sa-nav-cta{background:#10b981;margin-left:auto}
@media(max-width:760px){.sa-nav-in{overflow-x:auto;flex-wrap:nowrap}.sa-nav a{padding:11px 10px;font-size:.83rem}.sa-nav .sa-nav-cta{margin-left:0}}
.sa-footer{background:#0f172a;color:#e2e8f0;padding:46px 0 22px;margin-top:0;font-family:inherit}
.sa-footer .sa-in{max-width:1200px;margin:0 auto;padding:0 20px}
.sa-fgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:30px;text-align:left}
.sa-fcol h4{color:#fff;font-size:.98rem;margin:0 0 13px;font-weight:700}
.sa-fcol ul{list-style:none;margin:0;padding:0}
.sa-fcol li{margin-bottom:7px}
.sa-fcol a{color:#cbd5e1;text-decoration:none;font-size:.9rem}
.sa-fcol a:hover{color:#fff;text-decoration:underline}
.sa-fcol p{color:#cbd5e1;font-size:.9rem;line-height:1.6;margin:0 0 9px}
.sa-fbottom{border-top:1px solid rgba(255,255,255,.14);margin-top:30px;padding-top:18px;text-align:center;font-size:.83rem;color:#94a3b8;line-height:1.7}
.sa-fbottom a{color:#94a3b8;text-decoration:none;margin:0 6px}
.sa-fbottom a:hover{color:#fff}
.sa-sticky{display:none}
@media(max-width:760px){
 .sa-sticky{display:flex;position:fixed;left:0;right:0;bottom:0;z-index:9999;gap:8px;padding:8px 10px calc(8px + env(safe-area-inset-bottom));background:rgba(15,23,42,.96);box-shadow:0 -4px 18px rgba(0,0,0,.25)}
 .sa-sticky a{flex:1;display:flex;align-items:center;justify-content:center;gap:6px;min-height:46px;border-radius:10px;font-weight:700;font-size:.98rem;text-decoration:none;color:#fff}
 .sa-sticky .sa-st-wa{background:#25D366;flex:1.6}
 .sa-sticky .sa-st-tel{background:#1e40af}
 body{padding-bottom:66px}
 .whatsapp-float{display:none!important}
}"""


def nav_html(p, current=None, wa_text="Hola, vi gpscarro.com y quiero cotizar un GPS para mi vehículo"):
    items = [
        ("inicio", "", "Inicio"),
        ("servicios", "servicios/", "Servicios"),
        ("precios", "precios.html", "Precios"),
        ("ciudades", "ciudades/", "Cobertura"),
        ("industrias", "industrias/", "Industrias"),
        ("blog", "blog/", "Blog"),
        ("faq", "preguntas-frecuentes.html", "Preguntas"),
    ]
    out = ['<!-- SA:NAV --><nav class="sa-nav" aria-label="Navegación principal"><div class="sa-nav-in">']
    for key, href, label in items:
        cur = ' aria-current="page"' if key == current else ""
        out.append(f'<a href="{p}{href or ""}"{cur}>{label}</a>' if href else f'<a href="{p or "./"}"{cur}>{label}</a>')
    out.append(f'<a class="sa-nav-cta" href="{esc(wa(wa_text))}" target="_blank" rel="noopener">💬 WhatsApp</a>')
    out.append("</div></nav><!-- /SA:NAV -->")
    return "".join(out)


def footer_html(p):
    home = p or "./"
    return f"""<!-- SA:FOOTER --><footer class="sa-footer" role="contentinfo"><div class="sa-in"><div class="sa-fgrid">
<div class="sa-fcol"><h4>📍 {BRAND}</h4><p>Rastreo GPS vehicular en tiempo real para carros, motos, camiones y maquinaria. Instalación a domicilio en toda Colombia.</p>
<p><strong>WhatsApp:</strong> <a href="https://wa.me/{PHONE_WA}" target="_blank" rel="noopener">{PHONE_INTL}</a><br><strong>Llamadas:</strong> <a href="{tel()}">{PHONE_HUMAN}</a></p>
<p>Lunes a sábado, 7:00 a.m. a 7:00 p.m.<br>Certificado MinTIC · Policía Nacional</p></div>
<div class="sa-fcol"><h4>Servicios</h4><ul>
<li><a href="{p}servicios/gps-carros.html">GPS para carros</a></li>
<li><a href="{p}servicios/gps-motos.html">GPS para motos</a></li>
<li><a href="{p}servicios/gps-camiones.html">GPS para camiones</a></li>
<li><a href="{p}servicios/gps-maquinaria.html">GPS para maquinaria</a></li>
<li><a href="{p}precios.html">Precios 2026</a></li></ul></div>
<div class="sa-fcol"><h4>Cobertura</h4><ul>
<li><a href="{p}ciudades/gps-bogota.html">GPS Bogotá</a></li>
<li><a href="{p}ciudades/gps-medellin.html">GPS Medellín</a></li>
<li><a href="{p}ciudades/gps-cali.html">GPS Cali</a></li>
<li><a href="{p}ciudades/gps-barranquilla.html">GPS Barranquilla</a></li>
<li><a href="{p}departamentos/">Los 32 departamentos →</a></li>
<li><a href="{p}ciudades/">Todas las ciudades →</a></li></ul></div>
<div class="sa-fcol"><h4>Industrias</h4><ul>
<li><a href="{p}industrias/flotas-transporte.html">Flotas y transporte</a></li>
<li><a href="{p}industrias/taxis.html">Taxis y apps</a></li>
<li><a href="{p}industrias/domiciliarios.html">Domiciliarios</a></li>
<li><a href="{p}industrias/construccion.html">Construcción</a></li>
<li><a href="{p}industrias/">Ver todas →</a></li></ul></div>
<div class="sa-fcol"><h4>Ayuda</h4><ul>
<li><a href="{p}preguntas-frecuentes.html">Preguntas frecuentes</a></li>
<li><a href="{p}sobre-nosotros.html">Sobre nosotros</a></li>
<li><a href="{p}blog/">Blog y guías</a></li>
<li><a href="{p}blog/como-recuperar-carro-robado-gps.html">Si te roban el vehículo</a></li>
<li><a href="{home}#contacto">Cotizar</a></li></ul></div>
</div><div class="sa-fbottom">© 2026 {BRAND} · gpscarro.com · Cobertura nacional
<br><a href="{p}privacidad.html">Privacidad</a> · <a href="{p}terminos.html">Términos</a> · <a href="{p}sitemap.xml">Mapa del sitio</a> · <a href="{p}en/">English</a></div></div></footer><!-- /SA:FOOTER -->"""


def sticky_html(wa_text):
    return (
        '<!-- SA:STICKY --><div class="sa-sticky" aria-label="Contacto rápido">'
        f'<a class="sa-st-wa" href="{esc(wa(wa_text))}" target="_blank" rel="noopener">💬 WhatsApp</a>'
        f'<a class="sa-st-tel" href="{tel()}">📞 Llamar</a></div><!-- /SA:STICKY -->'
    )
