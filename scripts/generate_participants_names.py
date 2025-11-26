#!/usr/bin/env python3
"""Generate a CSV with participant names and their coordinator (team leader).

Scans CSV files in `rmi_2025/csv/` that contain registration rows and extracts
contestant names paired with their team leader. Writes `participants_names.csv`.
"""
import csv
import glob
import os
import sys


def find_key(keys, *substrings):
    for k in keys:
        kl = k.lower()
        if all(s.lower() in kl for s in substrings):
            return k
    return None


def main():
    repo_root = os.path.dirname(os.path.dirname(__file__))
    csv_dir = os.path.join(repo_root, 'rmi_2025', 'csv')
    pattern = os.path.join(csv_dir, '2025_online_4.csv')
    files = sorted(glob.glob(pattern))
    out_path = os.path.join(csv_dir, 'participants_names.csv')

    total_rows = 0
    total_pairs = 0

    with open(out_path, 'w', newline='', encoding='utf-8') as out_f:
        writer = csv.writer(out_f)
        writer.writerow(['Coordinator', 'Participant'])

        for fp in files:
            try:
                with open(fp, newline='', encoding='utf-8') as fh:
                    reader = csv.DictReader(fh)
                    if reader.fieldnames is None:
                        continue
                    # detect leader keys
                    keys = reader.fieldnames
                    leader_first_k = find_key(keys, 'first name', 'team leader') or find_key(keys, 'first name', 'leader')
                    leader_last_k = find_key(keys, 'last name', 'team leader') or find_key(keys, 'last name', 'leader')
                    deputy_first_k = find_key(keys, 'first name', 'deputy')
                    deputy_last_k = find_key(keys, 'last name', 'deputy')

                    # find contestant keys (1..n)
                    contestant_first_keys = [k for k in keys if 'first name' in k.lower() and 'contestant' in k.lower()]
                    contestant_last_keys = [k for k in keys if 'last name' in k.lower() and 'contestant' in k.lower()]

                    if not contestant_first_keys:
                        # fallback: columns named like 'First name of contestant 1' etc may be present but with slightly different casing
                        contestant_first_keys = [k for k in keys if 'contestant' in k.lower() and 'first' in k.lower()]
                        contestant_last_keys = [k for k in keys if 'contestant' in k.lower() and 'last' in k.lower()]

                    for row in reader:
                        total_rows += 1
                        leader_first = (row.get(leader_first_k) or '').strip() if leader_first_k else ''
                        leader_last = (row.get(leader_last_k) or '').strip() if leader_last_k else ''
                        if not leader_first and deputy_first_k:
                            leader_first = (row.get(deputy_first_k) or '').strip()
                        if not leader_last and deputy_last_k:
                            leader_last = (row.get(deputy_last_k) or '').strip()

                        coordinator = ' '.join([p for p in [leader_first, leader_last] if p]).strip()

                        # if coordinator empty, use empty string but still collect participants
                        # iterate matched contestant pairs by index
                        max_len = max(len(contestant_first_keys), len(contestant_last_keys))
                        # if keys lists are empty, try positional columns (common fallback)
                        if max_len == 0:
                            # try columns that contain 'Contestant' without first/last
                            cfs = [k for k in keys if 'contestant 1' in k.lower() or 'contestant' in k.lower()]
                            for k in cfs:
                                val = (row.get(k) or '').strip()
                                if val:
                                    writer.writerow([coordinator, val])
                                    total_pairs += 1
                            continue

                        for i in range(max_len):
                            first_k = contestant_first_keys[i] if i < len(contestant_first_keys) else None
                            last_k = contestant_last_keys[i] if i < len(contestant_last_keys) else None
                            first = (row.get(first_k) or '').strip() if first_k else ''
                            last = (row.get(last_k) or '').strip() if last_k else ''
                            if first or last:
                                participant = ' '.join([p for p in [first, last] if p]).strip()
                                writer.writerow([coordinator, participant])
                                total_pairs += 1
            except Exception:
                # ignore unreadable files
                continue

    print(f'Wrote {out_path} ({total_pairs} participant rows from {len(files)} files, scanned {total_rows} input rows)')


if __name__ == '__main__':
    main()
