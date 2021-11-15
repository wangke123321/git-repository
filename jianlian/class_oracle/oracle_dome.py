import cx_Oracle as Co


class DemoOracle:
    def __init__(self):
        self.connect = Co.connect('swtonline/swtonline@192.168.2.62:1521/chinapay')  # 连接数据库
        self.cursor = self.connect.cursor()  # 建游标

    def insert(self, sql):
        self.cursor.execute(sql)
        self.connect.commit()

    def delete(self, sql):
        self.cursor.execute(sql)
        self.connect.commit()

    def update(self, sql):
        self.cursor.execute(sql)
        self.connect.commit()

    def select_one(self, sql):  # 查找出第一条数据
        execute = self.cursor.execute(sql)
        return execute.fetchone()

    def select_all(self, sql):  # 查找出所有数据
        execute = self.cursor.execute(sql)
        return execute.fetchall()

    def close(self):  # 关停游标和数据库连接
        self.cursor.close()
        self.connect.close()

    def rollback(self):  # 回滚数据
        self.connect.rollback()

class DemoOracle100:
    def __init__(self):
        self.connect = Co.connect('swtonline/online@192.168.1.100:1521/oradb')  # 连接数据库
        self.cursor = self.connect.cursor()  # 建游标

    def insert(self, sql):
        self.cursor.execute(sql)
        self.connect.commit()

    def delete(self, sql):
        self.cursor.execute(sql)
        self.connect.commit()

    def update(self, sql):
        self.cursor.execute(sql)
        self.connect.commit()

    def select_one(self, sql):  # 查找出第一条数据
        execute = self.cursor.execute(sql)
        return execute.fetchone()

    def select_all(self, sql):  # 查找出所有数据
        execute = self.cursor.execute(sql)
        return execute.fetchall()

    def close(self):  # 关停游标和数据库连接
        self.cursor.close()
        self.connect.close()

    def rollback(self):  # 回滚数据
        self.connect.rollback()



if __name__ == '__main__':
    sql = "SELECT * from tbl_mer_info where mer_code = '%s' " % ('923002753996665',)
    res = DemoOracle100().select_one(sql)
    print(res)
    DemoOracle100().close()
