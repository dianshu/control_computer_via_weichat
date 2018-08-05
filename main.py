import itchat
from itchat.content import TEXT
from config import *
from cepingfu import CPF
import multiprocessing


app = itchat.new_instance()


@app.msg_register(TEXT)
def main(msg):
    if msg.text == '0':
        return HELP_MSG
    elif msg.text == '1':
        # 判断测评符是否正在刷单
        if True:
            process = multiprocessing.Process(target=cpf.main, name='cpf')
            process.wait()
        else:
            return '刷单程序运行中'
    elif msg.text == '2':
        # 判断测评符是否正在刷单
        if True:
            pass
        else:
            return '刷单程序已关闭'


# 登录，并进入主循环
app.auto_login(hotReload=True)
app.run(blockThread=False)

# 所有信息发送给to
to = app.search_friends(nickName=TO_NICKNAME)[0].userName

# 登录成功后，发送帮助信息
app.send(HELP_MSG, to)

# 测评符对象
cpf = CPF(app, to)
