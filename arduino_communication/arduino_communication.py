import time


class StopSwitch:
    def __init__(self, pin, board):
        self.pin = board.get_pin(f"a:{pin}:i")
        self.pin.enable_reporting()
        time.sleep(1)

    def get_state(self):
        print(self.pin.read())
        return self.pin.read()


class Led:
    def __init__(self, pin, board):
        self.pin = board.get_pin(f"d:{pin}:o")

    def on(self):
        self.pin.write(1)

    def off(self):
        self.pin.write(0)


class Magnet:
    def __init__(self, magnet_pin, board, board_2):
        self.magnet_pin = board.get_pin(f"d:{magnet_pin}:o")
        self.led = Led(2, board_2)

    def on(self):
        self.magnet_pin.write(1)
        self.led.on()
        time.sleep(1)

    def off(self):
        self.magnet_pin.write(0)
        self.led.off()
        time.sleep(1)


class Stepper:
    def __init__(self, dir_pin, step_pin, dir, board, reference_pin, board_2, second_dir_pin=False, alternative_reference_pin=False):
        print(6)
        self.dir_pin = board.get_pin(f"d:{dir_pin}:o")
        print(6.1)
        self.step_pin = board.get_pin(f"d:{step_pin}:o")
        print(6.5)
        self.stop = StopSwitch(reference_pin, board_2)
        print(6.51)
        self.last_single_step = 0
        self.second_dir_pin = second_dir_pin
        print(7)
        if self.second_dir_pin is not False:
            self.second_dir_pin = board.get_pin(f"d:{second_dir_pin}:o")
        if alternative_reference_pin is not False:
            self.second_stop = StopSwitch(board=board_2, pin= alternative_reference_pin)
            self.two_stops = True
        else:
            self.two_stops = False
            print(8)
        self.pos = 0
        self.target_pos = 0
        if dir:
            self.dir_true = 0
            self.dir_false = 1
        else:
            self.dir_true = 1
            self.dir_false = 0

    def reference(self):
        if self.two_stops:
            print("now both")
            while not (self.stop.get_state() < 0.5 or self.second_stop.get_state() < 0.5):
                self.step(False)
            if not (self.stop.get_state() < 0.5 and self.second_stop.get_state() < 0.5):
                print("now only one")
                if self.stop.get_state() < 0.5:
                    print("now only right")
                    while not self.second_stop.get_state() < 0.5:
                        self.single_step(False, False)
                else:
                    print("now only left")
                    while not self.stop.get_state() < 0.5:
                        self.single_step(True, False)

        else:
            while not self.stop.get_state() < 0.5:
                self.step(False)
        self.pos = 0

    def set_dir(self, dir):
        self.dir_pin.write(dir)

    def single_step(self, axis, dir):
        if axis:
            if dir:
                self.dir_pin.write(self.dir_true)
                if self.second_dir_pin is not False:
                    self.second_dir_pin.write(abs(1 - self.last_single_step))
            else:
                self.dir_pin.write(self.dir_false)
                if self.second_dir_pin is not False:
                    self.second_dir_pin.write(abs(1 - self.last_single_step))
        else:
            if dir:
                self.dir_pin.write(abs(1 - self.last_single_step))
                if self.second_dir_pin is not False:
                    self.second_dir_pin.write(self.dir_false)
            else:
                self.dir_pin.write(abs(1 - self.last_single_step))
                if self.second_dir_pin is not False:
                    self.second_dir_pin.write(self.dir_true)
        self.last_single_step = abs(1 - self.last_single_step)
        self.step_pin.write(1)
        #  time.sleep(0.0005)
        self.step_pin.write(0)

    def step(self, dir):
        if dir:
            self.dir_pin.write(self.dir_true)
            if self.second_dir_pin is not False:
                self.second_dir_pin.write(self.dir_false)
        else:
            self.dir_pin.write(self.dir_false)
            if self.second_dir_pin is not False:
                self.second_dir_pin.write(self.dir_true)

        self.step_pin.write(1)
        #  time.sleep(0.0005)
        self.step_pin.write(0)
        self.update_pos(dir)

    def update_pos(self, dir):
        if dir:
            self.pos += 1
        else:
            self.pos -= 1

    def move_to(self, new_pos):
        self.target_pos = new_pos

    def run(self):
        if self.pos < self.target_pos:
            self.step(True)
        elif self.pos > self.target_pos:
            self.step(False)

    def move(self, rel_pos):
        self.target_pos += rel_pos

    def run_to(self):
        while not self.pos == self.target_pos:
            self.run()
        self.step_pin.write(0)

    def in_movement(self):
        if self.pos == self.target_pos:
            return False
        return True


class Multistepper:
    def __init__(self):
        self.steppers = []

    def add_stepper(self, stepper):
        self.steppers.append(stepper)

    def run(self):
        for i in self.steppers:
            i.run()

    def move(self, rel_pos):
        for i in self.steppers:
            i.move(rel_pos)

    def move_to(self, pos):
        for i in self.steppers:
            i.move_to(pos)

    def run_to(self):
        running = True
        while running:
            start = time.time()
            #  time.sleep(1/1000)
            running = False
            for i in self.steppers:
                i.run()
                if i.in_movement():
                    running = True
            end = time.time()
            print(end - start)
