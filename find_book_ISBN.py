__author__ = 'Nattefrost'


# manubot cite isbn:978-2-8709-7180-2
#  --format {csljson,cslyaml,plain,markdown,docx,html,jats}
import urllib.request
import json
import re



def get_isbn_ref(isbn):
    """
    :return: Tuple containing the book data extracted from google API JSON
    """
    proper_isbn = isbn.replace("-", "") # regexp to check ISBN13 : ^\d{12}[\d|X]$
    """re.match('[0-9]{10,13}' , nb):"""
    res = urllib.request.urlopen('https://www.googleapis.com/books/v1/volumes?q=isbn:{}'.format(proper_isbn))
    str_res = res.readall().decode('utf-8')
    data = json.loads(str_res)

    try:
        title = data['items'][0]['volumeInfo']['title']
        author = data['items'][0]['volumeInfo']['authors'][0]
    except KeyError:
        title = "Unknown"
        author = "Unknown"
    try:
        publisher = data['items'][0]['volumeInfo']['publisher']
    except KeyError:
        publisher = "Unknown"

    return (title.capitalize(), author.capitalize(), publisher.capitalize())
