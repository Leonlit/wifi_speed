import sqlite3
from module.logger import log_to_file
from datetime import timedelta, datetime

class DBManagement:

    def construct_IP(self, ip):
        return str(ip.replace(".", "_"))

    def __init__(self, ip_addr):
        try:
            self.ip_addr = ip_addr
            self.tbName = self.construct_IP(ip_addr)
            self.conn = sqlite3.connect('wifi_speed.db')
            self.cursor = self.conn.cursor()
        except Exception as ex:
            log_to_file(f"unable to connect to database {self.tbName}", ex)
            if hasattr(ex, 'message'):
                print(ex.message)
            else:
                print(ex)

    def get_table_list(self):
        try:
            query = "select name from sqlite_master where type = 'table' and name not like 'SID_%';"
            self.cursor.execute(query)
            results = [name[0] for name in self.cursor.fetchall()]
            return results
        except Exception as ex:
            print(ex)
            log_to_file("Failed to get all tables name", ex)

    def create_table_if_not_exists(self):
        try:
            query = f"CREATE TABLE IF NOT EXISTS \"{self.tbName}\" (up real, down real, ping real, latency real, time timestamp, date timestamp)"
            self.cursor.execute(query)
            self.conn.commit()
        except Exception as ex:
            print(ex)
            log_to_file(f"Unable to create table ({self.tbName}) for the database", ex)

    def is_table_exists(self):
        try:
            query = f"SELECT name FROM sqlite_master WHERE type='table' AND name=\"{self.tbName}\""
            self.cursor.execute(query)
            if self.cursor.fetchone()[0]:
                return True
        except TypeError as ex:
            print()
            log_to_file("table does not exists", ex)
            return False
        except Exception as ex:
            print(ex)
            log_to_file("Error when checking if the table exists or not", ex)
        return False

    def close_connection(self):
        try:
            self.conn.close()
        except Exception as ex:
            log_to_file("Failed to close database connection", ex)
            if hasattr(ex, 'message'):
                print(ex.message)
            else:
                print(ex)

    def store_data(self, data):
        try:
            self.cursor.execute(f"INSERT INTO \"{self.tbName}\"  VALUES (?, ?, ?, ?, ?, ?)",
                                (data["down"], data["up"], data["ping"] , data["latency"],
                                data["time"], data["date"]))
            self.conn.commit()
        except sqlite3.DatabaseError as ex:
            log_to_file("Failed to write new data into table", ex)
            if hasattr(ex, 'message'):
                print(ex.message)
            else:
                print(ex)
            log_to_file(f"Error occured when inserting data into Database ({data})", ex)
        except Exception as ex:
            log_to_file(f"Unknown error occured", ex)

    def row_formatter(self, cursor, row):
        try:
            obj = {}
            for idx, column in enumerate(cursor.description):
                obj[column[0]] = row[idx]
            return obj
        except Exception as ex:
            log_to_file(f"Error occured when fomatting a single data from database. [{row}]", ex)
            if hasattr(ex, 'message'):
                print(ex.message)
            else:
                print(ex)

    # formatting the data from arrays to objects array
    def format_data (self, rows):
        try:
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
            
            if len(rows) != 0:
                result = {
                    "up": up,
                    "down": down,
                    "latency": latency,
                    "ping": ping,
                    "time": time,
                    "date": date,
                }
            else:
                result = {}
            return result
        except Exception as ex:
            if hasattr(ex, 'message'):
                print(ex.message)
            else:
                print(ex)
            log_to_file("Failed to convert all database content from row array to object array", ex)

    # getting all data and return an object/dictionary
    def get_all_data(self):
        try:
            if not self.is_table_exists():
                return None
            self.cursor.execute(f"SELECT * FROM \"{self.tbName}\"")
            rows = self.cursor.fetchall()
            results = self.format_data(rows)
            return results
        except sqlite3.DatabaseError as ex:
            log_to_file(f"Error occured when retrieving data from database", ex)
            print("Something went wrong when getting the data from the Database...")
            print(ex)

    # accept and value on how many data that's needed to be shown
    # 1 = 1 days, 3 = 3 days and so on, max is 30
    def get_filtered_data(self, value):
        try:
            print(value)
            limiter = str(datetime.now() - timedelta(hours = 24 * value))
            separator = limiter.split(" ")
            limiter_date = separator[0]
            limiter_time = separator[1].split(".")[0]
            if not self.is_table_exists():
                return None
            query = f"SELECT * FROM \"{self.tbName}\" WHERE (date = ? AND time >= ?) OR (date >= ?)"
            self.cursor.execute(query, (limiter_date, limiter_time, limiter_date))
            rows = self.cursor.fetchall()
            results = self.format_data(rows)
            print(results)
            return results
        except Exception as ex:
            log_to_file("Error when getting filtered data from database", ex)
            if hasattr(ex, 'message'):
                print(ex.message)
            else:
                print(ex)