#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate rmi_2026/pages/results.html (final ranking) from
data/results_aggregate_2026.csv (Rank, Username, names, Day 2, Day 1, Aggregate),
data/results_day1_2026.csv and data/results_day2_2026.csv (per-problem scores, country, team).

Columns: Rank, Name (team under the name), Country, Total, Day 1, Day 2, Day 1 problems, Day 2 problems; Rank and Name
stay fixed on the left when the table is scrolled sideways.
Equal aggregates share the same place. Medals go to every contestant, on-site and online,
by total score (cutoffs set by the organizers):
  gold   = total >= 125
  silver = total >= 79
  bronze = total >= 49.1
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

    # Medal cutoffs set by the organizers; they apply to everyone, on-site and online
    gold_cut = 125
    silver_cut = 79
    bronze_cut = 49.1
    for r in rows:
        a = r['agg']
        r['medal'] = 'gold' if a >= gold_cut else 'silver' if a >= silver_cut else 'bronze' if a >= bronze_cut else ''
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

    # Column order: Rank, Name (team under the name), Country, Total, Day 1, Day 2, Day 1 problems, Day 2 problems.
    # The team sits under the name (no separate column) so Total, Day 1 and Day 2 fit without scrolling,
    # on laptops (content area is ~736px wide) and on phones (country is a flag only there);
    # the per-problem scores are to the right.
    # main.js stretches Country, Total, Day 1 and Day 2 to fill the visible width, so the problem columns start
    # exactly at the right edge (a problem score never shows up half-visible: scroll to see them, or see none).
    # The empty spacer column only absorbs rounding leftovers.
    head = ('<th>Total</th><th>Day 1</th><th class="col-day2">Day 2</th><th class="col-spacer"><div class="spacer-box"></div></th>'
            + ''.join(f'<th class="prob">{e(p)}</th>' for p in p1) + ''.join(f'<th class="prob">{e(p)}</th>' for p in p2))
    body, counts = [], {'onsite': 0, 'online': 0}
    for r in rows:
        info = r['info']
        code = info['Country'].strip().upper()
        flag = FLAG_NAMES.get(code)
        if flag and (FLAGS_DIR / f'{flag}.svg').exists():
            country = f'<img src="assets/flags/{flag}.svg" alt="" class="country-flag" loading="lazy"> <span class="cc">{e(code)}</span>'
        else:
            country = f'<span class="cc cc-keep">{e(code)}</span>'
        name = f"{info['First name'].strip()} {info['Last name'].strip()}".strip()
        mode = 'online' if r['u'].upper().startswith('ONLINE') else 'onsite'
        counts[mode] += 1
        cls = f' class="name-{r["medal"]}"' if r['medal'] else ''
        scores = (f'<td><strong>{num(r["agg"])}</strong></td><td><strong>{num(r["day1"])}</strong></td>'
                  f'<td><strong>{num(r["day2"])}</strong></td><td class="col-spacer"></td>'
                  + ''.join(f'<td>{num(v)}</td>' for v in r['s1']) + ''.join(f'<td>{num(v)}</td>' for v in r['s2']))
        team = e(info['Team'].strip())
        body.append(
            f'              <tr data-mode="{mode}" data-total="{r["agg"]}"><td class="rank-cell col-rank"><strong>{r["place"]}</strong></td>'
            f'<td class="col-name"><span{cls}>{e(name)}</span><small class="team-sub">{team}</small></td>'
            f'<td class="country-cell" title="{e(code)}">{country}</td>{scores}</tr>')

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
      .results-main {{ overflow: visible !important; }} /* the theme's overflow:hidden would make the table its own scroll box and break sticky */
      /* Rank and Name stay visible while the table is scrolled sideways (opaque background so cells slide under them) */
      .results-main th.col-rank, .results-main td.col-rank {{ position: sticky; left: 0; z-index: 2; width: 3.25rem; min-width: 3.25rem; box-sizing: border-box; background: #fff !important; }}
      .results-main th.col-name, .results-main td.col-name {{ position: sticky; left: 3.25rem; z-index: 2; background: #fff !important; box-shadow: 1px 0 0 rgba(0,0,0,.08); }}
      .results-table.results-main .col-spacer {{ padding: 0 !important; border: 0 !important; min-width: 0; }}
      .results-main td.col-name {{ white-space: normal; }}
      .results-main .team-sub {{ display: block; font-size: .78rem; line-height: 1.25; color: #6b7280; margin-top: .1rem; }}
      /* Phones: Rank, Name, Country (flag only), Total, Day 1 and Day 2 fit without scrolling */
      @media (max-width: 600px) {{
        .results-table.results-main th, .results-table.results-main td {{ padding: .5rem .25rem !important; font-size: .88rem; }}
        .results-main th.col-rank, .results-main td.col-rank {{ width: 2.4rem; min-width: 2.4rem; }}
        .results-main th.col-name, .results-main td.col-name {{ left: 2.4rem; }}
        .results-main td.col-name {{ white-space: normal; width: 5rem; min-width: 5rem; max-width: 5rem; }}
        .results-main .team-sub {{ font-size: .72rem; line-height: 1.2; }}
        .results-main .cc:not(.cc-keep) {{ display: none; }}
        .results-main .country-flag {{ margin-right: 0 !important; }}
      }}
    </style>
  </head>
  <body>
    <button id="nav-toggle" class="nav-toggle" aria-controls="site-nav" aria-expanded="false">☰</button>
    <div class="container">
      <header class="site-header"><h1>Results</h1></header>
      <main class="content">
        <section class="results-section">
          <h2>Final ranking</h2>
          <div class="results-filter" id="results-filter" role="group" aria-label="Filter by participation" hidden>
            <button type="button" class="filter-btn is-active" data-filter="all" aria-pressed="true">All ({n})</button>
            <button type="button" class="filter-btn" data-filter="onsite" aria-pressed="false">On-site ({counts['onsite']})</button>
            <button type="button" class="filter-btn" data-filter="online" aria-pressed="false">Online ({counts['online']})</button>
          </div>
          <p class="results-count" id="results-count" aria-live="polite"></p>
          <div class="table-container">
            <table class="results-table results-main">
              <thead><tr><th class="col-rank">Rank</th><th class="col-name">Name</th><th>Country</th>{head}</tr></thead>
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
