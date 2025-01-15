from arduino_communication import Magnet, Stepper, Multistepper
import time
import pyfirmata
#arduino = pyfirmata.Arduino('COM5')
magnet = Magnet(7)
stepper_y = Stepper(6, 3)
#active = arduino.get_pin("d:8:o:")
#active.write(0)
magnet.on()
time.sleep(5)
stepper_y.move_to(872)
stepper_y.run_to()
time.sleep(5)
magnet.off()
stepper_y.move_to(0)
stepper_y.run_to()
