#!/usr/bin/env python3
"""Main script to process participant registrations and generate participants.html

This script uses a GUI to select online and onsite CSV files, then runs the processing pipeline.
"""
import csv
import os
import subprocess
import sys
import tkinter as tk
from tkinter import filedialog, messagebox

class ParticipantProcessor:
    def __init__(self, root):
        self.root = root
        self.root.title("RMI Participant Manager")
        self.root.geometry("400x200")
        self.root.configure(bg="#E6F3FF")  # Light blue background

        # Set the icon
        try:
            self.root.iconphoto(True, tk.PhotoImage(file='public/assets/organisers/vianu.png'))
        except tk.TclError:
            pass  # If logo not found, continue without icon

        # Center the window
        self.center_window()

        # Welcome label
        welcome_label = tk.Label(root, text="RMI Participant Manager", font=("Arial", 16, "bold"), bg="#E6F3FF", fg="#004080")
        welcome_label.pack(pady=20)

        # Buttons
        button_frame = tk.Frame(root, bg="#E6F3FF")
        button_frame.pack(pady=10)
        
        participants_btn = tk.Button(button_frame, text="Create Participants Page", command=self.open_participants_window, bg="#4CAF50", fg="white", font=("Arial", 12), width=20)
        participants_btn.pack(side='left', padx=10)
        
        medals_btn = tk.Button(button_frame, text="Assign Medals", command=self.open_medals_window, bg="#FF9800", fg="white", font=("Arial", 12), width=20)
        medals_btn.pack(side='left', padx=10)

        # Footer
        footer_label = tk.Label(root, text="© Rares Anghel", font=("Arial", 8), bg="#E6F3FF", fg="#004080")
        footer_label.pack(side='bottom', pady=10)

    def center_window(self):
        """Center the window on the screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def open_participants_window(self):
        """Open the participants processing window."""
        participants_win = tk.Toplevel(self.root)
        ParticipantsWindow(participants_win)

    def open_medals_window(self):
        """Open the medals assignment window."""
        medals_win = tk.Toplevel(self.root)
        MedalsWindow(medals_win)

class ParticipantsWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Create Participants Page")
        self.root.geometry("500x300")
        self.root.configure(bg="#E6F3FF")

        # Center the window
        self.center_window()

        self.online_file = ""
        self.onsite_file = ""

        # Welcome label
        welcome_label = tk.Label(root, text="Create Participants Page", font=("Arial", 14, "bold"), bg="#E6F3FF", fg="#004080", anchor='center')
        welcome_label.grid(row=0, column=0, columnspan=3, pady=10, sticky="ew")

        # Configure columns
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)

        # Online file selection
        tk.Label(root, text="Online CSV File:", bg="#E6F3FF", fg="#004080", anchor='center').grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        self.online_label = tk.Label(root, text="Not selected", fg="red", bg="#E6F3FF", anchor='center')
        self.online_label.grid(row=1, column=1, sticky="ew", padx=10, pady=5)
        tk.Button(root, text="Browse...", command=self.select_online, bg="#4CAF50", fg="white").grid(row=1, column=2, padx=10, pady=5)

        # Onsite file selection
        tk.Label(root, text="Onsite CSV File:", bg="#E6F3FF", fg="#004080", anchor='center').grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        self.onsite_label = tk.Label(root, text="Not selected", fg="red", bg="#E6F3FF", anchor='center')
        self.onsite_label.grid(row=2, column=1, sticky="ew", padx=10, pady=5)
        tk.Button(root, text="Browse...", command=self.select_onsite, bg="#4CAF50", fg="white").grid(row=2, column=2, padx=10, pady=5)

        # Status
        tk.Label(root, text="Status:", bg="#E6F3FF", fg="#004080", anchor='center').grid(row=3, column=0, sticky="ew", padx=10, pady=5)
        self.status_label = tk.Label(root, text="Ready", fg="blue", bg="#E6F3FF", anchor='center')
        self.status_label.grid(row=3, column=1, columnspan=2, sticky="ew", padx=10, pady=5)

        # Run button
        self.run_button = tk.Button(root, text="Create Page", command=self.run_processing, state="disabled", bg="#FF9800", fg="white", font=("Arial", 10, "bold"), width=12)
        self.run_button.grid(row=4, column=0, columnspan=3, pady=20)

        # Footer
        footer_label = tk.Label(root, text="© Rares Anghel", font=("Arial", 8), bg="#E6F3FF", fg="#004080")
        footer_label.grid(row=5, column=0, columnspan=3, pady=10)

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def select_online(self):
        self.root.focus_force()
        file = filedialog.askopenfilename(title="Select Online CSV File", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if file:
            self.online_file = file
            self.online_label.config(text=os.path.basename(file), fg="green")
            self.check_ready()
        self.root.focus_force()

    def select_onsite(self):
        self.root.focus_force()
        file = filedialog.askopenfilename(title="Select Onsite CSV File", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if file:
            self.onsite_file = file
            self.onsite_label.config(text=os.path.basename(file), fg="green")
            self.check_ready()
        self.root.focus_force()

    def check_ready(self):
        if self.online_file and self.onsite_file:
            self.run_button.config(state="normal")
        else:
            self.run_button.config(state="disabled")

    def run_processing(self):
        self.run_button.config(state="disabled")
        self.status_label.config(text="Merging registrations...", fg="orange")
        self.root.update()

        if not self.run_command(f'python scripts/merge_registrations.py --online "{self.online_file}" --onsite "{self.onsite_file}"'):
            self.reset_ui()
            return

        self.status_label.config(text="Cleaning and sorting...", fg="orange")
        self.root.update()

        if not self.run_command('python scripts/clean_registrations.py'):
            self.reset_ui()
            return

        self.status_label.config(text="Generating participants.html...", fg="orange")
        self.root.update()

        if not self.run_command('python scripts/generate_participants_from_cleaned.py'):
            self.reset_ui()
            return

        self.status_label.config(text="Complete!", fg="green")
        messagebox.showinfo("Success", "participants.html created!")
        self.reset_ui()

    def run_command(self, cmd):
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            messagebox.showerror("Error", f"Error: {cmd}\n{result.stderr}")
            return False
        return True

    def reset_ui(self):
        self.status_label.config(text="Ready", fg="blue")
        self.run_button.config(state="normal")

class MedalsWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Assign Medals")
        self.root.geometry("400x200")
        self.root.configure(bg="#E6F3FF")

        # Center the window
        self.center_window()

        # Welcome label
        welcome_label = tk.Label(root, text="Assign Medals to Results", font=("Arial", 14, "bold"), bg="#E6F3FF", fg="#004080", anchor='center')
        welcome_label.pack(pady=20)

        # Select file button
        self.select_btn = tk.Button(root, text="Select Results CSV", command=self.select_file, bg="#4CAF50", fg="white", font=("Arial", 12))
        self.select_btn.pack(pady=10)

        # Status
        self.status_label = tk.Label(root, text="Ready", fg="blue", bg="#E6F3FF")
        self.status_label.pack(pady=10)

        # Run button
        self.run_button = tk.Button(root, text="Assign Medals", command=self.assign_medals, state="disabled", bg="#FF9800", fg="white", font=("Arial", 10, "bold"))
        self.run_button.pack(pady=10)

        # Footer
        footer_label = tk.Label(root, text="© Rares Anghel", font=("Arial", 8), bg="#E6F3FF", fg="#004080")
        footer_label.pack(side='bottom', pady=10)

        self.results_file = ""

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def select_file(self):
        self.root.focus_force()
        file = filedialog.askopenfilename(title="Select Results CSV File", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if file:
            self.results_file = file
            self.status_label.config(text=f"Selected: {os.path.basename(file)}", fg="green")
            self.run_button.config(state="normal")
        self.root.focus_force()

    def assign_medals(self):
        self.run_button.config(state="disabled")
        self.status_label.config(text="Assigning medals...", fg="orange")
        self.root.update()

        output_file = self.results_file.replace('.csv', '_with_medals.csv')
        try:
            self.process_results_file(self.results_file, output_file)
            self.run_command('python scripts/generate_results_html.py')
            self.status_label.config(text="Complete!", fg="green")
            messagebox.showinfo("Success", f"Medals assigned! Saved to {output_file}")
        except Exception as e:
            self.status_label.config(text="Failed!", fg="red")
            messagebox.showerror("Error", f"Failed: {str(e)}")
        self.run_button.config(state="normal")

    def assign_medals_func(self, results):
        for row in results:
            rank_str = row.get('Rank', '').strip()
            try:
                rank = int(rank_str)
            except ValueError:
                row['medal'] = 'Unknown'
                continue
            
            if 1 <= rank <= 16:
                row['medal'] = 'Gold'
            elif rank <= 48:
                row['medal'] = 'Silver'
            elif rank <= 96:
                row['medal'] = 'Bronze'
            else:
                row['medal'] = ''
        
        return results

    def process_results_file(self, input_file, output_file):
        with open(input_file, 'r', newline='', encoding='utf-8-sig') as infile:
            reader = csv.DictReader(infile)
            results = list(reader)
        
        results = self.assign_medals_func(results)
        
        fieldnames = reader.fieldnames
        with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)

    def run_command(self, cmd):
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            messagebox.showerror("Error", f"Error: {cmd}\n{result.stderr}")
            return False
        return True

def main():
    root = tk.Tk()
    app = ParticipantProcessor(root)
    root.mainloop()

if __name__ == '__main__':
    main()