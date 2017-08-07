import bibtexparser
import argparse
import pdb
import json
from itertools import groupby
import operator
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
from multiprocessing import Pool


# with open("../scrapper/list_abbrev.json") as file_data:
with open("../scrapper/list_abbrev.json") as file_data:
    list_abbrev = json.load(file_data)


def get_status(bib):
    def is_journal(item):
        return item["name"].lower() == bib["journal"].lower()

    def is_abbrev(item):
        return item["abbrev"].lower() == bib["journal"].lower()
    bib["_text"] = ""
    bib["_type"] = "out_db"
    a_journal = filter(is_journal, list_abbrev)
    a_abbrev = filter(is_abbrev, list_abbrev)
    # pdb.set_trace()
    if len(a_journal) > 0:
        # pdb.set_trace()
        bib["_text"] = a_journal[0]["abbrev"]
        bib["_type"] = "expanded"
    elif len(a_abbrev) > 0:
        # pdb.set_trace()
        bib["_text"] = a_abbrev[0]["name"]
        bib["_type"] = "abreviated"
    return bib


def manual_update(bibs):
    actions = {
        "y": lambda: update_bibs(bibs),
        "n": lambda: bibs,
        "c": lambda: update_bibs(bibs, custom=True)
    }
    question = "Replace '{}' for {}? y(yes)/n(no)/c(custom): "
    question = question.format(bibs[0]["journal"], bibs[0]["_text"])
    action = raw_input(question)
    try:
        return actions.get(action)()
    except TypeError:
        return manual_update(bibs)


# def manual_update_out(bibs):
    # actions = {
        # "y": lambda: update_bibs(bibs, custom=True),
        # "n": lambda: bibs,
    # }
    # question = "Replace '{}' ? y(yes)/n(no): "
    # question = question.format(bibs[0]["journal"])
    # action = raw_input(question)
    # # try:
    # try:
        # return actions.get(action)()
    # except TypeError:
        # return manual_update_out(bibs)


def manual_update_out(bibs):
    is_abreviation = raw_input(
        "'{}' is a abreviation?y(yes)n(no): ".format(bibs[0]["journal"])
    )
    if is_abreviation == "y":
        full_name = raw_input("Insert journal name:\n")
        abreviation = bibs[0]["journal"]
    elif is_abreviation == "n":
        abreviation = raw_input("Insert abreviation:\n")
        full_name = bibs[0]["journal"]
    else:
        return update_bibs_out(bibs)
    list_abbrev.append({"name": full_name, "abbrev": abreviation})
    for i, bib in enumerate(bibs):
        bibs[i]["journal"] = abreviation
    return bibs


def update_bibs_out(grouped_bibs):
    print "\nThe next items does not exist in database."
    action = raw_input("Manually update your database?y(yes)/n(do nothing)")
    if action == "n":
        return grouped_bibs
    elif action == "y":
        grouped_bibs.sort(key=operator.itemgetter('journal'))
        grouped_by_journal = []

        for key, items in groupby(grouped_bibs, lambda i: i["journal"]):
            grouped_by_journal.append(list(items))
            updated_bibs = map(manual_update_out, grouped_by_journal)
            updated_bibs = reduce(lambda a, b: a+b, updated_bibs)
            return updated_bibs
    else:
        return update_bibs_out(grouped_bibs)


def update_bibs(bibs, custom=False):
    if custom:
        journal = raw_input("Insert abreviation:\n")
    else:
        journal = bibs[0]["_text"]

    for i, bib in enumerate(bibs):
        bibs[i]["journal"] = journal
    return bibs


def update_bibs_in(grouped_bibs):
    actions = {
        "y": lambda items: map(lambda bibs: update_bibs(bibs), items),
        "m": lambda items: map(lambda bibs: manual_update(bibs), items),
        "n": lambda items: items
    }
    print "\n "
    action = raw_input("Abbreviate everthing?" +
                       "y(yes, automatic)/m(manual)/n(do nothing)")
    grouped_bibs.sort(key=operator.itemgetter('journal'))
    grouped_by_journal = []
    for key, items in groupby(grouped_bibs, lambda i: i["journal"]):
        grouped_by_journal.append(list(items))

    try:
        updated_bibs = actions.get(action)(grouped_by_journal)
    except TypeError:
        return update_bibs_in(grouped_bibs)

    updated_bibs = reduce(lambda a, b: a+b, updated_bibs)
    return updated_bibs


def main():
    parser = argparse.ArgumentParser(
        prog="jta",
        description="Abreviate the journals name inside a bibtex file.")
    parser.add_argument(
        "--input", "-i",
        required=True,
        type=argparse.FileType("r"),
        help="bibtex input file"
    )
    parser.add_argument(
        "--output", "-o",
        required=True,
        # type=argparse.FileType("w"),
        help="bibtex output file")

    args = parser.parse_args()
    bibtex = bibtexparser.loads(args.input.read())
    bibs_journal, bibs_not_journal = [], []
    for bib in bibtex.entries:
        (bibs_journal
         if "journal" in bib else bibs_not_journal).append(bib)
    bibs_published, bibs_arxiv = [], []
    for bib in bibs_journal:
        (bibs_arxiv
         if "arxiv" in bib["journal"].lower()
         else bibs_published).append(bib)
    # pdb.set_trace()
    pool = Pool()
    bibs_status = pool.map(get_status, bibs_published)
    pool.close()
    pool.join()
    bibs_status.sort(key=operator.itemgetter('_type'))
    grouped_bibs = []
    for key, items in groupby(bibs_status, lambda i: i["_type"]):
        grouped_bibs.append(list(items))

    bibs_in_db, bibs_abreviated, bibs_out_db = [], [], []
    for bib in grouped_bibs:
        if bib[0]["_type"] == "out_db":
            bibs_out_db.append(bib)
        elif bib[0]["_type"] == "abreviated":
            bibs_abreviated.append(bib)
        else:
            bibs_in_db.append(bib)

    # bib_status = map(
    # lambda group: list(group[1]),
    # groupby(
    # map(get_status, bibs_journal),
    # operator.itemgetter("_type"))
    # )
    print "%d bibs are arxiv" % len(bibs_arxiv)
    print "%d bibs don't have journal tag " % len(bibs_not_journal)
    print "%d bibs are already abbreviated  " % len(bibs_abreviated[0])
    print "%d bibs can be easily abbreviated " % len(bibs_in_db[0])
    print "%d bibs must be manualy abbreviated, "% len(bibs_out_db[0]) + \
        "at least this time "
    # pdb.set_trace()
    updated_bibs = reduce(
        lambda a, b: a + b,  map(update_bibs_in, bibs_in_db)
    )
    updated_bibs += reduce(
        lambda a, b: a + b, map(update_bibs_out, bibs_out_db)
    )
    updated_bibs += bibs_abreviated[0]

    # bibs = bibs_in_db
    # bibs = bibs_out_db + bibs_expanded
    # pdb.set_trace()
    [
        [
            bib.pop(t, None) for bib in updated_bibs
        ]
        for t in ["_text", "_type"]
    ]
    updated_bibs += bibs_arxiv + bibs_not_journal
    # bibtex.entries = bibs

    writer = BibTexWriter()
    new_bibtex = BibDatabase()
    new_bibtex.entries = updated_bibs
    # pdb.set_trace()
    with open(args.output, 'w') as bibfile:
        bibfile.write(writer.write(new_bibtex).encode("utf8"))
    # bibtexparser.dump(bibtex, args.output.read())
    # pdb.set_trace()
    # return bibs


if __name__ == "__main__":
    main()
