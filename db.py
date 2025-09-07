import sqlite3

from flask import g


def get_connection():
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("PRAGMA foreign_keys = ON")
    cur.execute("PRAGMA encoding = 'UTF-8'")
    con.commit()
    con.row_factory = sqlite3.Row
    return con


def execute(sql, params=[]):
    con = get_connection()
    result = con.execute(sql, params)
    con.commit()
    g.last_insert_id = result.lastrowid
    con.close()


def last_insert_id():
    return g.last_insert_id


def query(sql, params=[]):
    con = get_connection()
    result = con.execute(sql, params).fetchall()
    con.close()
    return result
