# Converting this to [`jupyter-book`](https://jupyter.org/jupyter-book/intro.html)

1. Run [`nbconvert`](https://nbconvert.readthedocs.io/en/latest/) on notebooks to generate output.
2. Change filenames to
    + replace periods with dash except for the one before file extension.
    + replace parentheses with nothing
4. Move renamed notebooks to `content` folder in `ccd-as-book` with
5. Update TOC in `ccd-as-book` if needed.
