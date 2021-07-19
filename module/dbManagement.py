import sqlite3
from module.logger import log_to_file
from datetime import timedelta, datetime

class DBManagement:

    def constructIP(self, ip):
        return ip.replace(".", "_")

    def __init__(self, ip_addr):
        try:
            self.ip_addr = ip_addr
            self.conn = sqlite3.connect('wifi_speed.db')
            self.cursor = self.conn.cursor()
            query = '''CREATE TABLE IF NOT EXISTS {ip_addr}
                            (up real, down real, ping real, latency real, time timestamp, date timestamp)'''.format(ip_addr=ip_addr)
            self.cursor.execute(query)
            self.conn.commit()
        except Exception as ex:
            log_to_file(f"unable to connect to database {self.constructIP(ip_addr)}", ex)
            if hasattr(ex, 'message'):
                print(ex.message)
            else:
                print(ex)

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
            ip = self.ip_addr
            self.cursor.execute("INSERT INTO %s VALUES (?, ?, ?, ?, ?, ?)" % self.constructIP(ip),
                                (data["down"], data["up"], data["ping"] , data["latency"],
                                data["time"], data["date"]))
            self.conn.commit()
        except sqlite3.DatabaseError as ex:
            print("Failed to write new data into table")
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
            
            return {
                "up": up,
                "down": down,
                "latency": latency,
                "ping": ping,
                "time": time,
                "date": date,
            }
        except Exception as ex:
            if hasattr(ex, 'message'):
                print(ex.message)
            else:
                print(ex)
            log_to_file("Failed to convert all database content from row array to object array", ex)

    # getting all data and return an object/dictionary
    def get_all_data(self):
        try:
            self.cursor.execute("SELECT * FROM {ip_addr}".format(ip_addr=self.constructIP(self.ip_addr)))
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
<<<<<<< HEAD
<<<<<<< Updated upstream
        limiter = str(datetime.now() - timedelta(hours = 24 * value))
        separator = limiter.split(" ")
        limiter_date = separator[0]
        limiter_time = separator[1].split(".")[0]
        query = "SELECT * FROM wifi_speed WHERE ('date' >= ? AND 'time' >= ?) OR ('date' = ?) "
        
        self.cursor.execute(query, (limiter_date, limiter_time, str(datetime.now()).split(" ")[0]))
        rows = self.cursor.fetchall()
        results = self.format_data(rows)

=======
=======
>>>>>>> main
        try:
            limiter = str(datetime.now() - timedelta(hours = 24 * value))
            separator = limiter.split(" ")
            limiter_date = separator[0]
            limiter_time = separator[1].split(".")[0]
<<<<<<< HEAD
            query = "SELECT * FROM ? WHERE ('date' >= ? AND 'time' >= ?) OR ('date' = ?) "
            
            self.cursor.execute(query, (self.constructIP(self.ip_addr), limiter_date, limiter_time, str(datetime.now()).split(" ")[0]))
            rows = self.cursor.fetchall()
            results = self.format_data(rows)
        except Exception as ex:
            log_to_file("Error when getting filtered data from database", ex)
            if hasattr(ex, 'message'):
                print(ex.message)
            else:
                print(ex)
>>>>>>> Stashed changes
=======
            query = "SELECT * FROM wifi_speed WHERE ('date' >= ? AND 'time' >= ?) OR ('date' = ?) "
            
            self.cursor.execute(query, (limiter_date, limiter_time, str(datetime.now()).split(" ")[0]))
            rows = self.cursor.fetchall()
            results = self.format_data(rows)
        except Exception as ex:
            print(ex.message)
>>>>>>> main
        return results