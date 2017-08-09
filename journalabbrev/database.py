from __future__ import print_function
from builtins import map
from builtins import object
import json
import pkg_resources
import os.path
import bisect
# import pdb

home_path = os.path.expanduser("~")
config_file = home_path+"/.journalabbrev/db.json"
config_file_exists = os.path.exists(config_file)

if config_file_exists:
    db_path = config_file
else:
    db_path = pkg_resources.resource_filename("journalabbrev",
                                              "data/db_abbrev.json")


class Db_abbrev(object):
    def __init__(self):
        self.db_file = db_path
        self.updates_db = []
        self.open()

    def open(self):
        with open(self.db_file) as file_data:
            self.db = json.load(file_data)
            self.db_names = [
                item["name"].lower().replace(" ", "")
                for item in self.db
            ]
            self.db_abbrevs = [
                item["abbrev"].lower().replace(" ", "")
                for item in self.db
            ]

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

    def get_index(self, value, key="name"):
        value = value.lower().replace(" ", "")

        if key == "name":
            index = bisect.bisect(self.db_names, value) - 1
            if self.db_names[index] == value:
                return index
            else:
                return -1

        try:
            index = self.db_abbrevs.index(value)
        except ValueError:
            index = -1

        return index

    def find_closet_index(self, name):
        name = name.lower().replace(" ", "")

        index = bisect.bisect(self.db_names, name)

        return index

    def close(self):
        def action(data):
            what = data["what"]
            data.pop("what", None)

            if what == "insert":
                index = self.find_closet_index(data["name"])
    #avoid duplication
                if self.db_names[index-1] != data["name"]:
                    self.db.insert(index, data)
            else:
                index = self.get_index(data["name"])

                if index != -1:
                    self.db[index]["abbrev"] = data["abbrev"]

        if len(self.updates_db) > 0:

            list(map(action, self.updates_db))

            if not config_file_exists:
                os.makedirs(os.path.dirname(config_file))
                self.db_file = config_file

            with open(self.db_file, "w") as file_data:
                json.dump(self.db, file_data)

            print("Databse was updated")
