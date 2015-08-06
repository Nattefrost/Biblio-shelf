# Dialog to enter book references

import tkinter as tk
from tkinter import ttk
import db_access

class AddDialog:
    def __init__(self, parent):
        self.root = tk.Tk()
        self.isReadVar = tk.BooleanVar()
        self.root.eval('tk::PlaceWindow %s center' % self.root.winfo_pathname(self.root.winfo_id()))
        self.parent = parent
        self.root.title("Add a book")
        self.root.geometry("275x175")
        self.result = None
        self.style = ttk.Style()
        self.style.theme_use('clam')
        # StringVars to add a book
        self.titleVar = tk.StringVar()
        self.authorVar = tk.StringVar()
        self.collectionVar = tk.StringVar()


        # Entries to add a book

        self.title_entry = ttk.Entry(self.root,textvariable=self.titleVar,width=15)
        self.author_entry = ttk.Entry(self.root,textvariable=self.authorVar,width=15)
        self.collection_entry = ttk.Entry(self.root,textvariable=self.collectionVar, width=15)
        self.isRead_check = tk.Checkbutton(self.root,text="READ?",width=7,variable=self.isReadVar,command=self.change_bool)

        self.title_entry.grid(column=0,row=0)
        self.author_entry.grid(column=0,row=1)
        self.collection_entry.grid(column=0,row=2)
        self.isRead_check.grid(column=0,row=3)

        font = "Georgia 12"
        # labels
        self.title_label = tk.Label(self.root, text="Title",font=font).grid(column=1,row=0)
        self.author_label = tk.Label(self.root, text="Author",font=font).grid(column=1,row=1)
        self.collection_label = tk.Label(self.root, text="Publisher",font=font).grid(column=1,row=2)

        # Buttons
        self.cancel_btn = tk.Button(self.root, text="Cancel",command=self.cancel,relief= tk.GROOVE,bd=3,bg="indianred")
        self.validate_btn = tk.Button(self.root,relief=tk.RAISED, bd=3, text="Validate",command=self.validate,bg="palegreen")

        self.cancel_btn.grid(column=1,row=4)
        self.validate_btn.grid(column=0,row=4)

        self.root.mainloop()

    def change_bool(self):
        if self.isReadVar.get() != True:
            self.isReadVar.set(True)
        else:
            self.isReadVar.set(False)

    def cancel(self):
        self.root.destroy()

    def validate(self):
        db_access.add_book(self.title_entry.get().capitalize(), self.author_entry.get().capitalize(),
            self.collection_entry.get().capitalize() , self.isReadVar.get() )
        #self.parent.tree_data = db_access.get_books_to_view()
        self.parent.load_all_callback()
        self.root.destroy()
