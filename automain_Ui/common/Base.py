from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from common.log import Log
from common.config import *
import pyperclip
import pyautogui
import datetime
import time

import re
from datetime import timedelta
from datetime import datetime as dt
from common.data_process import RandomInfo
from common.data_process import FileOperate


class BaseMethod:
    expectetext = None
    def __init__(self):
        self.driver = None
        self.log = Log()
        self.driver_file_path = ConfigReader().get_value("file", "driver_file_path")
        self.file_download_path = ConfigReader().get_value("file", "file_download_path")  # 自动下载文件
        self.configreader = ConfigReader()

    def open_url(self, url):
        if "chromedrive" in self.driver_file_path:
            profile = webdriver.ChromeOptions()
            exploer = {'profile.default_content_settings.popups': 0,
                       'download.default_directory': (self.file_download_path).replace("\\\\", "\\")}
            profile.add_experimental_option('prefs', exploer)
            profile.add_experimental_option("excludeSwitches", ["enable-automation"])
            self.driver = webdriver.Chrome(self.driver_file_path, chrome_options=profile)
        elif "geckodriver" in self.driver_file_path:
            profile = webdriver.FirefoxProfile()
            profile.set_preference('browser.download.folderList', 2)
            profile.set_preference('browser.download.dir', self.file_download_path)
            profile.set_preference("browser.helperApps.alwaysAsk.force", False)
            profile.set_preference('browser.download.manager.showWhenStarting', False)
            profile.set_preference('browser.download.manager.focusWhenStarting', False)
            profile.set_preference('browser.download.manager.alertOnEXEOpen', False)
            profile.set_preference('browser.helperApps.neverAsk.openFile', 'application/exe')
            profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/octet-stream')
            profile.set_preference('browser.download.manager.showAlertOnComplete', False)
            self.driver = webdriver.Firefox(executable_path=self.driver_file_path, firefox_profile=profile)
        self.driver.get(url)
        self.driver.maximize_window()

    def find_element_by_type(self, search_type, value):
        try:
            ele = self.driver.find_element(search_type, value)
            return ele
        except Exception as e:
            self.log.logMsg(5, e)
            return None

    def find_ele(self, value):
        try:
            ele = None
            ele = ele if ele is not None else self.find_element_by_type(By.ID, value)
            ele = ele if ele is not None else self.find_element_by_type(By.NAME, value)
            ele = ele if ele is not None else self.find_element_by_type(By.CLASS_NAME, value)
            ele = ele if ele is not None else self.find_element_by_type(By.TAG_NAME, value)
            ele = ele if ele is not None else self.find_element_by_type(By.LINK_TEXT, value)
            ele = ele if ele is not None else self.find_element_by_type(By.PARTIAL_LINK_TEXT, value)
            ele = ele if ele is not None else self.find_element_by_type(By.XPATH, value)
            ele = ele if ele is not None else self.find_element_by_type(By.CSS_SELECTOR, value)
            if ele is None:
                self.log.logMsg(3, "NotFound:" + value)
            return ele
        except Exception as e:
            self.log.logMsg(3, e)
            return None

    def ele_click(self, ele):
        try:
            ele.click()
            return 0
        except Exception as e:
            self.log.logMsg(3, e)
            return 1

    def ele_clear(self, ele):
        try:
            ele.send_keys(Keys.CONTROL, 'a')
            ele.send_keys(Keys.BACK_SPACE)
            return 0
        except Exception as e:
            self.log.logMsg(3, e)
            return 1

    def ele_input(self, ele, value):
        try:
            self.ele_clear(ele)
            ele.send_keys(value)
            return 0
        except Exception as e:
            self.log.logMsg(3, e)
            return 1

    def ele_display(self, ele):  # 判断对象是否可见，即css的display属性是否为none
        try:
            self.driver.find_element_by_xpath(ele).is_displayed()
            return 0
        except Exception as e:
            self.log.logMsg(3, e)
            return 1

    def refresh(self):
        self.driver.refresh()

    def locateles(self):  # 获取标签属性 每个元素都有tag（标签）属性，如搜索框的标签属性，就是最前面的input
        count = self.driver.find_element_by_tag_name("table").find_elements_by_tag_name("tr")
        return count

    def quit(self):
        self.driver.quit()

    def close(self):
        windows = self.driver.window_handles
        if len(windows) > 1:
            self.driver.switch_to.window(windows[1 - len(windows)])  # 回到最新的页面
            self.driver.close()
        else:
            self.driver.close()

    def back(self):
        self.driver.back()

    def js_screenshotsave(self, screenshot_path, file_name, js):
        self.driver.execute_script(js)
        time.sleep(2)
        timestr = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        self.driver.get_screenshot_as_file(f'{screenshot_path}\\{timestr}_{file_name}.png')

    def getelements(self, positioningexpression, scroll):
        js = None
        pe_key, pe_value = str(positioningexpression).split("=")[0], str(positioningexpression).split("=")[1]
        if "ClassName=" in positioningexpression:
            js = (f'var q=document.getElementsByClassName("demo")[0].scrollTop=' + str(scroll)).replace("demo",
                                                                                                        pe_value)
        elif "Id=" in positioningexpression:
            js = (f'var q=document.getElementsById("demo").scrollTop=' + str(scroll)).replace("demo", pe_value)
        elif "Name=" in positioningexpression:
            js = (f'var q=document.getElementsByName("demo").scrollTop=' + str(scroll)).replace("demo", pe_value)
        return js

    def movedown_posit(self, positioningexpression, x, y, screenshot_path, file_name):
        pe_key, pe_value = str(positioningexpression).split("=")[0], str(positioningexpression).split("=")[1]
        timestr = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        self.driver.get_screenshot_as_file(f'{screenshot_path}\\{timestr}_{file_name}.png')
        for i in range(1, int(pe_value) + 1):
            if i == 1:
                ActionChains(self.driver).move_by_offset(x, y).click().perform()
                time.sleep(2)
                timestr = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
                self.driver.get_screenshot_as_file(f'{screenshot_path}\\{timestr}_{file_name}.png')
            else:
                ActionChains(self.driver).move_by_offset(0, 0.1).click().perform()
                time.sleep(2)
                timestr = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
                self.driver.get_screenshot_as_file(f'{screenshot_path}\\{timestr}_{file_name}.png')

    def screenshotsave(self, screenshot_path, file_name, positioningexpression):  # 滚动切图
        scrolllist = [scroll * 100 for scroll in range(2, 7, 2)]
        size = self.driver.get_window_size()
        height, width = size['height'], size['width']
        x, y = (lambda x: x + 16 - 67)(int(width)), (lambda y: y - 129 - 30)(int(height))
        windows = self.driver.window_handles
        try:
            if len(windows) > 1:
                self.driver.switch_to.window(windows[1 - len(windows)])
                timestr = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
                self.driver.get_screenshot_as_file(f'{screenshot_path}\\{timestr}_{file_name}.png')
                time.sleep(2)
                if "movedown=" in positioningexpression:
                    self.movedown_posit(positioningexpression, x, y, screenshot_path, file_name)
                for scroll in scrolllist:
                    scroll = scroll if int(height) < 600 else scroll + 100
                    if positioningexpression == "":
                        js = "var q=document.documentElement.scrollTop=" + str(scroll)
                        self.js_screenshotsave(screenshot_path, file_name, js)
                    elif "ClassName" or "Id" or "Name" in positioningexpression:
                        self.js_screenshotsave(screenshot_path, file_name,
                                               self.getelements(positioningexpression, scroll))
                self.driver.switch_to.window(windows[0])
            else:
                timestr = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
                self.driver.get_screenshot_as_file(f'{screenshot_path}\\{timestr}_{file_name}.png')
                time.sleep(2)
                if "movedown=" in positioningexpression:
                    self.movedown_posit(positioningexpression, x, y, screenshot_path, file_name)
                scrolllist = scrolllist if int(height) < 600 else [scroll + 100 for scroll in scrolllist]
                for scroll in scrolllist:
                    if positioningexpression == "":
                        js = "var q=document.documentElement.scrollTop=" + str(scroll)
                        self.js_screenshotsave(screenshot_path, file_name, js)
                    elif "ClassName" or "Id" or "Name" in positioningexpression:
                        self.js_screenshotsave(screenshot_path, file_name, self.getelements(positioningexpression, scroll))
            return 0
        except Exception as e:
            self.log.logMsg(3, e)
            return 1

    def point(self, step):
        # 页面切换至最新页面后点击x,y定位的坐标
        x, y = step.InputValue.split(",")[0], step.InputValue.split(",")[1]
        windows = self.driver.window_handles
        if len(windows) > 1:  # 如果有多个页面，新打开的窗口，位于最后一个
            self.driver.switch_to.window(windows[1 - len(windows)])  # 那么页面切换到最新页面
        else:
            pass
        time.sleep(3)
        ActionChains(self.driver).move_by_offset(int(x), int(y)).click().perform()

    def moveto_ele(self, loc):
        # 移动至新的坐标
        try:
            ActionChains(self.driver).move_to_element(self.find_ele(loc)).perform()
            return 0
        except Exception as e:
            self.log.logMsg(3, e)
            return 1

    def source_find(self, step):
        # 定位页面源
        try:
            source_text = self.driver.page_source
            if "not in:" in step.ExpectedResult:
                BaseMethod.expectetext=str(step.ExpectedResult).split("not in:")[1]
                if BaseMethod.expectetext not in source_text:
                    return 0
                else:
                    return 1
            else:
                if step.ExpectedResult in source_text:
                    return 0
                else:
                    return 1
        except Exception as e:
            self.log.logMsg(3, e)
            return -1

    def upload(self, filepath):
        # 文件上传
        try:
            pyperclip.copy(filepath)
            pyautogui.hotkey("ctrl", "v")
            # pyautogui.write(filepath, interval=0)
            time.sleep(2)
            pyautogui.press('enter')
            # pyautogui.press('enter', presses=2)
            return 0
        except Exception as e:
            self.log.logMsg(3, e)
            return 1


