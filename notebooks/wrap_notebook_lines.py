import uuid
import re
from textwrap import TextWrapper

import nbformat as nbf

from link_fix import markdown_cells


def find_links(text):
    """
    Find Markdown links in text and return a match object.

    Markdown links are expected to have the form [some txt](A-url.ext)
    or ![Alt text](cool-image.png).

    Parameters
    ----------

    text : str
        Text in which to search for links.

    Returns
    -------

    list
        List of ``re.Match`` objects, one for each link found. Each object
        has two named groups, 'link_text', which contains the the part between
        the square brackets, and 'link',which is the URL (or file name for an
        image).
    """
    markdown_link = \
        re.compile(r"!?\[(?P<link_text>.+?\n*?.*?)\]\((?P<link_url>.+?)\)",
                   flags=re.MULTILINE)
    groups = [m for m in markdown_link.finditer(text)]
    return groups


def find_latex(text):
    """
    Find Latex equation blocks in text and return a match object.

    Latex blocks are expected to begin and end with double dollar signs, $$.

    Parameters
    ----------

    text : str
        Text in which to search for latex.

    Returns
    -------

    list
        List of ``re.Match`` objects, one for each latex block found.
    """
    markdown_link = re.compile(r"\$\$.*?\$\$", flags=re.MULTILINE + re.DOTALL)
    groups = [m for m in markdown_link.finditer(text)]
    return groups


def protect_from_wrap(text, groups, restore_info=None):
    """
    Protect each match in groups that appears in text from wrapping by
    replacing it with a UUID in hex format (which won't be wrapped).

    Parameters
    ----------

    text : str
        The text in which groups (like markdown links or latex) are to be
        protected from wrapping.

    groups : list of ``re.Match`` objects
        Matches from a regex search for whatever it is that needs to be
        protected.

    restore_info : dict, optional
        Dictionary of protected items. UUIDs are the keys and the string they
        represent are the values. Allows ``protect_from_wrap`` to be called
        multiple times with different `groups`, building up the dictionary
        needed to undo the protection.
    """
    wrapped_text = text
    if restore_info is None:
        restore_info = {}

    # Reverse the groups so that the start positions in the string stays the
    # same as the text is processed.
    for group in groups[::-1]:
        link_id = uuid.uuid4().hex
        restore_info[link_id] = text[group.start(): group.end()]
        wrapped_text = (wrapped_text[:group.start()] + str(link_id) +
                        wrapped_text[group.end():])

    return wrapped_text, restore_info


def restore_protected_content(text, restore_dict):
    for k, v in restore_dict.items():
        text = text.replace(k, v)
    return text


def wrap_notebook_markdown(nb_name, wrap_at=80):
    with open(nb_name) as f:
        nb = nbf.read(f, as_version=4)

    wrapper = TextWrapper(width=wrap_at, break_long_words=False,
                          break_on_hyphens=False,
                          replace_whitespace=False, drop_whitespace=True)

    for cell in markdown_cells(nb):
        link_groups = find_links(cell['source'])
        protected, restore = protect_from_wrap(cell['source'], link_groups)
        latex_groups = find_latex(protected)
        protected, restore = protect_from_wrap(protected, latex_groups,
                                               restore_info=restore)
        lines = protected.split('\n')

        new_lines = []
        for line in lines:
            if line:
                new_lines.extend(wrapper.wrap(line))
            else:
                new_lines.append('')

        new_source = '\n'.join(new_lines)
        cell['source'] = restore_protected_content(new_source, restore)

    return nb
