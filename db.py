import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "imoveis.db")

def _dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = _dict_factory
    return conn

def query_all(sql, params=()):
    with get_conn() as conn:
        cur = conn.execute(sql, params)
        return cur.fetchall()

def query_one(sql, params=()):
    with get_conn() as conn:
        cur = conn.execute(sql, params)
        return cur.fetchone()

def execute(sql, params=()):
    with get_conn() as conn:
        cur = conn.execute(sql, params)
        conn.commit()
        return cur.lastrowid, cur.rowcount
