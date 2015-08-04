__author__ = 'Nattefrost'

# Accessing the db and fetching data.
# Nattefrost
# Summer 2015


import sqlite3 as lite



def get_books_to_view():
    con = None
    path = './books.db'
    con = lite.connect(path)
    cur = con.cursor()
    sql = 'SELECT title, read, author_id, editor_id from books'
    cur.execute(sql)
    all_books = cur.fetchall()
    con.commit()
    con.close()
    return all_books

def add_book(title, author, publisher, read):
    con = None
    path = './books.db'
    con = lite.connect(path)
    cur = con.cursor()
    cur.execute('INSERT INTO books(title, read, author_id, editor_id) VALUES(?,?,?,?)', (title, read, publisher, author,) )
    con.commit()
    con.close()

def mark_read(book):
    con = None
    path = './books.db'
    con = lite.connect(path)
    cur = con.cursor()
    sql = 'UPDATE books SET read = 1 WHERE title = "{}"'.format(book)
    cur.execute(sql)
    con.commit()
    con.close()

def remove_book(book):
    book_id = book[0][0]
    print(book_id)
    con = None
    path = './books.db'
    con = lite.connect(path)
    cur = con.cursor()
    cur.execute("DELETE FROM books WHERE id='{}'".format(book_id))
    con.commit()
    con.close()
