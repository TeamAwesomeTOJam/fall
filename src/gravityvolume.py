import weakref

import pygame
import pymunk

from settings import *


class GravityVolume(object):

    def __init__(self, vertices, g):
        self.vertices = vertices
        self.g = g
        self._init_pymunk()
    
    def _init_pymunk(self):
        self.body = pymunk.Body(pymunk.inf, pymunk.inf)
        self.shape = pymunk.Poly(self.body, self.vertices)
        self.shape.collision_type = COLLTYPE_GRAVITY
        
    def __getstate__(self):
        return {'vertices' : [(v[0], v[1]) for v in self.vertices],
                'g' : (self.g[0], self.g[1])}
    
    def __setstate__(self, state):
        self.vertices = state['vertices']
        self.g = state['g']
        self._init_pymunk()
        
    def draw(self, screen, game):
        points = self.shape.get_points()
        flipped = map(game.world2screen, points)
        pygame.draw.polygon(screen, (0,0,255), flipped, 1)
