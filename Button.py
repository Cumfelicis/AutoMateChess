import pygame as py

font = py.font.SysFont('Comic Sans MS', 30)


class Mouse:
    def __init__(self):
        self.mouse = py.mouse

    def get_pos(self):
        return self.mouse.get_pos()

    def is_pressed(self):
        return self.mouse.get_pressed()[0]


class Button:
    def __init__(self, x_pos, y_pos, x_size, y_size, window, text):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_size = x_size
        self.y_size = y_size
        self.window = window
        self.text = text
        self.mouse = Mouse()

    def draw_button(self):
        py.draw.rect(self.window, (255, 255, 255), (self.y_pos, self.x_pos, self.y_size, self.x_size))
        text_surface = font.render(self.text, False, (0, 0, 0))
        self.window.blit(text_surface, (self.y_pos + 25, self.x_pos + self.x_size / 4))

    def is_pressed(self):
        mouse_pos = self.mouse.get_pos()
        if self.mouse.is_pressed() and self.y_pos < mouse_pos[0] < self.y_pos + self.y_size and \
                self.x_pos < mouse_pos[1] < self.x_pos + self.x_size:
            return True
        return False
