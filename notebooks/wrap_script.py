from pathlib import Path

import nbformat as nbf

from wrap_notebook_lines import wrap_notebook_markdown

notebooks = Path('.').glob('??-??-*.ipynb')

for notebook in notebooks:
    print(f'Wrapping {notebook}...')
    new_source = wrap_notebook_markdown(notebook, wrap_at=80)
    with open(notebook, 'w') as f:
        nbf.write(new_source, f, version=4)
