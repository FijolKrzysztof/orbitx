from selenium import webdriver
from selenium.common import NoSuchWindowException
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.common.options import BaseOptions
from selenium.webdriver.support.wait import WebDriverWait
from src.webdriver_waits import SwitchedToNewTab

import pickle


def get_configured_webdriver(proxy_type):
    driver = None

    if proxy_type == 'proxy':
        PROXY = '78.140.195.66:3629'

        capabilities = webdriver.DesiredCapabilities.FIREFOX
        capabilities['marionette'] = True

        proxy = Proxy()
        proxy.proxy_type = ProxyType.MANUAL
        # proxy.http_proxy = PROXY
        # proxy.ssl_proxy = PROXY
        proxy.socks_proxy = PROXY
        proxy.socks_version = 4
        proxy.add_to_capabilities(capabilities)

        driver = webdriver.Firefox(capabilities=capabilities)

    if proxy_type == 'extension':
        driver = webdriver.Firefox()

        # cookies = pickle.load(open("cookies.pkl", "rb"))

        # for cookie in cookies:
        #     driver.add_cookie(cookie)

        driver.install_addon('extensions/firefox-webext@zenmate.com.xpi')
        driver.install_addon('extensions/veepn_free_fast_security_vpn-2.1.7.xpi')

        try:
            WebDriverWait(driver, 3).until(SwitchedToNewTab())

            driver.close()
            driver.switch_to.window(driver.window_handles[0])

        except (Exception,):
            pass

    driver.set_window_rect(0, 0, 1000, 1000)

    return driver
