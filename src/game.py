from settings import *
import os
import pygame
from pymunk import Vec2d
import pymunk as pm
from pygame.locals import *
from level import level
from player import Player
import pickle

class game(object):

    def __init__(self):
        self.camera_pos = Vec2d(0,0)
        
        self.on_screen = []
        self.player_collisions = []
        
        self.pan_left = False
        self.pan_right = False
        self.pan_up = False
        self.pan_down = False
        
        self.move_left = False
        self.move_right = False
        
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
        self.dec_snap_radius=0
        self.inc_snap_radius=0
        self.level_path=os.path.join(RES, 'level.pickle')
        self.level = level()
        
        #PHYICS!!!!
        pm.init_pymunk()
        self.space = pm.Space()
        self.space.gravity = Vec2d(0.0, -900.0)
        
        #the player
        self.player = Player(self)
        self.space.add(self.player.body, self.player.shape)
        
        #The screen to collide with what we need to draw
        self.screen_body = pm.Body(pm.inf, pm.inf)
        self.screen_shape = None
        self.set_screen_shape()
        
        self.space.add_collision_handler(COLLTYPE_SCREEN, COLLTYPE_DEFAULT, None, self.collide_screen, None, None)
        self.space.add_collision_handler(COLLTYPE_SCREEN, COLLTYPE_PLAYER, None, self.ignore_collision, None, None)
        self.space.add_collision_handler(COLLTYPE_DEFAULT, COLLTYPE_PLAYER, None, self.collect_player_collisions, None, None)
        
        
    
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
        return False
    
    def ignore_collision(self, space, arbiter):
        return False
    
    def collect_player_collisions(self, space, arbiter):
        for c in arbiter.contacts:
            self.player_collisions.append(c.position)
        return True
        


    def world2screen(self,v):
        x,y = v
        w = WIDTH
        h = HEIGHT
        rx = self.camera_pos.x
        ry = self.camera_pos.y
        return (int((x-rx)+w/2), int(-1*(y-ry)+h/2))
        
    def screen2world(self,v):
        x,y = v
        w = WIDTH
        h = HEIGHT
        rx = self.camera_pos.x
        ry = self.camera_pos.y
        return Vec2d((x-w/2) + rx,-1*(y-h/2)+ry)
    
    def load_level(self):
        try:
            infile = open(self.level_path, 'rb')
            level = pickle.load(infile)
            return level 
        except:
            return level()
    def save_level(self):
        outfile = open(self.level_path,'wb')
        pickle.dump(self.level,outfile)
        
    
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
                elif e.key == K_LEFT:
                    self.move_left = True
                elif e.key == K_RIGHT:
                    self.move_right = True
                elif e.key == K_COMMA and self.mode_edit:
                    self.dec_snap_radius= True
                elif e.key == K_PERIOD and self.mode_edit:
                    self.inc_snap_radius = True
                elif e.key == K_l and self.mode_edit:
                    self.load_level()
                elif e.key == K_k and self.mode_edit:
                    self.save_level()

            elif e.type == pygame.KEYUP:
                if e.key == K_a:
                    self.pan_left = False
                elif e.key == K_d:
                    self.pan_right = False
                elif e.key == K_w:
                    self.pan_up = False
                elif e.key == K_s:
                    self.pan_down = False
                elif e.key == K_LEFT:
                    self.move_left = False
                elif e.key == K_RIGHT:
                    self.move_right = False
                elif e.key == K_COMMA and self.mode_edit:
                    self.dec_snap_radius= False 
                elif e.key == K_PERIOD and self.mode_edit:
                    self.inc_snap_radius = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1 and self.mode_edit:
                    pos_snap=self.level.check_snap(self.screen2world(e.pos),self.snap_radius)
                    if pos_snap is not None:
                        self.pos_start=pos_snap
                    else:
                        self.pos_start=self.screen2world(e.pos)
            elif e.type == pygame.MOUSEBUTTONUP:
                if e.button == 1 and self.mode_edit:
                    pos_snap=self.level.check_snap(self.screen2world(e.pos),self.snap_radius)
                    if pos_snap is not None:
                        print pos_snap
                        self.pos_end=pos_snap
                    else:
                        self.pos_end=self.screen2world(e.pos)
        if self.mode_edit:
            self.pos_mouse=pygame.mouse.get_pos()
            if self.pos_mouse is not None: self.pos_mouse=self.screen2world(self.pos_mouse)


    def tick(self,screen,clock):
        time = clock.tick(60)/1000.0
        self.handle_input()

        if self.pan_left:
            self.camera_pos += Vec2d(-1 * PAN_SPEED, 0)
        if self.pan_right:
            self.camera_pos += Vec2d(PAN_SPEED, 0)
        if self.pan_up:
            self.camera_pos += Vec2d(0, PAN_SPEED)
        if self.pan_down:
            self.camera_pos += Vec2d(0, -1 * PAN_SPEED)
            
            
        #control the player
        speed = 0
        if self.move_left:
            speed -= PLAYER_SPEED
        if self.move_right:
            speed += PLAYER_SPEED
        
        self.player.body.velocity = Vec2d(speed, self.player.body.velocity[1])
            
        self.player.body.angle = 0
        self.player.body.angular_velocity = 0
        
        self.player.update(time)
        if self.mode_edit:
            if self.dec_snap_radius:
                self.snap_radius-=1
                if self.snap_radius<1: self.snap_radius=1
            if self.inc_snap_radius:
                self.snap_radius+=1
            if self.pos_start is not None and self.pos_end is not None:
                body = pm.Body(pm.inf, pm.inf)
                shape = pm.Segment(body, self.pos_start, self.pos_end, 5.0)
                shape.friction = 1.0
                self.space.add_static(shape)
                self.level.add_line(self.pos_start,self.pos_end,shape)
                self.pos_start = None
                self.pos_end= None

        self.physics(time)
        self.draw(screen)
        return 1
    
    def physics(self,time):
        self.set_screen_shape()
        self.player_collisions = []
        self.space.step(time)
    
    def draw(self,screen):
        screen.fill((255,255,255))

        #Draw the player
        r = self.player.shape.radius
        v = self.player.shape.body.position
        rot = self.player.shape.body.rotation_vector
        p = self.world2screen(v)
        p2 = Vec2d(rot.x, -rot.y) * r
        pygame.draw.circle(screen, (0,0,255), p, int(r), 2)
        pygame.draw.line(screen, (255,0,0), p, p+p2)
        pygame.draw.circle(screen, (0,0,255) , self.world2screen(Vec2d(0,0)), 20, 2)
        
        
        if self.mode_edit:
            pos_snap=self.level.check_snap(self.pos_mouse,self.snap_radius)
            if pos_snap is not None:
                pre_end=pos_snap
                pygame.draw.circle(screen, (255,0,0) , self.world2screen(pos_snap),self.snap_radius,1)
            else:
                pre_end=self.pos_mouse
            #Draw mouse drag
            if self.pos_start is not None and self.pos_mouse is not None:
                pygame.draw.line(screen, (0,0,0), self.world2screen(self.pos_start),self.world2screen(pre_end))
        #Draw other stuff
        for shape in self.on_screen:
            line = self.level.get_line(shape)
            pygame.draw.line(screen, (180,180,180), self.world2screen(line.start),self.world2screen(line.end),10)

        pygame.display.flip()
        
