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
        repre = f"""joueur 1 : {self.score[0]} 
joueur 2 : {self.score[1]}
joueur courrant : {self.playerID}"""
        return repre
    def __str__(self):
        return grid(self.MState, label=True, size=3)
    def on_clic(self, row, col):
        playerID = self.playerID 
        if self(row, col)!=0 : return
        self(row, col, playerID)
        #--
        self.history.append((row, col))
        row0, col0 = self.history[-2] 
        self.switch(row0, col0, True) #règle voisinage           
        #--
        self.switch(row, col, False) #règle voisinage
        self.align(row, col, playerID) #check si alignement 5 pions
        self.capture(row, col, playerID) #check si capture pion adverse
        self.playerID=2-(1+self.playerID)%2 #change ID joueur courant
        
        
     
        
#==============================================================================


code=f"""
#--------__init__--------
p = GameDemo(7)
print(p)
p

#--------rules--------
p.on_clic(1,1); print(p)
p.on_clic(3,3); print(p)

#----switch----
p.on_clic(3,4); p.on_clic(3,3); print(p)

p = GameDemo(7)
#----align----
for i in range(4): p(i, 3, p.playerID)
print(p)
p

p.on_clic(4,3)
print(p)
p

#----capture----


"""
testcode(code)