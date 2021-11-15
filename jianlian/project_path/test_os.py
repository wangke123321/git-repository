import os


# 新建一个目录/新建一个文件
os.mkdir("Alias")

# 跨级新建目录的 用/符号来代表路径的不同层级，必须保证上级层次是存在的
# 相对路径
os.mkdir("Alias/vict")
# 绝对路径
os.mkdir(os.getcwd()+'/vi')
# 转义字符 \n \r  可以通过加\ 还有r R 让转义字符失效

# 删除 删除文件 一级一级的删除
os.mkdir("Alias/vict")
os.rmdir('Alias')
# OSError: [WinError 145] 目录不是空的。：'Alisa'

# 路径的获取
path = os.getcwd()
print('获取的当前路径是:{}'.format(path))

# 获取路径2
path2 = os.path.realpath(__file__)
print(path2)

# 分割路径2 比 路径2少了一层的路径
path03 = os.path.split(path2)[0]
print(path03)

# 拼接路径 新建目录
# 方式一
new_path = os.getcwd()+'/python11'
os.mkdir(new_path)
print(new_path)

# 方式二
new_path01 = os.path.join(os.getcwd(), 'python11')
os.mkdir(new_path01)
print(new_path01)

# 判断目录还是文件，返回布尔值
# 文件
print(os.path.isfile('E:\python\project\jianlian\class_config'))
# 目录
print(os.path.isdir(os.getcwd()))

# 判断文件是否存在
print(os.path.exists(R'E:\python\project\jianlian\class_update_xml\feile'))

# 罗列当前路径下所有的文件和目录
print(os.listdir(os.getcwd()))

# 拓展题：
# 给定一个路径，请打印出所有的路径（直至这个路径下面没有目录为止）
# 思路：递归函数  写一个函数 相当于打印出所有的的路径出来
for path in os.listdir(os.getcwd()):
    if os.path.isdir(path):
        os.listdir(os.path.join(os.getcwd(), path))
        print("{}还需要进一步处理".format(path))
    else:
        print("这个已经是穷尽的路径", os.path.join(os.getcwd(), path))


# 异常处理
try:
    os.mkdir("Alisa")  # 嫌疑人
except NameError as e:  # 警力出动 针对于某个错误
    print('抓铺归案，进一步处理')


# 初级
# 1、处理某个错误 2、处理某种类型的错误 3、有错就抓
try:  # 警察
    os.mkdir("Alisa")
except:  # 警力出动
    print("抓铺归案，等待进一步处理")


# try except else finally
try:
    os.mkdir('Alisa')
except Exception as e:  # 把错误存起来，存到变量e里面去
    print('本次的错误是{}'.format(e))
    file = open('error.txt', 'a+', encoding='utf-8')
    file.write(str(e))
    file.close()
    raise e
else:  # 跟try是一起的，你好我就好，你不好我就不好
    print('OK')
finally:  # 有无错误，一直执行的
    pass
