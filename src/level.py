import os
import pickle
import pymunk as pm
from pymunk import Vec2d
from settings import COLLTYPE_LETHAL


class line(object):
    
    def __init__(self, start, end, shape, lethal=False):
        self.start = start
        self.end = end
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


class level(object):
    
    def __init__(self):
        self.lines = {}
        self.areas = []
        self.enemies = []
        self.snaps = {}
        
    def __getstate__(self):
        lines = self.lines.values()
        return {'lines' : lines,
                'areas' : self.areas,
                'enemies' : self.enemies,
                'snaps' : self.snaps}
    
    def __setstate__(self, state):
        self.lines = {}
        for line in state['lines']:
            self.lines[line.shape] = line
        self.areas = state['areas']
        self.enemies = state['enemies']
        self.snaps = state['snaps']

    def save_level(self, path):
        outfile = open(path, 'wb')
        pickle.dump(self, outfile)

    def get_line(self, shape):
        return self.lines[shape]
        
    def add_or_inc(self,dict,v):
        if v in dict:
            dict[v]+=1
        else:
            dict[v]=1

    def add_line(self, line):
        self.lines[line.shape] = line
        self.add_or_inc(self.snaps, (line.start[0], line.start[1]))
        self.add_or_inc(self.snaps, (line.end[0], line.end[1]))

    def add_gvol(self,vert_list,grav):
        print vert_list, grav

    def resnap(self):
        self.snaps={}
        for line in self.lines:
            self.add_or_inc(self.snaps, (line.start[0], line.start[1]))
            self.add_or_inc(self.snaps, (line.end[0], line.end[1]))
        
    def check_snap(self,u,r):
        for v in self.snaps.iterkeys():
            if (u[0]-v[0])**2 + (u[1]-v[1])**2 < r**2:
                return v


def load_level(path):
    in_file = open(path, 'rb')
    return pickle.load(in_file)

