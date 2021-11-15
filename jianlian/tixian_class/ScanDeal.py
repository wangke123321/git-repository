from datetime import datetime
from jianlian.project_path.project_path import *
from jianlian.class_oracle.oracle_dome import *
import pandas as pd
import requests
import hashlib
import random
import time
# 设置显示的最大列、宽等参数，消掉打印不完全中间的省略号
# pd.set_option('display.max_columns', 1000)
# pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)


def get_md5(md5_):
    md5 = hashlib.md5()  # 1-实例化加密对象
    md5.update(md5_.encode('utf-8'))  # 2- 进行加密操作
    return md5.hexdigest().upper()  # 3- 返回加密后的值


class ScanDeal():
    def __init__(self):
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    def request(self, inData):
        url = "http://127.0.0.1:8081/PosMerchant/wxTranNew?"
        resp = requests.post(url, headers=self.headers, data=inData)
        return resp.text
    @staticmethod
    def scanDeal():
        df = pd.read_csv(project_sm_tx, dtype={'tranType': str, 'loansFlag': str})
        key = 'XxJ2A2S01D9LJxwW2016'
        # time.sleep(5)
        for j in df.index.values:  # range(len(df['merCode']))
            tranDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            time1 = datetime.now().strftime("%Y%m%d%H%M%S%f")
            merOrderId = str(random.randint(999, 10000)) + time1
            wxOrderId = str(random.randint(999, 10000)) + time1
            df['md5'] = df['merCode'].map(str) + str(merOrderId) + str(wxOrderId) + df['tramAmt'].map(str) + str(tranDate) + df['tranType'].map(str) + str(key)
            # x = df.copy()
            # print(df['md5'])
            df.loc[j, 'md5'] = get_md5(str(df.loc[j, 'md5']))
            sql = "select substr('%s',0,3) from dual" % (df['merCode'][j])
            mer = DemoOracle().select_one(sql)[0]
            print(str(df['merCode'][j]) + '有效商户号')
            if mer == '847':
                sql = "SELECT TERM_ID from TBL_INVENTORY_MANAGEMENT_posp a where MER_CODE='%s'order by a.TERM_ID" % (
                df['merCode'][j])
                termID = DemoOracle().select_one(sql)[0]
                inData = "merCode=%s&merOrderId=%s&wxOrderId=%s&tramAmt=%s&termID=%s&tranDate=%s&tranType=%s&settDate=%s&originate=%s&tranPass=%s&loansFlag=%s&settType=%s&MD5=%s" % (
                df['merCode'][j], merOrderId, wxOrderId, df['tramAmt'][j], termID, tranDate, df['tranType'][j],
                df['settDate'][j], df['originate'][j], df['tranPass'][j], df['loansFlag'][j], df['settType'][j],
                df.loc[j, 'md5'])
                print(inData)
                returns = ScanDeal().request(inData)
                # print(returns)
                if returns == '00':
                    print('交易成功')
                elif returns == '01':
                    print('商户号错误')
                elif returns == '06':
                    print('交易类型错误')
                elif returns == '09':
                    print('MD5校验错误')
                elif returns == '99':
                    print('系统异常')
            elif mer == '923':
                inData = "merCode=%s&merOrderId=%s&wxOrderId=%s&tramAmt=%s&termID=20000284&tranDate=%s&tranType=%s&settDate=%s&originate=%s&tranPass=%s&loansFlag=%s&settType=%s&MD5=%s" % (
                df['merCode'][j], merOrderId, wxOrderId, df['tramAmt'][j], tranDate, df['tranType'][j],
                df['settDate'][j], df['originate'][j], df['tranPass'][j], df['loansFlag'][j], df['settType'][j],
                df.loc[j, 'md5'])
                print(inData)
                returns = ScanDeal().request(inData)
                if returns == '00':
                    print('交易成功')
                elif returns == '01':
                    print('商户号错误')
                elif returns == '06':
                    print('交易类型错误')
                elif returns == '09':
                    print('MD5校验错误')
                elif returns == '99':
                    print('系统异常')



if __name__ == '__main__':
    ScanDeal.scanDeal()