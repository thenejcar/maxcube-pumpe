import wiringpi
from time import sleep
from maxcube.cube import MaxCube
from maxcube.connection import MaxCubeConnection


# pin mappings for wiringpi
PIN1 = 0  # BCM17
PIN2 = 2  # BCM22
PIN3 = 3  # BCM23

class Controller:

    def __init__(self, address, port):

        # connect to the cube
        self.cube = MaxCube(MaxCubeConnection(address, port))

        # setup the output mode on all the pins
        wiringpi.wiringPiSetup()
        wiringpi.pinMode(PIN1, 1)
        wiringpi.pinMode(PIN2, 1)
        wiringpi.pinMode(PIN3, 1)

        # pin_status dict contains the current status of the output pins
        # status 0 means that the pump is operating normally (turned on)
        # status 1 means that the pump is turned off (1 on the GPIO pin opens the relay)
        self.pin_status = {
            PIN1: 0,
            PIN2: 0,
            PIN3: 0
        }

        # map apartment IDs to the output pins
        self.pin_mapping = {
            "10": PIN1,
            "11": PIN2
        }

    def update_pins(self):
        """
        update the GPIO pins to the status set in the self.pin_status dictionary
        """
        for pin in [PIN1, PIN2, PIN3]:
            wiringpi.digitalWrite(pin, self.pin_status[pin])

    def scan_and_update_pins(self):
        """
        Scan for all the connected thermostats. They are named "ID_name", where ID is the id of the apartment.

        If valves on all the thermostats in an apartment are set to 0, turn off the corresponding pin
        """
        self.cube.update()

        apartments = {}

        print(len(self.cube.devices), "devices found")
        for device in self.cube.devices:
            id = device.name.split("_")[0]
            if apartments[id] is None:
                apartments[id] = []
            apartments[id].append(device)

        for id in apartments.keys():
            all_off = True
            for x in apartments[id]:
                all_off &= x["valve_position"] == 0

            if all_off:
                if self.pin_status[self.pin_mapping[id]] == 0:
                    print("The pump for apartment", id, "will be turned off.")
                self.pin_status[self.pin_mapping[id]] = 1
            else:
                if self.pin_status[self.pin_mapping[id]] == 1:
                    print("The pump for apartment", id, "will be turned back on.")
                self.pin_status[self.pin_mapping[id]] = 0

            self.update_pins()

    def run_forever(self):
        while True:
            try:
                self.scan_and_update_pins()
                sleep(5 * 60)
            except Exception:
                print("Background sleep was terminated, exiting the loop")
                break

        # turn everything to 0 and exit
        wiringpi.wiringPiSetup()
        wiringpi.pinMode(PIN1, 1)
        wiringpi.pinMode(PIN2, 1)
        wiringpi.pinMode(PIN3, 1)
        wiringpi.digitalWrite(PIN1, 0)
        wiringpi.digitalWrite(PIN2, 0)
        wiringpi.digitalWrite(PIN3, 0)

        print("All the pumps are now on")
        print("Controller is shutting down")




