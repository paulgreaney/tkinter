# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 17:56:21 2021

@author: Paul.Greaney
"""
import tkinter as tk
from tkinter import ttk
from TrackForm import TrackForm
from sqlite_utils import delete_track

class Table(tk.Frame):
    def __init__(self, parent=None, connection=None,
                 headings=tuple(), widths=tuple(), rows=tuple()):
        super().__init__(parent)
        self.connection = connection
        self.table = ttk.Treeview(self, show="headings",
                                  selectmode="browse")
        self.table["columns"] = headings
        self.table["displaycolumns"] = headings
        self.rows = list(rows)
        for i, head in enumerate(headings):
            self.table.heading(head, text=head, anchor=tk.CENTER)
            self.table.column(head, anchor=tk.CENTER, width=widths[i],
                              stretch=True)
  
        scrolltable = ttk.Scrollbar(self, command=self.table.yview)
        self.table.configure(yscrollcommand=scrolltable.set)
        scrolltable.grid(row=1, column=1, sticky='ns')
        # sticky parameter makes the scrollbar span the full table
        self.table.grid(row=1, column=0, padx=(10,0))
        self.display_data()

    def on_tree_select(self, event):
        """sets the id of the currently selected item as an object #
           attribute, which can then be used to delete an entry"""
        selected_item = event.widget.focus()
        item = event.widget.item(selected_item)
        item_id = str(item['values'][0])
        self.delete_item_id = item_id
        
    def display_data(self):
        self.table.delete(*self.table.get_children())
        for row in self.rows:
            self.table.insert('', tk.END, values=tuple(row))

    def search_data(self):
        #Implement in child class
        """function to search records, depends on type of data 
        so implement in child classes"""
        raise NotImplementedError("Search method not implemented!")
