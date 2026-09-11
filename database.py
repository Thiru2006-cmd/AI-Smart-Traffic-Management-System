import sqlite3
from datetime import datetime


class TrafficDatabase:

    def __init__(self):
        self.connection = sqlite3.connect("traffic.db", check_same_thread=False)
        self.cursor = self.connection.cursor()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS traffic_data(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            timestamp TEXT,

            cars INTEGER,

            buses INTEGER,

            trucks INTEGER,

            motorcycles INTEGER,

            total INTEGER,

            traffic_level TEXT,

            green_signal INTEGER
        )
        """)

        self.connection.commit()

    def save_data(self,
                  cars,
                  buses,
                  trucks,
                  motorcycles,
                  total,
                  traffic_level,
                  green_signal):

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.cursor.execute("""
        INSERT INTO traffic_data
        (timestamp,cars,buses,trucks,motorcycles,total,traffic_level,green_signal)

        VALUES(?,?,?,?,?,?,?,?)
        """,

        (
            current_time,
            cars,
            buses,
            trucks,
            motorcycles,
            total,
            traffic_level,
            green_signal
        ))

        self.connection.commit()