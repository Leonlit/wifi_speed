import speedtest
import module.dbManagement as dbM

from module.logger import log_to_file
from datetime import datetime

class SpeedMonitor():
    __db = None

    def __init__(self, ip_addr):
        self.ip_addr = ip_addr

    def real_time_monitor(self):
        time = str(datetime.now()).split(".")[0]
        time = time.split(" ")
        output_template = {
            'down': 0,
            'up': 0,
            'time': time[1],
            'date': time[0],
            'ping': 0,
            'latency': 0,
            'ip_addr': self.ip_addr
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

            output_template['down'] = download
            output_template['up'] = upload
            output_template['ping'] = ping
            output_template['latency'] = latency

            print("client ip", self.ip_addr)

            self.__db = dbM.DBManagement(self.ip_addr)
            self.__db.create_table_if_not_exists()
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