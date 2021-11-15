import cx_Oracle as Co
# 连接数据库，下面括号里内容根据自己实际情况填写,配置


rms_oracle = Co.connect('swtonline/swtonline@192.168.2.62:1521/chinapay')
# 使用 cursor()方法获取操作游标操作权限
cursor = rms_oracle.cursor()  # type rms_oracle.

print(type(rms_oracle))
# 使用 execute 方法执行SQL语句
sql = "select * from TBL_fee a where CASH_BACK_STATE = 'POS-20-13'"
execute = cursor.execute(sql)

# 查询SQL结果第一行的参数
data = cursor.fetchone()


# 查询SQL结果所有的参数
data_all = cursor.fetchall()
print(data_all)


