__author__ = 'Nattefrost'
import sqlite3 as lite

def get_all_books():
    con = None
    path = './books.db'
    con = lite.connect(path)
    cur = con.cursor()
    sql = 'SELECT * from books'
    cur.execute(sql)
    all_books = cur.fetchall()
    con.commit()
    con.close()
    return all_books

def get_books_to_view():
    con = None
    path = './books.db'
    con = lite.connect(path)
    cur = con.cursor()
    sql = 'SELECT title, author, collection,read from books'
    cur.execute(sql)
    all_books = cur.fetchall()
    con.commit()
    con.close()
    return all_books

def add_book(title,author,collection,isbn,read):
    con = None
    path = './books.db'
    con = lite.connect(path)
    cur = con.cursor()
    cur.execute('INSERT INTO books(title, author, collection, ISBN, read) VALUES(?,?,?,?,?)', (title,author,collection,isbn,read,) )
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
    print("LOL")
    book_id = book[0][0]
    print(book_id)
    con = None
    path = './books.db'
    con = lite.connect(path)
    cur = con.cursor()
    cur.execute("DELETE FROM books WHERE id='{}'".format(book_id))
    con.commit()
    con.close()
