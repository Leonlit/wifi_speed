import os
from time import sleep

from module.SpeedMonitor import SpeedMonitor
from module.utilities import getIP

from flask_socketio import SocketIO, emit
from dotenv import load_dotenv
from flask import Flask, render_template, send_from_directory, request

app = Flask(__name__)
load_dotenv()

key = os.getenv('KEY')
app.config['SECRET_KEY'] = key
socketio = SocketIO(app, logger=True)

@app.route('/')
def home_page():
    ip = getIP()
    runner()
    return render_template("index.html", ipAddr=ip)

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

def runner():
    timer = 30
    try:
        monitor = SpeedMonitor()
        while True:
            data = monitor.real_time_monitor()
            print(data)
            emit("new_wifi_data",data)
            sleep(timer)
    except:
        print("exiting, hope the internet connection was great ;D")

if __name__ == '__main__':
    try:
        print(request.host_url)
        app.run(debug = False)
    except KeyboardInterrupt:
        print("Exiting the program.")
