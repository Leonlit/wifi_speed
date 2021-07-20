from datetime import datetime
import sys, os

def log_to_file(msg, ex):
    lineEx = sys.exc_info()[-1].tb_lineno
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    msg = ("-" * 100) + "\n" + msg + f"[{datetime.now()}] ({exc_type}, {fname}, {lineEx})\n{ex}" + "\n" + ("-" * 100) + "\n"
    try:
        with open("error.log", "a") as file:
            file.write(msg)
    except IOError as ex:
        print("Error when logging error into log file")