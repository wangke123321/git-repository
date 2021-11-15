from xml.dom.minidom import parse, parseString


class RealXml:
    @staticmethod
    def xml_file(file, value):
        dom = parseString(file)
        return_text = dom.getElementsByTagName(value)[0].firstChild.nodeValue
        returns = return_text.split()[0]
        if returns == '00':
            print('交易成功')
        elif returns == '01':
            print("md5错误")
        elif returns == '02':
            print("不是秒到商户,提现业务-查询提现商户-添加")
        elif returns == '03':
            print("不在提现时间范围内")
        elif returns == '04':
            print("没有查到该笔记录")
        elif returns == '05':
            print("刷卡卡号没有认证")
        elif returns == '06':
            print("重复")
        elif returns == '07':
            print("没有该刷卡头信息")
        elif returns == '08':
            print("该刷卡头没有绑定默认收款人")
        elif returns == '09':
            print("该收款号已超额,该收款号已超额==原因：提现金额 > 总交易金额-已提现金额，检查100库当天交易AB表总交易金额，提现表已成功提现金额")
        elif returns == '10':
            print("提现金额错误,提现金额错误==原因：(1)传入金额小于10块 （2）")
        elif returns == '11':
            print("数据添加失败")
        elif returns == '12':
            print("没有接受到请求数据")
        elif returns == '13':
            print("请求码错误")
        elif returns == '99':
            print("秒到异常")
        else:
            print('服务器错误')

    @staticmethod
    def xml_file_mpos(file, value):
        dom = parseString(file)
        return_text = dom.getElementsByTagName(value)[0].firstChild.nodeValue
        returns = return_text.split()[0]
        if returns == '00':
            print('交易成功')
        elif returns == '01':
            print("交易金额不正确")
        elif returns == '02':
            print("不在提现时间内")
        elif returns == '03':
            print("该刷卡头没有绑定默认收款人")
        elif returns == '04':
            print("查询不到默认收款人信息")
        elif returns == '05':
            print("该商户还有交易在审批中")
        elif returns == '06':
            print("刷卡头信息为空")
        elif returns == '07':
            print("当月累计超限")
        elif returns == '08':
            print("当天累计超限")
        elif returns == '09':
            print("结算金额有误小于0，不结算")
        elif returns == '10':
            print("未找到对应数据")
        elif returns == '11':
            print("单笔金额超100万")
        elif returns == '12':
            print("MD5加密错误")
        elif returns == '13':
            print("没有查到该笔交易")
        elif returns == '14':
            print("交易金额小于3元，不结算")
        elif returns == 'A6':
            print("代付成功，卡已过期，请重新认证")
        else:
            print('服务器错误')

if __name__ == '__main__':
    body = '<?xml version="1.0" encoding="UTF-8"?><S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/"><S:Body><ns2:withdrawCashResponse xmlns:ns2="http://mpos.zf/"><return>00</return><retur2>01</retur2></ns2:withdrawCashResponse></S:Body></S:Envelope>'
    RealXml.xml_file(body, 'retur2')