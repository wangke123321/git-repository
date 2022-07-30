from web_ui_auto_lib.check_handlers.web_check_handler import *


class checkBehaviorHandler(IBehaviorHandler):
    actual = None  # 实际结果
    expected = None  # 预期结果

    def __init__(self):
        pass

    def handle_behavior(self, bm, step: CaseStep):
        global actual, expected
        if step.InputValue == "Assertion":
            params = re.findall(r'\${([\s\S]+?)\}', step.ExpectedResult)  # Start Date: ${QueryStartDate}; Login failed
            if len(params):  # 其中如果 断言字段 包含${} 进入iF 否则不进入
                expected_result = ExecuteCase().relevantParams(step.ExpectedResult)  # 取${QueryStartDate}的值
                step.ExpectedResult = expected_result  # step.ExpectedResult = Start Date: 2021-05-05;
            result = bm.source_find(step)  # 取html页面源: Start Date: 2021-05-05;
            self.expected = step.ExpectedResult  # 预期结果是 Start Date:2021-05-05
            # 返回为 结果，预期结果，实际结果;(0,-1,1) !None None
        else:
            web_check = WebCheckHandler()
            result, self.actual, self.expected = web_check.handle_check(bm, step)
        return result