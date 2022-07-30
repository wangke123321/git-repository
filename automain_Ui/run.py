import sys
import time
from web_ui_auto_lib.test_case_lib import *
from web_ui_auto_lib.case_lib import *
from pip._vendor.distlib.compat import raw_input
log = Log()


def my_excepthook(exc_type, exc_value, tb):
    msg = ' Traceback (most recent call last):\n'
    while tb:
        filename: object = tb.tb_frame.f_code.co_filename
        name = tb.tb_frame.f_code.co_name
        lineno = tb.tb_lineno
        msg += ' File "%.500s", line %d, in %.500s\n' % (filename, lineno, name)
        tb = tb.tb_next
        msg += ' %s: %s\n' % (exc_type.__name__, exc_value)
    print(msg)


def start_run(a=1):
    # 执行入口一：
    if a == 1:
        sys.excepthook = my_excepthook
        suite = unittest.TestSuite()
        loader = unittest.TestLoader()
        suite.addTest(loader.loadTestsFromTestCase(TestCalc))
        runner = unittest.TextTestRunner()
        runner.run(suite)
    # 执行入口二：
    else:
        sys.excepthook = my_excepthook
        case_execer().exec_case()


if __name__ == '__main__':
    start_run(2)

# 运行加载模式：生成html报告
# from common.BeautifulReport import BeautifulReport as bf
# import os
# # 测试用例目录
# addTest_path = ConfigReader().get_value("file", "addTest_path")
# # 加载测试用例
# discover = unittest.defaultTestLoader.discover(addTest_path, pattern='test*.py')
# # 测试报告路径
# filepathname = ConfigReader().get_value("file", "report_html_path")
# if not os.path.exists(filepathname):
#     os.mkdir(filepathname)
# filepath = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
# runner = bf(discover)
# runner.report(report_dir=filepathname, filename=filepath, description="自动化测试html页面报告")

