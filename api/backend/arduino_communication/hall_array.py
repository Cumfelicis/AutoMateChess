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

STUPID = {
    0: 15,
    1: 14,
    2: 1,
    3: 3,
    4: 7,
    5: 5,
    6: 6,
    7: 4,
    8: 2,
    9: 13,
    10: 12,
    11: 11,
    12: 10,
    13: 9,
    14: 8,
    15: 0
}

class Array: 
    def __init__(self, board: Arduino, en_pin):
        self.board = board
        self.in_pins = [3, 2, 1, 0]
        for x, pin in enumerate(self.in_pins):
            self.in_pins[x] = HallSensor(pin, board=board)
        
        if en_pin is not None:
            self.en_pin = board.get_pin(f'd:{en_pin}:o')
            # self.en_pins = [board.get_pin(f'd:{en_pin + i}:o') for i in range(4)] 
            # self.en_pin.write(0)
            pass

        self.signal_pins = [[52, 50, 48, 46], [44, 42, 40, 38], [36, 34, 32, 30], [28, 26, 24, 22]]
        for x, pins in enumerate(self.signal_pins):
            for y, pin in enumerate(pins):
                self.signal_pins[x][y] = self.board.get_pin(f"d:{pin}:o")
        
        
        
        self.zero_values = self.get_zero_values()
        self.get_position()
        self.calibrate()

    def read(self, pos): # takes list as postion of the hall sensor to be read from
        sensor = 8 * pos[0] + pos[1] # transforms the input to fit the layout of the real hall-sensors
        bin_sensor = f'{((sensor % 16) + 8) % 15:04b}'  
        sensor_array = self.in_pins[3 - (sensor // 16)]
        for x, pin in enumerate(self.signal_pins[3 - (sensor // 16)]):
            pin.write(int(bin_sensor[x]))
        time.sleep(0.04)
        state = sensor_array.get_state()
        return state
    
    def get_zero_values(self):
        self.en_pin.write(1)
        time.sleep(0.5)
        result = [[self.read([j, i]) for i in range(8)] for j in range(8)]
        self.en_pin.write(0)
        return result
    
    def calibrate(self):
        self.zero_values = self.get_zero_values()
    



    def get_position(self):
        self.en_pin.write(1)
        time.sleep(0.5)
        pos = [[0 for _ in range(8)] for _ in range(8)]
        for x, i in enumerate(pos): 
            for y, _ in enumerate(i):
                pos[x][y] = self.get_piece(self.read([x, y]), [x, y])
                # pos[x][y] = self.read([x, y]) - self.zero_values[x][y]
                
        self.en_pin.write(0)
        print(pos)
        return pos
    


    @staticmethod 
    def beetween(number, left_border, right_border):
        return  left_border <= number and right_border >= number

    def get_piece(self, voltage, pos):
        '''
        for key, value in PIECEMAP.items():
            if self.beetween(voltage - self.zero_values[pos[0]][pos[1]], value - TOLERANCE, value + TOLERANCE):
                return key
        '''
        voltage = voltage - self.zero_values[pos[0]][pos[1]]
        if voltage > 0.02:
            return 1
        elif voltage < -0.02:
            return -1
        return 0


def read(pos): # takes list as postion of the hall sensor to be read from
        sensor = 8 * pos[0] + pos[1]
        bin_sensor = f'{sensor % 16:04b}'
        print(bin_sensor, [sensor // 16])



if __name__ == '__main__':
    read([0, 0])
    read([2, 4])