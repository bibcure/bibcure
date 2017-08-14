from __future__ import print_function
from builtins import input
from titletobib.crossref import get_bib_from_title
import bibtexparser


def update_doi(bib, get_first=True):
    if "doi" not in bib and "title" in bib and "journal" in bib:
        if "arxiv" not in bib["journal"].lower():
            found, bib_string = get_bib_from_title(bib["title"], get_first)
            if found:
                bib = bibtexparser.loads(bib_string).entries[0]
    return bib


def update_bibs_get_doi(bibs):
    action = input("Check if arxiv items are published?a(automatic)/m(manual)/n(do nothing)")

    if action not in ("a", "m", "n"):
        return update_bibs_get_doi(bibs)

    if action == "n":
        return bibs

    get_first = True if action == "a" else False

    for i, bib in enumerate(bibs):
        bibs[i] = update_doi(bib, get_first)
