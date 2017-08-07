import bibtexparser
import argparse
import pdb
import json
from itertools import groupby
import operator
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
from multiprocessing import Pool


class Db_abbrev():
    def __init__(self, db_file="../scrapper/list_abbrev.json"):
        self.db_file = db_file
        self.updates_db = []
        self.open()

    def open(self):
        with open(self.db_file) as file_data:
            self.db = json.load(file_data)

    def insert(self, name, abbrev):
        return self.updates_db.append({
            "name": name,
            "abbrev": abbrev,
            "what": "insert"
        })

    def update(self, name, abbrev):
        return self.updates_db.append({
            "name": name,
            "abbrev": abbrev,
            "what": "update"
        })

    def get_indexes(self, value, key="name"):
        def get_items_by_name(item):
            return item.get(key) == value

        indexes = self.db.index(
            filter(get_items_by_name, self.db)[0]
        )
        return indexes

    def close(self):
        def action(data):
            what = data["what"]
            data.pop("what", None)
            if what == "insert":
                self.db.append(data)
            else:
                index = self.get_indexes(data["name"])
                self.db[index]["abbrev"] = data["abbrev"]
        if len(self.updates_db) > 0:
            map(action, self.updates_db)
            with open(self.db_file, "w") as file_data:
                json.dump(self.db, file_data)


db_abbrev = Db_abbrev()


def get_status(bib):
    def is_journal(item):
        return item["name"].lower() == bib["journal"].lower()

    def is_abbrev(item):
        return item["abbrev"].lower() == bib["journal"].lower()
    bib["_text"] = ""
    bib["_type"] = "out_db"
    a_journal = filter(is_journal, db_abbrev.db)
    a_abbrev = filter(is_abbrev, db_abbrev.db)
    if len(a_journal) > 0:
        bib["_text"] = a_journal[0]["abbrev"]
        bib["_type"] = "expanded"
    elif len(a_abbrev) > 0:
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
        return manual_update_out(bibs)
    db_abbrev.insert(full_name, abreviation)
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
        abbrev = raw_input("Insert abreviation:\n")
        db_abbrev.update(
            bibs[0]["journal"],
            abbrev
        )
    else:
        abbrev = bibs[0]["_text"]

    for i, bib in enumerate(bibs):
        bibs[i]["journal"] = abbrev

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

    if len(bibs_arxiv) > 0:
        print "%d bibs are arxiv" % len(bibs_arxiv)
        updated_bibs = bibs_arxiv

    if len(bibs_not_journal) > 0:
        print "%d bibs don't have journal tag " % len(bibs_not_journal)

        updated_bibs += bibs_not_journal

    if len(bibs_abreviated) > 0:
        print "%d bibs are already abbreviated  " % len(bibs_abreviated[0])
        updated_bibs += bibs_abreviated[0]

    if len(bibs_in_db) > 0:
        print "%d bibs can be easily abbreviated " % len(bibs_in_db[0])
        updated_bibs = reduce(
            lambda a, b: a + b,  map(update_bibs_in, bibs_in_db)
        )

    if len(bibs_out_db) > 0:
        print "%d bibs must be manualy abbreviated, " % len(bibs_out_db[0]) + \
            "at least this time "
        updated_bibs += reduce(
            lambda a, b: a + b, map(update_bibs_out, bibs_out_db)
        )

    for bib in updated_bibs:
        if set(("_text", "_type")).issubset(bib) in bib:
            bib.pop("_text", None)
            bib.pop("_type", None)

    writer = BibTexWriter()
    new_bibtex = BibDatabase()
    new_bibtex.entries = updated_bibs
    with open(args.output, 'w') as bibfile:
        bibfile.write(writer.write(new_bibtex).encode("utf8"))
    db_abbrev.close()


if __name__ == "__main__":
    main()
