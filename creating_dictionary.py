#!/usr/bin/python3

"""
Script used to create the master dictionary from TCGA that holds all the information about the cases that meet the criteria specified in the 'filters' section of the API query.
This script needs as first argument the TCGA project name, and as second argument the path where the resulting tsv file will be stored.
"""

import sys
import requests
import json
import pandas

### START API
fields = [      # information to be retrieved
    "project.project_id",   # TCGA project name
    "disease_type",   # Disease's name
    #"case_id",   # UUIDs
    "id",  # Same as caseUUIDs
    "aliquot_ids",   # UUIDs
    "submitter_aliquot_ids",   # IDs  format: TCGA-XX-XXXX-XXX-XXX-XXXX-XX
    "submitter_id",   # IDs  format: TCGA-XX-XXXX
    "samples.sample_type",   # Name of the sample type (Primary tumor, Blood derived, etc.)
    "sample_ids",   # UUIDs
    "submitter_sample_ids",   # IDs  format: TCGA-XX-XXXX-XXX
    # "files.file_id" # file UUIDs
]

fields = ",".join(fields)

cases_endpt = "https://api.gdc.cancer.gov/cases"

filters = {    # search using these filters
    "op": "and",
    "content": [
        {
            "op": "in",
            "content": {
                # "field": "project.program.name",
                # "value": "TCGA"
                "field": "project.project_id",
                "value": "TCGA-" + sys.argv[1].upper()
            }
        },
        {
            "op": "=",
            "content": {
                "field": "files.analysis.workflow_type",
                "value": "ASCAT2"
            }
        },
        {
            "op": "=",
            "content": {
                "field": "files.data_type",
                "value": "Allele-specific Copy Number Segment"
            }
        }
    ]
}

params = {
    "filters": json.dumps(filters),
    "fields": fields,
    "format": "TSV",
    "sort":"project.project_id:asc", # sort by TCGA project name
    "size": "1200"  # maximum number of lines to be returned in the output
}

response = requests.get(cases_endpt, params=params)
### END API

gdc = response.content.decode('utf-8')
gdc = gdc.split("\r\n")
gdc_clean = []
for i in gdc:
    gdc_clean.append(i.split("\t"))
df = pandas.DataFrame(gdc_clean, columns=gdc_clean[0]).drop(0)   # transform response to pandas dataframe to write to a tsv file afterwards
df.to_csv(path_or_buf=sys.argv[2], sep="\t", index=False)

