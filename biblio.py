__author__ = 'Nattefrost'
# Listing all books i own using a tkinter interface

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import os
import ctypes
import db_access as db

class biblio:
    def __init__(self):
        self.root = tk.Tk()
        self.style = ttk.Style()
        self.booksList = []
        #self.root.windowIcon = tk.PhotoImage("photo", file="./book_icon.gif") # setting icon
        #self.root.tk.call('wm','iconphoto',self.root._w,self.root.windowIcon)
        self.root.geometry('{}x{}'.format(1042,670))
        self.root['bg'] = 'slategrey'
        self.style.theme_use('clam')
        self.root.title("Bibliotheque")
        self.tabControl = ttk.Notebook(self.root)
        self.books_view = tk.Frame(self.tabControl)
        self.inserting = tk.Frame(self.tabControl)
        self.tabControl.add(self.books_view,text="COLLECTION")
        self.tabControl.add(self.inserting,text="AJOUTER UN LIVRE")
        self.tabControl.enable_traversal()
        
        self.tabControl.place(x=0,y=0)


        self.entry_title_content = tk.StringVar()
        self.entry_title = ttk.Entry(self.root,textvariable=self.entry_title_content)
        self.entry_title.place(x=1100,y=35)
        self.find_title_button = ttk.Button(self.root,text="Trouver titre",command=self.findGivenBook).place(x=1230,y=35)
        # Author entry
        self.entry_author_content = tk.StringVar()
        self.entry_author = ttk.Entry(self.root,textvariable=self.entry_author_content)
        self.entry_author.place(x=1100,y=75)
        self.find_author_button = ttk.Button(self.root,text="Trouver auteur",command=self.findGivenAuthor).place(x=1230,y=75)
        # Editor entry
        self.entry_editor_content = tk.StringVar()
        self.entry_editor = ttk.Entry(self.root,textvariable=self.entry_editor_content)
        self.entry_editor.place(x=1100,y=115)
        self.find_editor_button = ttk.Button(self.root,text="Trouver editeur",command=self.findGivenEditor).place(x=1230,y=115)
        # UI to insert books into BDD
        self.book_title_content = tk.StringVar()
        self.book_author_content = tk.StringVar()
        self.book_editor_content = tk.StringVar()
        self.book_isbn_content = tk.StringVar()
        self.book_author = ttk.Entry(self.inserting,textvariable=self.book_author_content)
        self.book_title = ttk.Entry(self.inserting,textvariable=self.book_title_content)
        self.book_editor = ttk.Entry(self.inserting,textvariable=self.book_editor_content)
        self.book_isbn = ttk.Entry(self.inserting,textvariable=self.book_isbn_content)
        self.book_title.grid(column=0,row=1)
        self.book_author.grid(column=1,row=1)
        self.book_editor.grid(column=2,row=1)
        self.book_isbn.grid(column=3,row=1)
        self.book_read_content = tk.IntVar()
        self.book_read = tk.Checkbutton(self.inserting,bd=10,variable=self.book_read_content,selectcolor='lightsteelblue1',cursor='hand2')
        self.book_read.grid(column=4,row=1)
        self.commit_button = ttk.Button(self.inserting,text="Ajouter ce livre",command=self.insertBook)
        self.commit_button.grid(column=2,row=3)
        self.databases = self.find_dbs()
        # Combobox to choose database
        self.db_chooser = ttk.Combobox(self.root,values=self.databases)
        self.db_chooser.state(['readonly'])
        self.db_chooser.place(x=250,y=0)
        # Right click contextual menu
        self.contextual_menu = tk.Menu(self.root, tearoff=0)
        self.contextual_menu.add_command(label="Supprimer le livre",command=self.delete_book)
        self.contextual_menu.add_separator()
        self.contextual_menu.add_command(label="Indiquer qu'il est prete.")
        self.contextual_menu.add_separator()
        self.contextual_menu.add_command(label="J'ai lu ce livre.", command=self.confirm_read)
        # QUIT button
        self.exit_button = ttk.Button(self.root, text="Quitter",command=self.confirmQuit).place(x=1200,y=650)
        # keyboard bindings
        self.root.focus_set()
        #self.set_bindings()
        self.root.mainloop()

    def find_dbs(self):
        dbs_found = []
        for f in os.listdir('.'):
            if f.endswith('.db'):
                dbs_found.append(f)
        return dbs_found

    def insertBook(self):
        book_to_insert = [self.book_title_content.get(),self.book_author_content.get(),
                          self.book_editor_content.get(),self.book_isbn_content.get()]
        wrong = False
        for f in book_to_insert:
            if not f:
                wrong = True
        if wrong:
            tk.messagebox.showwarning(title="Bad argument",message="Au moins un des champs est vide.")
        else:
            db.add_book(str(self.book_title_content.get()),str(self.book_author_content.get()),str(self.book_editor_content.get()),str(self.book_isbn_content.get()),str(self.book_read_content.get()))
            self.clear_panels()
            self.getAllBooks()

    def getAllBooks(self, event=None):
        self.booksList = db.get_all_books()
        self.displayBooks()

    def displayBooks(self):
        if self.title.size() == len(self.booksList):
            print("Books Already loaded")
        elif self.title.size() > len(self.booksList):
            print("BOOKS LOADED FOR FUCK SAKE")
        else:
            for b in self.booksList:
                read = "Non"
                if b[5] is not 0:
                    read = "Oui"
                self.title.insert(0,b[1])
                self.author.insert(0,b[2])
                self.editor.insert(0,b[3])
                self.isbn.insert(0,b[4])
                self.is_read.insert(0, read)

    def interrupt_behaviour(self,event):
        return "break"

    def confirm_read(self):
        """
        Asks user to confirm update on selected book

        """
        book_title = self.title.get(tk.ACTIVE)
        book = [b for b in self.booksList if b[5] == 0 and b[1] == book_title]
        if len(book) > 0:
            decision = tk.messagebox.askokcancel ("Confirmez","Vous avez lu '{}' ?".format(book_title))
            if decision:
                db.mark_read(book_title)
                self.clear_panels()
                self.getAllBooks()
        else:
            tk.messagebox.showwarning(title="Deja lu",message="Vous avez deja lu ce livre.")


    def confirmQuit(self):
        """
        Asks user to confirm exit.

        """
        decision = tk.messagebox.askokcancel("Quitter", "Voulez-vous quitter ?")
        if decision:
            self.root.destroy()
        else:
            pass

    def findGivenBook(self):
        book_to_find = self.entry_title_content.get().lower()
        i = 0
        for book in self.booksList:
            read = "Non"
            if book[5] is not 0:
                read = "Oui"
            if self.booksList[i-1][1].lower() ==  book_to_find:
                self.clear_panels()
                self.title.insert(0,self.booksList[i-1][1])
                self.author.insert(0,self.booksList[i-1][2])
                self.editor.insert(0,self.booksList[i-1][3])
                self.isbn.insert(0,self.booksList[i-1][4])
                self.is_read.insert(0,read)
            i += 1

    def clear_panels(self, event=None):
        self.title.delete(0,tk.END)
        self.author.delete(0,tk.END)
        self.editor.delete(0,tk.END)
        self.isbn.delete(0,tk.END)
        self.is_read.delete(0,tk.END)

    def findGivenAuthor(self, event=None):
        if event:
            author_to_find = self.author.get(tk.ACTIVE).lower()
        else:
            author_to_find = self.entry_author_content.get().lower()
        books_found = [b for b in self.booksList if b[2].lower() == author_to_find]
        if len(books_found) > 0:
            self.clear_panels()
            for b in books_found:
                read = "Non"
                if b[5] is not 0:
                    read = "Oui"
                self.title.insert(0,b[1])
                self.author.insert(0,b[2])
                self.editor.insert(0,b[3])
                self.isbn.insert(0,b[4])
                self.is_read.insert(0,read)


    def findRead(self,event=None):
        if self.is_read.get(tk.ACTIVE) == "Oui":
            books = [b for b in self.booksList if b[5] == 1]
            read = "Oui"
        else:
            books = [b for b in self.booksList if b[5] == 0]
            read = "Non"
        self.clear_panels()
        for b in books:
                self.title.insert(0,b[1])
                self.author.insert(0,b[2])
                self.editor.insert(0,b[3])
                self.isbn.insert(0,b[4])
                self.is_read.insert(0,read)

    def findGivenEditor(self, event=None):
        if event:
            editor_to_find = self.editor.get(tk.ACTIVE).lower()
        else:
            editor_to_find = self.entry_editor_content.get().lower()
        books_found = [b for b in self.booksList if b[3].lower() == editor_to_find]
        if len(books_found) > 0:
            self.clear_panels()
            for b in books_found:
                read = "Non"
                if b[5] is not 0:
                    read = "Oui"
                self.title.insert(0,b[1])
                self.author.insert(0,b[2])
                self.editor.insert(0,b[3])
                self.isbn.insert(0,b[4])
                self.is_read.insert(0,read)


    def scrollAllBoxes(self,*args):
        self.title.yview(*args)
        self.author.yview(*args)
        self.editor.yview(*args)
        self.isbn.yview(*args)
        self.is_read.yview(*args)

    def contextual_menu_display(self,event):
        """
        Displays a menu under cursor when right click
        is pressed over the title lisbox
        :param event: right click
        :return: void
        """
        try:
            self.contextual_menu.tk_popup(event.x_root,event.y_root,0)
        self.label_read = tk.Label(self.inserting,text='LU').grid(column=4,row=0)
        finally:
            self.contextual_menu.grab_release()


    def delete_book(self):
        book_title =  self.title.get(tk.ACTIVE)
        complete_book = [b for b in self.booksList if b[1] == book_title]
        if len(complete_book) > 0:
            decision = tk.messagebox.askokcancel ("Confirmez","Supprimer '{}' ?".format(complete_book[0][1]))
            if decision:
                db.remove_book(complete_book)
                self.clear_panels()
                self.getAllBooks()



        # Doubleclick
        # Popup menu and scrolling
        #self.root.bind('<MouseWheel>',self.scrollAllBoxes)
        #self.title.bind('<Button-3>', self.contextual_menu_display)


if __name__ == "__main__":
    biblio()


