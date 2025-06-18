import tkinter as tk
import subprocess

# Funktionen für Buttons
def check_updates():
    output = subprocess.run(["powershell", "-Command", "winget upgrade --all --include-unknown"], capture_output=True, text=True)
    result_text.insert(tk.END, "Updates geprüft:\n")
    result_text.insert(tk.END, output.stdout + "\n")

def check_system_resources():
    output = subprocess.run(["powershell", "-Command", "Get-Process | Sort-Object CPU -Descending | Select-Object -First 5"], capture_output=True, text=True)
    result_text.insert(tk.END, "Systemressourcen:\n")
    result_text.insert(tk.END, output.stdout + "\n")

def run_sfc():
    def execute_sfc():
        result_text.insert(tk.END, "Starte SFC /Scannow...\n")
        output = subprocess.run(["powershell", "-Command", "sfc /scannow"], capture_output=True, text=True)
        result_text.insert(tk.END, "SFC abgeschlossen:\n")
        result_text.insert(tk.END, output.stdout + "\n")

   # Thread starten
    threading.Thread(target=execute_sfc).start()

# GUI erstellen
root = tk.Tk()
root.title("Cyberpunk Dashboard")
root.geometry("600x400")
root.configure(bg="#1c1c1c")  # Dunkler Hintergrund

# Buttons
btn_updates = tk.Button(root, text="Winget Updates prüfen", command=check_updates, bg="#00bcd4", fg="white", relief="flat")
btn_resources = tk.Button(root, text="Systemressourcen anzeigen", command=check_system_resources, bg="#00bcd4", fg="white", relief="flat")
btn_sfc = tk.Button(root, text="SFC /Scannow", command=run_sfc, bg="#00bcd4", fg="white", relief="flat")

# Ergebnisfeld
result_text = tk.Text(root, height=15, width=70, bg="#333333", fg="white", wrap="word", borderwidth=0)

# Layout
btn_updates.pack(pady=10)
btn_resources.pack(pady=10)
btn_sfc.pack(pady=10)
result_text.pack(pady=10)

# Hauptschleife
root.mainloop()
