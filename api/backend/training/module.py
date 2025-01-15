from abc import ABC, abstractmethod

class Module(ABC):

    @abstractmethod
    def on_robot_move(self, move):
        pass

    @abstractmethod
    def on_player_move(self, move):
        pass

    @abstractmethod
    def on_start(self, config):
        pass

    @abstractmethod
    def on_end(self, result):
        pass

    @abstractmethod
    def loop(self):
        pass