class ExecuteCase:
    total = 0
    success = 0
    fail = 0
    ignore = 0

    def __init__(self):
        self.publicDict = RandomInfo().publicDict
        self.staff_file_path = ConfigReader().get_value("file", "staff_file_path")
        self.fileoperate = FileOperate()
        self.log = Log()
        self.runstatus_file_path = ConfigReader().get_value("file", "runstatus_file_path")

    def relevantParams(self, data: str):
        # 提取${}里的字符串，并包含在 self.publicDict 中判断提取 value 值
        inputvalueRelevantParams = re.findall(r'\${([\s\S]+?)\}', data)
        if inputvalueRelevantParams == []:
            pass
        else:
            self.log.logMsg(4, "enter parameter replace")
            for relevantParams in inputvalueRelevantParams:
                if relevantParams in self.publicDict.keys():
                    strData = "${%s}" % relevantParams
                    publicRelevanValue = self.publicDict[relevantParams]
                    data = data.replace(strData, str(publicRelevanValue))
                    self.log.logMsg(4, "parameter replace success")
                else:
                    self.log.logMsg(3, "parameter replace fail")
        return data

    def runstatus_tofile(self, runstatus_file_path, status, step):
        # 返回为 一个 CSV文件 RunStatus,Step 的状态功能
        time_runstatus, runstatus_title = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S"), f'RunStatus,Step'
        self.fileoperate.writefile(runstatus_file_path + time_runstatus + ".csv", "csv", runstatus_title, "a+")
        runstatus = f'{str(status)},{int(step.Step)}'
        if status == 1:  # 为1代表成功 RunStatus 下的第一列 为1
            self.fileoperate.writefile(self.runstatus_file_path + time_runstatus + ".csv", "csv", str(status), "a+")
        else:  # 否则  RunStatus 下的第一列 为 输入的其他数字 ，Step 为报错的步骤
            self.fileoperate.writefile(self.runstatus_file_path + time_runstatus + ".csv", "csv", runstatus, "a+")

    def runreslut_count(self):
        # 统计的功能  总计，成功，失败，忽略 r+ 方法是写入到首行
        total = f'runresult,total:{self.total},success:{self.success},fail:{self.fail},ignore:{self.ignore}' + "\n"
        null_str = f',,,,' + "\n"
        self.fileoperate.writefile(self.filepathname + ".csv", "csv", null_str, "r+")
        self.fileoperate.writefile(self.filepathname + ".csv", "csv", total, "r+")

    def log_output(self, step, returnvalue, actual, expected):
        # 断言功能 returnvalue, actual, expected ： 返回状态值(-1,0,1) ，实际结果，预期结果
        if returnvalue == 0 and actual == None and expected == None:  # 只针对除check之外的操作返回断言
            self.log.logMsg(4, "run success ")
        elif returnvalue == 0 and expected != None and actual == None:  # check 断言 针对于 Assertion
            if "not in:" in step.ExpectedResult:
                self.log.logMsg(4, f'run success ->"{BaseMethod.expectetext}" not in page')
            else:
                self.log.logMsg(4, f'run success ->"{expected}" in page')
        elif returnvalue == 0 and expected != None and actual != None:  # check 断言 针对于 step.PositioningExpression
            self.log.logMsg(4, f'run success -> actualreslut == expectedreslut -> {actual} == {expected}')
        elif returnvalue == 1 and expected != None and actual == None:
            # check 操作 找不到页面源 预期结果不为空，实际结果为空
            if "not in:" in step.ExpectedResult:
                if step.IgnoreErr == 1:  # 断言机制，1为执行断言 0为忽略断言 ; EXCEL 设置
                    self.runstatus_tofile(self.runstatus_file_path, 0, step)  # 写入报错状态到的CSV文件
                    self.runreslut_count()  # 统计的功能写入 输出报告的首行
                    raise Exception(self.log.logMsg(2, f'run fail  -> "{BaseMethod.expectetext}" not in page'))  # 抛出异常，程序中断
                else:
                    self.log.logMsg(2, f'run fail  -> "{BaseMethod.expectetext}" not in page')
            else:
                if step.IgnoreErr == 1:  # 断言机制，1为执行断言 0为忽略断言 ; EXCEL 设置
                    self.runstatus_tofile(self.runstatus_file_path, 0, step)  # 写入报错状态到的CSV文件
                    self.runreslut_count()  # 统计的功能写入 输出报告的首行
                    raise Exception(self.log.logMsg(2, f'run fail  -> "{expected}" not in page'))  # 抛出异常，程序中断
                else:
                    self.log.logMsg(2, f'run fail  -> "{expected}" not in page')
        elif returnvalue == 1 and expected != None and actual != None:
            # web_check_handler --》 step.PositioningExpression 断言 预期结果 != 实际结果
            if step.IgnoreErr == 1:
                self.runstatus_tofile(self.runstatus_file_path, 0, step)
                self.runreslut_count()
                raise Exception(
                    self.log.logMsg(2, f'run fail -> actualreslut != expectedreslut -> {actual} != {expected}'))
            else:
                self.log.logMsg(2, f'run fail -> actualreslut != expectedreslut -> {actual}  !=  {expected}')
        elif returnvalue == 1 and expected == None and actual == None:
            # 只针对除check之外的操作返回断言,预期结果为空，实际结果为空
            if step.IgnoreErr == 1:
                self.runstatus_tofile(self.runstatus_file_path, 0, step)
                self.runreslut_count()
                raise Exception(self.log.logMsg(2, "run fail"))
            else:
                self.log.logMsg(2, "run fail")
        elif returnvalue == -1:  # 一般定位问题为找不到元素定位表达式
            if step.IgnoreErr == 1:  # 断言机制，1为执行断言 0为忽略断言 ; 在EXCEL 里面设置
                self.runstatus_tofile(self.runstatus_file_path, 0, step)  # 写入报错状态到的CSV文件
                if step.Behavior == "check" and step.InputValue == "Assertion":
                    self.runreslut_count()  # 统计的功能写入 输出报告的首行
                    raise Exception(self.log.logMsg(2, "element find fail"))  # 抛出异常：2级：Error 严重警告，程序中断
                else:
                    self.runreslut_count()
                    raise Exception(self.log.logMsg(2, "element locate fail"))
            else:  # 断言机制，1为执行断言 0为忽略断言 ; EXCEL 里面设置
                if step.Behavior == "check" and step.InputValue == "Assertion":
                    self.log.logMsg(2, "element find fail")  # 只是打印，不影响程序向下运行
                else:
                    self.log.logMsg(2, "element locate fail")

    def casesResult(self, bm, step, fileobj, returnvalue, filepathname):
        #  文件报告用例累加功能
        #  self.bm, step ：case ，ileobj 文件对象，returnvalue 状态 ，filepathname 路径名称
        self.filepathname, self.fileobj = filepathname, fileobj  # 在 caselib.py 中方便引用
        global total, success, fail
        self.total += 1  # 总计 累加
        if returnvalue == 0:  # 返回为状态为 0
            self.success += 1  # 成功 +1
            result = f'{int(step.Step)},{step.OperationPage},{step.Description},pass'  # 步骤 模块 注释 pass
            self.fileobj.write(result + "\n")  # 在 self.fileobj 用到是 caselib.py中的 self.fileobj.write 方法
        elif returnvalue == -1 or returnvalue == 1:  # 返回为状态为 -1 或者 1
            self.fail += 1  # 失败 +1
            result = f'{int(step.Step)},{step.OperationPage},{step.Description},fail'
            self.fileobj.write(result + "\n")
        return self.total, self.success, self.fail  # 返回 总计 成功 失败

    def casesResultignore(self):
        global ignore
        self.ignore += 1
        return self.ignore

    def relevantInput(self, step):
        # step.InputValue 输入框处理功能
        input_texts = str(step.InputValue)  # step.InputValue 是输入框
        if type(step.InputValue) is float:  # 如果输入框内容是浮点数
            str_inputvalue = str(step.InputValue).split(".")[1]  # 提取小数点后面的数字 如1.23 提取23给 str_inputvalue
            if str_inputvalue == "0":  # 判断 内容如果为0
                # params = re.findall(r'\${([\s\S]+?)\}', str(str(step.InputValue).split(".")[0]))
                input_texts = str(str(step.InputValue).split(".")[0])  # 提取小数点前面数字
            else:
                # params = re.findall(r'\${([\s\S]+?)\}', str(step.InputValue))
                input_texts = str(step.InputValue)  # 不为0的话，那就正常全部提取
        else:  # 如果是输入内容是${}格式的数据， 那提取出来赋值给 params
            params = re.findall(r'\${([\s\S]+?)\}', str(step.InputValue))
            if params:
                input_texts = ExecuteCase().relevantParams(step.InputValue)  # 提取上面 staff_file_path 的数据
            elif ".json" in str(step.InputValue):  # 如果输入内容包含 .json
                texts_key = step.InputValue.split("||")[1]  # 取值 输入内容 || 以后的内容，如果是 Password
                json_file = self.fileoperate.readfile(self.staff_file_path, "json")  # 调用读文件方法读取 json文件
                # json内容 = {"StaffId":"ascadmin","Password":"0000abc!"}
                input_texts = json_file[texts_key]  # 数据则为 0000abc！
            elif "today=" in step.InputValue:  # 如果输入内容包含 today= ，调用 # 取值 from datetime import datetime as dt
                input_texts = (dt.today()).strftime("%d-%h-%Y")  # 取值当前时间 日-时-年 13-Jun-2022
            elif "today-" in step.InputValue:  # 如果输入内容包含 today- ，
                inputnumber = step.InputValue.split("-")[1]  # 取值 输入内容 - 以后的内容
                if inputnumber.isdigit():  # 判断字符是否为阿拉伯数字  例如： -2
                    input_texts = (dt.today() + timedelta(days=-int(inputnumber))).strftime("%d-%h-%Y")
            elif "today+" in step.InputValue:  # 如果输入内容包含 today+ ，
                inputnumber = step.InputValue.split("+")[1]  # 取值 输入内容 + 以后的内容
                if inputnumber.isdigit():  # 判断字符是否为阿拉伯数字  例如： +2
                    input_texts = (dt.today() + timedelta(days=int(inputnumber))).strftime("%d-%h-%Y")
            else:
                pass
        step.InputValue = input_texts  # 最后重新赋值给输入框
        if step.OutputValue:  # 如果输出框有值，那么赋值到字典 self.publicDict 中，且self.publicDict[key]=value
            self.publicDict[step.OutputValue] = step.InputValue
