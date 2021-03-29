import time
import sqlite3
import speedtest

from datetime import datetime, timedelta

def logToFile(msg):
    msg = ("-" * 100) + "\n" + msg + "\n" + ("-" * 100)
    try:
        with open("error.log", "a") as file:
            file.write(msg)
    except IOError as ex:
        print("Error when logging error into log file")

class SpeedMonitor():

    def __init__(self):
        self.conn = sqlite3.connect('wifi_speed.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS wifi_speed
                     (ups real, downs real, time timestamp)''')
        self.conn.commit()

    def speedTester(self):
        servers = []
        threads = None
        resultString = ""
        try:
            speed = speedtest.Speedtest()
            speed.get_servers(servers)
            speed.get_best_server()
            speed.download(threads=threads)
            speed.upload(threads=threads)
            speed.results.share()

            results_dict = speed.results.dict()
            
            data = int(results_dict['download']) / 1024 / 1000
            download = str("%.2f" % round(data, 2)) 
            resultString = "download: " + str(data)

            data = int(results_dict['upload']) / 1024 / 1000
            upload = str("%.2f" % round(data, 2))
            resultString = resultString + ", upload: " + str(data)
            
            time = results_dict['timestamp'].split('.')[0]

            print(resultString, time)
            output = {'downs': download,
                    'ups': upload,
                    'time': time}
            return output
        except speedtest.SpeedtestBestServerFailure as ex:
            msg = f"Failed to connect to the best Server, retrying.... [{datetime.now()}]\n{ex}"
            print(msg)
            logToFile(msg)
            self.speedTester()
        except speedtest.ShareResultsConnectFailure as ex:
            msg = f"time Out occured, re-trying [{datetime.now()}]\n{ex}"
            print(msg)
            logToFile(msg)
            self.speedTester()
        except Exception as ex:
            msg = f"Unknown error occured [{datetime.now()}]\n{ex}"
            print(msg)
            logToFile(msg)
            self.speedTester()

    def storeData(self, data):
        try:
            self.cursor.execute("INSERT INTO wifi_speed VALUES ({downs},{ups},'{time}')".
                                format(downs=data["downs"], ups=data["ups"],
                                    time=data["time"]))
            self.conn.commit()
        except sqlite3.DatabaseError as ex:
            logToFile(f"Error occured when inserting data into Database ({data}) [{datetime.now()}]\n{ex}")
        except Exception as ex:
            logToFile(f"Unknown error occured [{datetime.now()}]\n{ex}")

    def runner(self):
        try:
            while True:
                data = self.speedTester()
                self.storeData(data)
                print("Sleeping for 60 seconds")
                time.sleep(60)
        except KeyboardInterrupt:
            print("exiting, hope the internet connection was great ;D")

if __name__ == '__main__':
    speed_find = SpeedMonitor()
    speed_find.runner()