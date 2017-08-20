from __future__ import print_function
from builtins import input
from arxivcheck.arxiv import check_arxiv_published
import bibtexparser


def update_bib(bib_arxiv, automatic=True):
    bib_id = bib_arxiv["ID"]

    arxiv_id = bib_arxiv["journal"].partition(":")[2]
    arxiv_title = bib_arxiv["title"]

    found, published, bib_string = check_arxiv_published(
        arxiv_id,
        field="id"
    )
    bib = bibtexparser.loads(bib_string)
    if found:
        if automatic:
            bib = bib.entries[0]
        else:
            question = "{} >> {} ".format(arxiv_title,
                                          bib.entries[0]["title"])
            question += " was "
            if not published:
                question += " not published. Use bib from arxiv?y/n"
            else:
                question += " published."
                question += " Replace with new bib ?y/n"

            replace = input(question)
            if replace == "y":
                bib = bib.entries[0]

    else:
        print("'{}' not founded with a id {}".format(
            arxiv_title,
            arxiv_id
        ))

    bib["ID"] = bib_id
    return bib


def update_bibs_arxiv(bibs):
    action = input("Check if arxiv have been published?y(yes, automatic)/m(manual)/n(do nothing)")

    if action not in ("y", "m", "n"):
        return update_bibs_arxiv(bibs)
    if action != "n":

        automatic = True if action == "y" else False
        for i, bib in enumerate(bibs):
            if "journal" in bib:
                if "arxiv" in bib["journal"].lower():
                    bibs[i] = update_bib(bib, automatic)
    return bibs
