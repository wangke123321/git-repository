import pandas as pd
from class_oracle.oracle_dome import *

csv = pd.read_csv('data.csv')
df = pd.DataFrame(csv)

def data():
    for item in range(len(df['merCode'])):
        try:  # 提取不同的商户号
            sql = "select substr('%s',0,3) from dual" % (df['merCode'][item])
            res = DemoOracle().select_one(sql)
            if res[0] == '847':
                sql01 = "select a.mer_code, b.mercode, c.mer_code, m.mer_code from TBL_INVENTORY_MANAGEMENT_posp a left join tbl_fee b on a.mer_code = b.mercode left join TBL_MERCHANT_COLLECT_FEE c on b.mercode = c.mer_code left join swtonlineb.tbl_mer_info m on m.mer_code = a.mer_code where a.machine_state = 1 and a.mer_code is not null and b.mercode is not null and c.mer_code is not null and m.mer_code is not null and a.mer_code='%s' order by a.create_date desc" % (df['merCode'][item])
                res01 = DemoOracle().select_all(sql01)
                if len(res01[0]) >= 4:  # 判断是否有效
                    """修改政策数据: sql02: 查终端号, sql03：修改大POS库存表, sql04：修改费表, sql05：修改无卡快捷费率,
                    sql06：修改商户信息表借记卡费率, sql07：修改成本表, sql08：修改提现费表, sql_pos:03,04,05,07,08
                    """
                    sql02 = "SELECT TERM_ID from TBL_INVENTORY_MANAGEMENT_posp a where MER_CODE='%s'order by a.TERM_ID" % (df['merCode'][item])
                    res02 = DemoOracle().select_all(sql02)  # 终端号：res02[0]
                    sql_pos = ["update TBL_INVENTORY_MANAGEMENT_posp set CASH_BACK_STATE='%s',USER_NAME2='%s',BRANCH='%s',MACHINE_ACTIVATE_DATE='%s',CREATE_DATE='%s' where MER_CODE='%s'" % (df['zhengC'][item], df['user2'][item], df['BRANCH'][item], df['DATE'][item], df['CDate'][item], df['merCode'][item]),
                               "update TBL_FEE set USERNAME2='%s',AMOUNT='%s',DAI_COMMISION_VALUE='%s',BRANCH='%s',CASH_BACK_STATE='%s',MERCHANT_TYPE='%s',CREATE_DATE='%s',VIP_FEE='%s',YUNFU_FEE='%s',WKKJ_TX_VALUE='%s',WKKJ_CREDIT_TX_VALUE='%s',OUT_FEE='%s',OUT_FEE_WSZF='%s',DAI_AMOUNT='%s',QZF_COMMISION_VALUE='%s',qyl_commision_value='%s',qyl_thousand_value='%s'  where MERCODE='%s'" % (df['user2'][item], df['AMOUNT'][item], df['Dai'][item], df['BRANCH'][item], df['zhengC'][item], df['TYPE'][item], df['DATE'][item], df['Dpos_VIP_FEE'][item], df['Yun'][item], df['wkkj_d_tx'][item], df['wkkj_j_tx'][item], df['qt_ckf'][item], df['wkkj_ckf'][item], df['Dfr'][item], df['ZFB'][item], df['yl2'][item], df['yl2_1k'][item], df['merCode'][item]),
                               "update TBL_FEE set ZFWK_CREDIT_COMMISION_VALUE='%s',ZFWK_COMMISION_VALUE='%s',QWKKJ_CREDIT_COMMISION_VALUE='%s',QWKKJ_COMMISION_VALUE='%s',WSZF_COMMISION_VALUE='%s',WSZF_CREDIT_COMMISION_VALUE='%s',SZYL_MER_COMMISION_VALUE='%s',QKJ_COMMISION_VALUE='%s' where MERCODE='%s'" % (df['wkkj_all'][item],df['wkkj_all'][item],df['wkkj_all'][item],df['wkkj_all'][item],df['wkkj_all'][item],df['wkkj_all'][item],df['wkkj_all'][item],df['wkkj_all'][item],df['merCode'][item]),
                               "update tbl_merchant_collect_fee set UNIONPAY_COST1='%s',PROXY_PROFIT1='%s',DAI_UNIONPAY_COST='%s',DAI_PROXY_PROFIT='%s',DZ_PROXY='10.000',VIP_COST='%s',VIP_PROFIT='%s',YUNFU_UNION_FEE='%s',YUNFU_PROXY_FEE='%s',UNIONPAY_COST2='%s', PROXY_PROFIT2='%s' where MER_CODE='%s'" % (df['JieCb'][item],df['JieFr'][item],df['DaiCb'][item],df['DaiFr'][item],df['Dpos_VIP_COST'][item],df['Dpos_VIP_PROFIT'][item],df['Yun_cb'][item],df['Yun_fr'][item],df['Jcf'][item],df['Jff'][item],df['merCode'][item]),
                               "update tbl_withdraw_cash_merchant set MERCHANT_STATE='0',REDUCTIONMONEY='%s' where MER_CODE='%s'" % (df['PosCharge'][item], df['merCode'][item])
                               ]
                    sql06 = ["update tbl_mer_info set MER_COMMISION_VALUE='%s'where MER_CODE='%s'" % (df['Jie'][item], df['merCode'][item])]
                    print('\n'+'=========================================================执行商户号：', df['merCode'][item], "=========================================================")
                    for i in sql_pos:
                        try:
                            DemoOracle().update(i)
                            print(i)
                        except:
                            DemoOracle().rollback()
                            print('sql执行错误1')
                    for j in sql06:
                        try:
                            DemoOracle100().update(j)
                            print(j)
                        except:
                            DemoOracle100().rollback()
                            print('sql执行错误2')
                else:
                    print('{0}是无效商户号'.format(df['merCode'][item]))
            elif res[0] == '923':
                sql1 = "select a.mer_code, b.mercode, c.mer_code, m.mer_code from TBL_INVENTORY_MANAGEMENT a left join tbl_fee b on a.mer_code = b.mercode left join TBL_MERCHANT_COLLECT_FEE c on b.mercode = c.mer_code left join swtonlineb.tbl_mer_info m on m.mer_code = a.mer_code where a.machine_state = 1 and a.mer_code is not null and b.mercode is not null and c.mer_code is not null and m.mer_code is not null and a.mer_code='%s' order by a.create_date desc" % (df['merCode'][item])
                res1 = DemoOracle().select_all(sql1)
                if len(res1[0]) >= 4:  # 判断是否有效
                    """修改政策数据: sql2:修改Mpos库存表, sql3：修改费表, sql4：修改商户信息表借记卡费率,
                    sql5：修改成本表, sql6：修改星劵成本表, sql7：修改提现费表, sql_m_pos:02,03,05,06,07
                    """
                    sql_m_pos =["update TBL_INVENTORY_MANAGEMENT set CASH_BACK_STATE='%s',USER_NAME2='%s',BRANCH='%s',UPDATE_DATE='%s',CREATE_DATE='%s',CASH_BACK_DATE='%s',STAR_VOUCHER_FEE='%s',MER_SIGN_COMMISION_VALUE='%s',VIP_FEE='%s',VIP_COST='%s',STAR_VOUCHER_COST='%s',MER_SIGN_WITHDRAW_FEE='%s',AGENT_COST_COMMISION_VALUE='%s',AGENT_COST_WITHDRAW_FEE='%s' where MER_CODE='%s'"  % (df['zhengC'][item],df['user2'][item],df['BRANCH'][item],df['DATE'][item],df['CDate'][item],df['DATE'][item],df['XJ'][item],df['Dai'][item],df['Mpos_VIP_FEE'][item],df['DaiCb'][item],df['XJ_cb'][item],df['MposCharge'][item],df['DaiCb'][item],df['MposCost'][item],df['merCode'][item]),
                                "update TBL_FEE set USERNAME2='%s',AMOUNT='%s',DAI_COMMISION_VALUE='%s',BRANCH='%s',CASH_BACK_STATE='%s',MERCHANT_TYPE='2',CREATE_DATE='%s',VIP_FEE='%s',YUNFU_FEE='%s',STAR_VOUCHER_FEE='%s',qyl_commision_value='%s',qyl_thousand_value='%s',qwkkj_commision_value='%s',qwkkj_credit_commision_value='%s',DAI_AMOUNT='%s',Fee_New_State=3 where MERCODE='%s'" % (df['user2'][item],df['AMOUNT'][item],df['Dai'][item],df['BRANCH'][item],df['zhengC'][item],df['CDate'][item],df['Mpos_VIP_FEE'][item],df['Yun'][item],df['XJ'][item],df['yl2'][item],df['yl2_1k'][item],df['wkkj_j'][item],df['wkkj_d'][item],df['Dfr'][item],df['merCode'][item]),
                                "update tbl_merchant_collect_fee set UNIONPAY_COST1='%s',PROXY_PROFIT1='%s',DAI_UNIONPAY_COST='%s',DAI_PROXY_PROFIT='%s',DZ_PROXY='10.000',VIP_COST='%s',VIP_PROFIT='%s',YUNFU_UNION_FEE='%s',YUNFU_PROXY_FEE='%s',WSZF_CREDIT_COST='%s',WSZF_COST='%s' where MER_CODE='%s'" % (df['JieCb'][item],df['JieFr'][item],df['DaiCb'][item],df['DaiFr'][item],df['Mpos_VIP_COST'][item],df['Mpos_VIP_PROFIT'][item],df['Yun_cb'][item],df['Yun_fr'][item],df['wkkj_j_cb'][item],df['wkkj_d_cb'][item],df['merCode'][item]),
                                "update tbl_merchant_collect_fee set star_voucher_cost='%s',star_voucher_profit='%s' where MER_CODE='%s'" % (df['XJ_cb'][item], df['XJ_fr'][item], df['merCode'][item]),
                                "update tbl_withdraw_cash_merchant set MERCHANT_STATE='0',NEW_SPECIAL_VALUE='%s' where MER_CODE='%s'" % (df['MposCharge'][item], df['merCode'][item])
                                ]
                    sql4 = ["update tbl_mer_info set MER_COMMISION_VALUE='%s' where MER_CODE='%s'" % (df['Jie'][item], df['merCode'][item])]
                    print('\n'+'=========================================================执行商户号：', df['merCode'][item],"=========================================================")
                    for x in sql_m_pos:
                        try:
                            DemoOracle().update(x)
                            print(x)
                        except:
                            DemoOracle().close()
                            print('sql执行错误1')
                    for y in sql4:
                        try:
                            DemoOracle100().update(y)
                            print(y)
                        except:
                            DemoOracle100().rollback()
                            print('sql执行错误2')
                else:
                    print('{0}是无效商户号'.format(df['merCode'][item]))
            elif res[0] == '922':
                print('{0}:922商户'.format(df['merCode'][item]))
            else:
                print("不存在这类商户号")
        except:
            DemoOracle().rollback()
            print('SQL语句执行错误3')
        finally:
            DemoOracle().close()
            DemoOracle100().close()

data()


