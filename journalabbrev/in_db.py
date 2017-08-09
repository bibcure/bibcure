from itertools import groupby
import operator


def manual_update_in(bibs, db_abbrev):
    actions = {
        "y": lambda: update_in(bibs, db_abbrev),
        "n": lambda: bibs,
        "c": lambda: update_in(bibs, db_abbrev, custom=True)
    }
    question = "Replace '{}' for {}? y(yes)/n(no)/c(custom): "
    question = question.format(bibs[0]["journal"], bibs[0]["_text"])
    action = raw_input(question)
    try:
        return actions.get(action)()
    except TypeError:
        return manual_update_in(bibs, db_abbrev)


def update_in(bibs, db_abbrev, custom=False):
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


def update_bibs_in(grouped_bibs, db_abbrev):
    actions = {
        "y": lambda items: map(
            lambda bibs: update_in(bibs, db_abbrev),
            items
        ),
        "m": lambda items: map(
            lambda bibs: manual_update_in(bibs, db_abbrev),
            items
        ),
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
        return update_bibs_in(grouped_bibs, db_abbrev)

    updated_bibs = reduce(lambda a, b: a+b, updated_bibs)
    return updated_bibs
