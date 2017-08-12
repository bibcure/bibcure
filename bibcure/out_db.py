from __future__ import print_function
from builtins import input
from itertools import groupby
import operator
from functools import reduce


def update_out(bibs, db_abbrev):
    is_abreviation = input(
        "'{}' is a abreviation?y(yes)n(no): ".format(bibs[0]["journal"])
    )
    if is_abreviation == "y":
        full_name = input("Insert journal name:\n")
        abreviation = bibs[0]["journal"]
    elif is_abreviation == "n":
        abreviation = input("Insert abreviation:\n")
        full_name = bibs[0]["journal"]
    else:
        return update_out(bibs, db_abbrev)
    db_abbrev.insert(full_name, abreviation)
    for i, bib in enumerate(bibs):
        bibs[i]["journal"] = abreviation
    return bibs


def update_bibs_out(grouped_bibs, db_abbrev):
    print("\nThe next items does not exist in database.")
    action = input("Manually update your database?y(yes)/n(do nothing)")
    if action == "n":
        return grouped_bibs
    elif action != "y":
        return update_bibs_out(grouped_bibs, db_abbrev)

    grouped_bibs.sort(key=operator.itemgetter('journal'))
    updated_bibs = []
    for key, items in groupby(grouped_bibs, lambda i: i["journal"]):
        updated_bibs.append(update_out(list(items), db_abbrev))

    updated_bibs = reduce(lambda a, b: a+b, updated_bibs)
    return updated_bibs
