import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "imoveis.db")

def init_db():
    with open("imoveis.sql", "r", encoding="utf-8") as f:
        sql_script = f.read()

    conn = sqlite3.connect(DB_PATH)
    try:
        conn.executescript(sql_script)
        conn.commit()
        print(f"Banco criado/populado em: {DB_PATH}")
    finally:
        conn.close()

if __name__ == "__main__":
    init_db()
