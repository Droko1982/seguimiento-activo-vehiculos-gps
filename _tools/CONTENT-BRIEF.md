# Brief de contenido local — gpscarro.com (Seguimiento Activo GPS)

Este brief define los datos que alimentan `_tools/build_locations.py`, que genera las
páginas de departamentos (`/departamentos/`) y ciudades/municipios (`/ciudades/`).
Las carpetas que empiezan por `_` no se publican en GitHub Pages.

## Hechos del negocio (usar SOLO estos; no inventar otros)

- Marca: **Seguimiento Activo GPS** (sitio gpscarro.com). Asesor comercial: Seguimiento Activo GPS.
- Instalación: **$120.000 COP**, pago único. Incluye dispositivo GPS en préstamo (comodato),
  instalación profesional y oculta, configuración y capacitación en la app.
- Mensualidad: **$47.600 COP**. Incluye rastreo 24/7, ubicación actualizada cada 30 segundos,
  historial de recorridos de 12 meses, alertas ilimitadas, geocercas, soporte técnico,
  app Monitor-X (Android e iPhone) y plataforma web.
- Sin cláusula de permanencia. Si cancelas, devuelves el equipo sin costo.
- Funciones: ubicación en tiempo real, geocercas con registro de entrada/salida, apagado remoto
  del motor desde la app (se usa con el vehículo detenido o a baja velocidad), alertas de
  velocidad, registro de encendido/apagado, odómetro y alertas de mantenimiento por kilometraje,
  reportes de uso.
- Certificado/registrado ante MinTIC. Proveedor autorizado por la Policía Nacional para rastreo
  satelital de maquinaria amarilla.
- Funciona en todo lugar con cobertura de red celular. Instalación a domicilio (casa, trabajo,
  parqueadero, bodega u obra), coordinada por WhatsApp. En ciudades principales suele ser en
  menos de 24 horas; en zonas apartadas se agenda la fecha.
- Vehículos: carros particulares, motos, camiones y tractomulas, flotas, maquinaria amarilla,
  taxis y conductores de plataformas, domiciliarios, rent a car, maquinaria agrícola.

## Reglas de redacción

- Español de Colombia, tuteo (tú), tildes correctas. Texto plano: sin markdown, sin HTML,
  sin comillas dobles dentro de los textos (usa comillas simples o ninguna).
- Cada entrada debe ser **única y local**: economía real del lugar, vías reales, barrios/sectores
  reales, terreno y clima, usos típicos de vehículos (mototaxi, carga, petróleo, palma, café,
  flores, puerto, frontera, turismo, minería, ganadería, etc.). Nada de frases plantilla
  repetidas entre lugares. Si dos lugares se parecen, busca el ángulo diferente.
- **Exactitud**: solo nombres de barrios, comunas, corregimientos, vías y municipios que existan.
  Si no estás seguro de un dato, no lo pongas. **No inventes estadísticas** ni cifras de robo,
  población o cantidad de vehículos. No digas que hay oficina o sede física en el lugar.
  No menciones competidores. No inventes testimonios. No pongas teléfonos ni precios distintos
  a los dos de arriba. No prometas recuperar vehículos; di que la ubicación en tiempo real
  se puede compartir con la Policía (línea 123) para facilitar la recuperación.
- En lugares con cobertura celular limitada fuera del casco urbano (Amazonía, Orinoquía,
  Pacífico, zonas rurales), dilo con honestidad: el GPS reporta donde haya cobertura celular y
  en tramos sin señal la ubicación se actualiza cuando el equipo la recupera.
- Longitudes: respétalas; son para que la página tenga contenido suficiente sin relleno.

## Esquema: lugar (municipio o capital)

```json
{
  "slug": "bello",
  "name": "Bello",
  "dept": "antioquia",
  "lat": 6.3373,
  "lon": -75.5580,
  "metro": "Área Metropolitana del Valle de Aburrá",
  "lead": "Frase de portada única, máx. 170 caracteres.",
  "intro": ["Párrafo 1 (70-110 palabras)", "Párrafo 2 (70-110 palabras)"],
  "uses": [
    {"icon": "🏍️", "title": "Máx. 45 caracteres", "text": "25-45 palabras"}
  ],
  "zones": ["8 a 14 barrios, comunas, sectores, corregimientos o veredas reales"],
  "roads": [{"name": "Vía o corredor real", "note": "15-30 palabras: por qué importa el GPS ahí"}],
  "install_note": "30-60 palabras: cómo se coordina la instalación en este lugar (único).",
  "faqs": [{"q": "Pregunta local real que haría un cliente de aquí", "a": "40-80 palabras"}],
  "nearby": ["slugs de la lista maestra, 3 a 5, cercanos geográficamente"]
}
```

