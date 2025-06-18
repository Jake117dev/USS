import tkinter as tk
from tkinter import ttk
import subprocess
import threading

# Funktion für DISM-Befehle
def run_dism(command, description):
    def execute_dism():
        result_text.insert(tk.END, f"{description}...\n")
        output = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True)
        result_text.insert(tk.END, f"{description} abgeschlossen:\n")
        result_text.insert(tk.END, output.stdout + "\n")
    
    threading.Thread(target=execute_dism).start()

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
root.geometry("600x400")
root.configure(bg="#1c1c1c")  # Dunkler Hintergrund

# Buttons
btn_checkhealth = tk.Button(
    root, text="DISM CheckHealth", 
    command=lambda: run_dism("DISM /Online /Cleanup-Image /CheckHealth", "DISM CheckHealth"),
    bg="#00bcd4", fg="white", relief="flat"
)
btn_scanhealth = tk.Button(
    root, text="DISM ScanHealth", 
    command=lambda: run_dism("DISM /Online /Cleanup-Image /ScanHealth", "DISM ScanHealth"),
    bg="#00bcd4", fg="white", relief="flat"
)
btn_restorehealth = tk.Button(
    root, text="DISM RestoreHealth", 
    command=lambda: run_dism("DISM /Online /Cleanup-Image /RestoreHealth", "DISM RestoreHealth"),
    bg="#00bcd4", fg="white", relief="flat"
)

# Tooltip hinzufügen
Tooltip(btn_checkhealth, "Prüft, ob das Image beschädigt ist.")
Tooltip(btn_scanhealth, "Führt eine tiefere Analyse des Images durch.")
Tooltip(btn_restorehealth, "Repariert das beschädigte Windows-Image.")

# Ergebnisfeld
result_text = tk.Text(root, height=15, width=70, bg="#333333", fg="white", wrap="word", borderwidth=0)

# Layout
btn_checkhealth.pack(pady=5)
btn_scanhealth.pack(pady=5)
btn_restorehealth.pack(pady=5)
result_text.pack(pady=10)

# Hauptschleife
root.mainloop()
