#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate rmi_2026/pages/results.html (Day 1 ranking) from data/results_day1_2026.csv.

The CSV is the standings export of contest 1 (Rank, Username, First name, Last name,
Country, Team, <3 problem columns>, Total). Usernames are not published.

Usage:
    python scripts/generate_results_day1_2026.py
    python scripts/build_site.py        # wraps the fragment into rmi_2026/results.html
"""
import csv
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / 'data' / 'results_day1_2026.csv'
OUT_PATH = ROOT / 'rmi_2026' / 'pages' / 'results.html'
FLAGS_DIR = ROOT / 'rmi_2026' / 'assets' / 'flags'

# ISO code -> flag file name (without .svg) in rmi_2026/assets/flags
FLAG_NAMES = {
    'AZ': 'azerbaijan', 'BG': 'bulgaria', 'BR': 'brazil', 'GE': 'georgia', 'GR': 'greece',
    'HR': 'croatia', 'HU': 'hungary', 'IT': 'italy', 'MD': 'moldova', 'RO': 'romania',
    'RS': 'serbia', 'TR': 'turkey', 'UA': 'ukraine', 'VN': 'vietnam',
}

e = html.escape


def num(value):
    value = value.strip()
    return str(int(float(value))) if float(value) == int(float(value)) else value


def main():
    with open(CSV_PATH, encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        fixed = {'Rank', 'Username', 'First name', 'Last name', 'Country', 'Team', 'Total'}
        problems = [c for c in reader.fieldnames if c not in fixed]
        rows = [r for r in reader if r['Rank'].strip()]

    head = ''.join(f'<th>{e(p)}</th>' for p in problems)
    body = []
    for r in rows:
        code = r['Country'].strip().upper()
        flag = FLAG_NAMES.get(code)
        if flag and (FLAGS_DIR / f'{flag}.svg').exists():
            country = (f'<img src="assets/flags/{flag}.svg" alt="" class="country-flag" loading="lazy"> '
                       f'{e(code)}')
        else:
            country = e(code)
        name = f"{r['First name'].strip()} {r['Last name'].strip()}".strip()
        scores = ''.join(f'<td>{num(r[p])}</td>' for p in problems)
        body.append(
            f'              <tr><td><strong>{e(r["Rank"].strip())}</strong></td><td>{e(name)}</td>'
            f'<td class="country-cell">{country}</td><td>{e(r["Team"].strip())}</td>{scores}'
            f'<td><strong>{num(r["Total"])}</strong></td></tr>'
        )

    page = f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>Results</title>
    <link rel="canonical" href="https://rmi.lbi.ro/rmi_2026/">
    <link rel="stylesheet" href="assets/css/style.css">
    <style>
      .table-container {{ overflow-x: auto; }}
      .results-table td.country-cell {{ white-space: nowrap; }}
      .results-table .country-flag {{ display: inline-block; height: 14px; width: auto; vertical-align: middle; margin-right: .25rem; }}
      .results-table td, .results-table th {{ white-space: nowrap; }}
    </style>
  </head>
  <body>
    <button id="nav-toggle" class="nav-toggle" aria-controls="site-nav" aria-expanded="false">☰</button>
    <div class="container">
      <header class="site-header"><h1>Results</h1></header>
      <main class="content">
        <section class="results-section">
          <h2>Day 1 ranking</h2>
          <p>Standings after the first contest day (Thursday, November 19th, 2026): {len(rows)} contestants, {len(problems)} problems. Day 2 and the final results will be published after the contest days.</p>
          <div class="table-container">
            <table class="results-table">
              <thead><tr><th>Rank</th><th>Name</th><th>Country</th><th>Team</th>{head}<th>Day 1</th></tr></thead>
              <tbody>
{chr(10).join(body)}
              </tbody>
            </table>
          </div>
        </section>
      </main>
      <footer class="site-footer">&copy; 2026 Tudor Vianu National High School of Computer Science - Rares Anghel</footer>
    </div>
    <script src="assets/js/main.js"></script>
  </body>
</html>
'''
    OUT_PATH.write_text(page, encoding='utf-8')
    print(f'Wrote {OUT_PATH.relative_to(ROOT)}: {len(rows)} rows, problems: {", ".join(problems)}')


if __name__ == '__main__':
    main()
