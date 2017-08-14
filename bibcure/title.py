from __future__ import print_function
from builtins import input
from titletobib.crossref import get_bib_from_title
import bibtexparser


def update_bib(bib, get_first=True):
    if "doi" not in bib and "title" in bib and "journal" in bib:
        if "arxiv" not in bib["journal"].lower():
            found, bib_string = get_bib_from_title(bib["title"], get_first)
            if found:
                bib = bibtexparser.loads(bib_string).entries[0]
    return bib


def update_bibs_get_doi(bibs):
    action = input("Try to get DOI?y(yes, automatic)/m(manual)/n(do nothing)")

    if action not in ("y", "m", "n"):
        return update_bibs_get_doi(bibs)

    if action == "n":
        return bibs

    get_first = True if action == "y" else False

    for i, bib in enumerate(bibs):
        bibs[i] = update_bib(bib, get_first)
