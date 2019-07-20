import nbformat as nbf
from astropy.table import Table

#oof = nbf.read('magical_transofrms.ipynb', as_version=4)

# gool = '06.01-Initial-reduction.ipynb'

gool = 'magical_transofrms.ipynb'

def markdown_cells(nb):
    """
    Iterator for markdown cells in notebook.
    """
    for cell in nb['cells']:
        if cell['cell_type'] == "markdown":
            yield cell


def link_fix(text, name_dict):
    """
    Replace old file names with new in markdown links.
    """
    new_text = text
    for old, new in name_dict.items():
        new_text = new_text.replace(f']({old})', f']({new})')
    return new_text


if __name__ == '__main__':
    names = {k: v for k, v in Table.read('old-and-new-names.csv')}

    for notebook_name in names.values():
        try:
            notebook = nbf.read(notebook_name, as_version=4)
        except FileNotFoundError:
            continue

        for cell in markdown_cells(notebook):
            new_source = link_fix(cell['source'], names)
            if new_source != cell['source']:
                print(f'fixed link in {notebook_name}')
                cell['source'] = new_source

        with open(notebook_name, 'w') as f:
            nbf.write(notebook, f)
