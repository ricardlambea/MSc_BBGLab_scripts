#!/usr/bin/python3

"""
This script takes as input the aliquot_IDs from BCRA-PCAWG and does the matching with these IDs in the
BRCA-TCGA dictionary.
As first argument it requires the absolute path from the TCGA project-specific dictionary; as second argument it
needs the absolute path from the file holding the PCAWG Aliquot_IDs; and as third argument it needs the
absolute path of the new intersection file that will be generated.
"""

import pandas as pd
import sys

# tcga = pd.read_csv('/workspace/projects/cndrivers/expression/testing/brca_dictionary.tsv', sep="\t")
# pcawg = pd.read_csv('/workspace/projects/cndrivers/pcawg_brca.tsv', sep="\t", header=None)
tcga = pd.read_csv(sys.argv[1], sep="\t")
pcawg = pd.read_csv(sys.argv[2], sep="\t", header=None)

pcawg_uuids = pcawg[5].to_list()

tcga = tcga.to_numpy()
m = [item.astype(str) for item in tcga]
j = list()
for item in m:
    j.append("\t".join(item))

counter = 0
row2print = list()

# with open('/workspace/projects/cndrivers/intersection.txt','w') as outfile:
with open(sys.argv[3], 'w') as outfile:
    for uuid in pcawg_uuids:
        for row in j:
            if uuid in row:
                counter += 1
                row2print.append(row)
        if counter > 1:
            sys.stderr.write(uuid + " appears more than once!!\n")
        elif counter < 1:
            sys.stderr.write(uuid + " was not found!!\n")
        else:
            outfile.write(uuid + "\t")
            for item in row2print:
                outfile.write(item + "\n")
        counter = 0
        row2print.clear()


### OLD CODE

# with open('/workspace/projects/cndrivers/test_intersect.txt','w') as outfile:
#     for uuid in pcawg_uuids:
#         for row in tcga:
#             if uuid in list(row):
#                 counter += 1
#                 row2print.append(row)
#         if counter > 1:
#             sys.stderr.write(uuid + " appears more than once!!\n")
#         elif counter < 1:
#             sys.stderr.write(uuid + " was not found!!\n")
#         else:
#             for item in row2print:
#                 outfile.write(uuid + "\t" + str(item) + "\n")
#         counter = 0
#         row2print.clear()

