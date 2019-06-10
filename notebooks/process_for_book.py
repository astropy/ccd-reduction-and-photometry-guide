from pathlib import Path
from argparse import ArgumentParser

input_nb_pattern = r'0[0123].*.ipynb'

p = Path('.')
(p / 'converted').mkdir(exist_ok=True)
input_notebooks = p.glob(input_nb_pattern)
#print([i for i in input_notebooks])
#print([i for i in p.iterdir()])

# CONVERT TO NOTEBOOK AND EXECUTE

#later...

# for conv in $to_convert
#   jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=-1 $conv
# end

# Fix names

converted_nb_pattern = '*.nbconvert.ipynb'

destination_converted_nbs = []
for path in p.glob(converted_nb_pattern):
    name = str(path)
    name = name.replace('(', '')
    name = name.replace(')', '')
    name = name.replace('.nbconvert', '')

    n_dots = name.count('.') - 1
    if n_dots:
        name = name.replace('.', '-', n_dots)

    print(name)
    path.rename(p / 'converted' / name)
