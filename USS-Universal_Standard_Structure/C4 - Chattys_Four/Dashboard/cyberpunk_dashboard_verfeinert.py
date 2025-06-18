import tkinter as tk
from tkinter import ttk
import subprocess
import threading
import psutil  # Modul für Systemressourcen

# Funktion für Prozesse mit Ladebalken
def run_process_with_progressbar(command, description, admin=False):
    def execute_process():
        start_progressbar()  # Ladebalken starten
        result_text.delete("1.0", tk.END)  # Ergebnisfeld leeren
        result_text.insert(tk.END, f"{description} gestartet...\n", "info")
        
        try:
            if admin:
                admin_command = f'Start-Process powershell -ArgumentList "{command}" -Verb RunAs'
                process = subprocess.Popen(
                    ["powershell", "-Command", admin_command],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8"
                )
            else:
                process = subprocess.Popen(
                    ["powershell", "-Command", command],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8"
                )
            
            while process.poll() is None:
                line = process.stdout.readline()
                if line:
                    result_text.insert(tk.END, line, "output")
                    result_text.see(tk.END)  # Automatisch scrollen
            
            stop_progressbar()  # Ladebalken stoppen
            if process.returncode == 0:
                result_text.insert(tk.END, f"{description} erfolgreich abgeschlossen!\n", "success")
            else:
                error_output = process.stderr.read()
                result_text.insert(tk.END, f"{description} fehlgeschlagen:\n{error_output}\n", "error")
        except Exception as e:
            stop_progressbar()
            result_text.insert(tk.END, f"Ein Fehler ist aufgetreten: {e}\n", "error")
    
    threading.Thread(target=execute_process).start()

# Ladebalken starten/stoppen
def start_progressbar():
    progressbar.pack(pady=10)
    progressbar.start()

def stop_progressbar():
    progressbar.stop()
    progressbar.pack_forget()

# Systemressourcen in Echtzeit anzeigen
def update_system_resources():
    cpu_label.config(text=f"CPU: {psutil.cpu_percent()}%")
    memory = psutil.virtual_memory()
    ram_label.config(text=f"RAM: {memory.percent}%")
    disk = psutil.disk_usage('/')
    disk_label.config(text=f"Disk: {disk.percent}%")
    root.after(1000, update_system_resources)  # Aktualisierung alle 1 Sekunde

# GUI erstellen
root = tk.Tk()
root.title("Cyberpunk Dashboard")
root.geometry("400x300")
root.configure(bg="#1c1c1c")

# Frames für Layout
frame_buttons = tk.Frame(root, bg="#1c1c1c")
frame_buttons.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

frame_resources = tk.Frame(root, bg="#1c1c1c")
frame_resources.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

# Buttons
btn_updates = tk.Button(
    frame_buttons, text="Winget Updates", 
    command=lambda: run_process_with_progressbar("winget upgrade --all --include-unknown", "Winget Updates"),
    bg="#00bcd4", fg="white", relief="flat"
)

btn_updates.pack(pady=5)

# Ladebalken
progressbar = ttk.Progressbar(root, mode="indeterminate", length=300)

# Ergebnisfeld (kleiner)
result_text = tk.Text(root, height=4, width=40, bg="#333333", fg="white", wrap="word", borderwidth=0)
result_text.tag_configure("info", foreground="#00bcd4")
result_text.tag_configure("success", foreground="green")
result_text.tag_configure("error", foreground="red")
result_text.tag_configure("output", foreground="white")
result_text.pack(pady=5)

# Systemressourcen-Anzeige
cpu_label = tk.Label(frame_resources, text="CPU: --%", bg="#1c1c1c", fg="cyan", font=("Arial", 10))
cpu_label.pack(side=tk.LEFT, padx=10)

ram_label = tk.Label(frame_resources, text="RAM: --%", bg="#1c1c1c", fg="cyan", font=("Arial", 10))
ram_label.pack(side=tk.LEFT, padx=10)

disk_label = tk.Label(frame_resources, text="Disk: --%", bg="#1c1c1c", fg="cyan", font=("Arial", 10))
disk_label.pack(side=tk.LEFT, padx=10)

# Hauptschleife mit Systemressourcen-Update
update_system_resources()
root.mainloop()
