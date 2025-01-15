
import pyfirmata.util
from ..arduino_communication import hall_array 
import time



arduino = pyfirmata.ArduinoMega('COM10')
it = pyfirmata.util.Iterator(arduino)
it.start()
time.sleep(1)

array = hall_array.Array(arduino, 52)
 
'''
while True:
  print([[array.read([j, i]) for i in range(8) ] for j in range(8)])
  time.sleep(5)
  print('new \n')
'''

'''
while True:
  sensor = int(input('sensor to read from:     '))
  print(array.read([sensor // 8, sensor % 8]))
'''

while True:
  input('detect position')
  print(array.get_position())



