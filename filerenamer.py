import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image
from PyPDF2 import PdfReader
from datetime import datetime
import pathlib

# Hardcoded author
AUTHOR = "JU"

# Supported file extensions
VALID_EXTENSIONS = ('.png', '.jpeg', '.jpg', '.pln', '.pdf', '.blend', '.docx', '.pptx', '.xlsx', '.mp4', '.mp3', '.zip', '.rar', '.7z', '.txt', '.md', '.csv', '.json', '.xml', '.html', '.css', '.js', '.py', '.java', '.c', '.cpp', '.h', '.hpp', '.cs', '.php', '.rb', '.sh', '.bat', '.ps1', '.sql', '.yml', '.yaml', '.toml', '.ini', '.cfg', '.conf', '.log', '.bak', '.tmp', '.temp', '.db', '.sqlite', '.db3', '.sqlitedb', '.xlsx', '.xls', '.xlsm', '.doc', '.docm', '.ppt', '.pptm', '.odt', '.ods', '.odp', '.odg', '.odf', '.ott', '.ots', '.otp', '.otg', '.otf', '.txt', '.rtf', '.csv', '.tsv', '.json', '.xml', '.html', '.css', '.js', '.py', '.java', '.c', '.cpp', '.h', '.hpp', '.cs', '.php', '.rb', '.sh', '.bat', '.ps1', '.sql', '.yml', '.yaml', '.toml', '.ini', '.cfg', '.conf', '.log', '.bak', '.tmp', '.temp', '.db', '.sqlite', '.db3', '.sqlitedb', '.xlsx', '.xls', '.xlsm', '.doc', '.docm', '.ppt', '.pptm', '.odt', '.ods', '.odp', '.odg', '.odf', '.ott', '.ots', '.otp', '.otg', '.otf', '.txt', '.rtf', '.csv', '.tsv', '.json', '.xml', '.html', '.css', '.js', '.py', '.java', '.c', '.cpp', '.h', '.hpp', '.cs', '.php', '.rb', '.sh', '.bat', '.ps1', '.sql', '.yml', '.yaml', '.toml', '.ini', '.cfg', '.conf', '.log', '.bak', '.tmp', '.temp', '.db', '.sqlite', '.db3', '.sqlitedb', '.xlsx', '.xls', '.')

def get_date_from_file(file_path):
    """Extract date from file metadata or fallback to creation date."""
    try:
        ext = os.path.splitext(file_path)[1].lower()
        if ext in ('.png', '.jpeg', '.jpg'):
            with Image.open(file_path) as img:
                exif = img._getexif()
                if exif and 36867 in exif:  # DateTimeOriginal
                    date_str = exif[36867]  # e.g., "2023:05:12 12:00:00"
                    return datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S").strftime("%Y%m%d")
        elif ext == '.pdf':
            with open(file_path, 'rb') as f:
                pdf = PdfReader(f)
                info = pdf.metadata
                if '/CreationDate' in info:
                    date_str = info['/CreationDate']  # e.g., "D:20231110120000"
                    return datetime.strptime(date_str[2:10], "%Y%m%d").strftime("%Y%m%d")
    except Exception:
        pass
    # Fallback to file creation time (macOS compatible)
    ctime = os.path.getctime(file_path)
    return datetime.fromtimestamp(ctime).strftime("%Y%m%d")

