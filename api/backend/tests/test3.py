import pyfirmata, pyfirmata.util
from ..arduino_communication.arduino_communication import Stepper, Magnet, Multistepper, StopSwitch
import time
print(1)
board_1 = pyfirmata.Arduino("COM11")
print('test')
board_2 = pyfirmata.ArduinoMega("COM10")

it = pyfirmata.util.Iterator(board_2)
it.start()
time.sleep(1)

switches = [StopSwitch(i, board_2) for i in range(5, 8)]

while True:
    for switch in switches:
        print(switch.get_state())
    time.sleep(1)