set windows-shell := ["cmd.exe", "/c"]

# List available recipes
default:
    @just --list

docs_langs := "az"

# Install every workspace member + tooling, and set up git hooks
setup:
    uv sync --all-packages
    uv run --no-sync pre-commit install --hook-type pre-commit --hook-type pre-push

# Format source files
format *files:
    uv run --no-sync ruff check {{ if files != "" { files } else { "." } }} --fix-only --exit-zero
    uv run --no-sync ruff format {{ if files != "" { files } else { "." } }}

# Lint source files
lint *files:
    uv run --no-sync ruff check {{ if files != "" { files } else { "." } }}
    uv run --no-sync ruff format {{ if files != "" { files } else { "." } }} --check

# Type-check
type-check *files:
    uv run --no-sync ty check {{ if files != "" { files } else { "packages" } }}

# Run every package's test suite (isolated per package) with coverage
test *args:
    uv run --no-sync python scripts/run_tests.py {{args}}

# Combine and display coverage
coverage title="":
    uv run --no-sync coverage combine coverage
    uv run --no-sync coverage report
    uv run --no-sync coverage html {{ if title != "" { '--title="Coverage report for ' + title + '"' } else { "" } }}

# Build documentation (Azerbaijani)
docs:
    uv run --no-sync zensical build -f docs/az/mkdocs.yml --strict

# Serve docs locally
docs-serve lang="az":
    uv run --no-sync zensical serve -f docs/{{lang}}/mkdocs.yml

# Run security scan
secure:
    uv run --no-sync bandit -r packages --config pyproject.toml

# Run all checks
all: format lint test docs

# Delete build artefacts and caches
clean:
    uv run --no-sync python scripts/clean.py
