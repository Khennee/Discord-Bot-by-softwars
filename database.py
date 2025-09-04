import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name="traydor.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS traydor_points (
                user_id TEXT PRIMARY KEY,
                username TEXT,
                points INTEGER DEFAULT 0
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS seasons (
                season_number INTEGER PRIMARY KEY,
                start_date TEXT
            )
        """)
        self.conn.commit()

    def add_points(self, user_id, username, points):
        cur = self.conn.cursor()
        cur.execute("""
            INSERT INTO traydor_points (user_id, username, points)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET points = points + excluded.points, username = excluded.username
        """, (user_id, username, points))
        self.conn.commit()
        return self.get_points(user_id)

    def get_points(self, user_id):
        cur = self.conn.cursor()
        cur.execute("SELECT points FROM traydor_points WHERE user_id = ?", (user_id,))
        row = cur.fetchone()
        return row[0] if row else 0

    def get_top(self, limit=10):
        cur = self.conn.cursor()
        cur.execute("SELECT username, points FROM traydor_points ORDER BY points DESC LIMIT ?", (limit,))
        return cur.fetchall()

    def reset_points(self):
        cur = self.conn.cursor()
        cur.execute("UPDATE traydor_points SET points = 0")
        self.conn.commit()

    def get_season_info(self):
        cur = self.conn.cursor()
        cur.execute("SELECT season_number, start_date FROM seasons ORDER BY season_number DESC LIMIT 1")
        row = cur.fetchone()
        if row:
            season_number, start_date = row
            if isinstance(start_date, str):
                start_date = datetime.fromisoformat(start_date)
            return season_number, start_date
        return None, None
    
    def new_season(self, season_number):
        cur = self.conn.cursor()
        start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        cur.execute(
            "INSERT INTO seasons (season_number, start_date) VALUES (?, ?)",
            (season_number, start_date.isoformat())
        )
        self.conn.commit()
