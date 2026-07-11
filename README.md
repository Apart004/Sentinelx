# SentinelX

> Open-source Blue Team Detection & Threat Intelligence Platform

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Status](https://img.shields.io/badge/status-active%20development-orange.svg)
![CI](https://github.com/Apart004/Sentinelx/actions/workflows/ci.yml/badge.svg)

SentinelX is an open-source platform for blue team analysts and security engineers. It automatically collects threat intelligence from multiple feeds, detects attacks using Sigma and YARA rules, enriches indicators of compromise, and automates incident response — all self-hosted, all offline-capable.

Built as a long-term project to learn and demonstrate real blue team engineering skills.

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                        SentinelX                        │
├──────────────┬──────────────┬───────────────────────────┤
│   Collectors │   Detection  │       Enrichment          │
│              │              │                           │
│ • AbuseIPDB  │ • Sigma rules│ • VirusTotal              │
│ • URLHaus    │ • YARA rules │ • AbuseIPDB               │
│ • MalwareBaz │ • MITRE map  │ • GeoIP                   │
│ • AlienVault │ • Alert gen  │ • Shodan                  │
│ • Feodo      │              │ • WHOIS                   │
├──────────────┴──────────────┴───────────────────────────┤
│                     MongoDB Database                     │
├─────────────────────────────────────────────────────────┤
│                   FastAPI REST API                       │
├─────────────────────────────────────────────────────────┤
│              React Dashboard (Web UI)                    │
├─────────────────────────────────────────────────────────┤
│                SOAR Automation Engine                    │
│         (Playbooks → Block IP, Notify, Log)             │
├─────────────────────────────────────────────────────────┤
│              AI Assistant (Local LLM via Ollama)        │
└─────────────────────────────────────────────────────────┘
```

---

## Current Status

| Phase | Description | Status |
|-------|-------------|--------|
| Phase 0 | Professional Foundation | 🔄 In Progress |
| Phase 1 | Threat Intelligence Engine | ⏳ Pending |
| Phase 2 | Home Lab Setup | ⏳ Pending |
| Phase 3 | Detection Engine | ⏳ Pending |
| Phase 4 | IOC Enrichment | ⏳ Pending |
| Phase 5 | Web UI | ⏳ Pending |
| Phase 6 | Incident Response | ⏳ Pending |
| Phase 7 | SOAR Automation | ⏳ Pending |
| Phase 8 | AI Assistant | ⏳ Pending |
| Phase 9 | Polish & Docs | ⏳ Pending |

---

## Getting Started

### Prerequisites
- Python 3.11+
- Docker + Docker Compose
- Git

### Installation

```bash
git clone https://github.com/Apart004/Sentinelx.git
cd Sentinelx
python3 -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.11+ |
| Database | MongoDB |
| API | FastAPI |
| Frontend | React + Vite |
| Detection | Sigma Rules, YARA |
| Containers | Docker + Docker Compose |
| CI/CD | GitHub Actions |
| AI | Ollama (local LLM) |

---

## License

MIT — see [LICENSE](LICENSE) for details.