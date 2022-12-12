# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 19:38:18 2021

@author: Paul.Greaney
"""

import tkinter as tk
from tkinter import ttk
from sqlite_utils import create_track, update_track

class TrackForm(tk.Toplevel):
    def __init__(self, master=None, update=False, track_info=None, 
                 connection=None):
        tk.Toplevel.__init__(self, master)
        labels = ['Track ID', 'Title', 'Album ID', 'Media Type ID', 'Genre ID', 
                  'Composer', 'Milliseconds', 'Bytes', 'Unit Price']
        self.track_info = track_info
        self.connection = connection
        if not self.track_info:
            self.track_info = tuple('' for i in range(len(labels)))
        else:
            self.track_info = tuple(tuple(self.track_info)[0])
            print(track_info)
        self.values = [tk.StringVar(value=self.track_info[i]) 
                       for i in range(len(labels))]
                
        for i, l in enumerate(labels):
            label = ttk.Label(self, text=l)
            label.grid(row=i, column=0, padx=(50,10), pady=(10, 10))
            if l=='Track ID':
                entrybox = ttk.Entry(self, state='disabled',
                                     textvariable=self.values[i])
                entrybox.grid(column=2, row=i, padx=(0,50), pady=(10, 10))
            else:
                entrybox = ttk.Entry(self, textvariable=self.values[i])
                entrybox.grid(column=2, row=i, padx=(0,50), pady=(10, 10))
        if update:
            update_button = ttk.Button(self, text='Update', 
                                       command=self.update, 
                                       style="TButton" )
            update_button.grid(row=9, columnspan=3, padx=30, pady=(30,30))
        else:
            submit_button = ttk.Button(self, text='Submit',
                                       command=self.submit,
                                       style="TButton" )
            submit_button.grid(row=9, columnspan=3, padx=30, pady=(30,30))

    def submit(self):
        """submit is used when creating a new record"""
        title, album_id, media_type_id, genre_id, composer,\
        milliseconds, bytes1, unit_price = [i.get() for i in self.values[1:]]
        
        new_entry_id = create_track(self.connection, (title, album_id,
                                       media_type_id, genre_id, 
                                       composer, milliseconds,
                                       bytes1, unit_price))
        self.destroy()
        self.new_track_info = [new_entry_id]+[i.get() for i in self.values[1:]]

    def update(self):
        """update is used when updating an existing record"""
        track_id, title, album_id, media_type_id, genre_id, composer,\
        milliseconds, bytes1, unit_price = [i.get() for i in self.values]
        
        update_track(self.connection, (title, album_id, media_type_id, 
                                       genre_id, composer, milliseconds,
                                       bytes1, unit_price, track_id))
        #note track_id goes last as we use it in the WHERE clause
        self.destroy()