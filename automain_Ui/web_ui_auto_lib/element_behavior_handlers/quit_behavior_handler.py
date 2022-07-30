from interfaces.ibehavior_handler import *
from common.log import Log


class quitBehaviorHandler(IBehaviorHandler):
    def __init__(self):
        self.log = Log()

    def handle_behavior(self, bm, step: CaseStep):
        try:
            bm.quit()
            return 0
        except Exception as e:
            return 1