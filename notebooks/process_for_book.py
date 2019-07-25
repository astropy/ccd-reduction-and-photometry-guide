from pathlib import Path
import shutil
import re

import nbformat as nbf

from wrap_notebook_lines import find_links
from link_fix import markdown_cells

input_nb_pattern = r'0[0123].*.ipynb'

p = Path('.')
(p / 'converted').mkdir(exist_ok=True)
input_notebooks = p.glob(input_nb_pattern)


def nuke_dir_tree(top):
    shutil.rmtree(top)


def clean():
    base = Path('.')
    nukes = ['example1-reduced', 'example2-reduced', 'example3-reduced']
    for nuke in nukes:
        try:
            for p in (base / nuke).iterdir():
                p.unlink()
            (base / nuke).rmdir()
        except FileNotFoundError:
            pass
    nuke_too = (base / 'path').glob('**/*.fits')
    try:
        for nuke in nuke_too:
            nuke.unlink()
    except FileNotFoundError:
        pass

    try:
        (base / 'example-with-cosmic-rays.fits').unlink()
    except FileNotFoundError:
        pass

    try:
        nuke_dir_tree(base / 'path')
    except FileNotFoundError:
        pass


# CONVERT TO NOTEBOOK AND EXECUTE

#later...
# set to_conv (find . -depth 1 -name 0[01234568]-\?\?-\*.ipynb | sort -)

# for conv in $to_conv
#   jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=-1 $conv
# end

# Fix names


def transform_names(old_names):
    new_names = []
    for path in old_names:
        name = str(path)
        name = name.replace('(', '')
        name = name.replace(')', '')
        name = name.replace('.nbconvert', '')

        n_dots = name.count('.') - 1
        if n_dots:
            name = name.replace('.', '-', n_dots)

        print(name)
        new_names.append(name)

    return new_names


def replace_link_urls(text, old_ext='.ipynb', new_ext='.html', path='.',
                      verbose=True):
    """
    Replace markdown links whose name exactly matches a local file with
    extension ``old_ext`` with a new link that ends ``new_ext``.

    Useful for turning links between notebooks into links between rendered HTML
    pages.

    Parameters
    ----------

    text : str
        The text to be 1) searched for markdown links that 2) will then be
        transformed if appropriate.

    old_ext : str, optional
        The old (i.e. original) file name extension.

    new_ext : str, optional
        The new file name extension that will replace ``old_ext``.

    path : str, optional
        The path on which to look for an existing file.

    verbose: bool, optional
        If ``True``, print a message whenever a link is replaced.
    """
    p = Path(path)

    # Identify the markdown links first. This vastly simplifies the regex
    # needed later for identifying links we may need to transform.
    links = find_links(text)

    new_text = text

    # This regex will be used to search the *url* part of a markdown link only.
    # It matches either a url that ends with old_ext or a url that has old_ext#
    # in it. That way links that include anchors will be transformed.
    match_ext = re.compile(r'.+' + old_ext + '$|.+' + old_ext + '#.*')

    # Work from the end towards the beginning of the string so
    # that indexes don't get messed up as we work.
    for link in links[::-1]:
        url = Path(link['link_url'])
        if str(url).count('#') > 1:
            raise ValueError(f'Do not know how to handle '
                             'link {url} with so many #')
        try:
            uri, anchor = str(url).split('#')
        except ValueError:
            uri = str(url)
            anchor = ''

        if match_ext.findall(str(url)) and (p / uri).exists():
            # Do not do a straight-up replace of old_ext with new_ext in case
            # someone tries something "clever" like foo.ipynb.ipynb.
            if anchor:
                new_url = '#'.join([str(url.with_suffix(new_ext)), anchor])
            else:
                new_url = str(url.with_suffix(new_ext))
            if verbose:
                print(f'Replacing {url}  ------>  {new_url}')
            new_text = (new_text[:link.start('link_url')] + str(new_url) +
                        new_text[link.end('link_url'):])

    return new_text


def replace_links_in_notebook(nb_file):
    notebook = nbf.read(nb_file, as_version=4)
    for cell in markdown_cells(notebook):
        cell['source'] = replace_link_urls(cell['source'])
    with open(nb_file, 'w') as f:
        nbf.write(notebook, f)


if __name__ == "__main__":
    converted_nb_pattern = '*.nbconvert.ipynb'

    old_names = [n for n in p.glob(converted_nb_pattern)]

    news = transform_names(old_names)

    for path, name in zip(old_names, news):
        path.rename(p / 'converted' / name)
