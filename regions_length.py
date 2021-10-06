#!/usr/bin/python3

"""
This script goes through all the projects of all datasets and retrieves the length of each one of the regions.
Then it creates an output file with two columns, the first one for the amplified regions' length,
and the second one for the deleted regions' length (only numbers).
"""

import sys
import pandas as pd
import re

project = sys.argv[1]
# project = 'tcga_brca/'
out_path = sys.argv[2] # "/workspace/projects/cndrivers/tcga/copy_number_lengths.tsv"
print("Parsing data from project " + project.rstrip("/") + ".")

#### AMPLIFICATIONS

# the script needs to be run 3 times, one for each path. Remember to uncomment the corresponding line of code
# path = '/workspace/projects/cndrivers/tcga/' + project + "gistic_output/amp_genes.conf_95.txt"
# path = '/workspace/projects/cndrivers/hartwig/' + project + "gistic_output/amp_genes.conf_95.txt"
path = '/workspace/projects/cndrivers/pcawg_open/' + project + 'amp_genes.conf_95.txt'

input_f = pd.read_csv(path, sep="\t", header=None)
long = input_f.iloc[3,1:-1].to_list()

final_list = []
for i in long:
    i = re.sub(r'^.*?:', '', i)
    start, end = i.split("-")[0], i.split("-")[1]
    length = int(end) - int(start) + 1
    final_list.append(int(length))


#### DELETIONS

# path = '/workspace/projects/cndrivers/tcga/' + project + "gistic_output/del_genes.conf_95.txt"
# path = '/workspace/projects/cndrivers/hartwig/' + project + "gistic_output/del_genes.conf_95.txt"
path = '/workspace/projects/cndrivers/pcawg_open/' + project + 'del_genes.conf_95.txt'

input_f = pd.read_csv(path, sep="\t", header=None)
long = input_f.iloc[3,1:-1].to_list()

final_list2 = []
for i in long:
    i = re.sub(r'^.*?:', '', i) # substitute everything from the beginning until ':' by nothing
    start, end = i.split("-")[0], i.split("-")[1]
    length = int(end) - int(start) + 1
    final_list2.append(int(length))

global_list = [final_list, final_list2]

df = pd.DataFrame(global_list).transpose()
df.columns = ['Amplifications', 'Deletions']
for line in df.values.tolist():
    df['tumor_type'] = project.rstrip('/')

df.to_csv(path_or_buf=out_path, sep="\t", index=False, mode='a', header=False)


