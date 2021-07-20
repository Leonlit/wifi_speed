from module.logger import log_to_file
from module.dbManagement import DBManagement
from module.SpeedMonitor import SpeedMonitor
from module.logger import log_to_file

import os, re

from time import sleep
from json import load
from urllib.request import urlopen
from urllib.error import HTTPError, URLError

from flask_socketio import SocketIO, emit
from dotenv import load_dotenv
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)
load_dotenv()

initial = True
key = os.getenv('KEY')
app.config['SECRET_KEY'] = key
socketio = SocketIO(app)

def check_ip (ip):
    return re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",ip)

def get_ip_addr(case):
    if case > 3 or case is None:
        raise Exception("Could not get public IP for a device")
    case = str(case)
    try:
        return {
            '0': urlopen("http://ip.42.pl/raw").read().decode("utf-8"),
            '1': load(urlopen('http://jsonip.com'))['ip'],
            '2': load(urlopen('http://httpbin.org/ip'))['origin'],
            '3': load(urlopen('https://api.ipify.org/?format=json'))['ip']
        }[case]
    except HTTPError as ex:
        print(ex)
        log_to_file("Data not retrieved because %s\nURL: %s", ex)
    except URLError as ex:
        print(ex)
        log_to_file("Some error occured when trying to discover the public ip address of the ip address", ex)
    except ValueError as ex:
        print(ex)
        log_to_file("Error while parsing the JSON data", ex)
    except Exception as ex:
        log_to_file(str(ex), ex)
    return get_ip_addr(case + 1)


# Web Routes 
@app.route('/')
def home_page():
    return render_template("index.html")

@app.route('/history/')
def history_page():
    return render_template("history.html")

# socket function to run another speedtest on the wifi
@socketio.on("new_wifi_data", namespace="/wifi_data")
def wifi_data():
    timer = 30
    try:
        ip_addr = get_ip_addr(0)
        if not ip_addr:
            return 
        global initial
        monitor = SpeedMonitor(ip_addr)
        data = monitor.real_time_monitor()
        if not initial:
            sleep(timer)
        initial = False
        emit("new_data", data)
    except Exception as ex:
        print("Something broke")
        print(ex)

# get all data for the wifi monitor
@socketio.on("get_all_data", namespace="/wifi_data")
def all_wifi_data():
    ip_addr = get_ip_addr(0)
    if not ip_addr:
        return 
    db = DBManagement(ip_addr)
    data = db.get_all_data()
    db.close_connection()
    emit("set_all_data", data)

# get the list of tables
@socketio.on("get_table_list", namespace="/wifi_data")
def get_list():
    ip_addr = get_ip_addr(0)
    if not ip_addr:
        return
    db = DBManagement(ip_addr)
    results = db.get_table_list()
    db.close_connection()
    emit("set_table_list", results)

# get certain range of data based on date and time
@socketio.on("get_filtered_data", namespace="/wifi_data")
def filter_wifi_data(data):
    try:
        if not data["ip_addr"]:
            ip_addr = get_ip_addr(0)
            if not ip_addr:
                return
        else:
            ip_addr = data["ip_addr"]
        if not check_ip(ip_addr):
            raise ValueError(f"User provided a wrong ip address{ip_addr}") 
        db = DBManagement(ip_addr)
        data = data
        if data == 0:
            data = db.get_all_data()
        else:
            result = db.get_filtered_data(data["value"])
        db.close_connection()
        emit("set_filtered_data", (result, data["value"], ip_addr))
    except ValueError as ex:
        log_to_file(str(ex), ex)
        print(ex)


# for providing js, css, media file and as well as media files
@app.route('/js/<path:path>')
def route_JS_File(path):
    return send_from_directory('assets/js', path)

@app.route('/css/<path:path>')
def route_CSS_File(path):
    return send_from_directory('assets/css', path)

@app.route('/icon/<path:path>')
def route_Image_File(path):
    return send_from_directory('assets/icon', path)

@app.route('/external/<path:path>')
def route_External_File(path): 
    return send_from_directory('assets/external', path)

if __name__ == '__main__':
    try:
        app.run(debug=True)
    except KeyboardInterrupt:
        print("Exiting the program.")
