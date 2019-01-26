from maxcube.cube import MaxCube
from maxcube.connection import MaxCubeConnection
import time



class Logger:
    def __init__(self, address, port):

        # connect to the cube
        self.cube = MaxCube(MaxCubeConnection(address, port))


    def log(self):
        self.cube.update()

        now = time.strftime("%Y-%m-%d %H:%M")
        apartments = {}

        print(len(self.cube.devices), "devices found")
        for device in self.cube.devices:
            id = device.name.split("_")[0]
            if apartments[id] is None:
                apartments[id] = []
            apartments[id].append(device)
            with open("log.csv", "a") as file:
                file.write(",".join([now, id, device.name, device.valve_position, device.actual_temperature]))
                file.close()

