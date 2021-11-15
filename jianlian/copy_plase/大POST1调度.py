import requests
from datetime import datetime, date, timedelta
import cx_Oracle
class HandleOracle:
    def __init__(self):
        # 建立连接
        self.conn = cx_Oracle.connect('swtonline/swtonline@192.168.2.62:1521/chinapay')
        # 创建一个游标对象
        self.cur = self.conn.cursor()
    def delete(self, sql):
        self.cur.execute(sql)
        self.conn.commit()
    def rollback(self):
        self.conn.rollback()
    def close(self):
        self.conn.close()
class Request():
    def request1(self):
        url1 = 'http://192.168.36.218:6080/PosMerchant/settleAccountTOneStep1Action!settleAccountStep1Producer.action'
        resp = requests.post(url1)
        return  resp.json()
    def request2(self,data):
        url2 = 'http://192.168.36.218:6080/PosMerchant/settleAccountTOneStep1Action!settleAccountStep1Consumer.action'
        resp = requests.post(url2,json=data)
        return resp.json()
    def request3(self):
        url3 = 'http://192.168.36.218:6080/PosMerchant/settleAccountTOneStep2Action!settleAccountStep2Producer.action'
        resp = requests.post(url3)
        return  resp.json()
    def request4(self,data):
        url4 = 'http://192.168.36.218:6080/PosMerchant/settleAccountTOneStep2Action!settleAccountStep2Consumer.action'
        resp = requests.post(url4,json=data)
        return resp.json()
if __name__ == '__main__':
    yesterday1 = (date.today() + timedelta(days=-1)).strftime("%Y%m%d")
    tomorrow1 = (date.today() + timedelta(days=+1)).strftime("%Y%m%d")
    yesterday2 = (date.today() + timedelta(days=-1)).strftime("%Y-%m-%d")
    tomorrow2 = (date.today() + timedelta(days=+1)).strftime("%Y-%m-%d")
    res1 = Request().request1() #第一次调Step1
    print(res1)
    if len(res1) == 0:
            # or yesterday != (res1[0]['endTranDate']) :
        # raise ('数据调度未清理')
        sql = [
                "DELETE FROM TBL_SETT_DATE_DAY  WHERE TO_CHAR(DATE_TIME,'yyyyMMdd') between '%s'and '%s'  AND SETT_CYCLE = 'T1_day'" % (yesterday1, tomorrow1),
                "DELETE FROM TBL_SETT_DATE  WHERE TO_CHAR(DATE_TIME,'yyyyMMdd') between '%s'and '%s'  AND SETT_CYCLE = '1'" % (yesterday1, tomorrow1),
                "DELETE FROM TBL_SETT_DATE_STEP  WHERE TO_CHAR(DATE_TIME,'yyyyMMdd') between '%s'and '%s'" % (yesterday1, tomorrow1),
                "DELETE FROM TBL_SETT_DATE_STEP_REQ  WHERE TRAN_DATE between '%s'and '%s'" % (yesterday1, tomorrow1),
                "DELETE FROM TBL_CHARGE_FEE_DETAIL_INFO  WHERE IDENTIFY_ID IN (  SELECT DISTINCT IDENTIFY_ID FROM TBL_TRAN_DETAIL_DATA_INFO  WHERE SETT_CYCLE = 'T1' AND sett_date between '%s'and '%s' AND MACHINE_TYPE IN ('01', '11') )" % (yesterday1, tomorrow1),
                "DELETE FROM TBL_MER_LEVERL_FEE_INFO  WHERE IDENTIFY_ID IN (  SELECT DISTINCT IDENTIFY_ID FROM TBL_TRAN_DETAIL_DATA_INFO  WHERE SETT_CYCLE = 'T1' AND sett_date between '%s'and '%s'  AND MACHINE_TYPE IN ('01', '11'))" % (yesterday1, tomorrow1),
                "DELETE FROM TBL_TRAN_DETAIL_DATA_INFO  WHERE SETT_CYCLE = 'T1'  AND sett_date between '%s'and '%s' AND MACHINE_TYPE IN ('01', '11')" % (yesterday1, tomorrow1),
                "DELETE FROM TBL_COLLECT_FEE WHERE ID IN ( SELECT t0.ID FROM TBL_COLLECT_FEE t0  INNER JOIN tbl_reality_amt t1 ON t0.mer_code = t1.mer_code AND t0.create_date = t1.create_date  INNER JOIN tbl_SETTLE_ACCOUNT t2 ON t1.mer_code = t2.mer_code AND t1.create_date = t2.sett_date  WHERE t1.term_num > 0  AND t2.sett_date between '%s'and '%s')" % (yesterday2, tomorrow2),
                "DELETE FROM TBL_REALITY_AMT WHERE REALITY_ID IN ( SELECT t1.REALITY_ID FROM tbl_reality_amt t1  INNER JOIN tbl_SETTLE_ACCOUNT t2 ON t1.mer_code = t2.mer_code AND t1.create_date = t2.sett_date  WHERE t2.sett_date between '%s'and '%s')" % (yesterday2, tomorrow2),
                "DELETE FROM TBL_CASH_BACK WHERE ID IN ( SELECT t0.ID FROM TBL_CASH_BACK t0  WHERE t0.deductions_date between '%s'and '%s'  AND SUBSTR(t0.serial_no, 0, 2) = 'T1')" % (yesterday2, tomorrow2),
                "DELETE FROM TBL_DEDUCTIONS_RECORDS WHERE ID IN ( SELECT t0.ID FROM TBL_DEDUCTIONS_RECORDS t0  WHERE SUBSTR(t0.deductions_time, 0, 10) between '%s'and '%s'  AND SUBSTR(t0.serial_no, 0, 2) = 'T1')" % (yesterday2, tomorrow2),
                "DELETE FROM TBL_SETT_PHONE p WHERE EXISTS (  SELECT t1.* FROM TBL_SETT_PHONE t1  INNER JOIN tbl_SETTLE_ACCOUNT t2 ON t1.mer_code = t2.mer_code AND t1.create_date = REPLACE(t2.sett_date, '-')  WHERE t2.sett_date between '%s'and '%s' AND p.mer_code = t1.mer_code AND p.create_date = t1.create_date)" % (yesterday2, tomorrow2),
                "DELETE FROM tbl_SETTLE_ACCOUNT WHERE SETT_DATE between '%s'and '%s'" % (yesterday2, tomorrow2),
                "DELETE FROM tbl_SETTLE_ACCOUNT_DAY WHERE SETT_DATE between '%s'and '%s'" % (yesterday2, tomorrow2),
                "DELETE FROM tbl_SETTLE_ACCOUNT_LIST WHERE SETT_DATE between '%s'and '%s'" % (yesterday2, tomorrow2)
                ]
        for i in sql:
            try:
                HandleOracle().delete(i)
                print('数据删除成功')
            except:
                HandleOracle().rollback()
                print('语句执行错误')
            HandleOracle().close()
        res1 = Request().request1()  # 第一次调Step1
        print(res1)
        for j in res1:
            # print(one)
            res2 = Request().request2(j) #第二次调Step1
        print(res2)
        res3 = Request().request3() #第一次调Step2
        print(res3)
        res4 = Request().request4(res3[0]) #第二次调Step2
        print(res4)
    else:
        for j in res1:
            # print(one)
            res2 = Request().request2(j) #第二次调Step1
        print(res2)
        res3 = Request().request3() #第一次调Step2
        print(res3)
        res4 = Request().request4(res3[0]) #第二次调Step2
        print(res4)