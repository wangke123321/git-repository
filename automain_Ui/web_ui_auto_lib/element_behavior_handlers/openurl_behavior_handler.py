from interfaces.ibehavior_handler import *
from common.log import Log


def skip_security(bm):
    try:
        bm.ele_click(bm.find_ele("details-button"))
        bm.ele_click(bm.find_ele("proceed-link"))
        return 0
    except Exception as e:
        bm.log.logMsg(3, e)
        return 1


class openurlBehaviorHandler(IBehaviorHandler):
    def __init__(self):
        self.log = Log()

    def handle_behavior(self, bm, step: CaseStep):
        try:
            bm.open_url(step.InputValue)
            # skip_security(bm)
            return 0
        except Exception as e:
            return 1