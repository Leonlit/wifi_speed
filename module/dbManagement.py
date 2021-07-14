import sqlite3
from module.logger import log_to_file

class DBManagement:

    def __init__(self):
        self.conn = sqlite3.connect('wifi_speed.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS wifi_speed
                        (up real, down real, time timestamp)''')
        self.conn.commit()

    def store_data(self, data):
        try:
            self.cursor.execute("INSERT INTO wifi_speed VALUES ({up},{down},'{time}')".
                                format(down=data["down"], up=data["up"],
                                    time=data["time"]))
            self.conn.commit()
        except sqlite3.DatabaseError as ex:
            log_to_file(f"Error occured when inserting data into Database ({data})", ex)
        except Exception as ex:
            log_to_file(f"Unknown error occured", ex)

    def get_data(self):
        try:
            self.cursor.execute("SELECT * FROM wifi_speed")
            rows = self.cursor.fetchall()
            return rows
        except sqlite3.DatabaseError as ex:
            log_to_file(f"Error occured when retrieving data from database", ex)
            print("Something went wrong when getting the data from the Database...")
            print(ex)