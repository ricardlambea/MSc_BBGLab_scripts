#!/usr/bin/python3

"""
This script takes as first argument one of the output files of gistic, either amp_genes.conf_99.txt
or del_genes.conf_99.txt, and generates as output one file with all the significant genes found by GISTIC.
As second argument it requires the absolute path of the output file.
"""

import sys
import pandas as pd
import re
import os


df1 = pd.read_csv(sys.argv[1], sep="\t")

genes1 = df1.iloc[3:,1:]
final_list1 = []

for (colname, coldata) in genes1.iteritems():
    if re.search("Unnamed", colname):
        continue
    tmp_list1 = coldata[coldata.notna()].values.tolist()
    final_list1.extend(tmp_list1)

with open(str(sys.argv[2]), 'w') as output:
    for gene in final_list1:
        output.write("%s\n" %gene)
    output.close()

