#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate final results.html from Day 1 and Day 2 CSVs with medal allocation"""

import csv
import os

# Define input and output paths
csv_day1_path = 'rmi_2025/csv/results_day1.csv'
csv_day2_path = 'rmi_2025/csv/results_day2.csv'
output_path = 'rmi_2025/pages/results.html'

# Check if CSVs exist
if not os.path.exists(csv_day1_path):
    print(f"Error: {csv_day1_path} not found.")
    exit(1)
if not os.path.exists(csv_day2_path):
    print(f"Error: {csv_day2_path} not found.")
    exit(1)

# Read Day 1 results
day1_data = {}
with open(csv_day1_path, 'r', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    header = next(reader)  # Skip header
    for row in reader:
        if len(row) < 11:
            continue
        username = row[0].strip()
        name = row[1].strip()
        team = row[2].strip()
        try:
            eng = float(row[3])
            guess = float(row[5])
            squir = float(row[7])
            day1_total = float(row[9])
        except ValueError:
            continue
        day1_data[username] = {
            'name': name,
            'team': team,
            'engineers': eng,
            'guess_perm': guess,
            'squirrel': squir,
            'day1': day1_total
        }

# Read Day 2 results and merge
rows = []
with open(csv_day2_path, 'r', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    header = next(reader)  # Skip header
    for row in reader:
        if len(row) < 11:
            continue
        username = row[0].strip()
        try:
            cheap = float(row[3])
            kor = float(row[5])
            oranges = float(row[7])
            day2_total = float(row[9])
        except ValueError:
            continue
        
        # Get Day 1 data
        if username in day1_data:
            d1 = day1_data[username]
            total = d1['day1'] + day2_total
            rows.append({
                'name': d1['name'],
                'team': d1['team'],
                'engineers': d1['engineers'],
                'guess_perm': d1['guess_perm'],
                'squirrel': d1['squirrel'],
                'day1': d1['day1'],
                'cheap': cheap,
                'kor': kor,
                'oranges': oranges,
                'day2': day2_total,
                'total': total
            })

# Sort by total descending
rows.sort(key=lambda x: x['total'], reverse=True)

# Assign medals based on rank with tie handling
# Medal ranges: 1-21 gold, 22-62 silver, 63-123 bronze
def assign_medals(sorted_rows):
    for i, row in enumerate(sorted_rows):
        row['rank'] = i + 1
    
    # Assign medals with tie handling
    for i, row in enumerate(sorted_rows):
        current_score = row['total']
        current_rank = row['rank']
        
        # Check if there are ties at boundary positions
        if current_rank <= 21:
            row['medal'] = 'gold'
            # Extend gold if there's a tie at position 22
            if current_rank == 21:
                for j in range(i + 1, len(sorted_rows)):
                    if sorted_rows[j]['total'] == current_score:
                        sorted_rows[j]['medal'] = 'gold'
                    else:
                        break
        elif current_rank <= 62:
            # Check if this score tied with gold
            if i > 0 and sorted_rows[i - 1].get('medal') == 'gold' and sorted_rows[i - 1]['total'] == current_score:
                row['medal'] = 'gold'
            else:
                row['medal'] = 'silver'
                # Extend silver if there's a tie at position 63
                if current_rank == 62:
                    for j in range(i + 1, len(sorted_rows)):
                        if sorted_rows[j]['total'] == current_score:
                            sorted_rows[j]['medal'] = 'silver'
                        else:
                            break
        elif current_rank <= 123:
            # Check if this score tied with silver
            if i > 0 and sorted_rows[i - 1].get('medal') == 'silver' and sorted_rows[i - 1]['total'] == current_score:
                row['medal'] = 'silver'
            else:
                row['medal'] = 'bronze'
                # Extend bronze if there's a tie at position 124
                if current_rank == 123:
                    for j in range(i + 1, len(sorted_rows)):
                        if sorted_rows[j]['total'] == current_score:
                            sorted_rows[j]['medal'] = 'bronze'
                        else:
                            break
        else:
            # Check if this score tied with bronze
            if i > 0 and sorted_rows[i - 1].get('medal') == 'bronze' and sorted_rows[i - 1]['total'] == current_score:
                row['medal'] = 'bronze'
            else:
                row['medal'] = ''

assign_medals(rows)

# Start HTML
html = """<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>Results - RMI 2025</title>
    <link rel="stylesheet" href="assets/css/style.css">
    <style>
        /* Small page-specific overrides that complement rms-theme */
        .table-container { overflow-x: auto; }
        /* Make page exactly viewport height on phones and let the table-area fill the remaining space.
            This keeps the header visible and makes the table scrollable inside the viewport. */
        @media (max-width: 760px) {
            html,body{height:100vh;margin:0}
            body{display:flex;flex-direction:column}
            .results-header{flex:0 0 auto;padding:.75rem 1rem;background:var(--card);border-bottom:1px solid rgba(0,0,0,0.06)}
            .table-container{flex:1 1 auto;overflow:auto;-webkit-overflow-scrolling:touch}
            /* Ensure table header stays visible inside the scrollable table container */
            .results-table thead th{position:sticky;top:0;background:var(--card);z-index:3}
        }
        /* Keep medal name colours (uses theme variables where appropriate) */
        .name-gold { color: #bb9413; font-weight: 600; }
        .name-silver { color: #807f81; font-weight: 600; }
        .name-bronze { color: #804A00; font-weight: 600; }
        /* Ensure sticky header on results (theme provides base styles) */
        .results-table thead th { position: sticky; top: 0; z-index: 2; }
    </style>
</head>
<body>
    <h2>Competition Results - Final</h2>
    <div class="table-container">
        <table class="results-table">
            <thead>
                <tr>
                    <th>Rank</th>
                    <th>Name</th>
                    <th>Team</th>
                    <th>Engineers</th>
                    <th>Guess-perm</th>
                    <th>Squirrel</th>
                    <th>Day 1</th>
                    <th>Cheap-AI</th>
                    <th>Kor</th>
                    <th>Oranges</th>
                    <th>Day 2</th>
                    <th>Total</th>
                </tr>
            </thead>
            <tbody>
"""

# Add rows
for row in rows:
    name_class = ''
    if row.get('medal') == 'gold':
        name_class = 'name-gold'
    elif row.get('medal') == 'silver':
        name_class = 'name-silver'
    elif row.get('medal') == 'bronze':
        name_class = 'name-bronze'
    
    html += f"""                <tr>
                    <td><strong>{row['rank']}</strong></td>
                    <td><span class="{name_class}">{row['name']}</span></td>
                    <td>{row['team']}</td>
                    <td>{row['engineers']:.2f}</td>
                    <td>{row['guess_perm']:.2f}</td>
                    <td>{row['squirrel']:.2f}</td>
                    <td><strong>{row['day1']:.2f}</strong></td>
                    <td>{row['cheap']:.2f}</td>
                    <td>{row['kor']:.2f}</td>
                    <td>{row['oranges']:.2f}</td>
                    <td><strong>{row['day2']:.2f}</strong></td>
                    <td><strong>{row['total']:.2f}</strong></td>
                </tr>
"""

# End HTML
html += """            </tbody>
        </table>
    </div>
</body>
</html>"""

# Write to file
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html)

# Count medals
gold_count = sum(1 for r in rows if r.get('medal') == 'gold')
silver_count = sum(1 for r in rows if r.get('medal') == 'silver')
bronze_count = sum(1 for r in rows if r.get('medal') == 'bronze')

print(f"Generated {output_path}!")
print(f"   Total rows: {len(rows)}")
print(f"   Gold medals: {gold_count}")
print(f"   Silver medals: {silver_count}")
print(f"   Bronze medals: {bronze_count}")
