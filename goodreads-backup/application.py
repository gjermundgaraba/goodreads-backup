from urllib.request import urlopen
from xml.dom.minidom import parse
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

user = config['CONFIG']['user']
key = config['CONFIG']['key']

test = urlopen("https://www.goodreads.com/review/list/" + user + ".xml?v=2&key=" + key)
dom = parse(test)

print(dom.toprettyxml())