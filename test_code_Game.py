# -*- coding: utf-8 -*-
"""
Created on Fri Jan  7 16:25:16 2022

@author: geeka
"""

from PenteZ import Game
from ezCLI import grid, testcode 

#==============TEST CODE FOR kernel class Game ================================
class GameDemo(Game):
    """demonstration class for Game class. Added few methodes for test of Game code"""
    def __repr__(self):
        """give main information about current game"""
        repre = f"joueur 1 : {self.score[0]} | joueur 2 : {self.score[1]} | joueur courrant : {self.playerID}"
        return repre
    #--------------------------------------------------------------------------
    def __str__(self):
        """representation of the grid with ezCLI.grid"""
        return grid(self.MState, label=True, size=3)
    #--------------------------------------------------------------------------
    def on_clic(self, row, col):
        """simulation of player click"""
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
#matrice "jouets" préremplies pour les tests
MtestAlign=[
      [1,0,0,0,0,0,0],
      [2,1,1,1,0,1,0],
      [2,1,0,0,1,2,0],
      [2,1,0,1,0,2,0],
      [2,1,1,0,1,2,0],
      [0,0,0,0,0,2,0],
      [0,0,2,2,2,0,2]
    ]
B=A=0
MtestCapture=[
    [2,0,0,1,2,B,1],
    [0,1,0,0,0,0,0],
    [0,0,1,0,1,0,0],
    [0,0,0,B,0,0,1],
    [0,0,2,0,0,0,2],
    [2,A,1,B,0,0,2],
    [0,0,0,1,2,2,A],
    ]

code=f"""
#--------__init__--------
p = GameDemo(7) #instance de GameDemo
print(p) #test de __str__
p #test de __call__

#---------__call__--------
print(p(6,0))
p(6,0,2) #modification de la valeur en 6,0
print(p, p(6,0))

#--------rules--------
#----switch----
p.on_clic(1,1); print(p) #mise en évidence de l'application de switch

p.on_clic(3,3); print(p) #l'ancien voisinage est bien effacé

p.on_clic(3,4); p.on_clic(3,3) #on ne peut pas modifier un state = 3
print(p)

print(p.history) # l'hystorique des points est bien mis à jour

#----align----
p = GameDemo(7) #nouvel objet pour la suite des tests
p.MState=MtestAlign #utilisation de la matrice pré-remplie
print(p)

p.on_clic(5,0) #alignement vertical
print(p)
p

p.on_clic(1,4) #alignement horizontal
print(p)
p

p.on_clic(6,5) #double, on peut bien réaliser deux alignements en même temps
print(p)
p

p.on_clic(0,6) #diagonal montante vers la droite
print(p)
p

p.on_clic(6,0) #réutilisation d'un alignement déjà utilisé
print(p)
p

p.on_clic(2,2) #diagonal descendante vers la droite
print(p)
p

#----capture----
p = GameDemo(7)
p.MState=MtestCapture
print(p)

p.on_clic(3,3) #diagonal descendante
print(p)
p

p.on_clic(5,1) #diagonal monte
print(p)
p

p.on_clic(5,3) #horizontal
print(p)
p

p.on_clic(6,6) #vertical (double)
print(p)
p

p.on_clic(0,5) #un joueur de peut pas s'auto-capturer entre deux pions de l'adversaire
print(p)
p
"""
testcode(code)