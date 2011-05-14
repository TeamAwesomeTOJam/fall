import pickle

class line():
    def __init__(self,start,end,shape,prop=None):
        self.start=start
        self.end=end
        self.prop=prop

class level():
    def __init__(self):
        self.lines={}
        self.areas=[]
        self.enemies=[]
        self.snaps={}

    def get_line(self, shape):
        return self.lines[shape]
        

    def add_or_inc(self,dict,v):
        if v in dict:
            dict[v]+=1
        else:
            dict[v]=1
    def add_line(self, start, end,shape):
        self.lines[shape] = line(start, end, shape)
        self.add_or_inc(self.snaps,(start[0],start[1]))
        self.add_or_inc(self.snaps,(end[0],end[1]))

    def resnap(self):
        self.snaps={}
        for line in self.lines:
            self.add_or_inc(self.snaps,(start[0],start[1]))
            self.add_or_inc(self.snaps,(end[0],end[1]))
        
    def check_snap(self,u,r):
        for v in self.snaps.iterkeys():
            if (u[0]-v[0])**2 + (u[1]-v[1])**2 < r**2:
                return v



        

