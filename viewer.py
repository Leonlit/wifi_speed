import matplotlib.pyplot as plt
from matplotlib.dates import date2num
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from dateutil import tz
import datetime as DT
import sqlite3

def getDataFromDB():
    try:
        conn = sqlite3.connect("wifi_speed.db")
        c = conn.cursor()
        c.execute("SELECT * FROM wifi_speed")
        rows = c.fetchall()
        return rows
    except sqlite3.DatabaseError as ex:
        print("Something went wrong when getting the data from the Database...")
        print(ex)

def constructGraph(uploads, downloads, dates):
    dates_D2N = [date2num(date) for date in dates]
    fig = plt.figure(num="Internet Speed")
    graph = fig.add_subplot()

    plt.subplots_adjust(bottom=0.15)
    graph.plot(dates_D2N, uploads, label="Upload speed")
    graph.plot(dates_D2N, downloads, label="Download speed")
    graph.set_xticks(dates_D2N)
    graph.set_xticklabels(
        [date.strftime("%H:%M:%S") for date in dates], rotation=45
    )

    plt.xlabel("Time")
    plt.ylabel("Speed in Mbps")
    plt.title("Internet Speed")
    plt.legend()
    plt.show()

def parseData(entries):
    dates = []
    uploads = []
    downloads = []
    for data in entries:
        uploads.append(data[0])
        downloads.append(data[1])
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        date = DT.datetime.strptime(data[2], "%Y-%m-%dT%H:%M:%S")
        date = date.replace(tzinfo=from_zone)
        date = date.astimezone(to_zone)
        dates.append(date)
    return (uploads, downloads, dates)

if __name__ == '__main__':
    entries = getDataFromDB()
    parsedData = parseData(entries)
    constructGraph(parsedData[0], parsedData[1], parsedData[2])
