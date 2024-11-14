class SimPin:
    def __init__(self, pin: int, digital: bool):
        self.pin = pin
        self.digital = digital
        self.voltage = 0
        self.state = 0

    def read(self) -> int:
        if self.digital:
            return self.state
        return self.voltage

    def write(self, value: int):
        if self.digital:
            self.state = value
        else:
            self.voltage = value


class SimArduino:
    def __init__(self):
        self.analog_pins = [SimPin(i, False) for i in range(10)]
        self.digital_pins = [SimPin(i, True) for i in range(20)]

    def get_pin(self, pin: str) -> SimPin:
        if pin[0] == 'd':
            return self.digital_pins[int(pin[2:len(pin) - 2])]
        return self.analog_pins[int(pin[2:len(pin) - 2])]


arduino = SimArduino()
print(arduino.get_pin('d:10:0'))
