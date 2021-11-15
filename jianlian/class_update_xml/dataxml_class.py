from xml.dom.minidom import parse, parseString

class RealXml:
    @staticmethod
    def xml_file(file, value):
        dom = parseString(file)
        return_text = dom.getElementsByTagName(value)[0].firstChild.nodeValue
        returns = return_text.split()[0]
        return returns

if __name__ == '__main__':
    # body = '<?xml version="1.0" encoding="UTF-8"?><S:Envelope xmlns:S="http://schemas.xmlsoap.org/soap/envelope/"><S:Body><ns2:withdrawCashResponse xmlns:ns2="http://mpos.zf/"><return>00</return><retur2>01</retur2></ns2:withdrawCashResponse></S:Body></S:Envelope>'
    # ll = RealXml.xml_file(body, 'retur2')
    # print(ll)
    file = r'D:\apache-tomcat-7.0.68-8080-11\webapps\PosMerchant\WEB-INF\web.xml'
    value = 'param-value'
    webxml = RealXml.xml_file(file, value)
    print(webxml)