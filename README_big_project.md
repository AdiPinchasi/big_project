# big_project.py

A full professional Python project scaffolder. Run it once, answer a few prompts, and get a production-ready project structure with testing, Docker, CI, linting, and documentation all wired up from the start.

---

## Usage

```bash
python big_project.py
```

No installation needed — pure Python standard library.

---

## What it asks

```
Project name: my_app
Short description: A data processing pipeline
Author name: Jane Dev
  Python version detected: 3.12
Where to create it [~/projects]: /home/user/dev
Add GitHub Actions CI workflow? (Y/n): y
Add pre-commit config? (Y/n): y
Initialise a git repository? (Y/n): y
Create a virtual environment? (Y/n): y
Virtual environment name [.venv]:
Where to create the venv [...]:
```

---

## What it creates

```
my_app/
├── src/
│   ├── __init__.py
│   ├── main.py
│   └── config.py
├── tests/
│   ├── __init__.py
│   └── test_main.py
├── docs/
│   └── index.md
├── scripts/
│   └── run.sh
├── config/
│   └── settings.yaml
├── .github/
│   └── workflows/
│       └── ci.yml
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── .env
├── .env.example
├── .gitignore
├── .pre-commit-config.yaml
├── CHANGELOG.md
├── LICENSE
└── README.md
```

---

## File and Folder Descriptions

### `src/`

The heart of your project — all application source code lives here. Keeping code in `src/` (rather than the root) prevents accidental imports of uninstalled code and keeps the root directory clean.

---

#### `src/__init__.py`

Marks `src/` as a Python package so you can do `from src.config import Config` anywhere in your project. Pre-filled with a package docstring. Add package-level imports or a `__version__` string here as the project matures.

---

#### `src/main.py`

The entry point of the application. Contains a `main()` function that is called when the script is run directly or via the CLI command defined in `pyproject.toml`. Start building your application logic here.

```bash
python src/main.py
```

---

#### `src/config.py`

A `Config` class that reads all configuration from environment variables. Centralising config here means the rest of your code never calls `os.getenv()` directly — it imports from `config` instead, making it easy to see all settings in one place and swap values between environments.

```python
from src.config import Config

if Config.DEBUG:
    print("Running in debug mode")
```

---

### `tests/`

The test suite. Keeping tests in a separate top-level folder (rather than inside `src/`) is the standard Python convention and makes it clear what is application code and what is test code.

---

#### `tests/__init__.py`

Marks `tests/` as a Python package. Required for pytest to correctly resolve imports when running tests.

---

#### `tests/test_main.py`

A starter smoke test that imports and calls `main()` to verify the entry point runs without raising an exception. Use this as the template for all future tests — one test file per source module is a good default convention.

```bash
pytest
```

---

### `docs/`

Project documentation. Keeping docs in a dedicated folder makes it easy to later plug in a documentation generator like MkDocs or Sphinx.

---

#### `docs/index.md`

The root page of your documentation, pre-filled with the project name, description, and placeholder sections for API reference and architecture notes. Edit this to document how your project works at a high level.

---

### `scripts/`

Utility shell scripts for common development tasks. Separate from `src/` because these are operational tools, not application code.

---

#### `scripts/run.sh`

A simple bash script that runs the application. Useful when you want a one-liner to start the app without remembering the full Python command, or when wiring up a process manager. The file is created with executable permissions (`chmod +x`) automatically.

```bash
./scripts/run.sh
```

---

### `config/`

Static configuration files that are not secrets — things that change between environments but are safe to commit to git. Secrets and credentials go in `.env`, not here.

---

#### `config/settings.yaml`

A YAML configuration file with default application settings like app name, environment, and logging format. Load this at startup using PyYAML or a config library like Dynaconf. Useful for settings that are more readable in YAML than as environment variables.

---

### `.github/workflows/`

GitHub Actions CI/CD pipeline definitions. GitHub reads these files automatically when you push to the repository and runs the defined workflows.

---

#### `.github/workflows/ci.yml`

A ready-to-run CI pipeline that triggers on every push to `main` or `develop` and on every pull request. It:

- Sets up the correct Python version
- Installs all dependencies
- Runs `flake8` for style checking
- Runs `black --check` to verify formatting
- Runs the full test suite with `pytest`

No configuration needed — push to GitHub and it works immediately.

---

### `Dockerfile`

