from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from src.webdriver_waits import ConfirmationPopup, SpecifyListenerPopup
from src.webdriver_waits import alarm

import pickle


def webdriver_create_cookies():
    # driver = webdriver.Firefox()
    # driver.install_addon('extensions/veepn_free_fast_security_vpn-2.1.7.xpi')
    # driver.set_window_rect(0, 0, 1000, 1000)
    #
    # WebDriverWait(driver, 10).until(ConfirmationPopup('Create cookies!'))
    #
    # pickle.dump(driver.get_cookies(), open('cookies.pkl', 'wb'))

    alarm()
