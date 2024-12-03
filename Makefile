.PHONY: .poetry  ## Check that Poetry is installed
.poetry:
	@poetry -V || echo 'Please install Poetry: https://python-poetry.org/docs/#installation'

.PHONY: .pre-commit  ## Check that pre-commit is installed
.pre-commit:
	@pre-commit -V || echo 'Please install pre-commit: https://pre-commit.com/'

.PHONY: install  ## Install the package, dependencies, and pre-commit for local development
install: .poetry
	poetry install --no-interaction

.PHONY: install-main
install-main: .poetry
	poetry install --no-interaction --only main

.PHONY: refresh-lockfiles  ## Sync lockfiles with requirements files.
refresh-lockfiles: .poetry
	poetry lock --no-update

.PHONY: rebuild-lockfiles  ## Rebuild lockfiles from scratch, updating all dependencies
rebuild-lockfiles: .poetry
	poetry lock

.PHONY: format  ## Auto-format python source files
format: .poetry
	poetry run ruff check --fix
	poetry run ruff format

.PHONY: lint  ## Lint python source files
lint: .poetry
	poetry run ruff check
	poetry run ruff format --check
	poetry run pylint .

.PHONY: type-check  ## Type-check python source files
type-check: .poetry
	poetry run mypy .

.PHONY: test  ## Run all tests
test: .poetry
	poetry run coverage run -m pytest --durations=10

lang=az

.PHONY: docs  ## Generate the docs
docs:
	poetry run mkdocs build -f docs/${lang}/mkdocs.yml --strict

.PHONY: docs-serve  ## Serve the docs
docs-serve:
	poetry run mkdocs serve -f docs/${lang}/mkdocs.yml

.PHONY: secure
secure:
	poetry run bandit -r integrify --config pyproject.toml

.PHONY: all  ## Run the standard set of checks performed in CI
all: format lint test

.PHONY: clean  ## Clear local caches and build artifacts
clean:
ifeq ($(OS),Windows_NT)
	del /s /q __pycache__
	del /s /q *.pyc *.pyo
	del /s /q *~ .*~
	del /s /q site
	del /s /q .cache
	del /s /q .mypy_cache
	del /s /q .pytest_cache
	del /s /q .ruff_cache
	del /s /q htmlcov
	del /s /q *.egg-info
	del /s /q .coverage .coverage.*
	del /s /q build
	del /s /q dist
	del /s /q site
	del /s /q docs\_build
	del /s /q coverage.xml
	del /s /q coverage.lcov
else
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]'`
	rm -f `find . -type f -name '*~'`
	rm -f `find . -type f -name '.*~'`
	rm -rf `find . -name site`
	rm -rf .cache
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf .mypy_cache	
	rm -rf htmlcov
	rm -rf *.egg-info
	rm -f .coverage
	rm -f .coverage.*
	rm -rf build
	rm -rf dist
	rm -rf site
	rm -rf docs/_build
	rm -rf coverage.xml
	rm -rf coverage.lcov
endif

.PHONY: new-integration  ## Create new integration folder
new-integration:
	mkdir src/integrify/${name}
	touch src/integrify/${name}/__init__.py src/integrify/${name}/client.py src/integrify/${name}/handlers.py src/integrify/${name}/env.py
	mkdir src/integrify/${name}/schemas
	touch src/integrify/${name}/schemas/__init__.py src/integrify/${name}/schemas/request.py src/integrify/${name}/schemas/response.py;
	
	mkdir tests/${name}
	touch tests/${name}/__init__.py tests/${name}/conftest.py tests/${name}/mocks.py

	mkdir docs/${lang}/docs/${name}
	touch docs/${lang}/docs/${name}/about.md docs/${lang}/docs/${name}/api-reference.md