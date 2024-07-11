from config import config


class SimStepper:
    def __init__(self, axis, magnet, clock, draw):
        self.axis = axis
        self.pos = 0
        self.target_pos = 0
        self.clock = clock
        self.magnet = magnet
        self.draw = draw

    def reference(self):
        pass

    def step(self, direction):
        if direction:
            self.pos += config['BOARD_SQUARE_SIZE'] / config['STEPS_PER_SQUARE']
            if self.pos > self.target_pos:
                self.pos = self.target_pos
        else:
            self.pos -= config['BOARD_SQUARE_SIZE'] / config['STEPS_PER_SQUARE']
            if self.pos < self.target_pos:
                self.pos = self.target_pos
        if self.axis:
            self.magnet.pos[0] = self.pos
        else:
            self.magnet.pos[1] = self.pos

    def move_to(self, new_pos):
        self.target_pos = new_pos

    def move(self, rel_pos):
        self.target_pos += rel_pos

    def run_to(self):
        while not self.pos == self.target_pos:
            self.clock.tick(30)
            self.run()
            self.draw()

    def run(self):
        if self.pos < self.target_pos:
            self.step(True)
        elif self.pos > self.target_pos:
            self.step(False)

    def in_movement(self):
        if self.pos == self.target_pos:
            return False
        return True


class SimMultistepper:
    def __init__(self, clock, draw):
        self.steppers = []
        self.clock = clock
        self.draw = draw

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
            self.clock.tick(30)
            #  time.sleep(1/1000)
            running = False
            for i in self.steppers:
                i.run()
                if i.in_movement():
                    running = True
            self.draw()
