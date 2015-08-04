__author__ = 'Nattefrost'

# Accessing the db and fetching data.
# Nattefrost
# Summer 2015

import time
import sqlite3 as lite



def get_books_to_view():
    con = None
    path = './books.db'
    con = lite.connect(path)
    cur = con.cursor()
    sql = """SELECT title, author, editor, read
             FROM Books B
             JOIN Authors A
             ON B.author_id = A.id
             JOIN Editors E
             ON B.editor_id = E.id; """
    cur.execute(sql)
    all_books = cur.fetchall()
    con.commit()
    con.close()
    return all_books

def add_book(title, author, editor, read):
    con = None
    id_ed = editor_exists(editor)
    id_au = author_exists(author)
    # CHECKING IF EDITOR AND AUTHOR DONT ALREADY EXIST IN DB
    if id_ed:
        editor = id_ed[0][0]
    else:
        insert_editor(editor)

    if id_au:
        author = id_au[0][0]
    else:
        insert_author(author)

    path = './books.db'
    con = lite.connect(path)
    cur = con.cursor()
    cur.execute('INSERT INTO books(title, editor_id, author_id, read) VALUES(?,?,?,?)', (title, editor, author, read) )
    con.commit()
    con.close()


def insert_author(author):
    con = None
    path = './books.db'
    con = lite.connect(path)
    cur = con.cursor()
    sql = "INSERT INTO Authors(author) VALUES(?)"
    cur.execute(sql, (author,) )
    con.commit()
    con.close()
    # RETURN ID JUST ENTERED SO IT DOESNT ENTER STRING INSTEAD OF ID, see LINE 34-42

def insert_editor(editor):
    con = None
    path = './books.db'
    con = lite.connect(path)
    cur = con.cursor()
    cur.execute("INSERT INTO Editors(editor) VALUES(?)",  (editor,) )
    con.commit()
    con.close()
    # RETURN ID JUST ENTERED

def author_exists(author):
    con = None
    path = './books.db'
    con = lite.connect(path)
    cur = con.cursor()
    sql = 'SELECT id FROM Authors WHERE author = "{}"'.format(author)
    cur.execute(sql)
    res = cur.fetchall()
    con.close()
    return res

def editor_exists(editor):
    con = None
    path = './books.db'
    con = lite.connect(path)
    cur = con.cursor()
    sql = 'SELECT id FROM Editors WHERE editor = "{}";'.format(editor)

    cur.execute(sql)
    res = cur.fetchall()
    con.close()
    return res


def mark_read(book):
    con = None
    path = './books.db'
    con = lite.connect(path)
    cur = con.cursor()
    sql = 'UPDATE books SET read = 1 WHERE title = "{}";'.format(book)
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
    cur.execute("DELETE FROM books WHERE id='{}';".format(book_id))
    con.commit()
    con.close()
