from .arduino_communication import HallSensor
from pyfirmata import Arduino
from ..config import config
import time

TOLERANCE = config['TOLERANCE']
PIECEMAP = {
    'p': -0.0889,
    'P': 0.0831,
    'B': 0.0665,
    'b': -0.0703,
    'N': 0.0499,
    'n': -0.0518,
    'R': 0.0382,
    'r': -0.04,
    'Q': 0.0264,
    'q': -0.0283,
    'K': 0.0137,
    'k': -0.0136
    
}

class Array:
    def __init__(self, board: Arduino, en_pin):
        self.board = board
        self.in_pins = [HallSensor(i, board=board) for i in range(4)]
        if en_pin is not None:
            self.en_pin = board.get_pin(f'd:{en_pin}:o')
            self.en_pin.write(0)

        self.signal_pins = [[board.get_pin(f'd:{i + 4 *j + 30}:o') for i in range(4)] for j in range(4)]
        
        self.zero_values = self.get_zero_values()

    def read(self, pos): # takes list as postion of the hall sensor to be read from
        sensor = 63 - (8 * pos[0] + (7 - pos[1]))  # transforms the input to fit the layout of the real hall-sensors
        bin_sensor = f'{sensor % 16:04b}'  
        sensor_array = self.in_pins[sensor // 16]
        for x, pin in enumerate(self.signal_pins[sensor // 16]):
            pin.write(int(bin_sensor[x]))
        time.sleep(0.05)
        return sensor_array.get_state()
    
    def get_zero_values(self):
        return [[self.read([j, i]) for i in range(8)] for j in range(8)]
    



    def get_position(self):
        pos = [[0 for _ in range(8)] for _ in range(8)]
        for x, i in enumerate(pos): 
            for y, _ in enumerate(i):
                pos[x][y] = self.get_piece(self.read([x, y]), [x, y])
        return pos

    @staticmethod 
    def beetween(number, left_border, right_border):
        return  left_border <= number and right_border >= number

    def get_piece(self, voltage, pos):
        for key, value in PIECEMAP.items():
            if self.beetween(voltage - self.zero_values[pos[0]][pos[1]], value - TOLERANCE, value + TOLERANCE):
                return key
        return '!'

def read(pos): # takes list as postion of the hall sensor to be read from
        sensor = 8 * pos[0] + pos[1]
        bin_sensor = f'{sensor % 16:04b}'
        print(bin_sensor, [sensor // 16])

if __name__ == '__main__':
    read([0, 0])
    read([2, 4])