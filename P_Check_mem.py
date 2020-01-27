#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import unittest
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
import time
import datetime
import matplotlib.pyplot as plt
from threading import Thread
class performanceCheck(unittest.TestCase):
    MEMORY = []
    MEMORY_PSS_TOTAL_VALUE = []
    MEMORY_PSS_TOTAL_VALUE_LIST = []
    TIME_SEC = []
    TIME_OUT = [10]
    PKG = "jp.naver.line.android"
    @classmethod
    def testExecute(self):
        print("[LOG]=============== TEST START ===============")
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '9.0'
        desired_caps['automationName'] = 'UiAutomator2'
        desired_caps['newComwomandTimeout'] = '180'
        desired_caps['deviceName'] = 'Samsung Galaxy S10'
        desired_caps['appPackage'] = 'jp.naver.line.android'
        desired_caps['appActivity'] = '.activity.SplashActivity'
        desired_caps['udid'] = '####' # udid
        desired_caps['noReset'] = 'true'
        self.driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
        time.sleep(3)

        # Call
        self.driver.find_element_by_xpath(
            "(//android.view.ViewGroup[@content-desc=\"@{bottomNavigationBarButtonViewModel.contentDescription\"])[4]/android.view.View").click()
        self.driver.find_element_by_xpath(
            "//android.widget.FrameLayout[@content-desc=\"Keypad button\"]/android.widget.ImageView").click()
        time.sleep(1)
        self.driver.find_element_by_id("jp.naver.line.android:id/input_number_edit").is_displayed()
        self.driver.find_element_by_id("jp.naver.line.android:id/input_number_edit").send_keys("####") #phone num

        # thread instance start
        t1 = Thread(target=performanceCheck.getPerformanceValue_thread, args=(self, 15))
        t1.start()
        self.driver.find_element_by_id("jp.naver.line.android:id/keypad_call_button").click()
        time.sleep(10)
        while (self.driver.find_element_by_id("jp.naver.line.android:id/line_out_status_text").is_displayed()):
            time.sleep(5)
            self.driver.find_element_by_id("jp.naver.line.android:id/voipcall_end_btn").click()
            break

        # Thread End
        t1.join()
        self.driver.quit()

        # Graph start
        self.generateGraph(self)

    # time (HH:MM:SS)
    def getCurrentTime(self):
        currentTime = time.strftime("%H:%M:%S")
        return currentTime

    # performance data
    def getPerformanceValue_thread(self, roopCount):
        print("[LOG]=============== resource measurement start ===============")
        for index in range(roopCount):
            self.TIME_SEC.append(time.strftime("%H:%M:%S"))
            self.MEMORY_LIST = self.driver.get_performance_data(self.PKG, "memoryinfo", self.TIME_OUT)
            self.MEMORY_PSS_TOTAL_VALUE = self.MEMORY_LIST[1]
            self.MEMORY_PSS_TOTAL_VALUE_LIST.append(int(self.MEMORY_PSS_TOTAL_VALUE[5]))
            time.sleep(1)
            print("[LOG] Memory data: " + self.MEMORY_PSS_TOTAL_VALUE[5])
        print("[LOG]=============== resource measurement end ===============")

    # write graph
    def generateGraph(self):
        x = self.TIME_SEC
        y = self.MEMORY_PSS_TOTAL_VALUE_LIST
        plt.plot(x, y, color='blue')
        plt.style.use(['ggplot'])
        plt.title('RAM Usage')
        plt.ylabel("memory:Total PSS(KB)")
        plt.xlabel('time(s)')
        plt.grid(True)
        plt.xticks(fontsize=9, rotation=90)
        plt.show()
if __name__ == '__main__':
    unittest.main()