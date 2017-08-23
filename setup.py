from setuptools import setup, find_packages

readme = open('README','r')
README_TEXT = readme.read()
readme.close()

setup(
    name="bibcure",
    version="0.2.6",
    packages = find_packages(exclude=["build",]),
    scripts=["bibcure/bin/bibcure"],
    long_description = README_TEXT,
    install_requires = ["bibtexparser", "future",
                      "doi2bib", "title2bib", "arxivcheck"],
    include_package_data=True,
    package_data={
        "data":["data/db_abbrev.json"]
    },
    license="AGPLv3",
    description=" Helps you to have a better bibtex file",
    author="Bruno Messias",
    author_email="messias.physics@gmail.com",
    download_url="https://github.com/bibcure/bibcure/archive/0.2.6.tar.gz",
    keywords=["bibtex", "arxiv", "doi", "abbreviate", "science","scientific-journals"],

    classifiers=[
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python",
        "Topic :: Text Processing :: Markup :: LaTeX",
    ],
    url="https://github.com/bibcure/bibcure"
)
