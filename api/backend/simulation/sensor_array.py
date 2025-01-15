from simulation.hall_sensor import SimHallSensor


class SimSensorArray:  # the Sensor Array to detect the current chess position
    def __init__(self):
        self.sensors = [[SimHallSensor([j, k]) for j in range(8)] for k in range(8)]

    def get_position(self, board) -> list[list[str]]:
        return [[self.sensors[j][k].get_piece(board) for j in range(8)] for k in range(8)]
