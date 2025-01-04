import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import pandas as pd
from tkinterdnd2 import TkinterDnD, DND_FILES

import config
import db


class ExcelReaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Excel File Reader")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)

        # Header Label
        self.header_label = tk.Label(
            root,
            text="Excel File Reader",
            font=("Arial", 16, "bold"),
            bg="#005a9e",
            fg="white",
            padx=20,
            pady=10
        )
        self.header_label.pack(fill=tk.X)

        # Instruction Label
        self.instruction_label = tk.Label(
            root,
            text="Drag and drop an Excel file here or click 'Open File'",
            font=("Arial", 12),
            fg="#555"
        )
        self.instruction_label.pack(pady=10)

        # Dropdown for selecting sheets
        self.sheet_selector_label = tk.Label(root, text="Select a sheet to display:", font=("Arial", 12))
        self.sheet_selector_label.pack(pady=5)

        self.sheet_selector = ttk.Combobox(root, state="readonly", width=40)
        self.sheet_selector.pack(pady=5)
        self.sheet_selector.bind("<<ComboboxSelected>>", self.on_sheet_select)

        # Table View Frame with Scrollbars
        self.table_frame = tk.Frame(root, bd=2, relief=tk.SUNKEN)
        self.table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.tree = ttk.Treeview(self.table_frame, columns=(), show="headings", selectmode="browse")
        self.tree.grid(row=0, column=0, sticky="nsew")

        # Scrollbars
        self.scrollbar_y = ttk.Scrollbar(self.table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.scrollbar_y.grid(row=0, column=1, sticky="ns")
        self.scrollbar_x = ttk.Scrollbar(self.table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.scrollbar_x.grid(row=1, column=0, sticky="ew")

        self.tree.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)

        # Configure table frame to expand properly
        self.table_frame.rowconfigure(0, weight=1)
        self.table_frame.columnconfigure(0, weight=1)

        # Action Buttons Frame
        self.buttons_frame = tk.Frame(root)
        self.buttons_frame.pack(fill=tk.X, pady=10)

        self.open_file_button = ttk.Button(self.buttons_frame, text="Open File", command=self.open_file_dialog)
        self.open_file_button.pack(side=tk.LEFT, padx=10)

        self.insert_db_button = ttk.Button(self.buttons_frame, text="Insert All Sheets to DB",
                                           command=self.insert_sheets_to_db, state=tk.DISABLED)
        self.insert_db_button.pack(side=tk.LEFT, padx=10)

        self.remove_file_button = ttk.Button(self.buttons_frame, text="Remove File", command=self.remove_file,
                                             state=tk.DISABLED)
        self.remove_file_button.pack(side=tk.LEFT, padx=10)

        # Enable drag-and-drop
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.on_drop)

    def open_file_dialog(self):
        file_path = filedialog.askopenfilename(title="Open Excel File", filetypes=[("Excel Files", "*.xlsx")])
        if file_path:
            self.read_excel_file(file_path)

    def on_drop(self, event):
        file_path = event.data
        if file_path.endswith(".xlsx"):
            self.read_excel_file(file_path)
        else:
            messagebox.showerror("Invalid File", "Please drop a valid Excel (.xlsx) file.")

    def read_excel_file(self, file_path):
        try:
            # Read the Excel file
            self.data = pd.read_excel(file_path, sheet_name=None)
            self.instruction_label.config(text=f"Loaded file: {file_path}")
            self.insert_db_button.config(state=tk.NORMAL)
            self.remove_file_button.config(state=tk.NORMAL)

            # Populate the dropdown with sheet names
            sheet_names = list(self.data.keys())
            self.sheet_selector["values"] = sheet_names
            if sheet_names:
                self.sheet_selector.current(0)
                self.display_sheet(sheet_names[0])

        except Exception as e:
            messagebox.showerror("Error", f"Failed to read the file: {str(e)}")

    def on_sheet_select(self, event):
        selected_sheet = self.sheet_selector.get()
        if selected_sheet:
            self.display_sheet(selected_sheet)

    def display_sheet(self, sheet_name):
        try:
            df = self.data[sheet_name]
            self.update_table(df)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to display sheet: {str(e)}")

    def update_table(self, df):
        self.tree["columns"] = list(df.columns)
        for col in df.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor=tk.CENTER)

        self.tree.delete(*self.tree.get_children())
        for _, row in df.iterrows():
            self.tree.insert("", tk.END, values=list(row))

    def insert_sheets_to_db(self):
        try:
            for sheet_name, df in self.data.items():
                df = df.where(pd.notnull(df), None)
                sheet_name = sheet_name.strip().lower().replace(" ", "_")
                db.insert_data_to_db(sheet_name, df)
            messagebox.showinfo("Success", "All sheets have been inserted into the database.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to insert data into the database: {str(e)}")

    def remove_file(self):
        self.data = {}
        self.instruction_label.config(text="Drag and drop an Excel file here or click 'Open File'")
        self.sheet_selector["values"] = []
        self.sheet_selector.set("")
        self.tree.delete(*self.tree.get_children())
        self.insert_db_button.config(state=tk.DISABLED)
        self.remove_file_button.config(state=tk.DISABLED)


if __name__ == "__main__":
    import os
    import sys
    import json

    if getattr(sys, 'frozen', False):
        # The executable is running in a frozen state
        # sys.executable is the full path to the main.exe file
        base_path = os.path.dirname(sys.executable)
    else:
        # Running in normal Python environment
        base_path = os.path.dirname(os.path.abspath(__file__))

    config_path = os.path.join(base_path, "config.json")


    with open(config_path, "r") as f:
        configurations = dict(json.load(f))
    config.dbconfig=configurations["db"]
    root = TkinterDnD.Tk()
    app = ExcelReaderApp(root)
    root.mainloop()
