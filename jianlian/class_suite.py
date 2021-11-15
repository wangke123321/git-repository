import sys
sys.path.append(r"E:\python\project")
sys.path.append(r"D:\python\Lib\site-packages")
sys.path.append(r"D:\python\Lib")
sys.path.append(r"C:\Users\ZF-JS\AppData\Roaming\Python\Python38\site-packages")
sys.path.append(r"D:\pycharm\PyCharm Community Edition 2021.1.1\plugins\python-ce\helpers\typeshed\stdlib")
sys.path.append(r"D:\oracleclient\oracleclient\instantclient_11_2")

# import sys
# sys.path.append("E:\\python\\project")
# sys.path.append("D:\\python\\Lib\\site-packages")
# sys.path.append("D:\\python\\Lib")
# sys.path.append("C:\\Users\\ZF-JS\\AppData\\Roaming\\Python\\Python38\\site-packages")
# sys.path.append("D:\\pycharm\\PyCharm Community Edition 2021.1.1\\plugins\\python-ce\\helpers\\typeshed\\stdlib\\")
# sys.path.append("D:\\oracleclient\\oracleclient\\instantclient_11_2\\")
# sys.path.append('E:\\新建文件夹\\PLSQL Developer\\')
# sys.path.append("C:\\Users\\ZF-JS\\AppData\\Local\\JetBrains\\PyCharmCE2021.1\\python_stubs\\-287100998")
# sys.path.append('D:\\oracleclient\\oracleclient\\instantclient_11_2')

import unittest
from jianlian.classs_api import TetsJianlian

suite = unittest.TestSuite()
loder = unittest.TestLoader()


"""执行计算表用例"""
# suite.addTest(TetsJianlian('test_jsb'))  # 计算表
# with open('jisuanbiao.txt', 'w+', encoding='UTF-8') as file:
#     runner = unittest.TextTestRunner(stream=file, verbosity=2)
#     runner.run(suite)

"""执行T1监控审核的用例"""
# suite.addTest(TetsJianlian('test_T1_Sheng_He'))
# with open('jisuanbiao.txt', 'w+', encoding='UTF-8') as file:
#     runner = unittest.TextTestRunner(stream=file, verbosity=2)
#     runner.run(suite)

"""刷卡交易提现"""
suite.addTest(TetsJianlian('test_tx'))
with open('tixianz.txt', 'w+', encoding='utf-8') as file:
    runner = unittest.TextTestRunner(stream=file, descriptions=True, verbosity=1)
    runner.run(suite)

"""刷卡交易提现T1工作日定时结算"""
# suite.addTest(TetsJianlian('test_t1step'))
# with open('tixianz.txt', 'w+', encoding='utf-8') as file:
#     runner = unittest.TextTestRunner(stream=file, descriptions=True, verbosity=1)
#     runner.run(suite)

"""刷卡交易提现T1节假日的定时结算"""
# suite.addTest(TetsJianlian('test_t3step'))
# with open('tixianz.txt', 'w+', encoding='utf-8') as file:
#     runner = unittest.TextTestRunner(stream=file, descriptions=True, verbosity=1)
#     runner.run(suite)

"""刷卡交易提现D1定时结算"""
# suite.addTest(TetsJianlian('test_d1step'))
# with open('tixianz.txt', 'w+', encoding='utf-8') as file:
#     runner = unittest.TextTestRunner(stream=file, descriptions=True, verbosity=1)
#     runner.run(suite)