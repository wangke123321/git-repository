from interfaces.ibehavior_handler import *
from common.log import *


class screenshotBehaviorHandler(IBehaviorHandler):

    def __init__(self):
        self.log = Log()
        self.screenshot_path = ConfigReader().get_value("file", "screenshot_path")

    def handle_behavior(self, bm, step: CaseStep):
        file_name = step.InputValue
        if not os.path.exists(self.screenshot_path):
            os.mkdir(self.screenshot_path)
        return_val = bm.screenshotsave(self.screenshot_path, file_name, step.PositioningExpression)
        return 0 if return_val == 0 else 1