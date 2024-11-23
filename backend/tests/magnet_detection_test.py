import Arduino
import Firmata
from arduino_comunication import hall_sensor
import time



arduino = Arduino()

num_pins = 4
tolerance = 12

data = [512 for _ in range(num_pins)]
pins = [HalLPin(arduino, i) for i in range(num_pins)]

def update_data():
  for i, x in enumerate(pins):
    data[i] = x.read()
  return data

def check_for_change(alt, new):
  previous = False
  updated = False
  for x, i in enumerate(alt):
    if not i in range(new[x] - tolerance, new[x] + tolerance):
      if i in range(512 - tolerance, 512 + tolerance):
        previous = x
      else:
        updated = x
  return previous, updated


def detect():
  while True:
    previous, updated = check_for_change(data.copy(), update_data)
    if previous is not False and updated is not False:
      print(f'Piece moved from previous to updated') # add curly braces
      
  
