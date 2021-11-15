import os
import time
import requests
import re
# from loguru import logger
import datetime
import subprocess
import ctypes, sys


def startServer(path,url):
    '''
    :param path: 服务路径
    :param url: 对应服务url
    :return:
    '''
    pt = subprocess.Popen(path, stdout=subprocess.PIPE)
    pt.wait(timeout=10)
    getTomcatName = subprocess.Popen('tasklist | findstr java.exe',shell=True,stdout=subprocess.PIPE).stdout.readlines()
    killPid = 'taskkill /PID ' + str(getTomcatName)[8:37]
    while True:
        requestStatus = requests.get(url=url)
        if re.search('java.exe', str(getTomcatName)[3:11]) and requestStatus.status_code == 404:
            print('tomcat 启动成功')
            # logger.info('tomcat 启动成功')
            break
        else:
            subprocess.Popen('taskkill /F /IM java.exe')
            pt
            time.sleep(5)
            # logger.info('tomcat 启动异常执行，重新启动')
            print('tomcat 启动异常执行，重新启动')

def shutdown():
    subprocess.Popen('taskkill /F /IM java.exe',shell=True,stdout=subprocess.PIPE)
    time.sleep(2)
    getTomcatName = subprocess.Popen('tasklist | findstr java.exe',
                                     shell=True,
                                     stdout=subprocess.PIPE
                                     ).stdout.readlines()
    print(getTomcatName)
    # logger.info(getTomcatName)
    if not getTomcatName:
        # logger.info('对应服务进程不存在，成功kill')
        print('对应服务进程不存在，成功kill')

if __name__ == '__main__':
    path = 'd: && cd D:\\apache-tomcat-7.0.88-8081\\bin && startup.bat'
    url = '127.0.0.1:8081'
    startServer(path, url)