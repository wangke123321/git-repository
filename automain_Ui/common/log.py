import os
from common.config import *
import colorlog
import time
import logging


class Log:
    def __init__(self):
        self.log_folder_path = ConfigReader().get_value("log", "log_folder_path")
        self.log_level = ConfigReader().get_value("log", "log_level")
        self.log_path = os.path.join("logs")
        if not os.path.exists(self.log_folder_path):
            os.mkdir(self.log_folder_path)
        self.logname = os.path.join(self.log_folder_path, '%s.log' % time.strftime('%Y-%m-%d'))
        self.logger = logging.getLogger()
        # 输出到控制台
        self.console_handler = logging.StreamHandler()
        # 输出到文件
        self.file_handler = logging.FileHandler(self.logname, mode='a', encoding='utf8')
        log_colors_config = {
            'DEBUG': 'white',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
        # 日志输出格式
        file_formatter = logging.Formatter(
            fmt='[%(asctime)s.%(msecs)03d] %(filename)s -> %(funcName)s line:%(lineno)d [%(levelname)s] : %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_formatter = colorlog.ColoredFormatter(
            fmt='%(log_color)s[%(asctime)s.%(msecs)03d] %(filename)s -> %(funcName)s line:%(lineno)d [%(levelname)s] : %(message)s',
            datefmt='%Y-%m-%d  %H:%M:%S',
            log_colors=log_colors_config
        )
        self.console_handler.setFormatter(console_formatter)
        self.file_handler.setFormatter(file_formatter)

        if not self.logger.handlers:
            self.logger.addHandler(self.console_handler)
            self.logger.addHandler(self.file_handler)
        self.console_handler.close()
        self.file_handler.close()

    def logMsg(self, level, message):
        # 控制台日志输出等级
        if int(self.log_level) == 1:
            self.logger.setLevel(logging.CRITICAL)
            self.console_handler.setLevel(logging.CRITICAL)
            self.file_handler.setLevel(logging.CRITICAL)
        elif int(self.log_level) == 2:
            self.logger.setLevel(logging.ERROR)
            self.console_handler.setLevel(logging.ERROR)
            self.file_handler.setLevel(logging.ERROR)
        elif int(self.log_level) == 3:
            self.logger.setLevel(logging.WARNING)
            self.console_handler.setLevel(logging.WARNING)
            self.file_handler.setLevel(logging.WARNING)
        elif int(self.log_level) == 4:
            self.logger.setLevel(logging.INFO)
            self.console_handler.setLevel(logging.INFO)
            self.file_handler.setLevel(logging.INFO)
        elif int(self.log_level) == 5:
            self.logger.setLevel(logging.DEBUG)
            self.console_handler.setLevel(logging.DEBUG)
            self.file_handler.setLevel(logging.DEBUG)
        # 控制台日志输出定义
        if level == 5:
            self.logger.debug(message)
        elif level == 4:
            self.logger.info(message)
        elif level == 3:
            self.logger.warning(message)
        elif level == 2:
            self.logger.error(message)
        elif level == 1:
            self.logger.critical(message)