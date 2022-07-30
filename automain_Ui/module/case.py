class CaseStep:

    def __init__(self):
        self.Step = 0  # 步骤
        self.Behavior = ''  # 操作
        self.OperationPage = ''  # 模块名
        self.Description = ''  # 注释
        self.ObjectName = ''  # 模块对象的类名
        self.PositioningExpression = ''  # 元素定位表达式
        self.InputValue = ''  # 输入框
        self.OutputValue = ''  # 输出框，也是引用框
        self.ExpectedResult = ''  # 断言
        self.WaitTime = 1  # 强制等待，单位/秒
        self.Enabled = 1  # 执行忽略机制，1为执行，0为忽略;EXCEL设置 [=1]"True";[=0]"False"
        self.IgnoreErr = 1  # 断言机制，1为执行断言 0为忽略断言 ; EXCEL 设置
        self.LoopCnt = 1  # 重复执行


class ElementMap:
    def __init__(self):
        self.Page = ''  # 模块名
        self.Type = ''  # 类型：Txt or Btn
        self.Name = ''  # 模块对象的类名
        self.TmpText = ''  # self.Page + self.Name
        self.SourceName = ''  # 元素定位表达式


class Case:

    def __init__(self):
        self.caseSteps = list()
        self.elementMaps = list()