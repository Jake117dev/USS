import tkinter as tk
from tkinter import ttk
import os

# Beispiel-Daten
programs = [
    {"name": "Photoshop.exe", "category": "Anwendung", "type": ".exe", "path": "C:\\Programme\\Adobe"},
    {"name": "AntivirusService", "category": "Systemdienst", "type": ".exe", "path": "C:\\System"},
    {"name": "BackupUtility.dll", "category": "Utility", "type": ".dll", "path": "C:\\Tools"},
]

# Funktion zum Öffnen von Dateien/Ordnern
def open_path(path):
    try:
        os.startfile(path)  # Funktioniert unter Windows
    except Exception as e:
        print(f"Fehler beim Öffnen des Pfads: {e}")

# Details anzeigen (rechte Seite)
def show_details(event):
    selected_item = program_list.selection()
    if selected_item:
        program = program_list.item(selected_item[0], "values")
        details.delete(1.0, tk.END)

        # Details einfügen
        details.insert(tk.END, f"Name: {program[0]}\n")
        details.insert(tk.END, f"Kategorie: {program[1]}\n")
        details.insert(tk.END, f"Typ: {program[2]}\n")

        # Pfad klickbar machen
        details.insert(tk.END, "Speicherort: ", "normal")
        details.insert(tk.END, f"{program[3]}\n", "link")
        details.tag_bind("link", "<Button-1>", lambda e, path=program[3]: open_path(path))
        details.tag_config("link", foreground="blue", underline=True)

        # Beispiel-Abhängigkeiten
        details.insert(tk.END, "\nAbhängigkeiten:\n- DLL_XYZ.dll\n- Service_A\n- Cert_ABC.crt\n", "normal")
        details.tag_config("normal", foreground="black")

# GUI erstellen
root = tk.Tk()
root.title("Programm-Abhängigkeits-Dashboard")
root.geometry("1000x600")

# Linke Programmliste mit Scrollbar
frame_left = tk.Frame(root)
frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(frame_left, orient=tk.VERTICAL)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

program_list = ttk.Treeview(frame_left, columns=("name", "category", "type", "path"), show="headings", yscrollcommand=scrollbar.set)
scrollbar.config(command=program_list.yview)

program_list.heading("name", text="Name")
program_list.heading("category", text="Kategorie")
program_list.heading("type", text="Typ")
program_list.heading("path", text="Speicherort")
program_list.column("name", width=200)
program_list.column("category", width=150)
program_list.column("type", width=100)
program_list.column("path", width=400)

# Programme hinzufügen
for prog in programs:
    program_list.insert("", tk.END, values=(prog["name"], prog["category"], prog["type"], prog["path"]))

program_list.bind("<ButtonRelease-1>", show_details)
program_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Rechte Details-Seite
details = tk.Text(root, wrap=tk.WORD)
details.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

root.mainloop()
