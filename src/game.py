from settings import *
import pygame
from pymunk import Vec2d
import pymunk as pm
from pygame.locals import *
from level import level

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

        #Editor events
        self.mode_edit=True
        self.pos_start=None
        self.pos_end=None
        self.pos_mouse=None
        self.snap_radius=5.0
        self.level = level()

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
        
    
    def handle_input(self):
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
                elif e.key == K_COMMA and self.mode_edit:
                    self.dec_snap_radius= True
                elif e.key == K_PERIOD and self.mode_edit:
                    self.inc_snap_radius = True
            elif e.type == pygame.KEYUP:
                if e.key == K_a:
                    self.pan_left = False
                elif e.key == K_d:
                    self.pan_right = False
                elif e.key == K_w:
                    self.pan_up = False
                elif e.key == K_s:
                    self.pan_down = False
                elif e.key == K_COMMA and self.mode_edit:
                    self.dec_snap_radius= False 
                elif e.key == K_PERIOD and self.mode_edit:
                    self.inc_snap_radius = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1 and self.mode_edit:
                    self.pos_start=self.screen2world(e.pos)
            elif e.type == pygame.MOUSEBUTTONUP:
                if e.button == 1 and self.mode_edit:
                    self.pos_end=self.screen2world(e.pos)
        if self.mode_edit:
            self.pos_mouse=pygame.mouse.get_pos()
            if self.pos_mouse is not None: self.pos_mouse=self.screen2world(self.pos_mouse)


    def tick(self,screen,clock):
        self.handle_input()
        if self.pan_left:
            self.camera_pos += Vec2d(-1 * PAN_SPEED, 0)
        if self.pan_right:
            self.camera_pos += Vec2d(PAN_SPEED, 0)
        if self.pan_up:
            self.camera_pos += Vec2d(0, PAN_SPEED)
        if self.pan_down:
            self.camera_pos += Vec2d(0, -1 * PAN_SPEED)
        if self.dec_snap_radius:
            self.snap_radius-=1
            if self.snap_radius<0: self.snap_radius=0
        if self.inc_snap_radius:
            self.snap_radius+=1
        if self.pos_start is not None and self.pos_end is not None:
            self.level.add_line(self.pos_start,self.pos_end)
            self.pos_start = None
            self.pos_end= None

        self.draw(screen)
        clock.tick(60)
        return 1
    
    def draw(self,screen):
        screen.fill((255,255,255))
        pygame.draw.circle(screen, (0,0,255) , self.world2screen(Vec2d(0,0)), 20, 2)
        #Draw mouse drag
        if self.pos_start is not None and self.pos_mouse is not None:
            pygame.draw.line(screen, (180,180,180), self.world2screen(self.pos_start),self.world2screen(self.pos_mouse))
        #Draw other stuff
        for line in self.level.lines:
            pygame.draw.line(screen, (180,180,180), self.world2screen(line[0]),self.world2screen(line[1]))

        pygame.display.flip()
        
