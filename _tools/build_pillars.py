"""Generate the pillar pages: precios.html, preguntas-frecuentes.html, sobre-nosotros.html.

These are written to be quoted by search engines and AI assistants: direct answers
first, facts in tables, and matching FAQPage / AboutPage structured data.
Run from the repository root:  python -I _tools/build_pillars.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_locations import (  # noqa: E402
    ctas, crumbs_jsonld, faq_jsonld, features_section, guides_section, head, money_offers, top,
)
from site_common import (  # noqa: E402
    BASE, BRAND, FIRST_YEAR_TXT, LEAD_TRACKING, ORG_ID, PHONE_E164, PHONE_HUMAN, PHONE_INTL,
    PRICE_INSTALL_TXT, PRICE_MONTH_TXT, TODAY, WEBSITE_ID, YEAR_AFTER_TXT, esc, footer_html,
    jsonld, org_node, sticky_html,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WA_GENERIC = "Hola, vi gpscarro.com y quiero cotizar un GPS para mi vehículo"

# --------------------------------------------------------------------- FAQ data
FAQ_GROUPS = [
    ("Precios y pagos", [
        ("¿Cuánto cuesta un GPS para carro en Colombia con Seguimiento Activo?",
         f"La instalación cuesta {PRICE_INSTALL_TXT} COP, en un solo pago, y la mensualidad {PRICE_MONTH_TXT} COP. "
         f"El primer año suma {FIRST_YEAR_TXT} y desde el segundo año {YEAR_AFTER_TXT} al año. El precio es el mismo en todo el país."),
        ("¿Qué incluye la mensualidad de $47.600?",
         "Rastreo 24 horas con ubicación actualizada cada 30 segundos, historial de recorridos de 12 meses, geocercas, alertas ilimitadas "
         "(velocidad, encendido, entrada y salida de zonas), apagado remoto del motor, odómetro, la app Monitor-X, la plataforma web, "
         "el plan de datos del equipo y soporte técnico."),
        ("¿Tengo que comprar el dispositivo GPS?",
         "No. El equipo se entrega en préstamo (comodato) mientras tengas el servicio activo. La instalación de $120.000 cubre el montaje, "
         "la configuración y la capacitación en la app."),
        ("¿Hay cláusula de permanencia?",
         "No. Puedes cancelar cuando quieras, sin multas. Al cancelar devuelves el equipo GPS y no pagas nada adicional."),
        ("¿El precio cambia según la ciudad o el tipo de vehículo?",
         "El precio base es el mismo en todo Colombia para carros, motos, camiones y maquinaria. Si tienes una flota o necesitas una "
         "configuración especial, te enviamos una cotización por WhatsApp."),
    ]),
    ("Instalación", [
        ("¿Dónde instalan el GPS?",
         "A domicilio, en el lugar que prefieras: tu casa, tu trabajo, un parqueadero, una bodega o una obra. Atendemos los 32 departamentos; "
         "en zonas apartadas acordamos la fecha por WhatsApp."),
        ("¿Qué tan rápido me instalan?",
         "En las ciudades principales la instalación normalmente queda agendada en menos de 24 horas. El técnico instala, prueba el equipo "
         "y activa la app en la misma visita."),
        ("¿En qué parte del vehículo queda el GPS?",
         "Queda oculto, en un punto que no está a la vista, para que sea difícil de encontrar y retirar. El técnico deja probado el corte de motor antes de irse."),
        ("¿Sirve para motos?",
         "Sí. Se instala un equipo compacto y oculto en la moto, con las mismas funciones: ubicación en tiempo real, alertas y apagado remoto."),
        ("¿Sirve para camiones, tractomulas y maquinaria amarilla?",
         "Sí. Seguimiento Activo es proveedor autorizado por la Policía Nacional para el rastreo satelital de maquinaria amarilla, y el servicio "
         "se usa en camiones, tractomulas, volquetas y flotas de carga."),
    ]),
    ("Funcionamiento", [
        ("¿Cada cuánto se actualiza la ubicación?",
         "Cada 30 segundos mientras el vehículo está en movimiento, lo que permite un seguimiento prácticamente en tiempo real desde la app."),
        ("¿El GPS funciona en todo Colombia?",
         "Sí, funciona en cualquier lugar del país con cobertura de red celular, en ciudades, carreteras y zonas rurales con señal."),
        ("¿Qué pasa cuando el vehículo pasa por una zona sin señal?",
         "El GPS deja de reportar mientras no haya cobertura celular y vuelve a actualizar la ubicación en cuanto el equipo recupera la señal."),
        ("¿Puedo apagar el motor desde el celular?",
         "Sí. Desde la app Monitor-X puedes inmovilizar el vehículo. Por seguridad, se usa con el vehículo detenido o a baja velocidad."),
        ("¿Qué son las geocercas?",
         "Son zonas virtuales que dibujas en el mapa, como tu casa, la oficina o una bodega. Cada entrada y salida queda registrada con fecha y hora, y recibes una alerta."),
        ("¿El GPS registra la velocidad y los encendidos del motor?",
         "Sí. Ves la velocidad en tiempo real, defines un límite con alerta, y queda un historial de cada encendido y apagado con fecha, hora y lugar."),
        ("¿Sirve para controlar el mantenimiento?",
         "Sí. El odómetro registra los kilómetros recorridos y puedes programar alertas para el cambio de aceite y otras revisiones según el kilometraje."),
        ("¿Cuánto tiempo guarda el historial de recorridos?",
         "12 meses. Puedes reproducir en el mapa cualquier recorrido del último año, con paradas y velocidades."),
    ]),
    ("App Monitor-X", [
        ("¿Qué es la app Monitor-X?",
         "Es la aplicación gratuita para Android y iPhone con la que ves tus vehículos en el mapa, recibes alertas, revisas el historial y apagas el motor a distancia. "
         "También puedes entrar desde la plataforma web."),
        ("¿Puedo ver varios vehículos en la misma cuenta?",
         "Sí. Todos tus carros, motos o camiones aparecen en una sola cuenta, algo especialmente útil para familias y empresas con flota."),
        ("¿La app tiene costo adicional?",
         "No. La app Monitor-X y la plataforma web están incluidas en la mensualidad."),
    ]),
    ("Robo y seguridad", [
        ("¿Qué hago si me roban el vehículo?",
         "Abre la app y verifica la ubicación en tiempo real, llama a la Policía al 123 y comparte la posición con la patrulla. "
         "Si el vehículo está detenido o va despacio, puedes apagar el motor desde la app. No intentes recuperarlo por tu cuenta."),
        ("¿El GPS evita que me roben el carro o la moto?",
         "Ningún sistema garantiza que no haya robo, pero el GPS te avisa de movimientos no autorizados y permite ubicar el vehículo en tiempo real, "
         "lo que facilita que las autoridades actúen rápido."),
        ("¿Un AirTag sirve como GPS para el carro?",
         "No es lo mismo. Un AirTag depende de que haya dispositivos Apple cerca y no apaga el motor ni guarda historial de recorridos. "
         "Un GPS vehicular reporta por red celular cada 30 segundos y queda conectado al vehículo."),
    ]),
    ("Empresas y flotas", [
        ("¿Sirve para controlar una flota de empresa?",
         "Sí. Ves todos los vehículos en un mapa, revisas recorridos, paradas, excesos de velocidad y horas de uso, y usas geocercas para clientes, bodegas y rutas."),
        ("¿Tienen soluciones para taxis, domiciliarios y rent a car?",
         "Sí. El servicio se usa en taxis y conductores de plataformas, motos de domicilio y mensajería, empresas de alquiler de vehículos, construcción y agricultura."),
    ]),
    ("Sobre Seguimiento Activo", [
        ("¿Qué certificaciones tiene Seguimiento Activo?",
         "Está registrado ante el MinTIC (Ministerio de Tecnologías de la Información y las Comunicaciones) y es proveedor autorizado por la Policía Nacional "
         "para el rastreo satelital de maquinaria amarilla."),
        ("¿Cómo los contacto?",
         f"Por WhatsApp o llamada al {PHONE_INTL}, las 24 horas, todos los días. Te atiende un asesor comercial. "
         "También puedes dejar tus datos en el formulario de cotización de gpscarro.com."),
        ("¿En qué ciudades tienen servicio?",
         "En todo Colombia: los 32 departamentos, con instalación a domicilio en ciudades principales, municipios intermedios y zonas rurales con cobertura celular."),
    ]),
]


def all_faqs():
    return [qa for _, items in FAQ_GROUPS for qa in items]


def write(name, content):
    open(os.path.join(ROOT, name), "w", encoding="utf-8", newline="\n").write(content)


def end(p, wa_text):
    return "</main>\n" + footer_html(p) + "\n" + sticky_html(wa_text) + "\n" + LEAD_TRACKING + "\n</body>\n</html>\n"


# ------------------------------------------------------------------- precios
def precios():
    url = BASE + "precios.html"
    p = ""
    title = "Precio GPS para Carro en Colombia 2026: $47.600/mes"
    desc = (f"¿Cuánto cuesta un GPS para carro o moto en Colombia? Instalación {PRICE_INSTALL_TXT}, mensualidad {PRICE_MONTH_TXT}, "
            f"primer año {FIRST_YEAR_TXT}. Equipo en préstamo y sin permanencia.")
    wa_text = "Hola, vi los precios en gpscarro.com y quiero cotizar un GPS"
    faqs = FAQ_GROUPS[0][1] + [
        ("¿Cuánto pago en total el primer año?",
         f"{FIRST_YEAR_TXT}: la instalación de {PRICE_INSTALL_TXT} más 12 mensualidades de {PRICE_MONTH_TXT}. Desde el segundo año pagas {YEAR_AFTER_TXT} al año."),
        ("¿Hay que pagar algo si cancelo?",
         "No. No hay multas ni permanencia. Solo devuelves el equipo GPS, que es prestado."),
    ]
    graph = [
        org_node(),
        {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": title, "description": desc, "inLanguage": "es-CO",
         "isPartOf": {"@id": WEBSITE_ID}, "breadcrumb": {"@id": url + "#breadcrumb"}, "dateModified": TODAY},
        {"@type": "Service", "@id": url + "#service", "name": "Servicio de rastreo GPS vehicular", "provider": {"@id": ORG_ID},
         "serviceType": "Rastreo y monitoreo GPS vehicular", "areaServed": {"@type": "Country", "name": "Colombia"},
         "offers": money_offers()},
        crumbs_jsonld(url, [("Inicio", BASE), ("Precios", url)]),
        faq_jsonld(faqs),
    ]
    rows = [
        ("Instalación", PRICE_INSTALL_TXT, "Pago único. Montaje oculto, configuración, prueba de corte de motor y capacitación."),
        ("Mensualidad", PRICE_MONTH_TXT, "Rastreo 24/7 cada 30 s, historial 12 meses, alertas, geocercas, app, plataforma web, datos y soporte."),
        ("Equipo GPS", "$0", "Se entrega en préstamo (comodato) mientras tengas el servicio."),
        ("App Monitor-X", "$0", "Android, iPhone y plataforma web, incluidas."),
        ("Primer año", FIRST_YEAR_TXT, "Instalación + 12 mensualidades."),
        ("Desde el segundo año", YEAR_AFTER_TXT + " al año", "Solo las 12 mensualidades."),
        ("Cancelación", "$0", "Sin permanencia ni multas; devuelves el equipo."),
    ]
    table = "".join(f"<tr><th scope=\"row\">{esc(a)}</th><td><strong>{esc(b)}</strong></td><td>{esc(c)}</td></tr>" for a, b, c in rows)
    comp = [
        ("Ubicación en tiempo real", "Sí, cada 30 segundos por red celular", "Solo cuando hay un iPhone cerca", "Depende del equipo y de la SIM que compres"),
        ("Apagado remoto del motor", "Sí, desde la app", "No", "Solo algunos modelos, con instalación"),
        ("Instalación oculta profesional", "Sí, a domicilio", "No aplica", "La haces tú o pagas aparte"),
        ("Plan de datos", "Incluido en la mensualidad", "No aplica", "Lo pagas aparte cada mes"),
        ("Historial y alertas", "12 meses, alertas ilimitadas", "No", "Variable"),
        ("Soporte en Colombia", "Sí, por WhatsApp", "No", "Normalmente no"),
    ]
    comp_rows = "".join(f"<tr><th scope=\"row\">{esc(a)}</th><td>{esc(b)}</td><td>{esc(c)}</td><td>{esc(d)}</td></tr>" for a, b, c, d in comp)
    out = [head(title, desc, url, None, jsonld(graph)).replace("</style>", TABLE_CSS + "</style>", 1),
           top(p, [("Inicio", "./"), ("Precios", None)], wa_text, current="precios")]
    out.append(f'<h1>Precio del GPS para carro en Colombia <span>(2026)</span></h1>'
               f'<p class="lead">Instalación de {PRICE_INSTALL_TXT} una sola vez y {PRICE_MONTH_TXT} al mes. El equipo es prestado, la app está incluida y no hay permanencia.</p>'
               f'<div class="chips"><span class="chip">Instalación {PRICE_INSTALL_TXT}</span><span class="chip g">{PRICE_MONTH_TXT}/mes</span>'
               f'<span class="chip">Primer año {FIRST_YEAR_TXT}</span><span class="chip">Sin permanencia</span></div>' + ctas(wa_text) +
               '</div></header>\n<main class="lp">')
    out.append(f'<section><h2>Respuesta corta</h2><p class="note" style="font-size:1.05rem">Un GPS vehicular con {BRAND} cuesta <strong>{PRICE_INSTALL_TXT}</strong> de instalación (pago único) '
               f'más <strong>{PRICE_MONTH_TXT} al mes</strong>. El primer año suma <strong>{FIRST_YEAR_TXT}</strong> y desde el segundo año <strong>{YEAR_AFTER_TXT}</strong> al año. '
               'El dispositivo es prestado, la app Monitor-X está incluida y puedes cancelar cuando quieras sin multas. El precio es el mismo en todo Colombia.</p></section>')
    out.append(f'<section><h2>Tabla de precios</h2><div class="tw"><table><thead><tr><th>Concepto</th><th>Valor (COP)</th><th>Qué incluye</th></tr></thead><tbody>{table}</tbody></table></div></section>')
    out.append('<section><h2>Precio por tipo de vehículo</h2><div class="cards">'
               f'<a class="card" href="servicios/gps-carros.html" style="text-decoration:none"><span class="ic">🚗</span><h3>Carros y camionetas</h3><p>{PRICE_INSTALL_TXT} + {PRICE_MONTH_TXT}/mes. Apagado remoto, geocercas y alertas.</p></a>'
               f'<a class="card" href="servicios/gps-motos.html" style="text-decoration:none"><span class="ic">🏍️</span><h3>Motos</h3><p>{PRICE_INSTALL_TXT} + {PRICE_MONTH_TXT}/mes. Equipo compacto de instalación oculta.</p></a>'
               f'<a class="card" href="servicios/gps-camiones.html" style="text-decoration:none"><span class="ic">🚛</span><h3>Camiones y flotas</h3><p>Desde {PRICE_MONTH_TXT}/mes por vehículo. Para flotas te enviamos una cotización a la medida.</p></a>'
               f'<a class="card" href="servicios/gps-maquinaria.html" style="text-decoration:none"><span class="ic">🚜</span><h3>Maquinaria amarilla</h3><p>Desde {PRICE_MONTH_TXT}/mes. Proveedor autorizado por la Policía Nacional.</p></a>'
               '</div></section>')
    out.append(f'<section><h2>GPS con mensualidad vs. otras opciones</h2><p>Antes de decidir, compara lo que realmente obtienes por tu dinero:</p>'
               f'<div class="tw"><table><thead><tr><th></th><th>{BRAND}</th><th>Rastreador tipo AirTag</th><th>GPS comprado por internet</th></tr></thead><tbody>{comp_rows}</tbody></table></div>'
               '<p>Más detalles en la guía <a href="blog/gps-vs-airtag-comparacion.html">GPS vehicular vs AirTag</a> y en <a href="blog/mejor-gps-carro-colombia-2026.html">cómo elegir el mejor GPS para carro en Colombia</a>.</p></section>')
    out.append(features_section())
    items = "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in faqs)
    out.append(f'<section id="preguntas"><h2>Preguntas sobre el precio</h2>{items}<p><a href="preguntas-frecuentes.html">Ver todas las preguntas frecuentes →</a></p></section>')
    out.append('<section><h2>Mismo precio en toda Colombia</h2><p>Instalamos a domicilio en los 32 departamentos. Revisa la cobertura de <a href="ciudades/">tu ciudad o municipio</a> o de <a href="departamentos/">tu departamento</a>.</p></section>')
    out.append(f'<div class="cta-final"><h2>Pide tu cotización ahora</h2><p>Te respondemos por WhatsApp, las 24 horas, todos los días.</p>{ctas(wa_text)}</div>')
    out.append(end(p, wa_text))
    write("precios.html", "".join(out))


TABLE_CSS = """.tw{overflow-x:auto;margin:10px 0}
table{width:100%;border-collapse:collapse;font-size:.95rem;min-width:560px}
th,td{border-bottom:1px solid #e2e8f0;padding:11px 12px;text-align:left;vertical-align:top;color:#334155}
thead th{background:#1e3a8a;color:#fff}
tbody th{color:#0f172a;font-weight:700}
tbody tr:nth-child(even){background:#f8fafc}
dl.facts{display:grid;grid-template-columns:minmax(150px,220px) 1fr;border:1px solid #e2e8f0;border-radius:14px;overflow:hidden}
dl.facts dt,dl.facts dd{padding:11px 14px;border-bottom:1px solid #e2e8f0}
dl.facts dt{background:#f8fafc;font-weight:700;color:#0f172a}
dl.facts dd{color:#334155}
@media(max-width:600px){dl.facts{grid-template-columns:1fr}dl.facts dt{border-bottom:0;padding-bottom:2px}}
.toc{display:flex;flex-wrap:wrap;gap:8px;margin:6px 0 4px}
"""


# --------------------------------------------------------- preguntas frecuentes
def faq_page():
    url = BASE + "preguntas-frecuentes.html"
    p = ""
    title = "Preguntas Frecuentes sobre GPS Vehicular | Seguimiento Activo"
    desc = (f"Dudas sobre el GPS para carro y moto: precio ({PRICE_INSTALL_TXT} + {PRICE_MONTH_TXT}/mes), "
            "instalación a domicilio, app Monitor-X, apagado remoto y qué hacer si hay robo.")
    wa_text = "Hola, tengo una pregunta sobre el GPS para mi vehículo"
    faqs = all_faqs()
    graph = [
        org_node(),
        {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": title, "description": desc, "inLanguage": "es-CO",
         "isPartOf": {"@id": WEBSITE_ID}, "breadcrumb": {"@id": url + "#breadcrumb"}, "dateModified": TODAY},
        crumbs_jsonld(url, [("Inicio", BASE), ("Preguntas frecuentes", url)]),
        faq_jsonld(faqs),
    ]
    out = [head(title, desc, url, None, jsonld(graph)).replace("</style>", TABLE_CSS + "</style>", 1),
           top(p, [("Inicio", "./"), ("Preguntas frecuentes", None)], wa_text, current="faq")]
    out.append(f'<h1>Preguntas frecuentes sobre el <span>GPS vehicular</span></h1>'
               f'<p class="lead">{len(faqs)} respuestas claras sobre precios, instalación, funcionamiento, la app Monitor-X y qué hacer si te roban el vehículo.</p>'
               + ctas(wa_text) + '</div></header>\n<main class="lp">')
    toc = "".join(f'<a class="tag" href="#g{i}">{esc(g)}</a>' for i, (g, _) in enumerate(FAQ_GROUPS))
    out.append(f'<section><h2>Temas</h2><div class="toc">{toc}</div></section>')
    for i, (g, items) in enumerate(FAQ_GROUPS):
        body = "".join(f"<details{' open' if i == 0 and j == 0 else ''}><summary>{esc(q)}</summary><p>{esc(a)}</p></details>"
                       for j, (q, a) in enumerate(items))
        out.append(f'<section id="g{i}"><h2>{esc(g)}</h2>{body}</section>')
    out.append('<section><h2>¿No encontraste tu respuesta?</h2><p>Escríbenos por WhatsApp y te respondemos personalmente. '
               'También puedes revisar los <a href="precios.html">precios en detalle</a>, los <a href="servicios/">servicios por tipo de vehículo</a> '
               'o la <a href="ciudades/">cobertura en tu ciudad</a>.</p>' + ctas(wa_text) + '</section>')
    out.append(guides_section(p))
    out.append(end(p, wa_text))
    write("preguntas-frecuentes.html", "".join(out))


# --------------------------------------------------------------- sobre nosotros
def about_page():
    url = BASE + "sobre-nosotros.html"
    p = ""
    title = "Sobre Seguimiento Activo GPS | Rastreo Vehicular Colombia"
    desc = (f"Quiénes somos: rastreo GPS vehicular en tiempo real para personas y empresas en toda Colombia. "
            f"Certificado MinTIC. Atención por WhatsApp {PHONE_HUMAN}.")
    wa_text = WA_GENERIC
    facts = [
        ("Nombre", BRAND),
        ("Sitio web", "gpscarro.com"),
        ("Servicio", "Rastreo y monitoreo GPS vehicular en tiempo real"),
        ("Atención comercial", "Seguimiento Activo GPS, asesor comercial"),
        ("WhatsApp y llamadas", PHONE_INTL),
        ("Horario", "Atención y soporte 24/7, todos los días"),
        ("Cobertura", "Los 32 departamentos de Colombia, con instalación a domicilio"),
        ("Precio", f"Instalación {PRICE_INSTALL_TXT} (pago único) y mensualidad {PRICE_MONTH_TXT}"),
        ("Permanencia", "No hay cláusula de permanencia; el equipo es prestado"),
        ("Aplicación", "Monitor-X para Android y iPhone, y plataforma web"),
        ("Certificaciones", "Registro MinTIC; proveedor autorizado por la Policía Nacional para rastreo de maquinaria amarilla"),
        ("Vehículos", "Carros, motos, camiones, tractomulas, flotas, taxis, motos de domicilio, rent a car, maquinaria amarilla y agrícola"),
    ]
    dl = "".join(f"<dt>{esc(a)}</dt><dd>{esc(b)}</dd>" for a, b in facts)
    person = {"@type": "Person", "@id": BASE + "#asesor-comercial", "name": "Seguimiento Activo GPS",
              "jobTitle": "Asesor comercial", "worksFor": {"@id": ORG_ID}, "telephone": PHONE_E164}
    org_full = org_node()
    org_full.update({
        "description": "Servicio colombiano de rastreo GPS vehicular en tiempo real para carros, motos, camiones y maquinaria, con instalación a domicilio en todo el país.",
        "contactPoint": [{"@type": "ContactPoint", "telephone": PHONE_E164, "contactType": "sales", "areaServed": "CO",
                          "availableLanguage": ["es", "en"]}],
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification",
                                       "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                                       "opens": "00:00", "closes": "23:59"}],
        "knowsAbout": ["Rastreo GPS vehicular", "Control de flotas", "Geocercas", "Inmovilización remota de vehículos",
                       "Rastreo de maquinaria amarilla", "Telemetría vehicular"],
        "sameAs": ["https://www.seguimientoactivo.com", "https://wa.me/573160592569"],
        "employee": {"@id": BASE + "#asesor-comercial"},
    })
    graph = [
        org_full, person,
        {"@type": "AboutPage", "@id": url + "#webpage", "url": url, "name": title, "description": desc, "inLanguage": "es-CO",
         "isPartOf": {"@id": WEBSITE_ID}, "about": {"@id": ORG_ID}, "breadcrumb": {"@id": url + "#breadcrumb"}, "dateModified": TODAY},
        crumbs_jsonld(url, [("Inicio", BASE), ("Sobre nosotros", url)]),
    ]
    out = [head(title, desc, url, None, jsonld(graph)).replace("</style>", TABLE_CSS + "</style>", 1),
           top(p, [("Inicio", "./"), ("Sobre nosotros", None)], wa_text, current=None)]
    out.append(f'<h1>Sobre <span>{BRAND}</span></h1>'
               '<p class="lead">Rastreo GPS vehicular en tiempo real para personas y empresas en toda Colombia, con instalación a domicilio y atención directa por WhatsApp.</p>'
               + ctas(wa_text) + '</div></header>\n<main class="lp">')
    out.append(f'<section><h2>Datos clave</h2><dl class="facts">{dl}</dl></section>')
    out.append('<section><h2>Qué hacemos</h2>'
               '<p>Instalamos dispositivos GPS en carros, motos, camiones y maquinaria para que sus dueños sepan en todo momento dónde está cada vehículo. '
               'Desde la app Monitor-X ves la ubicación actualizada cada 30 segundos, recibes alertas de velocidad, de encendido y de entrada o salida de zonas, '
               'revisas el historial de recorridos de los últimos 12 meses y, si hace falta, apagas el motor a distancia.</p>'
               '<p>El servicio funciona con un modelo simple: el equipo es prestado, pagas la instalación una vez y luego una mensualidad fija que incluye el plan de datos, '
               'la plataforma y el soporte. No hay permanencia; si cancelas, devuelves el equipo.</p>'
               '<p>Atendemos a personas que quieren proteger su vehículo y a empresas que necesitan controlar una flota: transportadores de carga, taxis, '
               'domiciliarios, empresas de alquiler de vehículos, constructoras y productores agrícolas.</p></section>')
    out.append('<section><h2>Cómo trabajamos</h2><ol class="steps">'
               f'<li>Cotizas por WhatsApp al {PHONE_HUMAN} o con el formulario del sitio.</li>'
               '<li>Agendamos la instalación a domicilio en el lugar que prefieras.</li>'
               '<li>El técnico instala el equipo oculto, prueba el corte de motor y activa la app.</li>'
               '<li>Quedas con soporte por WhatsApp para cualquier duda o emergencia.</li></ol></section>')
    out.append('<section><h2>Certificaciones y respaldo</h2>'
               '<p>Seguimiento Activo está registrado ante el Ministerio de Tecnologías de la Información y las Comunicaciones (MinTIC) y es proveedor autorizado por la '
               'Policía Nacional para el rastreo satelital de maquinaria amarilla. El sitio corporativo de la empresa es '
               '<a href="https://www.seguimientoactivo.com" target="_blank" rel="noopener">seguimientoactivo.com</a>; gpscarro.com es el canal de atención comercial '
               'de Seguimiento Activo GPS para clientes de todo el país.</p></section>')
    out.append('<section><h2>Cobertura nacional</h2><p>Instalamos en los 32 departamentos: desde Bogotá, Medellín, Cali y Barranquilla hasta municipios intermedios y zonas rurales. '
               'Consulta la <a href="ciudades/">cobertura por ciudad</a> o por <a href="departamentos/">departamento</a>.</p></section>')
    out.append(f'<div class="cta-final"><h2>Hablemos</h2><p>Te respondemos por WhatsApp o llamada al {PHONE_HUMAN}.</p>{ctas(wa_text)}</div>')
    out.append(end(p, wa_text))
    write("sobre-nosotros.html", "".join(out))


if __name__ == "__main__":
    precios()
    faq_page()
    about_page()
    print("pillar pages written: precios.html, preguntas-frecuentes.html, sobre-nosotros.html")
