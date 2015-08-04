# Dialog to enter book references

import tkinter as tk
from tkinter import ttk
import db_access

class AddDialog:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Add a book")
        self.root.geometry("275x175")
        self.result = None
        self.style = ttk.Style()
        self.style.theme_use('alt')

        # StringVars to add a book
        self.titleVar = tk.StringVar()
        self.authorVar = tk.StringVar()
        self.collectionVar = tk.StringVar()
        self.isReadVar = tk.IntVar()

        # Entries to add a book

        self.title_entry = tk.Entry(self.root,relief=tk.SUNKEN,bd=3,textvariable=self.titleVar,width=15)
        self.author_entry = tk.Entry(self.root,relief=tk.SUNKEN,bd=3,textvariable=self.authorVar,width=15)
        self.collection_entry = tk.Entry(self.root,relief=tk.SUNKEN,bd=3,textvariable=self.collectionVar, width=15)
        self.isRead_check = ttk.Checkbutton(self.root,text="READ?",width=6,variable=self.isReadVar)

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
        self.cancel_btn = ttk.Button(self.root, text="Cancel",command=self.cancel)
        self.validate_btn = ttk.Button(self.root, text="Validate",command=self.validate)

        self.cancel_btn.grid(column=0,row=4)
        self.validate_btn.grid(column=1,row=4)

        self.root.mainloop()

    def cancel(self):
        self.root.destroy()

    def validate(self):
        print( self.title_entry.get(), self.isReadVar.get() )
        db_access.add_book(self.titleVar.get(), self.authorVar.get(), self.collectionVar.get() , self.isReadVar.get() )
        self.root.destroy()
