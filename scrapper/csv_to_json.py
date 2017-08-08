import csv
import json

csvfile = open('data_healed.csv', 'r')
jsonfile = open('data_healed.json', 'w')

fieldnames = ("name", "abbrev")
reader = csv.DictReader( csvfile, fieldnames)
for row in reader:
    json.dump(row, jsonfile)
    jsonfile.write('\n')


