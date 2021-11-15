import subprocess
import requests
import logging.config
from logging import info

def startServer(path,url=None):
    '''
    :param path: 服务路径
    :param url: 对应服务url
    :return:
    '''
    pt = subprocess.Popen(path, stdout=subprocess.PIPE)
    pt.wait(timeout=10)
    # getTomcatName = subprocess.Popen('tasklist | findstr java.exe',shell=True,stdout=subprocess.PIPE).stdout.readlines()
    # killPid = 'taskkill /PID ' + str(getTomcatName)[8:37]
    while True:
        requestStatus = requests.get(url=url)
        # if re.search('java.exe',str(getTomcatName)[3:11]) and requestStatus.status_code == 404:
        if requestStatus.status_code == 200:
            logger.info('tomcat 启动成功')
            break
    path = r'D:\TestFiles\tomcat\apache-tomcat-7.0.88-2\bin\8877.bat'
    url = 'http://192.168.37.225:8877/PosMerchant'
    startServer(path, url)