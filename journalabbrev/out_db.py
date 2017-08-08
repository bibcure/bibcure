from itertools import groupby
import operator


def update_out(bibs, db_abbrev):
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
        return update_out(bibs)
    db_abbrev.insert(full_name, abreviation)
    for i, bib in enumerate(bibs):
        bibs[i]["journal"] = abreviation
    return bibs


def update_bibs_out(grouped_bibs, db_abbrev):
    print "\nThe next items does not exist in database."
    action = raw_input("Manually update your database?y(yes)/n(do nothing)")
    if action == "n":
        return grouped_bibs
    elif action == "y":
        grouped_bibs.sort(key=operator.itemgetter('journal'))
        grouped_by_journal = []

        for key, items in groupby(grouped_bibs, lambda i: i["journal"]):
            grouped_by_journal.append(list(items))
            updated_bibs = map(
                lambda bibs: update_out(bibs, db_abbrev),
                grouped_by_journal
            )
        updated_bibs = reduce(lambda a, b: a+b, updated_bibs)
        return updated_bibs
    else:
        return update_bibs_out(grouped_bibs)
