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

```
[agent-pi] --(ntfy/systemd)--> [FastAPI/RAG] --> [Ollama (GPU-Tower)]
    |                             ▲
    |                             |
[raid-pi] <--- RAID / Backup ----+
       \
        > Qdrant (Vector Search)
```

---

## ⚙️ Technologien & Komponenten

- `Raspberry Pi` (Agent-Node & RAID-Node)
- `Qdrant` für Vektorsuche
- `FastAPI`, `uvicorn`, `Python 3`, `venv`
- `rclone`, `smartmontools`, `ntfy`
- `Ollama` (lokaler LLM-Server auf Windows per `nssm`)
- `systemd`-Timer & Dienste

---

## 🛠️ Setup & Installation

### 📦 Raspberry Pi (agent-pi & raid-pi)

```bash
sudo apt update && sudo apt install unattended-upgrades ntfy rclone smartmontools
# 50unattended-upgrades anpassen, ntfy-Hook in /etc/apt/apt.conf.d/
# raid_report.sh + backup_agent.sh nach /usr/local/bin/, cron/timer einrichten
```

### 🧬 Qdrant (VectorDB)

```bash
cd /opt/qdrant
docker compose up -d
```

### 🧠 FastAPI RAG-Endpoint

```bash
cd /opt/uss_api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
systemctl enable uss-api.service uss-ready.service
systemctl start uss-api.service
```

### 🪟 Windows (Ollama LLM-Server)

```powershell
winget install nomic.gpt4all
setx OLLAMA_HOST 0.0.0.0
setx OLLAMA_MODELS "%USERPROFILE%\.ollama\models"
nssm install Ollama "C:\Users\mrieh\AppData\Local\Programs\Ollama\ollama.exe" serve
nssm set Ollama AppDirectory "C:\Users\mrieh\AppData\Local\Programs\Ollama"
nssm start Ollama
```

---

## 🔍 Nutzung

### Beispiel-Query an den `/ask`-Endpoint:

```bash
curl -X POST http://<pi-ip>:8000/ask \
     -H "Content-Type: application/json" \
     -d '{"query":"Wie registriere ich ein Modul?","top_k":4}'
```

➡️ Antwort: JSON mit `answer` + `sources` direkt aus deinem Code-Repo.

---

## 📜 Lizenz

Dieses Projekt steht unter der [Creative Commons BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).  
Siehe [LICENSE](./LICENSE) für Details.

---

## 🛣️ Roadmap (Next Steps)

- [ ] MMR + Cross-Encoder Re-Ranking  
- [ ] Deutsch-getuntes Modell (`mistral-7b-de`)  
- [ ] Automatisches Cleanup alter Backups  
- [ ] GitHub-Monorepo mit klarer Struktur: `api/`, `infra/`, `embeddings/`, `docs/`

---

💬 **Fragen oder Ideen?** → Öffne ein Issue oder schick 'nen Pull Request.  
🧭 Bleib neugierig – das USS fährt von selbst weiter 😉
