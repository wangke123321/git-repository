import unittest
from jianlian.requests_class.class_mode import Test_Http
from jianlian.class_t1d1_step import CaseT1D1
from jianlian.config.class_config import FileConfig
from jianlian.class_JSBadd import Jsb_Add
from jianlian.tixian_class.credit_card_class import ScanDeal
from jianlian.tomcat_class.tomcat_api import *
from jianlian.project_path.project_path import *
from jianlian.class_update_xml.class_update_xml import UpdateXml


class TetsJianlian(unittest.TestCase):

    def test_T1_Sheng_He(self):
        """T1监控审批接口"""
        url = FileConfig().config('class_config', 'T1_jk', 'url')
        res = Test_Http('post', url, data=None).test_request().json()
        try:
            self.assertEqual(True, res['success'])
        except AssertionError as e:
            print("test_T1_Sheng_He's is {0}", format(e))
            raise e
        print(res)

    def test_jsb(self):
        # 系统时间日期加 +1
        path_1 = 'date ' + DateTime().random_dates(1)
        startServer(path_1)
        time.sleep(5)
        # 启动服务 - 定时包 8080
        path = 'd: && cd D:\\apache-tomcat-7.0.68-8080-11\\bin && startup.bat'
        startServer(path)
        """计算表的调度"""
        url = FileConfig().config(project_tx_url, 'JSB', 'url')
        url_tow = FileConfig().config(project_tx_url, 'JSB', 'url_tow')
        Jsb_Add(url, url_tow).requests_jsb()

    def test_t1(self):
        """T1调度"""
        CaseT1D1.delete_data()
        t1_step = FileConfig().config(project_tx_url, 'MODE', 't1_step')
        t2_step = FileConfig().config(project_tx_url, 'MODE', 't2_step')
        step2_url = FileConfig().config(project_tx_url, 'MODE', 'step2_url')
        step3_url = FileConfig().config(project_tx_url, 'MODE', 'step3_url')
        CaseT1D1(t1_step, t2_step, step2_url, step3_url).test_t1()

    def test_d1(self):
        """D1调度"""
        CaseT1D1.delete_data_d1()
        D1 = FileConfig().config(project_tx_url, 'MODE_D1', 'D1')
        D2 = FileConfig().config(project_tx_url, 'MODE_D1', 'D2')
        CaseT1D1.test_d1(D1, D2)

    def test_tx(self):
        """
        1、mode=all，交替成功和失败；mode=00商户交易都是成功；mode=44商户交易都是失败；不传参数是默认
        2、t1d1=1 是T1商户结算； t1d1=4 是D1商户结算
        3、three='3'删除节假日数据 ；three为空是删除系统时间当天的的数据 """
        # 启动服务 - 自动发布包 8081
        path = 'd: && cd D:\\apache-tomcat-7.0.88-8081\\bin && startup.bat'
        startServer(path)
        # 跑刷卡交易
        url = FileConfig().config(project_tx_url, 'TX', 'get_8081')
        ScanDeal(url).credit_card()
        time.sleep(5)
        # 关闭服务
        time.sleep(5)
        path = 'd: && cd D:\\apache-tomcat-7.0.88-8081\\bin && shutdown.bat'
        shutdown(path)

    def test_t1step(self):
        """刷卡交易提现T1工作日定时结算 今天刷卡，明天结算 """
        # 启动服务 - 自动发布包 8081
        path = 'd: && cd D:\\apache-tomcat-7.0.88-8081\\bin && startup.bat'
        startServer(path)
        # 跑刷卡交易 credit_card 方法中：1、mode=all，交替成功和失败；mode=00商户交易都是成功；mode=44商户交易都是失败；不传参数是默认
        # 2、t1d1=1 是T1商户结算； t1d1=4 是D1商户结算 3、three='3'删除节假日数据 ；three为空是删除系统时间当天的的数据
        url = FileConfig().config(project_tx_url, 'TX', 'get_8081')
        ScanDeal(url).credit_card(t1d1=1)
        # 关闭服务
        # shutdown()
        # 修改 11 包的xml文件中的配置信息 修改 JobStep3 D1Step2Job 文件路径
        file = r'D:\apache-tomcat-7.0.68-8080-11\webapps\PosMerchant\WEB-INF\web.xml'
        UpdateXml.T1D1(file)
        # 系统时间日期加 +1
        path = 'date ' + DateTime().random_dates(1)
        startServer(path)
        # 启动服务 - 11定时包 8080
        path = 'd: && cd D:\\apache-tomcat-7.0.68-8080-11\\bin && startup.bat'
        startServer(path)
        # T1调度 删除三天的T1结算数据 昨天 今天 明天
        CaseT1D1.delete_data()
        t1_step = FileConfig().config('class_config', 'MODE', 't1_step')
        t2_step = FileConfig().config('class_config', 'MODE', 't2_step')
        step2_url = FileConfig().config('class_config', 'MODE', 'step2_url')
        step3_url = FileConfig().config('class_config', 'MODE', 'step3_url')
        CaseT1D1(t1_step, t2_step, step2_url, step3_url).test_t1()
        # 计算表
        url = FileConfig().config(project_tx_url, 'JSB', 'url')
        url_tow = FileConfig().config(project_tx_url, 'JSB', 'url_tow')
        Jsb_Add(url, url_tow).requests_jsb()
        # 修改定时时间
        url = r'D:\apache-tomcat-7.0.68-8080-11\webapps\PosMerchant\WEB-INF\JobStep3.xml'
        UpdateXml.jobstep3(url)
        # 关闭服务 - 11定时包 8080
        path = 'd: && cd D:\\apache-tomcat-7.0.68-8080-11\\bin && shutdown.bat'
        shutdown(path)
        # 启动服务 - 11定时包 8080
        time.sleep(5)
        path = 'd: && cd D:\\apache-tomcat-7.0.68-8080-11\\bin && startup.bat'
        startServer(path)
        # 等待定时结果结算

    def test_t3step(self):
        """刷卡交易提现T1节假日的定时结算"""
        # 启动服务 - 自动发布包 8081 现在是礼拜六
        path = 'd: && cd D:\\apache-tomcat-7.0.88-8081\\bin && startup.bat'
        startServer(path)
        # 跑刷卡交易 credit_card 方法中：1、mode=all，交替成功和失败；mode=00商户交易都是成功；mode=44商户交易都是失败；不传参数是默认
        # 2、t1d1=1 是T1商户结算； t1d1=4 是D1商户结算 3、three='3'删除节假日数据(礼拜五至礼拜一) ；three为空是删除系统时间当天的的数据
        url = FileConfig().config(project_tx_url, 'TX', 'get_8081')
        ScanDeal(url).credit_card(t1d1=1, mode='all', three='3')
        # 关闭服务
        # to_shutdown()
        # 启动服务 - 11定时包 8080 现在是礼拜六
        path = 'd: && cd D:\\apache-tomcat-7.0.68-8080-11\\bin && startup.bat'
        startServer(path)
        # 等待8S
        time.sleep(8)
        # 删除T1节假日结算表的脏数据 礼拜五 礼拜六 礼拜天 礼拜一
        # T1调度 礼拜六结算礼拜五 现在是礼拜六跑礼拜五的调度
        CaseT1D1.delete_data_T3()
        t1_step = FileConfig().config(project_tx_url, 'MODE', 't1_step')
        t2_step = FileConfig().config(project_tx_url, 'MODE', 't2_step')
        step2_url = FileConfig().config(project_tx_url, 'MODE', 'step2_url')
        step3_url = FileConfig().config(project_tx_url, 'MODE', 'step3_url')
        CaseT1D1(t1_step, t2_step, step2_url, step3_url).test_t1()
        # 计算表
        url = FileConfig().config(project_tx_url, 'JSB', 'url')
        url_tow = FileConfig().config(project_tx_url, 'JSB', 'url_tow')
        Jsb_Add(url, url_tow).requests_jsb()
        # 关闭服务 - 11定时包 8080
        path = 'd: && cd D:\\apache-tomcat-7.0.68-8080-11\\bin && shutdown.bat'
        shutdown(path)
        # 停留5S
        time.sleep(5)
        # 系统时间日期加 +1 现在是礼拜日
        path = 'date ' + DateTime().random_dates(1)
        startServer(path)
        # 启动服务 - 11定时包 8080
        path = 'd: && cd D:\\apache-tomcat-7.0.68-8080-11\\bin && startup.bat'
        startServer(path)
        # 等待8S
        time.sleep(8)
        # T1调度 礼拜天结算礼拜六 现在是礼拜日跑礼拜六的调度
        t1_step = FileConfig().config(project_tx_url, 'MODE', 't1_step')
        t2_step = FileConfig().config(project_tx_url, 'MODE', 't2_step')
        step2_url = FileConfig().config(project_tx_url, 'MODE', 'step2_url')
        step3_url = FileConfig().config(project_tx_url, 'MODE', 'step3_url')
        CaseT1D1(t1_step, t2_step, step2_url, step3_url).test_t1()
        # 计算表
        url = FileConfig().config(project_tx_url, 'JSB', 'url')
        url_tow = FileConfig().config(project_tx_url, 'JSB', 'url_tow')
        Jsb_Add(url, url_tow).requests_jsb()
        # 关闭服务 - 11定时包 8080
        path = 'd: && cd D:\\apache-tomcat-7.0.68-8080-11\\bin && shutdown.bat'
        shutdown(path)
        # 停留5S
        time.sleep(5)
        # 系统时间日期加 +1 现在是礼拜一
        path = 'date ' + DateTime().random_dates(1)
        startServer(path)
        # 启动服务 - 11定时包 8080
        path = 'd: && cd D:\\apache-tomcat-7.0.68-8080-11\\bin && startup.bat'
        startServer(path)
        # 等待8S
        time.sleep(8)
        # T1调度 礼拜一结算礼拜日 现在是礼拜一跑礼拜天的调度
        t1_step = FileConfig().config(project_tx_url, 'MODE', 't1_step')
        t2_step = FileConfig().config(project_tx_url, 'MODE', 't2_step')
        step2_url = FileConfig().config(project_tx_url, 'MODE', 'step2_url')
        step3_url = FileConfig().config(project_tx_url, 'MODE', 'step3_url')
        CaseT1D1(t1_step, t2_step, step2_url, step3_url).test_t1()
        # 计算表
        url = FileConfig().config(project_tx_url, 'JSB', 'url')
        url_tow = FileConfig().config(project_tx_url, 'JSB', 'url_tow')
        Jsb_Add(url, url_tow).requests_jsb()
        # 修改 11 包的xml文件中的配置信息 修改 JobStep3 D1Step2Job 文件路径
        file = r'D:\apache-tomcat-7.0.68-8080-11\webapps\PosMerchant\WEB-INF\web.xml'
        UpdateXml.T1D1(file)
        # 修改定时时间
        url = r'D:\apache-tomcat-7.0.68-8080-11\webapps\PosMerchant\WEB-INF\JobStep3.xml'
        UpdateXml.jobstep3(url)
        # 关闭服务 - 11定时包 8080
        path = 'd: && cd D:\\apache-tomcat-7.0.68-8080-11\\bin && shutdown.bat'
        shutdown(path)
        # 停留8S
        time.sleep(8)
        # 启动服务 - 11定时包 8080
        path = 'd: && cd D:\\apache-tomcat-7.0.68-8080-11\\bin && startup.bat'
        startServer(path)
        # 等待定时结果结算

    def test_d1step(self):
        """刷卡交易提现D1工作日定时结算 今天刷卡，明天结算 """
        # 启动服务 - 自动发布包 8081
        path = 'd: && cd D:\\apache-tomcat-7.0.88-8081\\bin && startup.bat'
        startServer(path)
        # 跑刷卡交易 credit_card 方法中：1、mode=all，交替成功和失败；mode=00商户交易都是成功；mode=44商户交易都是失败；不传参数是默认
        # 2、t1d1=1 是T1商户结算； t1d1=4 是D1商户结算 3、three='3'删除节假日数据 ；three为空是删除系统时间当天的的数据
        url = FileConfig().config(project_tx_url, 'TX', 'get_8081')
        ScanDeal(url).credit_card(mode='all', t1d1=4)
        # 关闭服务
        # shutdown()
        # 修改 11 包的xml文件中的配置信息 修改 JobStep3 D1Step2Job 文件路径
        file = r'D:\apache-tomcat-7.0.68-8080-11\webapps\PosMerchant\WEB-INF\web.xml'
        UpdateXml.T1D1(file)
        # 系统时间日期加 +1
        path = 'date ' + DateTime().random_dates(1)
        startServer(path)
        # 启动服务 - 11定时包 8080
        path = 'd: && cd D:\\apache-tomcat-7.0.68-8080-11\\bin && startup.bat'
        startServer(path)
        # 延时5S
        time.sleep(5)
        # D1调度 删除D1结算数据  今天 和 昨天  今天是结算日期 昨天是交易日期
        CaseT1D1.delete_data_d1()
        D1 = FileConfig().config(project_tx_url, 'MODE_D1', 'D1')
        D2 = FileConfig().config(project_tx_url, 'MODE_D1', 'D2')
        CaseT1D1.test_d1(D1, D2)
        # 计算表
        url = FileConfig().config(project_tx_url, 'JSB', 'url')
        url_tow = FileConfig().config(project_tx_url, 'JSB', 'url_tow')
        Jsb_Add(url, url_tow).requests_jsb()
        # 修改定时时间
        url = r'D:\apache-tomcat-7.0.68-8080-11\webapps\PosMerchant\WEB-INF\D1Step2Job.xml'
        UpdateXml.D1Step2Job(url)
        # 关闭服务 - 11定时包 8080
        path = 'd: && cd D:\\apache-tomcat-7.0.68-8080-11\\bin && shutdown.bat'
        shutdown(path)
        # 启动服务 - 11定时包 8080
        time.sleep(5)
        path = 'd: && cd D:\\apache-tomcat-7.0.68-8080-11\\bin && startup.bat'
        startServer(path)
        # 等待定时结果结算






