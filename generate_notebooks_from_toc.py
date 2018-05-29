import argparse
from collections import OrderedDict, defaultdict
import re
from pathlib import Path

import nbformat as nbf


def parse_toc(toc_markdown):
    """
    Generate set of essentially empty Jupyter notebooks from a table of
    contents in markdown.

    Parameters
    ----------

    toc_markdown : str
        Path to markdown file that contains only the table of contents. See
        Notes for a description of the format.

    Returns
    -------

    list
        A list of lists containing the table of contents entries.

    Notes
    -----

    The markdown file should contain a table of contents with entries
    indicated as headers in the "hashtag" format. For example,

        # First TOC entry, will be numbered 00
        # Second entry, will be numbered 01
        ## Section of the second entry, will be numbered 01.00
        ## Another section of the second entry, numbered 01.01
        # Third entry, numbered 02
        ## Section of third entry, 02.00
        ## Second section, 02.01
        ### Subsection of the second section, numbered 02.01.00

    Though further nesting could in principle be allowed, it isn't.
    """
    with open(toc_markdown) as f:
        lines = f.readlines()

    toc = defaultdict(OrderedDict)
    #toc = defaultdict(dd)
    current_level = 1
    current_dict = toc
    parents = []
    # Nuke blank lines and removing whitespace
    lines = [line.strip() for line in lines if line.strip()]
    for line in lines:
        matches = re.match(r'^(#+) +(.*)', line)
        level, title = matches.group(1, 2)
        level_n = len(level)
        if not current_level and level_n != 1:
            raise ValueError("Improperly formatted TOC")
        if level_n == current_level:
            # Just make a new entry...
            current_dict[title] = OrderedDict()
            latest_title = title
        if level_n > current_level:
            # Time for a new dictionary
            parents.append(current_dict)
            current_dict = current_dict[latest_title]
            current_dict[title] = OrderedDict()
            latest_title = title
        if level_n < current_level:
            level = current_level
            while level_n < level:
                current_dict = parents.pop()
                level -= 1
            current_dict[title] = OrderedDict()
            latest_title = title
        current_level = level_n
        print(level_n, title)
    return toc


def generate_notebooks(toc, directory, parent_string='', start=0, depth=0):
    """
    Generate notebooks/cells/anchors from a table of contents.

    The top two levels each get their own notebooks;  third-level
    TOC entries are created as h2 cells in the notebook and a links
    to those sections are added to the second-level notebook below
    that notebook's title.
    """
    results = []
    for num, entry in enumerate(toc.keys()):
        num_str = f'{num + start:02d}'
        if parent_string:
            num_str = '.'.join([parent_string, num_str])
        if len(toc[entry].keys()) > 0:
            kids = generate_notebooks(toc[entry], directory,
                                      parent_string=num_str, start=1,
                                      depth=depth + 1)
            if kids is None:
                kids = []
        else:
            kids = []
        if depth == 2:
            entry_cell = nbf.v4.new_markdown_cell(entry)
            results.append(entry_cell)
        else:
            notebook = nbf.v4.new_notebook()
            toc_kids = ''
            if depth == 1:
                # Kids are cells...
                toc_entries = []
                for cell in kids:
                    cell_text = cell['source']
                    toc_link = cell_text.replace(' ', '-')
                    toc_entries.append(f'+ [{cell_text}](#{toc_link})')
                    cell['source'] = '## ' + cell_text
                toc_kids = '\n'.join(toc_entries)

            else:
                # Top level, add a '00' to title
                num_str += '.00'

            title_cell = '\n'.join([f'# {entry}', toc_kids])
            title_cell = nbf.v4.new_markdown_cell(title_cell)
            notebook.cells = [cell for cell in [title_cell] + kids]
            notebook_title = num_str + '-' + entry.replace(' ', '-') + '.ipynb'
            path = Path(directory)
            path.mkdir(exist_ok=True)
            nbf.write(notebook, str(path / notebook_title))

        print('    ' * depth, num_str)
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate notebooks from '
                                     'markdown table of contents.')
    parser.add_argument('toc',
                        help='Table of contents from which to generate '
                             'the notebooks. Heading level (with #s) used '
                             'to determine chapters/subsections.')
    parser.add_argument('--destination-dir', default='.',
                        help='Directory to which results notebooks '
                             'should be written.')

    args = parser.parse_args()
    toc = parse_toc(args.toc)
    generate_notebooks(toc, args.destination_dir)
