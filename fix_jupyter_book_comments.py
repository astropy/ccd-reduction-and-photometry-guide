# This is intended to implement the fix to sphinx-comments in
# https://github.com/executablebooks/sphinx-comments/pull/18/
# This is a temporary fix until the PR is merged and released.
#
# The fix enables us to use utterances comments in Jupyter Book.

import re
from argparse import ArgumentParser
from pathlib import Path


def fix_utterances_script(html_path):
    with open(html_path, 'r') as f:
        notebook = f.read()

    new_notebook = notebook.replace("div.section", "section")
    new_notebook = new_notebook.replace(
        "sections !== null",
        "sections !== null && sections.length > 0"
    )
    if new_notebook != notebook:
        print(f"Fixing {html_path}")
        with open(html_path, 'w') as f:
            f.write(new_notebook)


def main(path):
    for html_path in Path(path).glob('**/*.html'):
        fix_utterances_script(html_path)


if __name__ == "__main__":
    parser = ArgumentParser(description='Fix Jupyter Book comments')
    parser.add_argument('path', help='Path to the Jupyter Book build directory',
                        type=str, default='_build/html')
    args = parser.parse_args()
    main(args.path)
