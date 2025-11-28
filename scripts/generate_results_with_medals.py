#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate CSV with NAME, COUNTRY, MEDAL columns from results CSVs"""

import csv
import os

# Define input and output paths
csv_day1_path = 'rmi_2025/csv/results_day1.csv'
csv_day2_path = 'rmi_2025/csv/results_day2.csv'
output_path = 'rmi_2025/csv/results_with_medals.csv'

# Mapping of team name -> country based on registration CSVs
TEAM_TO_COUNTRY = {
    # Greece
    "Greece": "Greece",
    
    # Ukraine
    "Ukraine": "Ukraine",
    "Ukraine_1": "Ukraine",
    "Ukraine_2": "Ukraine",
    "Ukraine_3": "Ukraine",
    "Ukraine_4": "Ukraine",
    "ALGO1": "Ukraine",
    "ALGO2": "Ukraine",
    "KyivNTFS": "Ukraine",
    "UPML_HAPPY!": "Ukraine",
    "KyivUPML118": "Ukraine",
    "Attempt": "Ukraine",
    "UPML_89": "Ukraine",
    
    # Georgia
    "Georgia_1": "Georgia",
    "Georgia_2": "Georgia",
    "Georgia_3": "Georgia",
    
    # Slovenia
    "Slovenia": "Slovenia",
    
    # Romania
    "Romania": "Romania",
    "Romania_1": "Romania",
    "Romania_2": "Romania",
    "Romania_3": "Romania",
    "Romania_4": "Romania",
    "Romania_5": "Romania",
    "Romania_6": "Romania",
    "Romania_G": "Romania",
    "Romania_J1": "Romania",
    "Romania_J2": "Romania",
    "InfO1_Ploiesti": "Romania",
    "Craiova": "Romania",
    "Vaslui": "Romania",
    "Iasi": "Romania",
    "Bucuresti_1": "Romania",
    "Bucuresti_2": "Romania",
    "Bucuresti_3": "Romania",
    "Vianu_1": "Romania",
    "Vianu_2": "Romania",
    "Vianu_3": "Romania",
    "Vianu_4": "Romania",
    "Vianu_J1": "Romania",
    "Vianu_J2": "Romania",
    
    # Bulgaria
    "Bulgaria": "Bulgaria",
    "Ruse-Pleven_BGR": "Bulgaria",
    "Sofia_Junior": "Bulgaria",
    "Sofia": "Bulgaria",
    "Mini_PSV": "Bulgaria",
    "Shkola_A_B_Gameloft_1": "Bulgaria",
    "Shkola_A_B_Gameloft_2": "Bulgaria",
    "Shkola_A_B_Gameloft_3": "Bulgaria",
    "Haskovo": "Bulgaria",
    "Varna-A": "Bulgaria",
    "Varna-BC": "Bulgaria",
    
    # Vietnam
    "Vietnam": "Vietnam",
    "HSGS": "Vietnam",
    "CSP_SuperKids": "Vietnam",
    "Demon": "Vietnam",
    "DownTown_Dwellers": "Vietnam",
    "Random": "Vietnam",
    
    # Moldova
    "Moldova": "Moldova",
    "The_Bitles": "Moldova",
    "Code_Warriors": "Moldova",
    "Bit_Masters": "Moldova",
    
    # Singapore
    "Singapore_HCI": "Singapore",
    "Singapore_NUSH": "Singapore",
    
    # Serbia
    "Serbia": "Serbia",
    
    # Poland
    "Poland": "Poland",
    
    # Italy
    "Italy": "Italy",
    
    # Hungary
    "Hungary": "Hungary",
}

def get_country_from_team(team_name):
    """Get country from team name, defaulting to the team name if not found"""
    return TEAM_TO_COUNTRY.get(team_name, team_name)

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
            day1_total = float(row[9])
        except ValueError:
            continue
        day1_data[username] = {
            'name': name,
            'team': team,
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
                'total': total
            })

# Sort by total descending
rows.sort(key=lambda x: x['total'], reverse=True)

# Assign medals based on rank with tie handling
def assign_medals(sorted_rows):
    for i, row in enumerate(sorted_rows):
        row['rank'] = i + 1
    
    # Assign medals with tie handling
    for i, row in enumerate(sorted_rows):
        current_score = row['total']
        current_rank = row['rank']
        
        # Check if there are ties at boundary positions
        if current_rank <= 21:
            row['medal'] = 'Gold'
            # Extend gold if there's a tie at position 22
            if current_rank == 21:
                for j in range(i + 1, len(sorted_rows)):
                    if sorted_rows[j]['total'] == current_score:
                        sorted_rows[j]['medal'] = 'Gold'
                    else:
                        break
        elif current_rank <= 62:
            # Check if this score tied with gold
            if i > 0 and sorted_rows[i - 1].get('medal') == 'Gold' and sorted_rows[i - 1]['total'] == current_score:
                row['medal'] = 'Gold'
            else:
                row['medal'] = 'Silver'
                # Extend silver if there's a tie at position 63
                if current_rank == 62:
                    for j in range(i + 1, len(sorted_rows)):
                        if sorted_rows[j]['total'] == current_score:
                            sorted_rows[j]['medal'] = 'Silver'
                        else:
                            break
        elif current_rank <= 123:
            # Check if this score tied with silver
            if i > 0 and sorted_rows[i - 1].get('medal') == 'Silver' and sorted_rows[i - 1]['total'] == current_score:
                row['medal'] = 'Silver'
            else:
                row['medal'] = 'Bronze'
                # Extend bronze if there's a tie at position 124
                if current_rank == 123:
                    for j in range(i + 1, len(sorted_rows)):
                        if sorted_rows[j]['total'] == current_score:
                            sorted_rows[j]['medal'] = 'Bronze'
                        else:
                            break
        else:
            # Check if this score tied with bronze
            if i > 0 and sorted_rows[i - 1].get('medal') == 'Bronze' and sorted_rows[i - 1]['total'] == current_score:
                row['medal'] = 'Bronze'
            else:
                row['medal'] = ''

assign_medals(rows)

# Write to CSV
with open(output_path, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['NAME', 'COUNTRY', 'MEDAL'])
    for row in rows:
        country = get_country_from_team(row['team'])
        writer.writerow([row['name'], country, row['medal']])

# Count medals
gold_count = sum(1 for r in rows if r.get('medal') == 'Gold')
silver_count = sum(1 for r in rows if r.get('medal') == 'Silver')
bronze_count = sum(1 for r in rows if r.get('medal') == 'Bronze')

print(f"Generated {output_path}!")
print(f"   Total rows: {len(rows)}")
print(f"   Gold medals: {gold_count}")
print(f"   Silver medals: {silver_count}")
print(f"   Bronze medals: {bronze_count}")
