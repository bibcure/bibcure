from setuptools import setup

setup(
    name="Journal Abbreviation",
    version="0.1",
    packages=["journalabbrev"],
    scripts=["bin/journalabbrev"],
    install_requires=["bibtexparser"],
    data_files=[
        ("/opt/journalabbreviation/", ["static/db_abbrev.json"])
    ],
    description="Abbreviates journal names inside in a given bibtex file",
    author="Bruno Messias",
    author_email="contato@brunomessias.com",
    url="https://github.com/devmessias/journalabbrev"
)
