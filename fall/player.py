import os

import pygame
import pymunk
from pymunk import Vec2d

from . import settings
from .stickman import StickMan, Animation

import math

class Player(object):

    def __init__(self, game):
        self.game = game
        
        self.body = pymunk.Body(settings.PLAYER_MASS, float("inf"))#pymunk.moment_for_circle(PLAYER_MASS, 0, PLAYER_RADIUS))
        
        self.pts = [(-10,-50),(-20,-30),(-20,40),(-10,50),(10,50),(20,40),(20,-30),(10,-50)]
        #pts = [(-10,-20),(-20,0),(-20,70),(-10,80),(10,80),(20,70),(20,0),(10,-20)]
        self.shape = pymunk.Poly(self.body, self.pts)
        self.shape.friction = settings.PLAYER_FRICTION
        self.shape.collision_type = settings.COLLTYPE_PLAYER
        
        self.model = StickMan(os.path.join(settings.RES, 'animations.pickle'))
        self.model.set_default_animation(0)
        self.dir = 1
        
        self.jump_sound = pygame.mixer.Sound(os.path.join(settings.RES, 'jump.ogg'))
        self.land_sound = pygame.mixer.Sound(os.path.join(settings.RES, 'land.ogg'))
        self.gravity_sound = pygame.mixer.Sound(os.path.join(settings.RES, 'gravity.ogg'))
        self.gravity_sound.set_volume(0.3)
        
        self.collisions = []
        self.last_on_ground = 0
        self.was_on_ground = False
        self.gravity = Vec2d(0, 0)
        self.last_gravity = Vec2d(0, 0)
        self.gravity_set = False
    
    def update(self, dt):
        self.model.update(dt)
    
    def walk(self):
        self.model.set_default_animation(1)
    
    def idle(self):
        self.model.set_default_animation(0)
    
    def fly(self):
        self.model.set_default_animation(5)
    
    def jump(self):
        self.jump_sound.play()
        self.model.play_animation(2)
    
        
    def draw(self, screen, game):
        surf = self.model.draw()
        if self.body.velocity.rotated(-1*self.game.player.gravity.angle - math.pi/2).x < -1*settings.FLIP_THRESHOLD:
            self.dir = -1
        elif self.body.velocity.rotated(-1*self.game.player.gravity.angle - math.pi/2).x > settings.FLIP_THRESHOLD:
            self.dir = 1
        if self.dir == -1:
            surf = pygame.transform.flip(surf, True, False)
        
        #diff = Vec2d(0,-1*surf.get_height() / 2.0 + 28)
        diff = Vec2d(0,-1*surf.get_height() / 2.0 + 58)
        diff = diff.rotated(-1*self.game.player.gravity.rotated(math.pi/2.0).angle)
        center = self.game.world2screen(self.body.position) + diff
        surf = pygame.transform.rotozoom(surf, self.game.player.gravity.rotated(math.pi/2.0).angle_degrees,1)
        
        rect = surf.get_rect()
        rect.center = center
        
        screen.blit(surf, rect.topleft)
        
        
