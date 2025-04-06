import pyfirmata, pyfirmata.util
from ..arduino_communication.arduino_communication import Stepper, Magnet, Multistepper
import time
print(1)
board_1 = pyfirmata.Arduino("COM7")
print('test')
board_2 = pyfirmata.ArduinoMega("COM10")
print(2)
magnet = Magnet(board_2, 2, 3, 4)
magnet.off()