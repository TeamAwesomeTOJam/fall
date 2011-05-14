import pickle

class line():
    def __init__(self,start,end,prop=None):
        self.start=start
        self.end=end
        self.prop=prop

class level():
    def __init__(self):
        self.lines=[]
        self.areas=[]
        self.enemies=[]
    def add_line(self,start,end):
        self.lines.append(line(start,end))
        



        