def parse_filename(filename):
    """Initial guess for NAME1 and NAME2 in camelCase."""
    base_name = os.path.splitext(filename)[0]
    words = base_name.split()
    if len(words) >= 2:
        name1 = ''.join(words[:len(words)//2])
        name2 = ''.join(words[len(words)//2:])
    else:
        name1 = base_name
        name2 = "File"
    return name1, name2

def rename_file(file_path, kind, name1, name2, version):
    """Rename a single file based on the template."""
    file_dir = os.path.dirname(file_path)
    filename = os.path.basename(file_path)
    if not filename.lower().endswith(VALID_EXTENSIONS):
        return None

    date = get_date_from_file(file_path)
    new_name = f"{date}_{AUTHOR}_{kind}_{name1}_{name2}_{version}{os.path.splitext(filename)[1]}"
    new_path = os.path.join(file_dir, new_name)
    
    if os.path.exists(new_path):
        return f"Skipped {filename}: {new_name} already exists"
    
    os.rename(file_path, new_path)
    return f"{filename} → {new_name}"

# UI Setup
class FileRenamerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Renamer")
        self.files = []
        self.preview_data = []

        # Folder picker button
        self.folder_button = tk.Button(root, text="Select Folder", command=self.select_folder)
        self.folder_button.pack(pady=10)
        self.folder_label = tk.Label(root, text="No folder selected", wraplength=300)
        self.folder_label.pack(pady=5)

        # Kind and Version selection
        options_frame = ttk.Frame(root)
        options_frame.pack(pady=5)
        
        tk.Label(options_frame, text="Kind of File:").pack(side=tk.LEFT)
        self.kind_var = tk.StringVar(value="PRSNL")
        tk.Button(options_frame, text="PRSNL", command=lambda: self.kind_var.set("PRSNL")).pack(side=tk.LEFT, padx=5)
        tk.Button(options_frame, text="UNI", command=lambda: self.kind_var.set("UNI")).pack(side=tk.LEFT, padx=5)
        tk.Label(options_frame, text="Client:").pack(side=tk.LEFT)
        self.client_entry = tk.Entry(options_frame, width=20)
        self.client_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(options_frame, text=" Version:").pack(side=tk.LEFT)
        self.version_var = tk.StringVar(value="0001a")
        tk.Button(options_frame, text="0001a", command=lambda: self.kind_var.set("0001a")).pack(side=tk.LEFT, padx=5)
        tk.Button(options_frame, text="FINAL", command=lambda: self.kind_var.set("FINAL")).pack(side=tk.LEFT, padx=5)

        # Action buttons
        action_frame = ttk.Frame(root)
        action_frame.pack(pady=5)
        tk.Button(action_frame, text="Preview", command=self.preview_files).pack(side=tk.LEFT, padx=5)
        tk.Button(action_frame, text="Set to FINAL", command=self.set_to_final).pack(side=tk.LEFT, padx=5)
        tk.Button(action_frame, text="Execute", command=self.execute_files).pack(side=tk.LEFT, padx=5)

        # Preview table
        self.tree = ttk.Treeview(root, columns=("OldName", "Date", "Kind", "Name1", "Name2", "Version"), show="headings", selectmode="extended")
        self.tree.heading("OldName", text="Old Name")
        self.tree.heading("Date", text="Date")
        self.tree.heading("Kind", text="Kind")
        self.tree.heading("Name1", text="Name1")
        self.tree.heading("Name2", text="Name2")
        self.tree.heading("Version", text="Version")
        self.tree.column("OldName", width=150)
        self.tree.column("Date", width=80)
        self.tree.column("Kind", width=80)
        self.tree.column("Name1", width=100)
        self.tree.column("Name2", width=100)
        self.tree.column("Version", width=80)
        self.tree.pack(pady=10, fill=tk.BOTH, expand=True)

        # Bind double-click to edit
        self.tree.bind("<Double-1>", self.edit_cell)

        # Log for execution results
        self.log = tk.Text(root, height=5, width=80)
        self.log.pack(pady=10)

    def select_folder(self):
        """Select a folder and load files."""
        folder = filedialog.askdirectory(title="Select Folder with Files")
        if folder:
            self.files = [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith(VALID_EXTENSIONS)]
            self.folder_label.config(text=f"Selected: {folder} ({len(self.files)} files)")
            self.preview_data = []
            self.tree.delete(*self.tree.get_children())
            self.log.delete(1.0, tk.END)

    def preview_files(self):
        """Generate editable preview table."""
        if not self.files:
            messagebox.showwarning("No Files", "Please select a folder first!")
            return

        kind = self.client_entry.get() if self.client_entry.get() else self.kind_var.get()
        version = self.version_var.get()
        self.preview_data = []
        self.tree.delete(*self.tree.get_children())

        for file_path in self.files:
            filename = os.path.basename(file_path)
            if not filename.lower().endswith(VALID_EXTENSIONS):
                continue
            date = get_date_from_file(file_path)
            name1, name2 = parse_filename(filename)
            self.preview_data.append([file_path, filename, date, kind, name1, name2, version])
            self.tree.insert("", "end", values=(filename, date, kind, name1, name2, version))

    def edit_cell(self, event):
        """Edit a cell in the Treeview."""
        item = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)
        if not item or column in ("#1", "#2"):  # Skip OldName and Date
            return

        col_idx = int(column[1:]) - 1  # Convert #N to index
        old_value = self.tree.item(item, "values")[col_idx]

        # Create entry widget for editing
        entry = tk.Entry(self.root)
        entry.place(x=event.x_root - self.root.winfo_rootx(), y=event.y_root - self.root.winfo_rooty())
        entry.insert(0, old_value)
        entry.focus_set()

        def save_edit(event):
            new_value = entry.get()
            values = list(self.tree.item(item, "values"))
            values[col_idx] = new_value
            self.tree.item(item, values=values)
            # Update preview_data
            for data in self.preview_data:
                if data[1] == values[0]:  # Match by old name
                    data[col_idx - 1] = new_value  # Adjust index for data list
            entry.destroy()

        entry.bind("<Return>", save_edit)
        entry.bind("<FocusOut>", save_edit)

    def set_to_final(self):
        """Set selected files' version to FINAL."""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select at least one file in the table!")
            return

        for item in selected:
            values = list(self.tree.item(item, "values"))
            values[5] = "FINAL"  # Version column is index 5
            self.tree.item(item, values=values)
            # Update preview_data
            for data in self.preview_data:
                if data[1] == values[0]:  # Match by old name
                    data[6] = "FINAL"  # Version is index 6 in data list

    def execute_files(self):
        """Apply renaming based on edited preview."""
        if not self.preview_data:
            messagebox.showwarning("No Preview", "Please preview files first!")
            return

        self.log.delete(1.0, tk.END)
        for file_path, _, _, kind, name1, name2, version in self.preview_data[:]:
            result = rename_file(file_path, kind, name1, name2, version)
            if result:
                self.log.insert(tk.END, f"{result}\n")
                if "Skipped" not in result:
                    self.files.remove(file_path)
                    self.preview_data.remove([file_path, _, _, kind, name1, name2, version])
        
        self.folder_label.config(text=f"Selected: {os.path.dirname(self.files[0] if self.files else '')} ({len(self.files)} files)")
        messagebox.showinfo("Done", "Files processed successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileRenamerApp(root)
    root.mainloop()