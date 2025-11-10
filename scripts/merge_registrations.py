import csv
import argparse

# Parse arguments
parser = argparse.ArgumentParser(description='Merge online and onsite registration CSV files.')
parser.add_argument('--online', required=True, help='Path to the online CSV file')
parser.add_argument('--onsite', required=True, help='Path to the onsite CSV file')
args = parser.parse_args()

# File paths
online_file = args.online
onsite_file = args.onsite
output_file = 'public/csv/2025_merged_registrations.csv'

# Read onsite file to get the full header
with open(onsite_file, 'r', newline='', encoding='utf-8') as f:
    onsite_reader = csv.reader(f)
    onsite_header = next(onsite_reader)
    onsite_rows = list(onsite_reader)

# Read online file
with open(online_file, 'r', newline='', encoding='utf-8') as f:
    online_reader = csv.reader(f)
    online_header = next(online_reader)  # Skip header
    online_rows = list(online_reader)

# Function to insert empty t-shirt columns into online rows
def insert_tshirt_columns(row):
    # Online rows have 21 columns, onsite have 27 with t-shirts inserted
    # Insert '' after each email position
    return [
        row[0],  # timestamp
        row[1],  # country
        row[2],  # team
        row[3],  # leader first
        row[4],  # leader last
        row[5],  # leader email
        '',      # leader t
        row[6],  # deputy first
        row[7],  # deputy last
        row[8],  # deputy email
        '',      # deputy t
        row[9],  # c1 first
        row[10], # c1 last
        row[11], # c1 email
        '',      # c1 t
        row[12], # c2 first
        row[13], # c2 last
        row[14], # c2 email
        '',      # c2 t
        row[15], # c3 first
        row[16], # c3 last
        row[17], # c3 email
        '',      # c3 t
        row[18], # c4 first
        row[19], # c4 last
        row[20], # c4 email
        ''       # c4 t
    ]

# Process online rows
processed_online_rows = [insert_tshirt_columns(row) for row in online_rows]

# Combine all rows
all_rows = onsite_rows + processed_online_rows

# Write to output file
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(onsite_header)
    writer.writerows(all_rows)

print(f"Merged {len(onsite_rows)} onsite and {len(processed_online_rows)} online registrations into {output_file}")