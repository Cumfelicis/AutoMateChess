from arduino_communication.arduino_communication import HallSensor
from pyfirmata import Arduino
from pyfirmata.util import Iterator
from config import config, piece_map
import time

print(1)





arduino = Arduino('COM7')

it = Iterator(arduino)
it.start()
time.sleep(1)


num_sensors = 3
tolerance = config['TOLERANCE']

data = [512 for _ in range(num_sensors)]
pins = [HallSensor(i, arduino) for i in range(num_sensors)]

def map_piece_to_voltage(voltage):
   for i in range(voltage - tolerance, voltage + tolerance):
     try:
       return piece_map[i]
     except Exception:
        pass
  
def update_data():
  for i, x in enumerate(pins):
    data[i] = x.get_state()
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


def detect_movement():
  while True:
    previous, updated = check_for_change(data.copy(), update_data)
    if previous is not False and updated is not False:
      print(f'Piece moved from {previous} to {updated}')
      detect_position()
    time.sleep(1)

def detect_data():
  while True:
    print(update_data())
    time.sleep(1)


def detect_position():
  print([map_piece_to_voltage(i) for i in update_data()])


print('start')
#detect_movement()
detect_data()
    
