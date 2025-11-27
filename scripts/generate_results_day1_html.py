#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate results1.html from CSV for Day 1 results"""

import csv
import os

# Define input and output paths
csv_path = 'rmi_2025/csv/results_day1.csv'
output_path = 'rmi_2025/pages/results1.html'

# Read CSV
if not os.path.exists(csv_path):
    print(f"Error: {csv_path} not found.")
    exit(1)

rows = []
with open(csv_path, 'r', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    header = next(reader)  # Skip header
    for row in reader:
        if len(row) < 11:
            continue
        name = row[1].strip()
        team = row[2].strip()
        try:
            eng = float(row[3])
            guess = float(row[5])
            squir = float(row[7])
            day1 = float(row[9])
            total = day1
        except ValueError:
            continue  # Skip invalid rows
        rows.append({
            'name': name,
            'team': team,
            'eng': eng,
            'guess': guess,
            'squir': squir,
            'day1': day1,
            'total': total
        })

# Sort by total descending
rows.sort(key=lambda x: x['total'], reverse=True)

# Assign ranks
for i, row in enumerate(rows, 1):
    row['rank'] = i

# Start HTML
html = """<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>Results Day 1 - RMI 2025</title>
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
        /* Ensure sticky header on results (theme provides base styles) */
        .results-table thead th { position: sticky; top: 0; z-index: 2; }
    </style>
</head>
<body>
    <h2>Competition Results - Day 1</h2>
    <div class="table-container">
        <table class="results-table">
            <thead>
                <tr>
                    <th>Rank</th>
                    <th>Name</th>
                    <th>Team</th>
                    <th>Engineers</th>
                    <th>Guess-permutation</th>
                    <th>Squirrel</th>
                    <th>Day 1</th>
                    <th>Total</th>
                </tr>
            </thead>
            <tbody>
"""

# Add rows
for row in rows:
    html += f"""                <tr>
                    <td><strong>{row['rank']}</strong></td>
                    <td>{row['name']}</td>
                    <td>{row['team']}</td>
                    <td>{row['eng']:.2f}</td>
                    <td>{row['guess']:.2f}</td>
                    <td>{row['squir']:.2f}</td>
                    <td><strong>{row['day1']:.2f}</strong></td>
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

print(f"Generated {output_path}!")
print(f"   Total rows: {len(rows)}")