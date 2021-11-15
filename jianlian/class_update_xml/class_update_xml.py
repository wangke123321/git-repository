from xml.dom.minidom import parse, parseString
from xml.etree import ElementTree
from jianlian.timeclass.class_time import DateTime
from jianlian.config.class_config import FileConfig


class UpdateXml:
    @staticmethod
    def jobstep3(url):
        """T1结算定时"""
        domtree = parse(url)
        # 文档根元素
        rootnode = domtree.documentElement
        names = rootnode.getElementsByTagName("value")
        data = []
        for i in range(len(names)):
            data.append(i)
        test_data = data[1]
        res = names[test_data].firstChild.data
        for name in names:
            if name.childNodes[0].data == res:
                pn = name.parentNode
                phone = pn.getElementsByTagName("value")[0]
                data = DateTime().random_minutes(3) + ' * * ? *'  # 电脑时间+3分钟
                phone.childNodes[0].data = data
                print('定时更新为：{}'.format(data))
        with open(url, 'w+', encoding='utf-8') as f:
            # 缩进 - 换行 - 编码
            domtree.writexml(f, addindent='')

    @staticmethod
    def D1Step2Job(url):
        """D1结算定时"""
        domtree = parse(url)
        # 文档根元素
        rootnode = domtree.documentElement
        names = rootnode.getElementsByTagName("value")
        data = []
        for i in range(len(names)):
            data.append(i)
        test_data = data[1]
        res = names[test_data].firstChild.data
        for name in names:
            if name.childNodes[0].data == res:
                pn = name.parentNode
                phone = pn.getElementsByTagName("value")[0]
                data = DateTime().random_minutes(3) + ' * * ? *'  # 电脑时间+3分钟
                phone.childNodes[0].data = data
                print('定时更新为：{}'.format(data))

        with open(url, 'w+', encoding='utf-8') as f:
            # 缩进 - 换行 - 编码
            domtree.writexml(f, addindent='')

    @staticmethod
    def WxZfbSettJob(url):
        """扫码T1结算 POS类型的结算定时"""
        domtree = parse(url)
        # 文档根元素
        rootnode = domtree.documentElement
        names = rootnode.getElementsByTagName("value")
        data = []
        for i in range(len(names)):
            data.append(i)
        test_data = data[1]
        res = names[test_data].firstChild.data
        for name in names:
            if name.childNodes[0].data == res:
                pn = name.parentNode
                phone = pn.getElementsByTagName("value")[0]
                data = DateTime().random_minutes(3) + ' * * ? *'  # 电脑时间+3分钟
                phone.childNodes[0].data = data
                print('定时更新为：{}'.format(data))

        with open(url, 'w+', encoding='utf-8') as f:
            # 缩进 - 换行 - 编码
            domtree.writexml(f, addindent='')

    def mode(self):
        domTree = parse("customer.xml")  # 定位xml文件
        rootNode = domTree.documentElement  # 获取XML文档对象
        names = rootNode.getElementsByTagName("name")  # 获取标签之间的数据 定位 <name>Acme Inc.</name>
        # 如果定位 <customer ID="C001"> 标签属性值 用 names = rootNode.getAttribute('name')
        for name in names:
            if name.childNodes[0].data == "Acme Inc.":
                # 获取到name节点的父节点
                pn = name.parentNode
                # 父节点的phone节点，其实也就是name的兄弟节点
                phone = pn.getElementsByTagName("phone")[0]
                # 更新phone的取值
                phone.childNodes[0].data = 99999

        with open('customer.xml', 'w', encoding='utf-8') as f:
            # 缩进 - 换行 - 编码
            domTree.writexml(f, addindent=' ')

    @staticmethod
    def replace_xml(url, values):  # 'values = '/WEB-INF/JobStep3.xml'
        """替换单个文件配置"""
        domtree = parse(url)
        # 文档根元素
        rootnode = domtree.documentElement
        names = rootnode.getElementsByTagName("param-value")
        data = []
        for i in range(len(names)):
            data.append(i)
        test_data = data[0]
        res = names[test_data].firstChild.data
        # values = '/WEB-INF/JobStep3.xml'
        for name in names:
            if name.childNodes[0].data == res:
                pn = name.parentNode
                phone = pn.getElementsByTagName("param-value")[0]
                if res.find(values) != -1:  # xml文件存在 values 的定时 =-1 是不存在
                    print('已经存在{}定时,无需替换'.format(values))
                else:
                    code = res.replace(res.split(',')[1], data)
                    phone.childNodes[0].data = code
                    print('定时更新为：{}'.format(code))

        with open(url, 'w+', encoding='utf-8') as f:
            # 缩进 - 换行 - 编码
            domtree.writexml(f, addindent='')

    @staticmethod
    def T1D1(url):
        """替换t1d1的web文件配置"""
        domtree = parse(url)
        # 文档根元素
        rootnode = domtree.documentElement
        names = rootnode.getElementsByTagName("param-value")
        data = []
        for i in range(len(names)):
            data.append(i)
        test_data = data[0]
        res = names[test_data].firstChild.data
        values = {'job3': '/WEB-INF/JobStep3.xml', 'd1': '/WEB-INF/D1Step2Job.xml'}
        for name in names:
            if name.childNodes[0].data == res:
                pn = name.parentNode
                phone = pn.getElementsByTagName("param-value")[0]
                if res.find(values['job3']) != -1 and res.find(values['d1']) != -1:  # xml文件存在 values 的定时 =-1 是不存在
                    print('web.xml文件已经存在JobStep3和D1Step2Job的定时,无需替换')
                else:
                    T1 = res.replace(res.split(',')[1], values['job3'])
                    print('修改web文件JobStep3的定时成功')
                    d1 = T1.replace(T1.split(',')[2], values['d1'])
                    print('修改web文件D1Step2Job的定时成功')
                    phone.childNodes[0].data = d1
                    print('定时更新为：{}'.format(d1))

        with open(url, 'w+', encoding='utf-8') as f:
            # 缩进 - 换行 - 编码
            domtree.writexml(f, addindent='')

if __name__ == '__main__':
    """T1结算"""
    # url = r'D:\apache-tomcat-7.0.68-8080-11\webapps\PosMerchant\WEB-INF\D1Step2Job.xml'
    # T1_url = FileConfig().conf('../class_config', 'settlement', 'T1_url')
    # UpdateXml.jobstep3(url)
    """D1结算"""
    # D1_url = FileConfig().conf('../class_config', 'settlement', 'D1_url')
    # UpdateXml.D1Step2Job(D1_url)
    """扫码T1结算 POS类型的结算"""
    # T1_url_sm = FileConfig().conf('../class_config', 'settlement', 'T1_url_sm')
    # UpdateXml.WxZfbSettJob(T1_url_sm)
    """查询替换单个配置文件名称 例如：web.xml 中的配置文件名称"""
    # file = r'D:\apache-tomcat-7.0.68-8080-11\webapps\PosMerchant\WEB-INF\web.xml'
    # values = '/WEB-INF/JobStep3.xml'
    # UpdateXml.replace_xml(file, values)
    """修改 web.xml 中的配置jobstep3和D1Step2Job名称"""
    # file = r'D:\apache-tomcat-7.0.68-8080-11\webapps\PosMerchant\WEB-INF\web.xml'
    # UpdateXml.T1D1(file)


