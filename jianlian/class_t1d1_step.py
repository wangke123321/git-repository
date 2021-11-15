from jianlian.requests_class.class_mode import Test_Http
from jianlian.config.class_config import FileConfig
from jianlian.timeclass.class_time import DateTime
from jianlian.T1data import T1delete
from jianlian.D1data import D1delete
from jianlian.project_path.project_path import *


class CaseT1D1:
    def __init__(self, t1_step_url, t2_step_url, t1_step2_url, t1_step3_url):
        self.t1_step_url = t1_step_url
        self.t2_step_url = t2_step_url
        self.t1_step2_url = t1_step2_url
        self.t1_step3_url = t1_step3_url

    @staticmethod
    def delete_data():
        t1 = DateTime().random_date(-1)
        t1_job = DateTime().random_date(1)
        t2 = DateTime().random_dates(-1)
        t2_job = DateTime().random_dates(1)
        T1delete.t1sql(t1, t1_job, t2, t2_job)

    @staticmethod
    def delete_data_T3():
        t1 = DateTime().random_date(-1)
        t1_job = DateTime().random_date(2)
        t2 = DateTime().random_dates(-1)
        t2_job = DateTime().random_dates(2)
        T1delete.t1sql(t1, t1_job, t2, t2_job)

    def test_t1(self):
        """T1调度"""
        t1_step_url = self.t1_step_url
        step2_url = self.t1_step2_url
        step3_url = self.t1_step3_url
        t1_step_res = Test_Http('get', t1_step_url).test_request().json()
        if len(t1_step_res) != 0:
            for item in t1_step_res:
                print('T1Step1请求参数：', item)
                url1 = self.t2_step_url
                t1_step1 = Test_Http('post', url1, json=item).test_request().json()
                result = t1_step1
                try:
                    if t1_step1['state'] == 'success':
                        pass
                    else:
                        print('T1Step1调用失败')
                except AssertionError as e:
                    print("test_t1's error is {0}", format(e))
                    raise e
                print('T1Step1的响应结果：', result)
            step2_res = Test_Http('get', step2_url).test_request().json()
            step2 = step2_res[0]
            step3_res = Test_Http('post', step3_url, json=step2).test_request().json()
            try:
                if step3_res['state'] == 'success':
                    pass
                else:
                    print('T1Step2调用失败')
            except AssertionError as e:
                print("test_t1's error is {0}", format(e))
                raise e
            print('T1step2调用响应结果为 ：', step3_res)
        else:
            print('重复请求，脏数据没有删除干净！')

    @staticmethod
    def delete_data_d1():
        d1 = DateTime().now_date()
        d1_ = DateTime().now_dates()
        d2_ = DateTime().random_dates(-1)
        D1delete.d1sql(d1, d1_, d2_, )

    @staticmethod
    def test_d1(url, url2):
        """ D1调度 """
        t1_step_res = Test_Http('post', url).test_request().json()
        if len(t1_step_res) != 0:
            for item in t1_step_res:
                print('D1Step1请求参数：', item)
                t1_step1 = Test_Http('post', url2, json=item).test_request().json()
                result = t1_step1
                try:
                    if t1_step1['success'] == True:
                        pass
                    else:
                        print('D1Step1调用失败')
                except AssertionError as e:
                    print("test_t1's error is {0}", format(e))
                    raise e
                print('D1Step1的响应结果：', result)
        else:
            print('重复请求，脏数据没有删除干净！')



if __name__ == '__main__':
    # CaseT1D1.delete_data()
    # t1_step = FileConfig().config('class_config', 'MODE', 't1_step')
    # t2_step = FileConfig().config('class_config', 'MODE', 't2_step')
    # step2_url = FileConfig().config('class_config', 'MODE', 'step2_url')
    # step3_url = FileConfig().config('class_config', 'MODE', 'step3_url')
    # CaseT1D1(t1_step, t2_step, step2_url, step3_url).test_t1()
    CaseT1D1.delete_data_d1()
    D1 = FileConfig().config(project_tx_url, 'MODE_D1', 'D1')
    D2 = FileConfig().config(project_tx_url, 'MODE_D1', 'D2')
    CaseT1D1.test_d1(D1, D2)

