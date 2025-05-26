__author__ = 'Nattefrost'
# DB creation script


import os.path
import sqlite3 as lite


def check_db_exists():
    if os.path.isfile("./books.db"):
        print('DB exists')
    else:
        print("DB doesnt exist")
        print("CREATING DATABASE ./books.db")
        create_db()

def create_db():
    con = None
    path = "./books.db"
    con = lite.connect(path)
    c = con.cursor()
    c.execute("CREATE TABLE Authors(id INTEGER PRIMARY KEY AUTOINCREMENT, author TEXT NOT NULL UNIQUE)")
    c.execute("CREATE TABLE Editors(id INTEGER PRIMARY KEY AUTOINCREMENT, editor TEXT NOT NULL UNIQUE)")
    c.execute("CREATE TABLE Books(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, read INT NOT NULL, "
              "author_id INT NOT NULL, editor_id INT NOT NULL, "
              "FOREIGN KEY(author_id) REFERENCES Authors(id),"
              "FOREIGN KEY(editor_id) REFERENCES Editors(id) )")
    c.execute("CREATE TABLE ISBN(id INTEGER PRIMARY KEY AUTOINCREMENT, isbn INTEGER UNIQUE)")
    c.execute("INSERT INTO Editors VALUES('0', 'Unknown') ")
    con.commit()
    con.close()

check_db_exists()
