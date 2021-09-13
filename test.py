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


# Web Routes 
@app.route('/')
def home_page():
    print(urlopen("http://ip.42.pl/raw").read().decode("utf-8"))
    print(load(urlopen('http://httpbin.org/ip'))['origin'])
    return "<h1>test</h1>"

if __name__ == '__main__':
    try:
        app.run(debug=False, host="0.0.0.0")
        
    except KeyboardInterrupt:
        print("Exiting the program.")
 