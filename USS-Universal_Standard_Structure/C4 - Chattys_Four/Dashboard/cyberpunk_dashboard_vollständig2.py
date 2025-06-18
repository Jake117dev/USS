import tkinter as tk
from tkinter import ttk
import subprocess
import threading

# Funktion für Prozesse
def run_process(command, description):
    def execute_process():
        result_text.insert(tk.END, f"{description}...\n")
        output = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True)
        result_text.insert(tk.END, f"{description} abgeschlossen:\n")
        result_text.insert(tk.END, output.stdout + "\n")
    
    threading.Thread(target=execute_process).start()

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
root.geometry("600x500")
root.configure(bg="#1c1c1c")  # Dunkler Hintergrund

# Buttons für Winget, SFC und DISM
btn_updates = tk.Button(
    root, text="Winget Updates prüfen", 
    command=lambda: run_process("winget upgrade --all --include-unknown", "Winget Updates prüfen"),
    bg="#00bcd4", fg="white", relief="flat"
)
btn_sfc = tk.Button(
    root, text="SFC /Scannow", 
    command=lambda: run_process("sfc /scannow", "SFC /Scannow durchführen"),
    bg="#00bcd4", fg="white", relief="flat"
)
btn_checkhealth = tk.Button(
    root, text="DISM CheckHealth", 
    command=lambda: run_process("DISM /Online /Cleanup-Image /CheckHealth", "DISM CheckHealth"),
    bg="#00bcd4", fg="white", relief="flat"
)
btn_scanhealth = tk.Button(
    root, text="DISM ScanHealth", 
    command=lambda: run_process("DISM /Online /Cleanup-Image /ScanHealth", "DISM ScanHealth"),
    bg="#00bcd4", fg="white", relief="flat"
)
btn_restorehealth = tk.Button(
    root, text="DISM RestoreHealth", 
    command=lambda: run_process("DISM /Online /Cleanup-Image /RestoreHealth", "DISM RestoreHealth"),
    bg="#00bcd4", fg="white", relief="flat"
)

# Tooltips hinzufügen
Tooltip(btn_updates, "Zeigt verfügbare Updates für installierte Anwendungen an.")
Tooltip(btn_sfc, "Überprüft und repariert beschädigte Systemdateien.")
Tooltip(btn_checkhealth, "Prüft, ob das Windows-Image beschädigt ist.")
Tooltip(btn_scanhealth, "Führt eine detaillierte Analyse des Images durch.")
Tooltip(btn_restorehealth, "Repariert das beschädigte Windows-Image.")

# Ergebnisfeld
result_text = tk.Text(root, height=15, width=70, bg="#333333", fg="white", wrap="word", borderwidth=0)

# Layout
btn_updates.pack(pady=5)
btn_sfc.pack(pady=5)
btn_checkhealth.pack(pady=5)
btn_scanhealth.pack(pady=5)
btn_restorehealth.pack(pady=5)
result_text.pack(pady=10)

# Hauptschleife
root.mainloop()
