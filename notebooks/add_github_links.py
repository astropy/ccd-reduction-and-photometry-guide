from pathlib import Path
from hashlib import md5
import random
import time
import os
import re

from github3 import login
import nbformat as nbf

from link_fix import markdown_cells

DEFAULT_COMMENT_GROUP = 'default-comment-group'


def github_magic(nb_file_for_book, original_notebook,
                 comment_group=DEFAULT_COMMENT_GROUP):
    """
    Add links in nb_file to lines on PR opened just for commenting
    on this specific file.
    """
    # 5. Scan the notebook for sections headers (level 2 or 3).   <---- BOTH
    # 6. Get line numbers IN The ORIGINAL notebook of these headers.    <--- ORIG
    # 7. Add a link after the header with text something like that below.   <--- BOTH
    #    Link is to the magical github place for making comments.
    # Done!
    repo = get_github_repo('astropy', 'ccd-reduction-and-photometry-guide')

    base_url = \
        create_pr_for_commenting(original_notebook, repo,
                                 comment_group=comment_group)

    heading_in_original = find_headers(original_notebook,
                                       highest_level=2,
                                       lowest_level=3)

    comment_link_text = ('*Click here to comment on this section on '
                         'GitHub (opens in new tab).*')

    cell_content_to_insert = \
        {k: f'\n[{comment_link_text}]({base_url + str(v)})' +
             '{:target="_blank"}\n'
            for k, v in heading_in_original.items()}

    book_nb = nbf.read(nb_file_for_book, as_version=4)

    for cell in markdown_cells(book_nb):
        for k, v in cell_content_to_insert.items():
            if k in cell['source']:
                pre, post = cell['source'].split(k)
                new_source = pre + k + v + post
                cell['source'] = new_source
    with open(nb_file_for_book, 'w') as fp:
        nbf.write(book_nb, fp)


def get_github_repo(owner, repo):
    """
    Log in to github and retrieve a reference to the requested
    repository.
    """
    token = os.getenv('GITHUB_TOKEN')

    if not token:
        raise RuntimeError('Set GITHUB_TOKEN to a '
                           'github token before running.')
    gh = login(token=token)

    return gh.repository(owner, repo)


def create_pr_for_commenting(original_nb, repo,
                             comment_group=DEFAULT_COMMENT_GROUP):
    """
    Create a new PR for the notebook original_nb against a (nearly) empty
    branch to make a clean difference for commenting.

    PRs/branches (which are necessary for opening the PRs) are labeled
    with ``comment_group`` to make it easier to process them in bulk later.


    Parameters
    ----------

    original_nb : str
        Name of the notebook for which the branch/PR is to be created.

    repo : github3.py Repo object
        Repository in which the PR/branch is to be created.

    comment_group : str, optional
        Name of the label applied to the PR opened with this function.

    Returns
    -------

    str
        URL to which the line number needs to be appended for a link directly
        to this file/line in the github PR.
    """

    # We are going to bling the h*ck out of this. Adding labels!
    # With colors set by the hash of the comment group name!
    label_name = comment_group
    label_color = md5(label_name.encode()).hexdigest()[:6]
    label_description = f'For commenting as part of {comment_group}'

    # We'll make new branches off the initial commit to get a nice,
    # clean diff.
    first_commit = '6e20c1c2f5ef09206f02a5f5f67fcd818859a8c9'

    # Pull requests are made against this branch, which was also from the
    # first commit. Again, gives nice diffs.
    pr_base = 'for-making-comments'
    branch_name = f'{comment_group}/{original_nb}'
    # 1. Add a branch for this file. Name is tag-file_name. <--- ORIG
    _ = repo.create_branch_ref(branch_name, sha=first_commit)
    with open(original_nb, 'rb') as f:
        nb_content = f.read()
    file_name = f'notebooks/{original_nb}'
    commit_msg = f'Only for commenting, part of {comment_group}'
    repo.create_file(file_name, commit_msg, nb_content, branch=branch_name)
    pr_title = f'For commenting on {original_nb} (part of {comment_group})'
    new_pr = repo.create_pull(pr_title, pr_base, branch_name)

    # So labels get added to issues, not PRs...
    pr_issue = new_pr.issue()

    # This should be the only label, grab it..
    label = pr_issue.add_labels(label_name)[0]
    # ...and add some bling!
    label.update(label_name, label_color, label_description)

    # Only one file, so our notebook will be it.
    this_notebook = [f for f in new_pr.files()][0]

    # The md5 has of the filename is part of the link for commenting.
    m = md5(this_notebook.filename.encode())

    # The only thing this URL needs added to it to go to a specific line
    # in the file is the line number.
    # About that "R" on the end: It indicates the line number is for the
    # "right" side of the difference, which turns out to be where our
    # file ends up.
    base_url_for_comment = (new_pr.html_url +
                            f'/files#diff-{m.hexdigest()}' +
                            'R')

    return base_url_for_comment


