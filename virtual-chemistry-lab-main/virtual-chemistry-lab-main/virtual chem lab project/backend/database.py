import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "lab.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS history (
    id TEXT PRIMARY KEY,
    user TEXT,
    chem_a TEXT,
    chem_b TEXT,
    result TEXT,
    description TEXT,
    safety TEXT,
    color TEXT,
    animation TEXT,
    created_at TEXT
);
"""

def get_conn():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_conn()
    conn.execute(SCHEMA)
    conn.commit()
    conn.close()

def insert_history(rec):
    conn = get_conn()
    conn.execute(
        """INSERT INTO history
           (id,user,chem_a,chem_b,result,description,safety,color,animation,created_at)
           VALUES (?,?,?,?,?,?,?,?,?,?)""",
        (
            rec["id"], rec["user"], rec["chemicals"][0], rec["chemicals"][1],
            rec["result"], rec["description"], rec["safety"],
            rec["color"], rec["animation"], rec["time"]
        )
    )
    conn.commit()
    conn.close()

def fetch_history():
    conn = get_conn()
    cur = conn.execute(
        "SELECT id,user,chem_a,chem_b,result,description,safety,color,animation,created_at "
        "FROM history ORDER BY datetime(created_at) DESC"
    )
    rows = cur.fetchall()
    conn.close()
    return [
        {
            "id": r[0],
            "user": r[1],
            "chemicals": [r[2], r[3]],
            "result": r[4],
            "description": r[5],
            "safety": r[6],
            "color": r[7],
            "animation": r[8],
            "time": r[9]
        }
        for r in rows
    ]

def fetch_history_by_id(rid):
    conn = get_conn()
    cur = conn.execute(
        "SELECT id,user,chem_a,chem_b,result,description,safety,color,animation,created_at "
        "FROM history WHERE id=?",
        (rid,)
    )
    r = cur.fetchone()
    conn.close()
    if not r:
        return None
    return {
        "id": r[0],
        "user": r[1],
        "chemicals": [r[2], r[3]],
        "result": r[4],
        "description": r[5],
        "safety": r[6],
        "color": r[7],
        "animation": r[8],
        "time": r[9]
    }
