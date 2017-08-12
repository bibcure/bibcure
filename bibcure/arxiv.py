from __future__ import print_function
from builtins import input
from arxivcheck.arxiv import check_arxiv_published
import bibtexparser
from itertools import groupby
import operator
from functools import reduce


def update_arxivs(bibs, automatic=True):
    arxiv_id = bibs[0]["journal"].partition(":")[2]
    arxiv_title = bibs[0]["title"]

    found, published, bib_string = check_arxiv_published(arxiv_id,
                                                         abbrev_journal=False)
    bib = bibtexparser.loads(bib_string)

    if found:
        for i in range(len(bibs)):
            if automatic:
                bibs[i] = bib.entries[0]
            else:
                question = "{} >> {} ".format(arxiv_title,
                                              bib.entries[0]["title"])

                question += " was "
                if not published:
                    question += " not published. Use bib from arxiv?y/n"
                else:
                    question += " published in "
                    question += "{}.".format(bib.entries[0]["journal"])
                    question += " Replace with new bib ?y/n"
                replace = input(question)
                if replace == "y":
                    bibs[i] = bib.entries[0]

    elif not found:
        print("'{}' not founded with a id {}".format(
            arxiv_title,
            arxiv_id
        ))

    return bibs


def update_bibs_arxiv(grouped_bibs):
    actions = {
        "a": lambda items: [update_arxivs(bibs, True) for bibs in items],
        "m": lambda items: [update_arxivs(bibs, False) for bibs in items],
        "n": lambda items: items
    }

    action = input("Check if arxiv items are published?a(automatic)/m(manual)/n(do nothing)")
    grouped_bibs.sort(key=operator.itemgetter('journal'))
    grouped_by_journal = []
    for key, items in groupby(grouped_bibs, lambda i: i["journal"]):
        grouped_by_journal.append(list(items))

    if action in ("a", "m", "n"):
        updated_bibs = actions.get(action)(grouped_by_journal)

    else:
        return update_bibs_arxiv(grouped_bibs)

    updated_bibs = reduce(lambda a, b: a+b, updated_bibs)
    return updated_bibs
