# CCD guide: preparation for publishing

Want to try to get all of the processing steps in going from notebooks to book in one place.

## Remove old outputs (in python)

```python
from process_for_book import clean
clean()
```

or

```shell
python -c "from process_for_book import clean; clean()"
```

## Generate list of notebooks to process (fish version):

```shell
# The sort below is important because later notebooks depend on
# output of earlier ones.
set to_conv (find . -depth 1 -name 0[01234568]-\?\?-\*.ipynb | sort -)
```

## Run the notebooks to generate output (fish version)

``shell
for conv in $to_conv
    jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=-1 $conv
end
```

## Move the generated notebooks to separate folder (fish shown)

```shell
# This can be refactored easily.
python process_for_book.py
```

## Replace links to notebooks with links to html

**Modifies notebooks in the directory with the *converted* notebooks**

```python
from pathlib import Path
import os

from process_for_book import replace_links_in_notebook

os.chdir('converted')

p = Path('.')

notebooks = p.glob('*.ipynb')
for notebook in notebooks:
    replace_links_in_notebook(str(notebook))

os.chdir('..')
```

## Set GitHub token


```shell
set -x GITHUB_TOKEN your_token_here
```

## Clean up old review rounds on GitHub, if any

**Set `GITHUB_TOKEN` first**

```python
from add_github_links import delete_branches_prs, get_github_repo
repo = get_github_repo('astropy', 'ccd-reduction-and-photometry-guide')
# Replace the name review-8e187b6 with the actual name you want
# to eliminate, of course.
delete_branches_prs('review-8036850', repo)
```


## Copy content from the working directory to content

This is silly, but right now it needs a copy/paste. DO NOT MOVE because
the logic in the link-adding code below is a little janky.

```shell
cp converted/* /Users/mcraig/Documents/Research/ccd-as-book/content
```

## Add links for commenting on each section

**Set `GITHUB_TOKEN` first**

```python
from add_github_links import commentify_all_notebooks
converted_for_book = '/Users/mattcraig/development/ccd-as-book/content/'
path_to_original = '.'
commentify_all_notebooks(converted_for_book,
                         path_to_original,
                         comment_group='review-8036850')
```

## Build the book markdown locally

```shell
# Change to root directory of book
jupyter-book build .
```

## Build/serve to check locally

Make ruby not suck: `set -x CONDA_BUILD_SYSROOT /Library/Developer/CommandLineTools/SDKs/MacOSX10.14.sdk/`

```shell
# Change to root directory of book
make serve
```

## CCD guide message for reviewers

Dear X,

Thanks for agreeing to take a look at the draft guide to reducing CCD data using astropy.

The most straightforward way to provide feedback does not require you to run any of the code on your computer (though that is an option if you prefer it).

You will need a free account on GitHub.com to make comments, and you will need to log into GitHub.

Please go to the book at https://mwcraig.github.io/ccd-as-book/00-00-Preface.html

Below each section heading is a link that says "Click here to comment on this section in GitHub".

Clicking on any of those links as you read through the guide will take you to the location of that section on GitHub so that you can make comments.

To make a comment:

+ When you move your mouse over a line, a blue "plus" sign will be visible at the beginning of the line (if you are logged in to GitHub).
+ Click that blue plus and a box for making a comment will appear.
+ When you are done writing your comment, click either "Add single comment" or "Start a review".
+ If you click "Start a review" then you will need to complete the review by clicking on "Finish your review" in the upper right hand corner of the screen.

Thanks,
Matt Craig
