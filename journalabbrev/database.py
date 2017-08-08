import json


class Db_abbrev():
    def __init__(self, db_file="/opt/journalabbreviation/db_abbrev.json"):
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
            print "Databse was updated"
