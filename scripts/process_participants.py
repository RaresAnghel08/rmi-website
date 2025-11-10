#!/usr/bin/env python3
"""Main script to process participant registrations and generate participants.html

This script uses a GUI to select online and onsite CSV files, then runs the processing pipeline.
"""
import os
import subprocess
import sys
import tkinter as tk
from tkinter import filedialog, messagebox

class ParticipantProcessor:
    def __init__(self, root):
        self.root = root
        self.root.title("Participant Processor")
        self.root.geometry("500x300")

        self.online_file = ""
        self.onsite_file = ""

        # Online file selection
        tk.Label(root, text="Online CSV File:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.online_label = tk.Label(root, text="Not selected", fg="red")
        self.online_label.grid(row=0, column=1, sticky="w", padx=10, pady=5)
        tk.Button(root, text="Browse...", command=self.select_online).grid(row=0, column=2, padx=10, pady=5)

        # Onsite file selection
        tk.Label(root, text="Onsite CSV File:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.onsite_label = tk.Label(root, text="Not selected", fg="red")
        self.onsite_label.grid(row=1, column=1, sticky="w", padx=10, pady=5)
        tk.Button(root, text="Browse...", command=self.select_onsite).grid(row=1, column=2, padx=10, pady=5)

        # Status
        tk.Label(root, text="Status:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.status_label = tk.Label(root, text="Ready", fg="blue")
        self.status_label.grid(row=2, column=1, columnspan=2, sticky="w", padx=10, pady=5)

        # Run button
        self.run_button = tk.Button(root, text="Run Processing", command=self.run_processing, state="disabled")
        self.run_button.grid(row=3, column=0, columnspan=3, pady=20)

    def select_online(self):
        file = filedialog.askopenfilename(
            title="Select Online CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if file:
            self.online_file = file
            self.online_label.config(text=os.path.basename(file), fg="green")
            self.check_ready()

    def select_onsite(self):
        file = filedialog.askopenfilename(
            title="Select Onsite CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if file:
            self.onsite_file = file
            self.onsite_label.config(text=os.path.basename(file), fg="green")
            self.check_ready()

    def check_ready(self):
        if self.online_file and self.onsite_file:
            self.run_button.config(state="normal")
        else:
            self.run_button.config(state="disabled")

    def run_processing(self):
        # Disable buttons
        self.run_button.config(state="disabled")
        self.status_label.config(text="Merging registrations...", fg="orange")
        self.root.update()

        # Run merge
        if not self.run_command(f'python scripts/merge_registrations.py --online "{self.online_file}" --onsite "{self.onsite_file}"'):
            self.reset_ui()
            return

        self.status_label.config(text="Cleaning and sorting registrations...", fg="orange")
        self.root.update()

        # Run clean
        if not self.run_command('python scripts/clean_registrations.py'):
            self.reset_ui()
            return

        self.status_label.config(text="Generating participants.html...", fg="orange")
        self.root.update()

        # Run generate
        if not self.run_command('python scripts/generate_participants_from_cleaned.py'):
            self.reset_ui()
            return

        self.status_label.config(text="Processing complete!", fg="green")
        messagebox.showinfo("Success", "participants.html has been generated successfully!")
        self.reset_ui()

    def run_command(self, cmd):
        """Run a command and check for errors."""
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            messagebox.showerror("Error", f"Error running: {cmd}\n{result.stderr}")
            return False
        else:
            print(result.stdout.strip())
            return True

    def reset_ui(self):
        self.status_label.config(text="Ready", fg="blue")
        self.run_button.config(state="normal")

def main():
    root = tk.Tk()
    app = ParticipantProcessor(root)
    root.mainloop()

if __name__ == '__main__':
    main()