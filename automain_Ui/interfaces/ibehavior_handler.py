from module.case import *


class IBehaviorHandler:
    # def handle_behavior(self,element_public_class,driver,step : CaseStep):
    def handle_behavior(self, selenium_wd_class, step: CaseStep):
        """
        handle behavior
        :param case_step:
        :return:
        """