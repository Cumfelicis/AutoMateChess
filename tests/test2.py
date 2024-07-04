import pyfirmata, pyfirmata.util
import arduino_communication
import time
print(1)
board_1 = pyfirmata.Arduino("COM5")
board_2 = pyfirmata.Arduino("COM3")
print(2)

stepper_x = arduino_communication.Stepper(5, 2, True, second_dir_pin=6, board=board_1, board_2=board_2, reference_pin=1, alternative_reference_pin=2)
stepper_y = arduino_communication.Stepper(7, 4, False, board=board_1, board_2=board_2, reference_pin=0)
print(3)
it = pyfirmata.util.Iterator(board_2)
it.start()
print(4)
magnet = arduino_communication.Magnet(12, board_1, board_2)
magnet.off()
print(5)
time.sleep(1)
print("test")
while True:
    stepper_x.move_to(500)
    stepper_x.run_to()
    time.sleep(1)
    stepper_x.move_to(0)
    stepper_x.run_to()
    time.sleep(1)


