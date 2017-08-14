
## Features

### Implemented

```
$ bibcure -i input.bib -o output.bib
```
Given a bib file...
* check if all arxivs items are published and automatic update bib(requires
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
* get a bib associated, if arxiv are published in some 
journal return bib associated with this journal (requires internet connection)

### Next Version
```
$ bibcure -i input.bib -o output.bib
```
Given a bibtex file...
* check if all arxivs items are published and automatic update bib(requires
internet connection)
* find and create DOI number associated with each bib item which has not
DOI field(requires
internet connection)
* complete all fields(url, journal, etc) of all bib items using DOI number(requires
internet connection)
* abbreviate jorunals names
* contract authors names
