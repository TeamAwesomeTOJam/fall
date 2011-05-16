import os
import pickle
import pygame
import pymunk as pm
from pymunk import Vec2d
from settings import *
from gravityvolume import *


class Line(object):
    
    def __init__(self, start, end, shape, lethal=False):
        self.start = (start[0], start[1])
        self.end = (end[0], end[1])
        self.shape = shape
        self.lethal = lethal
        if lethal:
            shape.collision_type = COLLTYPE_LETHAL
        
    def __getstate__(self):
        return {'start' : (self.start[0], self.start[1]),
                'end' : (self.end[0], self.end[1]),
                'lethal' : self.lethal
                }
    
    def __setstate__(self, state):
        self.start = state['start']
        self.end = state['end']
        self.lethal = state['lethal']
        self.shape = pm.Segment(pm.Body(pm.inf, pm.inf), self.start, self.end, 5.0)
        if self.lethal:
            self.shape.collision_type = COLLTYPE_LETHAL
            
    def draw(self, screen, game):
        if self.lethal:
            color = (255, 0, 0)
        else:
            color = (180, 180, 180)
        pygame.draw.line(screen, color, game.world2screen(self.start), game.world2screen(self.end), 10)


class Level(object):
    
    def __init__(self):
        self.goal = None
        self.lines = []
        self.gvols = []
        self.emitters = []
        self.coins = []
        self.snaps = {}

    def save_level(self, path):
        outfile = open(path, 'wb')
        pickle.dump(self, outfile)

    def dec_or_del(self,v,dict=None):
        if dict is None: dict=self.snaps
        if v in dict:
            dict[v]-=1
            if dict[v]<1:
                del dict[v]
        
    def add_or_inc(self,v,dict=None):
        if dict is None: dict=self.snaps
        if v in dict:
            dict[v]+=1
        else:
            dict[v]=1

    def add_line(self, line):
        self.lines.append(line)
        self.add_or_inc( (line.start[0], line.start[1]))
        self.add_or_inc((line.end[0], line.end[1]))

    def add_gvol(self, gvol):
        self.gvols.append(gvol)
        for m in gvol.vertices:
            self.add_or_inc((m[0],m[1]))
    
    def add_emitter(self, emitter):
        self.emitters.append(emitter)
        
    def add_coin(self, coin):
        self.coins.append(coin)
        
    def set_goal(self, goal):
        self.goal = goal

    def resnap(self):
        self.snaps={}
        for line in self.lines:
            self.add_or_inc((line.start[0], line.start[1]))
            self.add_or_inc((line.end[0], line.end[1]) )
        
    def check_snap(self,u,r):
        for v in self.snaps.iterkeys():
            if (u[0]-v[0])**2 + (u[1]-v[1])**2 < r**2:
                return v


def load_level(path):
    in_file = open(path, 'rb')
    return pickle.load(in_file)

