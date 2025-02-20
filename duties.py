"""Inspired from griffe-pydantic."""

import os
import shutil
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from duty import context, duty, tools

PYTHON_VERSIONS = os.getenv('PYTHON_VERSIONS', '3.9 3.10 3.11 3.12 3.13').split()

SRC = ('.',)
SEP = os.sep

DOCS_LANGS = ('az',)

if os.name == 'nt':
    import sys

    sys.stdin.reconfigure(encoding='utf-8')  # type: ignore[union-attr]
    sys.stdout.reconfigure(encoding='utf-8')  # type: ignore[union-attr]


@contextmanager
def environ(**kwargs: str) -> Iterator[None]:
    """Temporarily set environment variables."""
    original = dict(os.environ)
    os.environ.update(kwargs)
    try:
        yield
    finally:
        os.environ.clear()
        os.environ.update(original)


##################################################################################################
@duty
def setup(ctx: context.Context) -> None:
    """Setup the project."""
    if not shutil.which('uv'):
        raise ValueError('make: setup: uv must be installed, see https://github.com/astral-sh/uv')

    if not shutil.which('pre-commit'):
        raise ValueError('make: setup: pre-commit must be installed, see https://pre-commit.com/')

    ctx.run('pre-commit install')

    print('Installing dependencies (default environment)')  # noqa: T201
    default_venv = Path('.venv')
    if not default_venv.exists():
        ctx.run('uv venv')

    with environ(UV_PROJECT_ENVIRONMENT=str(default_venv.resolve())):
        ctx.run('uv sync')

    if PYTHON_VERSIONS:
        for ver in PYTHON_VERSIONS:
            print(f'\nInstalling dependencies (python{ver})')  # noqa: T201

            venv_path = Path(f'.venvs{SEP}{ver}')
            if not venv_path.exists():
                ctx.run(f'uv venv --python {ver} {venv_path}')

            with environ(UV_PROJECT_ENVIRONMENT=str(venv_path.resolve())):
                ctx.run('uv sync')


@duty
def format(ctx: context.Context):
    """Format the files."""
    ctx.run(
        tools.ruff.check(*SRC, fix_only=True, exit_zero=True),
        title='Auto-fixing code',
    )
    ctx.run(tools.ruff.format(*SRC), title='Formatting code')


@duty
def lint(ctx: context.Context):
    """Lint the files."""
    ctx.run(
        tools.ruff.check(*SRC),
        title='Linting with ruff check',
    )

    ctx.run(
        tools.ruff.format(*SRC, check=True),
        title='Linting with ruff format',
    )

    ctx.run('pylint .', title='Linting with pylint')


@duty
def type_check(ctx: context.Context):
    """Type check the files."""
    ctx.run(tools.mypy(*SRC), title='Type checking with mypy')


def pytest(ctx: context.Context, **kwds):
    """Helper function to run pytest"""
    args = ' '.join(f'--{k} {v}' for k, v in kwds.items() if v is not None)
    for ver in PYTHON_VERSIONS:
        venv_path = Path(f'.venvs{SEP}{ver}')

        with environ(VIRTUAL_ENV=str(venv_path)):
            ctx.run(
                'uv run --active coverage run --data-file=coverage/.coverage.py'
                + ver
                + ' -m pytest --durations=10 '
                + args,
                title=f'Running tests (python {ver})',
            )


@duty
def test_live(ctx: context.Context):
    """Run tests with live environment (--live)"""
    pytest(ctx, live=True)


@duty
def test_local(ctx: context.Context):
    """Run tests with local environment"""
    pytest(ctx)


@duty
def test_github(ctx: context.Context):
    """Run tests with github environment (--github)"""
    ctx.run(
        'uv run coverage run -m pytest --durations=10 --github',
        title='Running tests ',
    )


@duty
def coverage(ctx: context.Context, title: str = ''):
    """Generate coverage report"""
    ctx.run(tools.coverage.combine('coverage'))
    ctx.run(tools.coverage.report(), capture=False)
    ctx.run(tools.coverage.html(title=f'Coverage report {title}'))


@duty
def docs(ctx: context.Context):
    """Build the documentation."""
    for lang in DOCS_LANGS:
        ctx.run(
            tools.mkdocs.build(config_file=f'docs/{lang}/mkdocs.yml', strict=True),
            title=f'Building documentation ({lang})',
        )


@duty
def docs_serve(ctx: context.Context, lang='az'):
    """Serve the documentation."""
    ctx.run(
        tools.mkdocs.serve(config_file=f'docs/{lang}/mkdocs.yml', verbose=True),
        title=f'Serving documentation ({lang})',
    )


@duty
def secure(ctx: context.Context):
    """Run security checks with bandit."""
    ctx.run('bandit -r src/integrify --config pyproject.toml', title='Running bandit')


@duty(pre=['format', 'lint', 'test', 'docs'])
def all():
    """Run all main tasks: format, lint, test, docs."""


@duty
def clean(ctx: context.Context):  # pylint: disable=unused-argument
    """Delete build artifacts and cache files."""
    print('Cleaning...')  # noqa: T201
    paths_to_clean = ['htmlcov', 'coverage']
    for path in paths_to_clean:
        shutil.rmtree(path, ignore_errors=True)

    cache_dirs = {'site', '.cache', '.pytest_cache', '.mypy_cache', '.ruff_cache', '__pycache__'}
    for dirpath in Path('.').rglob('*/'):
        if dirpath.parts[0] not in ('.venv', '.venvs') and dirpath.name in cache_dirs:
            shutil.rmtree(dirpath, ignore_errors=True)

    print('Done.')  # noqa: T201


@duty
def new_integration(ctx: context.Context, name: str):
    # pylint: disable=all

    """Create files for new integration."""
    os.makedirs(f'src/integrify/{name}/schemas', exist_ok=True)
    os.makedirs(f'tests/{name}', exist_ok=True)

    for lang in DOCS_LANGS:
        os.makedirs(f'docs/{lang}/docs/integrations/{name}', exist_ok=True)

    # Create files in src/integrify/${name}
    open(f'src/integrify/{name}/__init__.py', 'a').close()
    open(f'src/integrify/{name}/client.py', 'a').close()
    open(f'src/integrify/{name}/handlers.py', 'a').close()
    open(f'src/integrify/{name}/env.py', 'a').close()

    # Create files in src/integrify/${name}/schemas
    open(f'src/integrify/{name}/schemas/__init__.py', 'a').close()
    open(f'src/integrify/{name}/schemas/request.py', 'a').close()
    open(f'src/integrify/{name}/schemas/response.py', 'a').close()
    open(f'src/integrify/{name}/schemas/enums.py', 'a').close()

    # Create files in tests/${name}
    open(f'tests/{name}/__init__.py', 'a').close()
    open(f'tests/{name}/conftest.py', 'a').close()
    open(f'tests/{name}/mocks.py', 'a').close()

    # Create files in docs/${lang}/docs/${name}
    open(f'docs/{lang}/docs/integrations/{name}/about.md', 'a').close()
    open(f'docs/{lang}/docs/integrations/{name}/api-reference.md', 'a').close()
