from urllib.request import urlopen
from xml.dom.minidom import parse
import configparser
import csv

config = configparser.ConfigParser()
config.read('config.ini')

user = config['CONFIG']['user']
key = config['CONFIG']['key']

xml = urlopen("https://www.goodreads.com/review/list/" + user + ".xml?v=2&key=" + key)
dom = parse(xml)

reviews = dom.getElementsByTagName("review")

books = []

for review in reviews:
    book = review.getElementsByTagName("book")[0]
    title = book.getElementsByTagName("title")[0]
    id = book.getElementsByTagName("id")[0]
    isbn = book.getElementsByTagName("isbn")[0]
    isbn13 = book.getElementsByTagName("isbn13")[0]

    book = {
        'title': title.firstChild.data,
        'id': id.firstChild.data
    }

    if isbn.getAttribute("nil") != "true":
        book['isbn'] = isbn.firstChild.data
    if isbn.getAttribute("nil") != "true":
        book['isbn13'] = isbn13.firstChild.data

    books.append(book)

with open('books.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',')

    for book in books:
        spamwriter.writerow([book['title'], book['id'], book['isbn'], book['isbn13']])