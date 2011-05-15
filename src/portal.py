import pygame
from pygame.locals import *
import pymunk

from settings import *


class Portal(object):
    
    def __init__(self, position):
        self.position = position
        self._init_pymunk()

    def _init_pymunk(self):
        self.body = pymunk.Body(pymunk.inf, pymunk.inf)
        self.body.position = self.position
        self.shape = pymunk.Circle(self.body, 30)
        self.shape.collision_type = COLLTYPE_GOAL
        
    def __getstate__(self):
        return {'position' : (self.position[0], self.position[1])}
    
    def __setstate__(self, state):
        self.position = state['position']
        self._init_pymunk()
        
    def draw(self, screen, game):
        x, y = game.world2screen(self.body.position)
        pygame.draw.ellipse(screen, (2,107,251), pygame.Rect(x - 30, y - 60, 60, 120), 4)
