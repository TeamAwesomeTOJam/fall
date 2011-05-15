import pygame
from pygame.locals import *
import pymunk

from settings import *


class Portal(object):
    
    def __init__(self, position):
        self.body = pymunk.Body(pymunk.inf, pymunk.inf)
        self.body.position = position
        self.shape = pymunk.Circle(self.body, 50)
        self.shape.collision_type = COLLTYPE_GOAL
        
    def draw(self, screen, game):
        x, y = self.world2screen(self.body.position)
        pygame.draw.ellipse(screen, (2,107,251), pygame.Rect(x - 30, y - 60, 60, 120), 4)
