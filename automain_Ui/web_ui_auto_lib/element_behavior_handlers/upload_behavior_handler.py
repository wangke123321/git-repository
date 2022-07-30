from interfaces.ibehavior_handler import *
from common.log import Log


class uploadBehaviorHandler(IBehaviorHandler):

    def __init__(self):
        self.log = Log()

    def handle_behavior(self, bm, step: CaseStep):
        ele = bm.find_ele(step.PositioningExpression)
        print(ele)
        if ele is None:
            return -1
        else:
            return_val = bm.upload(step.InputValue)
        return 0 if return_val == 0 else 1