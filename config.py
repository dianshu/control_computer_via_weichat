# coding:utf-8
from os import environ

# region 主程序相关设置项

# 微信收信人的昵称
TO_NICKNAME = '水'

# 登录成功后发送的帮助信息
HELP_MSG = '''
发送对应的数字，来运行对应的命令
0：显示此帮助
1：开始测评符刷单
2：停止测评符刷单
'''

# endregion

# region 测评符相关设置项

# 模拟器监听的端口号
port = '6555'

# driver 设置
desired_caps = {
        'deviceName': '127.0.0.1:%s' % port,
        'platformName': 'Android',
        'platformVersion': '6.0.1',
        'appPackage': 'com.quwanhe.buyer',
        'appActivity': '.MainActivity',
        'noReset': True
    }

START_APPIUM = environ.get('START_APPIUM')

# endregion
