def get_status(bib, db_abbrev):
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
