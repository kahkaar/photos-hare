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


def execute_many(sql_params):
    con = get_connection()
    cur = con.cursor()

    for sql, params in sql_params:
        cur.execute(sql, params)

    con.commit()
    con.close()


def _add_empty(items):
    items.append([])


def queries_get_last(execute_sql_params, query_sql_params):
    con = get_connection()
    cur = con.cursor()
    for sql_params in execute_sql_params:
        if len(sql_params) < 2:
            _add_empty(sql_params)

        sql, params = sql_params
        cur.execute(sql, params)

    if len(query_sql_params) < 2:
        _add_empty(query_sql_params)

    sql, params = query_sql_params[:2]
    result = cur.execute(sql, params).fetchall()

    con.commit()
    con.close()

    return result
