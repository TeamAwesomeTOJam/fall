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
        
    def __getstate__(self):
        return {'vertices' : [(v[0], v[1]) for v in self.vertices],
                'g' : (self.g[0], self.g[1])}
    
    def __setstate__(self, state):
        self.vertices = state['vertices']
        self.g = state['g']
        self._init_pymunk()


def handle_collision(space, arbiter):
    volume_shape, shape = arbiter.shapes
    volume = GravityVolume.volumes[volume_shape]
    body = shape.body
    body.reset_forces()
    body.apply_force((volume.g[0] * body.mass, volume.g[1] * body.mass))
    return False
        
