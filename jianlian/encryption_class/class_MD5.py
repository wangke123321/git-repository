import hashlib


class MD5:
    def __init__(self, data):
        self.data = data

    def md5_upper(self):  # MD5 加密输出 大写
        md5 = hashlib.md5()
        md5.update(self.data.encode('utf-8'))
        return md5.hexdigest().upper()

    def md5_lower(self):  # MD5 加密输出 小写 md5.hexdigest()[8:-8].lower() 16位
        md5 = hashlib.md5()
        md5.update(self.data.encode('utf-8'))
        return md5.hexdigest().lower()


# if __name__ == '__main__':
#     """【优化】增机审核终端信息查询接口，增加返回参数:http://192.168.2.235/zentao/story-view-5029.html"""
#     key = 'KUXC1234YIELAE98722yrjq2018'
#     mer_code = '847225007630001'
#     data = mer_code + key
#     res = MD5(data).md5_upper()
#     print(res)
if __name__ == '__main__':
    data = '847225007630001'
    res = MD5(data).md5_upper()
    print(res)


# JS = 'aaavvcc'
# hashlib.
# cs = hashlib.md5()
# cs.update(JS.encode('utf-8'))
# cs.hexdigest()
# print(cs.hexdigest().upper())