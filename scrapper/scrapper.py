from lxml import etree
import urllib2
import json


header = 'Mozilla/5.0 (X11; Linux x86_64) '
header += 'AppleWebKit/537.36 (KHTML, like Gecko)'
header += 'Chrome/59.0.3071.109 Safari/537.36'
chars = [chr(c) for c in range(ord("a"), ord("z")+1)]
parser = etree.HTMLParser()
list_of_words_not_abbvr = ["AND", "OF", "ACM", "IN", "NEW"]
[list_of_words_not_abbvr.append(c.capitalize()) for c in chars]


def get_url(initial):
    main_url = "http://www.personal.leeds.ac.uk/~menmwi/ISIabbr/%_abrvjt.html"
    return main_url.replace("%", initial.capitalize())


def get_urls():
    urls = list(map(get_url, chars))
    return urls


def get_html_tree(url):
    request = urllib2.Request(url)
    request.add_header('User-Agent', header)
    response = urllib2.urlopen(request)
    page = response.read()
    response.close()
    html_tree = etree.fromstring(page, parser)
    return html_tree


def humanize_abbvr(abbvr):
    removed_escape_chars = abbvr.replace("\t", "").replace("\n", "")
    capitalized_abbvr = removed_escape_chars.title().split(" ")
    capitalized_abbvr = list(map(
        lambda item: item if item in list_of_words_not_abbvr else item+".",
    capitalized_abbvr))
    return " ".join(capitalized_abbvr)


def get_itens(url):
    tree = get_html_tree(url)
    result = [
        {
            "name": name.text,
            "abbvr": abbvr.text
        }
        for name, abbvr in zip(tree.xpath("//dl//dt"), tree.xpath("//dl//dd"))
    ]
    result = list(filter(lambda item: item["abbvr"] is not None, result))
    result = [
        {
            "name": item["name"].replace("\t", "").replace("\n", ""),
            "abbvr": humanize_abbvr(item["abbvr"])
        }
        for item in result
    ]
    return result


def main():
    urls = get_urls()
    result = list(map(get_itens, urls))
    result = list(reduce(lambda a, b: a+b, result))
    with open('list_of_journal_abbrv.json', 'w') as fp:
        json.dump(result, fp)


if __name__ == "__main__":
    main()
