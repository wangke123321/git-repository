import time
import requests
from jianlian.timeclass.class_time import DateTime
from jianlian.config.class_config import FileConfig
import pandas as pd
from jianlian.class_oracle.oracle_dome import *
from jianlian.encryption_class.class_MD5 import MD5
from jianlian.tixian_class.asserqual_class import RealXml
from jianlian.project_path.project_path import *
from jianlian.tomcat_class.tomcat_api import *
from jianlian.login_api.login_wk import My_log
my_logger = My_log()


class ScanDeal:
    def __init__(self, url):
        self.url = url
        # self.url = FileConfig().conf('../class_config', 'TX', 'get_8081')  # 8081，8086 服务器

    def credit_card(self, t1d1=None, mode=None, three=None):
        """ mode=all，交替成功和失败；mode=00商户交易都是成功；mode=44商户交易都是失败；不传参数是默认
            t1d1只作用847，t1d1=1是T1结算 ；t1d1=4是D1结算
            three='3'删除节假日数据 ；three为空是删除系统时间当天的的数据
        """
        csv = pd.read_csv(project_tx, dtype={'tranAmt': str})
        df = pd.DataFrame(csv)
        """清理数据：62库 提现表 手刷代付数据 优惠交易表 100库 清理当天交易表 历史交易表 """
        l1 = DateTime().now_dates()  # yyyy-MM-dd 根据电脑时间
        l2 = DateTime().now_date()  # yyyyMMdd 根据电脑时间
        l3 = df['settDate'][0]  # yyyyMMdd 根据传参交易时间
        key01 = 'XxJ2A2S01D9LJx'  # 加密令牌
        t1 = DateTime().random_date(-1)  # yyyyMMdd 根据电脑时间
        t1_1 = DateTime().random_date(2)  # yyyyMMdd 根据电脑时间
        t2 = DateTime().random_dates(-1)  # yyyy-MM-dd 根据电脑时间
        t2_1 = DateTime().random_dates(2)  # yyyy-MM-dd 根据电脑时间
        if three == '3':
            d = ["DELETE FROM TBL_WITHDRAW_CASH_FEE WHERE TRAN_DATE between '%s' and '%s'" % (t2, t2_1),
                 "DELETE FROM TBL_WITHDRACASH_NOPER WHERE SETT_DATE between '%s' and '%s'" % (t1, t1_1),
                 "DELETE FROM TBL_PREFERENTIAL_TRAN_INFO WHERE SETT_DATE between '%s' and '%s'" % (t1, t1_1)]
            d1 = ["DELETE FROM TBL_DIRECT_POS_A WHERE SETT_DATE between '%s' and '%s'" % (t1, t1_1),
                  "DELETE FROM TBL_DIRECT_POS_HISTORY_A WHERE SETT_DATE between '%s' and '%s'" % (t1, t1_1)]
            for dt in d:
                try:
                    DemoOracle().delete(dt)
                    print(dt)
                except:
                    DemoOracle().rollback()
                    print('提前清理提现表等数据报错')

            for dt1 in d1:
                try:
                    DemoOracle100().delete(dt1)
                    print(dt1)
                except:
                    DemoOracle100().rollback()
                    print('提前清理数据当天历史交易表错误')
        else:
            d = ["DELETE FROM TBL_WITHDRAW_CASH_FEE WHERE TRAN_DATE='%s'" % (l1,),
                 "DELETE FROM TBL_WITHDRACASH_NOPER WHERE SETT_DATE = '%s'" % (l2,),
                 "DELETE FROM TBL_PREFERENTIAL_TRAN_INFO WHERE SETT_DATE = '%s'" % (l2,)]
            d1 = ["DELETE FROM TBL_DIRECT_POS_A WHERE SETT_DATE='%s'" % (l2,),
                  "DELETE FROM TBL_DIRECT_POS_HISTORY_A WHERE SETT_DATE='%s'" % (l2,)]
            for dt in d:
                try:
                    DemoOracle().delete(dt)
                    print(dt)
                except:
                    DemoOracle().rollback()
                    print('提前清理提现表等数据报错')

            for dt1 in d1:
                try:
                    DemoOracle100().delete(dt1)
                    print(dt1)
                except:
                    DemoOracle100().rollback()
                    print('提前清理数据当天历史交易表错误')

        for item in df.index.values:  # range(len(df['merCode'])) df.index.values 遍历csv中的数据
            headers = {'Content-Type': 'text/xml', 'User-Agent': 'Apache-HttpClient/4.5.3 (Java/1.8.0_144)', 'SOAPAction': "application/soap+xml;charset=utf-8", 'Content-Length': '410'}
            l4 = DateTime().now_month()  # 取当前时间 MMddHHMMSS
            l5 = '2010' + time.strftime("%d%H%M%S", time.localtime()) + '0'
            l6 = '051'  # 正常：051; 磁条卡限额转T1  设置：021或者022
            l7 = '2010' + time.strftime("%d%H%M%S", time.localtime())
            sql = "select substr('%s',0,3) from dual" % (df['merCode'][item])  # 提取不同的商户号
            mer_code = DemoOracle().select_one(sql)[0]
            if mer_code == '847':
                try:
                    print('\n' + '=========================================================执行商户号: ', df['merCode'][item],"=========================================================")
                    md5 = str(df['merCode'][item]) + str(df['tranAmt'][item]) + key01
                    md5Str = MD5(md5).md5_upper()
                    print("MD5加密前为：", md5)
                    print("MD5加密后为：", md5Str)
                    sql01 = "select a.mer_code, b.mercode, c.mer_code, m.mer_code from TBL_INVENTORY_MANAGEMENT_posp a left join tbl_fee b on a.mer_code = b.mercode left join TBL_MERCHANT_COLLECT_FEE c on b.mercode = c.mer_code left join swtonlineb.tbl_mer_info m on m.mer_code = a.mer_code where a.machine_state = 1 and a.mer_code is not null and b.mercode is not null and c.mer_code is not null and m.mer_code is not null and a.mer_code='%s' order by a.create_date desc" % (df['merCode'][item])
                    res01 = DemoOracle().select_all(sql01)
                    if len(res01[0]) >= 4:  # 判断是否有效
                        """插入：当天交易表 历史交易表 sql03：查询当天插入的交易信息 sql04：修改A表交易参考号 """
                        sql02 = "SELECT TERM_ID from TBL_INVENTORY_MANAGEMENT_posp a where MER_CODE='%s'order by a.TERM_ID" % (df['merCode'][item])
                        termID = DemoOracle().select_one(sql02)[0]  # 终端号：res02[0]
                        print('查出的终端号: ' + termID)
                        if t1d1 == None:
                            pass
                        else:  # D1商户 T1商户
                            sql_t1d1 = "update tbl_fee set MERCHANT_TYPE='%s' where mercode='%s' " % (t1d1, df['merCode'][item])
                            DemoOracle().update(sql_t1d1)
                            print(sql_t1d1)
                        sql03 = "insert into TBL_DIRECT_POS_A(ACQ_INS_CODE,TRACE_NUM,TRANS_DATETIME,TRANS_KEY1,TRANS_KEY2,PROCESS_FLAG,REV_FLAG,TIPS_FLAG,BEFORE_TRANS_CODE,AFTER_TRANS_CODE,TRANS_CLASS,TRANS_CURR,BILLING_CURR,ACQ_SETT_CURR,STAT_CURR,CURR_EXPONENT,TRANS_AMT,BILLING_AMT,ACQ_SETT_AMT,STAT_AMT,TIPS_AMT,TRANS_RATE,ACQ_SETT_RATE,STAT_RATE,CONV_DATE,ACCT_NUM,CARD_SEQUENCE_NUM,ACQ_CARD_TIME,SETT_DATE,MER_TYPE,ACQ_CNTRY_CODE,ISSR_CNTRY_CODE,SRV_ENTRY_MODE,FWD_INS_CODE,RECV_INS_CODE,ISSR_INS_CODE,RETRIVL_REF_NUM,ORIG_AUTH_CODE,RESP_AUTH_CODE,RESP_CODE,TERM_ID,MER_CODE,TERM_BATCH_ID,TERM_TRACE_NUM,MER_ADDR_NAME,MER_ACQ_INS_CODE,ORIG_MSG,ADDTNL_AMT,SELF_DEFINE,SA_SAV1,SA_SAV2,REC_CREATE_TIME,REC_UPDATE_TIME,REC_CODE,REC_ID,CARD_STATE,F59)values('0848475210','241079','%s','8475840572259629120726400006710'||TEST_DIRECT_POS_NUM.Nextval,'%s','0','0','0','PER','PBI','NRM','156','156','156','156','2222','%s',0,'%s','0',0,'90000000','90000000','%s','%s','196222531314232847456','001','0123230006','%s','5300','020','000','%s','0800000001','0814505800','0814505800','%s','  ','  ','00','%s','%s','000067','000761','深圳市红宝电器','0848475840','  ','0401001156C0000001542711002156C000000154271','002U00              00002067                B92D9130749A2A6604BFAE05D705C6B5                        02003100000002003000000006         26000000000000002263020000   48474520      0130100000100050             0848470000   N      0800000001                                                               ','     603100010230                                                                                                                                                                                                                                                             03031186847Q00045112967  F6   ','     603100010230                                                                                                                                                                                                                                                             03031186847Q00045112967  F6   ',TIMESTAMP '2020-04-22 01:04:31',TIMESTAMP '2020-04-22 01:04:31','012222100369960','a','%s','')" % (l4,l5,df['tranAmt'][item],df['tranAmt'][item],df['stat_date'][item],df['conv_date'][item],df['settDate'][item],l6,l7,termID,df['merCode'][item],df['card_state'][item])
                        print(sql03)
                        DemoOracle100().insert(sql03)
                        sql04 = "insert into TBL_DIRECT_POS_HISTORY_A(ACQ_INS_CODE,TRACE_NUM,TRANS_DATETIME,TRANS_KEY1,TRANS_KEY2,PROCESS_FLAG,REV_FLAG,TIPS_FLAG,BEFORE_TRANS_CODE,AFTER_TRANS_CODE,TRANS_CLASS,TRANS_CURR,BILLING_CURR,ACQ_SETT_CURR,STAT_CURR,CURR_EXPONENT,TRANS_AMT,BILLING_AMT,ACQ_SETT_AMT,STAT_AMT,TIPS_AMT,TRANS_RATE,ACQ_SETT_RATE,STAT_RATE,CONV_DATE,ACCT_NUM,CARD_SEQUENCE_NUM,ACQ_CARD_TIME,SETT_DATE,MER_TYPE,ACQ_CNTRY_CODE,ISSR_CNTRY_CODE,SRV_ENTRY_MODE,FWD_INS_CODE,RECV_INS_CODE,ISSR_INS_CODE,RETRIVL_REF_NUM,ORIG_AUTH_CODE,RESP_AUTH_CODE,RESP_CODE,TERM_ID,MER_CODE,TERM_BATCH_ID,TERM_TRACE_NUM,MER_ADDR_NAME,MER_ACQ_INS_CODE,ORIG_MSG,ADDTNL_AMT,SELF_DEFINE,SA_SAV1,SA_SAV2,REC_CREATE_TIME,REC_UPDATE_TIME,REC_CODE,REC_ID,CARD_STATE,F59)values('0848475210','241079','%s','8475840572259629120726400006710'||TEST_DIRECT_POS_NUM.Nextval,'%s','0','0','0','PER','PBI','NRM','156','156','156','156','2222','%s',0,'%s','0',0,'90000000','90000000','%s','%s','196222531314232847456','001','0123230006','%s','5300','020','000','%s','0800000001','0814505800','0814505800','%s','  ','  ','00','%s','%s','000067','000761','深圳市红宝电器','0848475840','  ','0401001156C0000001542711002156C000000154271','002U00              00002067                B92D9130749A2A6604BFAE05D705C6B5                        02003100000002003000000006         26000000000000002263020000   48474520      0130100000100050             0848470000   N      0800000001                                                               ','     603100010230                                                                                                                                                                                                                                                             03031186847Q00045112967  F6   ','     603100010230                                                                                                                                                                                                                                                             03031186847Q00045112967  F6   ',TIMESTAMP '2020-04-22 01:04:31',TIMESTAMP '2020-04-22 01:04:31','012222100369960','a','%s','')" % (l4,l5,df['tranAmt'][item],df['tranAmt'][item],df['stat_date'][item],df['conv_date'][item],df['settDate'][item],l6,l7,termID,df['merCode'][item],df['card_state'][item])
                        print(sql04)
                        DemoOracle100().insert(sql04)
                        time.sleep(1)  # 延时1S
                        sql05 = "select TRANS_DATETIME,ACQ_INS_CODE,RETRIVL_REF_NUM from TBL_DIRECT_POS_A where MER_CODE='%s' and SETT_DATE='%s' order by TRANS_DATETIME desc" % (df['merCode'][item], df['settDate'][item])
                        res03 = DemoOracle100().select_all(sql05)
                        termCode = res03[0][2]
                        res_num = termCode + '0'
                        sql06 = ["update TBL_DIRECT_POS_A set TRANS_KEY2 = '%s' where MER_CODE = '%s' and SETT_DATE = '%s' and RETRIVL_REF_NUM='%s'" % (res_num, df['merCode'][item], df['settDate'][item], termCode),
                                 "update TBL_DIRECT_POS_HISTORY_A set TRANS_KEY2 = '%s' where MER_CODE = '%s' and SETT_DATE = '%s' and RETRIVL_REF_NUM='%s'" % (res_num, df['merCode'][item], df['settDate'][item], termCode)]
                        for j in sql06:
                            print(j)
                            DemoOracle100().update(j)

                        body = '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:mpos="http://mpos.zf/">'\
                                    '<soapenv:Header/>'\
                                        '<soapenv:Body>'\
                                            '<mpos:withdrawCash>'\
                                            '<arg0>'+str(df['merCode'][item])+'</arg0>'\
                                            '<arg1>'+str(df['tranAmt'][item])+'</arg1>'\
                                            '<arg2>'+str(md5Str)+'</arg2>'\
                                            '<arg3>'+str(termID)+'</arg3>'\
                                            '<arg4>'+str(termCode)+'</arg4>'\
                                            '<arg5>'+str(df['settDate'][item])+'</arg5>'\
                                            '</mpos:withdrawCash>'\
                                        '</soapenv:Body>'\
                                    '</soapenv:Envelope>'

                        print('提现接口传参：' + body)

                        code = requests.request("POST", self.url, headers=headers, data=body.encode('utf-8')).text
                        RealXml.xml_file(code, 'return')
                        my_logger.info('API返回结果： \n{0}'.format(code))
                        if mode == 'all':
                            if int(item) % 2 == 0:
                                sql00 = "update TBL_WITHDRAW_CASH_FEE set OUT_STATE='00',AUDITING_STATE='00',MERCHANT_STATE='1' where MER_CODE ='%s' and RETRIVL_REF_NUM='%s'" % (df['merCode'][item], termCode)
                                print('提现成功sql：'+sql00)
                                DemoOracle().update(sql00)
                                print('{0}，商户提现成功'.format(df['merCode'][item]))
                            else:
                                sql44 = "update TBL_WITHDRAW_CASH_FEE set OUT_STATE='44',AUDITING_STATE='44',MERCHANT_STATE='1' where MER_CODE ='%s' and RETRIVL_REF_NUM='%s'" % (df['merCode'][item], termCode)
                                print('提现失败sql：' + sql44)
                                DemoOracle().update(sql44)
                                print('{0}，商户提现失败'.format(df['merCode'][item]))
                        elif mode == '00':  # 修改提现费为已成功
                            mode00 = "update TBL_WITHDRAW_CASH_FEE set OUT_STATE='00',AUDITING_STATE='00',MERCHANT_STATE='1' where MER_CODE ='%s' and RETRIVL_REF_NUM='%s'" % (df['merCode'][item], termCode)
                            print('提现成功sql：' + mode00)
                            DemoOracle().update(mode00)
                            print('{0}，商户提现成功'.format(df['merCode'][item]))
                        elif mode == '44':  # 修改提现费为失败
                            mode44 = "update TBL_WITHDRAW_CASH_FEE set OUT_STATE='44',AUDITING_STATE='44',MERCHANT_STATE='1' where MER_CODE ='%s' and RETRIVL_REF_NUM='%s'" % (df['merCode'][item], termCode)
                            print('提现失败sql：' + mode44)
                            DemoOracle().update(mode44)
                            print('{0}，商户提现失败'.format(df['merCode'][item]))
                        else:
                            pass
                except IndexError as e:
                    print('{0}是无效商户号'.format(df['merCode'][item]), e)
                    # raise e

            elif mer_code == '923':
                """ 提取有效的商户号 trans_data, ret_num """
                try:
                    print('\n' + '=========================================================执行商户号: ', df['merCode'][item],"=========================================================")
                    termTraceNum = '000761'
                    acqInsCode = '0848475210'
                    sql1 = "select a.mer_code, b.mercode, c.mer_code, m.mer_code from TBL_INVENTORY_MANAGEMENT a left join tbl_fee b on a.mer_code = b.mercode left join TBL_MERCHANT_COLLECT_FEE c on b.mercode = c.mer_code left join swtonlineb.tbl_mer_info m on m.mer_code = a.mer_code where a.machine_state = 1 and a.mer_code is not null and b.mercode is not null and c.mer_code is not null and m.mer_code is not null and a.mer_code='%s' order by a.create_date desc" % (df['merCode'][item])
                    res1 = DemoOracle().select_all(sql1)
                    if len(res1[0]) >= 4:  # 判断是否有效
                        """插入：当天交易表 历史交易表 查询当天插入的交易信息 """
                        sql2 = "insert into TBL_DIRECT_POS_A(ACQ_INS_CODE,TRACE_NUM,TRANS_DATETIME,TRANS_KEY1,TRANS_KEY2,PROCESS_FLAG,REV_FLAG,TIPS_FLAG,BEFORE_TRANS_CODE,AFTER_TRANS_CODE,TRANS_CLASS,TRANS_CURR,BILLING_CURR,ACQ_SETT_CURR,STAT_CURR,CURR_EXPONENT,TRANS_AMT,BILLING_AMT,ACQ_SETT_AMT,STAT_AMT,TIPS_AMT,TRANS_RATE,ACQ_SETT_RATE,STAT_RATE,CONV_DATE,ACCT_NUM,CARD_SEQUENCE_NUM,ACQ_CARD_TIME,SETT_DATE,MER_TYPE,ACQ_CNTRY_CODE,ISSR_CNTRY_CODE,SRV_ENTRY_MODE,FWD_INS_CODE,RECV_INS_CODE,ISSR_INS_CODE,RETRIVL_REF_NUM,ORIG_AUTH_CODE,RESP_AUTH_CODE,RESP_CODE,TERM_ID,MER_CODE,TERM_BATCH_ID,TERM_TRACE_NUM,MER_ADDR_NAME,MER_ACQ_INS_CODE,ORIG_MSG,ADDTNL_AMT,SELF_DEFINE,SA_SAV1,SA_SAV2,REC_CREATE_TIME,REC_UPDATE_TIME,REC_CODE,REC_ID,CARD_STATE,F59)values('0848475210','241079','%s','8475840572259629120726400006710'||TEST_DIRECT_POS_NUM.Nextval,'%s','0','0','0','PER','PBI','NRM','156','156','156','156','2222','%s',0,'%s','0',0,'90000000','90000000','%s','%s','196222531314232847456','001','0123230006','%s','5300','020','000','%s','0800000001','0814505800','0814505800','%s','  ','  ','00','%s','%s','000067','000761','深圳市红宝电器','0848475840','  ','0401001156C0000001542711002156C000000154271','002U00              00002067                B92D9130749A2A6604BFAE05D705C6B5                        02003100000002003000000006         26000000000000002263020000   48474520      0130100000100050             0848470000   N      0800000001                                                               ','     603100010230                                                                                                                                                                                                                                                             03031186847Q00045112967  F6   ','     603100010230                                                                                                                                                                                                                                                             03031186847Q00045112967  F6   ',TIMESTAMP '2020-04-22 01:04:31',TIMESTAMP '2020-04-22 01:04:31','012222100369960','a','%s','')" % (l4, l5, df['tranAmt'][item], df['tranAmt'][item], df['stat_date'][item], df['conv_date'][item], df['settDate'][item], l6, l7, '000761', df['merCode'][item], df['card_state'][item])
                        print(sql2)
                        DemoOracle100().insert(sql2)
                        sql3 = "insert into TBL_DIRECT_POS_HISTORY_A(ACQ_INS_CODE,TRACE_NUM,TRANS_DATETIME,TRANS_KEY1,TRANS_KEY2,PROCESS_FLAG,REV_FLAG,TIPS_FLAG,BEFORE_TRANS_CODE,AFTER_TRANS_CODE,TRANS_CLASS,TRANS_CURR,BILLING_CURR,ACQ_SETT_CURR,STAT_CURR,CURR_EXPONENT,TRANS_AMT,BILLING_AMT,ACQ_SETT_AMT,STAT_AMT,TIPS_AMT,TRANS_RATE,ACQ_SETT_RATE,STAT_RATE,CONV_DATE,ACCT_NUM,CARD_SEQUENCE_NUM,ACQ_CARD_TIME,SETT_DATE,MER_TYPE,ACQ_CNTRY_CODE,ISSR_CNTRY_CODE,SRV_ENTRY_MODE,FWD_INS_CODE,RECV_INS_CODE,ISSR_INS_CODE,RETRIVL_REF_NUM,ORIG_AUTH_CODE,RESP_AUTH_CODE,RESP_CODE,TERM_ID,MER_CODE,TERM_BATCH_ID,TERM_TRACE_NUM,MER_ADDR_NAME,MER_ACQ_INS_CODE,ORIG_MSG,ADDTNL_AMT,SELF_DEFINE,SA_SAV1,SA_SAV2,REC_CREATE_TIME,REC_UPDATE_TIME,REC_CODE,REC_ID,CARD_STATE,F59)values('0848475210','241079','%s','8475840572259629120726400006710'||TEST_DIRECT_POS_NUM.Nextval,'%s','0','0','0','PER','PBI','NRM','156','156','156','156','2222','%s',0,'%s','0',0,'90000000','90000000','%s','%s','196222531314232847456','001','0123230006','%s','5300','020','000','%s','0800000001','0814505800','0814505800','%s','  ','  ','00','%s','%s','000067','000761','深圳市红宝电器','0848475840','  ','0401001156C0000001542711002156C000000154271','002U00              00002067                B92D9130749A2A6604BFAE05D705C6B5                        02003100000002003000000006         26000000000000002263020000   48474520      0130100000100050             0848470000   N      0800000001                                                               ','     603100010230                                                                                                                                                                                                                                                             03031186847Q00045112967  F6   ','     603100010230                                                                                                                                                                                                                                                             03031186847Q00045112967  F6   ',TIMESTAMP '2020-04-22 01:04:31',TIMESTAMP '2020-04-22 01:04:31','012222100369960','a','%s','')" % (l4, l5, df['tranAmt'][item], df['tranAmt'][item], df['stat_date'][item], df['conv_date'][item], df['settDate'][item], l6, l7, '000761', df['merCode'][item], df['card_state'][item])
                        print(sql3)
                        DemoOracle100().insert(sql3)
                        time.sleep(1)  # 延时1S
                        sql4 = "select TRANS_DATETIME,ACQ_INS_CODE,RETRIVL_REF_NUM from TBL_DIRECT_POS_A where MER_CODE='%s' and SETT_DATE='%s' order by TRANS_DATETIME desc" % (df['merCode'][item], df['settDate'][item])
                        res_code = DemoOracle100().select_all(sql4)
                        trans_data, ret_num = res_code[0][0], res_code[0][2]  # 交易时间, 交易参考号
                        md5 = str(df['merCode'][item]) + termTraceNum + str(ret_num) + acqInsCode + termTraceNum + str(trans_data) + str(df['settDate'][item]) + str(df['tranAmt'][item]) + key01
                        md5Str = MD5(md5).md5_upper()
                        print("MD5加密前为：", md5)
                        print("MD5加密后为：", md5Str)

                        body = '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:mpos="http://mpos.zf/"><soapenv:Header/>' \
                                        '<soapenv:Body>' \
                                            '<mpos:withdrawCashFeeGD>' \
                                                '<arg0>'+str(df['merCode'][item])+'</arg0>' \
                                                '<arg1>'+str(termTraceNum)+'</arg1>' \
                                                '<arg2>'+str(ret_num)+'</arg2>'\
                                                '<arg3>'+str(acqInsCode)+'</arg3>'\
                                                '<arg4>'+str(termTraceNum)+'</arg4>'\
                                                '<arg5>'+str(trans_data)+'</arg5>'\
                                                '<arg6>'+str(df['settDate'][item])+'</arg6>'\
                                                '<arg7>'+str(df['tranAmt'][item])+'</arg7>'\
                                                '<arg8>'+md5Str+'</arg8>'\
                                            '</mpos:withdrawCashFeeGD>'\
                                    '</soapenv:Body>'\
                            '</soapenv:Envelope>'

                        print('提现接口传参：' + body)

                        code = requests.request("POST", self.url, headers=headers, data=body.encode('utf-8')).text
                        RealXml.xml_file_mpos(code, 'return')
                        my_logger.info('API返回结果： \n{0}'.format(code))
                        if mode == 'all':
                            if int(item) % 2 == 0:
                                sql00 = "update TBL_WITHDRAW_CASH_FEE set OUT_STATE='00',AUDITING_STATE='00',MERCHANT_STATE='1' where MER_CODE_KQ ='%s' and RETRIVL_REF_NUM='%s'" % (df['merCode'][item], ret_num)
                                print('提现成功sql：' + sql00)
                                DemoOracle().update(sql00)
                                print('{0}，商户提现成功'.format(df['merCode'][item]))
                            else:
                                sql44 = "update TBL_WITHDRAW_CASH_FEE set OUT_STATE='44',AUDITING_STATE='44',MERCHANT_STATE='1' where MER_CODE_KQ ='%s' and RETRIVL_REF_NUM='%s'" % (df['merCode'][item], ret_num)
                                print('提现失败sql：' + sql44)
                                DemoOracle().update(sql44)
                                print('{0}，商户提现失败'.format(df['merCode'][item]))
                        elif mode == '00':  # 修改提现费为已成功
                            mode00 = "update TBL_WITHDRAW_CASH_FEE set OUT_STATE='00',AUDITING_STATE='00',MERCHANT_STATE='1' where MER_CODE_KQ ='%s' and RETRIVL_REF_NUM='%s'" % (df['merCode'][item], ret_num)
                            print('提现成功sql：' + mode00)
                            DemoOracle().update(mode00)
                            print('{0}，商户提现成功'.format(df['merCode'][item]))
                        elif mode == '44':  # 修改提现失败
                            mode44 = "update TBL_WITHDRAW_CASH_FEE set OUT_STATE='44',AUDITING_STATE='44',MERCHANT_STATE='1' where MER_CODE_KQ ='%s' and RETRIVL_REF_NUM='%s'" % (df['merCode'][item], ret_num)
                            print('提现失败sql：' + mode44)
                            DemoOracle().update(mode44)
                            print('{0}，商户提现失败'.format(df['merCode'][item]))
                        else:
                            pass
                except IndexError as e:
                    print('{0}是无效商户号'.format(df['merCode'][item]), e)
                    # raise e

            elif mer_code == '922':
                print('{0}:922商户'.format(df['merCode'][item]))
            else:
                print("不存在这类商户号")
        DemoOracle100().close()
        DemoOracle().close()

if __name__ == '__main__':
    # 启动自动发布包
    path = 'd: && cd D:\\apache-tomcat-7.0.88-8081\\bin && startup.bat'
    startServer(path)
    # 跑刷卡交易
    url = FileConfig().config('../class_config', 'TX', 'get_8081')
    # url = 'http://127.0.0.1:8081/PosMerchant/ZfMposPort'
    ScanDeal(url).credit_card()