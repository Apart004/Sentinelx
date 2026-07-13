# ADR-001: Python Stack Selection for SentinelX

- **Status:** Accepted
- **Date:** 2025-01-01
- **Deciders:** Ansh (Apart004)
- **Tags:** `language`, `tooling`, `infrastructure`

---

## Context

SentinelX is an open-source Blue Team Detection & Threat Intelligence Platform. Before writing any application code, a foundational stack had to be chosen covering:

1. **Primary language** — what the platform is built in
2. **Dependency and build management** — how packages and project metadata are managed
3. **Code quality tooling** — formatter, linter, import sorter
4. **Testing framework** — how correctness is verified
5. **Configuration and secrets management** — how the platform is configured at runtime
6. **Structured logging** — how operational events are recorded
7. **Runtime environment** — how the platform is isolated and deployed
8. **Data persistence** — what database backs threat intelligence and detection data
9. **CI/CD** — how changes are validated automatically

These choices affect every subsequent phase of the project (Phases 1–9) and are expensive to change once code accumulates. The goal was a stack that is:

- Dominant in the security tooling ecosystem
- Low ceremony for a solo or small-team open-source project
- Enforces consistent quality without manual overhead
- Familiar to hiring managers and contributors reviewing a portfolio project

---

## Decision

### Language: Python 3.11+

Python was chosen as the primary language. It is the de facto standard for security tooling — the majority of open-source SIEM integrations, threat intelligence libraries (MISP, OpenCTI connectors, STIX/TAXII clients), and detection frameworks are Python-first. This maximises the available ecosystem for future phases and ensures the codebase is immediately legible to security engineers reviewing the project.

Alternative considered: **Go** — strong for high-throughput network tooling, but the security library ecosystem is thinner and the barrier for contributors is higher.

### Build & Dependency Management: `pyproject.toml` + `pip`

A single `pyproject.toml` (PEP 517/518) was chosen as the canonical project descriptor over the legacy `setup.py` + `requirements.txt` pattern. This colocates project metadata, dependencies, and tool configuration in one file, which is the current Python community standard. `pip` handles installs to keep tooling requirements minimal for contributors.

Alternative considered: **Poetry** — provides lockfile-based reproducibility but adds a non-standard CLI that can confuse contributors unfamiliar with it. Deferred until lockfile reproducibility becomes a concrete need.

### Formatter: Black

Black was chosen for code formatting. It is deliberately opinionated and produces a single canonical format with no configuration surface, eliminating all style debates. Its `--check` mode integrates cleanly into CI with a zero-config pass/fail signal.

### Linter: Ruff

Ruff was chosen as the linter. It reimplements the rule sets of Flake8, pycodestyle, and dozens of plugins in Rust, running orders of magnitude faster than the equivalents it replaces. For a project that will accumulate significant code across nine phases, fast feedback in CI matters. Its configuration lives in `pyproject.toml` alongside all other tool config.

Alternative considered: **Flake8** — slower, fragmented plugin ecosystem, separate config file required.

### Import Sorter: isort

isort was chosen to enforce consistent import ordering (stdlib → third-party → local). Black handles formatting; isort handles import structure. The two are configured to be compatible via the `profile = "black"` setting in `pyproject.toml`.

### Testing Framework: pytest

pytest was chosen over the standard library `unittest` module. It produces more readable test output, supports fixture-based setup/teardown, and has a rich plugin ecosystem (coverage, parametrize, async). The security community overwhelmingly uses pytest for Python tooling.

### Configuration & Secrets: `config.yaml` + `.env` + `python-dotenv` + `pydantic`

A layered configuration system was chosen:

- `config/config.yaml` — non-secret structured configuration (ports, paths, feature flags)
- `.env` (gitignored) — secrets and environment-specific overrides
- `python-dotenv` — loads `.env` at runtime
- `pydantic` — provides typed, validated settings objects that fail fast on misconfiguration

This pattern mirrors production-grade 12-factor application design and is immediately understandable to engineers from any background. Secrets are never committed; `.env.example` documents required variables.

Alternative considered: **Dynaconf** — more powerful multi-environment support but heavier, and the layered yaml+dotenv pattern covers all Phase 0–5 needs.

### Structured Logging: Loguru

Loguru was chosen over the standard library `logging` module. It provides structured, coloured output with zero boilerplate — `from loguru import logger` is sufficient. For a security platform, log quality is critical; structured JSON logs (configurable via Loguru sinks) are a prerequisite for future SIEM integration in Phase 3.

Alternative considered: **structlog** — more explicit structured logging, better for high-volume pipelines, but heavier setup for initial phases. Can be introduced later as a sink.

### Runtime Isolation & Deployment: Docker + Docker Compose

Docker was chosen to containerise the platform. This ensures environment reproducibility across development, CI, and any future lab or cloud deployment. Docker Compose orchestrates the multi-service topology (application + database) via a single `docker-compose.yml`.

The development workflow uses a local Python venv for iteration speed; Docker is used for integration testing and deployment packaging.

### Data Persistence: MongoDB (via Docker)

MongoDB was chosen as the primary data store for threat intelligence and detection artefacts. Threat intelligence data (IOCs, STIX bundles, enrichment results) is inherently document-shaped and schema-volatile — new intelligence formats cannot require a migration. MongoDB's flexible document model handles this cleanly. The official `motor` async driver will be used in application code.

Alternative considered: **PostgreSQL with JSONB** — excellent for structured data with JSONB escape hatches, but the relational overhead is unnecessary for the schema-flexible IOC/event data SentinelX will handle. PostgreSQL may be introduced in later phases for structured reporting data.

### CI/CD: GitHub Actions

GitHub Actions was chosen for CI. It is natively integrated with the GitHub repository, requires no external service, and has a large marketplace of actions. The CI pipeline runs on every push and pull request and enforces: Black format check, Ruff lint, isort check, and pytest. A passing CI badge is visible on the README.

---

## Consequences

### Positive

- The entire stack is expressible in `pyproject.toml` — one file governs the project
- All quality gates (format, lint, test) run automatically in CI with no manual steps
- Python's security ecosystem is fully accessible for all subsequent phases
- MongoDB's schema flexibility avoids migration overhead during the rapid early phases
- Docker ensures the platform runs identically in development and any deployment target

### Negative / Trade-offs

- **No lockfile:** `pyproject.toml` without Poetry or pip-compile means dependency versions are not pinned to an exact hash. Acceptable for a portfolio project; a `requirements-lock.txt` can be added before any production deployment.
- **MongoDB operational overhead:** Running MongoDB locally requires Docker to be running during development. Mitigated by making Docker opt-in (not started automatically) during code-only sessions.
- **Python GIL:** CPU-bound detection tasks may hit Python's Global Interpreter Lock. If Phase 3 detection workloads prove CPU-bound, async I/O (already available via `motor`) or subprocess-based parallelism can be introduced without changing the stack.

---

## References

- [PEP 517 – A build-system independent format for source trees](https://peps.python.org/pep-0517/)
- [PEP 518 – Specifying minimum build system requirements](https://peps.python.org/pep-0518/)
- [Black documentation](https://black.readthedocs.io/)
- [Ruff documentation](https://docs.astral.sh/ruff/)
- [Loguru documentation](https://loguru.readthedocs.io/)
- [12-Factor App — Config](https://12factor.net/config)
- [MITRE ATT&CK](https://attack.mitre.org/) — threat model reference for Phase 3+