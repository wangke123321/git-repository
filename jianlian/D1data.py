from jianlian.class_oracle.oracle_dome import DemoOracle
from jianlian.timeclass.class_time import DateTime


class D1delete:
    @staticmethod
    def d1sql(d1, d1_, d2_):
        """d1是交易结算的日期、格式(yyyymmdd）、 d1_交易结算日期、格式(yyyy-mm-dd）
           d2是交易日期 、格式(yyyymmdd）、d2_交易日期、格式(yyyy-mm-dd） """
        sql = [
            "DELETE FROM TBL_CHARGE_FEE_DETAIL_INFO  WHERE IDENTIFY_ID IN (SELECT DISTINCT IDENTIFY_ID FROM TBL_TRAN_DETAIL_DATA_INFO  WHERE SETT_CYCLE = 'D1' AND sett_date = '%s')" % (d1,),
            "DELETE FROM TBL_MER_LEVERL_FEE_INFO  WHERE IDENTIFY_ID IN (SELECT DISTINCT IDENTIFY_ID FROM TBL_TRAN_DETAIL_DATA_INFO  WHERE SETT_CYCLE = 'D1' AND sett_date = '%s')" % (d1,),
            "DELETE FROM TBL_TRAN_DETAIL_DATA_INFO  WHERE SETT_CYCLE = 'D1'  AND sett_date = '%s'" % (d1,),
            "DELETE FROM TBL_SETT_PHONE p WHERE p.create_date = '%s'" % (d1,),
            "DELETE FROM TBL_COLLECT_FEE WHERE ID IN ( SELECT t0.ID FROM TBL_COLLECT_FEE t0  INNER JOIN tbl_reality_amt t1 ON t0.mer_code = t1.mer_code AND t0.create_date = t1.create_date  INNER JOIN tbl_settle_account_d1 t2 ON t1.mer_code = t2.mer_code AND t1.create_date = t2.sett_date  WHERE t1.term_num > 0  AND t2.sett_date = '%s')" % (d1_,),
            "DELETE FROM TBL_REALITY_AMT WHERE REALITY_ID IN ( SELECT t1.REALITY_ID FROM tbl_reality_amt t1  INNER JOIN tbl_settle_account_d1 t2 ON t1.mer_code = t2.mer_code AND t1.create_date = t2.sett_date  WHERE t2.sett_date = '%s')" % (d1_,),
            "DELETE FROM TBL_CASH_BACK WHERE ID IN ( SELECT t0.ID FROM TBL_CASH_BACK t0  WHERE t0.deductions_date = '%s'  AND SUBSTR(t0.serial_no, 0, 2) = 'D1')" % (d1_,),
            "DELETE FROM TBL_DEDUCTIONS_RECORDS WHERE ID IN ( SELECT t0.ID FROM TBL_DEDUCTIONS_RECORDS t0  WHERE SUBSTR(t0.deductions_time, 0, 10) = '%s'  AND SUBSTR(t0.serial_no, 0, 2) = 'D1')" % (d1_,),
            "DELETE FROM TBL_SETTLE_ACCOUNT_D1 WHERE SETT_DATE between '%s' and '%s'" % (d2_, d1_),
            "DELETE from TBL_SETTLE_ACCOUNT_D1 where TRAN_DATE between '%s'and '%s'" % (d2_, d1_),
            "DELETE from tbl_SETTLE_ACCOUNT where TRAN_DATE between '%s'and '%s'" % (d2_, d1_),
            "DELETE from tbl_SETTLE_ACCOUNT_list where TRAN_DATE between '%s'and '%s'" % (d2_, d1_)]
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
    d1 = DateTime().random_date(1)
    d1_ = DateTime().random_dates(1)
    d2_ = DateTime().now_dates()
    D1delete.d1sql(d1, d1_, d2_,)