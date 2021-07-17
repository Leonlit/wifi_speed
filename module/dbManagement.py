import sqlite3
from module.logger import log_to_file
from datetime import timedelta, datetime

class DBManagement:

    def __init__(self):
        self.conn = sqlite3.connect('wifi_speed.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS wifi_speed
                        (up real, down real, ping real, latency real, time timestamp, date timestamp)''')
        self.conn.commit()

    def close_connection(self):
        self.conn.close()

    def store_data(self, data):
        try:
            self.cursor.execute("INSERT INTO wifi_speed VALUES ({up}, {down}, {ping}, {latency},'{time}', '{date}')".
                                format(down=data["down"], up=data["up"], ping=data["ping"] , latency=data["latency"],
                                time=data["time"], date=data["date"]))
            self.conn.commit()
        except sqlite3.DatabaseError as ex:
            log_to_file(f"Error occured when inserting data into Database ({data})", ex)
        except Exception as ex:
            log_to_file(f"Unknown error occured", ex)

    def row_formatter(self, cursor, row):
        obj = {}
        for idx, column in enumerate(cursor.description):
            obj[column[0]] = row[idx]
        return obj

    def format_data (self, rows):
        up = []
        down = [] 
        ping = []
        latency = []
        time = []
        date = []
        for row in rows:
            newData = self.row_formatter(self.cursor, row)
            up.append(newData["up"])
            down.append(newData["down"])
            ping.append(newData["ping"])
            latency.append(newData["latency"])
            time.append(newData["time"])
            date.append(newData["date"])
        return {
            "up": up,
            "down": down,
            "latency": latency,
            "ping": ping,
            "time": time,
            "date": date,
        }

    def get_all_data(self):
        try:
            self.cursor.execute("SELECT * FROM wifi_speed")
            rows = self.cursor.fetchall()
            results = self.format_data(rows)
            return results
        except sqlite3.DatabaseError as ex:
            log_to_file(f"Error occured when retrieving data from database", ex)
            print("Something went wrong when getting the data from the Database...")
            print(ex)

    def get_filtered_data(self, value):
        limiter = str(datetime.now() - timedelta(hours = 24 * value))
        separator = limiter.split(" ")
        limiter_date = separator[0]
        limiter_time = separator[1].split(".")[0]
        query = "SELECT * FROM wifi_speed WHERE ('date' >= ? AND 'time' >= ?) OR ('date' = ?) "
        self.cursor.execute(query, (limiter_date, limiter_time, str(datetime.now()).split(" ")[0]))
        rows = self.cursor.fetchall()
        results = self.format_data(rows)
        return results