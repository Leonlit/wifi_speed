import os

from module.SpeedMonitor import SpeedMonitor
from module.utilities import getIP

from flask_socketio import SocketIO, emit
from dotenv import load_dotenv
from flask import Flask, render_template, send_from_directory, request

app = Flask(__name__)
load_dotenv()

key = os.getenv('KEY')
app.config['SECRET_KEY'] = key
socketio = SocketIO(app)

@app.route('/')
def home_page():
    ip = getIP()
    return render_template("index.html", ipAddr=ip)

@socketio.on("new_wifi_data", namespace="/wifi_data")
def wifi_data():
    try:
        monitor = SpeedMonitor()
        data = monitor.real_time_monitor()
        emit("new_data", data)
    except Exception as ex:
        print("Something broke")
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
        app.run(debug = True)
    except KeyboardInterrupt:
        print("Exiting the program.")
