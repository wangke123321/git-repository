import time
import json
import os
import datetime
from datetime import datetime, timedelta
from common.log import Log


class RandomInfo:
    publicDict = {}

    def __init__(self):
        self.publicDict["date"] = str(datetime.today())
        self.publicDict["time"] = str(round(time.time() * pow(10, 3)))
        self.publicDict["today"] = (datetime.today()).strftime("%d-%h-%Y")
        self.publicDict["today+six"] =(datetime.today() + timedelta(days=6)).strftime("%d-%h-%Y")
        self.publicDict["today-six"] =(datetime.today() + timedelta(days=-6)).strftime("%d-%h-%Y")


class FileOperate:
    def __init__(self):
        self.log = Log()

    def writefile(self, file, filetype, filecontent, mode):
        if filetype in ("json", "txt", "csv"):
            filedir = os.path.dirname(file)
            os.makedirs(filedir, exist_ok=True)
            if mode == "a+":
                try:
                    fileobj = open(file, "a+", encoding="utf-8")
                    fileobj.write(filecontent + "\n")
                    return fileobj
                except IOError:
                    self.log.logMsg(3, "file open fail,%s file not exist" % file)
                    return None
            elif mode == "r+":
                try:
                    fileobj = open(file, "r+", encoding="utf-8")
                    old = fileobj.read()
                    fileobj.seek(0)
                    fileobj.write(filecontent)
                    fileobj.write(old)
                    return fileobj
                except IOError:
                    self.log.logMsg(3, "file open fail,%s file not exist" % file)
                    return None

    def readfile(self, filepath, filetype):
        if filetype == "json":
            try:
                with open(filepath, "r", encoding="UTF-8-sig") as jsonfile:
                    json_file = json.load(jsonfile)
                return json_file
            except IOError:
                self.log.logMsg(3, "file open fail,%s file not exist" % filepath)
                return None
        elif filetype == "txt":
            try:
                with open(filepath, "r", encoding="UTF-8-sig") as txtfile:
                    return txtfile
            except IOError:
                self.log.logMsg(3, "file open fail,%s file not exist" % filepath)
                return None

    def deletefile(self, filepath):
        files = os.listdir(filepath)
        if files is None:
            pass
        else:
            for file in files:
                dir_file_path = os.path.join(filepath, file)
                os.remove(dir_file_path)