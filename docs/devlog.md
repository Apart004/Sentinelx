# SentinelX Development Log

A day-by-day record of building SentinelX. One line per session — newest entry on top.

---

2026-07-15 — fixed IOC model enum serialization, schema now produces clean string output

2026-07-14 — designed IOC data schema (database/models.py) with pydantic, started Phase 1 on branch phase-1-threat-intel

2026-07-13 — wrote ADR-001 (Python stack decision record), completing Phase 0

2026-07-12 — wrote architecture.md with full system diagram, component breakdown, data flow

2026-07-11 — set up GitHub Actions CI (black, ruff, isort); first green build in 14s

2026-07-09 — added Docker setup (Dockerfile, docker-compose.yml with MongoDB + app container)

2026-07-05 — set up structured logging with loguru (console + file output, rotation, retention)

2026-07-02 — built config system (config.yaml + .env + loader.py), added pyyaml dependency

2026-06-27 — added base dependencies (pydantic, python-dotenv, loguru), fixed pyproject.toml package discovery

2026-06-25 — added community health files (CHANGELOG, CONTRIBUTING, SECURITY, CODE_OF_CONDUCT)

2026-06-24 — wrote README with architecture overview, badges, roadmap table

2026-06-21 — scaffolded folder structure, initialized Python project