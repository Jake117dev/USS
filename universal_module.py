import sys
import os

# Modulordner "modules" zum Pythonpfad hinzufügen
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

from admin_check import is_admin, restart_as_admin
from registry_module import initialize_module

def universal_module():
    """
    Hauptmodul: Startet mit Initialisierung und Admin-Check.
    """
    if not initialize_module():
        print("Initialisierung fehlgeschlagen. Programm wird beendet.")
        return None
    
    print("Initialisierung erfolgreich! Weiter mit Input...")
    # Hier folgt der Input-Schritt
