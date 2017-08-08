from setuptools import setup, find_packages
from os.path import expanduser

home = expanduser("~")

setup(
	name = "Journal Abbreviation",
	version = "0.1",
	scripts = ["bin/journalabbrev"],
	install_requires = ["bibtexparser"],
	data_files = [
		(home+"/.journalabbreviation/", ["static/db_abbrev.json"])
	],
	author = "Bruno Messias",
	author_email = "contato@brunomessias.com",
	url = "http://brunomessias.com"
)
