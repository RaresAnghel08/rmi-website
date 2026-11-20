#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate rmi_2026/pages/results.html (final ranking) from
data/results_aggregate_2026.csv (Rank, Username, names, Day 2, Day 1, Aggregate),
data/results_day1_2026.csv and data/results_day2_2026.csv (per-problem scores, country, team).

Equal aggregates share the same place. Medals follow the Competition Rules and go to on-site
contestants only (cutoffs computed on the on-site scoreboard):
  gold   = largest score with at least 1/12 of on-site contestants at or above it
  silver = largest score with at least 1/4 of on-site contestants at or above it
  bronze = smallest score with at most 1/2 of on-site contestants at or above it
The RMI Cup (team ranking) = sum of the best three on-site scores of a team; also written to RMI_Cup_2026.md.
Usernames are not published.

Usage:
    python scripts/generate_results_final_2026.py
    python scripts/build_site.py
"""
import csv
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / 'data'
OUT_PATH = ROOT / 'rmi_2026' / 'pages' / 'results.html'
FLAGS_DIR = ROOT / 'rmi_2026' / 'assets' / 'flags'
FLAG_NAMES = {
    'AZ': 'azerbaijan', 'BG': 'bulgaria', 'BR': 'brazil', 'GE': 'georgia', 'GR': 'greece',
    'HR': 'croatia', 'HU': 'hungary', 'IT': 'italy', 'MD': 'moldova', 'RO': 'romania',
    'RS': 'serbia', 'TR': 'turkey', 'UA': 'ukraine', 'VN': 'vietnam',
}
e = html.escape


def read(name):
    with open(DATA / name, encoding='utf-8-sig', newline='') as f:
        r = csv.DictReader(f)
        return r.fieldnames, [x for x in r if x['Rank'].strip()]


def num(v):
    f = round(float(v), 1)
    return str(int(f)) if f == int(f) else str(f)


def main():
    _, agg = read('results_aggregate_2026.csv')
    f1, d1 = read('results_day1_2026.csv')
    f2, d2 = read('results_day2_2026.csv')
    fixed = {'Rank', 'Username', 'First name', 'Last name', 'Country', 'Team', 'Total'}
    p1 = [c for c in f1 if c not in fixed]
    p2 = [c for c in f2 if c not in fixed]
    d1 = {r['Username']: r for r in d1}
    d2 = {r['Username']: r for r in d2}

    rows = []
    for a in agg:
        u = a['Username']
        i1, i2 = d1.get(u), d2.get(u)
        info = i1 or i2
        if not info:
            raise SystemExit(f'No country/team for {u}')
        rows.append({
            'u': u, 'info': info, 'agg': float(a['Aggregate']),
            's1': [i1[p] if i1 else '0' for p in p1],
            's2': [i2[p] if i2 else '0' for p in p2],
            'day1': float(a['Day 1']), 'day2': float(a['Day 2']),
        })
    rows.sort(key=lambda r: -r['agg'])
    prev = None
    place = 0
    for i, r in enumerate(rows, 1):
        if r['agg'] != prev:
            place, prev = i, r['agg']
        r['place'] = place
        r['onsite'] = r['u'].upper().startswith('RMI')

    # Medal cutoffs from the on-site scoreboard
    on = [r['agg'] for r in rows if r['onsite']]
    N = len(on)
    cnt = lambda sc: sum(1 for x in on if x >= sc)
    distinct = sorted(set(on), reverse=True)
    gold_cut = next(sc for sc in distinct if cnt(sc) >= N / 12)
    silver_cut = next(sc for sc in distinct if cnt(sc) >= N / 4)
    bronze_cut = 49.1  # set by the organizers (the strict 1/2 rule would give 50.6)
    for r in rows:
        a = r['agg']
        r['medal'] = '' if not r['onsite'] else 'gold' if a >= gold_cut else 'silver' if a >= silver_cut else 'bronze' if a >= bronze_cut else ''
    medals = {m: sum(1 for r in rows if r['medal'] == m) for m in ('gold', 'silver', 'bronze')}

    # RMI Cup: team score = sum of best three on-site scores
    teams = {}
    for r in rows:
        if r['onsite']:
            name = f"{r['info']['First name'].strip()} {r['info']['Last name'].strip()}".strip()
            teams.setdefault((r['info']['Team'].strip(), r['info']['Country'].strip().upper()), []).append((r['agg'], name))
    team_rows = []
    for (t, c), m in teams.items():
        m.sort(key=lambda x: -x[0])
        team_rows.append((round(sum(x for x, _ in m[:3]), 1), t, c, m[:3], len(m)))
    team_rows.sort(key=lambda x: -x[0])
    tprev, tplace = None, 0
    team_places = []
    for i, tr in enumerate(team_rows, 1):
        if tr[0] != tprev:
            tplace, tprev = i, tr[0]
        team_places.append(tplace)

    head = (''.join(f'<th>{e(p)}</th>' for p in p1) + '<th>Day 1</th>'
            + ''.join(f'<th>{e(p)}</th>' for p in p2) + '<th>Day 2</th>')
    body, counts = [], {'onsite': 0, 'online': 0}
    for r in rows:
        info = r['info']
        code = info['Country'].strip().upper()
        flag = FLAG_NAMES.get(code)
        if flag and (FLAGS_DIR / f'{flag}.svg').exists():
            country = f'<img src="assets/flags/{flag}.svg" alt="" class="country-flag" loading="lazy"> {e(code)}'
        else:
            country = e(code)
        name = f"{info['First name'].strip()} {info['Last name'].strip()}".strip()
        mode = 'online' if r['u'].upper().startswith('ONLINE') else 'onsite'
        counts[mode] += 1
        cls = f' class="name-{r["medal"]}"' if r['medal'] else ''
        scores = (''.join(f'<td>{num(v)}</td>' for v in r['s1']) + f'<td><strong>{num(r["day1"])}</strong></td>'
                  + ''.join(f'<td>{num(v)}</td>' for v in r['s2']) + f'<td><strong>{num(r["day2"])}</strong></td>')
        body.append(
            f'              <tr data-mode="{mode}" data-total="{r["agg"]}"><td class="rank-cell"><strong>{r["place"]}</strong></td>'
            f'<td><span{cls}>{e(name)}</span></td><td class="country-cell">{country}</td><td>{e(info["Team"].strip())}</td>'
            f'{scores}<td><strong>{num(r["agg"])}</strong></td></tr>')

    team_body = []
    for tp, (sc, t, c, m, size) in zip(team_places, team_rows):
        note = ' <em>(fewer than 3 contestants)</em>' if size < 3 else ''
        who = ', '.join(f'{e(nm)} ({num(x)})' for x, nm in m)
        team_body.append(f'              <tr><td class="rank-cell"><strong>{tp}</strong></td><td>{e(t)}{note}</td><td>{e(c)}</td><td><strong>{num(sc)}</strong></td><td>{who}</td></tr>')

    md = ['# RMI Cup 2026', '', '## Rule (from the Official Competition Rules)', '',
          '> Team score = sum of the best three individual scores. The top on-site team wins the RMI Cup.', '',
          'Computed on on-site contestants only, grouped by team; team score = sum of the three highest totals (Day 1 + Day 2).', '',
          '## Ranking', '', '| Place | Team | Country | Score | Counted contestants |', '|---|---|---|---|---|']
    for tp, (sc, t, c, m, size) in zip(team_places, team_rows):
        note = ' *(fewer than 3 contestants)*' if size < 3 else ''
        md.append(f"| {tp} | {t}{note} | {c} | **{num(sc)}** | " + ', '.join(f'{nm} ({num(x)})' for x, nm in m) + ' |')
    md += ['', f'**Winner: {team_rows[0][1]} ({team_rows[0][2]}) with {num(team_rows[0][0])} points.**', '']
    (ROOT / 'RMI_Cup_2026.md').write_text(chr(10).join(md), encoding='utf-8')

    n = len(rows)
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
          <h2>Final ranking</h2>
          <p>Final standings of RMI 2026 (Day 1 + Day 2): {n} contestants, {len(p1) + len(p2)} problems. Medals are awarded to on-site contestants only: gold from {num(gold_cut)} points ({medals['gold']} medals), silver from {num(silver_cut)} ({medals['silver']}), bronze from {num(bronze_cut)} ({medals['bronze']}).</p>
          <div class="results-filter" id="results-filter" role="group" aria-label="Filter by participation" hidden>
            <button type="button" class="filter-btn is-active" data-filter="all" aria-pressed="true">All ({n})</button>
            <button type="button" class="filter-btn" data-filter="onsite" aria-pressed="false">On-site ({counts['onsite']})</button>
            <button type="button" class="filter-btn" data-filter="online" aria-pressed="false">Online ({counts['online']})</button>
          </div>
          <p class="results-count" id="results-count" aria-live="polite"></p>
          <div class="table-container">
            <table class="results-table">
              <thead><tr><th>Rank</th><th>Name</th><th>Country</th><th>Team</th>{head}<th>Total</th></tr></thead>
              <tbody>
{chr(10).join(body)}
              </tbody>
            </table>
          </div>
        </section>
        <section class="results-section">
          <h2>RMI Cup &ndash; team ranking</h2>
          <p>Team score = sum of the best three individual scores of the on-site team members. The top on-site team wins the RMI Cup.</p>
          <div class="table-container">
            <table class="results-table">
              <thead><tr><th>Rank</th><th>Team</th><th>Country</th><th>Score</th><th>Counted contestants</th></tr></thead>
              <tbody>
{chr(10).join(team_body)}
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
    print(f'Wrote {OUT_PATH.relative_to(ROOT)}: {n} rows')


if __name__ == '__main__':
    main()
