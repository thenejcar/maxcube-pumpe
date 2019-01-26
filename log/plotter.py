from matplotlib import pyplot as plt
from matplotlib import patches as mpatches

import csv
import time
import random


def plot_and_reset():
    names = set()
    logs = {}

    colors = {}

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
                colors[thermostat] = randomised_color()

        file.close()

    timestamps = sorted(logs.keys())

    # todo: clear the log

    # write valve chart
    plt.title("Valves from " + timestamps[0] + " to " + timestamps[-1])

    for id in names.keys():
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_ylabel('Valve position')
        ax.grid(which='major', linestyle='-')
        ax.grid(which='minor', linestyle=':')

        legend = []

        for name in names[id]:
            color = colors[name]

            x = []
            y = []
            for t in timestamps:
                if name in logs[t]:
                    x.append(t)
                    y.append(float(logs[t][name]["valve"]))
                # if name is not in the dict, skip this datapoint

            ax.plot(x, y, '-', color=color)
            legend.append(mpatches.Patch(color=color, label=name))

        fig.legend(handles=legend)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.draw()
    plt.savefig('valves.pdf')


def randomised_color(color=None):
    base = 0.1

    def rd():
        return random.uniform(0.2, 1.0)

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
