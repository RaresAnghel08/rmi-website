#!/usr/bin/env python3
"""Build the static site: one real HTML file per route, plus sitemap.xml.

Routes are declared in rmi_2026/menu.json (`slug` per page; the empty slug is
the home page and is served at /rmi_2026/). Content is read from the fragments
in rmi_2026/pages/ (the files the results/participants generators and the
admin dashboard write), wrapped in the shared site shell and written to:

    rmi_2026/index.html        ->  /rmi_2026/
    rmi_2026/<slug>.html       ->  /rmi_2026/<slug>.html
    rmi_2026/sitemap.xml       ->  /rmi_2026/sitemap.xml

The site is deployed by uploading rmi_2026/ as a subfolder (rmi.lbi.ro/rmi_2026/)
on the legacy Apache host, same as every previous edition (rmi_2025/, rmi_2024/,
...). Asset and nav links are page-relative (no leading "/") so the pages work
unchanged regardless of the mount point; only fully-qualified URLs (canonical,
Open Graph, JSON-LD, sitemap) need the real BASE_PATH prefix.

Usage:
    python scripts/build_site.py           # regenerate pages + sitemap
    python scripts/build_site.py --serve   # ...then preview on :8000 with clean URLs
"""
import html
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE_DIR = ROOT / 'rmi_2026'
SITE_URL = 'https://rmi.lbi.ro'
BASE_PATH = '/rmi_2026'  # real, reachable mount point on the Apache host
SITE_NAME = 'Romanian Master of Informatics 2026'
ORG_NAME = 'Tudor Vianu National High School of Computer Science'
SOCIAL_IMAGE = f'{SITE_URL}{BASE_PATH}/assets/organisers/vianu.png'


def load_pages():
    """Return (menu, pages) where pages are menu items that have a route."""
    menu = json.loads((SITE_DIR / 'menu.json').read_text(encoding='utf-8'))
    menu.sort(key=lambda c: c.get('weight', 0))
    pages = [it for cat in menu for it in cat.get('items', []) if 'slug' in it]
    slugs = [p['slug'] for p in pages]
    if len(set(slugs)) != len(slugs):
        sys.exit('menu.json: duplicate slugs')
    if '' not in slugs:
        sys.exit('menu.json: no page with slug "" (the home page)')
    return menu, pages


def page_url(item):
    """Fully-qualified URL, for canonical/Open Graph/JSON-LD/sitemap only."""
    return f"{SITE_URL}{BASE_PATH}/{item['slug']}.html" if item['slug'] else f'{SITE_URL}{BASE_PATH}/'


def page_href(item):
    """Page-relative link: every generated page lives flat in rmi_2026/."""
    return f"{item['slug']}.html" if item['slug'] else 'index.html'


def output_file(item):
    return SITE_DIR / (f"{item['slug']}.html" if item['slug'] else 'index.html')


def extract_content(fragment_path):
    """Inline <style> blocks + inner HTML of <main class="content">."""
    text = fragment_path.read_text(encoding='utf-8')
    styles = ''.join(re.findall(r'<style\b.*?</style>', text, re.S | re.I))
    m = re.search(r'<main\b[^>]*class="[^"]*\bcontent\b[^"]*"[^>]*>', text)
    if m:
        end = text.rfind('</main>')
        body = text[m.end():end if end > m.end() else len(text)]
    else:
        body = text
    return styles, body.strip()


def render_nav(menu, current):
    out = []
    for cat in menu:
        out.append(f'          <h4>{html.escape(cat["name"])}</h4>')
        out.append('          <ul class="nav-group">')
        for it in cat.get('items', []):
            title = html.escape(it['title'])
            if 'slug' in it:
                is_cur = it['slug'] == current['slug']
                cls = ' class="active" aria-current="page"' if is_cur else ''
                out.append(f'            <li><a href="{page_href(it)}"{cls}>{title}</a></li>')
            elif 'url' in it:
                out.append(f'            <li><a href="{html.escape(it["url"])}" target="_blank" rel="noopener">{title}</a></li>')
        out.append('          </ul>')
    return '\n'.join(out)


