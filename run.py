from ctrl.controller import Controller

# create a new controller and specify the maxcube cube address/port
controller = Controller('192.168.0.2', 62910)

# run the controller forever (default check interval is 5 min)
controller.run_forever()

