from datetime import datetime, date, timedelta  # timedelta 修改时间函数 日期
from dateutil.relativedelta import relativedelta  # relativedelta 修改时间函数 月份
import time


class DateTime:
    def now_date(self):  # 当前的时间格式 :yyyyMMdd
        return date.today().strftime('%Y%m%d')

    def now_dates(self):  # 当前的时间格式 :yyyy-mm-dd
        return date.today()

    def now_month(self):  # 取当前时间 MMddHHMMSS
        return time.strftime("%m%d%H%M%S", time.localtime())

    def random_date(self, days):  # 当前的时间天数的格式加减
        days = (date.today() + timedelta(days=days)).strftime("%Y%m%d")
        return days

    def random_dates(self, days):  # 当前的时间天数的格式加减
        days = (date.today() + timedelta(days=days)).strftime("%Y-%m-%d")
        return days

    def random_month(self, month):  # 当前的日期的月的加减
        months = (datetime.now() + relativedelta(months=month)).strftime("%Y%m%d")
        return months

    def random_months(self, month):  # 当前的日期的月的加减
        months = (datetime.now() + relativedelta(months=month)).strftime("%Y-%m-%d")
        return months

    def random_minutes(self, minutes):  # 当前日期的分钟的加减
        minutes = (datetime.today() + relativedelta(minutes=minutes)).strftime('%S %M %H')
        return minutes


if __name__ == '__main__':
    data = DateTime().now_month()
    print(data)



# print(date.today())  # 显示当前日期格式 YYYY-mm-dd
# print(date.today().strftime("%Y%m%d"))  # 显示当前日期格式 YYYYmmdd
# print((date.today() + timedelta(days=1)).strftime("%Y%m%d"))  # 显示当前日期格式+1 YYYY-mm-dd
# print((date.today() + timedelta(days=-1)).strftime("%Y%m%d"))  # 显示当前日期格式-1 YYYY-mm-dd
# print(timedelta(days=1))  # 一天的时间


# import time
# print(time.strftime("%Y%m%d %X", time.gmtime(time.time()))) #0时区
# print(time.strftime("%Y%m%d %X", time.localtime())) #当前时区
# print(time.strftime("%Y-%m-%d"))


# 在本月基础上减去一个月
#datetime_now = datetime.now()  # 当前日期  2021-10-16 16:26:21.633000
# datetime_three_month_ago = datetime_now + relativedelta(months=1)  # 加上一个月
# print(datetime_three_month_ago.strftime("%Y%m%d %X"))

