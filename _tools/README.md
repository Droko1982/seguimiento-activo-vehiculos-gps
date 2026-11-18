# Herramientas del sitio gpscarro.com

Esta carpeta no se publica (GitHub Pages ignora las carpetas que empiezan por `_`).

## Reconstruir el sitio

```bash
python -I _tools/build_all.py
```

| Script | Qué genera |
|---|---|
| `build_locations.py` | Páginas de ciudades/municipios (`ciudades/`) y departamentos (`departamentos/`) a partir de `data/*.json` |
| `build_pillars.py` | `precios.html`, `preguntas-frecuentes.html` (todas las preguntas viven aquí) y `sobre-nosotros.html` |
| `enhance_pages.py` | Menú, footer y barra fija de WhatsApp/Llamar en las páginas escritas a mano |
| `build_index_files.py` | `sitemap.xml`, `llms.txt` y `llms-full.txt` (resúmenes para asistentes de IA) |
| `indexnow.py` | Avisa a Bing (ChatGPT/Copilot), Yandex y otros de URLs nuevas. Ejecutar **después** de publicar |
| `fix_meta.py`, `fix_schema.py` | Correcciones puntuales ya aplicadas (títulos/descripciones y schema de entidad única) |
| `og-image.html` | Fuente de `og-image.png` (imagen al compartir en WhatsApp/Facebook) |

## Cambiar datos del negocio

- Teléfono, precios y nombre: `site_common.py` (y luego `build_all.py`). Las páginas escritas a mano
  (inicio, servicios, industrias, blog) tienen los valores en su HTML: búscalos y reemplázalos.
- Contenido local de una ciudad o departamento: edita su entrada en `data/*.json` siguiendo
  `CONTENT-BRIEF.md` y ejecuta `build_all.py`.
- Las páginas generadas llevan el comentario `SA:GENERATED`: no las edites a mano.

## Imagen para redes (og-image.png)

```bash
chrome --headless=new --window-size=1200,630 --screenshot=og-image.png _tools/og-image.html
```
Luego comprimir a PNG de 256 colores (menos de 300 KB, que es el límite práctico de WhatsApp).
