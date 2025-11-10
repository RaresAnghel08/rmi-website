import csv

# File paths
input_file = 'rmi_2025/csv/2025_merged_registrations.csv'
output_file = 'rmi_2025/csv/2025_cleaned_registrations.csv'

# Columns to keep (0-based indices)
# 1: Country name
# 2: Team name...
# 3: First name of the team leader
# 4: Last name of the team leader
# 7: First name of the deputy leader
# 8: Last name of the deputy leader
# 11: First name of contestant 1
# 12: Last name of contestant 1
# 15: First name of contestant 2
# 16: Last name of contestant 2
# 19: First name of contestant 3
# 20: Last name of contestant 3
# 23: First name of contestant 4
# 24: Last name of contestant 4
columns_to_keep = [1, 2, 3, 4, 7, 8, 11, 12, 15, 16, 19, 20, 23, 24]

# Read the input file
with open(input_file, 'r', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    rows = list(reader)

# Filter columns
filtered_header = [header[i] for i in columns_to_keep]
filtered_rows = [[row[i] for i in columns_to_keep] for row in rows]

# If team name is empty, set it to country name
for row in filtered_rows:
    if not row[1].strip():
        row[1] = row[0]

# Sort by Team Name (index 1), then by Country Name (index 0)
sorted_rows = sorted(filtered_rows, key=lambda x: (x[1].lower(), x[0].lower()))

# Write to output file
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(filtered_header)
    writer.writerows(sorted_rows)

print(f"Cleaned and sorted {len(sorted_rows)} registrations into {output_file}")