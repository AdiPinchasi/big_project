#!/usr/bin/env python3
"""
big_project.py  —  Full professional Python project scaffolder
Run:  python big_project.py
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import date


# ── helpers ───────────────────────────────────────────────────────

def ask(prompt, default=None):
    suffix = f" [{default}]" if default else ""
    while True:
        answer = input(f"{prompt}{suffix}: ").strip()
        if answer:
            return answer
        if default is not None:
            return default
        print("  ✗  This field is required.")


def ask_yes_no(prompt, default="y"):
    options = "Y/n" if default == "y" else "y/N"
    while True:
        answer = input(f"{prompt} ({options}): ").strip().lower()
        if not answer:
            return default == "y"
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("  ✗  Please enter y or n.")


def ask_choice(prompt, choices, default=None):
    print(f"\n  {prompt}")
    for i, c in enumerate(choices, 1):
        marker = " (default)" if c == default else ""
        print(f"    {i}. {c}{marker}")
    while True:
        raw = input(f"  Choice [1-{len(choices)}]: ").strip()
        if not raw and default:
            return default
        if raw.isdigit() and 1 <= int(raw) <= len(choices):
            return choices[int(raw) - 1]
        print("  ✗  Invalid choice.")


def banner(text):
    width = max(len(text) + 4, 44)
    print("\n" + "═" * width)
    print(f"  {text}")
    print("═" * width)


def section(text):
    print(f"\n  ▸ {text}")


def write_file(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    rel = path
    try:
        rel = path.relative_to(Path.cwd())
    except ValueError:
        pass
    print(f"    ✔  {rel}")


# ══ FILE TEMPLATES ════════════════════════════════════════════════

def tpl_readme(name, description, author):
    return f"""\
# {name}

{description}

## Table of Contents

