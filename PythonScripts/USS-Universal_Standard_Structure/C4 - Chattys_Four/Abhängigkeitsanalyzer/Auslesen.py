import tkinter as tk
from tkinter import ttk
import os
import winreg
import psutil
import ctypes
import sys
import pefile  # Für DLL-Abhängigkeiten

# Admin-Rechte prüfen und erzwingen
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()

# Alle Registry-Daten eines Programms auslesen
def get_all_registry_data(subkey):
    data = {}
    try:
        for j in range(winreg.QueryInfoKey(subkey)[1]):  # Anzahl der Werte
            value_name, value_data, _ = winreg.EnumValue(subkey, j)
            data[value_name] = value_data
    except Exception:
        pass
    return data

# Programme aus der Registry auslesen
def get_installed_programs():
    programs = []
    reg_paths = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",  # Standard-Programme
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall",  # 32-Bit-Programme
    ]
    reg_hives = [winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER]  # Beide Registry-Hives durchsuchen

    for reg_hive in reg_hives:
        for reg_path in reg_paths:
            try:
                with winreg.OpenKey(reg_hive, reg_path) as key:
                    for i in range(0, winreg.QueryInfoKey(key)[0]):  # Alle Subkeys durchgehen
                        try:
                            subkey_name = winreg.EnumKey(key, i)
                            with winreg.OpenKey(key, subkey_name) as subkey:
                                data = get_all_registry_data(subkey)
                                name = data.get("DisplayName", "Unbekannt")
                                path = data.get("InstallLocation", data.get("DisplayIcon", "Nicht angegeben"))
                                if path == "Nicht angegeben" and data.get("DisplayIcon"):
                                    path = os.path.dirname(data.get("DisplayIcon"))
                                version = data.get("DisplayVersion", "Unbekannt")
                                executable_type = ".exe" if path.endswith(".exe") else "Unbekannt"
                                programs.append({
                                    "name": name,
                                    "path": path,
                                    "type": executable_type,
                                    "version": version,
                                    "details": data  # Alle Registry-Daten speichern
                                })
                        except Exception:
                            pass
            except FileNotFoundError:
                continue

    return programs

# Laufende Prozesse hinzufügen
def get_running_processes(programs):
    for proc in psutil.process_iter(attrs=["name", "exe", "cmdline"]):
        try:
            if proc.info["exe"] and proc.info["name"]:
                already_in_programs = any(p["path"] == proc.info["exe"] for p in programs)
                if not already_in_programs:
                    programs.append({
                        "name": proc.info["name"],
                        "path": proc.info["exe"],
                        "type": ".exe",
                        "version": "Laufender Prozess",
                        "details": {}
                    })
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            pass

# DLL-Abhängigkeiten auslesen
def get_dll_dependencies(executable_path):
    try:
        pe = pefile.PE(executable_path)
        dlls = [entry.dll.decode('utf-8') for entry in pe.DIRECTORY_ENTRY_IMPORT]
        return dlls
    except Exception:
        return []

# Details anzeigen (rechte Seite)
def show_details(event):
    selected_item = program_list.selection()
    if selected_item:
        program = program_list.item(selected_item[0], "values")
        details.delete(1.0, tk.END)
        details.insert(tk.END, f"Name: {program[0]}\n", "bold")
        details.insert(tk.END, f"Typ: {program[2]}\n", "bold")
        details.insert(tk.END, f"Version: {program[3]}\n", "bold")

        # Pfad anzeigen und klickbar machen
        details.insert(tk.END, "Speicherort: ", "bold")
        details.insert(tk.END, f"{program[1]}\n", "link")
        details.tag_bind("link", "<Button-1>", lambda e, path=program[1]: open_path(path))
        details.tag_config("link", foreground="blue", underline=True, cursor="hand2")

        # Registry-Details anzeigen
        details.insert(tk.END, "\nRegistry-Daten:\n", "bold")
        full_details = programs[int(selected_item[0])]["details"]
        for key, value in full_details.items():
            details.insert(tk.END, f"{key}: ", "bold")
            details.insert(tk.END, f"{value}\n")

        # DLL-Abhängigkeiten anzeigen
        dlls = get_dll_dependencies(program[1])
        if dlls:
            details.insert(tk.END, "\nAbhängigkeiten (DLLs):\n", "bold")
            for dll in dlls:
                details.insert(tk.END, f"- {dll}\n")

# Datei oder Ordner öffnen
def open_path(path):
    try:
        if os.path.exists(path):
            os.startfile(path)
        else:
            print(f"Pfad existiert nicht: {path}")
    except Exception as e:
        print(f"Fehler beim Öffnen des Pfads: {e}")

# GUI erstellen
root = tk.Tk()
root.title("Programm-Abhängigkeits-Dashboard")
root.geometry("1200x700")

# Linke Programmliste mit Scrollbar
frame_left = tk.Frame(root)
frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(frame_left, orient=tk.VERTICAL)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

program_list = ttk.Treeview(frame_left, columns=("name", "path", "type", "version"), show="headings", yscrollcommand=scrollbar.set)
scrollbar.config(command=program_list.yview)

program_list.heading("name", text="Name")
program_list.heading("path", text="Speicherort")
program_list.heading("type", text="Typ")
program_list.heading("version", text="Version")
program_list.column("name", width=300)
program_list.column("path", width=400)
program_list.column("type", width=100)
program_list.column("version", width=100)

# Programme dynamisch laden
programs = get_installed_programs()
get_running_processes(programs)  # Laufende Prozesse hinzufügen
for idx, prog in enumerate(programs):
    program_list.insert("", tk.END, values=(prog["name"], prog["path"], prog["type"], prog["version"]), iid=str(idx))

program_list.bind("<ButtonRelease-1>", show_details)
program_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Rechte Details-Seite
details = tk.Text(root, wrap=tk.WORD)
details.tag_config("bold", font=("TkDefaultFont", 10, "bold"))
details.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

root.mainloop()