Defines how to containerise the application. Uses a **two-stage build** for a smaller, more secure final image:

- **Builder stage** — installs all dependencies into a temporary layer
- **Runtime stage** — copies only the installed packages and source code, resulting in a lean image with no build tools

Additional security measures baked in:
- Runs as a **non-root user** (`appuser`) so a container breach cannot escalate to root
- Sets `PYTHONUNBUFFERED=1` so logs appear immediately in Docker output
- Sets `PYTHONDONTWRITEBYTECODE=1` to skip `.pyc` file generation inside the container

```bash
docker build -t my_app .
docker run --env-file .env my_app
```

---

### `docker-compose.yml`

Defines your application as a Docker Compose service so you can start the full stack with one command. Pre-configured to:

- Build from the local `Dockerfile`
- Load environment variables from `.env`
- Mount `src/` as a volume so code changes reflect inside the container without rebuilding
- Restart automatically unless stopped manually

```bash
docker compose up --build
```

---

### `Makefile`

A set of short command aliases so you never have to remember long flags. Every common task is one word:

| Command | What it does |
|---|---|
| `make install` | Install runtime and dev dependencies |
| `make test` | Run the full test suite with coverage |
| `make lint` | Run flake8 and mypy |
| `make format` | Auto-format all code with black |
| `make clean` | Delete all caches, `.pyc` files, and coverage reports |
| `make docker-build` | Build the Docker image |
| `make docker-run` | Run the Docker container with `.env` |

---

### `pyproject.toml`

The single source of truth for project metadata and tool configuration. Replaces the older `setup.py`, `setup.cfg`, `tox.ini`, and separate config files for each tool. Contains:

- **`[project]`** — name, version, description, author, Python version requirement (auto-detected from your system), and the CLI entry point
- **`[tool.pytest]`** — tells pytest where to find tests and enables coverage reporting by default
- **`[tool.black]`** — sets line length and target Python version for the formatter
- **`[tool.mypy]`** — enables strict type checking
- **`[tool.flake8]`** — sets max line length to match black so the two tools never conflict

---

### `requirements.txt`

Runtime dependencies — packages your application needs to run in production. Add one package per line, pinned to a minimum version:

```
requests>=2.28.0
pydantic>=2.0.0
```

Install with:

```bash
pip install -r requirements.txt
```

---

### `requirements-dev.txt`

Development and testing dependencies — tools only needed when working on the project, not when running it in production. Pre-filled with:

| Package | Purpose |
|---|---|
| `pytest` | Test runner |
| `pytest-cov` | Coverage reporting inside pytest |
| `black` | Code formatter |
| `flake8` | Style linter |
| `mypy` | Static type checker |
| `pre-commit` | Git hook manager |

Install with:

```bash
pip install -r requirements-dev.txt
```

---

### `.env`

Local environment variables — API keys, database URLs, feature flags, and anything else that changes between environments or must not be shared. This file is **git-ignored** so its contents never reach version control.

```
APP_ENV=development
LOG_LEVEL=INFO
API_KEY=your_key_here
DATABASE_URL=postgresql://user:pass@localhost/db
```

In production, inject the same variables through your hosting platform's secret manager rather than copying this file to a server.

---

### `.env.example`

A safe-to-commit template showing which environment variables the project expects, with all values left blank or set to placeholder strings. When a new developer clones the project, they copy this file to `.env` and fill in their own values:

```bash
cp .env.example .env
```

Unlike `.env`, this file **is tracked by git** — it documents the required configuration without exposing any real secrets.

---

### `.gitignore`

Tells git which files and folders to never track. The generated file covers:

| Section | What is ignored |
|---|---|
| Python | `__pycache__/`, `*.pyc`, `*.pyo`, `*.pdb`, compiled files |
| Build & dist | `dist/`, `build/`, `*.egg-info/`, wheels |
| Virtual environments | `.venv/`, `venv/`, `env/`, `ENV/`, `virtualenv/`, `Pipfile.lock`, `poetry.lock` |
| Secrets | `.env`, `.env.local`, `.env.*.local` — but **not** `.env.example` |
| Caches | pytest, mypy, ruff, hypothesis, tox, nox, coverage reports |
| IDEs | VS Code, PyCharm/JetBrains, Vim, Emacs, Sublime Text, Spyder, Rope |
| OS files | `.DS_Store`, `._*` (macOS), `Thumbs.db`, `Desktop.ini` (Windows) |
| Logs & databases | `*.log`, `*.sqlite`, `*.db`, `logs/` |
| Jupyter | `.ipynb_checkpoints/` |
| Docker | `docker-compose.override.yml` |
| Docs build | `docs/_build/`, `site/` |
| Temp files | `*.tmp`, `*.bak`, `tmp/`, `temp/` |