- [Overview](#overview)
- [Setup](#setup)
- [Usage](#usage)
- [Docker](#docker)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

{description}

## Setup

### With pip

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### With Make

```bash
make install
```

## Usage

```bash
python src/main.py
```

## Docker

```bash
# Build and run
docker compose up --build

# Or manually
docker build -t {name} .
docker run --env-file .env {name}
```

## Testing

```bash
pytest
# or
make test
```

## Project Structure

```
{name}/
├── src/                    # Application source code
│   ├── __init__.py
│   ├── main.py             # Entry point
│   └── config.py           # Configuration loader
├── tests/                  # Test suite
│   ├── __init__.py
│   └── test_main.py
├── docs/                   # Documentation
│   └── index.md
├── scripts/                # Utility scripts
│   └── run.sh
├── config/                 # Config files
│   └── settings.yaml
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions CI
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── .env.example
├── .gitignore
├── CHANGELOG.md
├── LICENSE
└── README.md
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m "Add my feature"`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request

## License

MIT License — see [LICENSE](LICENSE) for details.

---

*Author: {author} — {date.today().year}*
"""


def tpl_main(name):
    return f'''\
"""
{name} — entry point
"""


def main() -> None:
    print("Hello from {name}!")


if __name__ == "__main__":
    main()
'''


def tpl_config(name):
    return '''\
"""
Configuration loader — reads from environment variables and .env file.
"""

import os


class Config:
    APP_ENV: str = os.getenv("APP_ENV", "development")
    DEBUG: bool = APP_ENV != "production"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    @classmethod
    def is_production(cls) -> bool:
        return cls.APP_ENV == "production"
'''


def tpl_init(name):
    return f'"""{ name } package"""\n'


def tpl_test_main():
    return '''\
"""Tests for main module."""

from src.main import main


def test_main_runs():
    """Smoke test — main() should not raise."""
    main()
'''


def tpl_test_init():
    return '"""Test package"""\n'


def tpl_gitignore():
    return """\
# ── Python ────────────────────────────────────────────────────────
__pycache__/
*.py[cod]
*.pyo
*.pyd
*.pdb
.Python

# ── Build & distribution ──────────────────────────────────────────
*.egg
*.egg-info/
dist/
build/
eggs/
parts/
var/
sdist/
develop-eggs/
.installed.cfg
lib/
lib64/
wheels/
pip-wheel-metadata/
MANIFEST
*.manifest
*.spec
site/

# ── Virtual environments ──────────────────────────────────────────
.venv/
venv/
env/
ENV/
.env/
virtualenv/
.virtualenv/
Pipfile.lock
poetry.lock

# ── Environment & secrets ─────────────────────────────────────────
.env
.env.local
.env.*.local
!.env.example

# ── Caches ────────────────────────────────────────────────────────
.cache/
.pytest_cache/
.mypy_cache/
.dmypy.json
.ruff_cache/
.hypothesis/
.tox/
.nox/
*.cover
.coverage
.coverage.*
htmlcov/
coverage.xml
nosetests.xml
pip-log.txt
pip-delete-this-directory.txt

# ── IDE & editors ─────────────────────────────────────────────────
# VS Code
.vscode/
!.vscode/extensions.json

# JetBrains (PyCharm, IntelliJ)
.idea/
*.iml
*.iws
*.ipr
out/

# Vim / Emacs
*.swp
*.swo
*~
\#*\#
.\#*
*.orig

# Sublime Text
*.sublime-project
*.sublime-workspace

# Spyder
.spyderproject.cfg
.spyproject/

# Rope
.ropeproject/

# ── OS generated ──────────────────────────────────────────────────
# macOS
.DS_Store
.AppleDouble
.LSOverride
._*
.Spotlight-V100
.Trashes

# Windows
Thumbs.db
Thumbs.db:encryptable
ehthumbs.db
Desktop.ini
$RECYCLE.BIN/
*.lnk

# Linux
*~

# ── Logs & databases ──────────────────────────────────────────────
*.log
*.sql
*.sqlite
*.sqlite3
*.db
logs/
log/

# ── Jupyter ───────────────────────────────────────────────────────
.ipynb_checkpoints/
*.ipynb_checkpoints
profile_default/
ipython_config.py

# ── Docker ────────────────────────────────────────────────────────
.dockerignore
docker-compose.override.yml

# ── Docs build output ─────────────────────────────────────────────
docs/_build/
docs/site/
site/

# ── Temporary files ───────────────────────────────────────────────
*.tmp
*.temp
*.bak
*.backup
tmp/
temp/
"""


def tpl_dotenv():
    return """\
# ── Application ───────────────────────────────────────────────────
APP_ENV=development
LOG_LEVEL=INFO

# ── Secrets (never commit real values) ───────────────────────────
# API_KEY=your_key_here
# DATABASE_URL=postgresql://user:pass@localhost/db
# SECRET_KEY=change_me
"""


def tpl_dotenv_example():
    return """\
# Copy this file to .env and fill in your values
# cp .env.example .env

APP_ENV=development
LOG_LEVEL=INFO
# API_KEY=
# DATABASE_URL=
# SECRET_KEY=
"""


def tpl_requirements():
    return """\
# Runtime dependencies
# Example:
# requests>=2.28.0
# pydantic>=2.0.0
"""


def tpl_requirements_dev():
    return """\
# Development & testing dependencies
pytest>=7.0.0
pytest-cov>=4.0.0
black>=23.0.0
flake8>=6.0.0
mypy>=1.0.0
pre-commit>=3.0.0
"""


def tpl_pyproject(name, description, author, python_version):
    return f"""\
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.backends.legacy:build"

[project]
name = "{name}"
version = "0.1.0"
description = "{description}"
authors = [{{ name = "{author}" }}]
requires-python = ">={python_version}"
readme = "README.md"
license = {{ text = "MIT" }}

[project.scripts]
{name} = "src.main:main"

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--cov=src --cov-report=term-missing"

[tool.black]
line-length = 88
target-version = ["py{python_version.replace('.', '')}"]

[tool.mypy]
python_version = "{python_version}"
strict = true
ignore_missing_imports = true

[tool.flake8]
max-line-length = 88
extend-ignore = ["E203", "W503"]
"""


def tpl_dockerfile(name, python_version):
    return f"""\
# ── Builder stage ─────────────────────────────────────────────────
FROM python:{python_version}-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \\
    && pip install --no-cache-dir -r requirements.txt

# ── Runtime stage ─────────────────────────────────────────────────
FROM python:{python_version}-slim AS runtime

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python{python_version}/site-packages /usr/local/lib/python{python_version}/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy source
COPY src/ ./src/

# Non-root user for security
RUN adduser --disabled-password --gecos "" appuser
USER appuser

ENV APP_ENV=production
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

CMD ["python", "src/main.py"]
"""


def tpl_docker_compose(name, python_version):
    return f"""\
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: runtime
    container_name: {name}
    env_file:
      - .env
    volumes:
      - ./src:/app/src
    restart: unless-stopped
"""


def tpl_makefile(name):
    return f"""\
.PHONY: install test lint format clean docker-build docker-run

install:
\tpip install -r requirements.txt
\tpip install -r requirements-dev.txt

test:
\tpytest

lint:
\tflake8 src tests
\tmypy src

format:
\tblack src tests

clean:
\tfind . -type d -name __pycache__ -exec rm -rf {{}} +
\tfind . -name "*.pyc" -delete
\trm -rf .coverage htmlcov .pytest_cache .mypy_cache

docker-build:
\tdocker build -t {name} .

docker-run:
\tdocker run --env-file .env {name}
"""


def tpl_ci(python_version):
    return f"""\
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "{python_version}"

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Lint
        run: |
          flake8 src tests
          black --check src tests

      - name: Test
        run: pytest
"""


def tpl_changelog(name):
    today = date.today().strftime("%Y-%m-%d")
    return f"""\
# Changelog

All notable changes to **{name}** will be documented here.

Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased]

## [0.1.0] — {today}

### Added
- Initial project scaffold
- Basic project structure
- Docker support
- GitHub Actions CI
"""


def tpl_license(author):
    year = date.today().year
    return f"""\
MIT License

Copyright (c) {year} {author}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


def tpl_docs_index(name, description):
    return f"""\
# {name} Documentation

{description}

## Getting Started

See the [README](../README.md) for setup and usage instructions.

## API Reference

_Document your modules and functions here._

## Architecture

_Describe the overall design and key decisions here._
"""


def tpl_settings_yaml():
    return """\
# Application settings
app:
  name: my_app
  env: development
  debug: true

logging:
  level: INFO
  format: "%(asctime)s — %(name)s — %(levelname)s — %(message)s"
"""


def tpl_run_sh(name):
    return f"""\
#!/usr/bin/env bash
# Run the application
set -euo pipefail

echo "Starting {name}..."
python src/main.py "$@"
"""


def tpl_precommit():
    return """\
repos:
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black

  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
"""


# ══ MAIN ══════════════════════════════════════════════════════════

def main():
    banner("Big Project Scaffolder")

    # ── Gather info ──────────────────────────────────────────────
    print()
    project_name = ask("Project name").strip().replace(" ", "_")
    description  = ask("Short description", default="A Python project")
    author       = ask("Author name", default="Your Name")
    python_ver = f"{sys.version_info.major}.{sys.version_info.minor}"
    print(f"  Python version detected: {python_ver}")

    default_location = str(Path.home() / "projects")
    project_location = Path(
        ask("Where to create it", default=default_location)
    ).expanduser().resolve()

    project_root = project_location / project_name

    if project_root.exists():
        print(f"\n  ⚠  Directory already exists: {project_root}")
        if not ask_yes_no("  Overwrite / merge?", default="n"):
            print("  Aborted.")
            sys.exit(0)

    # ── Optional extras ──────────────────────────────────────────
    banner("Optional Extras")
    use_github_actions = ask_yes_no("Add GitHub Actions CI workflow?")
    use_precommit      = ask_yes_no("Add pre-commit config?")
    use_git            = ask_yes_no("Initialise a git repository?")

    # ── Create files ─────────────────────────────────────────────
    banner("Creating Project Structure")

    section("Source code")
    write_file(project_root / "src" / "__init__.py",  tpl_init(project_name))
    write_file(project_root / "src" / "main.py",      tpl_main(project_name))
    write_file(project_root / "src" / "config.py",    tpl_config(project_name))

    section("Tests")
    write_file(project_root / "tests" / "__init__.py", tpl_test_init())
    write_file(project_root / "tests" / "test_main.py", tpl_test_main())

    section("Docs")
    write_file(project_root / "docs" / "index.md",
               tpl_docs_index(project_name, description))

    section("Scripts")
    run_sh = project_root / "scripts" / "run.sh"
    write_file(run_sh, tpl_run_sh(project_name))
    run_sh.chmod(0o755)

    section("Config")
    write_file(project_root / "config" / "settings.yaml", tpl_settings_yaml())

    section("Docker")
    write_file(project_root / "Dockerfile",
               tpl_dockerfile(project_name, python_ver))
    write_file(project_root / "docker-compose.yml",
               tpl_docker_compose(project_name, python_ver))

    section("Python project files")
    write_file(project_root / "pyproject.toml",
               tpl_pyproject(project_name, description, author, python_ver))
    write_file(project_root / "requirements.txt",     tpl_requirements())
    write_file(project_root / "requirements-dev.txt", tpl_requirements_dev())
    write_file(project_root / "Makefile",             tpl_makefile(project_name))

    section("Root files")
    write_file(project_root / "README.md",
               tpl_readme(project_name, description, author))
    write_file(project_root / "CHANGELOG.md",  tpl_changelog(project_name))
    write_file(project_root / "LICENSE",       tpl_license(author))
    write_file(project_root / ".gitignore",    tpl_gitignore())
    write_file(project_root / ".env",          tpl_dotenv())
    write_file(project_root / ".env.example",  tpl_dotenv_example())

    if use_github_actions:
        section("GitHub Actions")
        write_file(project_root / ".github" / "workflows" / "ci.yml",
                   tpl_ci(python_ver))

    if use_precommit:
        section("Pre-commit")
        write_file(project_root / ".pre-commit-config.yaml", tpl_precommit())

    # ── Virtual environment ──────────────────────────────────────
    banner("Virtual Environment")

    if ask_yes_no("Create a virtual environment?"):
        venv_name = ask("Virtual environment name", default=".venv")
        venv_loc  = ask(
            "Where to create the venv",
            default=str(project_root)
        )
        venv_path = Path(venv_loc).expanduser().resolve() / venv_name

        print(f"\n  Creating venv at: {venv_path}")
        try:
            subprocess.run([sys.executable, "-m", "venv", str(venv_path)],
                           check=True)
            print(f"  ✔  Virtual environment created")
            if os.name == "nt":
                activate_cmd = str(venv_path / "Scripts" / "activate.bat")
            else:
                activate_cmd = f"source {venv_path / 'bin' / 'activate'}"
            print(f"\n  To activate:\n  {activate_cmd}")
        except subprocess.CalledProcessError as e:
            print(f"  ✗  Failed: {e}")
    else:
        print("  Skipped.")

    # ── Git init ─────────────────────────────────────────────────
    if use_git:
        banner("Git")
        try:
            subprocess.run(["git", "init", str(project_root)], check=True,
                           capture_output=True)
            subprocess.run(["git", "-C", str(project_root),
                            "add", "."], check=True, capture_output=True)
            subprocess.run(["git", "-C", str(project_root),
                            "commit", "-m", "Initial commit — big_project scaffold"],
                           check=True, capture_output=True)
            print(f"  ✔  Git repository initialised with first commit")
            print(f"\n  To push to GitHub:")
            print(f"  git -C {project_root} remote add origin https://github.com/YOUR_USER/{project_name}.git")
            print(f"  git -C {project_root} push -u origin main")
        except subprocess.CalledProcessError as e:
            print(f"  ✗  Git init failed: {e}")
        except FileNotFoundError:
            print("  ✗  Git not found — install git and run manually")

    # ── Summary ──────────────────────────────────────────────────
    banner("Done!")
    print(f"\n  Project created at:\n  {project_root}\n")
    print("  Structure:")
    for p in sorted(project_root.rglob("*")):
        # skip venv internals
        parts = p.relative_to(project_root).parts
        if any(x in parts for x in (".venv", "venv", "__pycache__", ".git")):
            continue
        rel   = p.relative_to(project_root)
        depth = len(rel.parts) - 1
        indent = "  " + "    " * depth
        icon   = "📁" if p.is_dir() else "📄"
        print(f"  {indent}{icon} {p.name}")
    print()
    print(f"  Next steps:")
    print(f"  1. cd {project_root}")
    print(f"  2. pip install -r requirements.txt -r requirements-dev.txt")
    print(f"  3. pytest")
    print(f"  4. docker compose up --build")
    print()


if __name__ == "__main__":
    main()
