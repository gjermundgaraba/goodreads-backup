from urllib.request import urlopen
from xml.dom.minidom import parse
import configparser
import csv
import math


def main():
    config = configparser.ConfigParser()
    config.read('config.ini')

    per_page = 20  # 1-200
    user = config['CONFIG']['user']
    key = config['CONFIG']['key']
    header = config['CONFIG']['header'].lower() in ('yes', 'true', '1')

    current_page = 1
    xml = urlopen(get_url(user, key, per_page, current_page))
    dom = parse(xml)

    total_reviews = int(dom.getElementsByTagName('reviews')[0].getAttribute('total'))
    number_of_pages = math.ceil(total_reviews / per_page)

    books = []

    while current_page <= number_of_pages:
        extract_books(books, dom)

        current_page += 1
        xml = urlopen(get_url(user, key, per_page, current_page))
        dom = parse(xml)

    shelves = extract_shelves(books)

    write_shelves_to_disk(shelves, header)


def extract_books(books, dom):
    reviews = dom.getElementsByTagName('review')
    for review in reviews:
        book_element = review.getElementsByTagName('book')[0]
        title_element = book_element.getElementsByTagName('title')[0]
        id_element = book_element.getElementsByTagName('id')[0]
        isbn_element = book_element.getElementsByTagName('isbn')[0]
        isbn13_element = book_element.getElementsByTagName('isbn13')[0]
        started_at = review.getElementsByTagName('started_at')[0]
        read_at = review.getElementsByTagName('read_at')[0]

        shelves_element = review.getElementsByTagName('shelves')[0]
        book_shelves = []
        for shelf in shelves_element.getElementsByTagName('shelf'):
            book_shelves.append(shelf.getAttribute('name'))

        book = {
            'title': title_element.firstChild.data,
            'id': id_element.firstChild.data,
            'shelves': book_shelves
        }

        if isbn_element.getAttribute('nil') != 'true':
            book['isbn'] = isbn_element.firstChild.data
        else:
            book['isbn'] = ''

        if isbn13_element.getAttribute('nil') != 'true':
            book['isbn13'] = isbn13_element.firstChild.data
        else:
            book['isbn13'] = ''

        if started_at.firstChild is not None:
            book['started_at'] = started_at.firstChild.data
        else:
            book['started_at'] = ''

        if read_at.firstChild is not None:
            book['read_at'] = read_at.firstChild.data
        else:
            book['read_at'] = ''

        books.append(book)


def extract_shelves(books):
    shelves = {}
    for book in books:
        for shelf in book['shelves']:
            if shelf not in shelves:
                shelves[shelf] = []
            shelves[shelf].append(book)
    return shelves


def write_shelves_to_disk(shelves, header):
    for shelf_name, shelf in shelves.items():
        with open(shelf_name + '.csv', 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')

            if header:
                csv_writer.writerow(['Goodreads Id', 'Title', 'ISBN', 'ISBN13', 'Started At', 'Read At'])

            for book in shelf:
                book_title = book['title']
                book_id = book['id']
                isbn = book['isbn']
                isbn13 = book['isbn13']
                started_at = book['started_at']
                read_at = book['read_at']

                csv_writer.writerow([book_id, book_title, isbn, isbn13, started_at, read_at])


def get_url(user, key, per_page, page):
    return 'https://www.goodreads.com/review/list/' + user + '.xml?v=2&key=' + key + '&per_page=' + str(
        per_page) + '&page=' + str(page)


if __name__ == '__main__':
    main()
