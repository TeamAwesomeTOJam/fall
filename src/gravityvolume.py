import weakref

import pygame
import pymunk

from settings import *


class GravityVolume(object):

    volumes = weakref.WeakValueDictionary()

    def __init__(self, vertices, g):
        self.vertices = vertices
        self.g = g
        self._init_pymunk()
        
    def __del__(self):
        del GravityVolume.volumes[self.shape]
    
    def _init_pymunk(self):
        self.body = pymunk.Body(pymunk.inf, pymunk.inf)
        self.shape = pymunk.Poly(self.body, self.vertices)
        self.shape.collision_type = COLLTYPE_GRAVITY
        GravityVolume.volumes[self.shape] = self
        
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


def handle_collision(space, arbiter):
    volume_shape, shape = arbiter.shapes
    volume = GravityVolume.volumes[volume_shape]
    body = shape.body
    body.reset_forces()
    body.apply_force((volume.g[0] * body.mass, volume.g[1] * body.mass))
    return False
        
        
