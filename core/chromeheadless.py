#!/usr/bin/env python
# encoding: utf-8
'''
@author: LoRexxar
@contact: lorexxar@gmail.com
@file: chromeheadless.py.py
@time: 2020/3/17 15:17
@desc:
'''


import time

import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

import os
import traceback
from urllib.parse import urlparse

from LSpider.settings import CHROME_WEBDRIVER_PATH, CHROME_PROXY
from utils.base import random_string
from utils.log import logger


class ChromeDriver:
    def __init__(self):
        self.chromedriver_path = CHROME_WEBDRIVER_PATH
        self.checkos()

        try:
            self.init_object()

        except selenium.common.exceptions.SessionNotCreatedException:
            logger.error("[Chrome Headless] ChromeDriver version wrong error.")
            exit(0)

        except selenium.common.exceptions.WebDriverException:
            logger.error("[Chrome Headless] ChromeDriver load error.")
            exit(0)

        self.origin_url = ""

    def checkos(self):

        if os.name == 'nt':
            self.chromedriver_path = os.path.join(self.chromedriver_path, "chromedriver_win32.exe")
        elif os.name == 'posix':
            self.chromedriver_path = os.path.join(self.chromedriver_path, "chromedriver_linux64")
        else:
            self.chromedriver_path = os.path.join(self.chromedriver_path, "chromedriver_mac64")

    def init_object(self):

        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--disable-gpu')
        self.chrome_options.add_argument('--ignore-certificate-errors')

        # proxy
        desired_capabilities = self.chrome_options.to_capabilities()
        desired_capabilities['acceptSslCerts'] = True
        desired_capabilities['acceptInsecureCerts'] = True
        desired_capabilities['proxy'] = {
            "httpProxy": CHROME_PROXY,
            "ftpProxy": CHROME_PROXY,
            "sslProxy": CHROME_PROXY,
            "noProxy": None,
            "proxyType": "MANUAL",
            "class": "org.openqa.selenium.Proxy",
            "autodetect": False,
        }

        self.chrome_options.add_argument('user-agent="Mozilla/5.0 (iPod; U; CPU iPhone OS 2_1 like Mac OS X; ja-jp) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5F137 Safari/525.20"')

        self.driver = webdriver.Chrome(chrome_options=self.chrome_options, executable_path=self.chromedriver_path, desired_capabilities=desired_capabilities)

        self.driver.set_page_load_timeout(15)
        self.driver.set_script_timeout(5)

    def get_resp(self, url, cookies=None, times=0):

        try:
            self.origin_url = url

            if cookies:
                self.driver.add_cookie(self.check_cookie(cookies))

            self.driver.get(url)
            self.driver.implicitly_wait(10)
            self.click_page()

        except selenium.common.exceptions.TimeoutException:
            logger.warning("[ChromeHeadless]Chrome Headless request timeout..{}".format(url))
            if times > 0:
                return False

            logger.warning("[ChromeHeadless]retry once..{}".format(url))
            self.get_resp(url, cookies, times+1)
            return False

        except selenium.common.exceptions.InvalidArgumentException:
            logger.warning("[ChromeHeadless]Request error...{}".format(url))
            logger.warning("[ChromeHeadless]{}".format(traceback.format_exc()))
            return False

        return self.driver.page_source

    def check_cookie(self, cookies):
        result = {}

        for cookie in cookies.split(';'):
            key = cookie.split('=')[0]
            value = cookie.split('=')[1]

            if key and value:
                result[key] = value

        return result

    def click_page(self):

        self.click_link()
        self.click_button()

    def check_back(self):
        if self.check_host():
            new_url = self.driver.current_url
            self.driver.back()
            return True
        return False

    def click_link(self):
        """
        遇到一个问题，如果页面变化，那么获取到的标签hook会丢失，这里我们尝试用计数器来做
        """

        links = self.driver.find_elements_by_tag_name('a')
        links_len = len(links)

        for i in range(links_len):

            try:
                link = links[i]

                href = link.get_attribute('href')

                if not href:
                    continue

                if href.startswith('#'):
                    link.click()

                    self.check_back()

                if href == "javascript:void(0);":
                    link.click()

                    self.check_back()

            except selenium.common.exceptions.ElementNotInteractableException:
                logger.warning("[ChromeHeadless][Click Page] error interact")

                self.check_back()
                links = self.driver.find_elements_by_tag_name('a')
                continue

            except selenium.common.exceptions.StaleElementReferenceException:
                logger.warning("[ChromeHeadless][Click Page] page reload or wrong back redirect")

                self.get_resp(self.origin_url, "", 1)
                links = self.driver.find_elements_by_tag_name('a')
                continue

            except IndexError:
                logger.warning("[ChromeHeadless][Click Page] wrong index for link")
                continue

            except selenium.common.exceptions.NoSuchElementException:
                logger.warning("[ChromeHeadless][Click Page] No Such Element")
                return

    def click_button(self):

        try:
            inputs = self.driver.find_elements_by_tag_name('input')
            input_lens = len(inputs)

            if not inputs:
                return

            for i in range(input_lens):
                try:
                    input = inputs[i]

                    input.send_keys(random_string())

                except selenium.common.exceptions.ElementNotInteractableException:
                    logger.warning("[ChromeHeadless][Click button] error interact")

                    if self.check_back():
                        inputs = self.driver.find_elements_by_tag_name('input')
                    continue

                except selenium.common.exceptions.StaleElementReferenceException:
                    logger.warning("[ChromeHeadless][Click button] page reload or wrong back redirect")

                    self.get_resp(self.origin_url, "", 1)
                    inputs = self.driver.find_elements_by_tag_name('input')
                    continue

                except IndexError:
                    logger.warning("[ChromeHeadless][Click button] wrong index for button")
                    continue

            submit = self.driver.find_element_by_xpath("//input[@type='submit']")
            submit.click()

            buttons = self.driver.find_elements_by_tag_name('button')
            buttons_len = len(buttons)

            for i in range(buttons_len):

                try:

                    button = buttons[i]
                    button.click()

                    if self.check_back():
                        buttons = self.driver.find_elements_by_tag_name('button')

                except selenium.common.exceptions.ElementNotInteractableException:
                    logger.warning("[ChromeHeadless][Click button] error interact")

                    if self.check_back():
                        buttons = self.driver.find_elements_by_tag_name('button')
                    continue

                except selenium.common.exceptions.StaleElementReferenceException:
                    logger.warning("[ChromeHeadless][Click button] page reload or wrong back redirect")

                    self.get_resp(self.origin_url, "", 1)
                    buttons = self.driver.find_elements_by_tag_name('button')
                    continue

                except IndexError:
                    logger.warning("[ChromeHeadless][Click button] wrong index for button")
                    continue

        except selenium.common.exceptions.NoSuchElementException:
            logger.warning("[ChromeHeadless][Click Page] No Such Element")
            return

    def check_host(self):
        origin = urlparse(self.origin_url)
        now = urlparse(self.driver.current_url)

        if (origin.netloc != now.netloc) or (origin.path.replace('/', '') != now.path.replace('/', '')) or (origin.params != now.params) or (origin.query != now.query):
            return now.geturl()

        return False

    def close_driver(self):
        self.driver.quit()
        # self.driver.close()
        time.sleep(1)

    def __del__(self):
        self.close_driver()


if __name__ == "__main__":
    Req = ChromeDriver()

    Req.get_resp("https://lightless.me")

    # print(Req.get_resp("https://cdn.jsdelivr.net/npm/jquery@3.3.1/dist/jquery.min.js"))
