## Description


![](https://raw.githubusercontent.com/bibcure/logo/master/logo_64x64.png) Bibcure helps in boring tasks by keeping your bibfile up to date and normalized.

###  Requirements

Bibcure uses the wonderful [Bibtex parser](https://github.com/sciunto-org/python-bibtexparser). In this moment we waiting for new release of bibtexparser to solve some bugs.
## Install

```
$ sudo pip install bibcure
```
## Features and how to use

#### bibcure
Given a bib file...
```
$ bibcure -i input.bib -o output.bib
```
* check sure the Arxiv items have been published, then update them(requires
internet connection)
* complete all fields(url, journal, etc) of all bib items using DOI number(requires
internet connection)
* find and create DOI number associated with each bib item which has not
DOI field(requires
internet connection)
* abbreviate jorunals names

#### doitobib
Given a DOI number...
```
$ doitobib 10.1038/s41524-017-0032-0
```
* get bib item given a doi(requires
internet connection)

You can easily append
a bib into a bibfile, just do
```
$ doitobib 10.1038/s41524-017-0032-0 >> file.bib
```
#### titletobib
Given a title...
```
$ titletobib An useful paper
```
* search papers related and return a bib for the selected paper(requires
internet connection)

You can easily append
a bib into a bibfile, just do
```
$ titletobib An useful paper --first >> file.bib
```
#### arxivcheck


Given a arxiv id...
```
$ arxivcheck 1601.02785
```
* check if has been published, and then returns the updated bib (requires internet connection)


Given a title...
```
$ arxivcheck --title An useful paper published on arxiv
```
search papers related and return a bib the first item. 
You can easily append a bib into a bibfile, just do
```
$ arxivcheck --title An useful paper published on arxiv >> file.bib
```
You also can interact with results, just pass --ask parameter
```
$ arxivcheck --ask --title An useful paper published on arxiv 
```
### Next Version
```
$ bibcure -i input.bib -o output.bib
```
* contract authors names

