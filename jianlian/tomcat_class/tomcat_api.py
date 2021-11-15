import subprocess
import time
from jianlian.timeclass.class_time import DateTime
import requests


def startServer(path):
    pt = subprocess.Popen(path, stdout=subprocess.PIPE, shell=True, encoding="utf-8")
    pt.wait(timeout=30)
    res = 'tasklist | findstr java.exe'
    subprocess.Popen(res, shell=True, stdout=subprocess.PIPE).stdout.readlines()
    # requestStatus = Request().request()
    # print(requestStatus)
    # if requestStatus == 200:
    #     print("启动成功")

def shutdown(path):
    time.sleep(5)
    # subprocess.Popen('taskkill /F /IM java.exe', shell=True, stdout=subprocess.PIPE)
    pt = subprocess.Popen(path, stdout=subprocess.PIPE, shell=True, encoding="utf-8")
    pt.wait(timeout=30)


def to_shutdown():
    time.sleep(5)
    subprocess.Popen('taskkill /F /IM java.exe', shell=True, stdout=subprocess.PIPE)
    # pt = subprocess.Popen(path, stdout=subprocess.PIPE, shell=True, encoding="utf-8")
    # pt.wait(timeout=30)




if __name__ == '__main__':
    # path =r"D:\apache-tomcat-7.0.68-8080-11\bin\startup.bat"
    # path = 'd: && cd D:\\apache-tomcat-7.0.88-8081\\bin && startup.bat'
    # path = 'date ' + DateTime().random_dates(1)
    # path = 'date 2021-09-24'
    path = 'd: && cd D:\\apache-tomcat-7.0.88-8081\\bin && shutdown.bat'
    # startServer(path)
    shutdown(path)
