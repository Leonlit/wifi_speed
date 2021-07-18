from module.dbManagement import DBManagement
import os
from time import sleep
from module.SpeedMonitor import SpeedMonitor

from flask_socketio import SocketIO, emit
from dotenv import load_dotenv
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)
load_dotenv()

initial = True
key = os.getenv('KEY')
app.config['SECRET_KEY'] = key
socketio = SocketIO(app)

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
        global initial
        monitor = SpeedMonitor()
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
    db = DBManagement()
    data = db.get_all_data()
    db.close_connection()
    emit("set_all_data", data )

# get certain range of data based on date and time
@socketio.on("get_filtered_data", namespace="/wifi_data")
def filter_wifi_data(value):
    db = DBManagement()
    value = value
    if value == 0:
        data = db.get_all_data()
    else:
        data = db.get_filtered_data(value)
    db.close_connection()
    emit("set_filtered_data", (data, value))


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
        app.run()
    except KeyboardInterrupt:
        print("Exiting the program.")
