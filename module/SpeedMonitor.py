import speedtest
import module.dbManagement as dbM
import collections

from module.logger import log_to_file
from datetime import datetime

class SpeedMonitor():
    __db = None

    def real_time_monitor(self):
        time = str(datetime.now()).split(".")[0]
        time = time.split(" ")
        output_template = {
            'down': 0,
            'up': 0,
            'time': time[1],
            'date': time[0],
            'ping': 0,
            'latency': 0
        }

        servers = []
        threads = None
        # resultString = ""
        try:
            speed = speedtest.Speedtest()
            speed.get_servers(servers)
            speed.get_best_server()
            speed.download(threads=threads)
            speed.upload(threads=threads)
            speed.results.share()

            results_dict = speed.results.dict()
            print(results_dict)

            data = int(results_dict['download']) / 1024 / 1000
            download = str("%.2f" % round(data, 2)) 
            # resultString = "download: " + download

            data = int(results_dict['upload']) / 1024 / 1000
            upload = str("%.2f" % round(data, 2))
            # resultString = resultString + ", upload: " + upload

            data = int(results_dict["ping"])
            ping = str("%.2f" % round(data, 2))
            # resultString = resultString + ", ping: " + ping

            data = int(results_dict["server"]["latency"])
            latency = str("%.2f" % round(data, 2))
            # resultString = resultString + ", latency: " + ping

            print(resultString)
            output_template['down'] = download
            output_template['up'] = upload
            output_template['ping'] = ping
            output_template['latency'] = latency

            ip_addr = results_dict["client"]["ip"]

            print("client ip", ip_addr)

            self.__db = dbM.DBManagement(ip_addr)
            self.__db.store_data(output_template)
            self.__db.close_connection()
            return output_template
        except speedtest.SpeedtestBestServerFailure as ex:
            msg = f"Failed to connect to the best Server, retrying...."
            print(msg)
            log_to_file(msg, ex)
            return output_template
        except speedtest.ShareResultsConnectFailure as ex:
            msg = f"Time Out occured, re-trying"
            print(msg)
            log_to_file(msg, ex)
            return output_template
        except Exception as ex:
            msg = f"Unknown error occured"
            print(msg, ex)
            log_to_file(msg, ex)
            return output_template

    def get_pass_data(self):
        print("Refreshing", datetime.now())
        try:
            entries = self.__db.get_data()               # get data from a sqlite3 db
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
            log_to_file(f"Error occured when plotting chart", ex)
            return