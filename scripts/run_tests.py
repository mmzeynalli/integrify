"""Run each package's test suite in its own pytest process.

Every package ships a top-level ``tests`` package (``packages/<pkg>/tests/``),
so collecting them all under one root makes pytest import several different
``tests.conftest`` modules under the same dotted name -> ImportPathMismatchError.
Running one package at a time keeps each ``tests`` package unambiguous. Coverage
is accumulated across the per-package runs into a single data file (honouring the
``COVERAGE_FILE`` env var, e.g. in CI).
"""

import glob
import os
import subprocess
import sys


def main() -> int:
    test_dirs = sorted(p for p in glob.glob('packages/*/tests') if os.path.isdir(p))
    if not test_dirs:
        print('no package test directories found under packages/*/tests')
        return 0

    extra = sys.argv[1:]
    failures = []
    for index, tdir in enumerate(test_dirs):
        cmd = [sys.executable, '-m', 'coverage', 'run']
        if index:
            cmd.append('--append')  # first run resets the data file, the rest accumulate
        cmd += ['-m', 'pytest', tdir, *extra]
        print(f'\n=== {tdir} ===', flush=True)
        if subprocess.run(cmd, check=False).returncode:
            failures.append(tdir)

    if failures:
        print('\nFAILED: ' + ', '.join(failures), file=sys.stderr)
        return 1
    print('\nAll package test suites passed.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
