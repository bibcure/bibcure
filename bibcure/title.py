from __future__ import print_function
from builtins import input
from titletobib.crossref import get_bib_from_title
import bibtexparser


def update_bib(bib, get_first=True):
    bib_id = bib["ID"]
    if "doi" not in bib and "title" in bib:
        found, bib_string = get_bib_from_title(bib["title"], get_first)
        if found:
            bib = bibtexparser.loads(bib_string).entries[0]
    bib["ID"] = bib_id
    return bib


def update_bibs_get_doi(bibs):
    action = input("Get DOI absent using the title?y(yes, automatic)/m(manual)/n(do nothing)")

    if action not in ("y", "m", "n"):
        return update_bibs_get_doi(bibs)

    if action != "n":
        get_first = True if action == "y" else False
        for i, bib in enumerate(bibs):
            if "journal" in bib:
                if "arxiv" not in bib["journal"].lower():
                    bibs[i] = update_bib(bib, get_first)
            else:
                    bibs[i] = update_bib(bib, get_first)

    return bibs
