PYTHON_VERSIONS := 3.9 3.10 3.11 3.12 3.13

.PHONY: .uv  ## Check that uv is installed
.uv:
	@uv -V || echo 'Please install uv: https://docs.astral.sh/uv/getting-started/installation/'

.PHONY: .pre-commit  ## Check that pre-commit is installed
.pre-commit:
	@pre-commit -V || echo 'Please install pre-commit: https://pre-commit.com/'

.PHONY: install  ## Install the package, dependencies, and pre-commit for local development
install: .uv .pre-commit
	uv pip install -r pyproject.toml

.PHONY: format  ## Auto-format python source files
format: .uv
	uv run ruff check --fix
	uv run ruff format

.PHONY: lint  ## Lint python source files
lint: .uv
	uv run ruff check
	uv run ruff format --check
	uv run pylint .

.PHONY: type-check  ## Type-check python source files
type-check: .uv
	uv run mypy .

.PHONY: test-live  ## Run all tests
test-live: .uv
ifeq ($(OS),Windows_NT)
	@FOR %%v IN ($(PYTHON_VERSIONS)) DO \
		uv venv --python %%v .venvs\%%v & \
		venvs\%%v\Scripts\activate & \
		uv run --active coverage run --data-file=coverage\.coverage.py%%v -m pytest --live --durations=10
else
	for v in ${PYTHON_VERSIONS}; do \
		uv run --python $$v coverage run --data-file=coverage/.coverage.py$$v -m pytest --live --durations=10; \
	done
endif

.PHONY: test-local  ## Run all tests except live tests
test-local: .uv
ifeq ($(OS),Windows_NT)
	@FOR %%v IN ($(PYTHON_VERSIONS)) DO \
		uv venv --python %%v .venvs\%%v & \
		.venvs\%%v\Scripts\activate & \
		uv sync --active & \
		uv run --active coverage run --data-file=coverage\.coverage.py%%v -m pytest --durations=10
else
	for v in ${PYTHON_VERSIONS}; do \
		uv venv --python $$v .venvs/$$v & \
		VIRTUAL_ENV=.venvs/$$v uv run --active coverage run --data-file=coverage/.coverage.py$$v -m pytest -m --durations=10; \
	done
endif

.PHONY: test-github  ## Run test for one python version, as GA handles it
test-github: .uv
	uv run coverage run -m pytest --github --durations=10

.PHONY: cov-report
cov-report:
	@uv run coverage combine coverage/
	@uv run coverage report
	@uv run coverage html --title "Coverage for ${{ github.sha }}"

lang=az

.PHONY: docs  ## Generate the docs
docs:
	uv run mkdocs build -f docs/${lang}/mkdocs.yml --strict

.PHONY: docs-serve  ## Serve the docs
docs-serve:
	uv run mkdocs serve -f docs/${lang}/mkdocs.yml

.PHONY: secure
secure:
	uv run bandit -r src/integrify --config pyproject.toml

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
ifeq ($(OS),Windows_NT)
	@if not exist src\integrify\$(name) mkdir src\integrify\$(name)
	@type nul > src\integrify\$(name)\__init__.py
	@type nul > src\integrify\$(name)\client.py
	@type nul > src\integrify\$(name)\handlers.py
	@type nul > src\integrify\$(name)\env.py
	@if not exist src\integrify\$(name)\schemas mkdir src\integrify\$(name)\schemas
	@type nul > src\integrify\$(name)\schemas\__init__.py
	@type nul > src\integrify\$(name)\schemas\request.py
	@type nul > src\integrify\$(name)\schemas\response.py

	@if not exist tests\$(name) mkdir tests\$(name)
	@type nul > tests\$(name)\__init__.py
	@type nul > tests\$(name)\conftest.py
	@type nul > tests\$(name)\mocks.py

	@if not exist docs\$(lang)\docs\$(name) mkdir docs\$(lang)\docs\$(name)
	@type nul > docs\$(lang)\docs\$(name)\about.md
	@type nul > docs\$(lang)\docs\$(name)\api-reference.md
else
	mkdir src/integrify/${name}
	touch src/integrify/${name}/__init__.py src/integrify/${name}/client.py src/integrify/${name}/handlers.py src/integrify/${name}/env.py
	mkdir src/integrify/${name}/schemas
	touch src/integrify/${name}/schemas/__init__.py src/integrify/${name}/schemas/request.py src/integrify/${name}/schemas/response.py;

	mkdir tests/${name}
	touch tests/${name}/__init__.py tests/${name}/conftest.py tests/${name}/mocks.py

	mkdir docs/${lang}/docs/${name}
	touch docs/${lang}/docs/${name}/about.md docs/${lang}/docs/${name}/api-reference.md
endif