# coding:utf-8
from appium import webdriver
# import logging
from config import *
from time import sleep
from selenium.common.exceptions import NoSuchElementException
import subprocess
import pyautogui as pg
import traceback
import sys
from random import choice
import os


class CPF(object):
    # logging.basicConfig(format='%(levelname)s [%(asctime)s]: %(message)s', datefmt='%H:%M:%S', level=logging.INFO)

    def __init__(self, wei_chat, to):
        self.driver = None
        self.count = 0
        self.swiped = False
        self.wei_chat = wei_chat
        self.to = to

    def main(self):
        self.set_up()
        self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_capabilities=desired_caps)
        self.driver.implicitly_wait(10)
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
        self.wei_chat.send('循环接单中', toUserName=self.to)
        # logging.info('循环接单中')
        if not self.swiped:
            self.driver.swipe(200, 1200, 200, 900)
        self.get_order()

    @staticmethod
    def set_up():
        tasks = subprocess.getoutput('TASKLIST')
        if tasks.find('TianTian') == -1:
            # logging.info('启动天天模拟器')
            with open(os.devnull, 'w') as nohup:
                subprocess.Popen(SIMULATOR, shell=True, stdout=nohup)
            sleep(15)
        if tasks.find('Appium') == -1:
            # logging.info('启动Appium')
            with open(os.devnull, 'w') as nohup:
                subprocess.Popen(APPIUM, shell=True, stdout=nohup)
            pos = None
            while not pos:
                pos = pg.locateCenterOnScreen(START_APPIUM)
                sleep(1)
            pg.click(pos)
        # logging.info(subprocess.getoutput('adb connect 127.0.0.1:6555'))

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
                # logging.info('已循环%d次' % self.count)
        except NoSuchElementException:
            try:
                self.driver.find_element_by_accessibility_id('确定').click()
                sleep(3)
            except NoSuchElementException:
                traceback.print_exc()
                self.wei_chat.send('接单成功', toUserName=self.to)
                # logging.info('接单成功')
                sys.exit(0)
            else:
                self.get_order()
