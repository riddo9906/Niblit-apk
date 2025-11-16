# memory.py
import sqlite3
import json
import time
from typing import List, Tuple

DB_FILE = "niblit_memory.db"

class MemoryStore:
    def __init__(self, db_path=DB_FILE):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._init_tables()

    def _init_tables(self):
        c = self.conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS facts(
                        id INTEGER PRIMARY KEY,
                        key TEXT,
                        value TEXT,
                        tags TEXT,
                        ts INTEGER
                    )""")
        c.execute("""CREATE TABLE IF NOT EXISTS history(
                        id INTEGER PRIMARY KEY,
                        session TEXT,
                        role TEXT,
                        content TEXT,
                        ts INTEGER
                    )""")
        self.conn.commit()

    def add_fact(self, key: str, value: str, tags: List[str]=None):
        tags = json.dumps(tags or [])
        ts = int(time.time())
        c = self.conn.cursor()
        c.execute("INSERT INTO facts(key,value,tags,ts) VALUES(?,?,?,?)", (key, value, tags, ts))
        self.conn.commit()

    def get_facts(self, limit=50) -> List[Tuple]:
        c = self.conn.cursor()
        c.execute("SELECT key,value,tags,ts FROM facts ORDER BY ts DESC LIMIT ?", (limit,))
        return c.fetchall()

    def forget_fact(self, key):
        c = self.conn.cursor()
        c.execute("DELETE FROM facts WHERE key = ?", (key,))
        self.conn.commit()

    def add_message(self, session: str, role: str, content: str):
        ts = int(time.time())
        c = self.conn.cursor()
        c.execute("INSERT INTO history(session,role,content,ts) VALUES(?,?,?,?)", (session,role,content,ts))
        self.conn.commit()

    def get_recent_history(self, session: str, limit=20) -> List[Tuple]:
        c = self.conn.cursor()
        c.execute("SELECT role,content,ts FROM history WHERE session=? ORDER BY ts DESC LIMIT ?", (session, limit))
        rows = c.fetchall()
        return list(reversed(rows))  # return oldest->newest