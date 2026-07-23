# SentinelX

> Open-source Blue Team Detection & Threat Intelligence Platform

![CI](https://github.com/Apart004/Sentinelx/actions/workflows/ci.yml/badge.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Status](https://img.shields.io/badge/status-active%20development-orange.svg)
![Phase](https://img.shields.io/badge/phase-1%20threat%20intelligence-blueviolet.svg)

SentinelX is an open-source platform for blue team analysts and security engineers. It automatically collects threat intelligence from multiple feeds, detects attacks using Sigma and YARA rules, enriches indicators of compromise, and automates incident response — all self-hosted, all offline-capable.

Built as a long-term portfolio project to demonstrate real blue team engineering skills across threat intelligence, detection engineering, incident response, and SOAR automation.

---

## Architecture

```
External Feeds (AbuseIPDB, URLHaus, MalwareBazaar, AlienVault, Feodo)
        │
        ▼
[Collectors] → [Normalizer + Deduplicator] → [MongoDB]
                                                  │
                          ┌───────────────────────┼─────────────────────┐
                          │                       │                     │
                          ▼                       ▼                     ▼
                  [Detection Engine]    [Enrichment Pipeline]    [SOAR Engine]
                  Sigma + YARA rules    VT, GeoIP, Shodan        Playbooks
                  MITRE ATT&CK map      24hr cache               Block, Notify
                          │                       │                     │
                          └───────────────────────┴─────────────────────┘
                                                  │
                                                  ▼
                                          [FastAPI REST API]
                                                  │
                                                  ▼
                                        [React Dashboard]
                                   Alerts │ IOC Search │ Cases
                                                  │
                                                  ▼
                                        [AI Assistant]
                                        Ollama (offline)
```

---

## Current Status

| Phase | Description | Status |
|-------|-------------|--------|
| Phase 0 | Professional Foundation | ✅ Complete |
| Phase 1 | Threat Intelligence Engine | 🔄 In Progress |
| Phase 2 | Home Lab Setup | ⏳ Pending |
| Phase 3 | Detection Engine | ⏳ Pending |
| Phase 4 | IOC Enrichment | ⏳ Pending |
| Phase 5 | Web UI | ⏳ Pending |
| Phase 6 | Incident Response | ⏳ Pending |
| Phase 7 | SOAR Automation | ⏳ Pending |
| Phase 8 | AI Assistant | ⏳ Pending |
| Phase 9 | Polish & Docs | ⏳ Pending |

### Phase 1 Progress — Threat Intelligence Engine

- [x] P1-T1: IOC data schema (Pydantic model)
- [x] P1-T2: MongoDB connection with connection pooling
- [x] P1-T3: IOC indexing strategy
- [ ] P1-T4: Abstract base collector class
- [ ] P1-T5: AbuseIPDB collector
- [ ] P1-T6: URLHaus collector
- [ ] P1-T7: MalwareBazaar collector
- [ ] P1-T8: AlienVault OTX collector
- [ ] P1-T9: Feodo Tracker collector
- [ ] P1-T10: IOC normalizer
- [ ] P1-T11: Deduplication logic
- [ ] P1-T12: Confidence scoring
- [ ] P1-T13: APScheduler-based scheduler
- [ ] P1-T14: Feed health monitor
- [ ] P1-T15: CLI search tool
- [ ] P1-T16: Unit tests
- [ ] P1-T17: README update

---

## What SentinelX Can Do (Phase 1 complete)

> Coming soon — IOC collection pipeline pulling real data from 5+ threat feeds

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

### Start MongoDB

```bash
docker compose up -d mongodb
```

### Run linters

```bash
black .
ruff check .
isort .
```

### Run tests

```bash
pytest
```

---

## Project Structure

```
sentinelx/
├── collectors/     # Threat intel feed collectors (AbuseIPDB, URLHaus, etc.)
├── detection/      # Sigma/YARA detection engine
├── enrichment/     # IOC enrichment pipeline (VT, GeoIP, Shodan)
├── database/       # MongoDB client, models, and indexes
├── api/            # FastAPI REST API
├── ui/             # React frontend
├── soar/           # Playbook automation engine
├── ai/             # Local LLM integration (Ollama)
├── tests/          # Unit and integration tests
├── docs/           # Architecture, ADRs, devlog
├── config/         # Config loader and logging setup
└── docker/         # Docker utilities
```

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.11+ |
| Database | MongoDB 7.0 |
| API | FastAPI |
| Frontend | React + Vite |
| Detection | Sigma Rules, YARA |
| Containers | Docker + Docker Compose |
| CI/CD | GitHub Actions |
| AI | Ollama (local LLM) |
| Data Validation | Pydantic v2 |
| Logging | Loguru |

---

## Development Log

See [`docs/devlog.md`](docs/devlog.md) for a day-by-day record of what was built each session.

---

## Documentation

- [`docs/architecture.md`](docs/architecture.md) — Full system architecture and component breakdown
- [`docs/adr/001-python-stack.md`](docs/adr/001-python-stack.md) — Architecture Decision Record: why Python, MongoDB, FastAPI

---

## Interview Talking Point

> "SentinelX is an open-source blue team platform I've been actively developing. Currently it has a working threat intelligence schema, MongoDB connection layer with indexing, Docker environment, GitHub Actions CI, and structured logging. I'm actively building the IOC collection pipeline from 5+ threat feeds. The GitHub has 30+ commits and full documentation."

---

## Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for guidelines.

## Security

See [`SECURITY.md`](SECURITY.md) for the security policy.

## License

MIT — see [`LICENSE`](LICENSE) for details.
