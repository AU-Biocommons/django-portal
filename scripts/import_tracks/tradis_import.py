"""Bulk import tradis-vault genomes from excel sheet."""

import json
import os
import pandas as pd
import requests
from pathlib import Path

os.chdir(Path(__file__).parent)

XLS_PATH = Path("data/schembri_tracks.xlsx")
JSON_OUTFILE = Path("data/tracks.json")


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


class PubmedDoiFetcher:
    """Fetch DOIs by scraping pubmed."""

    BASE_URL = "https://pubmed.ncbi.nlm.nih.gov"
    DOI_HTML_ANCHOR = 'data-ga-action="DOI"'

    def __init__(self):
        self.cache = {}

    def get(self, pubmed_id):
        """Fetch pubmed webpage and parse out DOI."""
        if pubmed_id in self.cache:
            print(f"Returning cached DOI for {pubmed_id}...")
            return self.cache[pubmed_id]
        print(f"Fetching DOI for pubmed ID {pubmed_id}... ")
        if not pubmed_id or pd.isna(pubmed_id):
            return None
        r = requests.get(self.BASE_URL + f"/{pubmed_id}")
        if r.status_code != 200:
            return None
        doi = self._parse_doi(r.text)
        self.cache[pubmed_id] = doi
        return doi

    def _parse_doi(self, html):
        """Parse DOI from pubmed webpage."""
        return (
            html
            .split(self.DOI_HTML_ANCHOR)[1]
            .split('<')[0]
            .strip(' \n<>')
        )


pm_doi_fetcher = PubmedDoiFetcher()
EXPECT_COLS = {
    "lab_name": "Lab Name",
    "genome_accession": "Ref sequence",
    "name": "Name",
    "description": "Description",
    "reference": "Source",
    "condition": "Condition",
    "ncbi_bioproject": "Submission ID",
    "doi": (pm_doi_fetcher, "Pubmed ID"),
}
EXTENDED_METADATA_KEYS = [
    # Add keys here that aren't listed above in EXPECT_COLS
    "Molecule",
    "Taxonomy ID",
    "Protocol",
    "Platform",
]

tracks = []
df = pd.read_excel(XLS_PATH, sheet_name=0, header=0)

for ix, row in df.iterrows():
    print(f"Parsing row {ix}... ")
    track = {
        key: get_value(row, field)
        if type(field) is not tuple
        else field[0].get(get_value(row, field[1]))
        for key, field in EXPECT_COLS.items()
    }
    track["group_name"] = "tradis-vault"
    metadata = {}
    for key in EXTENDED_METADATA_KEYS:
        val = get_value(row, key)
        if val:
            metadata[key] = val
    track["metadata"] = metadata
    tracks.append(track)

print(f"Writing tracks to {JSON_OUTFILE}")
with open(JSON_OUTFILE, "w") as f:
    json.dump(tracks, f)
print(f"Once you have created the required genomes,"
      " you can import the exported tracks with:\n"
      "$ python manage.py import_tracks"
      f" --json ../scripts/import_tracks/{JSON_OUTFILE}")
