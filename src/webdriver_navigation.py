from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from src.webdriver_waits import ConfirmationPopup, SpecifyListenerPopup, SpecifyRowIndexPopup, SpecifyDirectionOfOddsMovement, SpecifyStrategyPopup
from src.webdriver_configuration import get_configured_webdriver
from src.webdriver_orbitx_actions import login, listen, get_current_odds


def open_orbitx():
    url = 'https://www.orbitxch.com/'

    # driver = get_configured_webdriver('proxy')
    driver = get_configured_webdriver('extension')

    WebDriverWait(driver, 10).until(ConfirmationPopup('Connect to VPN!'))

    driver.get(url)

    WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.NAME, 'username')))

    login(driver)

    WebDriverWait(driver, 10).until(ConfirmationPopup('Choose event!'))

    strategy = WebDriverWait(driver, 10).until(SpecifyStrategyPopup())

    if strategy == 'PENDULUM':
        pendulum_strategy(driver, strategy)
    if strategy == 'BIG_SHIFT':
        big_shift_strategy(driver, strategy)
    if strategy == 'COLLECT_DATA':
        collect_data(driver, strategy)


def collect_data(driver, strategy):
    listener = WebDriverWait(driver, 10).until(SpecifyRowIndexPopup())

    listen(driver, [listener], strategy)


def pendulum_strategy(driver, strategy):
    listener1 = WebDriverWait(driver, 10).until(SpecifyListenerPopup())
    listener2 = WebDriverWait(driver, 10).until(SpecifyListenerPopup())

    listen(driver, [listener1, listener2], strategy)


def big_shift_strategy(driver, strategy):
    listener1 = WebDriverWait(driver, 10).until(SpecifyDirectionOfOddsMovement())

    listener2_type = 'LAY' if listener1['type'] == 'BACK' else 'BACK'
    listener2_step = listener1['step']

    listener2 = {
        'type': listener2_type,
        'row': listener1['row'],
        'odds': get_current_odds(driver, listener2_type, listener1['row'], listener2_step),
        'step': listener2_step,
        'money': listener1['money'],
        'functions': ['PLACE_BET', 'ALARM']}

    listener1['step'] = '1'
    listener1['odds'] = get_current_odds(driver, listener1['type'], listener1['row'], listener1['step'])

    listen(driver, [listener1, listener2], strategy)
