# 🚀 USS-Stack – Lokales RAG-System mit Pi & Ollama

**„Ich baue Systeme, die sich selbst sichern, schützen und weiterentwickeln.“**

USS-Stack (Unmanned Self-sustaining Ship) ist ein modular aufgebautes, agentenbasiertes RAG-Framework, das vollständig lokal betrieben wird – auf Raspberry Pi-Geräten und einem GPU-Windows-Tower mit Ollama.  
Ziel ist ein selbstheilendes, bootfestes System mit intelligenter Automatisierung für Updates, RAID-Überwachung, Backups und vektorbasierte KI-Abfragen.

---

## 🧠 Kernfeatures auf einen Blick

- 📦 **Unattended Upgrades** mit `ntfy` Push-Benachrichtigungen  
- 🧲 **RAID-Monitoring inkl. SMART-Checks & Emoji-Fazit**  
- 🔐 **Backup-Agent mit rclone, Tar A/B-Prinzip & sha256-Prüfsummen**  
- 🧬 **Qdrant VectorDB mit über 100k Code-Chunks**  
- 🤖 **FastAPI-RAG-Endpoint (`/ask`) zur LLM-Abfrage via Ollama**  
- 🧠 **Lokaler Ollama-LLM als Chat-Backend auf GPU-Server**  
- 🔁 **Bootfeste Einrichtung via systemd & NSSM (Windows Services)**

---

## 🏗️ Architekturübersicht

```text
[agent-pi] --(ntfy/systemd)--> [FastAPI/RAG] --> [Ollama (GPU-Tower)]
    |                             ▲
    |                             |
[raid-pi] <--- RAID / Backup ----+
       \
        > Qdrant (Vector Search)


⚙️ Technologien & Komponenten
Raspberry Pi (Agent-Node & RAID-Node)

Qdrant für Vektorsuche

FastAPI, uvicorn, Python 3, venv

rclone, smartmontools, ntfy

Ollama (lokaler LLM-Server auf Windows per nssm)

systemd-Timer & Dienste

🛠️ Setup & Installation
Detaillierte Installationsschritte findest du im unteren Teil des Repos (README oder /docs/-Ordner).

Für Schnellstarter:

# Pi: Basis-Tools & Agent-Skripte
sudo apt install unattended-upgrades ntfy rclone smartmontools

# Qdrant starten (Docker)
cd /opt/qdrant
docker compose up -d

# FastAPI-RAG-Service aktivieren
cd /opt/uss_api
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
systemctl enable uss-api.service uss-ready.service

# Windows: Ollama-Service (LLM)
winget install nomic.gpt4all
nssm install Ollama "...\ollama.exe" serve
🔍 Beispiel: RAG-Abfrage

curl -X POST http://<pi-ip>:8000/ask \
     -H "Content-Type: application/json" \
     -d '{"query":"Wie registriere ich ein Modul?","top_k":4}'
📦 Antwort: JSON mit answer + sources direkt aus deinem Code-Repo.

📜 Lizenz
Dieses Projekt steht unter CC BY-NC-SA 4.0.
→ Siehe LICENSE für Details.

🛣️ Roadmap (Next Steps)
 MMR + Cross-Encoder Re-Ranking

 Deutsch-getuntes Modell (mistral-7b-de)

 Automatisches Cleanup alter Backups

 GitHub-Monorepo mit klarer Trennung: api/, infra/, embeddings/, docs/
