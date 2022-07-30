from common.doexcel import DoExcel
from module.case import *


class ExcelCaseReader:

    def __init__(self):
        self.excel = DoExcel()

    def read_case(self):
        " read case file and return case "
        case = Case()

        xlsx_list = self.excel.get_excellist()
        for xlsx in xlsx_list:
            if "~$" in xlsx:
                pass
            else:
                all_value_case = self.excel.get_listdict_all_value(xlsx)
                for value in all_value_case:
                    case_step = CaseStep()
                    case_step.Step = value['Step']
                    case_step.Behavior = value['Behavior']
                    case_step.OperationPage = value['OperationPage']
                    case_step.Description = value['Description']
                    case_step.ObjectName = value['ObjectName']
                    case_step.PositioningExpression = value['PositioningExpression']
                    case_step.InputValue = value['InputValue']
                    case_step.OutputValue = value['OutputValue']
                    case_step.ExpectedResult = value['ExpectedResult']
                    case_step.WaitTime = value['WaitTime']
                    case_step.Enabled = value['Enabled']
                    case_step.IgnoreErr = value['IgnoreErr']
                    case_step.LoopCnt = value['LoopCnt']
                    case.caseSteps.append(case_step)

                all_map = self.excel.get_listdict_all_value_map()
                for value in all_map:
                    element_map = ElementMap()
                    element_map.Page = value["Page"]
                    element_map.Type = value["Type"]
                    element_map.Name = value["Name"]
                    element_map.TmpText = value["TmpText"]
                    element_map.SourceName = value["SourceName"]
                    case.elementMaps.append(element_map)
        return case