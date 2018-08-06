import itchat
from itchat.content import TEXT
from config import *
import traceback
import os
import subprocess


app = itchat.new_instance()
pid = -1


@app.msg_register(TEXT)
def main(msg):
    if msg.text == '0':
        return HELP_MSG
    elif msg.text == '1':
        if pid < 0:
            with open(os.devnull, 'w') as nohup:
                p = subprocess.Popen(CPF_RUN_CMD, shell=True, stdout=nohup)
                global pid
                pid = p.pid
        return '刷单程序已启动'
    elif msg.text == '2':
        # 判断测评符是否正在刷单
        if pid > 0:
            subprocess.Popen('kill -9 %d' % pid)
        return '刷单程序已关闭'
    else:
        return HELP_MSG


# 登录
app.auto_login(hotReload=True)

# 所有信息发送给to
# to = app.loginInfo['User'].userName
to = app.search_friends(nickName=TO_NICKNAME)[0].userName

# 登录成功后，发送帮助信息
app.send(HELP_MSG, to)

# 进入主循环
app.run()
