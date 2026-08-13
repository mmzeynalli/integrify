# List available recipes
default:
    @just --list

python_versions := "3.9 3.10 3.11 3.12 3.13"
docs_langs := "az"

# Set up all Python venvs and install pre-commit hooks
setup:
    #!/usr/bin/env sh
    set -e
    pre-commit install
    uv sync
    for ver in {{python_versions}}; do
        uv venv --python "$ver" ".venvs/$ver"
        UV_PROJECT_ENVIRONMENT="$PWD/.venvs/$ver" uv sync
    done

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

# Run tests across all Python versions with coverage
test:
    #!/usr/bin/env sh
    set -e
    mkdir -p coverage
    for ver in {{python_versions}}; do
        VIRTUAL_ENV=".venvs/$ver" uv run --active --no-sync \
            coverage run --data-file="coverage/.coverage.py$ver" \
            -m pytest -sv --durations=10
    done

# Combine and display coverage
coverage title="":
    uv run --no-sync coverage combine coverage
    uv run --no-sync coverage report
    uv run --no-sync coverage html {{ if title != "" { '--title="Coverage report for ' + title + '"' } else { "" } }}

# Build documentation
docs:
    #!/usr/bin/env sh
    set -e
    for lang in {{docs_langs}}; do
        uv run --no-sync zensical build -f "docs/$lang/mkdocs.yml" --strict
    done

# Serve docs locally
docs-serve lang="az":
    uv run --no-sync zensical serve -f docs/{{lang}}/mkdocs.yml

# Run security scan
secure:
    uv run --no-sync bandit -r packages --config pyproject.toml

# Run all checks: format, lint, test, docs
all: format lint test docs

# Delete build artefacts and caches
clean:
    #!/usr/bin/env sh
    rm -rf htmlcov coverage
    find . \
        -not -path './.venv/*' \
        -not -path './.venvs/*' \
        -type d \( \
            -name site -o -name .cache -o -name .pytest_cache \
            -o -name .ruff_cache -o -name __pycache__ \
        \) -exec rm -rf {} + 2>/dev/null || true
    echo "Done."
