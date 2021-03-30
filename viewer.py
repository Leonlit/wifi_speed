import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.dates import date2num
from dateutil import tz
import datetime as DT
import sqlite3
from time import sleep

conn = sqlite3.connect("wifi_speed.db")
cursor = conn.cursor()

def getDataFromDB():
    try:
        cursor.execute("SELECT * FROM wifi_speed")
        rows = cursor.fetchall()
        return rows
    except sqlite3.DatabaseError as ex:
        print("Something went wrong when getting the data from the Database...")
        print(ex)

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

def realTimeGraph(dummy):
    print("Refreshing", DT.datetime.now())
    entries = getDataFromDB()       # get data from a sqlite3 db
    parsedData = parseData(entries) # separating the data & formatting them
    uploads = parsedData[0]
    downloads = parsedData[1]
    dates = parsedData[2]

    dates_D2N = [date2num(date) for date in dates]
    
    plt.cla()
    ax.plot(dates_D2N, uploads, label="Upload speed")
    ax.plot(dates_D2N, downloads, label="Download speed")
    ax.set_xticks(dates_D2N)
    ax.set_xticklabels(
        [date.strftime("%H:%M:%S") for date in dates], rotation=45
    )
    ax.set_xlabel("Time", fontsize=10)
    ax.set_ylabel("Speed in Mbps", fontsize=10)
    ax.set_title("Internet Speed")
    ax.legend()
    plt.subplots_adjust(bottom=0.15)

if __name__ == '__main__':
    fig, ax = plt.subplots(num="Internet Speed")
    ani = FuncAnimation(plt.gcf(), realTimeGraph, interval=20000)
    plt.show()