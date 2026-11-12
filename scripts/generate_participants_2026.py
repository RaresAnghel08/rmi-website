#!/usr/bin/env python3
"""Build the RMI 2026 participants page.

Two steps, both done by this script:

1. IMPORT (only when the raw registration exports change)

       python scripts/generate_participants_2026.py \
           --registrations path/to/international_form.csv \
           --ro-regional   path/to/romanian_regional_form.csv

   Either option can be used alone: each one replaces only the teams that came
   from that form (column `source`) and keeps the teams from the other form.
   Pass the *complete* export each time (not just the new rows).

   Reads the raw Google-Form exports, repairs them (mojibake, typos in country
   names, duplicate submissions, ...) and writes data/participants_2026.csv.
   Only public information is kept (names, team, country, type, participation);
   e-mails, phone numbers, T-shirt sizes and free-text notes are dropped, so the
   normalised file can be committed. Keep the raw exports out of the repository.

2. GENERATE (always)

   Reads data/participants_2026.csv and writes rmi_2026/pages/participants.html.
   Then run `python scripts/build_site.py` to produce rmi_2026/participants.html.

Edit data/participants_2026.csv by hand for late changes, then re-run the script.
"""
import argparse
import csv
import html
import io
import sys
from collections import Counter, OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_CSV = ROOT / 'data' / 'participants_2026.csv'
FLAGS_DIR = ROOT / 'rmi_2026' / 'assets' / 'flags'
OUT_PATH = ROOT / 'rmi_2026' / 'pages' / 'participants.html'

FIELDS = ['country', 'type', 'participation', 'team', 'leader', 'deputy',
          'contestant1', 'contestant2', 'contestant3', 'contestant4', 'contestant5', 'source']

# Spellings found in the registration forms -> display name.
COUNTRY_ALIASES = {
    'bulgaira': 'Bulgaria',
    'hrvatska': 'Croatia',
    'moldova, republic of': 'Moldova',
    'republica moldova': 'Moldova',
    'romania': 'Romania',
    'românia': 'Romania',
    'turkiye': 'Türkiye',
    'türkiye': 'Türkiye',
    'turkey': 'Türkiye',
}
# Display name -> flag file (without .svg) when it differs from the lower-cased name.
FLAG_FILES = {'Türkiye': 'turkey'}

# Romanian regional centres have no "team name" in their form: name them after the city.
# Explicit order of the national teams inside a country (listed teams come first, in this
# order; everything else follows: remaining national teams, then regional ones, alphabetically).
TEAM_ORDER = {
    'Romania': ['Romania 1', 'Romania 2', 'Romania 3', 'Romania 4',
                'Romania - Girls Senior', 'Romania Juniors 1', 'Romania Juniors 2',
                'Romania - Girls Junior'],
}

# Contestants that are not in the participant fields of the Romanian regional form
# (e.g. only mentioned in the free-text notes), keyed by county. Added after the form's contestants.
RO_EXTRA_CONTESTANTS = {
    'Dolj': ['Grigorie Radu-Ștefan'],
}

RO_CENTRE_TEAM = {'Dolj': 'Craiova', 'Suceava': 'Suceava', 'Prahova': 'Ploiești - CNMV',
                  'Gorj': 'Târgu Jiu', 'Neamț': 'Piatra Neamț', 'Hunedoara': 'Orăștie'}


# --------------------------------------------------------------------------- import

def fix_mojibake(text):
    """Undo UTF-8 text that was decoded as cp1252 and saved again as UTF-8."""
    raw = bytearray()
    for ch in text:
        try:
            raw += ch.encode('cp1252')
        except UnicodeEncodeError:
            if ord(ch) > 255:
                return text  # genuinely non-latin text, leave it
            raw.append(ord(ch))
    try:
        return raw.decode('utf-8')
    except UnicodeDecodeError:
        return text


def read_export(path):
    text = Path(path).read_text(encoding='utf-8-sig', newline='')
    reader = csv.DictReader(io.StringIO(text))
    reader.fieldnames = [fix_mojibake(h) for h in reader.fieldnames]
    return [{k: fix_mojibake((v or '').strip()) for k, v in row.items() if k} for row in reader]


def clean_name(name):
    name = ' '.join(name.split())
    # Romanian cedilla forms -> the correct comma-below letters
    name = name.translate(str.maketrans('şŞţŢ', 'șȘțȚ'))
    # SURNAME Given-name -> Surname Given-name (also fully upper-case names)
    return ' '.join(w.title() if len(w) > 2 and w.isupper() else w for w in name.split())


