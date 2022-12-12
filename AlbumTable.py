# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 17:56:21 2021

@author: Paul.Greaney
"""
import tkinter as tk
from tkinter import ttk
from Table import Table
from TrackTable import TrackTable

class AlbumTable(Table):
    def __init__(self, master=None, connection=None,
                 rows=tuple(), mode=1):
        self.widths=(40, 400)
        super().__init__(master, connection=connection, 
                         headings=('ID', 'Album'), widths=self.widths,
                         rows=rows)
        self.mode = mode
        self.table.bind("<Double-Button-1>", self.on_double_click_get_tracks)
        self.search = tk.StringVar()
        search_form = tk.Frame(self, width=250)
        search_form.grid(row=1, column=2)
        search_label = ttk.Label(search_form, text="Search")
        search_label.grid(row=1, column=2)
        search_field = ttk.Entry(search_form, textvariable=self.search,
                                 width=20)
        search_field.grid(row=3, column=2, padx=15)
        search_button = ttk.Button(search_form, text="Search", 
                                    command=self.search_data)
        search_button.grid(row=4, column=2, pady=(5,0))
        view_all_button = ttk.Button(search_form, text="View All", 
                                     command=self.display_data)
        view_all_button.grid(row=5, column=2, pady=(5,0))

    def on_double_click_get_tracks(self, event):
        item_id = event.widget.focus()
        item = event.widget.item(item_id)
        cursor = self.connection.cursor()

        values = item['values']
        albumid = str(values[0])
        cursor.execute("SELECT TrackId, Name, Composer, Milliseconds \
                            FROM tracks WHERE AlbumID=(?)", (albumid,))
        data = (row for row in cursor.fetchall())
        tracks_win = tk.Toplevel()
        table = TrackTable(parent=tracks_win, connection=self.connection,
                           rows=data, mode=self.mode)
        table.pack(expand=tk.YES, fill=tk.BOTH)
    
    def search_data(self):
        """function to search records"""
        #checking search text is empty or not
        if self.search.get() != "":
            #clearing current display data
            self.table.delete(*self.table.get_children())
            cursor=self.connection.execute("SELECT * FROM albums \
                                           WHERE title LIKE ?", 
                                           ('%' + str(self.search.get()) 
                                            + '%',))
            #fetch all matching records
            fetch = cursor.fetchall()
            #loop for displaying all records into GUI
            for data in fetch:
                self.table.insert('', 'end', values=(data))