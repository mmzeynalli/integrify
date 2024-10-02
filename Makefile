ifdef OS
	PYTHON ?= .venv/Scripts/python.exe
	TYPE_CHECK_COMMAND ?= echo Pytype package doesn't support Windows OS
else
	PYTHON ?= .venv/bin/python
	TYPE_CHECK_COMMAND ?= ${PYTHON} -m pytype --config=pytype.cfg src
endif

SETTINGS_FILENAME = pyproject.toml

.PHONY: 
install-poetry:
	curl -sSL https://install.python-poetry.org | python3 -

.PHONY: install
install:
	poetry run poetry install

.PHONY: install-main
install-main:
	poetry run poetry install --only main

.PHONY: secure
secure:
	poetry run bandit -r integrify --config ${SETTINGS_FILENAME}

.PHONY: test
test:
	poetry run poetry run pytest -s