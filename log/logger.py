from maxcube.cube import MaxCube
from maxcube.connection import MaxCubeConnection
import time



class Logger:
    def __init__(self, address, port):

        # connect to the cube
        self.cube = MaxCube(MaxCubeConnection(address, port))


    def log(self, today):
        self.cube.update()

        now = time.strftime("%Y-%m-%d %H:%M")
        apartments = {}

        print(len(self.cube.devices), "devices found")
        for device in self.cube.devices:
            id = device.name.split("_")[0]
            if id not in apartments:
                apartments[id] = []
            apartments[id].append(device)
            with open(today + "-log.csv", "a") as file:
                row = ",".join([now, id, device.name, str(device.valve_position), str(device.actual_temperature)]) + "\n"
                file.write(row)
                file.close()
