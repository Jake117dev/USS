import tkinter as tk
from tkinter import ttk
import subprocess
import threading
import psutil
import time

# Globale Variablen für Netzwerkstatistiken
last_bytes_recv = psutil.net_io_counters().bytes_recv
last_bytes_sent = psutil.net_io_counters().bytes_sent
last_update_time = time.time()

# Funktion für Prozesse mit Ladebalken
def run_process_with_progressbar(command, description):
    def execute_process():
        start_progressbar()  # Ladebalken starten
        result_text.delete("1.0", tk.END)  # Ergebnisfeld leeren
        result_text.insert(tk.END, f"{description} gestartet...\n", "info")
        
        try:
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

# Systemressourcen und Netzwerkauslastung in Echtzeit anzeigen
def update_system_resources():
    global last_bytes_recv, last_bytes_sent, last_update_time

    # CPU und RAM
    cpu_label.config(text=f"CPU: {psutil.cpu_percent()}%")
    memory = psutil.virtual_memory()
    ram_label.config(text=f"RAM: {memory.percent}%")
    disk = psutil.disk_usage('/')
    disk_label.config(text=f"Disk: {disk.percent}%")

    # Netzwerk
    current_bytes_recv = psutil.net_io_counters().bytes_recv
    current_bytes_sent = psutil.net_io_counters().bytes_sent
    current_time = time.time()

    # Geschwindigkeit berechnen
    elapsed_time = current_time - last_update_time
    download_speed = (current_bytes_recv - last_bytes_recv) / elapsed_time
    upload_speed = (current_bytes_sent - last_bytes_sent) / elapsed_time

    # Werte aktualisieren
    last_bytes_recv = current_bytes_recv
    last_bytes_sent = current_bytes_sent
    last_update_time = current_time

    # Anzeige aktualisieren
    net_label.config(text=f"Netzwerk: ↓ {download_speed/1024:.2f} KB/s ↑ {upload_speed/1024:.2f} KB/s")

    # Alle 1 Sekunde aktualisieren
    root.after(1000, update_system_resources)

# Funktion für Tooltip
class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        widget.bind("<Enter>", self.show_tooltip)
        widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event):
        if self.tooltip_window:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")
        label = tk.Label(
            self.tooltip_window, text=self.text, bg="yellow", fg="black",
            font=("Arial", 10, "normal"), relief="solid", borderwidth=1
        )
        label.pack()

    def hide_tooltip(self, event):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

# GUI erstellen
root = tk.Tk()
root.title("Cyberpunk Dashboard")
root.geometry("500x350")
root.configure(bg="#1c1c1c")

# Frames für Layout
frame_buttons = tk.Frame(root, bg="#1c1c1c")
frame_buttons.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

frame_resources = tk.Frame(root, bg="#1c1c1c")
frame_resources.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)

# Buttons mit Rasteranordnung
buttons = [
    ("Winget Updates", "winget upgrade --all --include-unknown", "Prüft und aktualisiert installierte Programme."),
    ("SFC /Scannow", "sfc /scannow", "Überprüft und repariert beschädigte Systemdateien."),
    ("DISM CheckHealth", "DISM /Online /Cleanup-Image /CheckHealth", "Prüft, ob das Windows-Image beschädigt ist."),
    ("DISM ScanHealth", "DISM /Online /Cleanup-Image /ScanHealth", "Führt eine tiefere Analyse des Images durch."),
    ("DISM RestoreHealth", "DISM /Online /Cleanup-Image /RestoreHealth", "Repariert das beschädigte Windows-Image.")
]

for idx, (text, command, tooltip) in enumerate(buttons):
    btn = tk.Button(
        frame_buttons, text=text, 
        command=lambda c=command, d=text: run_process_with_progressbar(c, d),
        bg="#00bcd4", fg="white", relief="flat", width=20
    )
    btn.grid(row=idx // 2, column=idx % 2, padx=10, pady=5)
    Tooltip(btn, tooltip)

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

net_label = tk.Label(frame_resources, text="Netzwerk: --", bg="#1c1c1c", fg="cyan", font=("Arial", 10))
net_label.pack(side=tk.LEFT, padx=10)

# Hauptschleife mit Systemressourcen-Update
update_system_resources()
root.mainloop()
