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
        
    def add_line(self, start, end,shape):
        self.lines[shape] = line(start, end, shape)
    
    def get_line(self, shape):
        return self.lines[shape]
        



        

