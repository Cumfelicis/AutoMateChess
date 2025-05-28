import pyfirmata, pyfirmata.util
from ..arduino_communication.arduino_communication import Stepper, Magnet, Multistepper
from .. arduino_communication.hall_array import Array
import time
print(1)
board_1 = pyfirmata.Arduino("/dev/ttyACM1")
print('test')
board_2 = pyfirmata.ArduinoMega("/dev/ttyACM0")
print(2)
it = pyfirmata.util.Iterator(board_2)
it.start()
time.sleep(1)

stepper_x = Stepper(5, 2, True, board=board_1, board_2=board_2, reference_pin=7, alternative_reference_pin=6)
stepper_y = Stepper(6, 3, False, board=board_1, board_2=board_2, reference_pin=5)
magnet = Magnet(board_2, 8, 9, 10)
multistepper = Multistepper()
multistepper.add_stepper(stepper_x)
multistepper.add_stepper(stepper_y)
print(3)
print(4)
stepper_x.reference()
stepper_y.reference()
time.sleep(0.5)
magnet.off()
time.sleep(0.5)
array = Array(board_2, 2)
# magnet = Magnet(12, board_1, board_2)
# magnet.off()
print(5)
time.sleep(1)

print("test")
# stepper_x.move(10000)
# stepper_x.run_to()
'''
while True:
    magnet.on(True)
    stepper_x.move_to(-5000)
    time.sleep(0.5)
    stepper_y.move_to(-5000)
    multistepper.run_to()
    time.sleep(1)
    magnet.off()
    stepper_x.move_to(0)
    stepper_x.run_to()
    time.sleep(0.5)
    magnet.on(False)
    stepper_y.move_to(0)
    stepper_y.run_to()
    time.sleep(1)
    magnet.off()
    time.sleep(1)
'''
'''
while True:  
    stepper_x.reference()
    time.sleep(1)
    stepper_y.reference()
    time.sleep(1)  
    stepper_x.move_to(9000)
    stepper_x.run_to()
    time.sleep(1)
    stepper_y.move_to(9000)
    stepper_y.run_to()
    time.sleep(1)
'''


#stepper_x.reference()
#stepper_y.reference()


while True:
    stepper_x.reference()
    magnet.on(True)
    time.sleep(1)
    stepper_x.move_to(8800)
    stepper_x.run_to()
    magnet.off()
    time.sleep(1)
    stepper_x.reference()
    magnet.on(True)
    time.sleep(1)
    stepper_x.move_to(8800)
    stepper_x.run_to()
    magnet.off()
    time.sleep(1)
    magnet.on(True)
    stepper_x.reference()
    magnet.off()
    time.sleep(1)
    stepper_x.move_to(8800)
    stepper_x.run_to()
    magnet.on(True)
    time.sleep(1)

'''
while True:
    magnet.on(False)
    time.sleep(10)
    magnet.off()
    time.sleep(10)
    magnet.on(True)
    time.sleep(10)
    magnet.off()
    time.sleep(10)
'''


'''
stepper_y.move_to(50 + 7 * 1260)
stepper_y.run_to()
while True:
    for i in range(8, 10):
        for j in range(8):
            stepper_x.move_to(j * 1260 + 50)
            stepper_x.run_to()
            input('continue')
            stepper_x.reference()
            time.sleep(1)
        stepper_y.reference()
        stepper_y.move_to(i * 1260 + 50)
        stepper_y.run_to()
        time.sleep(5)
    stepper_y.reference() 
'''

'''
while True:
    print(array.get_position())
    time.sleep(1)
'''




'''
while True:
    x = int(input('pos x'))
    y = int(input('pos y'))
    stepper_x.move_to(x)
    stepper_y.move_to(y)
    multistepper.run_to()
'''