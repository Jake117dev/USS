import tkinter as tk
from tkinter import ttk
import subprocess
import threading

# Funktion für Prozesse
def run_process(command, description):
    def execute_process():
        insert_result(f"{description} gestartet...\n", "info")
        output = subprocess.run(["powershell", "-Command", command], capture_output=True, text=True)
        if output.returncode == 0:
            insert_result(f"{description} abgeschlossen:\n", "success")
        else:
            insert_result(f"{description} fehlgeschlagen:\n", "error")
        insert_result(output.stdout + "\n", "output")
    
    threading.Thread(target=execute_process).start()

# Funktion zum Einfügen von Ergebnissen mit Formatierung
def insert_result(text, tag):
    result_text.configure(state="normal")  # Entsperren des Textfelds
    result_text.insert(tk.END, text, tag)
    result_text.configure(state="disabled")  # Wieder sperren
    result_text.see(tk.END)  # Automatisches Scrollen

# GUI erstellen
root = tk.Tk()
root.title("Cyberpunk Dashboard")
root.geometry("600x500")
root.configure(bg="#1c1c1c")  # Dunkler Hintergrund

# Buttons
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

# Scrollbarer Ergebnisbereich
frame_result = tk.Frame(root)
frame_result.pack(pady=10, fill=tk.BOTH, expand=True)
scrollbar = tk.Scrollbar(frame_result)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

result_text = tk.Text(frame_result, height=15, width=70, bg="#333333", fg="white", wrap="word", borderwidth=0, yscrollcommand=scrollbar.set)
result_text.tag_configure("info", foreground="#00bcd4")
result_text.tag_configure("success", foreground="green")
result_text.tag_configure("error", foreground="red")
result_text.tag_configure("output", foreground="white")
result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar.config(command=result_text.yview)

# Layout der Buttons
btn_updates.pack(pady=5)
btn_sfc.pack(pady=5)
btn_checkhealth.pack(pady=5)
btn_scanhealth.pack(pady=5)
btn_restorehealth.pack(pady=5)

# Hauptschleife
root.mainloop()
