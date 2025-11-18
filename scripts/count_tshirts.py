#!/usr/bin/env python3
"""Count T-shirt sizes for leaders and participants across CSVs.

Usage: run from repository root or directly:
  python scripts/count_tshirts.py

The script searches for CSV files in `rmi_2025/csv` and aggregates:
- leaders: team leader + deputy leader sizes
- participants: all contestant sizes

Outputs totals and per-size breakdowns.
"""
from pathlib import Path
import csv
from collections import Counter, defaultdict
import sys
import re


def find_csv_dir():
    repo_root = Path(__file__).resolve().parents[1]
    csv_dir = repo_root / 'rmi_2025' / 'csv'
    return csv_dir


def normalize_size(s: str) -> str:
    if s is None:
        return ''
    s = s.strip()
    if not s:
        return ''
    # Common normalizations: remove spaces, uppercase
    s = s.upper().replace(' ', '')
    # Accept variants like XXL, XXXL, XS, S, M, L, XL
    return s


def process_file(path: Path, leader_ctr: Counter, participant_ctr: Counter, seen_leaders: set, seen_participants: set):
    try:
        with path.open('r', encoding='utf-8-sig', newline='') as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames or []

            # build mapping of t-shirt columns to name columns
            tshirt_to_names = {}
            for h in headers:
                if 't-shirt' in h.lower():
                    h_lower = h.lower()
                    if 'team leader' in h_lower:
                        role = 'team leader'
                    elif 'deputy' in h_lower:
                        role = 'deputy leader'
                    elif 'contestant' in h_lower:
                        match = re.search(r'contestant (\d+)', h_lower)
                        if match:
                            num = match.group(1)
                            role = f'contestant {num}'
                        else:
                            continue
                    else:
                        continue
                    if 'contestant' in role:
                        num = role.split()[-1]
                        first_col = f'First name of contestant {num}'
                        last_col = f'Last name of contestant {num}'
                    else:
                        first_col = f'First name of the {role}'
                        last_col = f'Last name of the {role}'
                    tshirt_to_names[h] = (first_col, last_col, role)

            for row in reader:
                for tshirt_col, (first_col, last_col, role) in tshirt_to_names.items():
                    val = row.get(tshirt_col, '')
                    size = normalize_size(val)
                    if not size:
                        continue
                    first = row.get(first_col, '').strip()
                    last = row.get(last_col, '').strip()
                    if not first or not last:
                        continue
                    key = (first, last)
                    if 'leader' in role:
                        if key not in seen_leaders:
                            seen_leaders.add(key)
                            leader_ctr[size] += 1
                    else:  # contestant
                        if key not in seen_participants:
                            seen_participants.add(key)
                            participant_ctr[size] += 1
    except Exception as e:
        print(f"Error processing {path}: {e}", file=sys.stderr)


def print_summary(title: str, ctr: Counter):
    total = sum(ctr.values())
    print(f"{title}: total = {total}")
    if total == 0:
        print("  (no entries)")
        return
    # sort sizes: common order then by count
    common_order = ['XS', 'S', 'M', 'L', 'XL', 'XXL', 'XXXL', 'XXXXL']
    ordered = []
    for s in common_order:
        if ctr.get(s):
            ordered.append((s, ctr[s]))
    # remaining sizes (including blank)
    remainder = [(s, c) for s, c in ctr.items() if s not in common_order]
    remainder.sort(key=lambda x: -x[1])
    for s, c in ordered + remainder:
        label = s if s else '(blank)'
        print(f"  {label}: {c}")


def main():
    leader_ctr = Counter()
    participant_ctr = Counter()
    seen_leaders = set()
    seen_participants = set()

    if len(sys.argv) > 1:
        p = Path(sys.argv[1])
        if not p.exists():
            print(f"File not found: {p}")
            return 1
        print(f"Processing single file: {p}")
        process_file(p, leader_ctr, participant_ctr, seen_leaders, seen_participants)
    else:
        csv_dir = find_csv_dir()
        default_file = csv_dir / '2025_onsite_3.csv'
        if not default_file.exists():
            print(f"Default CSV not found: {default_file}")
            return 1
        print(f"Processing {default_file}")
        process_file(default_file, leader_ctr, participant_ctr, seen_leaders, seen_participants)

    print_summary('Leaders (team leader + deputy)', leader_ctr)
    print()
    print_summary('Participants (contestants)', participant_ctr)
    return 0


if __name__ == '__main__':
    sys.exit(main())
