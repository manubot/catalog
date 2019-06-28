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
    input_catalog = yaml.safe_load(read_file)
logging.info(f"catalog consists of {len(input_catalog):,} records")

"""
- manubot:
    - repository_url: https://github.com/greenelab/deep-review
    - manuscript_url: https://greenelab.github.io/deep-review/
  preprint:
    - citaiton_id: doi:10.1101/142760
  journal:
    - citation_id: doi:10.1098/rsif.2017.0387
"""

def process_record(record):
    """
    Expand a catalog record with retrieved metadata
    """
    output = {}
    output['manubot'] = {
        'repository_url': record['repository_url'],
        'manuscript_url': record['manuscript_url'],
        'citation': f"url:{record['manuscript_url']}",
    }
    for publication_type in 'preprint', 'journal':
        citation = record.get(f'{publication_type}_citation')
        if not citation:
            continue
        if not is_valid_citation(citation):
            continue
        output[publication_type] = {
            'citation': citation,
        }
    for item in output.values():
        citation = standardize_citation(item['citation'])
        item['csl_item'] = citation_to_citeproc(citation)
    return output


catalog = []
for record in input_catalog:
    catalog.append(process_record(record))

json_catalog = json.dumps(catalog, indent=2, ensure_ascii=False)
directory.joinpath('output').mkdir(exist_ok=True)
directory.joinpath('output', 'catalog.json').write_text(json_catalog + '\n')
