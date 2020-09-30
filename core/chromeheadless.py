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
import random
from urllib.parse import urlparse

from LSpider.settings import CHROME_WEBDRIVER_PATH, CHROME_PROXY, IS_OPEN_CHROME_PROXY
from LSpider.settings import CHROME_DOWNLOAD_PATH
from utils.log import logger


def random_string(length=8):
    seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+=-"
    sa = []
    for i in range(length):
        sa.append(random.choice(seed))
    salt = ''.join(sa)
    return salt


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
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-images')
        self.chrome_options.add_argument('--ignore-certificate-errors')
        self.chrome_options.add_argument('--allow-running-insecure-content')
        self.chrome_options.add_argument('blink-settings=imagesEnabled=false')
        self.chrome_options.add_argument('--omnibox-popup-count="5"')
        self.chrome_options.add_argument("--disable-popup-blocking")
        self.chrome_options.add_argument("--disable-web-security")
        self.chrome_options.add_argument("--disk-cache-size=1000")

        # for download path
        try:
            if os.path.exists(CHROME_DOWNLOAD_PATH):
                os.mkdir(CHROME_DOWNLOAD_PATH)

            chrome_downloadfile_path = CHROME_DOWNLOAD_PATH
        except:
            chrome_downloadfile_path = "./tmp"


        prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': chrome_downloadfile_path}
        self.chrome_options.add_experimental_option('prefs', prefs)

        # proxy
        desired_capabilities = self.chrome_options.to_capabilities()
        if IS_OPEN_CHROME_PROXY:
            logger.info("[Chrome Headless] Proxy {} init".format(CHROME_PROXY))

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
            # self.chrome_options.add_argument('--proxy-server={}'.format(CHROME_PROXY))

        self.chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36')

        self.driver = webdriver.Chrome(chrome_options=self.chrome_options, executable_path=self.chromedriver_path, desired_capabilities=desired_capabilities)

        self.driver.set_page_load_timeout(15)
        self.driver.set_script_timeout(5)

    def get_resp(self, url, cookies=None, times=0, isclick=True):

        try:
            self.origin_url = url
            self.driver.implicitly_wait(10)
            self.driver.get(url)

            if cookies:
                self.add_cookie(cookies)
                self.driver.implicitly_wait(10)
                self.driver.get(url)

            # else:
            # 检查是否是登录界面
            if self.check_login():
                logger.info("[ChromeHeadless] Page {} need login.".format(url))
                return 2, True, ""

            if isclick:
                if not self.click_page():
                    self.driver.implicitly_wait(10)
                    self.driver.get(url)

            return 1, self.driver.page_source, self.driver.title

        except selenium.common.exceptions.InvalidSessionIdException:
            logger.warning("[ChromeHeadless]Chrome Headless quit unexpectedly..")

            self.init_object()

            logger.warning("[ChromeHeadless]retry once..{}".format(url))
            self.get_resp(url, cookies, times + 1, isclick)
            return -1, False, ""

        except selenium.common.exceptions.TimeoutException:
            logger.warning("[ChromeHeadless]Chrome Headless request timeout..{}".format(url))
            if times > 0:
                return -1, False, ""

            logger.warning("[ChromeHeadless]retry once..{}".format(url))
            self.get_resp(url, cookies, times+1, isclick)
            return -1, False, ""

        except selenium.common.exceptions.InvalidCookieDomainException:
            logger.warning("[ChromeHeadless]Chrome Headless request with cookie error..{}".format(url))

            logger.warning("[ChromeHeadless]retry once..{}".format(url))
            self.get_resp(url, None, times + 1, isclick)
            return -1, False, ""

        except selenium.common.exceptions.InvalidArgumentException:
            logger.warning("[ChromeHeadless]Request error...{}".format(url))
            logger.warning("[ChromeHeadless]{}".format(traceback.format_exc()))
            return -1, False, ""

    def add_cookie(self, cookies):

        for cookie in cookies.split(';'):
            key = cookie.split('=')[0].strip()
            value = cookie.split('=')[1].strip()

            if key and value:
                try:
                    self.driver.add_cookie({'name': key, 'value': value})

                except selenium.common.exceptions.UnableToSetCookieException:
                    logger.warning("[ChromeHeadless] Wrong Cookie {} set..".format(key))
                    continue

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

                self.check_back()
                return

            except IndexError:
                logger.warning("[ChromeHeadless][Click Page] wrong index for link")
                continue

            except selenium.common.exceptions.NoSuchElementException:
                logger.warning("[ChromeHeadless][Click Page] No Such Element")
                return

    def smart_input(self, input):
        """
        简单的智能表单填充
        :param input:
        :return:
        """

        # user
        for key in ['user', '用户名', 'name']:
            if key in input.get_attribute('innerHTML'):
                input.send_keys('admin')
                return

        # pass
        for key in ['pass', 'pwd', '密码']:
            if key in input.get_attribute('innerHTML'):
                input.send_keys('123456')
                return

        # email
        for key in ['email']:
            if key in input.get_attribute('innerHTML'):
                input.send_keys('{}@{}.com'.format(random_string(4), random_string(4)))
                return

        # phone
        for key in ['phone']:
            if key in input.get_attribute('innerHTML'):
                input.send_keys('{}'.format(random.randint(13000000000, 14000000000)))
                return

        # address
        for key in ['address', 'street']:
            if key in input.get_attribute('innerHTML'):
                input.send_keys('4492 Garfield Road')
                return

        # checkbox
        if input.get_attribute('type') == 'checkbox':
            input.click()

        if input.get_attribute('type') == 'radio':
            input.click()

        input.send_keys(random_string())

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

                    self.smart_input(input)

                except selenium.common.exceptions.ElementNotInteractableException:
                    logger.warning("[ChromeHeadless][Click button] error interact")

                    if self.check_back():
                        inputs = self.driver.find_elements_by_tag_name('input')
                    continue

                except selenium.common.exceptions.StaleElementReferenceException:
                    logger.warning("[ChromeHeadless][Click button] page reload or wrong back redirect")

                    return

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

                    return

                except IndexError:
                    logger.warning("[ChromeHeadless][Click button] wrong index for button")
                    continue

        except selenium.common.exceptions.NoSuchElementException:
            logger.warning("[ChromeHeadless][Click Page] No Such Element")
            return

    def check_login(self):
        """
        检查当前页面是否有登录框
        :return:
        """
        try:
            is_has_login_form = False
            is_has_login_button = False
            is_has_login_input = False

            forms = self.driver.find_elements_by_tag_name('form')
            forms_len = len(forms)

            if not forms:
                is_has_login_form = False

            for i in range(forms_len):
                form = forms[i]

                for key in ['login', '登录', 'sign', '用户名', 'user', 'pass', '用户名', 'pwd', 'phone', '注册']:
                    if key in form.text:
                        is_has_login_form = True

            buttons = self.driver.find_elements_by_tag_name('button')
            buttons_len = len(buttons)

            if not buttons:
                is_has_login_button = False

            for i in range(buttons_len):
                button = buttons[i]

                if button.is_enabled() and button.is_displayed():

                    for key in ['login', 'sign', 'user', 'pass']:
                        if key in button.get_attribute('innerHTML'):
                            is_has_login_button = True
            inputs = self.driver.find_elements_by_tag_name('input')
            inputs_len = len(inputs)

            if not inputs:
                is_has_login_input = False

            for i in range(inputs_len):
                input = inputs[i]

                if input.is_enabled() and input.is_displayed():

                    for key in ['login', 'sign', 'user', 'pass', 'account', 'phone', '手机']:
                        if key in input.get_attribute('innerHTML'):
                            is_has_login_input = True

            if is_has_login_button or is_has_login_form or is_has_login_input:
                return True
            else:
                return False

        except selenium.common.exceptions.NoSuchElementException:
            logger.warning("[ChromeHeadless][Click Page] No Such Element")
            return

        except:
            logger.error("[ChromeHeadless] Bad check...{}".format(traceback.format_exc()))
            return False

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

    Req.get_resp("http://152.136.99.52/phpmyadmin_s3cr3t/sql.php?server=1&db=lspider&table=spider_subdomainlist&pos=0", isclick=False)

    # print(Req.get_resp("https://cdn.jsdelivr.net/npm/jquery@3.3.1/dist/jquery.min.js"))
