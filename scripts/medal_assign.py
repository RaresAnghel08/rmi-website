#!/usr/bin/env python3
"""Script to assign medals to contest results based on rank.

This script reads a CSV file with contest results, assigns medals based on rank,
and saves the updated CSV with a 'medal' column.
"""
import csv
import os
import tkinter as tk
from tkinter import filedialog, messagebox

def assign_medals(results):
    """Assign medals based on rank."""
    for row in results:
        rank_str = row.get('Rank', '').strip()
        try:
            rank = int(rank_str)
        except ValueError:
            row['medal'] = 'Unknown'
            continue
        
        if 1<=rank and rank <= 16:
            row['medal'] = 'Gold'
        elif rank <= 48:
            row['medal'] = 'Silver'
        elif rank <= 96:
            row['medal'] = 'Bronze'
        else:
            row['medal'] = ''
    
    return results

def process_results(input_file, output_file):
    """Process the results file and assign medals."""
    with open(input_file, 'r', newline='', encoding='utf-8-sig') as infile:  # utf-8-sig for BOM
        reader = csv.DictReader(infile)
        results = list(reader)
    
    # Assign medals
    results_with_medals = assign_medals(results)
    
    # Write to output file (use existing fieldnames, assuming 'medal' is already there)
    fieldnames = reader.fieldnames
    with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results_with_medals)

def select_file():
    """Open file dialog to select results CSV file."""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    file_path = filedialog.askopenfilename(
        title="Select Results CSV File",
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    
    return file_path

def main():
    # Select input file
    input_file = select_file()
    if not input_file:
        messagebox.showinfo("Cancelled", "No file selected.")
        return
    
    # Generate output file name
    base_name = os.path.splitext(input_file)[0]
    output_file = f"{base_name}_with_medals.csv"
    
    try:
        process_results(input_file, output_file)
        messagebox.showinfo("Success", f"Medals assigned! Saved to {output_file}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to process file: {str(e)}")

if __name__ == '__main__':
    main()