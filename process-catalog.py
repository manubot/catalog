import json
import logging
import pathlib

import requests
import yaml
from manubot.cite.citekey import citekey_to_csl_item, CiteKey

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

directory = pathlib.Path(__file__).parent
with directory.joinpath('catalog.yml').open() as read_file:
    input_catalog = yaml.safe_load(read_file)
logging.info(f"catalog consists of {len(input_catalog):,} records")


def get_journal(csl_item):
    keys = [
        'container-title',
        'container-title-short',
        'publisher',
        'event',
        'collection-title',
    ]
    for key in keys:
        if key in csl_item:
            return csl_item[key]


def get_title(csl_item):
    keys = [
        'title',
        'title-short',
    ]
    for key in keys:
        if key in csl_item:
            return csl_item[key]


def get_authors_text(csl_item, max_length=100):
    """
    Return string of authors like:
    Ching, Himmelstein, Beaulieu-Jones, Kalinin, Do, Way, Ferrero, Agapow, Zietz, Hoffman, Xie, Rosen, et al

    "et al" is inserted when adding another name would cause
    authors_text to exceed max_length.
    """
    authors = list()
    keys = [
        'author',
        'collection-editor',
        'composer',
        'container-author',
        'director',
        'editor',
        'editorial-director',
        'translator',
    ]
    for key in keys:
        if key in csl_item:
            authors = csl_item[key]
            break
    authors_text = ''
    for author in authors:
        try:
            # name = f"{author['given']} {author['family']}"]
            name = author['family']
        except KeyError:
            if 'literal' in author:
                name = author['literal']
            else:
                continue
        if authors_text:
            authors_text += ', '
        if len(name) + len(authors_text) > max_length:
            authors_text += 'et al'
            break
        authors_text += name
    return authors_text


def get_date(csl_item):
    """
    Return date in iso-like format, such as:
    2019
    2019-05
    2019-05-01
    """
    try:
        return '-'.join(f'{int(x):02d}' for x in csl_item['issued']['date-parts'][0])
    except Exception:
        return None


def get_date_summary(csl_item):
    """
    Return date like
    2019
    Jun 2019
    """
    date = get_date(csl_item)
    if not date:
        return None
    import calendar
    date_parts = [int(x) for x in date.split('-')]
    if len(date_parts) == 1:
        year, = date_parts
        month = 0
    else:
        year, month = date_parts[:2]
    return f"{calendar.month_abbr[month]} {year}".strip()


def get_thumbnail_url_from_html(url):
    """
    Extract the URL to a thumbnail image from the HTML
    <head> <meta> values returned by the query URL.
    """
    from bs4 import BeautifulSoup
    from urllib.parse import urljoin
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features="html.parser")
    for prop in 'og:image', 'twitter:image':
        if tag := soup.find("meta",  property=prop):
            break
    else:
        return None
    url = tag.get('content')
    url = urljoin(response.url, url)
    return url


def process_record(record):
    """
    Expand a catalog record with retrieved metadata
    """
    output = {}
    html_url = record.pop('html_url')
    output['manubot'] = {
        'repo_url': record.pop('repo_url'),
        'url': html_url,
        'citation': f"url:{html_url}",
    }
    if 'thumbnail_url' in record:
        thumbnail_url = record.pop('thumbnail_url')
    else:
        thumbnail_url = get_thumbnail_url_from_html(html_url)
    if thumbnail_url:
        output['manubot']['thumbnail_url'] = thumbnail_url
    for publication_type in 'preprint', 'journal':
        citation = record.pop(f'{publication_type}_citation', None)
        if not citation:
            continue
        citekey = CiteKey(citation)
        if not citekey.is_handled_prefix:
            logging.warning(f"unhandled citekey: {citation!r}")
            continue
        report = citekey.inspect()
        if report:
            logging.warning(f"citekey failed inspection: {citation!r}\n{report}")
            continue
        output[publication_type] = {
            'citation': citekey.standard_id,
        }
    for item in output.values():        
        csl_item = citekey_to_csl_item(item['citation'])
        if 'url' not in item and 'URL' in csl_item:
            item['url'] = csl_item['URL']
        item['title'] = get_title(csl_item)
        item['authors'] = get_authors_text(csl_item)
        item['journal'] = get_journal(csl_item)
        item['date_iso'] = get_date(csl_item)
        item['date_human'] = get_date_summary(csl_item)
        item['csl_item'] = csl_item
    output['extras'] = record
    return output


catalog = []
for record in input_catalog:
    catalog.append(process_record(record))

missing_thumbnails = '\n'.join(record["manubot"]["url"] for record in catalog if 'thumbnail_url' not in record["manubot"])
logging.info(f"The following manuscripts are missing thumbnails:\n{missing_thumbnails}")

json_catalog = json.dumps(catalog, indent=2, ensure_ascii=False)
directory.joinpath('output').mkdir(exist_ok=True)
directory.joinpath('output', 'catalog.json').write_text(json_catalog + '\n')