---

### `.pre-commit-config.yaml`

Configures pre-commit hooks — scripts that run automatically every time you run `git commit`. Catches problems before they ever reach the repository. Pre-configured with:

| Hook | What it does |
|---|---|
| `black` | Auto-formats Python code to a consistent style |
| `flake8` | Flags style violations and undefined names |
| `trailing-whitespace` | Removes trailing spaces from every line |
| `end-of-file-fixer` | Ensures every file ends with a newline |
| `check-yaml` | Validates all YAML files are well-formed |
| `check-added-large-files` | Prevents accidentally committing large binary files |

Activate once after cloning:

```bash
pip install pre-commit
pre-commit install
```

---

### `CHANGELOG.md`

A human-readable log of every notable change to the project, organised by version and date. Following the [Keep a Changelog](https://keepachangelog.com) format makes it easy for users and contributors to see what changed between releases. Pre-filled with an `[Unreleased]` section and the initial `0.1.0` entry.

---

### `LICENSE`

The MIT License, pre-filled with your name and the current year. Without a license file, your code is technically "all rights reserved" by default, meaning no one can legally use, copy, or contribute to it. MIT is the most permissive and widely used open-source license — it lets anyone use the code for any purpose as long as they include the original license notice.

---

### `README.md`

The front page of your project — the first thing anyone reads when they open your repository. Pre-filled with a full template covering overview, setup instructions, Docker commands, testing, project structure, contributing guidelines, and license. Edit the overview section to describe what your project actually does.

---

## Example session

```
════════════════════════════════════════════
  Big Project Scaffolder
════════════════════════════════════════════

Project name: data_pipeline
Short description [A Python project]: A real-time data processing pipeline
Author name [Your Name]: Jane Dev
  Python version detected: 3.12
Where to create it [~/projects]:

════════════════════════════════════════════
  Optional Extras
════════════════════════════════════════════
Add GitHub Actions CI workflow? (Y/n):
Add pre-commit config? (Y/n):
Initialise a git repository? (Y/n): y

════════════════════════════════════════════
  Creating Project Structure
════════════════════════════════════════════

  ▸ Source code
    ✔  src/__init__.py
    ✔  src/main.py
    ✔  src/config.py

  ▸ Tests
    ✔  tests/__init__.py
    ✔  tests/test_main.py

  ▸ Docs
    ✔  docs/index.md

  ▸ Scripts
    ✔  scripts/run.sh

  ▸ Config
    ✔  config/settings.yaml

  ▸ Docker
    ✔  Dockerfile
    ✔  docker-compose.yml

  ▸ Python project files
    ✔  pyproject.toml
    ✔  requirements.txt
    ✔  requirements-dev.txt
    ✔  Makefile

  ▸ Root files
    ✔  README.md
    ✔  CHANGELOG.md
    ✔  LICENSE
    ✔  .gitignore
    ✔  .env
    ✔  .env.example

  ▸ GitHub Actions
    ✔  .github/workflows/ci.yml

  ▸ Pre-commit
    ✔  .pre-commit-config.yaml

  ✔  Git repository initialised with first commit

════════════════════════════════════════════
  Done!
════════════════════════════════════════════

  Next steps:
  1. cd ~/projects/data_pipeline
  2. pip install -r requirements.txt -r requirements-dev.txt
  3. pytest
  4. docker compose up --build
```

---

## Notes

- **Project name** — spaces are automatically converted to underscores
- **Existing directory** — if the target folder already exists, the script asks before overwriting
- **GitHub Actions, pre-commit, and git init** — each is optional and asked separately
- **Python version** — automatically detected from the Python running the script; stamped into `pyproject.toml`, `Dockerfile`, and `ci.yml` so all three are always in sync. No menu, no prompt.
- **Two-stage Dockerfile** — the final image contains no build tools, keeping it small and reducing the attack surface
- **Works on Windows, macOS, and Linux** — activation command for the venv is adjusted automatically per platform

---

## Requirements

Python 3.6 or later. No third-party packages.
