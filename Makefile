ifdef OS
	PYTHON ?= .venv/Scripts/python.exe
	TYPE_CHECK_COMMAND ?= echo Pytype package doesn't support Windows OS
else
	PYTHON ?= .venv/bin/python
	TYPE_CHECK_COMMAND ?= ${PYTHON} -m pytype --config=pytype.cfg src
endif

SETTINGS_FILENAME = pyproject.toml

.PHONY: install
install:
	poetry install --no-interaction

.PHONY: install-main
install-main:
	poetry install --no-interaction --only main

.PHONY: secure
secure:
	poetry run bandit -r integrify --config ${SETTINGS_FILENAME}

.PHONY: test
test:
	poetry run pytest -s