from interfaces.ibehavior_handler import *
from common.log import Log


class clickBehaviorHandler(IBehaviorHandler):

    def __init__(self):
        self.log = Log()

    def handle_behavior(self, bm, step: CaseStep):
        ele = bm.find_ele(step.PositioningExpression)
        if ele is None:
            return -1
        else:
            return_val = bm.ele_click(ele)
            return 0 if return_val == 0 else 1