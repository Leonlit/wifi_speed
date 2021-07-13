import speedtest
import module.dbManagement as dbM
import collections

from module.logger import logToFile
from datetime import datetime

class SpeedMonitor():
    __db = None

    def __init__(self):
        self.__db = dbM.DBManagement()

    def real_time_monitor(self):
        output_template = {
            'downs': 0,
            'ups': 0,
            'time': str(datetime.now())
        }

        servers = []
        threads = None
        resultString = ""
        try:
            speed = speedtest.Speedtest()
            speed.get_servers(servers)
            speed.get_best_server()
            speed.download(threads=threads)
            speed.upload(threads=threads)
            speed.results.share()

            results_dict = speed.results.dict()
            
            data = int(results_dict['download']) / 1024 / 1000
            download = str("%.2f" % round(data, 2)) 
            resultString = "download: " + download

            data = int(results_dict['upload']) / 1024 / 1000
            upload = str("%.2f" % round(data, 2))
            resultString = resultString + ", upload: " + upload

            output_template['downs'] = download
            output_template['ups'] = upload
            self.__db.storeData(output_template)
            print(output_template)
            return output_template
        except speedtest.SpeedtestBestServerFailure as ex:
            msg = f"Failed to connect to the best Server, retrying...."
            print(msg)
            logToFile(msg, ex)
            return output_template
        except speedtest.ShareResultsConnectFailure as ex:
            msg = f"Time Out occured, re-trying"
            print(msg)
            logToFile(msg, ex)
            return output_template
        except Exception as ex:
            msg = f"Unknown error occured"
            print(msg, ex)
            logToFile(msg, ex)
            return output_template

    def get_pass_data(self):
        print("Refreshing", datetime.now())
        try:
            entries = self.__db.getData()               # get data from a sqlite3 db
            dates = []
            uploads = []
            downloads = []
            for data in entries:
                uploads.append(data[0])
                downloads.append(data[1])
                dates.append(data[2])
            dataTemplate = collections.namedtuple("data", ["uploads", "downloads", "dates"])
            data = dataTemplate(uploads, downloads, dates)
            return data
        except Exception as ex:
            logToFile(f"Error occured when plotting chart", ex)
            return