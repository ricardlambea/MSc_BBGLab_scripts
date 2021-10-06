#!/usr/bin/python3

"""
This script generates the qmap file to run the DESeq2 normalization on the given data.
When executing the qmap, the parameters like the memory or the number of cores are hardcoded.
"""

import subprocess
import sys
import argparse

parser = argparse.ArgumentParser(description="This script generates the qmap file to run the DESeq2 normalization on the given data.")
parser.add_argument('norm_script', type=str, help='Absolute path to the R normalization script.')
parser.add_argument('gene_list', type=str, help='Absolute path of the file holding all the genes that have to be analyzed.')
parser.add_argument('ensembl', type=str, help='Absolute path of the tsv file containing the genes returned as significant by GISTIC2.0, and their corresponding ensembl_IDs.')
parser.add_argument('all_thres', type=str, help='Absolute path of the GISTIC output file named "all_thresholded.by_genes.txt".')
parser.add_argument('expression', type=str, help='Absolute path of the tsv expression file holding the information of the raw counts of transcripts.')
parser.add_argument('dictionary', type=str, help='Absolute path of the tsv file that holds all the information of the cases and files on TCGA.')
parser.add_argument('deseq2_output', type=str, help='Name of the deseq2 output file that will be generated.')
parser.add_argument('qmap_file', type=str, help='Name of the qmap file that will be generated and immediately run.')
args = parser.parse_args()

# generate qmap file
subprocess.run(['qmap', 'template', '--conda-env', 'R', 'Rscript ' + sys.argv[1] + ' {{' + sys.argv[2] + '}} ' + sys.argv[3] + ' ' + sys.argv[4] + ' ' + sys.argv[5] + ' ' + sys.argv[6] + ' ' + sys.argv[7], '-o', sys.argv[8]])

# execute qmap file previosuly generated
subprocess.run(['qmap', 'submit', sys.argv[8], '-m', '15', '-c', '1', '-g', '1','--max-running','50'])

