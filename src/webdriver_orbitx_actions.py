import time
import datetime
import traceback

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from src.webdriver_waits import alarm
from src.sql_actions import add_odds, add_match_data

username = 'JordanRaikkonen'
password = 'Lakspqow1!'


def login(driver):
    driver.find_element(By.NAME, 'username').send_keys(username)
    driver.find_element(By.NAME, 'password').send_keys(password)
    driver.find_element(By.CLASS_NAME, 'js-login').click()


def listen(driver, listeners, strategy):
    match_data = scrape_match_data(driver)
    counter = 60
    while True:
        if counter > 55:
            match_time = datetime.datetime.strptime(match_data['time'], '%H:%M')
            today_match_time = datetime.datetime.combine(datetime.date.today(), match_time.time())
            time_difference = today_match_time - datetime.datetime.now()
            minute = time_difference.total_seconds() / 60
            if minute < 0:
                print('Match has started')
                alarm()
                return
            odds = get_current_odds(driver, 'BACK', listeners[0]['row'])
            if minute > 180 | add_odds(match_data['id'], odds, int(minute)):
                counter = 0

        else:
            counter += 1

        if strategy == 'PENDULUM':
            if check_how_many_unmatched_bets(driver) == 0:
                listeners = []


        for listener in listeners:
            current_odds_match_listener = False
            if listener['type'] == 'LAY':
                if listener['odds'] <= get_current_odds(driver, 'LAY', listener['row']):
                    current_odds_match_listener = True
            if listener['type'] == 'BACK':
                if listener['odds'] >= get_current_odds(driver, 'BACK', listener['row']):
                    current_odds_match_listener = True
            if current_odds_match_listener:
                if 'UPDATE_LISTENER' in listener['functions']:
                    update_listener(driver, listeners)
                if 'PLACE_BET' in listener['functions']:
                    place_bet(driver, listener['type'], listener['row'], listener['money'])
                if 'ALARM' in listener['functions']:
                    alarm()
                    counter = 60
        time.sleep(1)


def get_current_odds(driver, bet_type, index, step = '0'):
    try:
        odds_class_name = ''
        if bet_type == 'BACK':
            odds_class_name = 'js-back-' + step
        if bet_type == 'LAY':
            odds_class_name = 'js-lay-' + step
        html_odds_container = driver.find_elements(By.CLASS_NAME, odds_class_name)[index]
        html_odds = html_odds_container.find_element(By.CLASS_NAME, 'biab_odds').text
        return float(html_odds)
    except(Exception,):
        print('Error getting odds ======================')
        traceback.print_exc()
        time.sleep(1)
        return get_current_odds(driver, bet_type, index)


def place_bet(driver, bet_type, index, money):
    odds_class_name = ''
    if bet_type == 'BACK':
        odds_class_name = 'js-back-0'
    if bet_type == 'LAY':
        odds_class_name = 'js-lay-0'
    driver.find_elements(By.CLASS_NAME, odds_class_name)[index].click()
    WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'js-size')))
    driver.find_element(By.CLASS_NAME, 'js-size').send_keys(money)
    confirm_bets_button = driver.find_element(By.CLASS_NAME, 'biab_toggle-confirm-bets')
    if 'biab_checked' in confirm_bets_button.get_attribute('class'):
        confirm_bets_button.click()
    driver.find_element(By.ID, 'biab_placeBetsBtn').click()



def check_how_many_unmatched_bets(driver):
    return driver.find_elements(By.CLASS_NAME, 'biab_bets-unmatched').length


def scrape_match_data(driver):
    home = driver.find_elements(By.CLASS_NAME, 'biab_game-title')[0].text
    away = driver.find_elements(By.CLASS_NAME, 'biab_game-title')[1].text
    date_time = driver.find_element(By.CLASS_NAME, 'biab_market-date').text
    date = date_time[0:len(date_time) - 7]
    match_time = date_time[len(date_time) - 5:len(date_time)]
    matched_element = driver.find_element(By.CLASS_NAME, 'biab_market-tv')
    matched_string = matched_element.find_element(By.CSS_SELECTOR, 'span').text
    matched = float(matched_string.replace(',', ''))
    match_id = add_match_data(home, away, date, match_time, matched)
    return {'id': match_id, 'home': home, 'away': away, 'date': date, 'time': match_time, 'matched': matched}


def update_listener(driver, listeners):
    for listener in listeners:
        listener['odds'] = get_current_odds(driver, listener['type'], listener['row'], listener['step'])
