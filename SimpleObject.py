import math


class SimpleObject:
    
    def __init__(self, ipx, ipy, itheta, mag, tfactor):
        self.px = ipx
        self.py = ipy
        self.theta = itheta
        self.fFactor = mag
        self.tFactor = tfactor
        self.sensor = [-1, -1, -1, -1, -1] # 135, 120, 90, 60, 45
        
    def update(self):
        if (self.tFactor > 0): # turning left
            self.theta += 1
        if (self.tFactor < 0): #turning right
            self.theta -= 1
            
            
            
        if (self.fFactor > 0): # moving forwards
            self.py += self.fFactor * math.sin(self.theta)
            self.px += self.fFactor * math.cos(self.theta)
        if (self.fFactor < 0): # moving backwards
            self.py -= self.fFactor * math.sin(self.theta)
            self.px -= self.fFactor * math.sin(self.theta)

        
    
    def __str__(self):
        return f"(Currposex, Currposey): ( {self.px}"
    