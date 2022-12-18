import traceback
import sqlite3

from src.webdriver_create_cookies import webdriver_create_cookies
from src.webdriver_navigation import open_orbitx
from src.webdriver_waits import alarm
from src.sql_actions import create_new_table
from src.data_display import display_data

alarm_turned_on = False

try:
    # create_new_table()
    open_orbitx()
    # webdriver_create_cookies()
    # display_data()

except(Exception,):
    traceback.print_exc()
    alarm()
