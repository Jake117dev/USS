from admin_check import is_admin, restart_as_admin
import winreg

def initialize_module():
    """
    Initialisierung des Moduls:
    - Admin-Rechte prüfen und ggf. anfordern
    - Registry-Zugriff testen
    """
    # Schritt 1: Admin-Check
    if not is_admin():
        print("Admin-Rechte erforderlich. Programm wird neu gestartet...")
        restart_as_admin()

    # Schritt 2: Registry-Zugriff prüfen
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE"):
            print("Registry-Zugriff erfolgreich.")
        return True
    except PermissionError:
        print("Fehler: Keine Berechtigung, auf die Registry zuzugreifen.")
        return False
    except Exception as e:
        print(f"Unbekannter Fehler bei der Registry-Initialisierung: {e}")
        return False
