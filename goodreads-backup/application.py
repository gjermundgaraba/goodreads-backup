from urllib.request import urlopen
from xml.dom.minidom import parse
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

user = config['CONFIG']['user']
key = config['CONFIG']['key']

xml = urlopen("https://www.goodreads.com/review/list/" + user + ".xml?v=2&key=" + key)
dom = parse(xml)

reviews = dom.getElementsByTagName("review")

for review in reviews:
    book = review.getElementsByTagName("book")[0]
    title = book.getElementsByTagName("title")[0]
    id = book.getElementsByTagName("id")[0]
    isbn = book.getElementsByTagName("isbn")[0]
    isbn13 = book.getElementsByTagName("isbn13")[0]

    print(title.firstChild.data)
    print(id.firstChild.data)
    if isbn.getAttribute("nil") != "true":
        print(isbn.firstChild.data)
    if isbn.getAttribute("nil") != "true":
        print(isbn13.firstChild.data)
    print("")

print("")