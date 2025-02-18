import os
import shutil
import subprocess
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator

from duty import context, duty, tools

PYTHON_VERSIONS = os.getenv('PYTHON_VERSIONS', '3.9 3.10 3.11 3.12 3.13').split()
CMD = 1 if os.getenv('SHELL') == 'cmd.exe' else 0
SEP = os.sep

COMMANDS = {
    'venv-activate': ['. .venvs/{py}/bin/activate', '.venvs\\{py}\\Scripts\\activate'],
    'set-env': ['export', 'set'],
}


def shell(cmd: str, **kwargs: Any) -> None:
    """Run a shell command."""
    subprocess.run(cmd, shell=True, check=True, stderr=subprocess.STDOUT, **kwargs)  # noqa: S602


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
    ctx.run(
        tools.ruff.check(*[], fix_only=True, exit_zero=True),
        title='Auto-fixing code',
    )
    ctx.run(tools.ruff.format(*[]), title='Formatting code')


@duty
def lint(ctx: context.Context):
    pass


@duty
def type_check(ctx: context.Context):
    pass


@duty
def test_live(ctx: context.Context):
    pass


@duty
def test_local(ctx: context.Context):
    pass


@duty
def test_github(ctx: context.Context):
    pass


@duty
def coverage(ctx: context.Context):
    pass


@duty
def docs(ctx: context.Context):
    ctx.run('mkdocs build', title='Building documentation')


@duty
def docs_serve(ctx: context.Context):
    pass


@duty
def secure(ctx: context.Context):
    pass


@duty(pre=['format', 'lint', 'test', 'docs'])
def all(ctx: context.Context):
    pass


@duty
def clean(ctx: context.Context):
    pass


@duty
def new_integration(ctx: context.Context):
    pass
