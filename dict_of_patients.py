#!/usr/bin/python3

"""
This script takes as input 5 arguments: 1) The absolute path of the copy-number file; 2) The absolute path of the global expression matrix; 3) The absoulte path of the TCGA dictionary generated for the current project;
4) The absolute path of the new 2 column dictionary that will be generated; and 5) The absolute path of the patient-specific expression matrix that will be generated.
Then, the script will create two files, one for the two column dictionary of the current patients, and another for the filtered expression matrix.
"""

import sys
import pandas as pd
import time
start_time = time.time() # calculate execution time

# cnfile = pd.read_csv("/workspace/projects/cndrivers/test_brca_fullrun/brca_ASCAT2_GISTIC.txt", sep="\t", header=None)
# expressionfile = pd.read_csv("/workspace/projects/cndrivers/expression/TCGA_counts_barcode.tsv", sep="\t", index_col=0)
# tcga_dictionary = pd.read_csv("/workspace/projects/cndrivers/test_brca_fullrun/brca_dictionary_ene28.tsv", sep="\t")
cnfile = pd.read_csv(sys.argv[1], sep="\t", header=None)
expressionfile = pd.read_csv(sys.argv[2], sep="\t", index_col=0)
tcga_dictionary = pd.read_csv(sys.argv[3], sep="\t")
print("Input data loaded.")

counter = 0
linktable = list()
aliquot_uuids = cnfile[0].unique() # get only unique aliquotIDs
for aliquot_id in aliquot_uuids:
    for line in tcga_dictionary.values.tolist():
        if aliquot_id in line: # if cn aliquotID is in the current line of TCGA dictionary, print both
            item = aliquot_id + "\t" + str(line)
            linktable.append(item)
            counter += 1 # just to keep track of the number of ids, should always be 1062 for all TCGA-BRCA
            break
# print(counter)

all_sampleIDs = list(expressionfile.columns)
expressionIDs = list()

for id in all_sampleIDs:
    for line in linktable:
        if id in line:
            item = id + "\t" + line.split("\t")[0]
            expressionIDs.append(item)
            break
# print(len(expressionIDs)) # should be 1165 for TCGA-BRCA all patients

# print("--- %s seconds ---" % (time.time() - start_time))

with open(sys.argv[4],'w') as outfile:
    for i in expressionIDs:
        outfile.write(i + "\n")
print("Dictionary " + str(sys.argv[4]) + " ready.")
#
# filter the expression matrix to just store the info about the patients of a specific project
ensembl_ids = list(expressionfile.index.values)
df = pd.DataFrame(index=ensembl_ids)
expressionIDs = [ i.split("\t")[0] for i in expressionIDs ]
for id in expressionIDs:
    col = expressionfile[id]
    df[id] = col
df.to_csv(sys.argv[5], sep="\t")
print("Filtered expression matrix ready.")






