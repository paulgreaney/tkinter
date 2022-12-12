# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 17:55:54 2021

@author: Paul.Greaney
"""

import tkinter as tk
from tkinter import ttk
from sqlite_utils import create_album, create_artist

class NewAlbumForm(tk.Toplevel):
    def __init__(self, master=None, artists=None, connection=None):
        tk.Toplevel.__init__(self, master)
        labels = ['Title', 'Artist']
        self.artists = artists
        self.connection = connection
        self.album_title = tk.StringVar()
        self.artist_name = tk.StringVar()
        self.artists_list = sorted(list(self.artists.values()))
                
        label = ttk.Label(self, text='Title')
        label.grid(row=1, column=0, sticky=tk.W, padx=(50,10), pady=(30, 0))
        label = ttk.Label(self, text='Artist')
        label.grid(row=2, column=0, sticky=tk.W, padx=(50,10), pady=(30, 30))
        entrybox = ttk.Entry(self, textvariable=self.album_title)
        entrybox.grid(column=1, row=1, padx=(0,50), pady=(30, 0))  

        artist_combobox = ttk.Combobox(self, textvariable=self.artist_name)
        artist_combobox['values'] = self.artists_list
        artist_combobox.bind('<KeyRelease>', self.check_input)
        artist_combobox.grid(column=1, row=2, padx=(0,50), pady=(30, 30)) 
        submit_button = ttk.Button(self, text='Submit', command=self.submit, 
                                   style="TButton" )
        submit_button.grid(row=3, columnspan=2, padx=30, pady=(30,30))

    def check_input(self, event):
        value = event.widget.get()
        if value == '':
            artist_combobox['values'] = list(self.artists.values())
        else:
            data = []
            for item in self.artists_list:
                if value.lower() in item.lower():
                    data.append(item)
            artist_combobox['values'] = data
        
    def submit(self):
        title = self.album_title.get()
        artist = self.artist_name.get()
        artist_id = None
        for k, v in list(self.artists.items()):
            if v == artist:
                artist_id = k
        if artist_id == None:
            #create entry in artist table
            create_artist(self.connection, (artist,))
            #note that when there's only one value, 
            #we need a comma to make it a tuple of the form expected
        create_album(self.connection, (title, artist_id))
        self.destroy()
