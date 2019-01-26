from matplotlib import pyplot as plt
from matplotlib import patches as mpatches

import csv
import time
import random


def plot_and_reset():
    names = set()
    logs = {}

    colors = {}
    colormap = {
        "8": "r",
        "10": "g",
        "11": "b"
    }

    # read the data
    with open('log.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            timestamp = row[0]
            apartment = row[1]
            thermostat = row[2]
            valve = row[3]
            temp = row[4]

            if timestamp not in logs:
                logs[timestamp] = {}

            logs[timestamp][thermostat] = {
                "time": timestamp,
                "id": apartment,
                "name": thermostat,
                "valve": valve,
                "temp": temp
            }

            if thermostat not in names:
                names.add(thermostat)

            if thermostat not in colors:
                colors[thermostat] = colormap[apartment]

        file.close()

    timestamps = sorted(logs.keys())

    # todo: clear the log

    # write valve chart
    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(111)
    ax.set_label("Valves from " + timestamps[0] + " to " + timestamps[-1])
    ax.set_ylabel('Valve position')
    ax.grid(which='major', linestyle='-')
    ax.grid(which='minor', linestyle=':')

    legend = []

    for name in names:
        color = colors[name]

        y = [logs[t][name]["valve"] for t in timestamps]
        ax.plot(timestamps, y, '-', color=color)
        legend.append(mpatches.Patch(color=color, label=name))

    plt.legend(handles=legend)
    plt.draw()
    fig.savefig('valves.pdf')


def randomised_color(color):
    base = 0.1

    rd = (lambda: random.uniform(0.2, 0.95))

    if color == "r":
        return (rd(), base, base)
    elif color == "g":
        return (base, rd(), base)
    elif color == "b":
        return (base, base, rd())
    elif color == "c":
        return (base, rd(), rd())
    elif color == "y":
        return (rd(), rd(), base)
    elif color == "m":
        return (rd(), base, rd())
    else:
        return (rd(), rd(), rd())
