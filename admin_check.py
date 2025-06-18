import ctypes
import sys

def is_admin():
    """
    Prüft, ob das Programm mit Administratorrechten ausgeführt wird.
    :return: True, wenn Admin-Rechte vorhanden sind, sonst False.
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def restart_as_admin():
    """
    Startet das Programm mit Administratorrechten neu.
    """
    try:
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, __file__, None, 1
        )
        sys.exit()  # Beendet das aktuelle Programm
    except Exception as e:
        print(f"Fehler beim Neustart mit Admin-Rechten: {e}")
        sys.exit(1)
