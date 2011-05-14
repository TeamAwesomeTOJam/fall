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
        
    def _clear_pymunk(self):
        self.body = None
        self.shape = None
    

def handle_collision(space, arbiter):
    volume, shape = arbiter.shapes
    body = shape.body
    body.reset_forces()
    body.apply_force(volume.g * body.mass)
    return False
        