#!/usr/bin/env python3
"""Generate pages/participants.html from csv/2025_cleaned_registrations.csv

Reads available flag SVGs from assets/flags and uses them when country names match the filename.
"""
import csv
import os
import html

ROOT = os.path.dirname(os.path.dirname(__file__))
CSV_PATH = os.path.join(ROOT, 'rmi_2025', 'csv', '2025_cleaned_registrations.csv')
FLAGS_DIR = os.path.join(ROOT, 'rmi_2025', 'assets', 'flags')
OUT_PATH = os.path.join(ROOT, 'rmi_2025', 'pages', 'participants.html')


def load_flags():
    flags = {}
    if not os.path.isdir(FLAGS_DIR):
        return flags
    for fn in os.listdir(FLAGS_DIR):
        if fn.lower().endswith('.svg'):
            name = os.path.splitext(fn)[0].lower()
            flags[name] = 'assets/flags/' + fn
    return flags


def read_csv():
    rows = []
    with open(CSV_PATH, 'r', encoding='utf-8') as fh:
        reader = csv.reader(fh)
        header = next(reader)  # Skip header
        for r in reader:
            if not r or len(r) < 14:
                continue
            country = r[0].strip()
            team = r[1].strip()
            # Leader
            first = r[2].strip()
            last = r[3].strip()
            if first or last:
                name = f"{first} {last}".strip()
                rows.append({'name': name, 'team': team, 'country': country, 'role': 'leader'})
            # Deputy
            first = r[4].strip()
            last = r[5].strip()
            if first or last:
                name = f"{first} {last}".strip()
                rows.append({'name': name, 'team': team, 'country': country, 'role': 'leader'})
            # Contestants
            for i in range(6, 14, 2):
                first = r[i].strip()
                last = r[i+1].strip()
                if first or last:
                    name = f"{first} {last}".strip()
                    rows.append({'name': name, 'team': team, 'country': country, 'role': ''})
    return rows


def generate_html(rows, flags):
        head = '''<!doctype html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width,initial-scale=1">
        <title>Participants</title>
        <link rel="stylesheet" href="assets/css/style.css">
    </head>
    <body>
        <div class="container">
            <header class="site-header"><h1>Participants</h1></header>
            <main class="content">
                <section class="participants-section">
                    <h2>Participants</h2>
                    <div class="participants-grid">
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
                key = rep_country.lower().split(' (')[0] if rep_country else ''
                flag_html = ''
                if key in flags:
                        flag_html = f'<img src="{flags[key]}" alt="{html.escape(rep_country)}" class="flag-img"/>'

                # categorize leaders and students
                leaders = [m for m in members if (m.get('role') or '').lower().strip() in ('lider', 'leader')]
                students = [m for m in members if m not in leaders]

                # build team card
                rows_html.append('            <div class="team-card">')
                rows_html.append(f'              <div class="team-flag-header">{flag_html}</div>')
                rows_html.append(f'              <div class="team-name">{html.escape(team_name)}</div>')
                rows_html.append('              <div class="team-info">')

                # leaders (each on separate line)
                rows_html.append('                <div class="team-leaders">')
                rows_html.append('                  <span class="label">Leaders:</span>')
                if leaders:
                        rows_html.append('                  <div class="member-list">')
                        for leader in leaders:
                                if leader.get('name'):
                                        rows_html.append(f'                    <div class="member-item">{html.escape(leader["name"])}</div>')
                        rows_html.append('                  </div>')
                else:
                        rows_html.append('                  <span class="none">—</span>')
                rows_html.append('                </div>')

                # students (each on separate line)
                rows_html.append('                <div class="team-students">')
                rows_html.append('                  <span class="label">Students:</span>')
                if students:
                        rows_html.append('                  <div class="member-list">')
                        for student in students:
                                if student.get('name'):
                                        rows_html.append(f'                    <div class="member-item">{html.escape(student["name"])}</div>')
                        rows_html.append('                  </div>')
                else:
                        rows_html.append('                  <span class="none">—</span>')
                rows_html.append('                </div>')

                rows_html.append('              </div>')
                rows_html.append('            </div>')

        tail = '''
                    </div>
                </section>
            </main>
            <footer class="site-footer">&copy; 2025 Tudor Vianu National High School of Computer Science - Built by <a href="https://linkedin.com/in/raresanghel" target="_blank" rel="noopener" title="Visit Rares Anghel's LinkedIn profile">Rares Anghel</a></footer>
        </div>
        <link rel="icon" href="assets/organisers/vianu.png" type="image/png">
        <script src="assets/js/main.js"></script>
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
    print(f'Wrote {OUT_PATH} ({len(rows)} members, {len(flags)} flags available)')


if __name__ == '__main__':
    main()