def commentify_all_notebooks(book_nb_path, original_nb_path,
                             comment_group=DEFAULT_COMMENT_GROUP):
    """
    Add comment-on-github links to each notebook in the book.
    """
    book_content_p = Path(book_nb_path)
    original_p = Path(original_nb_path)

    to_comment = [b for b in book_content_p.glob('??-??-*.ipynb')]
    originals = [original_p / book.name for book in to_comment]

    if not all(o.exists() for o in originals):
        raise RuntimeError('One of the files does not exist in originals')

    for book, original in zip(to_comment, originals):
        print(f'on {book.name}')
        github_magic(str(book), str(original), comment_group=comment_group)
        # Don't be greedy
        time.sleep(1)


def find_headers(notebook_name, highest_level=2, lowest_level=3):
    """
    Find all headers in the specified range in the notebook.

    Parameters
    ----------
    notebook_name : str
        Name of a Jupyter notebook.

    highest_level : int, optional
        The highest level header to be identified (1 is highest, 6 is lowest).

    lowest_level : int, optional
        The lowest level header to be identified (1 is highest, 6 is lowest).
        Must be less than or equal to ``highest_level``.

    Returns
    -------

    dict
        Keys of the dictionary are the headings (including the leading
        hashtags), values are the line number on which the heading
        appears in the json source of the notebook.
    """
    headings = {}

    # No idea at all why any line number offset is needed, but this
    # seems to do the trick.
    line_number_offset = 1

    # Generate the part of the regex pattern that represents the hashtags
    # that are the beginning of a heading.
    hashtags = []
    for level in range(highest_level, lowest_level + 1):
        hashtags.append('#' * level)

    hashtags = '|'.join(hashtags)

    header = re.compile(r'(' + f'({hashtags})' + r' +[a-zA-Z].+?\n)')

    notebook = nbf.read(notebook_name, as_version=4)
    for cell in markdown_cells(notebook):
        groups = [g for g in re.finditer(header, cell['source'])]
        for g in groups:
            # We have a header, will get line numbers shortly
            headings[g.group(0)] = -1

    with open(notebook_name, 'r') as f:
        nb_lines = f.readlines()

    for head in headings.keys():
        for line_num, line in enumerate(nb_lines):
            if head[:-1] in line:
                if headings[head] > 0:
                    print(f'Oh no! Bad {notebook_name}')
                    print(f'...duplicate heading: {head}')
                    raise RuntimeError('oh no')
                headings[head] = line_num + line_number_offset

    return headings


def delete_branches_prs(comment_group, repo):
    """
    WARNING: THIS IRREVERSIBLY NUKES STUFF ON GITHUB. It does not in any way
    affect local files.

    Close all PRs and delete all branches with the label whose
    name is ``comment_group``.

    Parameters
    ----------

    comment_group : str
        The label used for PRs/branches in this bundle for review.

    repo : github3 Repo
        The repository on which to act.
    """
    # 1 Get a list of the "issues" with this label
    pr_issues = [_ for _ in repo.issues(labels=comment_group)]
    # 2 GEt a list of refs to use later for deleting branches
    refs = [ref for ref in repo.refs()]

    # Buildup lists of closures/deletions so that the user can be warned
    # of what will be deleted.
    PRs_to_close = []
    branches_to_delete = []

    for pri in pr_issues:
        # 2. Get the PR
        pr = pri.pull_request()
        # 3. Get name of the branch
        head = pr.head
        # 4. Add the pr to the closure list
        PRs_to_close.append(pr)

        # 5. Find the ref that matches this branch
        for ref in refs:
            if ref.ref.endswith(head.ref):
                # Add the branch to the deletion list
                branches_to_delete.append(ref)
                break
        else:
            raise RuntimeError(f'No ref for branch {head.ref} found')

    warning = [f"Pull requests to be closed ({len(PRs_to_close)}):\n"]
    for pr in PRs_to_close:
        warning.append(f" - #{pr.number} {pr.title}")
        warning.append(f"\t\t{pr.html_url}")

    response = ''
    print('\n'.join(warning), '\n')
    while response not in ['yes', 'no']:
        response = input("DO YOU WANT TO CLOSE "
                         "THESE PRs (yes or no)?  >  ")

    if response == 'yes':
        for pr in PRs_to_close:
            # Be a good citizen
            time.sleep(random.uniform(0.1, 0.5))
            pr.close()

    print('\n\n')
    warning = [f"These {len(branches_to_delete)} branches will "
               f"be PERMANENTLY DELETED:\n"]

    for branch in branches_to_delete:
        warning.append(f"\t{branch.ref}")

    response = ''
    print('\n'.join(warning), '\n')

    while response not in ['yes', 'no']:
        response = input("DO YOU WANT TO DELETE THESE "
                         "BRANCHES (yes or no)?  >  ")

    if response == 'yes':
        for branch in branches_to_delete:
            branch.delete()
