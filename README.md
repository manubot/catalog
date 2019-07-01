# Manubot Catalog

[![Travis CI Build Status](https://travis-ci.com/manubot/catalog.svg?branch=master)](https://travis-ci.com/manubot/catalog)

Manubot is a workflow and set of tools for the next generation of scholarly publishing.
Learn more at <https://manubot.org/>.

This repository stores a catalog of mansucripts that were made using Manubot.
These manuscripts are displayed at <https://manubot.org/catalog/>.
The `catalog.json` file produced by this codebase is available at `https://manubot.github.io/catalog/catalog.json`.

## Contributing

We encourage anyone to add mansucripts to the catalog.
In-progress manuscripts are acceptable.
Basically, any manuscript that has a substantial amount of content that is not part of [Rootstock](https://manubot.github.io/rootstock/) is of interest.

To add a manuscript to the catalog, add a record in [`catalog.yml`](catalog.yml).
`catalog.yml` is a YAML formatted file.
An example manuscript with documentation comments is below:

```yaml
- repo_url: https://github.com/greenelab/deep-review  # URL to GitHub repository with Manuscript source code
  html_url: https://greenelab.github.io/deep-review/  # URL for Manubot HTML output (usually hosted by GitHub Pages)
  preprint_citation: doi:10.1101/142760  # optional: Manubot-style citation for a preprint corresponding to the manuscript
  journal_citation: doi:10.1098/rsif.2017.0387  # optional: Manubot-style citation for a published article corresponding to the manuscript
```

For more information on how to create citations for `preprint_citation` and `journal_citation`, see Manubot's citation-by-identifier [documentation here](https://github.com/manubot/rootstock/blob/master/USAGE.md#citations).
