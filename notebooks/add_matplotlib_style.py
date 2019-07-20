from pathlib import Path

import nbformat as nbf

to_fix = Path('.').glob('??-??-?*.ipynb')


style_cell = nbf.v4.new_code_cell("# Use custom style for larger fonts and figures\nplt.style.use('guide.mplstyle')")


def add_cell_before(nbcells):
    """
    Figure which cell, if any, the style file cell
    should be added.

    Parameters
    ----------

    nbcells : list of notebook cells
        The cells to look at to decide if we need to add
        the style.

    Returns
    -------

    None or int
        Either the index before which the new cell should be inserted
        or None if no insertino is needed.
    """
    insert_before = None
    for idx, c in enumerate(nbcells):
        if c['cell_type'] != 'code':
            continue
        if ('import matplotlib' in c['source'] or
                'from matplotlib' in c['source']):
            insert_before = idx + 1
        if style_cell['source'] in c['source']:
            insert_before = None

    return insert_before


for nb_file in to_fix:
    print(f"Examining {nb_file}")
    with open(nb_file) as f:
        notebook = nbf.read(f, as_version=4)
    insert_at = add_cell_before(notebook['cells'])
    if insert_at is not None:
        print(f"\tInserting style cell in {nb_file}")
        notebook['cells'].insert(insert_at, style_cell)
        with open(nb_file, 'w') as f:
            nbf.write(notebook, f)
    else:
        print("\tNo insertion needed")
