import matplotlib.pyplot as plt

from src.sql_actions import get_all


def display_data():
    data = get_all()

    for row in data:
        print(row)

