import random
import math

import pymunk
import pygame
from pygame.locals import *

from settings import *


class Particle(object):

    def __init__(self, velocity, ttl=15):
        self.ttl = ttl
        self.body = pymunk.Body(1, 1)
        self.body.velocity = velocity
        self.shape = pymunk.Circle(self.body, 1)
        self.shape.collision_type = COLLTYPE_PARTICLE
                

class Emitter(object):
    
    def __init__(self, position, period):
        self.position = position
        self.period = period
        self.counter = 0
        
    def update(self, game, dt):
        self.counter += dt
        if self.counter > self.period:
            self.counter -= self.period
            pv = pymunk.Vec2d(0, 1)
            pv.length = 100
            pv.angle = random.random() * math.pi * 2
            p = Particle(pv)
            game.particles.append(p)
            game.space.add(p.body, p.shape)
        