# -*- coding: utf-8 -*-
"""AutomatingFileTransfer.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jIt5gj4MOGsWMHOOSrGu-pK2MNisrXlh
"""

import ftplib
import os
import shutil 
import datetime as dt
import schedule
import time

                             
class FtpTransferer:
    def __init__(self, ftp_host, ftp_user, ftp_pass, local_dir, current_dir):
        self.ftp_host = ftp_host
        self.ftp_user = ftp_user
        self.ftp_pass = ftp_pass
        self.local_dir = local_dir
        self.current_dir = current_dir
        self.ftp = ""

    def connect(self):
        try:
            self.ftp = ftplib.FTP(self.ftp_host)
            self.ftp.login(self.ftp_user, self.ftp_pass)
        except Exception as e:
            Logger("Error", e).write()

    def disconnect(self):
        self.ftp.quit()

    def transfer(self):
        if os.path.exists(self.local_dir):
            dir_list = []
            dir_list = self.ftp.nlst()

        ##If we uncomment this:

        #   file = 'readme.txt'
        #    with open(file, "wb") as f:
        #     self.ftp.retrbinary(f"RETR {file}", f.write)
        #     shutil.move(self.current_dir+'/'+file, self.local_dir+'/'+file)

        ## And comment this for, it used to work

            for file in dir_list:
                try:
                    print(file)
                    with open(file, "wb") as f:
                        self.ftp.retrbinary(f"RETR {file}", f.write)
                        shutil.move(self.current_dir+'/'+file, self.local_dir+'/'+file)
                        Logger("Info", file+' transfered').write()
                except Exception as e:
                    Logger("Error", e).write()
        else:
            Logger("Error","The path you provided does not exist").write()

class Logger:
    def __init__(self, log_type, message):
        self.log_type = log_type
        self.message = message

    def write(self):
        now = dt.datetime.now()
        files = os.listdir("TransferFilesLog/")
        if "log.csv" in files:
            with open("TransferFilesLog/log.csv", "a") as f:
                f.write(f"{now},{self.log_type},{self.message}\n")
        else:
            with open("TransferFilesLog/log.csv", "w") as f:
                f.write(f"{now},{self.log_type},{self.message}\n")

def main_func():
    ftp_host = "test.rebex.net"
    local_dir = ""  #your local dir
    current_dir = ""   #your current dir
    ftp_user = "demo"
    ftp_pass = "password"
    ftp_transferer = FtpTransferer(ftp_host, ftp_user, ftp_pass, local_dir, current_dir)
    ftp_transferer.connect()
    ftp_transferer.transfer()
    ftp_transferer.disconnect()

schedule.every().day.at("11:30").do(main_func)
while True:
    schedule.run_pending()
    time.sleep(1)