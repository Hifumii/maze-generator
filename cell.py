import pygame
from constants import *


class Cell:

    def __init__(self, x, y, size=CELL_SIZE):
        self.x = x
        self.y = y
        self.size = size
        self.line_color = WHITE
        self.line_width = 2
        self.walls = {'left': True, 'right': True, 'top': True, 'bottom': True}

    def draw(self, surface):

        if self.walls['left']:
            start_pos = (self.x, self.y)
            end_pos = (self.x, self.y + self.size)
            pygame.draw.line(surface, self.line_color, start_pos, end_pos, self.line_width)

        if self.walls['right']:
            start_pos = (self.x + self.size, self.y)
            end_pos = (self.x + self.size, self.y + self.size)
            pygame.draw.line(surface, self.line_color, start_pos, end_pos, self.line_width)

        if self.walls['top']:
            start_pos = (self.x, self.y)
            end_pos = (self.x + self.size, self.y)
            pygame.draw.line(surface, self.line_color, start_pos, end_pos, self.line_width)

        if self.walls['bottom']:
            start_pos = (self.x, self.y + self.size)
            end_pos = (self.x + self.size, self.y + self.size)
            pygame.draw.line(surface, self.line_color, start_pos, end_pos, self.line_width)
