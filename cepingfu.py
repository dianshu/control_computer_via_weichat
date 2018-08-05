# coding:utf-8
from appium import webdriver
import logging
from config import desired_caps, START_APPIUM
from time import sleep
from selenium.common.exceptions import NoSuchElementException
import itchat
import subprocess
import pyautogui as pg
from sys import exit
import traceback
import sys
from random import choice


class CPF(object):
    logging.basicConfig(format='%(levelname)s [%(asctime)s]: %(message)s', datefmt='%H:%M:%S', level=logging.INFO)
    itchat.auto_login(hotReload=True)
    cha = itchat.search_friends(nickName='水')[0].userName

    def __init__(self):
        self.set_up()
        self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_capabilities=desired_caps)
        self.driver.implicitly_wait(10)
        self.count = 0
        self.swiped = False

    def main(self):
        try:
            sleep(2)
            self.driver.find_element_by_accessibility_id('接 单').click()
            self.driver.swipe(200, 1200, 200, 900)
            sleep(2)
        except NoSuchElementException:
            sleep(2)
            self.driver.find_element_by_accessibility_id('接单中').click()
            sleep(2)
            self.driver.swipe(200, 1200, 200, 900)
            self.swiped = True
            sleep(2)
            self.driver.find_element_by_accessibility_id('停止').click()
        itchat.send('循环接单中', toUserName=self.cha)
        logging.info('循环接单中')
        if not self.swiped:
            self.driver.swipe(200, 1200, 200, 900)
        self.get_order()

    def set_up(self):
        tasks = subprocess.getoutput('TASKLIST')
        if tasks.find('TianTian') == -1:
            logging.info('启动天天模拟器')
            subprocess.Popen(r'C:\ttmnq\TianTian.exe')
            sleep(15)
        if tasks.find('Appium') == -1:
            logging.info('启动Appium')
            subprocess.Popen(r'C:\Users\Bai\AppData\Local\appium-desktop\app-1.6.1\Appium.exe')
            pos = None
            if START_APPIUM:
                while not pos:
                    pos = pg.locateCenterOnScreen(START_APPIUM)
                    sleep(1)
                pg.click(pos)
            else:
                logging.critical('环境变量START_APPIUM未设置')
                input('输入任意值退出')
                exit(1)
        logging.info(subprocess.getoutput('adb connect 127.0.0.1:6555'))

    def get_order(self):
        try:
            while 1:
                sleep(2)
                self.driver.find_element_by_accessibility_id('接 单').click()
                # 接单的间隔，单位为秒
                interval = choice(range(2, 7))
                sleep(interval)
                try:
                    self.driver.find_element_by_accessibility_id('停止').click()
                except NoSuchElementException:
                    pass
                sleep(1)
                self.count += 1
                logging.info('已循环%d次' % self.count)
        except NoSuchElementException:
            try:
                self.driver.find_element_by_accessibility_id('确定').click()
                sleep(3)
            except NoSuchElementException:
                traceback.print_exc()
                itchat.send('接单成功', toUserName=self.cha)
                logging.info('接单成功')
                sys.exit()
            else:
                self.get_order()


if __name__ == '__main__':
    CPF().main()
