#!/usr/bin/env python3
"""Generate pages/contest/participants.html from csv/teams.csv

Reads available flag SVGs from assets/flags and uses them when country names match the filename.
"""
import csv
import os
import html

ROOT = os.path.dirname(os.path.dirname(__file__))
CSV_PATH = os.path.join(ROOT, 'csv', 'teams.csv')
FLAGS_DIR = os.path.join(ROOT, 'assets', 'flags')
OUT_PATH = os.path.join(ROOT, 'pages', 'contest', 'participants.html')


def load_flags():
    flags = {}
    if not os.path.isdir(FLAGS_DIR):
        return flags
    for fn in os.listdir(FLAGS_DIR):
        if fn.lower().endswith('.svg'):
            name = os.path.splitext(fn)[0].lower()
            flags[name] = '/assets/flags/' + fn
    return flags


def read_csv():
    rows = []
    with open(CSV_PATH, 'r', encoding='utf-8') as fh:
        reader = csv.reader(fh)
        for r in reader:
            # Expecting: name, ?, team, country, role
            if not r:
                continue
            # pad to 5
            while len(r) < 5:
                r.append('')
            name = r[0].strip()
            team = r[2].strip()
            country = r[3].strip()
            role = r[4].strip()
            # skip completely empty rows
            if not (name or team or country or role):
                continue
            rows.append({'name': name, 'team': team, 'country': country, 'role': role})
    return rows


def generate_html(rows, flags):
    head = '''<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>Participants</title>
    <link rel="stylesheet" href="/assets/css/style.css">
  </head>
  <body>
    <div class="container">
      <header class="site-header"><h1>Participants</h1></header>
      <main class="content">
        <section class="participants-section">
          <h2>Participants</h2>
          <div class="participants-list">
'''

    # group rows by team (use empty string for unspecified team)
    teams = {}
    for r in rows:
        team = r['team'] or 'No team'
        teams.setdefault(team, []).append(r)

    rows_html = []
    for team_name in sorted(teams.keys()):
        members = teams[team_name]
        # pick a representative country for the flag (first non-empty)
        rep_country = ''
        for m in members:
            if m['country']:
                rep_country = m['country']
                break
        key = rep_country.lower() if rep_country else ''
        flag_html = ''
        if key in flags:
            flag_html = f'<img src="{flags[key]}" alt="{html.escape(rep_country)}"/>'

        # Leaders and Students
        leaders = [m for m in members if (m['role'] or '').lower().strip() in ('lider','leader')]
        students = [m for m in members if m not in leaders]

        # Team header: flag + team name
        rows_html.append(f'            <div class="team-block">')
        rows_html.append(f'              <div class="team-header">')
        rows_html.append(f'                <div class="team-flag">{flag_html}</div>')
        rows_html.append(f'                <div class="team-name">{html.escape(team_name)}</div>')
        rows_html.append(f'              </div>')

        # Leaders (inline comma-separated)
        rows_html.append(f'              <div class="team-leaders"><strong>Leaders:</strong> ')
        if leaders:
            leader_names = ', '.join(html.escape(l['name']) for l in leaders if l['name'])
            rows_html.append('                <span class="member-list">' + leader_names + '</span>')
        else:
            rows_html.append('                <span class="none">—</span>')
        rows_html.append('              </div>')

        # Students (inline comma-separated)
        rows_html.append(f'              <div class="team-students"><strong>Students:</strong> ')
        if students:
            student_names = ', '.join(html.escape(s['name']) for s in students if s['name'])
            rows_html.append('                <span class="member-list">' + student_names + '</span>')
        else:
            rows_html.append('                <span class="none">—</span>')
        rows_html.append('              </div>')

        rows_html.append('            </div>')

    tail = '''
          </div>
        </section>
      </main>
      <footer class="site-footer">&copy; RMI</footer>
    </div>
  </body>
</html>
'''

    return head + "\n".join(rows_html) + tail


def main():
    flags = load_flags()
    rows = read_csv()
    html_out = generate_html(rows, flags)
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, 'w', encoding='utf-8') as fh:
        fh.write(html_out)
    print(f'Wrote {OUT_PATH} ({len(rows)} rows, {len(flags)} flags available)')


if __name__ == '__main__':
    main()
