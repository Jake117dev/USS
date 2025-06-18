import customtkinter as ctk

# Hauptfenster erstellen
root = ctk.CTk()
root.geometry("600x400")
root.title("Cyberpunk Dashboard")

# Farbschema setzen
ctk.set_appearance_mode("dark")  # Dark-Theme
ctk.set_default_color_theme("dark-blue")  # Alternativ: "blue", "green"

# Hintergrundfarbe anpassen
root.configure(bg="#1C1C1C")

# Titel-Label
title_label = ctk.CTkLabel(
    master=root, 
    text="Cyberpunk Dashboard", 
    font=("Arial", 24, "bold"), 
    text_color="#00FFFF"
)
title_label.pack(pady=20)

# Buttons mit Farbakzenten
button_1 = ctk.CTkButton(
    master=root, 
    text="Button 1", 
    fg_color="#00FFFF",  # Türkis
    hover_color="#FF00FF",  # Pink
    text_color="white",
    width=200,
    height=50,
    corner_radius=15  # Abgerundete Kanten
)
button_1.pack(pady=10)

button_2 = ctk.CTkButton(
    master=root, 
    text="Button 2", 
    fg_color="#FF00FF",  # Pink
    hover_color="#00FFFF",  # Türkis
    text_color="white",
    width=200,
    height=50,
    corner_radius=15
)
button_2.pack(pady=10)

button_3 = ctk.CTkButton(
    master=root, 
    text="Button 3", 
    fg_color="#8A2BE2",  # Lila
    hover_color="#00FFFF",  # Türkis
    text_color="white",
    width=200,
    height=50,
    corner_radius=15
)
button_3.pack(pady=10)

# Platzhalter für zukünftige Widgets
placeholder_label = ctk.CTkLabel(
    master=root, 
    text="Hier kommen weitere Widgets hin...", 
    font=("Arial", 14), 
    text_color="#FFFFFF"
)
placeholder_label.pack(pady=20)

# Hauptschleife starten
root.mainloop()
