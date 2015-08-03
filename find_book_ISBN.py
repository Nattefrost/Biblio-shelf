__author__ = 'Nattefrost'

import urllib.request
import json

#https://www.googleapis.com/books/v1/volumes?q=isbn:2020291606

def get_isbn_ref(isbn=None):
    """
    :return: Tuple containing the book data extracted from google API JSON
    """
    res = urllib.request.urlopen('https://www.googleapis.com/books/v1/volumes?q=isbn:2277212202')
    str_res = res.readall().decode('utf-8')
    data = json.loads(str_res)
    title = data['items'][0]['volumeInfo']['title']
    author = data['items'][0]['volumeInfo']['authors'][0]
    try:
        publisher = data['items'][0]['volumeInfo']['publisher']
    except KeyError:
        publisher = "Unknown"
    return (title, author, publisher)

get_isbn_ref() # remove once data is processed