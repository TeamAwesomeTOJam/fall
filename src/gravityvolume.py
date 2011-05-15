import pymunk

from settings import *


class GravityVolume(object):

    volumes = {}

    def __init__(self, vertices, g):
        self.vertices = vertices
        self.g = g
        self._init_pymunk()
        
    def _init_pymunk(self):
        self.body = pymunk.Body(pymunk.inf, pymunk.inf)
        self.shape = pymunk.Poly(self.body, self.vertices)
        self.shape.collision_type = COLLTYPE_GRAVITY
        GravityVolume.volumes[self.shape] = self
        
    def _clear_pymunk(self):
        del GravityVolume.volumes[self.shape]
        self.body = None
        self.shape = None


def handle_collision(space, arbiter):
    volume_shape, shape = arbiter.shapes
    volume = GravityVolume.volumes[volume_shape]
    body = shape.body
    body.reset_forces()
    body.apply_force((volume.g[0] * body.mass, volume.g[1] * body.mass))
    return False
        