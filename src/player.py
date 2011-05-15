import os

import pygame
import pymunk
from pymunk import Vec2d

from settings import *
from stickman import StickMan, Animation

import math

class Player(object):

    def __init__(self, game):
        self.game = game
        
        self.body = pymunk.Body(PLAYER_MASS, pymunk.inf)#pymunk.moment_for_circle(PLAYER_MASS, 0, PLAYER_RADIUS))
        
        self.pts = [(-10,-50),(-20,-30),(-20,40),(-10,50),(10,50),(20,40),(20,-30),(10,-50)]
        #pts = [(-10,-20),(-20,0),(-20,70),(-10,80),(10,80),(20,70),(20,0),(10,-20)]
        self.shape = pymunk.Poly(self.body, self.pts, (0,0))
        self.shape.friction = PLAYER_FRICTION
        self.shape.collision_type = COLLTYPE_PLAYER
        
        self.model = StickMan(os.path.join(RES, 'animations.pickle'))
        self.model.set_default_animation(0)
        self.dir = 1
    
    def update(self, dt):
        self.model.update(dt)
    
    def walk(self):
        self.model.set_default_animation(1)
    
    def idle(self):
        self.model.set_default_animation(0)
    
    def fly(self):
        self.model.set_default_animation(5)
    
    def jump(self):
        self.model.play_animation(2)
    
        
    def draw(self, screen):
        surf = self.model.draw()
        
        if self.body.velocity.rotated(-1*self.game.player.body.force.angle - math.pi/2).x < -1*FLIP_THRESHOLD:
            self.dir = -1
        elif self.body.velocity.rotated(-1*self.game.player.body.force.angle - math.pi/2).x > FLIP_THRESHOLD:
            self.dir = 1
        if self.dir == -1:
            surf = pygame.transform.flip(surf, True, False)
        
        #diff = Vec2d(0,-1*surf.get_height() / 2.0 + 28)
        diff = Vec2d(0,-1*surf.get_height() / 2.0 + 58)
        diff.rotate(-1*self.game.player.body.force.rotated(math.pi/2.0).get_angle())
        center = self.game.world2screen(self.body.position) + diff
        
        surf = pygame.transform.rotozoom(surf, self.game.player.body.force.rotated(math.pi/2.0).get_angle_degrees(),1)
        
        rect = surf.get_rect()
        rect.center = center
        
        screen.blit(surf, rect.topleft)
        
        
