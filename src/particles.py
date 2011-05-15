import random

import pymunk
import pygame
from pygame.locals import *

from settings import *


class Particle(object):

    def __init__(self, velocity, ttl=10):
        self.ttl = ttl
        self.body = pymunk.Body(1, 1)
        self.body.velocity = velocity
        self.shape = pymunk.Circle(self.body, 1)
        self.shape.collision_type = COLLTYPE_PARTICLE
                

class Emitter(object):
    
    def __init__(self, game, position, period):
        self.game = game
        self.position = position
        self.period = period
        self.counter = 0
        
    def update(self, dt):
        self.counter += dt
        if self.counter > self.period:
            self.counter -= self.period
            pv = pymunk.Vec2d()
            pv.length = 100
            pv.angle = random.random() * 2*3.14159
            self.game.particles.append(Particle(pv))
        