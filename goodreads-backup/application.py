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
    book_element = review.getElementsByTagName("book")[0]
    title = book_element.getElementsByTagName("title")[0]
    id = book_element.getElementsByTagName("id")[0]
    isbn = book_element.getElementsByTagName("isbn")[0]
    isbn13 = book_element.getElementsByTagName("isbn13")[0]

    shelves_element = review.getElementsByTagName("shelves")[0]
    book_shelves = []
    for shelf in shelves_element.getElementsByTagName("shelf"):
        book_shelves.append(shelf.getAttribute("name"))

    book = {
        'title': title.firstChild.data,
        'id': id.firstChild.data,
        'shelves': book_shelves
    }

    if isbn.getAttribute("nil") != "true":
        book['isbn'] = isbn.firstChild.data
    if isbn.getAttribute("nil") != "true":
        book['isbn13'] = isbn13.firstChild.data

    books.append(book)

shelves = {}

for book in books:
    for shelf in book['shelves']:
        if shelf not in shelves:
            shelves[shelf] = []
        shelves[shelf].append(book)

for shelf_name, shelf in shelves.items():
    with open(shelf_name + '.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')

        for book in shelf:
            title = book['title']
            id = book['id']

            spamwriter.writerow([id, title])


