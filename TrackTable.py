# -*- coding: utf-8 -*-
"""
Created on Tue Oct  5 17:56:21 2021

@author: Paul.Greaney
"""
import tkinter as tk
from tkinter import ttk
import csv
from TrackForm import TrackForm
from sqlite_utils import delete_track
from Table import Table

class TrackTable(Table):
    def __init__(self, parent=None, connection=None,
                 headings=tuple(), widths=tuple(), rows=tuple(), mode=1):
        self.widths = (100, 300, 300, 100)
        super().__init__(parent, connection=connection,
                         headings=('TrackID', 'Name', 'Composer', 
                                   'Milliseconds'), widths=self.widths, 
                         rows=rows)
        self.mode = mode
        self.table.bind("<Double-Button-1>", 
                        self.on_double_click_get_track_info)
        self.table.bind("<<TreeviewSelect>>", self.on_tree_select)

        if self.mode==1:
            button_state='disabled'
        elif self.mode==2:
            button_state='normal'
            
        new_track_button = ttk.Button(self, text='Add Track',
                                   command=self.new_track,
                                   style="TButton", state=button_state)
        new_track_button.grid(row=3, padx=30, pady=(20,5))
        delete_button = ttk.Button(self, text='Delete Track',
                                   command=self.delete_track,
                                   style="TButton", state=button_state)
        delete_button.grid(row=4, padx=30, pady=(5,5))
        save_button = ttk.Button(self, text='Save as CSV',
                                   command=self.save_csv,
                                   style="TButton")
        save_button.grid(row=5, padx=30, pady=(5,20))

    def new_track(self):
        """open a TrackForm window to add a new track"""
        track_form = TrackForm(update=False, track_info=None,
                               connection=self.connection)
        track_form.wait_window()
        print(track_form.new_track_info)
        self.table.insert('', 'end', values=track_form.new_track_info)
    
    def delete_track(self):
        """delete a track"""
        delete_track(self.connection, (self.delete_item_id,))
        self.table.delete(self.table.selection())
        
    def on_double_click_get_track_info(self, event):
        item_id = event.widget.focus()
        item = event.widget.item(item_id)
        cursor = self.connection.cursor()

        values = item['values']
        trackid = str(values[0])
        cursor.execute("SELECT * \
                            FROM tracks WHERE TrackId=(?)", (trackid,))
        track_data = (row for row in cursor.fetchall())
        # open a new form with the data pre-populated
        track_form = TrackForm(self, update=True, track_info=track_data,
                               connection=self.connection)
    
    def save_csv(self):
        with open("tracks.csv", "w", newline='') as myfile:
            csvwriter = csv.writer(myfile, delimiter=',')
            csvwriter.writerow(['ID', 'Name', 'Composer', 'Size'])

            for row_id in self.table.get_children():
                row = self.table.item(row_id)['values']
                csvwriter.writerow(row)