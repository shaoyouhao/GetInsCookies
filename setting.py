import os

# 浏览器的状态, False隐藏窗口
has_screen = False

# mongoDB数据库的连接
URI = os.environ.get("REMOTE_DB", "")

# mysql数据连接
HOST = "xxx.xxx.xxx.xxx"
USER = "root"
PASSWORD = "xxx"
DB = "xxx"
PORT = 3306