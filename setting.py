import os

# 浏览器的状态, False隐藏窗口
has_screen = False

# 数据库的连接
URI = os.environ.get("REMOTE_DB", "")
