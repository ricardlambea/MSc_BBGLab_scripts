#!/usr/bin/python3

"""
This script takes as first argument the TCGA file containing the fileUUIDs from TCGA-XXXX project (Primary Tumor),
and as second argument the file containing the PCAWG UUIDs as first field and their corresponding information from the
TCGA dictionary. Then it generates an output file (which name is set by means of the third argument) with all the
fileUUIDs that match between the two input files.
"""

import pandas as pd
import sys

tcga = pd.read_csv(sys.argv[1], sep="\t", header=None)
pcawg = pd.read_csv(sys.argv[2], sep="\t", header=None)

for tcga_item in tcga.values.tolist():
    for i in range(len(pcawg)):
        pcawg_item = pcawg.iloc[i].values.tolist()
        if str(tcga_item[0]) in pcawg_item:
            with open(sys.argv[3],'a') as outfile:
                outfile.write(str(tcga_item[0]) + "\n")
            break



