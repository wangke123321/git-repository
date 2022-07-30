from common.config import *
import importlib
from common.log import Log
from web_ui_auto_lib.element_behavior_handlers.check_behavior_handler import checkBehaviorHandler
from module.excel_case_reader import *
from common.data_process import RandomInfo
from common.data_process import FileOperate
from common.Base import ExecuteCase
from common.Base import BaseMethod
import time
import datetime
import unittest


class TestCalc(unittest.TestCase):
    """  csv 日志名称  """
    filepathname = ConfigReader().get_value("file", "report_file_path") + datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

    def setup(self):
        """ 开始测试 """

    def test_exec_case(self):
        """ 集成加载Case """
        self.log = Log()
        self.bm = BaseMethod()
        self.ec = ExecuteCase()
        self.staff_file_path = ConfigReader().get_value("file", "staff_file_path")  # json文件数据
        self.report_file_path = ConfigReader().get_value("file", "report_file_path")  # csv日志路径
        self.fileoperate = FileOperate()
        self.checkbehaviorhandler = checkBehaviorHandler()
        self.runstatus_file_path = ConfigReader().get_value("file", "runstatus_file_path")  # 返回一个状态为1的csv文件

        case = ExcelCaseReader().read_case()
        excel_title = f'Step,OperationPage,Description,CaseResult'
        self.fileobj = self.fileoperate.writefile(self.filepathname + ".csv", "csv", excel_title, "a+")
        for step in case.caseSteps:  # case.caseSteps EXCEL中的用例的步骤数 从1开始
            step.WaitTime = 1 if step.WaitTime == "" else step.WaitTime  # 等待操作，默认为空等待1S，否则为其本身
            step.Enabled = 1 if step.Enabled == "" else step.Enabled  # 执行操作，默认为空执行 否则为其本身
            step.IgnoreErr = 1 if step.IgnoreErr == "" else step.IgnoreErr  # 断言执行操作，默认为空执行断言 否则为其本身
            self.log.logMsg(4, f'step{int(step.Step)}: {int(step.Step)},{step.Behavior},{step.Description},{step.OperationPage},{step.PositioningExpression},{step.InputValue},{step.OutputValue},{step.ExpectedResult},{int(step.WaitTime)},{int(step.Enabled)},{int(step.IgnoreErr)},{int(step.LoopCnt)}')
            if step.Enabled == 1:  # 执行操作
                if step.Behavior != "check":  # 如果在excel的操作选项中不包含 check
                    module_name = "web_ui_auto_lib." + "element_behavior_handlers." + step.Behavior + "_behavior_handler"  # 引用各个操作文件的绝对路径
                    class_name = step.Behavior + "BehaviorHandler"  # 引用所有操作中的类名字
                    module = importlib.import_module(module_name)  # 利用 import_module 函数返回为一个类对象
                    aclass = getattr(module, class_name)  # 利用反射，获取所有操作类
                    time.sleep(int(step.WaitTime))  # 强制等待
                    handle_behavior = getattr(aclass, "handle_behavior")  # 利用反射，获取所有操作类下面的 BehaviorHandler 方法
                    returnvalue = handle_behavior(aclass(), self.bm, step)  # 调用所有操作类下的 handle_behavior 函数获取到返回 状态
                    # 统计部分 self.total, self.success, self.fail：总计 成功 失败，写入CSV文件
                    self.total, self.success, self.fail = self.ec.casesResult(self.bm, step, self.fileobj, returnvalue, TestCalc.filepathname)
                    # 断言部分  returnvalue，返回状态 0：成功  1：失败  -1：报错
                    self.ec.log_output(step, returnvalue, None, None)
                else:
                    time.sleep(int(step.WaitTime))
                    handle_behavior = getattr(checkBehaviorHandler, "handle_behavior")
                    returnvalue = handle_behavior(checkBehaviorHandler, self.bm, step)
                    self.total, self.success, self.fail = self.ec.casesResult(self.bm, step, self.fileobj, returnvalue, TestCalc.filepathname)
                    self.ec.log_output(step, returnvalue, checkBehaviorHandler.actual, checkBehaviorHandler.expected)
                    checkBehaviorHandler.actual = None
                    checkBehaviorHandler.expected = None
            else:
                self.log.logMsg(3, "case ignore")
                self.ignore = self.ec.casesResultignore()
            if len(case.caseSteps) - case.caseSteps.index(step) == 1:  # case.caseSteps.index 用例索引数 从0开始 所以默认=1
                self.ec.runstatus_tofile(self.runstatus_file_path, 1, step)  # 跑完之后返回状态为 1 的CSV文件
        self.log.logMsg(4, "global dictionary：{}".format(RandomInfo().publicDict))  # 打印全局变量
        self.ec.runreslut_count()  # 统计的功能 总计，成功，失败

    def tearDown(self):
        """ 结束测试 """