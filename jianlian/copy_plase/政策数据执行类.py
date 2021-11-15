import pandas as pd
from jlapi.Ocracle.swtonline import HandleOracle
def csvControl():
    df = pd.read_csv('Data/政策批量修改数据.csv')
    df = pd.DataFrame(df)
    for j in range(len(df['merCode'])):
        try:
            # 提取有效的商户号
            sql = "select a.mer_code, b.mercode, c.mer_code, m.mer_code from TBL_INVENTORY_MANAGEMENT_posp a left join tbl_fee b on a.mer_code = b.mercode left join TBL_MERCHANT_COLLECT_FEE c on b.mercode = c.mer_code left join swtonlineb.tbl_mer_info m on m.mer_code = a.mer_code where a.machine_state = 1 and a.mer_code is not null and b.mercode is not null and c.mer_code is not null and m.mer_code is not null and a.mer_code='%s' order by a.create_date desc" % (df['merCode'][j])
            merCode01 = HandleOracle().find_all(sql)
            if len((merCode01)[0]) >= 4:
                print(str(df['merCode'][j])+'有效商户号')
            sql1 = [
                    "update TBL_INVENTORY_MANAGEMENT_posp set CASH_BACK_STATE='%s',USER_NAME2='%s',BRANCH='%s',MACHINE_ACTIVATE_DATE='%s',CREATE_DATE='%s' where MER_CODE='%s'" % (df['zhengC'][j], df['user2'][j], df['BRANCH'][j], df['DATE'][j], df['CDate'][j], df['merCode'][j]),
                    "update TBL_FEE set USERNAME2='%s',AMOUNT='%s',DAI_COMMISION_VALUE='%s',BRANCH='%s',CASH_BACK_STATE='%s',MERCHANT_TYPE='%s',CREATE_DATE='%s',VIP_FEE='%s',YUNFU_FEE='%s',WKKJ_TX_VALUE='%s',WKKJ_CREDIT_TX_VALUE='%s',OUT_FEE='%s',OUT_FEE_WSZF='%s',qwkkj_commision_value='%s',qwkkj_credit_commision_value='%s',DAI_AMOUNT='%s'，WSZF_COMMISION_VALUE='%s',WSZF_CREDIT_COMMISION_VALUE='%s',SZYL_MER_COMMISION_VALUE='%s'  where MERCODE='%s'" % (df['user2'][j], df['AMOUNT'][j], df['Dai'][j], df['BRANCH'][j], df['zhengC'][j], df['TYPE'][j],df['DATE'][j], df['Dpos_VIP_FEE'][j], df['Yun'][j], df['wkkj_d_tx'][j], df['wkkj_j_tx'][j],df['qt_ckf'][j], df['wkkj_ckf'][j], df['wkkj_j'][j], df['wkkj_d'][j], df['Dfr'][j],df['WSZF_COMMISION_VALUE'][j], df['WSZF_CREDIT_COMMISION_VALUE'][j], df['SZYL_MER_COMMISION_VALUE'][j],df['merCode'][j]),
                    "update tbl_merchant_collect_fee set UNIONPAY_COST1='%s',PROXY_PROFIT1='%s',DAI_UNIONPAY_COST='%s',DAI_PROXY_PROFIT='%s',DZ_PROXY='10.000',VIP_COST='%s',VIP_PROFIT='%s',YUNFU_UNION_FEE='%s',YUNFU_PROXY_FEE='%s',UNIONPAY_COST2='%s', PROXY_PROFIT2='%s'，WSZF_CREDIT_COST='%s',WSZF_COST='%s' where MER_CODE='%s'" % (df['JieCb'][j], df['JieFr'][j],df['DaiCb'][j], df['DaiFr'][j], df['Dpos_VIP_COST'][j], df['Dpos_VIP_PROFIT'][j], df['Yun_cb'][j], df['Yun_fr'][j], df['Jcf'][j], df['Jff'][j], df['wkkj_d_cb'][j], df['wkkj_j_cb'][j], df['merCode'][j],),
                    "update tbl_withdraw_cash_merchant set MERCHANT_STATE='0',REDUCTIONMONEY='%s' where MER_CODE='%s'"%(df['PosCharge'][j], df['merCode'][j])
                    ]
            sql2 = ["update tbl_mer_info set MER_COMMISION_VALUE='%s'where MER_CODE='%s'" % (df['Jie'][j], df['merCode'][j])]
            for one1 in sql1:
                try:
                    HandleOracle().update1(one1)
                    print('数据更新成功')
                except:
                    HandleOracle().rollback()
                    print('语句执行错误')
                HandleOracle().close()
            for one2 in sql2:
                try:
                    HandleOracle().update2(one2)
                    print('数据更新成功')
                except:
                    HandleOracle().rollback()
                    print('语句执行错误')
                HandleOracle().close()
        except IndexError as e:
            print(str(df['merCode'][j])+"无效商户号",e)
if __name__ == '__main__':
    csvControl()