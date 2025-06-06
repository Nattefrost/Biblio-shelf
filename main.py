__author__ = 'Nattefrost'

import tkinter as tk
import db_creation
import db_access
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox
import find_book_ISBN as isbn
import math
import add_dialog
import plot
import stats
from barcode_reader import barcode_reader

class Biblio(tk.Frame):
    def __init__(self, root ):
        tk.Frame.__init__(self, root)
        #root.attributes("-fullscreen", True) 
        root['bg'] = 'lightgray'
        root.windowIcon = tk.PhotoImage("photo", file="./book_icon.gif") # setting icon
        root.tk.call('wm','iconphoto',root._w, root.windowIcon)
        root['bd'] = 10
        root['relief'] = tk.FLAT
        root.resizable(1,1)
        #root.geometry("850x685")
        root.geometry("1024x768")
        self.PLOT_WINDOW = 0
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.tree_data = db_access.get_books_to_view()
        self.treeFrame = tk.Frame(root,relief=tk.FLAT).grid(row=0,column=0)
        self.view = ttk.Treeview(self.treeFrame, height=27,
                                    columns=("id","Title","Author","Collection"),
                                    selectmode='browse',
                                    displaycolumns=[0,1,2,3])
        self.view['show'] = 'headings' #removes first empty column
        self.view.heading('#0', text='id', anchor='w')
        self.view.heading('#1', text="Title", anchor="w")
        self.view.heading('#2', text="Author", anchor="w")
        self.view.heading('#3', text="Publisher", anchor="w")
        self.view.heading('#4',text="Read",anchor="w")
        self.view.grid(row=1,column=0,sticky=tk.W+tk.S+tk.NE,columnspan=3)
        self.ysb = ttk.Scrollbar(self.treeFrame, orient='vertical', command=self.view.yview)
        self.view.configure(yscroll=self.ysb.set )
        self.ysb.grid(row=1,column=3,sticky=tk.E+tk.N+tk.S)
        self.view.tag_configure('oddrow', background='black',foreground="white")
        self.view.tag_configure('evenrow',background='#133596', foreground='white')
        self.insert_content(self.tree_data)

        # Searchbar
        self.searchVar = tk.StringVar()
        self.search_entry = tk.Entry(root, bg="#9DB8AE", bd=1,fg="#280041", relief=tk.SOLID, font="Consolas 12 bold italic",textvariable=self.searchVar)
        self.search_entry.grid(row=2,column=0,sticky=tk.W+tk.N+tk.E,columnspan=3)

        # Search buttons
        self.search_title_button = ttk.Button(root, text='Search title',underline=7, command=self.onClick_title )
        self.search_title_button.grid(row=3,column=0,sticky=tk.W+tk.S+tk.E)
        self.search_author_button = ttk.Button(root,text="Search author",underline=7,command=self.onClick_author)
        self.search_author_button.grid(row=3,column=1,sticky=tk.W+tk.S+tk.E)
        self.search_col_button = ttk.Button(root,text="Search publisher",underline=10,command=self.onClick_collection)
        self.search_col_button.grid(row=3,column=2,sticky=tk.W+tk.S+tk.E)
        self.scan_barcode_button = ttk.Button(root,text="Scan barcode",underline=5,command=self.onClick_scan_barcode)
        self.scan_barcode_button.grid(row=4,column=1,sticky=tk.W+tk.S+tk.E)
        self.load_all = ttk.Button(root,text='Reload (F5)', command=self.load_all_callback)
        self.load_all.grid(row=4,column=0,sticky=tk.W+tk.S+tk.E)
        self.load_stats = ttk.Button(root, text="Show stats", command=self.onClick_stats)
        self.load_stats.grid(row=4,column=2,sticky=tk.W+tk.S+tk.E)

        # Right click contextual menu
        self.contextual_menu = tk.Menu(root, tearoff=0, activebackground='#690093',activeforeground="white",bg="gray8",
                                       fg="white",font="Verdana 10 bold",relief=tk.FLAT)
        self.contextual_menu.add_command(label="Delete selected book.",command=self.delete_selected)
        self.contextual_menu.add_separator()
        self.contextual_menu.add_command(label="Mark book as read.",command=self.mark_read )
        self.contextual_menu.add_separator()
        self.contextual_menu.add_command(label="Add full book references.                            F1",command=self.add_book_window)
        self.contextual_menu.add_command(label="Add book by ISBN number. Needs network  F2",command=self.ask_isbn)
        self.contextual_menu.add_separator()
        self.contextual_menu.add_command(label="Cancel")

        # Keyboard bindings
        root.bind('<Button-3>', self.contextual_menu_display )
        root.bind('<Return>', self.onClick_title )
        root.bind('<Control-o>', self.load_all_callback )
        root.bind('<Control-a>', self.onClick_author )
        root.bind('<Control-l>', self.onClick_collection)
        root.bind('<Control-b>', self.onClick_scan_barcode)
        root.bind('<F2>', self.ask_isbn)
        root.bind('<F1>', self.add_book_window)
        root.bind('<F5>', self.load_all_callback)

        root.mainloop()


  # TODO check keys in json
    def ask_isbn(self, event=None):
        isbn_nb = simpledialog.askstring(title="Search book by ISBN", prompt="ISBN number :")
        if isbn_nb:
            book_data = isbn.get_book_by_isbn(isbn_nb)
            print(book_data)
            if 'publisher' in book_data:
                author_name = "{} {}".format(book_data['author'][0]['family'], book_data['author'][0]['given'])
                #book_data['publisher'] = "Unknown"
                res = messagebox.askquestion("Add this book ?","\nTitle : {} \nAuthor : {} \nPublisher : {}\nISBN : {} ".format(book_data['title'], author_name, book_data['publisher'], book_data['ISBN']) )
                if res == "yes":
                    db_access.add_book(book_data['title'], author_name ,book_data['publisher'], book_data['ISBN'] ,False)
                    self.load_all_callback()
            else:
                messagebox.showerror("Book not found", """Could not find the book. \nPlease enter full book references""")



    def mark_read(self):
        item = self.view.selection()[0]
        to_mark = self.view.item(item,"values")
        db_access.mark_read(to_mark[0])
        self.load_all_callback()
    # buttons onclick

    def delete_selected(self):
        item = self.view.selection()
        to_delete = self.view.item(item,"values")
        if to_delete:
            res = messagebox.askquestion("Delete book ?","Are you sure you want to delete this book : {} ?".format(to_delete[0]))
            if res == "yes":
                db_access.remove_book(to_delete)
                self.view.delete(self.view.selection())
                self.load_all_callback()

    def onClick_title(self, event=None):
        self.search_start(0)
    def onClick_author(self, event=None):
        self.search_start(1)
    def onClick_collection(self, event=None):
        self.search_start(2)
    def onClick_stats(self, event=None):
        if not self.PLOT_WINDOW:
            self.PLOT_WINDOW +=1
            plot.TkPlot(stats.generate_authors_top_ten(), self)
    def load_all_callback(self,event=None):
        self.clean_tree()
        self.tree_data = db_access.get_books_to_view()
        self.insert_content(self.tree_data)

    def search_start(self, criteria):
        pattern = self.searchVar.get().lower()
        if len(pattern) > 0:
            found_books = []
            for x in range(len(self.tree_data)):
                if self.tree_data[x][criteria].lower().startswith(pattern):
                    found_books.append(self.tree_data[x])
            if len(found_books) == 0:
                found_books = (["NO BOOK WAS FOUND"])
            self.clean_tree()
            self.insert_content(found_books)


    def add_book_window(self, event=None):
        add_dialog.AddDialog(self)

    def clean_tree(self):
        self.view.delete(*self.view.get_children())

    def insert_content(self, data):
        for x in range(len(data)):
            if x % 2 == 0:
                self.view.insert('', 'end', values=data[x],tags=("oddrow",))
            else:
                self.view.insert('', 'end', values=data[x],tags=("evenrow",))

    def contextual_menu_display(self, event):
        """
        Displays a menu under cursor when right click
        is pressed over the treeview table
        :param event: right click
        :return: void
        """
        try:
            self.contextual_menu.tk_popup(event.x_root,event.y_root,0)
        finally:
            self.contextual_menu.grab_release()

    def onClick_scan_barcode(self, event=None):
        isbn_list = barcode_reader.scan_barcode(0)
        for isbn_nb in isbn_list:
          db_access.insert_isbn(isbn_nb)

    


if __name__ == "__main__":
    db_creation.check_db_exists()
    root = tk.Tk()
    root.title("Biblio")
    app = Biblio(root)
