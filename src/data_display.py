import tkinter as tk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from src.sql_actions import get_all_data, get_column_names


match_index = 0


def display_data():
    window = tk.Tk()
    fig = Figure(figsize=(6, 4))

    data = get_all_data()
    column_names = get_column_names()

    chart = fig.add_subplot(111)

    buttons_frame = tk.Frame(window)
    buttons_frame.pack()

    back_button = tk.Button(buttons_frame, text='Back')
    back_button.pack(side=tk.LEFT)

    next_button = tk.Button(buttons_frame, text="Next")
    next_button.pack(side=tk.RIGHT)

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    set_data(data, 0, column_names, chart, canvas)

    def next_index():
        global match_index
        if match_index < len(data) - 1:
            match_index += 1
            set_data(data, match_index, column_names, chart, canvas)

    def previous_index():
        global match_index
        if match_index > 0:
            match_index -= 1
            set_data(data, match_index, column_names, chart, canvas)

    next_button.config(command=next_index)
    back_button.config(command=previous_index)

    window.mainloop()


def set_data(data, match_index, column_names, chart, canvas):
    x_values = column_names[6:len(column_names)]
    y_values = data[match_index][6:len(column_names)]

    for i in range(len(x_values)):
        x_values[i] = x_values[i].replace("Minute_", "")

    matched = '{:,}'.format(int(data[match_index][5]))

    chart.cla()
    chart.plot(x_values, y_values)
    chart.set_title(data[match_index][4] + '\n' + data[match_index][1] + ' vs ' + data[match_index][2] + '\n' + matched)
    chart.set_xticks(range(0, len(x_values), 20))
    chart.set_xlabel('Minutes')
    chart.set_ylabel('Odds')

    canvas.draw()
