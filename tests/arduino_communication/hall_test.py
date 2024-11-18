import arduino_communication
import pyfirmata.util
import time

board_2 = pyfirmata.Arduino("COM3")

hall_pin = board_2.get_pin(f"a:3:i")
hall_pin.enable_reporting()
led = arduino_communication.Led(2, board_2)

it = pyfirmata.util.Iterator(board_2)
it.start()
time.sleep(1)

while True:
    print(hall_pin.read())
    if hall_pin.read() <  0.5:
        led.on()
    else:
        led.off()




