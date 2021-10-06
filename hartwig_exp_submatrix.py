#!/usr/bin/python3

import pandas as pd
import os
import sys
from glob import glob
import re

expressionfile = sys.argv[1] # path of the global expression matrix
expressionfile = pd.read_csv(expressionfile, sep="\t", index_col=0, compression='gzip')

hartwig_dirs = [ x for x in glob("/workspace/projects/cndrivers/hartwig/*", recursive=True) if os.path.isdir(x) ]
ids_without_expression = []

for dir in hartwig_dirs:
    print(dir)
    for file in os.listdir(dir):
        if re.match("gistic_input_\w*.tsv", file):
            print("Reading file: " + str(file))
            cnfile = pd.read_csv(dir + "/" + file, sep="\t", header=None)  # cn file project-especific
            break
        else:
            continue
    cnfile_ids = cnfile[0].unique()
    # print(cnfile_ids)

    # filter the expression matrix to just store the info about the patients of a specific project
    ensembl_ids = list(expressionfile.index.values)
    df = pd.DataFrame(index=ensembl_ids)
    for id in cnfile_ids:
        try:
            col = expressionfile[id]
            df[id] = col
        except:
            ids_without_expression.append(id)
    df.to_csv(dir + '/expression_matrix.tsv', sep="\t") # path of the generated project-especific expression matrix
    print("Filtered expression matrix copied in: " + str(dir) + "/expression_matrix.tsv.")
    print("File of ids without expression has this length: " + str(len(ids_without_expression)))

df2 = pd.DataFrame(data=ids_without_expression)
df2.to_csv('/workspace/projects/cndrivers/hartwig/ids_without_expression.txt', header=False,index=False, sep="\t") # path of the file holding all the ids without expression
