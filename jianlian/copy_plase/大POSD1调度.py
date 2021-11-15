import requests
import cx_Oracle
from datetime import datetime, date, timedelta
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
        url1 = 'http://192.168.36.218:6080/PosMerchant/settleAccountD1Action_settleD1Producer.action'
        resp = requests.post(url1)
        return  resp.json()
    def request2(self,data):
        url2 = 'http://192.168.36.218:6080/PosMerchant/settleAccountD1Action_settleD1Consumer.action'
        resp = requests.post(url2,json=data)
        return resp.json()
if __name__ == '__main__':
    yesterday1 = (date.today() + timedelta(days=-1)).strftime("%Y%m%d")
    tomorrow1 = (date.today() + timedelta(days=+1)).strftime("%Y%m%d")
    yesterday2 = (date.today() + timedelta(days=-1)).strftime("%Y-%m-%d")
    tomorrow2 = (date.today() + timedelta(days=+1)).strftime("%Y-%m-%d")
    sql = [
        "DELETE FROM TBL_CHARGE_FEE_DETAIL_INFO WHERE IDENTIFY_ID IN ( SELECT DISTINCT IDENTIFY_ID FROM TBL_TRAN_DETAIL_DATA_INFO WHERE SETT_CYCLE = 'D1' AND sett_date between '%s' and '%s' AND MACHINE_TYPE IN ('01', '11'))"%(yesterday1,tomorrow1),
        "DELETE FROM TBL_MER_LEVERL_FEE_INFO WHERE IDENTIFY_ID IN ( SELECT DISTINCT IDENTIFY_ID FROM TBL_TRAN_DETAIL_DATA_INFO WHERE SETT_CYCLE = 'D1' AND sett_date between '%s' and '%s' AND MACHINE_TYPE IN ('01', '11'))"%(yesterday1,tomorrow1),
        "DELETE FROM TBL_TRAN_DETAIL_DATA_INFO WHERE SETT_CYCLE = 'D1' AND sett_date between '%s' and '%s' AND MACHINE_TYPE IN ('01', '11')"%(yesterday1,tomorrow1),
        "DELETE FROM TBL_COLLECT_FEE WHERE ID IN ( SELECT t0.ID FROM TBL_COLLECT_FEE t0 INNER JOIN tbl_reality_amt D1 ON t0.mer_code = D1.mer_code AND t0.create_date = D1.create_date INNER JOIN tbl_SETTLE_ACCOUNT_D1 t2 ON D1.mer_code = t2.mer_code AND D1.create_date = t2.sett_date WHERE D1.term_num > 0 AND t2.sett_date between '%s' and '%s')"%(yesterday2,tomorrow2),
        "DELETE FROM TBL_REALITY_AMT WHERE REALITY_ID IN ( SELECT D1.REALITY_ID FROM tbl_reality_amt D1 INNER JOIN tbl_SETTLE_ACCOUNT_D1 t2 ON D1.mer_code = t2.mer_code AND D1.create_date = t2.sett_date WHERE t2.sett_date between '%s' and '%s')"%(yesterday2,tomorrow2),
        "DELETE FROM TBL_CASH_BACK WHERE ID IN ( SELECT t0.ID FROM TBL_CASH_BACK t0 WHERE t0.deductions_date between '%s' and '%s' AND SUBSTR(t0.serial_no, 0, 2) = 'D1')"%(yesterday2,tomorrow2),
        "DELETE FROM TBL_DEDUCTIONS_RECORDS WHERE ID IN ( SELECT t0.ID FROM TBL_DEDUCTIONS_RECORDS t0 WHERE SUBSTR(t0.deductions_time, 0, 10) between '%s' and '%s' AND SUBSTR(t0.serial_no, 0, 2) = 'D1')"%(yesterday2,tomorrow2),
        "DELETE FROM TBL_SETT_PHONE p WHERE EXISTS ( SELECT D1.* FROM TBL_SETT_PHONE D1 INNER JOIN tbl_SETTLE_ACCOUNT_D1 t2 ON D1.mer_code = t2.mer_code AND D1.create_date = REPLACE(t2.sett_date, '-') WHERE t2.sett_date between '%s' and '%s' AND p.mer_code = D1.mer_code AND p.create_date = D1.create_date)"%(yesterday2,tomorrow2),
        "DELETE FROM tbl_SETTLE_ACCOUNT_D1 WHERE SETT_DATE between '%s' and '%s'"%(yesterday2,tomorrow2)
           ]
    for one in sql:
        try:
            HandleOracle().delete(one)
            print('数据删除成功')
        except:
            HandleOracle().rollback()
            print('语句执行错误')
        HandleOracle().close()
    res1 = Request().request1() #第一次调Step1
    print(res1)
    if len(res1) == 0:
        raise ('数据调度未清理')
    for j in res1:
        # print(one)
        res2 = Request().request2(j) #第二次调Step1
    print(res2)