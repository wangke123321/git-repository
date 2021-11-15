from jianlian.requests_class.class_mode import Test_Http
from jianlian.config.class_config import FileConfig


class Jsb_Add:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def requests_jsb(self, a=None):
        x_url = self.x
        y_url = self.y
        res = Test_Http('get', x_url, data=None).test_request().json()
        try:
            result = res[0]  # 打印返回的日期
        except IndexError as e:
            print("test_jsb's error is {0}".format(a))
            print("没有交易数据")
            raise e
        res_tow = Test_Http("post", y_url, data=None, json=result).test_request().json()  # 第二次请求计算表
        data = res_tow['success']
        if data is True:
            print('计算表请求调用成功')
        else:
            print('计算表调用失败')
        print(res_tow)

if __name__ == '__main__':
    url = FileConfig().config('class_config', 'JSB', 'url')
    url_tow = FileConfig().config('class_config', 'JSB', 'url_tow')
    Jsb_Add(url, url_tow).requests_jsb()
