# -*- coding: utf-8 -*-
"""
Created on Fri Jan  7 16:25:16 2022

@author: geeka
"""

from PenteZ import Game
from ezCLI import grid, testcode 

#==============TEST CODE FOR kernel class Game ==============
class GameDemo(Game):
    """demonstration class for Game class. Add methode for test of Game code"""
    def __repr__(self):
        repre = f"joueur 1 : {self.score[0]} | joueur 2 : {self.score[1]} | joueur courrant : {self.playerID}"
        return repre
    def __str__(self):
        return grid(self.MState, label=True, size=3)
    def on_clic(self, row, col):
        playerID = self.playerID 
        if self(row, col)!=0 : return
        self(row, col, playerID)
        #--voisinage
        self.history.append((row, col))
        row0, col0 = self.history[-2] 
        self.switch(row0, col0, True) #règle voisinage           
        self.switch(row, col, False) 
        #--règles points
        self.align(row, col, playerID) #check si alignement 5 pions
        self.capture(row, col, playerID) #check si capture pion adverse
        #--joueur suivant
        self.playerID=2-(1+self.playerID)%2 #change ID joueur courant
        
        
     
        
#==============================================================================

MtestAlign=[
      [1,0,0,0,0,0,0],
      [2,1,1,1,0,1,0],
      [2,1,0,0,1,2,0],
      [2,1,0,1,0,2,0],
      [2,1,1,0,1,2,0],
      [0,0,0,0,0,2,0],
      [0,0,2,2,2,0,2]
    ]
MtestCapture=[
    [2,0,0,0,0,0,0],
    [0,1,0,0,0,0,0],
    [0,0,1,0,1,0,0],
    [0,0,0,B,0,0,0],
    [0,0,2,0,0,0,0],
    [2,A,1,B,0,0,0],
    [0,0,0,0,0,0,0],
    ]

code=f"""
#--------__init__--------
p = GameDemo(7)
print(p)
p

#--------rules--------
p.on_clic(1,1); print(p)

p.on_clic(3,3); print(p)

#----switch----
p.on_clic(3,4); p.on_clic(3,3)
print(p)
print(p.history)

#----align----
p = GameDemo(7)
p.MState=MtestAlign
print(p)

p.on_clic(5,0) #vertical
print(p)
p

p.on_clic(1,4) #horizontal
print(p)
p

p.on_clic(6,5) #double
print(p)
p

p.on_clic(0,6) #diagonal up
print(p)
p

p.on_clic(6,0) #vertical again
print(p)
p

p.on_clic(2,2) #diagonal down
print(p)
p

#----capture----



"""
testcode(code)