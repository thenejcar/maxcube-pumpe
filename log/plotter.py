from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import dates
from dateutil import parser

import csv
import random


def plot(today):
    names = {}
    logs = {}

    colors = {}

    # read the data into a dictionary
    with open(today + "-log.csv", 'r') as file:
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

            if apartment not in names:
                names[apartment] = set()

            if thermostat not in names[apartment]:
                names[apartment].add(thermostat)

            if thermostat not in colors:
                colors[thermostat] = color(thermostat)

        file.close()

    timestamps = sorted(logs.keys())

    # write charts
    write_pdf("temps.pdf", "Temperatures", "Temperature", "temp", names, timestamps, colors, logs)
    write_pdf("valves.pdf", "Valves", "Valve %", "valve", names, timestamps, colors, logs)


def write_pdf(filename, titlestart, ylabel, dict_key, names, timestamps, colors, logs):
    with PdfPages(filename) as pdf:
        for id in names.keys():
            fig = plt.figure()
            ax = fig.add_subplot(111)
            plt.title(titlestart + " from " + timestamps[0] + " to " + timestamps[-1])
            ax.set_ylabel(ylabel)
            ax.grid(which='major', linestyle=':')

            ax.xaxis.set_major_locator(dates.HourLocator())
            ax.xaxis.set_major_formatter(dates.DateFormatter('%H:%M'))

            for name in names[id]:
                color = colors[name]

                x = []
                y = []
                for t in timestamps:
                    if name in logs[t]:
                        value = logs[t][name][dict_key]
                        if value is not None and value != 'None':
                            x.append(parser.parse(t))
                            y.append(float(value))
                        # if value was not recorded, skip the datapoint
                    # if name is not in the dict, skip this datapoint

                ax.plot(x, y, '-', color=color, label=name)

            ax.legend(loc='best')
            plt.xticks(rotation=90)
            plt.tight_layout()
            plt.draw()
            pdf.savefig(fig)

def color(name):
    r = (0.9, 0,   0,   0.8)
    g = (0,   0.9, 0,   0.8)
    b = (0,   0,   0.9, 0.8)
    c = (0,   0.9, 0.9, 0.8)
    m = (0.9, 0,   0.9, 0.8)
    y = (0.9, 0.9, 0,   0.8)
    o = (0.5, 0.5, 0,   0.8)
    p = (0.5, 0,   0.5, 0.8)

    # predefined colors
    if name == "8_Spalnica":
        return r
    elif name == "8_Dnevna soba":
        return g
    elif name == "8_Vetrolov":
        return b

    elif name == "10_Kuhinja":
        return y
    elif name == "10_Dnevna1":
        return g
    elif name == "10_Spalnica":
        return r
    elif name == "10_Soba":
        return m
    elif name == "10_Kopalnica":
        return o
    elif name == "10_Savna":
        return p
    elif name == "10_Dnevna2":
        return c
    elif name == "10_Vetrolov":
        return b

    elif name == "11_Dnevna soba":
        return g
    elif name == "11_Kuhinja":
        return y
    elif name == "11_Kopalnica":
        return r
    elif name == "11_Vetrolov":
        return b

    # otherwise, generate randombly
    return randomised_color()


def randomised_color(color=None):
    base = 0.05

    def rd():
        return random.uniform(0.1, 0.8)

    if color == "r":
        return (rd(), base, base, 0.8)
    elif color == "g":
        return (base, rd(), base, 0.8)
    elif color == "b":
        return (base, base, rd(), 0.8)
    elif color == "c":
        return (base, rd(), rd(), 0.8)
    elif color == "y":
        return (rd(), rd(), base, 0.8)
    elif color == "m":
        return (rd(), base, rd(), 0.8)
    else:
        return (rd(), rd(), rd(), 0.8)
