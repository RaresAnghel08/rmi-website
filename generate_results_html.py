#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate results.html from CSV with medal colors"""

import csv

# Read CSV
with open('csv/results.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    rows = list(reader)

# Start HTML
html = """<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>Results - RMI 2024</title>
    <style>
        .name-gold { color: #bb9413; font-weight: 600; }
        .name-silver { color: #807f81; font-weight: 600; }
        .name-bronze { color: #804A00; font-weight: 600; }
        .results-table { 
            font-size: 0.9rem; 
            width: 100%;
            border-collapse: collapse;
        }
        .results-table th { 
            white-space: nowrap; 
            padding: 0.6rem 0.5rem; 
            background-color: #2c3e50;
            color: #ecf0f1;
            border: 1px solid #34495e;
            text-align: left;
        }
        .results-table td { 
            padding: 0.5rem 0.4rem; 
            border: 1px solid #ddd;
        }
        .results-table tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        .table-container {
            overflow-x: auto;
        }
    </style>
</head>
<body>
    <h2>Competition Results</h2>
    <div class="table-container">
        <table class="results-table">
            <thead>
                <tr>
                    <th>Rank</th>
                    <th>Name</th>
                    <th>Country</th>
                    <th>Choose Interval</th>
                    <th>Octagon</th>
                    <th>Skittlez</th>
                    <th>Day 1</th>
                    <th>Signals</th>
                    <th>Ramen</th>
                    <th>Jump Civilization</th>
                    <th>Day 2</th>
                    <th>Total Score</th>
                </tr>
            </thead>
            <tbody>
"""

# Add rows
for row in rows:
    rank = row.get('Rank', '').strip()
    name = row.get('Name', '').strip()
    country = row.get('Country', '').strip()
    choose = row.get('Choose Interval', '').strip()
    octagon = row.get('Octagon', '').strip()
    skittlez = row.get('Skittlez', '').strip()
    day1 = row.get('Day 1', '').strip()
    signals = row.get('Signals', '').strip()
    ramen = row.get('Ramen', '').strip()
    jump = row.get('Jump Civilization', '').strip()
    day2 = row.get('Day 2', '').strip()
    score = row.get('Total Score', '').strip()
    medal = row.get('medal', '').strip().lower()
    
    # Determine name class
    name_class = ''
    if medal == 'gold':
        name_class = 'name-gold'
    elif medal == 'silver':
        name_class = 'name-silver'
    elif medal == 'bronze':
        name_class = 'name-bronze'
    
    html += f"""                <tr>
                    <td><strong>{rank}</strong></td>
                    <td><span class="{name_class}">{name}</span></td>
                    <td>{country}</td>
                    <td>{choose}</td>
                    <td>{octagon}</td>
                    <td>{skittlez}</td>
                    <td><strong>{day1}</strong></td>
                    <td>{signals}</td>
                    <td>{ramen}</td>
                    <td>{jump}</td>
                    <td><strong>{day2}</strong></td>
                    <td><strong>{score}</strong></td>
                </tr>
"""

# End HTML
html += """            </tbody>
        </table>
    </div>
</body>
</html>"""

# Write to file
with open('pages/results.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ Generated pages/results.html with medal colors!")
print(f"   Total rows: {len(rows)}")
print(f"   Gold medals: {sum(1 for r in rows if r.get('medal', '').strip().lower() == 'gold')}")
print(f"   Silver medals: {sum(1 for r in rows if r.get('medal', '').strip().lower() == 'silver')}")
print(f"   Bronze medals: {sum(1 for r in rows if r.get('medal', '').strip().lower() == 'bronze')}")
