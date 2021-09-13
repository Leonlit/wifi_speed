import sqlite3
from module.logger import log_to_file

class IPManagement:

    def __init__(self):
        try:
            self.conn = sqlite3.connect('wifi_speed.db')
            self.cursor = self.conn.cursor()
            self.create_table_if_not_exists()
        except Exception as ex:
            log_to_file(f"unable to connect to database {self.tbName}", ex)
            if hasattr(ex, 'message'):
                print(ex.message)
            else:
                print(ex)

    def create_table_if_not_exists(self):
        try:
            query = f"CREATE TABLE IF NOT EXISTS SID_IP (SID TEXT, IP TEXT)"
            self.cursor.execute(query)
            self.conn.commit()
        except Exception as ex:
            print(ex)
            log_to_file(f"Unable to create table (SID_IP) for the database", ex)

    def store_ip_address(self, sid, ip_addr):
        try:
            self.cursor.execute("INSERT INTO SID_IP VALUES (?, ?)", (sid, ip_addr))
            self.conn.commit()
            return True
        except sqlite3.DatabaseError as ex:
            print("Failed to write new data into table")
            if hasattr(ex, 'message'):
                print(ex.message)
            else:
                print(ex)
            log_to_file(f"Error occured when inserting data into Database ({sid}, {ip_addr})", ex)
        except Exception as ex:
            log_to_file(f"Unknown error occured", ex)
        return False

    def get_sid_ip(self, sid):
        try:
            query = "select IP from SID_IP where SID = ?"
            self.cursor.execute(query, (sid,))
            result = self.cursor.fetchone()
            print(result)
            if result is None:
                return False
            else:
                return result[0]
        except Exception as ex:
            print(ex)
            log_to_file(f"Failed to get IP address for {sid}", ex)

    def delete_sip_ip(self, sid):
        try:
            query = "DELETE from SID_IP where SID = ?"
            self.cursor.execute(query, (sid,))
            self.conn.commit()
            if self.cursor.rowcount < 1:
                return False
            else:
                return True
        except Exception as ex:
            print(ex)
            log_to_file(f"Failed to get IP address for {sid}", ex)

    def close_connection(self):
        try:
            self.conn.close()
        except Exception as ex:
            log_to_file("Failed to close database connection", ex)
            if hasattr(ex, 'message'):
                print(ex.message)
            else:
                print(ex)