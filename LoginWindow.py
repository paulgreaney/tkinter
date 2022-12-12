# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 17:55:54 2021

@author: Paul.Greaney
"""

import tkinter as tk
from tkinter import ttk
from sqlite_utils import check_credentials

class LoginWindow(tk.Toplevel):
    def __init__(self, master=None, connection=None):
        tk.Toplevel.__init__(self, master)
        self.connection = connection
        self.master = master
        self.name_var = tk.StringVar()
        self.password_var = tk.StringVar()
        
        
        name_label = ttk.Label(self, text='Username')
        name_label.grid(row=1, column=1, padx=10, pady=10)
        password_label = ttk.Label(self, text='Password')
        password_label.grid(row=2, column=1, padx=10, pady=10)
        self.username_input_area = ttk.Entry(self, width=20, 
                                             textvariable=self.name_var)
        self.username_input_area.grid(row=1, column=2, columnspan=2, 
                                 padx=10, pady=10)
        self.password_input_area= ttk.Entry(self, width=20, show = '*',
                                            textvariable=self.password_var)
        self.password_input_area.grid(row=2, column=2, columnspan=2, 
                                 padx=10, pady=10)
        submit_button = ttk.Button(self, text='Submit', command=self.submit)
        submit_button.grid(row=3, column=2, padx=10, pady=10)
    
        cancel_button = ttk.Button(self, text='Cancel', command=self.cancel)
        cancel_button.grid(row=3, column=3, padx=10, pady=10)
        # usually, forms like this accept a 'submit' click via the enter
        # or return key, so let's bind that key to the submit method
        self.bind('<Return>', self.submit)
        
    def submit(self, event=None):
        name=self.name_var.get()
        password=self.password_var.get()
        
        mode = check_credentials(self.connection, name, password)
        if mode in [1,2]:
            self.destroy()
            self.master.mode = mode
            # used to activate admin buttons if authorised
            self.master.display_dashboard_frame()
            # remember self.master is the root window, so we can use methods
            # defined in MusicApp by calling them as self.master.<method>
        elif mode==-1:
            # a -1 returned from check_credentials means there's a database
            # error - display a suitable error box
            self.error_win = tk.Toplevel()
            error_label = ttk.Label(self.error_win, text='Database error')
            error_label.grid(row=1, column=1, padx=50, pady=10)
            ok_button = ttk.Button(self.error_win, text='OK', 
                                   command=self.error_win_okay)
            ok_button.grid(row=2, column=1, padx=50, pady=10)
        else:
            # the login details are incorrect - display a message and clear
            # the boxes to give the user another chance
            self.error_win = tk.Toplevel()
            incorrect_label = ttk.Label(self.error_win, 
                text='Incorrect username or password')
            incorrect_label.grid(row=1, column=1, padx=10, pady=10)
            ok_button = ttk.Button(self.error_win, text='OK', 
                                   command=self.error_win_okay)
            ok_button.grid(row=2, column=1, padx=10, pady=10)
            self.error_win.bind('<Return>', self.error_win_okay)
            self.error_win.grab_set()

    def error_win_okay(self, event=None):
        self.error_win.destroy()
        self.grab_set()
        self.username_input_area.delete(0, 'end')
        self.password_input_area.delete(0, 'end')
        
    def cancel(self):
        def yes():
            cbox.destroy()
            self.destroy()
            
        def no():
            cbox.destroy()
            
        cbox = tk.Toplevel()
        cbox.grab_set()
        cboxlabel = ttk.Label(cbox, text="Are you sure?")
        cboxlabel.grid(row=1, column=1, columnspan=2, padx=20, pady=20)
        yes_button = ttk.Button(cbox, text='Yes', command=yes)
        yes_button.grid(row=2, column=1, padx=(10,5), pady=10)
        no_button = ttk.Button(cbox, text='No', command=no)
        no_button.grid(row=2, column=2, padx=(5,10), pady=10)
