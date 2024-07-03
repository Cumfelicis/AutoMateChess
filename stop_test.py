import pyfirmata, pyfirmata.util
import arduino_communication
import time

board_1 = pyfirmata.Arduino("COM5")
board_2 = pyfirmata.Arduino("COM3")

stepper_x = arduino_communication.Stepper(5, 2, True, second_dir_pin=6, board=board_1, board_2=board_2, reference_pin=1, alternative_reference_pin=2)
#stepper_x = arduino_communication(5, 2, True, board=board_1)
stepper_y = arduino_communication.Stepper(7, 4, False, board=board_1, board_2=board_2, reference_pin=0)
magnet

it = pyfirmata.util.Iterator(board_2)
it.start()

time.sleep(1)


stepper_x.move_to(8 * 312)
stepper_x.run_to()


