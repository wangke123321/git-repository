from jianlian.class_oracle.oracle_dome import DemoOracle
from jianlian.timeclass.class_time import DateTime


class T1delete:
    @staticmethod
    def t1sql(t1, t1_, t2, t2_):  # t1昨天的日期、 t1_明天日期 格式(yyyymmdd）、 t2昨天的日期、 t2_明天日期 格式(yyyy-mm-dd）
        sql = [
        "DELETE FROM TBL_SETT_DATE_DAY  WHERE TO_CHAR(DATE_TIME,'yyyyMMdd') between '%s'and '%s'  AND SETT_CYCLE = 'T1_day'" % (t1, t1_),
        "DELETE FROM TBL_SETT_DATE  WHERE TO_CHAR(DATE_TIME,'yyyyMMdd') between '%s'and '%s'  AND SETT_CYCLE = '1'" % (t1, t1_),
        "DELETE FROM TBL_SETT_DATE_STEP  WHERE TO_CHAR(DATE_TIME,'yyyyMMdd') between '%s'and '%s'" % (t1, t1_),
        "DELETE FROM TBL_SETT_DATE_STEP_REQ  WHERE TRAN_DATE between '%s'and '%s'" % (t1, t1_),
        "DELETE FROM TBL_CHARGE_FEE_DETAIL_INFO  WHERE IDENTIFY_ID IN (  SELECT DISTINCT IDENTIFY_ID FROM TBL_TRAN_DETAIL_DATA_INFO  WHERE SETT_CYCLE = 'T1' AND sett_date between '%s'and '%s' AND MACHINE_TYPE IN ('01', '11') )" % (t1, t1_),
        "DELETE FROM TBL_MER_LEVERL_FEE_INFO  WHERE IDENTIFY_ID IN (  SELECT DISTINCT IDENTIFY_ID FROM TBL_TRAN_DETAIL_DATA_INFO  WHERE SETT_CYCLE = 'T1' AND sett_date between '%s'and '%s'  AND MACHINE_TYPE IN ('01', '11'))" % (t1, t1_),
        "DELETE FROM TBL_TRAN_DETAIL_DATA_INFO  WHERE SETT_CYCLE = 'T1'  AND sett_date between '%s'and '%s' AND MACHINE_TYPE IN ('01', '11')" % (t1, t1_),
        "DELETE FROM TBL_COLLECT_FEE WHERE ID IN ( SELECT t0.ID FROM TBL_COLLECT_FEE t0  INNER JOIN tbl_reality_amt t1 ON t0.mer_code = t1.mer_code AND t0.create_date = t1.create_date  INNER JOIN tbl_SETTLE_ACCOUNT t2 ON t1.mer_code = t2.mer_code AND t1.create_date = t2.sett_date  WHERE t1.term_num > 0  AND t2.sett_date between '%s'and '%s')" % (t2, t2_),
        "DELETE FROM TBL_REALITY_AMT WHERE REALITY_ID IN ( SELECT t1.REALITY_ID FROM tbl_reality_amt t1  INNER JOIN tbl_SETTLE_ACCOUNT t2 ON t1.mer_code = t2.mer_code AND t1.create_date = t2.sett_date  WHERE t2.sett_date between '%s'and '%s')" % (t2, t2_),
        "DELETE FROM TBL_CASH_BACK WHERE ID IN ( SELECT t0.ID FROM TBL_CASH_BACK t0  WHERE t0.deductions_date between '%s'and '%s'  AND SUBSTR(t0.serial_no, 0, 2) = 'T1')" % (t2, t2_),
        "DELETE FROM TBL_DEDUCTIONS_RECORDS WHERE ID IN ( SELECT t0.ID FROM TBL_DEDUCTIONS_RECORDS t0  WHERE SUBSTR(t0.deductions_time, 0, 10) between '%s'and '%s'  AND SUBSTR(t0.serial_no, 0, 2) = 'T1')" % (t2, t2_),
        "DELETE FROM TBL_SETT_PHONE p WHERE EXISTS (  SELECT t1.* FROM TBL_SETT_PHONE t1  INNER JOIN tbl_SETTLE_ACCOUNT t2 ON t1.mer_code = t2.mer_code AND t1.create_date = REPLACE(t2.sett_date, '-')  WHERE t2.sett_date between '%s'and '%s' AND p.mer_code = t1.mer_code AND p.create_date = t1.create_date)" % (t2, t2_),
        "DELETE FROM tbl_SETTLE_ACCOUNT WHERE SETT_DATE between '%s'and '%s'" % (t2, t2_),
        "DELETE FROM tbl_SETTLE_ACCOUNT_DAY WHERE SETT_DATE between '%s'and '%s'" % (t2, t2_),
        "DELETE FROM tbl_SETTLE_ACCOUNT_LIST WHERE SETT_DATE between '%s'and '%s'" % (t2, t2_)]
        for i in sql:
            try:
                DemoOracle().delete(i)
                print(i)
            except:
                DemoOracle().rollback()
                print('SQL语句执行错误')
            finally:
                DemoOracle().close()

if __name__ == '__main__':
    t1 = DateTime().random_date(-1)
    t1_job = DateTime().random_date(1)
    t2 = DateTime().random_dates(-1)
    t2_job = DateTime().random_dates(1)
    T1delete.t1sql(t1, t1_job, t2, t2_job)