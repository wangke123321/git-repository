# from jlapi.Ocracle.swtonline import HandleOracle
from class_oracle.oracle_dome import *
from datetime import datetime
import pandas as pd
import time
import requests
import hashlib
from xml.dom.minidom import parseString



def get_md5(md5_):
    md5 = hashlib.md5()  # 1-实例化加密对象
    md5.update(md5_.encode('ISO-8859-1'))  # 2- 进行加密操作
    print(md5.hexdigest().upper())
    return md5.hexdigest().upper()  # 3- 返回加密后的值


class ScanDeal():
    def __init__(self):
        self.headers = {'Content-Type': 'text/xml'}

    def scandaeal(self, inData):
        url = " http://127.0.0.1:8081/PosMerchant/ZfMposPort"
        resp = requests.post(url, headers=self.headers, data=inData)
        return resp.text

    def csvControl(data):
        # 密钥
        key = 'XxJ2A2S01D9LJx'
        acqInsCode = '0848475210'
        # 遍历每行
        for j in range(len(df['merCode'])):
            # 获取当前系统时间
            time1 = datetime.now().strftime("%m%d%H%M%S")
            time2 = datetime.now().strftime("%d%H%M%S")
            # 拼接md5
            df['md5'] = df['merCode'].map(str) + df['tranAmt'] + str(key)
            # print(df['md5'])
            # print(df['tranAmt'])
            # 调用md5
            df.loc[j, 'md5'] = get_md5(str(df.loc[j, 'md5']))
            # print(df.loc[j, 'md5'])
            # 截取判断847和923商户
            sql = "select substr('%s',0,3) from dual" % (df['merCode'][j])
            mer = DemoOracle().select_one(sql)[0]
            # print(mer)
            if mer =='847':
                # 提取终端号
                sql1 = "SELECT TERM_ID from TBL_INVENTORY_MANAGEMENT_posp a where MER_CODE='%s'order by a.TERM_ID" % (df['merCode'][j])
                termID = DemoOracle().select_one(sql1)[0]
                try:
                    # 提取有效的商户号
                    sql2 = "select a.mer_code, b.mercode, c.mer_code, m.mer_code from TBL_INVENTORY_MANAGEMENT_posp a left join tbl_fee b on a.mer_code = b.mercode left join TBL_MERCHANT_COLLECT_FEE c on b.mercode = c.mer_code left join swtonlineb.tbl_mer_info m on m.mer_code = a.mer_code where a.machine_state = 1 and a.mer_code is not null and b.mercode is not null and c.mer_code is not null and m.mer_code is not null and a.mer_code='%s' order by a.create_date desc" % (
                    df['merCode'][j])
                    merCode01 = DemoOracle().select_all(sql2)
                    if len((merCode01)[0]) >= 4:
                        print(str(df['merCode'][j]) + '有效商户号')
                    # 插入当天交易信息表
                    sql3 = "insert into TBL_DIRECT_POS_A(ACQ_INS_CODE,TRACE_NUM,TRANS_DATETIME,TRANS_KEY1,TRANS_KEY2,PROCESS_FLAG,REV_FLAG,TIPS_FLAG,BEFORE_TRANS_CODE,AFTER_TRANS_CODE,TRANS_CLASS,TRANS_CURR,BILLING_CURR,ACQ_SETT_CURR,STAT_CURR,CURR_EXPONENT,TRANS_AMT,BILLING_AMT,ACQ_SETT_AMT,STAT_AMT,TIPS_AMT,TRANS_RATE,ACQ_SETT_RATE,STAT_RATE,CONV_DATE,ACCT_NUM,CARD_SEQUENCE_NUM,ACQ_CARD_TIME,SETT_DATE,MER_TYPE,ACQ_CNTRY_CODE,ISSR_CNTRY_CODE,SRV_ENTRY_MODE,FWD_INS_CODE,RECV_INS_CODE,ISSR_INS_CODE,RETRIVL_REF_NUM,ORIG_AUTH_CODE,RESP_AUTH_CODE,RESP_CODE,TERM_ID,MER_CODE,TERM_BATCH_ID,TERM_TRACE_NUM,MER_ADDR_NAME,MER_ACQ_INS_CODE,ORIG_MSG,ADDTNL_AMT,SELF_DEFINE,SA_SAV1,SA_SAV2,REC_CREATE_TIME,REC_UPDATE_TIME,REC_CODE,REC_ID,CARD_STATE,F59)values('%s','241079','%s','8475840572259629120726400006710'||TEST_DIRECT_POS_NUM.Nextval,'2010%s0','0','0','0','PER','PBI','NRM','156','156','156','156','2222','%s',0,'%s','0',0,'90000000','90000000','%s','%s','196222531314232847456','001','0123230006','%s','5300','020','000','051','0800000001','0814505800','0814505800','2010%s','  ','  ','00','%s','%s','000067','000761','深圳市红宝电器','0848475840','  ','0401001156C0000001542711002156C000000154271','002U00              00002067                B92D9130749A2A6604BFAE05D705C6B5                        02003100000002003000000006         26000000000000002263020000   48474520      0130100000100050             0848470000   N      0800000001                                                               ','     603100010230                                                                                                                                                                                                                                                             03031186847Q00045112967  F6   ','     603100010230                                                                                                                                                                                                                                                             03031186847Q00045112967  F6   ',TIMESTAMP '2020-04-22 01:04:31',TIMESTAMP '2020-04-22 01:04:31','012222100369960','','%s','')"%(acqInsCode,time1,time2,df['tranAmt'][j],df['tranAmt'][j],df['stat_date'][j],df['conv_date'][j],df['settDate'][j],time2,termID,df['merCode'][j],df['card_state'][j])
                    DemoOracle100().insert(sql3)
                    # 插入历史交易信息表
                    sql4 = "insert into TBL_DIRECT_POS_HISTORY_A(ACQ_INS_CODE,TRACE_NUM,TRANS_DATETIME,TRANS_KEY1,TRANS_KEY2,PROCESS_FLAG,REV_FLAG,TIPS_FLAG,BEFORE_TRANS_CODE,AFTER_TRANS_CODE,TRANS_CLASS,TRANS_CURR,BILLING_CURR,ACQ_SETT_CURR,STAT_CURR,CURR_EXPONENT,TRANS_AMT,BILLING_AMT,ACQ_SETT_AMT,STAT_AMT,TIPS_AMT,TRANS_RATE,ACQ_SETT_RATE,STAT_RATE,CONV_DATE,ACCT_NUM,CARD_SEQUENCE_NUM,ACQ_CARD_TIME,SETT_DATE,MER_TYPE,ACQ_CNTRY_CODE,ISSR_CNTRY_CODE,SRV_ENTRY_MODE,FWD_INS_CODE,RECV_INS_CODE,ISSR_INS_CODE,RETRIVL_REF_NUM,ORIG_AUTH_CODE,RESP_AUTH_CODE,RESP_CODE,TERM_ID,MER_CODE,TERM_BATCH_ID,TERM_TRACE_NUM,MER_ADDR_NAME,MER_ACQ_INS_CODE,ORIG_MSG,ADDTNL_AMT,SELF_DEFINE,SA_SAV1,SA_SAV2,REC_CREATE_TIME,REC_UPDATE_TIME,REC_CODE,REC_ID,CARD_STATE,F59)values('%s','241079','%s','8475840572259629120726400006710'||TEST_DIRECT_POS_NUM.Nextval,'2010%s0','0','0','0','PER','PBI','NRM','156','156','156','156','2222','%s',0,'%s','0',0,'90000000','90000000','%s','%s','196222531314232847456','001','0123230006','%s','5300','020','000','051','0800000001','0814505800','0814505800','2010%s','  ','  ','00','%s','%s','000067','000761','深圳市红宝电器','0848475840','  ','0401001156C0000001542711002156C000000154271','002U00              00002067                B92D9130749A2A6604BFAE05D705C6B5                        02003100000002003000000006         26000000000000002263020000   48474520      0130100000100050             0848470000   N      0800000001                                                               ','     603100010230                                                                                                                                                                                                                                                             03031186847Q00045112967  F6   ','     603100010230                                                                                                                                                                                                                                                             03031186847Q00045112967  F6   ',TIMESTAMP '2020-04-22 01:04:31',TIMESTAMP '2020-04-22 01:04:31','012222100369960','','%s','')" % (acqInsCode, time1, time2, df['tranAmt'][j], df['tranAmt'][j], df['stat_date'][j], df['conv_date'][j],df['settDate'][j], time2, termID, df['merCode'][j], df['card_state'][j])
                    DemoOracle100().insert(sql4)
                    # 查询当天插入交易信息 使用新插入的交易数据做提现
                    time.sleep(0.02)
                    sql5 = "select TRANS_DATETIME,ACQ_INS_CODE,RETRIVL_REF_NUM from swtonlineb.TBL_DIRECT_POS_A where MER_CODE='%s' and SETT_DATE='%s' order by TRANS_DATETIME desc" % (df['merCode'][j],df['settDate'][j])
                    RETRIVL_REF_NUM  = DemoOracle().select_all(sql5)[0][2]
                    print(RETRIVL_REF_NUM)
                    # 秒到提现请求体
                    inData =    '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:mpos="http://mpos.zf/">'\
                                '<soapenv:Header/>'\
                                    '<soapenv:Body>'\
                                        '<mpos:withdrawCash>'\
                                        '<arg0>'+str(df['merCode'][j])+'</arg0>'\
                                        '<arg1>'+str(df['tranAmt'][j])+'</arg1>'\
                                        '<arg2>'+str(df.loc[j, 'md5'])+'</arg2>'\
                                        '<arg3>'+str(termID)+'</arg3>'\
                                        '<arg4>'+str(RETRIVL_REF_NUM)+'</arg4>'\
                                        '<arg5>'+str(df['settDate'][j])+'</arg5>'\
                                        '</mpos:withdrawCash>'\
                                '</soapenv:Body>'\
                                '</soapenv:Envelope>'
                    # print(inData)
                    resp = ScanDeal().scandaeal(inData)
                    print(resp)
                    dom = parseString(resp)
                    return_text = dom.getElementsByTagName('return')[0].firstChild.nodeValue
                    returns = return_text.split()[0]
                    print(returns)
                    if returns == '00':
                        print('交易成功')
                    elif returns == '01':
                        print('md5错误')
                    elif returns == '10':
                        print('提现金额错误')
                    elif returns == '99':
                        print('秒到异常')
                except IndexError as e:
                    print(str(df['merCode'][j]) + "无效商户号", e)
            # if mer =='923':
            #     inData = "merCode=%s&merOrderId=%s&wxOrderId=%s&tramAmt=%s&termID=%s&tranDate=%s&tranType=%s&settDate=%s&originate=%s&tranPass=%s&loansFlag=%s&settType=%s&MD5=%s" % (df['merCode'][j], merOrderId, wxOrderId, df['tramAmt'][j], df['termID'][j], tranDate, df['tranType'][j],df['settDate'][j], df['originate'][j], df['tranPass'][j], df['loansFlag'][j], df['settType'][j], x.loc[j, 'md5'])
            #     print(inData)
            #     print(ScanDeal().scandaeal(inData))

if __name__ == '__main__':
    df = pd.read_csv(r'/jianlian/tixian_class/tx_data.csv', dtype={'tranAmt':str})
    # df = pd.DataFrame(df)
    ScanDeal.csvControl(df)
