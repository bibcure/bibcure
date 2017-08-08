from setuptools import setup


files = ["journal_files/*"]
readme = open('README.md','r')
README_TEXT = readme.read()
readme.close()

setup(
    name="journalabbrev",
    version="0.1.1",
    packages=["journalabbrev"],
    scripts=["bin/journalabbrev"],
    long_description = README_TEXT,
    install_requires=["bibtexparser"],
    data_files=[
        ("/opt/journalabbreviation/", ["static/db_abbrev.json"])
    ],
    licencse="GPL-3.0",
    description="Abbreviates journal names inside in a given bibtex file",
    author="Bruno Messias",
    author_email="contato@brunomessias.com",
    download_url="https://github.com/devmessias/journalabbrev/archive/0.1.1.tar.gz",
    keywords=["bibtex", "abbreviate", "science","scientific-journals"],
    classifiers=[
        'Intended Audience :: Science/Research',
        'Programming Language :: Python',
        'Topic :: Text Processing :: Markup :: LaTeX',
    ],
    url="https://github.com/devmessias/journalabbrev"
)
