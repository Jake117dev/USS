import tkinter as tk
import subprocess
import threading

# Funktion für SFC /Scannow
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
btn_sfc = tk.Button(root, text="SFC /Scannow", command=run_sfc, bg="#00bcd4", fg="white", relief="flat")

# Ergebnisfeld
result_text = tk.Text(root, height=15, width=70, bg="#333333", fg="white", wrap="word", borderwidth=0)

# Layout
btn_sfc.pack(pady=10)
result_text.pack(pady=10)

# Hauptschleife
root.mainloop()
