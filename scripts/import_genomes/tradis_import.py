"""Bulk import tradis-vault genomes from excel sheet."""

import json
import os
import pandas as pd
import requests
from pathlib import Path

os.chdir(Path(__file__).parent)

XLS_PATH = Path("data/230828_tradis_vault_samples_update.xlsx")
JSON_OUTFILE = Path("data/genomes.json")

pmid_dois = {}


def get_value(row, key):
    """Return row value while omitting NaN values."""
    value = row[key]
    if pd.isna(value):
        return None
    if type(value) is int or type(value) is float:
        return value
    if value.strip() == "":
        return None
    if value.strip() == "...":
        return None
    return value


def get_doi_from_pubmed(pubmed_id):
    """Fetch pubmed webpage and parse out DOI."""
    print(f"Fetching DOI for pubmed ID {pubmed_id}... ")
    if not pubmed_id or pd.isna(pubmed_id):
        return None
    url = f"https://pubmed.ncbi.nlm.nih.gov/{pubmed_id}"
    r = requests.get(url)
    if r.status_code != 200:
        return None
    doi = r.text.split('data-ga-action="DOI"')[1].split('<')[0].strip(' \n<>')
    return doi


genomes = []
df = pd.read_excel(XLS_PATH, sheet_name=0, header=0)

for ix, row in df.iterrows():
    print(f"Parsing row {ix}... ")
    if row["Pubmed ID"] in pmid_dois:
        doi = pmid_dois[row["Pubmed ID"]]
    else:
        doi = get_doi_from_pubmed(row["Pubmed ID"])
        pmid_dois[row["Pubmed ID"]] = doi

    genome = {
        "group_name": "tradis-vault",
        "lab_name": get_value(row, "Lab Name"),
        "name": get_value(row, "Name"),
        "description": get_value(row, "Description"),
        "reference": get_value(row, "Source"),
        "doi": doi,
        "strain": get_value(row, "Strain"),
        "species": "Escherichia coli",
        "condition": get_value(row, "Condition"),
        "ncbi_bioproject": get_value(row, "Submission ID"),
    }
    metadata = {}
    for key in [
        "File Type",
        "Taxonomy ID",
        "Platform",
    ]:
        val = get_value(row, key)
        if val:
            metadata[key] = val
    genome["metadata"] = metadata
    genomes.append(genome)

print(f"Writing genomes to {JSON_OUTFILE}")
with open(JSON_OUTFILE, "w") as f:
    json.dump(genomes, f)
