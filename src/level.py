import os
import pickle
import pymunk as pm
from pymunk import Vec2d


class line():
    def __init__(self,start,end,shape,prop=None):
        self.start=start
        self.end=end
        self.shape=shape
        self.prop=prop

class level_save():
    def __init__(self,level):
        self.lines=[]
        self.areas=level.areas
        self.enemies=level.enemies
        self.snaps=level.snaps

        for key in level.lines.iterkeys():
            line=level.lines[key]
            self.lines.append(((line.start[0],line.start[1]),(line.end[0],line.end[1]),line.prop))


class level():
    def __init__(self, loadfile=None):
        if loadfile==None:
            self.lines={}
            self.areas=[]
            self.enemies=[]
            self.snaps={}
            self.gvols={}
        else:
            self.load_level()
                
    def load_level(self,path):
        try:
            infile = open(path, 'rb')
            slevel = pickle.load(infile)
            self.lines={}
            self.areas=slevel.areas
            self.enemies=slevel.enemies
            self.snaps=slevel.snaps
            for line in slevel.lines:
                body = pm.Body(pm.inf, pm.inf)
                start=Vec2d(line[0])
                end=Vec2d(line[1])
                shape = pm.Segment(body, start, end, 5.0)
                self.add_line(start,end,shape,line[2])
        except:
            return level()

    def save_level(self,path):
        outfile = open(path,'wb')
        save=level_save(self)
        pickle.dump(save,outfile)

    def get_line(self, shape):
        return self.lines[shape]
        

    def add_or_inc(self,dict,v):
        if v in dict:
            dict[v]+=1
        else:
            dict[v]=1
    def add_line(self, start, end,shape,prop=None):
        self.lines[shape] = line(start, end, shape,prop)
        self.add_or_inc(self.snaps,(start[0],start[1]))
        self.add_or_inc(self.snaps,(end[0],end[1]))

    def add_gvol(self,vert_list,grav):
        print vert_list, grav

    def resnap(self):
        self.snaps={}
        for line in self.lines:
            self.add_or_inc(self.snaps,(start[0],start[1]))
            self.add_or_inc(self.snaps,(end[0],end[1]))
        
    def check_snap(self,u,r):
        for v in self.snaps.iterkeys():
            if (u[0]-v[0])**2 + (u[1]-v[1])**2 < r**2:
                return v



        

