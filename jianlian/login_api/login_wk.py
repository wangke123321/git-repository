# logging --是python自带的一个日志模块

# 它的作用主要有两个，
# 1、代替print,可以把大部分想要调试的信息打印出来或者是输出到指定的文件
# 2、可以对一些输出的调试信息分类做输出，级别控制：
# debug/info/warning/error/critical

# import logging
# 级别控制：# 默认收集的是 warning (包括warning)以上的问题
# logging.debug('小小今天很活跃')
# logging.info('小小666')
# logging.warning('pp')
# logging.error('lll')
# logging.critical('小夏')
# 输入到控制台结果是：# 默认收集的是 warning (包括warning)以上的问题
# ERROR:root:lll ======= 输出的消息分别是：级别、日志收集器默认为root、内容
# WARNING:root:pp
# CRITICAL:root:kkkkkk

# 写日志需要经过下面两个渠道：
# Logger 收集日志 debug info error
# handdler 输出日志的渠道，指定的文件，还是控制台，默认到控制台

# 定义一个日志收集器 # 如果不设置级别 或者 'python11' 为空，那么它将会默认从warning以上去收集（不包含warning）
# my_logger = logging.getLogger('python11')
# 设定级别 注意的是  DEBUG 要大写
# my_logger.setLevel('DEBUG')

# 创建我们自己的输出渠道
# ch = logging.StreamHandler()
# ch.setLevel('DEBUG')
# 把收集渠道和输出渠道对接
# my_logger.addHandler(ch)

# 收集日志
# my_logger.debug('python11期')
# my_logger.info('pyton11期，6')
# my_logger.error('python11期,最强！')


# import logging
#
# # 创建一个收集器
# my_logging = logging.getLogger('项目名称')
# # 定义级别，收集的是DEBUG以上的级别
# my_logging.setLevel('DEBUG')
# # 定义一个输出到控制台  Stream-->控制台 Handler 组织，操作者
# ch = logging.StreamHandler()
# # 定义一个输出，输出到文件
# fh = logging.FileHandler('fhandler.txt', encoding='utf-8')
# # 设置输出控制器的级别 输出的时候包含定义的级别，其中输出到控制台是error以上级别，输出到文本的是debug以上级别
# ch.setLevel('ERROR')
# fh.setLevel('DEBUG')
# # 把收集控制器和输出控制器连接起来 指定到输出渠道
# my_logging.addHandler(ch)
# my_logging.addHandler(fh)
#
# # 采集信息
# my_logging.debug('控制住这条信息debug')
# my_logging.info('控制住这条信息info')
# my_logging.warning('控制住这条信息warning')
# my_logging.error('控制住这条信息error')
# my_logging.critical('控制住这条信息critical')
#
# # 关闭日志收集器
# my_logging.removeHandler(ch)
# my_logging.removeHandler(fh)


"""formatter:决定日志记录的最终输出格式(不然日志会乱七八糟)Formatter对象定义了最终log信息的顺序，
结构和内容，规定了日志输出按照什么样的格式，默认的时间格式为：%Y-%m-%d %H:%M:%S,下面是 formatter 常用的一些信息"""

# formatter = logging.Formatter('%(asctime)s-%(levelname)s-%(filename)s-%(name)s-日志信息:%(message)s')


# import logging
# # 创建一个收集器 名称：收到错误级别
# my_logging = logging.getLogger('项目')
# # 定义级别，收集的是DEBUG以上的级别
# my_logging.setLevel('DEBUG')
#
# # 设置输出格式
# formatter = logging.Formatter('%(asctime)s-%(levelname)s-%(filename)s-%(name)s-日志信息:%(message)s')
#
# # 定义一个输出到控制台  Stream-->控制台 Handler 组织，操作者
# ch = logging.StreamHandler()
# ch.setLevel('ERROR')
# ch.setFormatter(formatter)
#
# fh = logging.FileHandler('fhandler.txt', encoding='utf-8')
# fh.setLevel('DEBUG')
# fh.setFormatter(formatter)
#
# # 把收集控制器和输出控制器连接起来 指定到输出渠道
# my_logging.addHandler(ch)
# my_logging.addHandler(fh)
#
# # 采集信息
# my_logging.debug('控制住这条信息debug')
# my_logging.info('控制住这条信息info')
# my_logging.warning('控制住这条信息warning')
# my_logging.error('控制住这条信息error')
# my_logging.critical('控制住这条信息critical')
import logging
class My_log():

    def mylog(self, msg, level):
        # 创建一个收集器 名称：收到错误级别
        my_logging = logging.getLogger('刷卡交易')
        # 定义级别，收集的是DEBUG以上的级别
        my_logging.setLevel('DEBUG')

        # 设置输出格式
        formatter = logging.Formatter('%(asctime)s-%(levelname)s-%(filename)s-%(name)s-日志信息:%(message)s')

        # 定义一个输出渠道：StreamHandler 输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel('DEBUG')
        ch.setFormatter(formatter)  # 加上输出格式
        # FileHandler 输出到文本
        fh = logging.FileHandler(r'E:\python\project\jianlian\code.txt', encoding='utf-8')
        fh.setLevel('DEBUG')
        fh.setFormatter(formatter)  # 加上输出格式

        # 把收集控制器和输出控制器连接起来 指定到输出渠道
        my_logging.addHandler(ch)
        my_logging.addHandler(fh)

        # 收集信息
        if level == 'DEBUG':
            my_logging.debug(msg)
        elif level == 'INFO':
            my_logging.info(msg)
        elif level == 'WARNING':
            my_logging.warning(msg)
        elif level == 'ERROR':
            my_logging.error(msg)
        elif level == 'CRITICAL':
            my_logging.critical(msg)

        # 关闭日志收集器
        my_logging.removeHandler(ch)
        my_logging.removeHandler(fh)

    def debug(self, msg):
        self.mylog(msg, 'DEBUG')
    def info(self, msg):
        self.mylog(msg, 'INFO')
    def warning(self, msg):
        self.mylog(msg, 'WARNING')
    def error(self, msg):
        self.mylog(msg, 'ERROR')
    def critical(self, msg):
        self.mylog(msg, 'CRITICAL')


if __name__ == '__main__':
    my_logger = My_log()
    my_logger.debug('昆山市')
    my_logger.error('多少岁的')
    my_logger.critical('啥大事')
    # My_log().mylog('ERROR问题1', 'ERROR')
    # My_log().mylog('ERROR问题2', 'ERROR')
    # My_log().mylog('ERROR问题3', 'ERROR')



