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
OUT_PATH = os.path.join(ROOT, 'pages', 'participants.html')


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

        # group rows by team (use 'No team' if unspecified)
        teams = {}
        for r in rows:
                team = r['team'] or 'No team'
                teams.setdefault(team, []).append(r)

        rows_html = []
        for team_name in sorted(teams.keys()):
                members = teams[team_name]

                # representative country for the flag (first non-empty)
                rep_country = ''
                for m in members:
                        if m.get('country'):
                                rep_country = m['country']
                                break
                key = rep_country.lower() if rep_country else ''
                flag_html = ''
                if key in flags:
                        flag_html = f'<img src="{flags[key]}" alt="{html.escape(rep_country)}"/>'

                # categorize leaders and students
                leaders = [m for m in members if (m.get('role') or '').lower().strip() in ('lider', 'leader')]
                students = [m for m in members if m not in leaders]

                # build team block
                rows_html.append('            <div class="team-block">')
                rows_html.append('              <div class="team-header">')
                rows_html.append(f'                <div class="team-flag">{flag_html}</div>')
                rows_html.append(f'                <div class="team-name">{html.escape(team_name)}</div>')
                rows_html.append('              </div>')

                # leaders (inline)
                if leaders:
                        leader_names = ', '.join(html.escape(l['name']) for l in leaders if l.get('name'))
                        rows_html.append(f'              <div class="team-leaders"><strong>Leaders:</strong> <span class="member-list">{leader_names}</span></div>')
                else:
                        rows_html.append('              <div class="team-leaders"><strong>Leaders:</strong> <span class="none">—</span></div>')

                # students (inline)
                if students:
                        student_names = ', '.join(html.escape(s['name']) for s in students if s.get('name'))
                        rows_html.append(f'              <div class="team-students"><strong>Students:</strong> <span class="member-list">{student_names}</span></div>')
                else:
                        rows_html.append('              <div class="team-students"><strong>Students:</strong> <span class="none">—</span></div>')

                rows_html.append('            </div>')

        tail = '''
                    </div>
                </section>
            </main>
            <footer class="site-footer">&copy; RMI</footer>
        </div>
        <link rel="icon" href="/assets/organisers/vianu.png" type="image/png">
        <script src="/assets/js/main.js"></script>
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
