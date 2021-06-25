import os

# 浏览器的状态, False隐藏窗口
has_screen = False

# mongoDB数据库的连接
ISMONGO = False  # 是否使用mongo数据库
URI = os.environ.get("REMOTE_DB", "mongodb://crawler:Duoshoubang@120.55.84.175/dsb")

# mysql数据连接
HOST = "112.124.40.161"
USER = "root"
PASSWORD = "DevOps2021!"
DB = "kol_analysis"
PORT = 3306