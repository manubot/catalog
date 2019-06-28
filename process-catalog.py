import json
import logging
import pathlib

import yaml
from manubot.cite.util import (
    is_valid_citation,
    standardize_citation,
    citation_to_citeproc,
)

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

directory = pathlib.Path(__file__).parent
with directory.joinpath('catalog.yml').open() as read_file:
    catalog = yaml.safe_load(read_file)
logging.info(f"catalog consists of {len(catalog):,} records")


def process_record(record):
    """
    Expand a catalog record with retrieved metadata
    """
    record['manubot_html_csl_item'] = citation_to_citeproc(f"url:{record['manubot_html_url']}")
    for publication_type in 'preprint', 'journal':
        citation = record.get(f'{publication_type}_cite')
        if not citation:
            continue
        if not is_valid_citation(citation):
            continue
        citation = standardize_citation(citation)
        csl_item = citation_to_citeproc(citation)
        record[f'{publication_type}_csl_item'] = csl_item
    return record


for record in catalog:
    process_record(record)

json_catalog = json.dumps(catalog, indent=2, ensure_ascii=False)
directory.joinpath('output').mkdir(exist_ok=True)
directory.joinpath('output', 'catalog.json').write_text(json_catalog + '\n')
