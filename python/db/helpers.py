import sqlite3
from contextlib import closing
from flask import Flask

def connect_db(app):
    return sqlite3.connect(app.config['DATABASE'])

def make_dicts(cur, row):
    return dict((cur.description[idx][0], value) for idx, value in enumerate(row))

def query_db(query, args=(), one=False):
    try:
        cur = Flask.db.execute(query, args)
    except sqlite3.OperationalError, msg:
        print msg
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv
