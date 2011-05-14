from settings import *
import pygame
from pymunk import Vec2d
import pymunk as pm
from pygame.locals import *
#from level import level

class game(object):

    def __init__(self):
        self.camera_pos = Vec2d(0,0)
        
        self.pan_left = False
        self.pan_right = False
        self.pan_up = False
        self.pan_down = False
        
        #PHYICS!!!!
        pm.init_pymunk()
        self.space = pm.Space()
        self.space.gravity = Vec2d(0.0, -900.0)
    
        #self.level = 

    def world2screen(self,v):
        x,y = v
        w = WIDTH
        h = HEIGHT
        rx = self.camera_pos.x
        ry = self.camera_pos.y
        return ((x-rx)+w/2,-1*(y-ry)+h/2)
        
    def screen2world(self,v):
        x,y = v
        w = WIDTH
        h = HEIGHT
        rx = self.camera_pos.x
        ry = self.camera_pos.y
        return Vec2d((x-w/2) + rx,-1*(y-h/2)+ry)
        
    
    def handel_input(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()
            elif e.type == pygame.KEYDOWN:
                if e.key == K_a:
                    self.pan_left = True
                elif e.key == K_d:
                    self.pan_right = True
                elif e.key == K_w:
                    self.pan_up = True
                elif e.key == K_s:
                    self.pan_down = True
            elif e.type == pygame.KEYUP:
                if e.key == K_a:
                    self.pan_left = False
                elif e.key == K_d:
                    self.pan_right = False
                elif e.key == K_w:
                    self.pan_up = False
                elif e.key == K_s:
                    self.pan_down = False

    def tick(self,screen,clock):
        self.handel_input()
        if self.pan_left:
            self.camera_pos += Vec2d(-1 * PAN_SPEED, 0)
        if self.pan_right:
            self.camera_pos += Vec2d(PAN_SPEED, 0)
        if self.pan_up:
            self.camera_pos += Vec2d(0, PAN_SPEED)
        if self.pan_down:
            self.camera_pos += Vec2d(0, -1 * PAN_SPEED)
        self.draw(screen)
        clock.tick(60)
        return 1
    
    def draw(self,screen):
        screen.fill((255,255,255))
        pygame.draw.circle(screen, (0,0,255) , self.world2screen(Vec2d(0,0)), 20, 2)
        pygame.display.flip()
        
