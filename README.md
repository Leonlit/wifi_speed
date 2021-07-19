## Wifi Monitor
A simple wifi monitor with a somewhat beautiful web interface built with flask

## Setting up the project
Note that it's better for you to use a virtual environment for installing the packages\libraries required for this project

To setup the project, simply execute 
```
pip3 install -r requirements.txt
```
provided that you have pip/pip3 installed


## How to run the project
To run the project simply execute (after all packages/libaries has been downloaded)
```
python app.py
```

To run the project for all other devices in your network, use this command instead:
```
flask run  --host=0.0.0.0
```

## tech and tools used
 - The big three trio in building websites (HTML, CSS & JS)
 - Socket.io
 - Flask
 - SQLITE3