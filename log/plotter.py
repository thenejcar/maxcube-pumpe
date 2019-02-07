from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import dates
from dateutil import parser

import csv
import random


def plot_and_reset():
    names = {}
    logs = {}

    colors = {}

    # read the data into a dictionary
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

            if apartment not in names:
                names[apartment] = set()

            if thermostat not in names[apartment]:
                names[apartment].add(thermostat)

            if thermostat not in colors:
                colors[thermostat] = randomised_color()

        file.close()

    timestamps = sorted(logs.keys())

    # write charts
    write_pdf("temps.pdf", "Temperatures", "Temperature", "temp", names, timestamps, colors, logs)
    write_pdf("valves.pdf", "Valves", "Valve %", "valve", names, timestamps, colors, logs)

    # clean the csv
    with open('log.csv', 'w') as file:
        file.write("time,apartment,thermostat,valve,temp\n")
        file.close()


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
