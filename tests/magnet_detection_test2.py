import Arduino
import Firmata
from arduino_comunication import hall_sensor
import time



arduino = Arduino()

num_pins = 4
tolerance = 12

data = [512 for _ in range(num_pins)]
pins = [HalLPin(arduino, i) for i in range(num_pins)]


piece_map = {
  K: ,
  Q: ,
  R: ,
  B: ,
  N: ,
  P: ,
  k: ,
  q: ,
  r: ,
  b: ,
  n: ,
  p: ,
   # TODO: add curly braces

def map_piece_to_voltage(voltage):
   for i in range(voltage - tolerance, voltage + tolerance):
     try:
       return piece_map[i]
    except Exception:
        pass
  
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


def detect_movement():
  while True:
    previous, updated = check_for_change(data.copy(), update_data)
    if previous is not False and updated is not False:
      print(f'Piece moved from previous to updated') # add curly braces
      detect_position()
    time.sleep(1)


def detect_position():
  print([map_piece_to_voltage(i) for i in update_data()])

  if __name__ == '__main__':
    detect_movement()
    