def clean_country(name):
    name = name.strip()
    return COUNTRY_ALIASES.get(name.lower(), name)


def clean_team(name, country):
    name = ' '.join(name.split()).translate(str.maketrans('şŞţŢ', 'șȘțȚ'))
    prefix = country + '_'
    return name.replace('_', ' ', 1) if name.startswith(prefix) else name  # Georgia_Team 1 -> Georgia Team 1


def parse_timestamp(ts):
    from datetime import datetime
    for fmt in ('%d/%m/%Y %H:%M:%S', '%m/%d/%Y %H:%M:%S', '%m-%d-%Y %H:%M:%S'):
        try:
            return datetime.strptime(ts, fmt)
        except ValueError:
            pass
    return datetime.min


def default_type(row, country):
    # The form sometimes leaves "Type" empty; such teams (e.g. Bucharest 1/2) are regional.
    print(f"  '{row['Team name']}' ({country}) has no Type in the form: using Regional", file=sys.stderr)
    return 'Regional'


def import_international(path):
    teams = OrderedDict()
    for row in read_export(path):
        if not row.get('Team name') or not row.get('Country'):
            continue  # blank / stray lines at the end of the export
        country = clean_country(row['Country'])
        leader = clean_name(row.get('Team leader name', ''))
        if '@' in leader:  # a submission where the e-mail was typed into the name field
            leader = clean_name(row.get('Contact person (name)', ''))
        team = {
            'country': country,
            'type': row['Type'].strip().title() or default_type(row, country),
            'participation': row['Participation'].strip(),
            'team': clean_team(row['Team name'], country),
            'leader': leader,
            'deputy': clean_name(row.get('Deputy leader name', '')),
        }
        for i in range(1, 5):
            team[f'contestant{i}'] = clean_name(row.get(f'Participant {i} (name)', ''))
        team['source'] = 'international'
        team['_ts'] = parse_timestamp(row['Timestamp'])
        key = (country.lower(), team['team'].lower())
        if key in teams:
            print(f"  duplicate submission for '{team['team']}' ({country}): keeping the latest one",
                  file=sys.stderr)
            if team['_ts'] < teams[key]['_ts']:
                continue
        teams[key] = team
    return list(teams.values())


def import_ro_regional(path):
    teams = []
    for row in read_export(path):
        county = row.get('Județ', '')
        if not county:
            continue
        contestants = [clean_name(row.get(f'Participant {i}', '')) for i in range(1, 5)]
        contestants = [c for c in contestants if c] + RO_EXTRA_CONTESTANTS.get(county, [])
        contestants += [''] * (5 - len(contestants))
        leader = clean_name(row.get('Team leader', ''))
        if leader in contestants:  # a student was entered as team leader: use the contact person (the teacher)
            leader = clean_name(row.get('Nume complet', ''))
        team = {
            'country': 'Romania',
            'type': 'Regional',
            # These counties host a contest centre and compete from it.
            'participation': 'Online',
            'team': RO_CENTRE_TEAM.get(county, county),
            'leader': leader,
            'deputy': clean_name(row.get('Deputy leader', '')),
            'source': 'ro-regional',
        }
        for i, name in enumerate(contestants, 1):
            team[f'contestant{i}'] = name
        teams.append(team)
    return teams


def run_import(international=None, ro_regional=None):
    existing = load_teams() if DATA_CSV.exists() else []
    keep = lambda source: [t for t in existing if t.get('source') == source]
    teams = (import_international(international) if international else keep('international')) \
        + (import_ro_regional(ro_regional) if ro_regional else keep('ro-regional'))
    DATA_CSV.parent.mkdir(exist_ok=True)
    with DATA_CSV.open('w', encoding='utf-8', newline='') as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(teams)
    print(f'Wrote {DATA_CSV.relative_to(ROOT)} ({len(teams)} teams)')


# --------------------------------------------------------------------------- generate

def load_teams():
    with DATA_CSV.open(encoding='utf-8', newline='') as fh:
        return [{k: (v or '').strip() for k, v in row.items()} for row in csv.DictReader(fh)]


def flag_for(country):
    stem = FLAG_FILES.get(country, country.lower())
    path = FLAGS_DIR / f'{stem}.svg'
    return f'assets/flags/{stem}.svg' if path.exists() else None


def esc(s):
    return html.escape(s, quote=True)


