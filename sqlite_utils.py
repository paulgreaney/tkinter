# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 21:11:17 2021

@author: Paul.Greaney
"""
import sqlite3
import os

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object
    """
    conn = None
    if not os.path.exists(db_file):
        raise Exception("Database file does not exist: {}".format(db_file))
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    c = conn.cursor()
    c.execute(create_table_sql)

def create_project(conn, project):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO projects(name,begin_date,end_date)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    conn.commit()
    return cur.lastrowid

def create_task(conn, task):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """

    sql = ''' INSERT INTO tasks(name,priority,status_id,project_id,begin_date,end_date)
              VALUES(?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()
    return cur.lastrowid

def create_album(conn, album):
    """
    Create a new album
    :param conn: the connection
    :param album: tuple of album information
    :return:
    """

    sql = ''' INSERT INTO albums(Title,ArtistId)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, album)
    conn.commit()
    return cur.lastrowid

def create_artist(conn, artist):
    """
    Create a new artist
    :param conn: the connection
    :param album: tuple of artist information
    :return:
    """

    sql = ''' INSERT INTO artists(Name)
              VALUES(?) '''
    cur = conn.cursor()
    cur.execute(sql, artist)
    conn.commit()
    return cur.lastrowid

def create_track(conn, track):
    """
    Create a new track
    :param conn: the connection
    :param album: tuple of track information
    :return:
    """

    sql = ''' INSERT INTO tracks(Name, AlbumId, MediaTypeId,
              GenreId, Composer, Milliseconds, Bytes, UnitPrice)
              VALUES(?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, track)
    conn.commit()
    return cur.lastrowid

def update_track(conn, track):
    """
    Create a new task
    :param conn: the connection
    :param album: tuple of album information
    :return:
    """

    sql = ''' UPDATE tracks SET Name=?, AlbumId=?, MediaTypeId=?,
              GenreId=?, Composer=?, Milliseconds=?, Bytes=?, UnitPrice=?
              WHERE TrackId=?'''
    cur = conn.cursor()
    cur.execute(sql, track)
    conn.commit()
    return cur.lastrowid

def delete_track(conn, track_id):
    """
    Delete a track from the table
    :param conn: the connection
    :param track_id: the track id
    :return:
    """

    sql = ''' DELETE FROM tracks WHERE TrackId=? '''
    cur = conn.cursor()
    cur.execute(sql, track_id)
    conn.commit()
    return cur.lastrowid

def check_credentials(conn, name, password):
    try:
        cursor = conn.cursor()
        cursor.execute('''SELECT username, password, user_type_id FROM users''')
        data = cursor.fetchall()
        for row in data:
            if row[0]==name and row[1]==password:
                return row[2] #user type
        return False
    except sqlite3.Error as e:
        print("Error in database: ", e)
        return -1
