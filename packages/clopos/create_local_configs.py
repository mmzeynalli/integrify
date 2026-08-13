import shutil
from pathlib import Path


def promote_example_files(root_dir='.'):
    root = Path(root_dir)

    shutil.move('README.md', 'Template-README.md')

    for example_file in root.rglob('*.example*'):
        target_file = example_file.with_name(example_file.name.replace('.example', ''))

        if target_file.exists():
            print(f'🟡 Skipped (already exists): {target_file}')  # noqa: T201
        else:
            shutil.move(example_file, target_file)
            print(f'✅ Renamed: {target_file}')  # noqa: T201


if __name__ == '__main__':
    promote_example_files()
