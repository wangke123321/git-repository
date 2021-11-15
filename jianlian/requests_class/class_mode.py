import requests


class Test_Http():
    def __init__(self, method, url, data=None, headers=None, verify=None, json=None):
        self.method = method
        self.url = url
        self.data = data
        self.headers = headers
        self.verify = verify
        self.json = json

    def test_request(self):
        headers = {'Content-Type': 'application/json;charset=UTF-8'}
        res = requests.request(self.method, self.url, data=self.data, json=self.json, headers=headers)
        if res:
            return res