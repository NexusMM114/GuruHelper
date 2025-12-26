import sqlite3

db = sqlite3.connect("rose.db", check_same_thread=False)
cur = db.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS warns (
    user_id INTEGER,
    chat_id INTEGER,
    count INTEGER
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS notes (
    chat_id INTEGER,
    name TEXT,
    content TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS filters (
    chat_id INTEGER,
    word TEXT
)
""")

db.commit()
