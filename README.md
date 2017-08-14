
## Features

### Implemented

```
$ bibcure -i input.bib -o output.bib
```
Given a bib file...

* check if all arxivs items are published and automatic update bib
* abbreviate all jorunals names in the gived bibtex file
* find and create DOI number associated with each bib item which has not
DOI field
* complete all fields(url, journal, etc) of all bib items using DOI number

```
$ doitobib 10.1038/s41524-017-0032-0
```
Given a DOI number...

* get a bib(requires
internet connection)

```
$ titletobib An useful paper
```
Given a title

* search papers related and return a bib for the selected paper(requires
internet connection)
```
$ arxivcheck 1601.02785
```
Given a arxiv id...

* get a bib associated, if arxiv are published in some 
journal return bib associated with this journal (requires internet connection)

### Next Features
``````
$ bibcure -i input.bib -o output.bib
```
Given a bib file...

* check if all arxivs items are published and automatic update bib
* find and create DOI number associated with each bib item which has not
DOI field
* complete all fields(url, journal, etc) of all bib items using DOI number
* abbreviate jorunal's names in a given bibtex file
