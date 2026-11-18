"""One-off: shorten <title> and meta description on hand-written pages so Google
does not truncate them (titles <= 60 chars, descriptions <= 158 chars).
Run from the repository root:  python -I _tools/fix_meta.py
"""
import html
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = "WhatsApp 316 059 2569."

META = {
    "blog/app-monitor-x-tutorial.html": ("App Monitor-X: Tutorial para Rastrear tu Vehículo", None),
    "blog/beneficios-gps-carro.html": ("10 Beneficios de Instalar GPS en tu Carro en Colombia", None),
    "blog/como-funciona-gps-vehicular.html": ("Cómo Funciona el GPS Vehicular: Guía Completa 2026",
        "Cómo funciona el GPS vehicular paso a paso: satélites, red celular, app y alertas en tiempo real. Guía clara para entender tu rastreador."),
    "blog/como-recuperar-carro-robado-gps.html": ("Cómo Recuperar un Carro Robado con GPS en Colombia", None),
    "blog/geocercas-que-son.html": ("Qué Son las Geocercas GPS y Cómo Usarlas", None),
    "blog/gps-flotas-ahorro.html": ("Cómo el GPS Reduce Costos en Flotas de Transporte", None),
    "blog/gps-motocicletas-guia-completa.html": ("GPS para Motos en Colombia 2026: Precios e Instalación",
        "Guía de GPS para motos en Colombia 2026: instalación $120.000, mensualidad $47.600, equipo oculto y apagado remoto. Protege tu moto del robo."),
    "blog/gps-vs-airtag-comparacion.html": ("GPS Vehicular vs AirTag 2026: ¿Cuál Protege Mejor?", None),
    "blog/gps-vs-robo-carros.html": ("GPS Antirrobo: Cómo Proteger tu Carro del Robo", None),
    "blog/index.html": ("Blog GPS Vehicular: Guías y Consejos | Seguimiento Activo", None),
    "blog/mejor-gps-carro-colombia-2026.html": ("Mejor GPS para Carro en Colombia 2026: Guía de Compra", None),
    "en/index.html": ("GPS Vehicle Tracking in Colombia | Seguimiento Activo",
        "Real-time GPS tracking for cars, motorcycles and trucks in Colombia. Installation COP 120,000, monthly COP 47,600, no lock-in. WhatsApp +57 316 059 2569."),
    "industrias/agricultura.html": ("GPS para Agricultura: Rastreo de Tractores y Cosechadoras", None),
    "industrias/construccion.html": ("GPS para Maquinaria de Construcción en Colombia",
        "GPS para retroexcavadoras, volquetas, grúas y equipos de obra en Colombia. Autorizado por la Policía Nacional. Instalación $120.000, mensualidad $47.600."),
    "industrias/domiciliarios.html": ("GPS para Domiciliarios y Motos de Delivery en Colombia",
        "GPS para domiciliarios y mensajeros: rastreo de motos de delivery en tiempo real, alertas y apagado remoto. Instalación $120.000, mensualidad $47.600."),
    "industrias/flotas-transporte.html": ("GPS para Flotas de Transporte en Colombia | Control 24/7",
        "Control de flotas de transporte y logística en Colombia: rutas, paradas, velocidad y reportes en tiempo real. Instalación $120.000, mensualidad $47.600."),
    "industrias/index.html": ("GPS por Industria: Flotas, Taxis, Domicilios y Más", None),
    "industrias/rent-a-car.html": ("GPS para Rent a Car: Rastreo de Vehículos de Alquiler", None),
    "industrias/taxis.html": ("GPS para Taxis y Conductores de Uber, DiDi e inDrive", None),
    "servicios/gps-camiones.html": (None,
        "GPS para camiones y flotas en Colombia: rastreo en tiempo real, geocercas, alertas y reportes. Instalación $120.000, mensualidad $47.600. Certificado MinTIC."),
    "servicios/gps-carros.html": ("GPS para Carros en Colombia: Rastreador desde $47.600/mes",
        "GPS para carros en Colombia: ubicación en tiempo real, geocercas, apagado remoto y app Monitor-X. Instalación $120.000, mensualidad $47.600, sin permanencia."),
    "servicios/gps-maquinaria.html": ("GPS para Maquinaria Amarilla | Autorizado Policía Nacional",
        "Rastreo GPS de excavadoras, retroexcavadoras, bulldozers y equipo pesado. Proveedor autorizado por la Policía Nacional. Instalación $120.000, $47.600/mes."),
    "servicios/gps-motos.html": ("GPS para Motos en Colombia: Rastreador desde $47.600/mes",
        "GPS para motos: equipo oculto, ubicación en tiempo real, alertas y apagado remoto desde la app Monitor-X. Instalación $120.000, mensualidad $47.600."),
    "servicios/index.html": ("Servicios GPS: Carros, Motos, Camiones y Maquinaria",
        "Rastreo GPS para carros, motos, camiones, flotas y maquinaria amarilla en Colombia. Instalación $120.000, mensualidad $47.600. Certificado MinTIC."),
}

KEPT_CAPITALS = {
    "armenia": ("Armenia", "Quindío"), "bogota": ("Bogotá", None), "cucuta": ("Cúcuta", "Norte de Santander"),
    "ibague": ("Ibagué", "Tolima"), "monteria": ("Montería", "Córdoba"), "neiva": ("Neiva", "Huila"),
    "pasto": ("Pasto", "Nariño"), "popayan": ("Popayán", "Cauca"), "santa-marta": ("Santa Marta", "Magdalena"),
    "valledupar": ("Valledupar", "Cesar"), "villavicencio": ("Villavicencio", "Meta"),
}


def first_fit(cands, n):
    for c in cands:
        if len(c) <= n:
            return c
    return cands[-1]


for slug, (city, dept) in KEPT_CAPITALS.items():
    where = f"{city}, {dept}" if dept else city
    t = first_fit([f"GPS en {where} | Rastreo desde $47.600/mes", f"GPS en {city} | Rastreo Vehicular desde $47.600/mes",
                   f"GPS en {city} | Rastreo Vehicular $47.600"], 60)
    if slug == "bogota":
        t = "GPS en Bogotá | Rastreo de Carros y Motos desde $47.600/mes"
    d = first_fit([f"GPS para carros, motos y camiones en {where}. Instalación a domicilio $120.000, mensualidad $47.600, sin permanencia. {W}",
                   f"GPS para carros, motos y camiones en {city}. Instalación a domicilio $120.000, mensualidad $47.600, sin permanencia. {W}",
                   f"GPS en {city}: instalación $120.000, mensualidad $47.600, sin permanencia. {W}"], 158)
    META[f"ciudades/gps-{slug}.html"] = (t, d)

changed = 0
for rel, (t, d) in META.items():
    p = os.path.join(ROOT, rel)
    s = open(p, encoding="utf-8").read()
    o = s
    if t:
        assert len(t) <= 60, (rel, len(t))
        s = re.sub(r"<title>.*?</title>", lambda m: f"<title>{html.escape(t, quote=False)}</title>", s, count=1, flags=re.S)
    if d:
        assert len(d) <= 160, (rel, len(d))
        s = re.sub(r'<meta name="description" content="[^"]*">',
                   lambda m: f'<meta name="description" content="{html.escape(d, quote=True)}">', s, count=1)
    if s != o:
        open(p, "w", encoding="utf-8", newline="").write(s)
        changed += 1
print("pages updated:", changed)
