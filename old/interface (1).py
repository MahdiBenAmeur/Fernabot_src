import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from tkinterdnd2 import TkinterDnD, DND_FILES
import db

class ExcelReaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Excel File Reader")
        self.root.geometry("600x400")

        self.label = tk.Label(root, text="Drag and drop an Excel file here or click 'Open File'", anchor='center')
        self.label.pack(pady=20)

        # Text widget to display the Excel file content
        self.text_area = tk.Text(root, wrap=tk.WORD, height=10, width=60)
        self.text_area.config(state=tk.DISABLED)  # Make it read-only
        self.text_area.pack(pady=10)

        # Open file button
        self.open_file_button = tk.Button(root, text="Open File", command=self.open_file_dialog)
        self.open_file_button.pack(pady=10)

        # Insert data to DB button
        self.insert_db_button = tk.Button(root, text="Insert All Sheets to DB", command=self.insert_sheets_to_db)
        self.insert_db_button.pack(pady=10)

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
            # Read the Excel file using pandas, let it use the first row as header
            self.data = pd.read_excel(file_path, sheet_name=None)  # No need to skip rows
            self.label.config(text=f"Loaded file: {file_path}")
            self.text_area.config(state=tk.NORMAL)  # Enable text area to insert text
            self.text_area.delete(1.0, tk.END)  # Clear the text area before inserting new data

            # Display the names of all sheets
            sheet_names = "\n".join(self.data.keys())
            self.text_area.insert(tk.END, f"Sheets:\n{sheet_names}")  # Display sheet names
            self.text_area.config(state=tk.DISABLED)  # Make it read-only again
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read the file: {str(e)}")

    def insert_sheets_to_db(self):
        try:
            db.insert_courses_to_db(self.data["courses"])
            self.data["entrep"] = self.data["entrep"].where(pd.notnull(self.data["entrep"]), None)
            db.insert_entrep_to_db(self.data["entrep"])
            db.insert_emplois_to_db(self.data["emplois"])
            db.insert_scholars_Fellowships_internship_to_db(self.data["scholars Fellowships internship"])

            messagebox.showinfo("Success", "All sheets have been inserted into the database.")
        except Exception as e:
            print("Error", f"Failed to insert data into the database: {str(e)}")

if __name__ == "__main__":
    root = TkinterDnD.Tk()  # Use TkinterDnD.Tk() instead of standard Tk()
    app = ExcelReaderApp(root)
    root.mainloop()
