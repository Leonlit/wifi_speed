from datetime import datetime

def logToFile(msg, ex):
    msg = ("-" * 100) + "\n" + msg + f"[{datetime.now()}]\n{ex}" + "\n" + ("-" * 100)
    try:
        with open("error.log", "a") as file:
            file.write(msg)
    except IOError as ex:
        print("Error when logging error into log file")