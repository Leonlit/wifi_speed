import sqlite3
from module.logger import logToFile

class DBManagement:

    def __init__(self):
        self.conn = sqlite3.connect('wifi_speed.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS wifi_speed
                        (ups real, downs real, time timestamp)''')
        self.conn.commit()

    def storeData(self, data):
        try:
            self.cursor.execute("INSERT INTO wifi_speed VALUES ({ups},{downs},'{time}')".
                                format(downs=data["downs"], ups=data["ups"],
                                    time=data["time"]))
            self.conn.commit()
        except sqlite3.DatabaseError as ex:
            logToFile(f"Error occured when inserting data into Database ({data})", ex)
        except Exception as ex:
            logToFile(f"Unknown error occured", ex)

    def getData(self):
        try:
            self.cursor.execute("SELECT * FROM wifi_speed")
            rows = self.cursor.fetchall()
            return rows
        except sqlite3.DatabaseError as ex:
            logToFile(f"Error occured when retrieving data from database", ex)
            print("Something went wrong when getting the data from the Database...")
            print(ex)