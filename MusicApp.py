# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 15:45:34 2021

@author: Paul.Greaney
"""

import tkinter as tk
from tkinter import ttk
from NewAlbumForm import NewAlbumForm
from AlbumTable import AlbumTable
from sqlite_utils import create_connection
from LoginWindow import LoginWindow

class MusicApp(tk.Tk):
    def __init__(self):
        super().__init__()
        database = r"sample.db"

        self.geometry("800x400")
        self.mode = 1 #non-admin user by default
        self.connection = create_connection(database)
        self.cursor = self.connection.cursor()
        self.create_welcome_frame()
        self.create_dashboard_frame()
        self.create_albums_frame()
        self.display_welcome_frame()
        self.mainloop()
        self.connection.close()

    def create_welcome_frame(self):
        self.welcome_frame = tk.Frame(self)
        label = ttk.Label(self.welcome_frame, text='Welcome to the Music App', 
                          font=("Arial", 20))
        label.grid(row=1, column=1, padx=10, pady=10)
        login_button = ttk.Button(self.welcome_frame, text='Login', 
                                  command=self.login)
        login_button.grid(row=2, column=1, padx=20, pady=20)
        
    def create_dashboard_frame(self):
        self.dashboard_frame = tk.Frame(master=self)
        self.view_albums_button = ttk.Button(self.dashboard_frame, 
            text='View Albums', command=self.display_albums_frame)
        self.view_albums_button.grid(row=1, column=0, padx=20, pady=20)
        logout_button = ttk.Button(self.dashboard_frame, text='Logout',
                                             command=self.logout)
        logout_button.grid(row=2, column=0, padx=20, pady=20)

    def create_albums_frame(self):
        self.albums_frame = tk.Frame(master=self)
        self.cursor.execute("SELECT * FROM albums")
        data = (row for row in self.cursor.fetchall())
        self.dashboard_button = ttk.Button(self.albums_frame, 
            text='Dashboard', command=self.display_dashboard_frame)
        self.dashboard_button.grid(row=0, column=0, padx=20, pady=(0,20))
        self.label = ttk.Label(self.albums_frame, text='Albums', 
                          font=("Arial", 20)).grid(row=1, column=0)
        
        self.table = AlbumTable(self.albums_frame, connection=self.connection, 
                                rows=data, mode=self.mode)
        self.table.grid(row=2, column=0, sticky='news')

        # note that self.mode is set in LoginWindow via self.master.mode
        if self.mode==1:
            button_state='disabled'
        elif self.mode==2:
            button_state='normal'
        self.albums_frame.new_album_button = ttk.Button(self.albums_frame, 
                                           text='New Album', 
                                           state=button_state, 
                                           command=self.new_album)
        self.albums_frame.new_album_button.grid(row=3, column=0, pady=20)

    def login(self):
        self.login_window = LoginWindow(master=self, 
                                        connection=self.connection)
        self.login_window.grab_set()
        self.login_window.wait_window()

    def logout(self):
        self.display_welcome_frame()
        
    def display_welcome_frame(self):
        self.dashboard_frame.place_forget()
        self.albums_frame.place_forget()
        self.welcome_frame.place(in_=self, anchor="c", relx=.5, rely=.5)

    def display_albums_frame(self):
        self.create_albums_frame()
        # calling this each time to regenerate the frame, in case admin
        # priveleges change
        self.welcome_frame.place_forget()
        self.dashboard_frame.place_forget()
        self.albums_frame.place(in_=self, anchor="c", relx=.5, rely=.5)

    def display_dashboard_frame(self):
        self.welcome_frame.place_forget()
        self.albums_frame.place_forget()
        self.dashboard_frame.place(in_=self, anchor="c", relx=.5, rely=.5)
        
    def new_album(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT ArtistId, Name FROM artists")
        data = (row for row in cursor.fetchall())
        new_album_form = NewAlbumForm(artists=dict(data), 
                                      connection=self.connection)
        
if __name__=='__main__':
    app = MusicApp()
