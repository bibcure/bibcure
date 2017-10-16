# bibcure (Beta Version)

![logo_64x64](https://raw.githubusercontent.com/bibcure/logo/master/logo_64x64.png)
Bibcure helps in boring tasks by keeping your [bibtex](http://www.bibtex.org/) file up to date and normalized.

![bibcure_op](https://raw.githubusercontent.com/bibcure/logo/master/gifs/bibcure_op.gif)

# Requirements/Install

Bibcure uses the wonderful [Bibtex parser](https://github.com/sciunto-org/python-bibtexparser).
In this moment we waiting for new release of [`python-bibtexparser`](https://github.com/sciunto-org/python-bibtexparser) to solve some bugs.

Install it using [`pip`](https://pip.pypa.io/):

```bash
$ sudo python /usr/bin/pip install bibcure
# or
$ sudo pip install bibcure
# or
$ sudo pip3 install bibcure  # for Python 3
```

You can also install from the source: git clone the repository, and install with the [`setup.py`](setup.py) script.

## `scihub2pdf` (beta)

![sci_hub_64](https://raw.githubusercontent.com/bibcure/logo/master/sci_hub_64.png)
If you want download articles via a DOI number, article title or a bibtex file, using the
database of arXiv, libgen or sci-hub, see [bibcure/scihub2pdf](https://github.com/bibcure/scihub2pdf).

----

# Features and how to use

## `bibcure`

Given a bib file...

```bash
$ bibcure -i input.bib -o output.bib
```

* check sure the arXiv items have been published, then update them (requires internet connection),

* complete all fields(url, journal, etc) of all bib items using DOI number (requires internet connection),

* find and create DOI number associated with each bib item which has not DOI field (requires internet connection),

* abbreviate journals names.


## `arxivcheck`

Given an arXiv id...

```bash
$ arxivcheck 1601.02785
```

* check if has been published, and then returns the updated bib (requires internet connection).

Given a title...

```bash
$ arxivcheck --title "A useful paper with hopefully unique title published on arxiv"
```

* search papers related and return a bibtex file for the first item.

You can easily append a bib into a bibfile, just do

```bash
$ arxivcheck --title "A useful paper with hopefully unique title published on arxiv" >> file.bib
```

You also can interact with results, just pass `--ask` parameter:

```bash
$ arxivcheck --ask --title "A useful paper with hopefully unique title published on arxiv"
```


## `scihub2pdf`

Given a bibtex file

```bash
$ scihub2pdf -i input.bib
```

Given a DOI number...

```bash
$ scihub2pdf 10.1038/s41524-017-0032-0
```

Given an arXiv id...

```bash
$ scihub2pdf arxiv:1708.06891
```

Given a title...

```bash
$ scihub2bib --title "A useful paper with hopefully unique title"
```

or arxiv...

```bash
$ scihub2bib --title arxiv:"A useful paper with hopefully unique title"
```

Location folder as argument:

```bash
$ scihub2pdf -i input.bib -l somefolder/
```

Use libgen instead sci-hub:

```bash
$ scihub2pdf --uselibgen -i input.bib
```


## `doi2bib`

Given a DOI number...

```bash
$ doi2bib 10.1038/s41524-017-0032-0
```

* get bib item given a DOI (requires internet connection)

You can easily append a bib into a bibfile, just do:

```bash
$ doi2bib 10.1038/s41524-017-0032-0 >> file.bib
```

You also can generate a bibtex from a txt file containing a list of DOIs:

```bash
$ doi2bib --input file_with_dois.txt --output refs.bib
```

## `title2bib`

Given a title...

```bash
$ title2bib "A useful paper with hopefully unique title"
```

* search papers related and return a bib for the selected paper (requires internet connection)

You can easily append a bib into a bibfile, just do

```bash
$ title2bib "A useful paper with hopefully unique title" --first >> file.bib
```

You also can generate a bibtex from a txt file containing a list of "titles"

```bash
$ title2bib --input file_with_titles.txt --output refs.bib --first
```

----

## Comparison: Sci-Hub vs LibGen

### Sci-Hub
- Stable
- Annoying CAPTCHA
- Fast

### Libgen
- Unstable
- No CAPTCHA
- Slow

----

## License
*GNU Affero General Public License v3.0.*
For more details, see [the `LICENSE` file](LICENSE).