- `metro`: nombre del área metropolitana si aplica; si no, `null`.
- `uses`: exactamente 4. `roads`: 3 o 4. `faqs`: exactamente 3. `zones`: 8 a 14.
- `nearby`: SOLO slugs de la lista maestra de abajo, nunca el propio.

## Esquema: departamento

```json
{
  "slug": "antioquia",
  "name": "Antioquia",
  "capital": "medellin",
  "iso": "CO-ANT",
  "lat": 6.2442,
  "lon": -75.5812,
  "lead": "Frase de portada única, máx. 170 caracteres.",
  "intro": ["3 párrafos de 70-110 palabras cada uno"],
  "subregions": [{"name": "Valle de Aburrá", "municipios": ["Medellín", "Bello", "Itagüí"]}],
  "roads": [{"name": "Vía real", "note": "15-30 palabras"}],
  "uses": [{"icon": "🚛", "title": "Máx. 45 caracteres", "text": "25-45 palabras"}],
  "faqs": [{"q": "Pregunta", "a": "40-80 palabras"}]
}
```

- `subregions`: 3 a 6 subregiones reales (las oficiales del departamento cuando existan), con
  3 a 8 municipios reales cada una, escritos con tildes exactamente como su nombre oficial.
  Incluye la capital y los municipios de la lista maestra que pertenezcan al departamento.
- `roads`: 4 o 5. `uses`: exactamente 4. `faqs`: exactamente 3.
- `capital`: slug de la capital en la lista maestra.

## Lista maestra de slugs de lugares (para `nearby` y `capital`)

Capitales: arauca, armenia, barranquilla, bogota, bucaramanga, cali, cartagena, cucuta,
florencia, ibague, leticia, manizales, medellin, mitu, mocoa, monteria, neiva, pasto, pereira,
popayan, puerto-carreno, puerto-inirida, quibdo, riohacha, san-andres, san-jose-del-guaviare,
santa-marta, sincelejo, tunja, valledupar, villavicencio, yopal.

Municipios: soacha, chia, zipaquira, facatativa, fusagasuga, girardot, mosquera, madrid, funza,
cajica (Cundinamarca); bello, itagui, envigado, rionegro, sabaneta, apartado, turbo, caucasia
(Antioquia); palmira, buenaventura, tulua, cartago, buga, jamundi, yumbo (Valle del Cauca);
soledad, malambo, sabanalarga (Atlántico); floridablanca, giron, piedecuesta, barrancabermeja,
san-gil (Santander); villa-del-rosario, los-patios, ocana, pamplona (Norte de Santander);
magangue, turbaco, el-carmen-de-bolivar (Bolívar); duitama, sogamoso, chiquinquira,
puerto-boyaca (Boyacá); dosquebradas, santa-rosa-de-cabal (Risaralda); calarca (Quindío);
la-dorada, chinchina (Caldas); espinal, melgar (Tolima); pitalito, garzon (Huila); acacias,
granada-meta, puerto-lopez (Meta); aguazul (Casanare); aguachica (Cesar); cienaga (Magdalena);
maicao (La Guajira); lorica, cerete, sahagun (Córdoba); corozal (Sucre); ipiales, tumaco
(Nariño); santander-de-quilichao (Cauca); puerto-asis (Putumayo); saravena, tame (Arauca);
san-vicente-del-caguan (Caquetá).

## Slugs de departamento

amazonas, antioquia, arauca, atlantico, bolivar, boyaca, caldas, caqueta, casanare, cauca,
cesar, choco, cordoba, cundinamarca, guainia, guaviare, huila, la-guajira, magdalena, meta,
narino, norte-de-santander, putumayo, quindio, risaralda, san-andres-y-providencia, santander,
sucre, tolima, valle-del-cauca, vaupes, vichada.

(Bogotá D.C. se trata dentro de Cundinamarca y tiene su propia página de ciudad.)
