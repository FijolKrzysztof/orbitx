import os
import time
import tkinter as tk

from tkinter import LEFT, W, CENTER
from multiprocessing import Process, Value
from ctypes import c_bool
from variables import alarm_turned_on


class SpecifyListenerPopup:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry('%dx%d+%d+%d' % (200, 250, 1000, 0))

        self.type = tk.StringVar()
        self.row = tk.StringVar()
        self.odds = tk.StringVar()
        self.money = tk.StringVar()

        tk.Label(self.window, text='Add listener').pack()

        container = tk.Frame(self.window, bd=10)
        container.pack()

        tk.Radiobutton(container, value='BACK', text='Back', variable=self.type).pack(anchor=W, side=LEFT, ipadx=2)
        tk.Radiobutton(container, value='LAY', text='Lay', variable=self.type).pack(anchor=W, side=LEFT, ipadx=2)

        tk.Label(self.window, text='Row index').pack()
        tk.Entry(self.window, justify=CENTER, textvariable=self.row).pack()

        tk.Label(self.window, text='Odds').pack()
        tk.Entry(self.window, justify=CENTER, textvariable=self.odds).pack()

        tk.Label(self.window, text='Money').pack()
        tk.Entry(self.window, justify=CENTER, textvariable=self.money).pack()

        tk.Button(self.window, text='Confirm', wraplength=100, width=100, command=self.__close_window).pack(pady=10)

        self.window.mainloop()

    def __close_window(self):
        self.window.destroy()

    def __call__(self, driver):
        return {
            'type': self.type.get(),
            'row': int(self.row.get()),
            'odds': float(self.odds.get()),
            'money': int(self.money.get()),
            'functions': ['PLACE_BET', 'ALARM']
        }


class SpecifyStrategyPopup:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry('%dx%d+%d+%d' % (200, 250, 1000, 0))

        self.strategy = tk.StringVar()

        tk.Label(self.window, text='Specify strategy').pack()

        container = tk.Frame(self.window, bd=10)
        container.pack()

        tk.Radiobutton(container, value='BIG_SHIFT', text='Big shift', variable=self.strategy).pack()
        tk.Radiobutton(container, value='PENDULUM', text='Pendulum', variable=self.strategy).pack()
        tk.Radiobutton(container, value='COLLECT_DATA', text='Collect data', variable=self.strategy).pack()

        tk.Button(self.window, text='Confirm', wraplength=100, width=100, command=self.__close_window).pack(pady=10)

        self.window.mainloop()

    def __close_window(self):
        self.window.destroy()

    def __call__(self, driver):
        return self.strategy.get()


class SpecifyDirectionOfOddsMovement:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry('%dx%d+%d+%d' % (200, 250, 1000, 0))

        self.type = tk.StringVar()
        self.row = tk.StringVar()
        self.step = tk.StringVar()
        self.money = tk.StringVar()

        tk.Label(self.window, text='Specify which way will odds go').pack()

        container = tk.Frame(self.window, bd=10)
        container.pack()

        tk.Radiobutton(container, value='BACK', text='Back', variable=self.type).pack(anchor=W, side=LEFT, ipadx=2)
        tk.Radiobutton(container, value='LAY', text='Lay', variable=self.type).pack(anchor=W, side=LEFT, ipadx=2)

        tk.Label(self.window, text='Row index').pack()
        tk.Entry(self.window, justify=CENTER, textvariable=self.row).pack()

        tk.Label(self.window, text='Step').pack()
        tk.Entry(self.window, justify=CENTER, textvariable=self.step).pack()

        tk.Label(self.window, text='Money').pack()
        tk.Entry(self.window, justify=CENTER, textvariable=self.money).pack()

        tk.Button(self.window, text='Confirm', wraplength=100, width=100, command=self.__close_window).pack(pady=10)

        self.window.mainloop()

    def __close_window(self):
        self.window.destroy()

    def __call__(self, driver):
        return {
            'type': self.type.get(),
            'row': int(self.row.get()),
            'step': self.step.get(),
            'money': int(self.money.get()),
            'functions': ['UPDATE_LISTENER']
        }


class SpecifyRowIndexPopup:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry('%dx%d+%d+%d' % (200, 250, 1000, 0))

        self.row = tk.StringVar()
        self.money = tk.StringVar()

        tk.Label(self.window, text='Row index').pack()
        tk.Entry(self.window, justify=CENTER, textvariable=self.row).pack()

        tk.Button(self.window, text='Confirm', wraplength=100, width=100, command=self.__close_window).pack(pady=10)

        self.window.mainloop()

    def __close_window(self):
        self.window.destroy()

    def __call__(self, driver):
        return {
            'type': None,
            'row': int(self.row.get()),
            'functions': [],
        }


class ConfirmationPopup:
    def __init__(self, message):
        self.window = tk.Tk()
        self.window.geometry('%dx%d+%d+%d' % (100, 100, 1000, 0))
        self.button = tk.Button(text=message, wraplength=100, width=10, height=10, command=self.__close_window)
        self.button.pack()
        self.window.mainloop()

    def __close_window(self):
        self.window.destroy()

    def __call__(self, driver):
        return True


class SwitchedToNewTab:
    def __call__(self, driver):
        try:
            driver.switch_to.window(driver.window_handles[1])
            return True
        except (Exception,):
            return False


def alarm():
    def close_window():
        window.destroy()

    def make_sound():
        try:
            if alarm_turned_on:
                os.system("beep -f 500 -l 100")
            window.after(5000, make_sound)
        except(Exception,):
            pass

    window = tk.Tk()
    window.geometry('%dx%d+%d+%d' % (100, 100, 1000, 0))
    button = tk.Button(text='Stop alarm', wraplength=100, width=10, height=10, command=close_window)
    button.pack()
    window.after(1000, make_sound)
    window.mainloop()
