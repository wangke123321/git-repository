from common.Base import ExecuteCase
from interfaces.ibehavior_handler import *
from common.log import Log
import re


class inputBehaviorHandler(IBehaviorHandler):

    def __init__(self):
        self.log = Log()
        self.ec = ExecuteCase()

    def handle_behavior(self, bm, step: CaseStep):
        self.ec.relevantInput(step)
        # if re.findall('{([\s\S]+?)\}', step.PositioningExpression) != []:
        #     self.ec.relevantTable(bm, step)
        ele = bm.find_ele(step.PositioningExpression)
        if ele is None:
            return -1
        else:
            return_val = bm.ele_input(ele, step.InputValue)
            return 0 if return_val == 0 else 1