import pandas as pd



# csv = pd.read_csv(r"E:\python\project\jianlian\tixian_class\tx_data.csv", dtype={'tranAmt': str})
# df = pd.DataFrame(csv)
#
#
# for i in df.index.values:
#     if int(i) % 2 == 0:
#         print('我是偶数{}'.format(i))
#     else:
#         print('我是奇数{}'.format(i))

# class TestPandas:
#     @staticmethod
#     def real_excel(self, file_name, sheet_name):  # 遍历EXCEL中 'id', 'url', 'data', 'method', 'expoct' 数据 外面是列表里面是字典
#         file = pd.read_excel(file_name, sheet_name)
#         xlsx_data = []
#         for i in file.index.values:  # 遍历的是索引数
#             test = file.loc[i, ['id', 'url', 'data', 'method', 'expoct']].to_dict()  # id url..代表表格索引列名
#             xlsx_data.append(test)
#         return xlsx_data
#
#     @staticmethod
#     def real_csv(file_name):
#         file = pd.read_csv(file_name, dtype={'tranAmt': str})
#         df = pd.DataFrame(file)
#         xlsx_data = []  # 遍历 xlsx文件 存放的值加入字典
#         for i in df.index.values:
#             test = df.loc[
#                 i, ['merCode', 'tranAmt', 'settDate', 'card_state', 'stat_date', 'conv_date', 'threadID']].to_dict()
#             xlsx_data.append(test)
#         return xlsx_data
#
# if __name__ == '__main__':
#     csv = TestPandas.real_csv(r'E:\python\project\jianlian\tixian_class\tx_data.csv')
#     for y in csv:
#         print(y)





# print(df.index.values)
# print(df.loc[0].to_dict())
# print(df.loc[0, ['tranAmt']].to_dict())

# for i in range(len(df['merCode'])):
#     print(df['merCode'][i])


# file = pd.read_excel(r'E:\python\project\jianlian\tixian_class\tx_data.csv', dtype={'tranAmt': str})
# cols = [1, 2]

ex = pd.read_excel(r'E:\python\project\test_tools\test_data\test_data.xlsx', sheet_name='register')
df = pd.DataFrame(ex)
# 取第索引为id=1的一列的数据，后面加上values为列表
print(df.loc[0, ['url']].to_dict())
# print(ex.loc[1, ['id', 'url', 'data', 'method', 'expoct']].to_dict())
# print(ex.loc[:].to_dict())
#print(ex.loc[:, ['id']].to_dict())  # 遍历 xlsx文件 并且把所有的id 存放为一个字典
#print(ex.loc[0].values)  # 遍历第一行的数据为一个列表
#print(ex.values)  # 遍历 xlsx文件 存放为一个列表
#print(ex.index.values)  # 遍历 xlsx文件 存放的索引值

