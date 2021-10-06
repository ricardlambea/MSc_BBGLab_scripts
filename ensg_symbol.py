#!/usr/bin/python3

"""
This script is a reused part of Claudia's script to extract information of genes. In this case it retrieves
the ensembl ID and the gene symbol for each gene, and returns an output file with two columns, respectively.
"""

import os, sys
os.environ["PATH"] = os.path.dirname(sys.executable) + os.pathsep + os.environ["PATH"]
from glob import glob
import warnings
warnings.simplefilter("ignore") # Change the filter in this process
os.environ["PYTHONWARNINGS"] = "ignore" # Also affect subprocesses
import pandas as pd

GENCODE_RELEASE = '35'
BUILD = 'hg38'
RELEASE = '2'
FEATURE = 'annotation'

gencode_annotations = glob(f'/workspace/projects/genomic_regions/raw_data/gencode/release_{GENCODE_RELEASE}/{BUILD}/gencode.v{GENCODE_RELEASE}*.{FEATURE}.gtf.gz')
# gencode_annotations = glob(f'/workspace/projects/cndrivers/gencode_head') # to test only

if len(gencode_annotations) == 1:
    gencode_annotations = gencode_annotations[0]
else:
    print('Glob mached more than on file:')
    for f in gencode_annotations:
        print('-', f)

print(gencode_annotations)


gencode = pd.read_csv(
    gencode_annotations,
    compression='gzip',
    sep="\t",
    header=None,
    skiprows=5,
    usecols=[0, 2, 3, 4, 6, 8],
    names=['CHROMOSOME', 'TYPE', 'START', 'END', 'STRAND', 'INFOS']
)

print(len(gencode))


# Remove the `chr` prefix from the CHROMOSOME column
gencode['CHROMOSOME'] = gencode['CHROMOSOME'].map(lambda x: x[3:])

# Filter chromosomes
chromosomes = set(map(str, list(range(1, 23)) + ['X', 'Y', 'M']))
gencode['CHROMOSOME_FILTER'] = gencode.apply(lambda x: 'PASS' if x['CHROMOSOME'] in chromosomes else 'FAIL', axis=1)
gencode = gencode.loc[gencode['CHROMOSOME_FILTER'] == 'PASS'].copy()
gencode.drop(['CHROMOSOME_FILTER'], axis=1)

# Parse the INFOS column
gencode['INFOS'] = gencode['INFOS'].map(
    lambda line: {
        i.split()[0]: i.split()[1].replace('"', '') for i in line.split(";") if len(i.split()) > 1
    }
)

# Get gene ID
gencode['GENE_ID'] = gencode['INFOS'].map(lambda x: x.get('gene_id', 'NaN.'))
# Remove gene ID version (eg 'ENSG00000223972.5_2' -> 'ENSG00000223972')
# If 'PAR_Y' (gene in pseudoautosomal chrY region) in gene ID, keep it so that it can be distinguished from chrX gene
gencode['GENE_ID'] = gencode.apply(lambda x: x['GENE_ID'].split('.')[0] if 'PAR_Y' not in x['GENE_ID'] else f"{x['GENE_ID'].split('.')[0]}_PAR_Y", axis=1)

# Get transcript ID
gencode['TRANSCRIPT_ID'] = gencode['INFOS'].map(lambda x: x.get('transcript_id', 'NaN.'))
# Remove transcript ID version (eg 'ENST00000223972.5_2' -> 'ENST00000223972')
# If 'PAR_Y' (gene in pseudoautosomal chrY region) in gene ID, keep it so that it can be distinguished from chrX gene
gencode['TRANSCRIPT_ID'] = gencode.apply(lambda x: x['TRANSCRIPT_ID'].split('.')[0] if 'PAR_Y' not in x['TRANSCRIPT_ID'] else f"{x['TRANSCRIPT_ID'].split('.')[0]}_PAR_Y", axis=1)

# Get gene type
gencode['GENE_TYPE'] = gencode['INFOS'].map(lambda x: x.get('gene_type', 'NaN'))

# Get symbol
gencode['SYMBOL'] = gencode['INFOS'].map(lambda x: x.get('gene_name', 'NaN'))

# Get transcript type
gencode['TRANSCRIPT_TYPE'] = gencode['INFOS'].map(lambda x: x.get('transcript_type', 'NaN'))

gencode = gencode[['GENE_ID','SYMBOL']] # subset of original gencode dataframe

ensg_symbol = dict()
[ensg_symbol.setdefault(x[0], x[1]) for x in gencode.to_numpy()] # convert to dictionary to store only unique elements

a = pd.DataFrame.from_dict(ensg_symbol, orient='index', columns=['SYMBOL']) # reconvert to dataframe
a.reset_index(level=0, inplace=True) # set index as a column
a.rename(columns={'index': 'ENSG', 'SYMBOL': 'SYMBOL'}, inplace=True) # rename index column
a.to_csv(path_or_buf="/workspace/projects/cndrivers/ensg_symbol.tsv", sep="\t", index=False)