def render_team(team):
    kind = team['type'].lower()
    mode = team['participation'].lower().replace('-', '')
    contestants = [team.get(f'contestant{i}', '') for i in range(1, 6) if team.get(f'contestant{i}', '')]

    out = ['            <article class="team-card team-card--compact">',
           f'              <div class="team-name">{esc(team["team"])}</div>',
           '              <div class="team-badges">',
           f'                <span class="badge badge-{esc(kind)}">{esc(team["type"])}</span>',
           f'                <span class="badge badge-{esc(mode)}">{esc(team["participation"])}</span>',
           '              </div>',
           '              <div class="team-info">']

    def block(css, label, names):
        out.append(f'                <div class="{css}">')
        out.append(f'                  <span class="label">{label}</span>')
        if names:
            out.append('                  <ul class="member-list">')
            out.extend(f'                    <li class="member-item">{esc(n)}</li>' for n in names)
            out.append('                  </ul>')
        else:
            out.append('                  <span class="none">&mdash;</span>')
        out.append('                </div>')

    block('team-leaders', 'Team leader', [team['leader']] if team['leader'] else [])
    if team['deputy']:
        block('team-leaders', 'Deputy leader', [team['deputy']])
    block('team-students', f'Contestants ({len(contestants)})', contestants)

    out += ['              </div>', '            </article>']
    return '\n'.join(out)


def team_sort_key(t):
    order = TEAM_ORDER.get(t['country'], [])
    rank = order.index(t['team']) if t['team'] in order else len(order)
    return (t['country'].lower(), rank, t['type'] != 'National', t['team'].lower())


def render_page(teams):
    countries = OrderedDict()
    for t in sorted(teams, key=team_sort_key):
        countries.setdefault(t['country'], []).append(t)

    n_contestants = sum(1 for t in teams for i in range(1, 6) if t.get(f'contestant{i}'))
    modes = Counter(t['participation'] for t in teams)
    kinds = Counter(t['type'] for t in teams)

    stats = [
        (len(countries), 'countries'),
        (len(teams), 'teams'),
        (n_contestants, 'contestants'),
        (modes.get('On-site', 0), 'teams on-site'),
        (modes.get('Online', 0), 'teams online'),
    ]

    parts = ['''<!doctype html>
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
          <p>Teams registered for RMI 2026, grouped by country. <strong>National</strong> teams represent a country;
          <strong>regional</strong> teams represent a school, city or county. Teams marked <strong>on-site</strong> compete in
          Bucharest, those marked <strong>online</strong> compete remotely.</p>
          <p class="participants-note">The list is based on the registrations received so far and may still change.</p>
          <ul class="participants-stats" aria-label="Summary">''']
    parts += [f'            <li><strong>{n}</strong> {label}</li>' for n, label in stats]
    parts.append('          </ul>')
    # shown by assets/js/main.js (needs JS; without it every country simply stays expanded)
    parts.append('          <button type="button" class="toggle-all" id="toggle-all" hidden>Collapse all</button>')

    for country, items in countries.items():
        flag = flag_for(country)
        flag_html = f'<img src="{flag}" alt="" class="country-flag" loading="lazy">' if flag else ''
        count = f'{len(items)} team' + ('s' if len(items) != 1 else '')
        parts.append(f'''
          <details class="country-section" open>
            <summary class="country-summary">
              <h2 class="country-heading" id="c-{esc(country.lower().replace(" ", "-"))}">{flag_html}<span>{esc(country)}</span><small>{count}</small></h2>
            </summary>
            <div class="participants-grid">''')
        parts.extend(render_team(t) for t in items)
        parts.append('            </div>\n          </details>')

    parts.append('''        </section>
      </main>
      <footer class="site-footer">&copy; 2026 Tudor Vianu National High School of Computer Science - Built by <a href="https://linkedin.com/in/raresanghel" target="_blank" rel="noopener" title="Visit Rares Anghel's LinkedIn profile">Rares Anghel</a></footer>
    </div>
    <script src="assets/js/main.js"></script>
  </body>
</html>
''')
    return '\n'.join(parts), len(countries), len(teams), n_contestants, kinds


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--registrations', help='raw export of the international registration form')
    ap.add_argument('--ro-regional', help='raw export of the Romanian regional-centres form')
    args = ap.parse_args()

    if args.registrations or args.ro_regional:
        run_import(args.registrations, args.ro_regional)

    page, n_countries, n_teams, n_contestants, kinds = render_page(load_teams())
    OUT_PATH.write_text(page, encoding='utf-8', newline='\n')
    print(f'Wrote {OUT_PATH.relative_to(ROOT)}: {n_countries} countries, {n_teams} teams '
          f'({dict(kinds)}), {n_contestants} contestants')


if __name__ == '__main__':
    main()
