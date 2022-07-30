from interfaces.ibehavior_handler import *
from common.Base import ExecuteCase
import re


class WebCheckHandler(IBehaviorHandler):
    def handle_check(self, bm, step: CaseStep):
        actual = None  # 实际结果
        expected = None  # 预期结果
        result = 1  # 结果
        try:
            ele = bm.find_ele(step.PositioningExpression)
            if ele is None:
                return -1, actual, expected  # -1 None None
            actual = ele.text
            params = re.findall(r'\${([\s\S]+?)\}', step.ExpectedResult)  # Start Date: ${QueryStartDate};
            if len(params):  # 如果断言字段 包含${} 进入iF 否则不进入
                expected_result = ExecuteCase().relevantParams(step.ExpectedResult)  # 取${QueryStartDate}的值
                step.ExpectedResult = expected_result  # step.ExpectedResult = Start Date: 2021-05-05;
            self.expected = step.ExpectedResult  # 预期结果是 Start Date:2021-05-05  -->预期结果 实际的数字
            if actual == self.expected:
                result = 0  # 0 !None !None
        except:
            result = 1  # 1 !None !None
        return result, actual, self.expected

# from interfaces.icheck_handler import *
# import re
# from common.base import ExecuteCase
#
# class WebCheckHandler(ICheckHandler):
#
#     def __init__(self):
#         pass
#
#     def handle_check(self, selenium_wd_class, step: CaseStep):
#         actual = None  # Username is required
#         expected = None  # Start Date: 2021-05-05 或者是 Login failed
#         result = 1
#         try:
#             ele = selenium_wd_class.find_ele(step.PositioningExpression)  # 表达式 //*[contains(text(),'Username is required')]
#             if ele is None:
#                 return -1,actual,expected  # 查找元素定位表达式找不到 返回值 -1 None None
#
#             actual = ele.text  # Username is required
#             params = re.findall(r'\${([\s\S]+?)\}', step.ExpectedResult)  # Start Date: ${QueryStartDate}; Login failed
#             # 提取出来后是：=:Username is required 或者 Start Date: ${QueryStartDate}
#             if len(params):  # 其中如果 断言字段 包含${} 进入iF 否则不进入
#                 expectedresult = ExecuteCase().relevantParams(step.ExpectedResult) # 取${QueryStartDate}的值
#                 step.ExpectedResult=expectedresult  # step.ExpectedResult = Start Date: 2021-05-05
#             expecteds = step.ExpectedResult.split(":")  # 分割后 ：变成 Start Date 和 2021-05-05  两个部分
#             lens = len(expecteds)
#             expected = ""
#             if lens > 1:
#                 i = 1
#                 while i < lens:
#                     expected += expecteds[i] + ":"  # 提取出最后一个 2021-05-05 并加上:  最后 ==》 expected = 2021-05-05:
#                     i += 1
#             else:
#                 return -1
#
#             self.expected = expected.strip(":")  # 2021-05-05
#             if expecteds[0] == "=" and expected == "calc":  # =:calc
#                 vals = step.InputValue.split("+")
#                 calc_result = 0
#                 for v in vals:
#                     calc_result += float(v)
#                 if float(actual) == calc_result:
#                     result = 0
#             elif expecteds[0] == "=":
#                 if actual == self.expected:
#                     result = 0
#             elif expecteds[0] == ">":
#                 if actual > self.expected:
#                     result = 0
#             elif expecteds[0] == ">=":
#                 if actual >= self.expected:
#                     result = 0
#             elif expecteds[0] == "<":
#                 if actual < self.expected:
#                     result = 0
#             elif expecteds[0] == "<=":
#                 if actual <= self.expected:
#                     result = 0
#             elif expecteds[0] == "contains":
#                 is_contain = self.expected in actual
#                 if is_contain:
#                     result = 0
#         except:
#             result = 1
#         print(f'-------------------------------------------------------------------{result, actual, self.expected}')
#         return result,actual,self.expected