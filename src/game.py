from settings import *
import pygame
from pymunk import Vec2d
import pymunk as pm
from pygame.locals import *
#from level import level

class game(object):

    def __init__(self):
        self.camera_pos = Vec2d(0,0)
        
        self.on_screen = []
        
        self.pan_left = False
        self.pan_right = False
        self.pan_up = False
        self.pan_down = False
        
        #PHYICS!!!!
        pm.init_pymunk()
        self.space = pm.Space()
        self.space.gravity = Vec2d(0.0, -900.0)
        
        #The screen to collide with what we need to draw
        self.screen_body = pm.Body(pm.inf, pm.inf)
        self.screen_shape = None
        self.set_screen_shape()
        self.space.add_collision_handler(COLLTYPE_SCREEN, COLLTYPE_DEFAULT, None, self.collide_screen, None, None)
    
        #self.level = 
        
    def set_screen_shape(self):
        if self.screen_shape:
            self.space.remove(self.screen_shape)
        pts = map(self.screen2world,[(0, 0), (WIDTH, 0), (WIDTH, HEIGHT), (0, HEIGHT)])
        self.screen_shape = pm.Poly(self.screen_body, pts)
        self.screen_shape.collision_type = COLLTYPE_SCREEN
        self.space.add(self.screen_shape)
        self.on_screen = []
        
    
    def collide_screen(self, space, arbiter):
        s1,s2 = arbiter.shapes
        self.on_screen.append(s2)

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
        time = clock.tick(60)/1000.0
        
        self.handel_input()
        if self.pan_left:
            self.camera_pos += Vec2d(-1 * PAN_SPEED, 0)
        if self.pan_right:
            self.camera_pos += Vec2d(PAN_SPEED, 0)
        if self.pan_up:
            self.camera_pos += Vec2d(0, PAN_SPEED)
        if self.pan_down:
            self.camera_pos += Vec2d(0, -1 * PAN_SPEED)
        
        self.physics(time)
        self.draw(screen)
        return 1
    
    def physics(self,time):
        self.set_screen_shape()
        self.space.step(time)
        
        
    
    def draw(self,screen):
        screen.fill((255,255,255))
        pygame.draw.circle(screen, (0,0,255) , self.world2screen(Vec2d(0,0)), 20, 2)
        pygame.display.flip()
        
