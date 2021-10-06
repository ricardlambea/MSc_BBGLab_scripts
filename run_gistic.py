#!/usr/bin/python3

"""This scripts runs the software GISTIC2.0 on the given input data."""

import sys
import subprocess
import argparse

parser = argparse.ArgumentParser(description="This scripts runs the software GISTIC2.0 on the given input data.", epilog="Good luck in your copy number analysis journey!")
parser.add_argument('runner', type=str, help='Absolut path to the runner.sh script.')
parser.add_argument('b', type=str, help='Absolut path to the directory where the resulting files will be stored. This directory has to be created before the script is run.')
parser.add_argument('seg', type=str, help='Absolut path to the segmentation file, which is the input required by GISTIC2.0.')
parser.add_argument('refgene', type=str, help='Absolut path to the reference genome file required by GISTIC2.0. These files can be found in the directory "/workspace/projects/cndrivers/gistic_software/refgenefiles/".')
args = parser.parse_args()

create_dir = subprocess.run(['mkdir',sys.argv[2]])
result = subprocess.run([sys.argv[1],'-b',sys.argv[2],'-seg',sys.argv[3],'-refgene',sys.argv[4]])
