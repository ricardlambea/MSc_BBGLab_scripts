#!/usr/bin/python3

"""
This script goes through all the projects in TCGA and retrieves all the genes present in each one of
the significant regions detected by GISTIC2.0. Then it creates an output file where each row is a
region, the information of the mutation happening in that region, and all the genes involved.
"""

import pandas as pd
import sys


# project = sys.argv[1]
project = 'tcga_acc/'
print("Parsing data from project " + project.rstrip("/") + ".")

path = "/workspace/projects/cndrivers/tcga/" + project + "gistic_output/amp_genes.conf_95.txt"
input_f = pd.read_csv(path, sep="\t", header=None)
# print(input_f)
cytobands = input_f.iloc[0,1:-1].to_list()
longitude_amps = input_f.iloc[3,1:-1].to_list()
amp_genes = input_f.iloc[4:,1:-1]
amp_genes.columns = cytobands
amp_genes = amp_genes.transpose()
amp_genes.insert(0, 'Mutation', [ 'Amplification' for i in range(len(cytobands)) ], True)
amp_genes.insert(1, 'Position', [ i for i in longitude_amps ], True)
# print(amp_genes)
amp_dict = dict()
for index, row in amp_genes.iterrows():
    chrarm = index # chromosomal arm region
    muttype_and_genomicpos = row[:2].to_list() # mutation type and genomic position
    genes = {x for x in set(row.to_list()[2:]) if pd.notna(x)} # set of genes
    amp_dict[index, muttype_and_genomicpos[0], muttype_and_genomicpos[1]] = genes


path2 = "/workspace/projects/cndrivers/tcga/" + project + "gistic_output/del_genes.conf_95.txt"
input_f2 = pd.read_csv(path2, sep="\t", header=None)
cytobands2 = input_f2.iloc[0,1:-1].to_list()
longitude_dels = input_f2.iloc[3,1:-1].to_list()
del_genes = input_f2.iloc[4:,1:-1]
del_genes.columns = cytobands2
del_genes = del_genes.transpose()
del_genes.insert(0, 'Mutation', [ 'Deletion' for i in range(len(cytobands2)) ], True)
del_genes.insert(1, 'Position', [ i for i in longitude_dels ], True)
# print(del_genes)
del_dict = dict()
for index, row in del_genes.iterrows():
    chrarm = index # chromosomal arm region
    muttype_and_genomicpos = row[:2].to_list() # mutation type and genomic position
    genes = {x for x in set(row.to_list()[2:]) if pd.notna(x)} # set of genes
    del_dict[index, muttype_and_genomicpos[0], muttype_and_genomicpos[1]] = genes


with open("/workspace/projects/cndrivers/tcga/" + project + "genes_x_region_amp.tsv", 'w') as fh:
    for key, value in amp_dict.items():
        fh.write("%s\t%s\t%s\t" %(key[0],key[1],key[2]))
        for i in value:
            fh.write("%s\t" %(i))
        else:
            fh.write("\n")

with open("/workspace/projects/cndrivers/tcga/" + project + "genes_x_region_del.tsv", 'w') as fh:
    for key, value in del_dict.items():
        fh.write("%s\t%s\t%s\t" %(key[0],key[1],key[2]))
        for i in value:
            fh.write("%s\t" %(i))
        else:
            fh.write("\n")

