## Description


![](https://raw.githubusercontent.com/bibcure/logo/master/logo_64x64.png) Bibcure helps in boring tasks by keeping your bibfile up to date and normalized.
## Install

```
$ sudo pip install bibcure
```
## Features and how to use

```
$ bibcure -i input.bib -o output.bib
```
Given a bib file...
* check sure the Arxiv items have been published, then update them(requires
internet connection)
* complete all fields(url, journal, etc) of all bib items using DOI number(requires
internet connection)
* find and create DOI number associated with each bib item which has not
DOI field(requires
internet connection)
* abbreviate jorunals names
```
$ doitobib 10.1038/s41524-017-0032-0
```
Given a DOI number...
* get bib item given a doi(requires
internet connection)

```
$ titletobib An useful paper
```
Given a title...
* search papers related and return a bib for the selected paper(requires
internet connection)
```
$ arxivcheck 1601.02785
```
Given a arxiv id...
* given an arixiv id, check if has been published, and then returns the updated bib (requires internet connection)

### Next Version
```
$ bibcure -i input.bib -o output.bib
```
* contract authors names
