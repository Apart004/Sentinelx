# SentinelX — Architecture

## Overview

SentinelX is a modular Blue Team Detection & Threat Intelligence Platform. Each component is
independently deployable and communicates through a shared MongoDB database and internal APIs.

---

## System Diagram

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

## Component Breakdown

### Collectors (`collectors/`)
Pulls IOCs from external threat intelligence feeds on a schedule.
- Each feed has its own collector class inheriting from `CollectorBase`
- All raw IOCs are normalized into a standard schema before storage
- Deduplication runs before every insert — existing IOCs are updated, not duplicated
- Feed health is monitored; failures are logged and alerted

### Detection Engine (`detection/`)
Evaluates incoming logs against Sigma and YARA rules.
- Sigma rules are parsed from `.yml` files and executed against log entries
- Every match generates a structured alert with severity, timestamp, and raw log
- All alerts are automatically mapped to MITRE ATT&CK technique IDs
- False positive tuning supported via per-rule whitelists

### Enrichment Pipeline (`enrichment/`)
Automatically enriches every IOC in a fired alert.
- Queries VirusTotal, AbuseIPDB, Shodan, GeoIP, and WHOIS
- Results are cached in MongoDB with a 24-hour TTL to respect API rate limits
- Enrichment confidence score combines signals from multiple sources

### SOAR Engine (`soar/`)
Automates response actions when playbook conditions are met.
- Playbooks define trigger conditions and ordered action lists
- Actions include: email, Slack/Discord webhook, firewall block, GitHub issue
- Every action is logged with timestamp and result
- Manual override available per alert

### API Layer (`api/`)
FastAPI REST API exposing all platform data.
- JWT authentication on all endpoints
- OpenAPI docs auto-generated at `/docs`
- Rate limiting on all public endpoints

### AI Assistant (`ai/`)
Local LLM integration for analyst assistance.
- Runs via Ollama — fully offline, no data leaves the network
- Explains alerts in plain English
- Summarizes case timelines
- Suggests Sigma rules from log patterns

---

## Data Flow
External Feed → Collector → Normalizer → MongoDB (iocs)
│
Log Source → Detection Engine → Alert → MongoDB (alerts)
│
├── Enrichment Pipeline → MongoDB (enrichment)
│
├── SOAR Engine → Actions (block, notify, log)
│
└── Case Management → MongoDB (cases)
│
FastAPI → React UI
│
AI Assistant

---

## Technology Decisions

See [`docs/adr/`](adr/) for full Architecture Decision Records.

| Decision | Choice | Reason |
|----------|--------|--------|
| Language | Python 3.11+ | Ecosystem fit for security tooling |
| Database | MongoDB | Flexible schema for varied IOC/alert shapes |
| API | FastAPI | Async, auto-docs, type-safe |
| Detection | Sigma + YARA | Industry standard formats |
| Containers | Docker + Compose | One-command deployment |
| AI | Ollama (local) | Offline-capable, no data exfiltration |

---

## Directory Structure
sentinelx/
├── collectors/     # Threat intel feed collectors
├── detection/      # Sigma/YARA detection engine
├── enrichment/     # IOC enrichment pipeline
├── database/       # MongoDB client and models
├── api/            # FastAPI REST API
├── ui/             # React frontend
├── soar/           # Playbook automation engine
├── ai/             # Local LLM integration
├── tests/          # Unit and integration tests
├── docs/           # Architecture, ADRs, devlog
├── config/         # Config loader and logging setup
└── docker/         # Docker utilities

