"""Rebuild every generated part of gpscarro.com, in the right order.

  python -I _tools/build_all.py

1. build_locations.py   -> ciudades/*, departamentos/* (from _tools/data/*.json)
2. build_pillars.py     -> precios.html, preguntas-frecuentes.html, sobre-nosotros.html
3. enhance_pages.py     -> shared nav, footer and mobile WhatsApp/call bar on hand-written pages
4. build_index_files.py -> sitemap.xml, llms.txt, llms-full.txt

After publishing (git push to master), notify Bing/IndexNow:
  python -I _tools/indexnow.py
"""
import os
import runpy

HERE = os.path.dirname(os.path.abspath(__file__))
for script in ("build_locations.py", "build_pillars.py", "enhance_pages.py", "build_index_files.py"):
    print(f"== {script}")
    runpy.run_path(os.path.join(HERE, script), run_name="__main__")
