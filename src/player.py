import os

import pygame
import pymunk

from settings import *
from stickman import StickMan, Animation

class Player(object):

    def __init__(self, game):
        self.game = game
        self.body = pymunk.Body(PLAYER_MASS, pymunk.moment_for_circle(PLAYER_MASS, 0, PLAYER_RADIUS))
        self.body.position = pymunk.Vec2d(0, 0)
        self.shape = pymunk.Circle(self.body, PLAYER_RADIUS, (0,0))
        self.shape.friction = PLAYER_FRICTION
        self.shape.collision_type = COLLTYPE_PLAYER
        self.model = StickMan(os.path.join(RES, 'animations.pickle'))
        self.model.set_default_animation(1)
    
    def update(self, dt):
        self.model.update(dt)
        
    def draw(self, screen):
        surf = self.model.draw()
        #print self.body.velocity
        if self.body.velocity.y < 0:
            surf = pygame.transform.flip(surf, True, False)
        x, y = self.game.world2screen(self.body.position)
        x -= surf.get_width() / 2.0
        y -= surf.get_height() - PLAYER_RADIUS - 8 
        screen.blit(surf, (x, y))
        
        