def json_ld(item, is_home):
    org = {'@type': 'Organization', 'name': ORG_NAME, 'url': 'https://portal.lbi.ro',
           'logo': SOCIAL_IMAGE}
    if is_home:
        graph = [org, {
            '@type': 'Event',
            'name': SITE_NAME,
            'startDate': '2026-11-16',
            'endDate': '2026-11-20',
            'eventStatus': 'https://schema.org/EventScheduled',
            'eventAttendanceMode': 'https://schema.org/OfflineEventAttendanceMode',
            'location': {'@type': 'Place', 'name': ORG_NAME,
                         'address': {'@type': 'PostalAddress', 'addressLocality': 'Bucharest',
                                     'addressCountry': 'RO'}},
            'description': 'The 14th Romanian Master of Informatics (RMI 2026) in Bucharest, Romania.',
            'url': page_url(item),
            'organizer': {'@type': 'Organization', 'name': ORG_NAME, 'url': 'https://portal.lbi.ro'},
        }]
    else:
        graph = [{
            '@type': 'BreadcrumbList',
            'itemListElement': [
                {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': f'{SITE_URL}{BASE_PATH}/'},
                {'@type': 'ListItem', 'position': 2, 'name': item['title'], 'item': page_url(item)},
            ],
        }]
    data = json.dumps({'@context': 'https://schema.org', '@graph': graph}, indent=2, ensure_ascii=False)
    return data.replace('</', '<\\/')


def render_page(item, menu):
    is_home = item['slug'] == ''
    styles, body = extract_content((SITE_DIR / item['path']))
    url = page_url(item)
    desc = html.escape(item['description'], quote=True)
    if is_home:
        title = f'{SITE_NAME} (RMI 2026) | Bucharest, November 16-20'
        social_title = SITE_NAME
    else:
        title = f"{item['title']} | RMI 2026"
        social_title = f"{item['title']} | {SITE_NAME}"
    title, social_title = html.escape(title), html.escape(social_title, quote=True)

    # every page gets exactly one <h1>: the site title on home, the page title elsewhere
    site_title_tag = 'h1' if is_home else 'div'
    page_h1 = '' if is_home or re.search(r'<h1\b', body) else f'<h1>{html.escape(item["title"])}</h1>\n        '

    return f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="theme-color" content="#261C4A">

    <title>{title}</title>

    <meta name="description" content="{desc}">
    <meta name="robots" content="index, follow">
    <meta name="author" content="Colegiul Național de Informatică &#34;Tudor Vianu&#34;">
    <meta name="keywords" content="RMI, Romanian Master of Informatics, RMI 2026, informatics competition, Bucharest, Tudor Vianu">
    <link rel="canonical" href="{url}">
    <link rel="alternate" hreflang="en" href="{url}">

    <link rel="stylesheet" href="assets/css/style.css">

    <link rel="apple-touch-icon" sizes="180x180" href="apple-touch-icon.png">
    <link rel="icon" href="assets/organisers/vianu.png" type="image/png">
    <link rel="manifest" href="site.webmanifest">
    <meta name="msapplication-TileColor" content="#261C4A">

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">

    <script type="application/ld+json">
{json_ld(item, is_home)}
    </script>

    <meta property="og:type" content="website">
    <meta property="og:site_name" content="{SITE_NAME}">
    <meta property="og:title" content="{social_title}">
    <meta property="og:description" content="{desc}">
    <meta property="og:url" content="{url}">
    <meta property="og:image" content="{SOCIAL_IMAGE}">

    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{social_title}">
    <meta name="twitter:description" content="{desc}">
    <meta name="twitter:image" content="{SOCIAL_IMAGE}">
  </head>
  <body>
    <header class="site-header">
      <div class="container header-inner">
        <a href="index.html"><img src="static/assets/logo.svg" alt="RMI 2026 logo" class="logo"></a>
        <{site_title_tag} class="site-title">Romanian Master of Informatics</{site_title_tag}>
        <div class="organised-by">
          <div class="by-label">Organized By</div>
          <a href="https://portal.lbi.ro" target="_blank" rel="noopener">
            <img src="assets/organisers/vianu.png" alt="Tudor Vianu" class="vianu-logo">
          </a>
        </div>
      </div>
    </header>

    <div class="container layout">
      <button id="nav-toggle" class="nav-toggle" aria-controls="site-nav" aria-expanded="false" aria-label="Toggle navigation">☰</button>
      <nav id="site-nav" class="site-nav" aria-label="Main navigation">
        <div id="nav-list" class="nav-groups">
{render_nav(menu, item)}
        </div>
      </nav>

      <main id="content" class="content">
        <section id="rendered" class="rendered">
        {styles}{page_h1}{body}
        </section>
      </main>
    </div>

    <footer class="site-footer">&copy; 2026 {ORG_NAME} - Built by <a href="https://linkedin.com/in/raresanghel" target="_blank" rel="noopener" title="Visit Rares Anghel's LinkedIn profile">Rares Anghel</a></footer>

    <script src="assets/js/main.js" defer></script>
  </body>
</html>
'''


def lastmod(item):
    """Date the page's content last changed (git), falling back to the file mtime."""
    src = SITE_DIR / item['path']
    try:
        out = subprocess.run(['git', 'log', '-1', '--format=%cs', '--', str(src)],
                             cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
        if out:
            return out
    except (OSError, subprocess.CalledProcessError):
        pass
    return date.fromtimestamp(src.stat().st_mtime).isoformat()


def render_sitemap(pages):
    rows = []
    for it in pages:
        rows.append(
            '  <url>\n'
            f'    <loc>{html.escape(page_url(it))}</loc>\n'
            f'    <lastmod>{lastmod(it)}</lastmod>\n'
            f'    <changefreq>{it.get("changefreq", "monthly")}</changefreq>\n'
            f'    <priority>{it.get("priority", "0.5")}</priority>\n'
            '  </url>')
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + '\n'.join(rows) + '\n</urlset>\n')


def build():
    menu, pages = load_pages()
    for it in pages:
        output_file(it).write_text(render_page(it, menu), encoding='utf-8', newline='\n')
        print(f"  {page_href(it) if it['slug'] else '/':<14} <- {it['path']}")
    (SITE_DIR / 'sitemap.xml').write_text(render_sitemap(pages), encoding='utf-8', newline='\n')
    print(f'Built {len(pages)} pages + sitemap.xml')


def serve(port=8000):
    """Tiny preview server that mimics Vercel's clean URLs."""
    import http.server
    import os

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **kw):
            super().__init__(*a, directory=str(SITE_DIR), **kw)

        def translate_path(self, path):
            p = super().translate_path(path)
            if not os.path.exists(p) and not os.path.splitext(p)[1] and os.path.exists(p + '.html'):
                return p + '.html'
            return p

    print(f'Serving {SITE_DIR} at http://localhost:{port}/')
    http.server.ThreadingHTTPServer(('', port), Handler).serve_forever()


if __name__ == '__main__':
    build()
    if '--serve' in sys.argv:
        serve()
