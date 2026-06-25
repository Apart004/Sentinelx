# Contributing to SentinelX

Thanks for your interest in contributing!

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/<your-username>/Sentinelx.git`
3. Create a feature branch: `git checkout -b feat/your-feature-name`
4. Set up your environment:
```bash
   python3 -m venv venv
   source venv/bin/activate  # Windows: .\venv\Scripts\Activate.ps1
   pip install -e ".[dev]"
```

## Before Submitting a PR

- Run `black .` to format your code
- Run `ruff check .` to lint
- Run `isort .` to sort imports
- Run `pytest` to make sure tests pass
- Follow [Conventional Commits](https://www.conventionalcommits.org/) for commit messages

## Code Style

- Line length: 100 characters
- Python 3.11+
- Type hints encouraged

## Reporting Issues

Open a GitHub Issue with as much detail as possible — logs, steps to reproduce, expected vs actual behavior.